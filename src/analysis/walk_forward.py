from __future__ import annotations

from dataclasses import replace
from itertools import product
from math import inf

from src.analysis.metrics import summarize_backtest
from src.backtest.engine import run_backtest
from src.backtest.models import (
    BacktestConfig,
    Candle,
    WalkForwardCandidateResult,
    WalkForwardReport,
    WalkForwardWindowResult,
)
from src.strategy.registry import get_strategy


def _parameter_snapshot(config: BacktestConfig) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "short_ma_period": config.strategy.short_ma_period,
        "long_ma_period": config.strategy.long_ma_period,
        "allow_reversal": config.strategy.allow_reversal,
    }
    for key, value in sorted(config.strategy.parameters.items()):
        snapshot[f"parameters.{key}"] = value
    return snapshot


def _current_parameter_value(config: BacktestConfig, key: str) -> object:
    if key == "short_ma_period":
        return config.strategy.short_ma_period
    if key == "long_ma_period":
        return config.strategy.long_ma_period
    if key == "allow_reversal":
        return config.strategy.allow_reversal
    if key.startswith("parameters."):
        parameter_key = key.split(".", 1)[1]
        return config.strategy.parameters.get(parameter_key)
    raise ValueError(f"Unsupported walk-forward search key: {key}")


def _expand_compact_numeric_range(spec: dict[str, object]) -> list[object]:
    start = spec.get("start")
    stop = spec.get("stop")
    step = spec.get("step", 1)
    if not isinstance(start, (int, float)) or not isinstance(stop, (int, float)) or not isinstance(step, (int, float)):
        raise ValueError("Range-based walk_forward.search_space specs require numeric start/stop/step.")
    if step == 0:
        raise ValueError("Range-based walk_forward.search_space specs require a non-zero step.")

    values: list[object] = []
    current = float(start)
    comparator = (lambda value: value <= float(stop) + 1e-12) if step > 0 else (lambda value: value >= float(stop) - 1e-12)
    while comparator(current):
        if isinstance(start, int) and isinstance(stop, int) and isinstance(step, int):
            values.append(int(round(current)))
        else:
            values.append(round(current, 10))
        current += float(step)
    if not values:
        raise ValueError("Range-based walk_forward.search_space spec produced no values.")
    return values


def _expand_current_centered_range(config: BacktestConfig, key: str, spec: dict[str, object]) -> list[object]:
    current_value = _current_parameter_value(config, key)
    if not isinstance(current_value, (int, float)):
        raise ValueError(f"Current-centered walk_forward.search_space for '{key}' requires a numeric current value.")

    radius = spec.get("radius", 1)
    step = spec.get("step", 1)
    minimum = spec.get("minimum")
    maximum = spec.get("maximum")
    if not isinstance(radius, (int, float)) or radius < 0:
        raise ValueError(f"'walk_forward.search_space.{key}.radius' must be a non-negative number.")
    if not isinstance(step, (int, float)) or step <= 0:
        raise ValueError(f"'walk_forward.search_space.{key}.step' must be a positive number.")
    if minimum is not None and not isinstance(minimum, (int, float)):
        raise ValueError(f"'walk_forward.search_space.{key}.minimum' must be numeric when provided.")
    if maximum is not None and not isinstance(maximum, (int, float)):
        raise ValueError(f"'walk_forward.search_space.{key}.maximum' must be numeric when provided.")

    start = float(current_value) - float(radius)
    stop = float(current_value) + float(radius)
    values: list[object] = []
    current = start
    while current <= stop + 1e-12:
        candidate = round(current, 10)
        if isinstance(current_value, int) and isinstance(radius, int) and isinstance(step, int):
            candidate = int(round(candidate))
        if minimum is not None and candidate < minimum:
            current += float(step)
            continue
        if maximum is not None and candidate > maximum:
            current += float(step)
            continue
        values.append(candidate)
        current += float(step)
    if not values:
        raise ValueError(f"Current-centered walk_forward.search_space for '{key}' produced no values.")
    return values


def _expand_search_values(config: BacktestConfig, key: str, raw_spec: object) -> list[object]:
    if isinstance(raw_spec, list):
        return raw_spec
    if not isinstance(raw_spec, dict):
        raise ValueError(f"walk_forward.search_space for '{key}' must be a list or object.")
    if "values" in raw_spec:
        raw_values = raw_spec["values"]
        if not isinstance(raw_values, list) or not raw_values:
            raise ValueError(f"'walk_forward.search_space.{key}.values' must be a non-empty list.")
        return raw_values
    if raw_spec.get("around_current") is True:
        return _expand_current_centered_range(config, key, raw_spec)
    if {"start", "stop"}.issubset(raw_spec):
        return _expand_compact_numeric_range(raw_spec)
    raise ValueError(
        f"walk_forward.search_space for '{key}' must use a list, a values list, a start/stop range, or around_current."
    )


def _build_candidate_config(config: BacktestConfig, parameter_values: dict[str, object]) -> BacktestConfig | None:
    strategy_kwargs = {
        "name": config.strategy.name,
        "short_ma_period": config.strategy.short_ma_period,
        "long_ma_period": config.strategy.long_ma_period,
        "allow_reversal": config.strategy.allow_reversal,
        "parameters": dict(config.strategy.parameters),
    }

    for key, value in parameter_values.items():
        if key == "short_ma_period":
            if not isinstance(value, int) or value < 1:
                return None
            strategy_kwargs["short_ma_period"] = value
        elif key == "long_ma_period":
            if not isinstance(value, int) or value < 2:
                return None
            strategy_kwargs["long_ma_period"] = value
        elif key == "allow_reversal":
            if not isinstance(value, bool):
                return None
            strategy_kwargs["allow_reversal"] = value
        elif key.startswith("parameters."):
            parameter_key = key.split(".", 1)[1]
            strategy_kwargs["parameters"][parameter_key] = value
        else:
            return None

    if (
        config.strategy.name == "moving_average_cross"
        and strategy_kwargs["short_ma_period"] >= strategy_kwargs["long_ma_period"]
    ):
        return None

    return replace(config, strategy=replace(config.strategy, **strategy_kwargs))


def _generate_candidate_configs(config: BacktestConfig) -> list[tuple[dict[str, object], BacktestConfig]]:
    search_space = config.walk_forward.search_space
    if not search_space:
        return [(_parameter_snapshot(config), config)]

    expanded_search_space = {
        key: _expand_search_values(config, key, raw_spec)
        for key, raw_spec in search_space.items()
    }

    candidate_configs: list[tuple[dict[str, object], BacktestConfig]] = []
    keys = sorted(expanded_search_space)
    seen_parameter_sets: set[tuple[tuple[str, object], ...]] = set()
    for values in product(*(expanded_search_space[key] for key in keys)):
        parameter_values = dict(zip(keys, values, strict=True))
        candidate_config = _build_candidate_config(config, parameter_values)
        if candidate_config is None:
            continue
        snapshot = _parameter_snapshot(candidate_config)
        snapshot_key = tuple(sorted(snapshot.items()))
        if snapshot_key in seen_parameter_sets:
            continue
        seen_parameter_sets.add(snapshot_key)
        candidate_configs.append((snapshot, candidate_config))

    if not candidate_configs:
        raise ValueError("Walk-forward search_space did not produce any valid candidate configs.")
    return candidate_configs


def _selection_metric_value(summary, metric: str) -> float:
    if metric == "total_pnl":
        return summary.total_pnl
    if metric == "profit_factor":
        return summary.profit_factor if summary.profit_factor != inf else 1_000_000.0
    if metric == "win_rate":
        return summary.win_rate
    raise ValueError(f"Unsupported selection metric: {metric}")


def _score_summary(summary, metric: str) -> tuple[float, ...]:
    metric_value = _selection_metric_value(summary, metric)
    return (
        0.0 if summary.stopped_early else 1.0,
        1.0 if summary.trade_count > 0 else 0.0,
        metric_value,
        summary.total_pnl,
        summary.win_rate,
        -summary.max_drawdown,
        float(summary.trade_count),
    )


def run_walk_forward_validation(
    candles: list[Candle],
    config: BacktestConfig,
    *,
    symbol: str | None = None,
) -> WalkForwardReport:
    training_bars = config.walk_forward.training_bars
    test_bars = config.walk_forward.test_bars
    step_bars = config.walk_forward.step_bars
    minimum_test_trades = config.walk_forward.minimum_test_trades
    selection_metric = config.walk_forward.selection_metric

    if len(candles) < training_bars + test_bars:
        raise ValueError("Not enough candles to run walk-forward validation.")

    candidate_configs = [
        (parameter_snapshot, candidate_config)
        for parameter_snapshot, candidate_config in _generate_candidate_configs(config)
        if get_strategy(candidate_config.strategy.name).minimum_candles(candidate_config)
        <= min(training_bars, test_bars)
    ]
    if not candidate_configs:
        raise ValueError("No walk-forward candidates fit inside the configured training/test window sizes.")

    windows: list[WalkForwardWindowResult] = []
    cursor = training_bars
    window_index = 0

    while cursor + test_bars <= len(candles):
        training = candles[cursor - training_bars : cursor]
        testing = candles[cursor : cursor + test_bars]

        evaluated_candidates: list[tuple[tuple[float, ...], dict[str, object], BacktestConfig, object]] = []
        for parameter_snapshot, candidate_config in candidate_configs:
            training_result = run_backtest(training, candidate_config)
            training_summary = summarize_backtest(training_result)
            score = _score_summary(training_summary, selection_metric)
            evaluated_candidates.append((score, parameter_snapshot, candidate_config, training_summary))

        evaluated_candidates.sort(key=lambda item: item[0], reverse=True)
        best_score, best_candidate_parameters, best_candidate_config, best_training_summary = evaluated_candidates[0]

        testing_result = run_backtest(testing, best_candidate_config)
        testing_summary = summarize_backtest(testing_result)

        fail_reasons: list[str] = []
        if testing_summary.trade_count < minimum_test_trades:
            fail_reasons.append("too_few_test_trades")
        if config.risk.max_drawdown is not None and testing_summary.max_drawdown > config.risk.max_drawdown:
            fail_reasons.append("max_drawdown_exceeded")
        if testing_summary.stopped_early:
            fail_reasons.append("stopped_early")

        top_training_candidates = [
            WalkForwardCandidateResult(
                rank=rank,
                parameters=parameter_snapshot,
                selection_metric_value=_selection_metric_value(training_summary, selection_metric),
                training_summary=training_summary,
            )
            for rank, (_, parameter_snapshot, _, training_summary) in enumerate(
                evaluated_candidates[: config.walk_forward.top_candidates_per_window],
                start=1,
            )
        ]

        windows.append(
            WalkForwardWindowResult(
                window_index=window_index,
                training_start=training[0].timestamp,
                training_end=training[-1].timestamp,
                testing_start=testing[0].timestamp,
                testing_end=testing[-1].timestamp,
                candidate_count=len(candidate_configs),
                selected_parameters=best_candidate_parameters,
                top_training_candidates=top_training_candidates,
                training_summary=best_training_summary,
                testing_summary=testing_summary,
                passed=not fail_reasons,
                fail_reasons=fail_reasons,
            )
        )

        window_index += 1
        cursor += step_bars

    passing_windows = sum(1 for window in windows if window.passed)
    total_windows = len(windows)
    return WalkForwardReport(
        symbol=symbol,
        strategy_name=config.strategy.name,
        training_bars=training_bars,
        test_bars=test_bars,
        step_bars=step_bars,
        selection_metric=selection_metric,
        search_enabled=bool(config.walk_forward.search_space),
        total_windows=total_windows,
        passing_windows=passing_windows,
        pass_rate=(passing_windows / total_windows) if total_windows else 0.0,
        windows=windows,
    )
