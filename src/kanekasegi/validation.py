from __future__ import annotations

import argparse
import json
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from .config import AppConfig, load_config
from .observability import summarize_trade_records, write_walk_forward_review
from .portfolio_lab import simulate_portfolio
from .research import _load_candles, _load_external_factors, _score_result, _select_candidates
from .rule_lab import RuleCandidate, RuleLabResult, run_rule_lab
from .runtime_env import load_dotenv
from .types import MarketCandle


def _month_key(candle: MarketCandle) -> str:
    if candle.trading_day:
        return candle.trading_day[:7]
    return candle.timestamp.strftime("%Y-%m")


def _ordered_months(candles: list[MarketCandle]) -> list[str]:
    return sorted({_month_key(candle) for candle in candles})


def _ordered_months_by_timeframe(candles_by_timeframe: dict[str, list[MarketCandle]]) -> list[str]:
    months: set[str] = set()
    for candles in candles_by_timeframe.values():
        months.update(_ordered_months(candles))
    return sorted(months)


def _slice_candles_by_months(candles: list[MarketCandle], months: set[str]) -> list[MarketCandle]:
    return [candle for candle in candles if _month_key(candle) in months]


def _window_definitions(
    months: list[str],
    train_months: int,
    test_months: int,
    step_months: int,
    window_mode: str = "rolling",
) -> list[dict[str, object]]:
    if train_months <= 0 or test_months <= 0 or step_months <= 0:
        raise ValueError("train_months, test_months, and step_months must be positive")
    if window_mode not in {"rolling", "expanding"}:
        raise ValueError("window_mode must be 'rolling' or 'expanding'")
    windows: list[dict[str, object]] = []
    start_index = 0
    while start_index + train_months + test_months <= len(months):
        if window_mode == "rolling":
            train = months[start_index : start_index + train_months]
        else:
            train = months[: start_index + train_months]
        test = months[start_index + train_months : start_index + train_months + test_months]
        windows.append(
            {
                "window_index": len(windows) + 1,
                "train_months": train,
                "test_months": test,
                "window_mode": window_mode,
            }
        )
        start_index += step_months
    return windows


def _latest_train_test_window(months: list[str], train_months: int, test_months: int) -> dict[str, object]:
    if len(months) < train_months + test_months:
        raise ValueError("not enough months for requested train/test split")
    split_index = len(months) - test_months
    return {
        "window_index": 1,
        "train_months": months[max(0, split_index - train_months) : split_index],
        "test_months": months[split_index:],
    }


def _window_bounds(candles: list[MarketCandle]) -> tuple[str | None, str | None]:
    if not candles:
        return None, None
    ordered = sorted(candles, key=lambda candle: candle.timestamp)
    return ordered[0].timestamp.isoformat(), ordered[-1].timestamp.isoformat()


def _window_bounds_by_timeframe(candles_by_timeframe: dict[str, list[MarketCandle]]) -> tuple[str | None, str | None]:
    merged = [candle for candles in candles_by_timeframe.values() for candle in candles]
    return _window_bounds(merged)


def _selection_tuple(payload: dict[str, object], selection_metric: str) -> tuple[float, ...]:
    if selection_metric == "profit":
        primary = float(payload["profit"])
    elif selection_metric == "win_rate":
        primary = float(payload["win_rate"])
    elif selection_metric == "max_drawdown":
        primary = -float(payload["max_drawdown"])
    else:
        primary = float(payload["score"])
    return (
        primary,
        float(payload["profit"]),
        -float(payload["max_drawdown"]),
        int(payload["trades"]),
        float(payload["win_rate"]),
    )


def _candidate_best_params(candidate: RuleCandidate) -> dict[str, object]:
    return asdict(candidate)


def _window_trade_metrics(result: RuleLabResult | object) -> dict[str, object]:
    trade_records = getattr(result, "trade_records", [])
    return summarize_trade_records(list(trade_records))


def _is_oos_ratio(is_pnl: float, oos_pnl: float) -> float | None:
    if abs(oos_pnl) < 1e-9:
        return None
    return is_pnl / oos_pnl


def _parameter_stability_warning(
    selected_oos_pnl: float,
    neighbor_oos_pnls: list[float],
) -> bool:
    if not neighbor_oos_pnls:
        return False
    if any((selected_oos_pnl >= 0 > neighbor) or (selected_oos_pnl <= 0 < neighbor) for neighbor in neighbor_oos_pnls):
        return True
    if selected_oos_pnl == 0:
        return any(abs(neighbor) > 0 for neighbor in neighbor_oos_pnls)
    spread = max(abs(selected_oos_pnl - neighbor) for neighbor in neighbor_oos_pnls)
    return spread > abs(selected_oos_pnl) * 0.5


def _result_payload(candidate: RuleCandidate, result: RuleLabResult) -> dict[str, object]:
    payload = {
        "name": candidate.name,
        "timeframe": candidate.timeframe,
        "entry_mode": candidate.entry_mode,
        "entry_buffer_ticks": candidate.entry_buffer_ticks,
        "profit": round(result.profit, 2),
        "trades": result.trades,
        "wins": result.wins,
        "losses": result.losses,
        "win_rate": round(result.win_rate, 4),
        "max_drawdown": round(result.max_drawdown, 2),
        "min_available_balance": round(result.min_available_balance, 2),
        "profitable_months": result.profitable_months,
        "losing_months": result.losing_months,
        "average_monthly_pnl": round(result.average_monthly_pnl, 2),
        "active_months": result.active_months,
        "profitable_month_ratio": round((result.profitable_months / result.active_months), 4) if result.active_months else 0.0,
    }
    payload["score"] = _score_result(payload)
    return payload


def _portfolio_payload(result: dict[str, object]) -> dict[str, object]:
    if not isinstance(result, dict):
        result = {
            "candidate_names": result.candidate_names,
            "profit": result.profit,
            "trades": result.trades,
            "wins": result.wins,
            "losses": result.losses,
            "win_rate": result.win_rate,
            "max_drawdown": result.max_drawdown,
            "min_available_balance": result.min_available_balance,
            "profitable_months": result.profitable_months,
            "losing_months": result.losing_months,
            "average_monthly_pnl": result.average_monthly_pnl,
            "active_months": result.active_months,
        }
    payload = {
        "candidate_names": list(result["candidate_names"]),
        "profit": round(float(result["profit"]), 2),
        "trades": int(result["trades"]),
        "wins": int(result["wins"]),
        "losses": int(result["losses"]),
        "win_rate": round(float(result["win_rate"]), 4),
        "max_drawdown": round(float(result["max_drawdown"]), 2),
        "min_available_balance": round(float(result["min_available_balance"]), 2),
        "profitable_months": int(result["profitable_months"]),
        "losing_months": int(result["losing_months"]),
        "average_monthly_pnl": round(float(result["average_monthly_pnl"]), 2),
        "active_months": int(result["active_months"]),
        "profitable_month_ratio": round(
            (float(result["profitable_months"]) / float(result["active_months"])) if result["active_months"] else 0.0,
            4,
        ),
    }
    payload["score"] = _score_result(payload)
    return payload


def _candidate_rejection_reasons(
    result: dict[str, object],
    *,
    min_trades: int,
    min_profit: float,
    min_win_rate: float,
    max_drawdown: float | None = None,
) -> tuple[bool, str | None]:
    trades = int(result["trades"])
    profit = float(result["profit"])
    win_rate = float(result["win_rate"])
    drawdown = float(result.get("max_drawdown", 0.0))
    if trades == 0:
        return False, "no_trades"
    if trades < min_trades:
        return False, "too_few_trades"
    if profit <= min_profit:
        return False, "non_positive_total_pnl"
    if win_rate < min_win_rate:
        return False, "win_rate_below_threshold"
    if max_drawdown is not None and drawdown > max_drawdown:
        return False, "drawdown_above_threshold"
    return True, None


def _portfolio_rejection_reasons(
    train_result: dict[str, object],
    test_result: dict[str, object],
    *,
    min_train_trades: int,
    min_test_trades: int,
    min_test_profit: float,
    min_test_win_rate: float,
    max_test_drawdown: float | None = None,
) -> list[str]:
    reasons: list[str] = []
    train_accepted, train_reason = _candidate_rejection_reasons(
        train_result,
        min_trades=min_train_trades,
        min_profit=0.0,
        min_win_rate=0.0,
    )
    test_accepted, test_reason = _candidate_rejection_reasons(
        test_result,
        min_trades=min_test_trades,
        min_profit=min_test_profit,
        min_win_rate=min_test_win_rate,
        max_drawdown=max_test_drawdown,
    )
    if not train_accepted and train_reason:
        reasons.append(f"train:{train_reason}")
    if not test_accepted and test_reason:
        reasons.append(f"test:{test_reason}")
    return reasons


def _load_candles_by_timeframe(base_config: AppConfig, candidates: list[RuleCandidate]) -> dict[str, list[MarketCandle]]:
    candles_by_timeframe: dict[str, list[MarketCandle]] = {}
    for candidate in candidates:
        if candidate.timeframe in candles_by_timeframe:
            continue
        config = deepcopy(base_config)
        config.runtime.timeframe = candidate.timeframe
        candles_by_timeframe[candidate.timeframe] = _load_candles(config)
    return candles_by_timeframe


def run_candidate_train_test_validation(
    config_path: str,
    base_config: AppConfig,
    *,
    candidate_names: list[str],
    train_months: int = 12,
    test_months: int = 4,
    min_train_trades: int = 30,
    min_test_trades: int = 10,
    min_test_profit: float = 0.0,
    min_test_win_rate: float = 0.0,
    max_test_drawdown: float | None = None,
) -> dict[str, object]:
    candidates = _select_candidates(candidate_names)
    external_factors = _load_external_factors(base_config)
    candles_by_timeframe = _load_candles_by_timeframe(base_config, candidates)
    months = _ordered_months_by_timeframe(candles_by_timeframe)
    window = _latest_train_test_window(months, train_months, test_months)
    train_set = set(window["train_months"])
    test_set = set(window["test_months"])
    results: list[dict[str, object]] = []

    for candidate in candidates:
        timeframe_candles = candles_by_timeframe[candidate.timeframe]
        train_candles = _slice_candles_by_months(timeframe_candles, train_set)
        test_candles = _slice_candles_by_months(timeframe_candles, test_set)
        train_result = _result_payload(candidate, run_rule_lab(train_candles, base_config, [candidate], external_factors=external_factors)[0])
        test_result = _result_payload(candidate, run_rule_lab(test_candles, base_config, [candidate], external_factors=external_factors)[0])
        train_accepted, train_reason = _candidate_rejection_reasons(
            train_result,
            min_trades=min_train_trades,
            min_profit=0.0,
            min_win_rate=0.0,
        )
        test_accepted, test_reason = _candidate_rejection_reasons(
            test_result,
            min_trades=min_test_trades,
            min_profit=min_test_profit,
            min_win_rate=min_test_win_rate,
            max_drawdown=max_test_drawdown,
        )
        rejected_reasons = [reason for reason in (f"train:{train_reason}" if train_reason else None, f"test:{test_reason}" if test_reason else None) if reason]
        results.append(
            {
                "name": candidate.name,
                "accepted": train_accepted and test_accepted,
                "train_accepted": train_accepted,
                "train_rejection_reason": train_reason,
                "test_accepted": test_accepted,
                "test_rejection_reason": test_reason,
                "rejected_reasons": rejected_reasons,
                "train": train_result,
                "test": test_result,
            }
        )

    ranked = sorted(
        results,
        key=lambda item: (
            item["accepted"],
            item["test_accepted"],
            item["train_accepted"],
            float(item["test"]["profit"]),
            -float(item["test"]["max_drawdown"]),
            int(item["test"]["trades"]),
            float(item["train"]["profit"]),
            -float(item["train"]["max_drawdown"]),
        ),
        reverse=True,
    )
    return {
        "mode": "candidate_train_test",
        "months": months,
        "train_months": window["train_months"],
        "test_months": window["test_months"],
        "criteria": {
            "min_train_trades": min_train_trades,
            "min_test_trades": min_test_trades,
            "min_test_profit": min_test_profit,
            "min_test_win_rate": min_test_win_rate,
            "max_test_drawdown": max_test_drawdown,
        },
        "results": ranked,
    }


def run_candidate_walk_forward_validation(
    config_path: str,
    base_config: AppConfig,
    *,
    candidate_names: list[str],
    train_months: int = 12,
    test_months: int = 4,
    step_months: int = 4,
    window_mode: str = "rolling",
    selection_metric: str = "score",
    neighbor_count: int = 3,
    min_train_trades: int = 30,
    min_test_trades: int = 10,
    min_test_profit: float = 0.0,
    min_test_win_rate: float = 0.0,
    max_test_drawdown: float | None = None,
) -> dict[str, object]:
    candidates = _select_candidates(candidate_names)
    external_factors = _load_external_factors(base_config)
    candles_by_timeframe = _load_candles_by_timeframe(base_config, candidates)
    months = _ordered_months_by_timeframe(candles_by_timeframe)
    windows = _window_definitions(months, train_months, test_months, step_months, window_mode)
    candidate_summaries = {
        candidate.name: {
            "name": candidate.name,
            "tested_windows": 0,
            "accepted_windows": 0,
            "positive_test_windows": 0,
            "total_test_profit": 0.0,
            "total_test_score": 0.0,
            "total_test_win_rate": 0.0,
            "total_test_drawdown": 0.0,
        }
        for candidate in candidates
    }
    window_results: list[dict[str, object]] = []
    oos_trade_records = []

    for window in windows:
        train_set = set(window["train_months"])
        test_set = set(window["test_months"])
        candidate_results = []
        for candidate in candidates:
            timeframe_candles = candles_by_timeframe[candidate.timeframe]
            train_candles = _slice_candles_by_months(timeframe_candles, train_set)
            test_candles = _slice_candles_by_months(timeframe_candles, test_set)
            train_result_raw = run_rule_lab(train_candles, base_config, [candidate], external_factors=external_factors)[0]
            test_result_raw = run_rule_lab(test_candles, base_config, [candidate], external_factors=external_factors)[0]
            train_result = _result_payload(candidate, train_result_raw)
            test_result = _result_payload(candidate, test_result_raw)
            train_accepted, train_reason = _candidate_rejection_reasons(
                train_result,
                min_trades=min_train_trades,
                min_profit=0.0,
                min_win_rate=0.0,
            )
            test_accepted, test_reason = _candidate_rejection_reasons(
                test_result,
                min_trades=min_test_trades,
                min_profit=min_test_profit,
                min_win_rate=min_test_win_rate,
                max_drawdown=max_test_drawdown,
            )
            accepted = train_accepted and test_accepted
            rejected_reasons = [reason for reason in (f"train:{train_reason}" if train_reason else None, f"test:{test_reason}" if test_reason else None) if reason]
            candidate_results.append(
                {
                    "name": candidate.name,
                    "candidate": candidate,
                    "accepted": accepted,
                    "train_accepted": train_accepted,
                    "train_rejection_reason": train_reason,
                    "test_accepted": test_accepted,
                    "test_rejection_reason": test_reason,
                    "rejected_reasons": rejected_reasons,
                    "train": train_result,
                    "test": test_result,
                    "train_result_raw": train_result_raw,
                    "test_result_raw": test_result_raw,
                }
            )

            summary = candidate_summaries[candidate.name]
            summary["tested_windows"] += 1
            summary["accepted_both_windows"] = summary.get("accepted_both_windows", 0) + (1 if accepted else 0)
            summary["accepted_test_windows"] = summary.get("accepted_test_windows", 0) + (1 if test_accepted else 0)
            summary["positive_test_windows"] += 1 if float(test_result["profit"]) > 0 else 0
            summary["total_test_profit"] += float(test_result["profit"])
            summary["total_test_score"] += float(test_result["score"])
            summary["total_test_win_rate"] += float(test_result["win_rate"])
            summary["total_test_drawdown"] += float(test_result["max_drawdown"])
            summary["worst_test_drawdown"] = max(float(summary.get("worst_test_drawdown", 0.0)), float(test_result["max_drawdown"]))
            summary["total_test_trades"] = summary.get("total_test_trades", 0) + int(test_result["trades"])
            summary["total_train_profit"] = summary.get("total_train_profit", 0.0) + float(train_result["profit"])
            summary["total_train_trades"] = summary.get("total_train_trades", 0) + int(train_result["trades"])

        ranked_by_is = sorted(
            candidate_results,
            key=lambda item: _selection_tuple(item["train"], selection_metric),
            reverse=True,
        )
        selected = ranked_by_is[0]
        selected_test_records = list(selected["test_result_raw"].trade_records)
        oos_trade_records.extend(
            [trade.__class__(**{**asdict(trade), "wf_window_id": _window_id(window)}) for trade in selected_test_records]
        )
        neighbor_slice = ranked_by_is[1 : 1 + max(0, neighbor_count - 1)]
        neighbor_oos_pnls = [float(item["test"]["profit"]) for item in neighbor_slice]
        train_start, train_end = _window_bounds(_slice_candles_by_months(candles_by_timeframe[selected["candidate"].timeframe], train_set))
        test_start, test_end = _window_bounds(_slice_candles_by_months(candles_by_timeframe[selected["candidate"].timeframe], test_set))
        is_metrics = _window_trade_metrics(selected["train_result_raw"])
        oos_metrics = _window_trade_metrics(selected["test_result_raw"])
        selected_window = {
            "window_index": window["window_index"],
            "window_id": _window_id(window),
            "window_mode": window_mode,
            "train_months": window["train_months"],
            "test_months": window["test_months"],
            "train_start": train_start,
            "train_end": train_end,
            "test_start": test_start,
            "test_end": test_end,
            "accepted": selected["accepted"],
            "train_accepted": selected["train_accepted"],
            "train_rejection_reason": selected["train_rejection_reason"],
            "test_accepted": selected["test_accepted"],
            "test_rejection_reason": selected["test_rejection_reason"],
            "rejected_reasons": list(selected["rejected_reasons"]),
            "optimization_method": "best_in_sample_candidate",
            "best_params": _candidate_best_params(selected["candidate"]),
            "selected_candidate": selected["name"],
            "selected_train_score": float(selected["train"]["score"]),
            "neighbor_candidates": [
                {
                    "name": item["name"],
                    "train_score": float(item["train"]["score"]),
                    "oos_profit": float(item["test"]["profit"]),
                }
                for item in neighbor_slice
            ],
            "parameter_stability_warning": _parameter_stability_warning(float(selected["test"]["profit"]), neighbor_oos_pnls),
            "is_metrics": is_metrics,
            "oos_metrics": oos_metrics,
            "is_oos_ratio": _is_oos_ratio(float(selected["train"]["profit"]), float(selected["test"]["profit"])),
            "train": selected["train"],
            "test": selected["test"],
            "results": [
                {
                    key: value
                    for key, value in item.items()
                    if key not in {"candidate", "train_result_raw", "test_result_raw"}
                }
                for item in ranked_by_is
            ],
        }
        window_results.append(
            selected_window
        )

    summary_rows = []
    for summary in candidate_summaries.values():
        tested_windows = max(1, int(summary["tested_windows"]))
        summary_rows.append(
            {
                "name": summary["name"],
                "tested_windows": summary["tested_windows"],
                "accepted_windows": summary.get("accepted_both_windows", 0),
                "accepted_both_windows": summary.get("accepted_both_windows", 0),
                "accepted_test_windows": summary.get("accepted_test_windows", 0),
                "positive_test_windows": summary["positive_test_windows"],
                "total_test_profit": round(summary["total_test_profit"], 2),
                "average_test_profit": round(summary["total_test_profit"] / tested_windows, 2),
                "average_test_score": round(summary["total_test_score"] / tested_windows, 4),
                "average_test_win_rate": round(summary["total_test_win_rate"] / tested_windows, 4),
                "average_test_drawdown": round(summary["total_test_drawdown"] / tested_windows, 2),
                "worst_test_drawdown": round(summary.get("worst_test_drawdown", 0.0), 2),
                "total_test_trades": summary.get("total_test_trades", 0),
                "total_train_profit": round(summary.get("total_train_profit", 0.0), 2),
                "total_train_trades": summary.get("total_train_trades", 0),
            }
        )
    summary_rows.sort(
        key=lambda item: (
            item["accepted_both_windows"],
            item["accepted_test_windows"],
            item["total_test_profit"],
            -item["worst_test_drawdown"],
            item["total_test_trades"],
        ),
        reverse=True,
    )
    positive_windows = [
        (window["window_id"], float(window.get("oos_metrics", {}).get("net_pnl", 0.0)))
        for window in window_results
        if float(window.get("oos_metrics", {}).get("net_pnl", 0.0)) > 0
    ]
    total_positive = sum(value for _, value in positive_windows)
    dominant_window_id = None
    if positive_windows and total_positive > 0:
        dominant_window_id, _ = max(positive_windows, key=lambda item: item[1])
    for window in window_results:
        window["single_window_dependency_flag"] = window["window_id"] == dominant_window_id and total_positive > 0

    return {
        "mode": "candidate_walk_forward",
        "candidate_names": [candidate.name for candidate in candidates],
        "months": months,
        "train_months": train_months,
        "test_months": test_months,
        "step_months": step_months,
        "window_mode": window_mode,
        "selection_metric": selection_metric,
        "neighbor_count": neighbor_count,
        "criteria": {
            "min_train_trades": min_train_trades,
            "min_test_trades": min_test_trades,
            "min_test_profit": min_test_profit,
            "min_test_win_rate": min_test_win_rate,
            "max_test_drawdown": max_test_drawdown,
        },
        "windows": window_results,
        "summary": summary_rows,
        "aggregate_summary": {
            "tested_windows": len(window_results),
            "accepted_windows": sum(1 for window in window_results if window["accepted"]),
            "accepted_test_windows": sum(1 for window in window_results if window["test_accepted"]),
            "positive_test_windows": sum(1 for window in window_results if float(window["oos_metrics"].get("net_pnl", 0.0)) > 0),
            "total_test_profit": round(sum(float(window["oos_metrics"].get("net_pnl", 0.0)) for window in window_results), 2),
            "average_test_win_rate": round(
                sum(float(window["test"]["win_rate"]) for window in window_results) / max(1, len(window_results)),
                4,
            ),
            "worst_test_drawdown": round(
                max((float(window["oos_metrics"].get("max_drawdown", 0.0)) for window in window_results), default=0.0),
                2,
            ),
        },
        "_oos_trade_records": oos_trade_records,
    }


def run_portfolio_walk_forward_validation(
    config_path: str,
    base_config: AppConfig,
    *,
    candidate_names: list[str],
    train_months: int = 12,
    test_months: int = 4,
    step_months: int = 4,
    window_mode: str = "rolling",
    selection_metric: str = "score",
    neighbor_count: int = 3,
    min_train_trades: int = 30,
    min_test_trades: int = 10,
    min_test_profit: float = 0.0,
    min_test_win_rate: float = 0.0,
    max_test_drawdown: float | None = None,
    include_trade_records: bool = False,
) -> dict[str, object]:
    candidates = _select_candidates(candidate_names)
    external_factors = _load_external_factors(base_config)
    candles_by_timeframe = _load_candles_by_timeframe(base_config, candidates)
    months = _ordered_months_by_timeframe(candles_by_timeframe)
    windows = _window_definitions(months, train_months, test_months, step_months, window_mode)
    window_results: list[dict[str, object]] = []
    accepted_windows = 0
    accepted_test_windows = 0
    positive_test_windows = 0
    total_test_profit = 0.0
    total_test_win_rate = 0.0
    total_test_drawdown = 0.0
    worst_test_drawdown = 0.0
    total_test_trades = 0
    oos_trade_records = []

    for window in windows:
        train_set = set(window["train_months"])
        test_set = set(window["test_months"])
        train_candles_by_timeframe = {
            timeframe: _slice_candles_by_months(candles, train_set)
            for timeframe, candles in candles_by_timeframe.items()
        }
        test_candles_by_timeframe = {
            timeframe: _slice_candles_by_months(candles, test_set)
            for timeframe, candles in candles_by_timeframe.items()
        }
        train_result_raw = simulate_portfolio(
            train_candles_by_timeframe,
            base_config,
            candidates,
            external_factors=external_factors,
            wf_window_id=f"wf_{window['window_index']:02d}_train",
        )
        test_result_raw = simulate_portfolio(
            test_candles_by_timeframe,
            base_config,
            candidates,
            external_factors=external_factors,
            wf_window_id=_window_id(window),
        )
        train_result = _portfolio_payload(train_result_raw)
        test_result = _portfolio_payload(test_result_raw)
        is_metrics = summarize_trade_records(list(train_result_raw.trade_records))
        oos_metrics = summarize_trade_records(list(test_result_raw.trade_records))
        train_accepted, train_reason = _candidate_rejection_reasons(
            train_result,
            min_trades=min_train_trades,
            min_profit=0.0,
            min_win_rate=0.0,
        )
        test_accepted, test_reason = _candidate_rejection_reasons(
            test_result,
            min_trades=min_test_trades,
            min_profit=min_test_profit,
            min_win_rate=min_test_win_rate,
            max_drawdown=max_test_drawdown,
        )
        rejected_reasons = _portfolio_rejection_reasons(
            train_result,
            test_result,
            min_train_trades=min_train_trades,
            min_test_trades=min_test_trades,
            min_test_profit=min_test_profit,
            min_test_win_rate=min_test_win_rate,
            max_test_drawdown=max_test_drawdown,
        )
        accepted = train_accepted and test_accepted
        accepted_windows += 1 if accepted else 0
        positive_test_windows += 1 if float(test_result["profit"]) > 0 else 0
        accepted_test_windows = accepted_test_windows + (1 if test_accepted else 0)
        total_test_profit += float(test_result["profit"])
        total_test_win_rate += float(test_result["win_rate"])
        total_test_drawdown += float(test_result["max_drawdown"])
        worst_test_drawdown = max(worst_test_drawdown, float(test_result["max_drawdown"]))
        total_test_trades = total_test_trades + int(test_result["trades"])
        if include_trade_records:
            oos_trade_records.extend(test_result_raw.trade_records)
        train_start, train_end = _window_bounds_by_timeframe(train_candles_by_timeframe)
        test_start, test_end = _window_bounds_by_timeframe(test_candles_by_timeframe)
        window_results.append(
            {
                "window_index": window["window_index"],
                "window_id": _window_id(window),
                "window_mode": window_mode,
                "train_months": window["train_months"],
                "test_months": window["test_months"],
                "train_start": train_start,
                "train_end": train_end,
                "test_start": test_start,
                "test_end": test_end,
                "accepted": accepted,
                "train_accepted": train_accepted,
                "train_rejection_reason": train_reason,
                "test_accepted": test_accepted,
                "test_rejection_reason": test_reason,
                "rejected_reasons": rejected_reasons,
                "optimization_method": "fixed_candidate_set",
                "best_params": {"candidate_names": [candidate.name for candidate in candidates]},
                "parameter_stability_warning": False,
                "neighbor_candidates": [],
                "is_metrics": is_metrics,
                "oos_metrics": oos_metrics,
                "is_oos_ratio": _is_oos_ratio(float(train_result["profit"]), float(test_result["profit"])),
                "train": train_result,
                "test": test_result,
            }
        )

    divisor = max(1, len(window_results))
    positive_windows = [
        (window["window_id"], float(window.get("oos_metrics", {}).get("net_pnl", 0.0)))
        for window in window_results
        if float(window.get("oos_metrics", {}).get("net_pnl", 0.0)) > 0
    ]
    total_positive = sum(value for _, value in positive_windows)
    dominant_window_id = None
    if positive_windows and total_positive > 0:
        dominant_window_id, _ = max(positive_windows, key=lambda item: item[1])
    for window in window_results:
        window["single_window_dependency_flag"] = window["window_id"] == dominant_window_id and total_positive > 0

    return {
        "mode": "portfolio_walk_forward",
        "candidate_names": [candidate.name for candidate in candidates],
        "months": months,
        "train_months": train_months,
        "test_months": test_months,
        "step_months": step_months,
        "window_mode": window_mode,
        "selection_metric": selection_metric,
        "neighbor_count": neighbor_count,
        "criteria": {
            "min_train_trades": min_train_trades,
            "min_test_trades": min_test_trades,
            "min_test_profit": min_test_profit,
            "min_test_win_rate": min_test_win_rate,
            "max_test_drawdown": max_test_drawdown,
        },
        "windows": window_results,
        "summary": {
            "tested_windows": len(window_results),
            "accepted_windows": accepted_windows,
            "accepted_both_windows": accepted_windows,
            "accepted_test_windows": accepted_test_windows,
            "positive_test_windows": positive_test_windows,
            "total_test_profit": round(total_test_profit, 2),
            "average_test_profit": round(total_test_profit / divisor, 2),
            "average_test_win_rate": round(total_test_win_rate / divisor, 4),
            "average_test_drawdown": round(total_test_drawdown / divisor, 2),
            "worst_test_drawdown": round(worst_test_drawdown, 2),
            "total_test_trades": total_test_trades,
        },
        **({"_oos_trade_records": oos_trade_records} if include_trade_records else {}),
    }


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.backtest-nk225micro.yaml")
    parser.add_argument("--candidate", action="append", required=True)
    parser.add_argument("--mode", choices=("candidate-train-test", "candidate-walk-forward", "portfolio-walk-forward"), default="candidate-train-test")
    parser.add_argument("--train-months", type=int)
    parser.add_argument("--test-months", type=int)
    parser.add_argument("--step-months", type=int)
    parser.add_argument("--window-mode", choices=("rolling", "expanding"))
    parser.add_argument("--selection-metric", choices=("score", "profit", "win_rate", "max_drawdown"))
    parser.add_argument("--neighbor-count", type=int)
    parser.add_argument("--min-train-trades", type=int)
    parser.add_argument("--min-test-trades", type=int)
    parser.add_argument("--min-test-profit", type=float)
    parser.add_argument("--min-test-win-rate", type=float)
    parser.add_argument("--max-test-drawdown", type=float)
    parser.add_argument("--output")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mode.value != "backtest":
        raise ValueError("validation requires mode=backtest")

    train_months = args.train_months if args.train_months is not None else config.walk_forward.train_months
    test_months = args.test_months if args.test_months is not None else config.walk_forward.test_months
    step_months = args.step_months if args.step_months is not None else config.walk_forward.step_months
    window_mode = args.window_mode or config.walk_forward.window_mode
    selection_metric = args.selection_metric or config.walk_forward.selection_metric
    neighbor_count = args.neighbor_count if args.neighbor_count is not None else config.walk_forward.neighbor_count
    min_train_trades = args.min_train_trades if args.min_train_trades is not None else config.walk_forward.min_train_trades
    min_test_trades = args.min_test_trades if args.min_test_trades is not None else config.walk_forward.min_test_trades
    min_test_profit = args.min_test_profit if args.min_test_profit is not None else config.walk_forward.min_test_profit
    min_test_win_rate = args.min_test_win_rate if args.min_test_win_rate is not None else config.walk_forward.min_test_win_rate
    max_test_drawdown = args.max_test_drawdown if args.max_test_drawdown is not None else config.walk_forward.max_test_drawdown

    if args.mode == "candidate-train-test":
        result = run_candidate_train_test_validation(
            args.config,
            config,
            candidate_names=args.candidate,
            train_months=train_months,
            test_months=test_months,
            min_train_trades=min_train_trades,
            min_test_trades=min_test_trades,
            min_test_profit=min_test_profit,
            min_test_win_rate=min_test_win_rate,
            max_test_drawdown=max_test_drawdown,
        )
    elif args.mode == "candidate-walk-forward":
        result = run_candidate_walk_forward_validation(
            args.config,
            config,
            candidate_names=args.candidate,
            train_months=train_months,
            test_months=test_months,
            step_months=step_months,
            window_mode=window_mode,
            selection_metric=selection_metric,
            neighbor_count=neighbor_count,
            min_train_trades=min_train_trades,
            min_test_trades=min_test_trades,
            min_test_profit=min_test_profit,
            min_test_win_rate=min_test_win_rate,
            max_test_drawdown=max_test_drawdown,
        )
    else:
        result = run_portfolio_walk_forward_validation(
            args.config,
            config,
            candidate_names=args.candidate,
            train_months=train_months,
            test_months=test_months,
            step_months=step_months,
            window_mode=window_mode,
            selection_metric=selection_metric,
            neighbor_count=neighbor_count,
            min_train_trades=min_train_trades,
            min_test_trades=min_test_trades,
            min_test_profit=min_test_profit,
            min_test_win_rate=min_test_win_rate,
            max_test_drawdown=max_test_drawdown,
            include_trade_records=True,
        )

    if args.mode in {"candidate-walk-forward", "portfolio-walk-forward"}:
        oos_trade_records = list(result.pop("_oos_trade_records", []))
        summary_payload = dict(result["aggregate_summary"]) if args.mode == "candidate-walk-forward" else dict(result["summary"])
        result["observability_outputs"] = write_walk_forward_review(
            Path("docs"),
            Path("output"),
            mode=str(result["mode"]),
            candidate_names=list(result["candidate_names"]),
            windows=list(result["windows"]),
            summary=summary_payload,
            trade_records=oos_trade_records,
            settings={
                "window_mode": result["window_mode"],
                "train_months": result["train_months"],
                "test_months": result["test_months"],
                "step_months": result["step_months"],
                "selection_metric": result.get("selection_metric", "score"),
                "neighbor_count": result.get("neighbor_count", 0),
            },
            optimization_method="best_in_sample_candidate"
            if args.mode == "candidate-walk-forward"
            else "fixed_candidate_set",
        )
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    print(rendered)


def _window_id(window: dict[str, object]) -> str:
    return f"wf_{int(window['window_index']):02d}"


if __name__ == "__main__":
    main()
