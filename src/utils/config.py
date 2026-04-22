from __future__ import annotations

import json
from pathlib import Path

from src.backtest.models import BacktestConfig, DataSource, OutputConfig, RiskConfig, StrategyConfig, WalkForwardConfig
from src.utils.errors import ConfigurationError


def _require_mapping(payload: object, name: str) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ConfigurationError(f"'{name}' must be an object.")
    return payload


def _require_bool(payload: dict[str, object], key: str) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise ConfigurationError(f"'{key}' must be a boolean.")
    return value


def _require_int(payload: dict[str, object], key: str, *, minimum: int | None = None) -> int:
    value = payload.get(key)
    if not isinstance(value, int):
        raise ConfigurationError(f"'{key}' must be an integer.")
    if minimum is not None and value < minimum:
        raise ConfigurationError(f"'{key}' must be >= {minimum}.")
    return value


def _optional_int(
    payload: dict[str, object],
    key: str,
    *,
    default: int,
    minimum: int | None = None,
) -> int:
    if key not in payload:
        value = default
    else:
        value = payload.get(key)
        if not isinstance(value, int):
            raise ConfigurationError(f"'{key}' must be an integer.")
    if minimum is not None and value < minimum:
        raise ConfigurationError(f"'{key}' must be >= {minimum}.")
    return value


def _require_float(
    payload: dict[str, object],
    key: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    value = payload.get(key)
    if not isinstance(value, (int, float)):
        raise ConfigurationError(f"'{key}' must be a number.")
    numeric_value = float(value)
    if minimum is not None and numeric_value < minimum:
        raise ConfigurationError(f"'{key}' must be >= {minimum}.")
    if maximum is not None and numeric_value > maximum:
        raise ConfigurationError(f"'{key}' must be <= {maximum}.")
    return numeric_value


def _load_data_sources(data: dict[str, object], primary_data_file: str) -> list[DataSource]:
    raw_sources = data.get("sources")
    if raw_sources is None:
        return [DataSource(symbol=Path(primary_data_file).stem.upper(), file_path=Path(primary_data_file))]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ConfigurationError("'data.sources' must be a non-empty list when provided.")

    sources: list[DataSource] = []
    for index, item in enumerate(raw_sources):
        if not isinstance(item, dict):
            raise ConfigurationError(f"'data.sources[{index}]' must be an object.")
        symbol = item.get("symbol")
        file_path = item.get("file_path")
        if not isinstance(symbol, str) or not symbol.strip():
            raise ConfigurationError(f"'data.sources[{index}].symbol' must be a non-empty string.")
        if not isinstance(file_path, str) or not file_path.strip():
            raise ConfigurationError(f"'data.sources[{index}].file_path' must be a non-empty string.")
        sources.append(DataSource(symbol=symbol.strip(), file_path=Path(file_path)))
    return sources


def _load_walk_forward_config(root: dict[str, object]) -> WalkForwardConfig:
    raw_walk_forward = root.get("walk_forward", {})
    walk_forward = _require_mapping(raw_walk_forward, "walk_forward")
    selection_metric = walk_forward.get("selection_metric", "total_pnl")
    if not isinstance(selection_metric, str) or selection_metric not in {"total_pnl", "profit_factor", "win_rate"}:
        raise ConfigurationError("'walk_forward.selection_metric' must be one of: total_pnl, profit_factor, win_rate.")

    raw_search_space = walk_forward.get("search_space", {})
    search_space_payload = _require_mapping(raw_search_space, "walk_forward.search_space")
    search_space: dict[str, object] = {}
    for key, raw_values in search_space_payload.items():
        if not isinstance(key, str) or not key.strip():
            raise ConfigurationError("Keys in 'walk_forward.search_space' must be non-empty strings.")
        if isinstance(raw_values, list):
            if not raw_values:
                raise ConfigurationError(f"'walk_forward.search_space.{key}' must be a non-empty list.")
        elif isinstance(raw_values, dict):
            if not raw_values:
                raise ConfigurationError(f"'walk_forward.search_space.{key}' mapping must not be empty.")
        else:
            raise ConfigurationError(
                f"'walk_forward.search_space.{key}' must be a list or an object describing a generated range."
            )
        search_space[key] = raw_values

    return WalkForwardConfig(
        training_bars=_optional_int(walk_forward, "training_bars", default=12, minimum=2),
        test_bars=_optional_int(walk_forward, "test_bars", default=6, minimum=1),
        step_bars=_optional_int(walk_forward, "step_bars", default=6, minimum=1),
        minimum_test_trades=_optional_int(walk_forward, "minimum_test_trades", default=1, minimum=0),
        selection_metric=selection_metric,
        search_space=search_space,
        top_candidates_per_window=_optional_int(walk_forward, "top_candidates_per_window", default=3, minimum=1),
    )


def load_backtest_config(path: str | Path) -> BacktestConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigurationError(f"Config file not found: {config_path}")

    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ConfigurationError(f"Invalid JSON config: {error}") from error

    root = _require_mapping(payload, "config")
    data = _require_mapping(root.get("data"), "data")
    strategy = _require_mapping(root.get("strategy"), "strategy")
    risk = _require_mapping(root.get("risk"), "risk")
    output = _require_mapping(root.get("output"), "output")
    walk_forward_config = _load_walk_forward_config(root)

    data_file = data.get("file_path")
    if not isinstance(data_file, str) or not data_file.strip():
        raise ConfigurationError("'data.file_path' must be a non-empty string.")
    data_sources = _load_data_sources(data, data_file)

    strategy_name = strategy.get("name", "moving_average_cross")
    if not isinstance(strategy_name, str):
        raise ConfigurationError("'strategy.name' must be a string.")

    strategy_config = StrategyConfig(
        name=strategy_name,
        short_ma_period=_optional_int(strategy, "short_ma_period", default=3, minimum=1),
        long_ma_period=_optional_int(strategy, "long_ma_period", default=5, minimum=2),
        allow_reversal=_require_bool(strategy, "allow_reversal"),
        parameters=_require_mapping(strategy.get("parameters", {}), "strategy.parameters"),
    )
    if not strategy_config.name.strip():
        raise ConfigurationError("'strategy.name' must be a non-empty string.")
    if strategy_config.name == "moving_average_cross" and strategy_config.short_ma_period >= strategy_config.long_ma_period:
        raise ConfigurationError("'short_ma_period' must be smaller than 'long_ma_period'.")

    max_consecutive_losses = risk.get("max_consecutive_losses")
    if max_consecutive_losses is not None:
        if not isinstance(max_consecutive_losses, int) or max_consecutive_losses < 1:
            raise ConfigurationError("'max_consecutive_losses' must be null or an integer >= 1.")

    max_drawdown = risk.get("max_drawdown")
    if max_drawdown is not None:
        if not isinstance(max_drawdown, (int, float)) or not 0.0 < float(max_drawdown) <= 1.0:
            raise ConfigurationError("'max_drawdown' must be null or a number between 0 and 1.")

    risk_config = RiskConfig(
        stop_loss=_require_float(risk, "stop_loss", minimum=0.0),
        take_profit=_require_float(risk, "take_profit", minimum=0.0),
        spread=_require_float(risk, "spread", minimum=0.0),
        commission=_require_float(risk, "commission", minimum=0.0),
        initial_capital=_require_float(risk, "initial_capital", minimum=0.01),
        risk_per_trade=_require_float(risk, "risk_per_trade", minimum=0.0, maximum=1.0),
        max_consecutive_losses=max_consecutive_losses,
        max_drawdown=float(max_drawdown) if max_drawdown is not None else None,
    )
    if risk_config.stop_loss <= 0.0:
        raise ConfigurationError("'stop_loss' must be greater than 0.")
    if risk_config.take_profit <= 0.0:
        raise ConfigurationError("'take_profit' must be greater than 0.")
    if risk_config.risk_per_trade <= 0.0:
        raise ConfigurationError("'risk_per_trade' must be greater than 0.")

    output_directory = output.get("directory", "output")
    trades_file = output.get("trades_file", "trades.csv")
    summary_file = output.get("summary_file", "summary.json")
    equity_curve_file = output.get("equity_curve_file", "equity_curve.csv")
    signal_snapshot_file = output.get("signal_snapshot_file", "signal_snapshot.json")
    signal_history_file = output.get("signal_history_file", "signal_history.csv")
    papertrade_state_file = output.get("papertrade_state_file", "papertrade_state.json")
    papertrade_journal_file = output.get("papertrade_journal_file", "papertrade_journal.jsonl")
    notifications_file = output.get("notifications_file", "notifications.jsonl")
    scan_summary_file = output.get("scan_summary_file", "scan_summary.json")
    period_summary_csv_file = output.get("period_summary_csv_file", "period_summary.csv")
    period_summary_json_file = output.get("period_summary_json_file", "period_summary.json")
    walk_forward_summary_file = output.get("walk_forward_summary_file", "walk_forward_summary.json")
    compare_summary_file = output.get("compare_summary_file", "compare_summary.json")
    if not isinstance(output_directory, str) or not output_directory.strip():
        raise ConfigurationError("'output.directory' must be a non-empty string.")
    if not isinstance(trades_file, str) or not trades_file.strip():
        raise ConfigurationError("'output.trades_file' must be a non-empty string.")
    if not isinstance(summary_file, str) or not summary_file.strip():
        raise ConfigurationError("'output.summary_file' must be a non-empty string.")
    if not isinstance(equity_curve_file, str) or not equity_curve_file.strip():
        raise ConfigurationError("'output.equity_curve_file' must be a non-empty string.")
    if not isinstance(signal_snapshot_file, str) or not signal_snapshot_file.strip():
        raise ConfigurationError("'output.signal_snapshot_file' must be a non-empty string.")
    if not isinstance(signal_history_file, str) or not signal_history_file.strip():
        raise ConfigurationError("'output.signal_history_file' must be a non-empty string.")
    if not isinstance(papertrade_state_file, str) or not papertrade_state_file.strip():
        raise ConfigurationError("'output.papertrade_state_file' must be a non-empty string.")
    if not isinstance(papertrade_journal_file, str) or not papertrade_journal_file.strip():
        raise ConfigurationError("'output.papertrade_journal_file' must be a non-empty string.")
    if not isinstance(notifications_file, str) or not notifications_file.strip():
        raise ConfigurationError("'output.notifications_file' must be a non-empty string.")
    if not isinstance(scan_summary_file, str) or not scan_summary_file.strip():
        raise ConfigurationError("'output.scan_summary_file' must be a non-empty string.")
    if not isinstance(period_summary_csv_file, str) or not period_summary_csv_file.strip():
        raise ConfigurationError("'output.period_summary_csv_file' must be a non-empty string.")
    if not isinstance(period_summary_json_file, str) or not period_summary_json_file.strip():
        raise ConfigurationError("'output.period_summary_json_file' must be a non-empty string.")
    if not isinstance(walk_forward_summary_file, str) or not walk_forward_summary_file.strip():
        raise ConfigurationError("'output.walk_forward_summary_file' must be a non-empty string.")
    if not isinstance(compare_summary_file, str) or not compare_summary_file.strip():
        raise ConfigurationError("'output.compare_summary_file' must be a non-empty string.")

    return BacktestConfig(
        data_file=Path(data_file),
        strategy=strategy_config,
        risk=risk_config,
        output=OutputConfig(
            directory=Path(output_directory),
            trades_file=trades_file,
            summary_file=summary_file,
            equity_curve_file=equity_curve_file,
            signal_snapshot_file=signal_snapshot_file,
            signal_history_file=signal_history_file,
            papertrade_state_file=papertrade_state_file,
            papertrade_journal_file=papertrade_journal_file,
            notifications_file=notifications_file,
            scan_summary_file=scan_summary_file,
            period_summary_csv_file=period_summary_csv_file,
            period_summary_json_file=period_summary_json_file,
            walk_forward_summary_file=walk_forward_summary_file,
            compare_summary_file=compare_summary_file,
        ),
        data_sources=data_sources,
        walk_forward=walk_forward_config,
    )
