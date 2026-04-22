from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from .config import AppConfig, load_config
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


def _window_definitions(months: list[str], train_months: int, test_months: int, step_months: int) -> list[dict[str, object]]:
    if train_months <= 0 or test_months <= 0 or step_months <= 0:
        raise ValueError("train_months, test_months, and step_months must be positive")
    windows: list[dict[str, object]] = []
    start_index = 0
    while start_index + train_months + test_months <= len(months):
        train = months[start_index : start_index + train_months]
        test = months[start_index + train_months : start_index + train_months + test_months]
        windows.append(
            {
                "window_index": len(windows) + 1,
                "train_months": train,
                "test_months": test,
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
    windows = _window_definitions(months, train_months, test_months, step_months)
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

    for window in windows:
        train_set = set(window["train_months"])
        test_set = set(window["test_months"])
        candidate_results = []
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
            accepted = train_accepted and test_accepted
            rejected_reasons = [reason for reason in (f"train:{train_reason}" if train_reason else None, f"test:{test_reason}" if test_reason else None) if reason]
            candidate_results.append(
                {
                    "name": candidate.name,
                    "accepted": accepted,
                    "train_accepted": train_accepted,
                    "train_rejection_reason": train_reason,
                    "test_accepted": test_accepted,
                    "test_rejection_reason": test_reason,
                    "rejected_reasons": rejected_reasons,
                    "train": train_result,
                    "test": test_result,
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

        window_results.append(
            {
                "window_index": window["window_index"],
                "train_months": window["train_months"],
                "test_months": window["test_months"],
                "results": sorted(
                    candidate_results,
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
                ),
            }
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

    return {
        "mode": "candidate_walk_forward",
        "months": months,
        "train_months": train_months,
        "test_months": test_months,
        "step_months": step_months,
        "criteria": {
            "min_train_trades": min_train_trades,
            "min_test_trades": min_test_trades,
            "min_test_profit": min_test_profit,
            "min_test_win_rate": min_test_win_rate,
            "max_test_drawdown": max_test_drawdown,
        },
        "windows": window_results,
        "summary": summary_rows,
    }


def run_portfolio_walk_forward_validation(
    config_path: str,
    base_config: AppConfig,
    *,
    candidate_names: list[str],
    train_months: int = 12,
    test_months: int = 4,
    step_months: int = 4,
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
    windows = _window_definitions(months, train_months, test_months, step_months)
    window_results: list[dict[str, object]] = []
    accepted_windows = 0
    accepted_test_windows = 0
    positive_test_windows = 0
    total_test_profit = 0.0
    total_test_win_rate = 0.0
    total_test_drawdown = 0.0
    worst_test_drawdown = 0.0
    total_test_trades = 0

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
        train_result = _portfolio_payload(
            simulate_portfolio(train_candles_by_timeframe, base_config, candidates, external_factors=external_factors)
        )
        test_result = _portfolio_payload(
            simulate_portfolio(test_candles_by_timeframe, base_config, candidates, external_factors=external_factors)
        )
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
        window_results.append(
            {
                "window_index": window["window_index"],
                "train_months": window["train_months"],
                "test_months": window["test_months"],
                "accepted": accepted,
                "train_accepted": train_accepted,
                "train_rejection_reason": train_reason,
                "test_accepted": test_accepted,
                "test_rejection_reason": test_reason,
                "rejected_reasons": rejected_reasons,
                "train": train_result,
                "test": test_result,
            }
        )

    divisor = max(1, len(window_results))
    return {
        "mode": "portfolio_walk_forward",
        "candidate_names": [candidate.name for candidate in candidates],
        "months": months,
        "train_months": train_months,
        "test_months": test_months,
        "step_months": step_months,
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
    }


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.backtest-nk225micro.yaml")
    parser.add_argument("--candidate", action="append", required=True)
    parser.add_argument("--mode", choices=("candidate-train-test", "candidate-walk-forward", "portfolio-walk-forward"), default="candidate-train-test")
    parser.add_argument("--train-months", type=int, default=12)
    parser.add_argument("--test-months", type=int, default=4)
    parser.add_argument("--step-months", type=int, default=4)
    parser.add_argument("--min-train-trades", type=int, default=30)
    parser.add_argument("--min-test-trades", type=int, default=10)
    parser.add_argument("--min-test-profit", type=float, default=0.0)
    parser.add_argument("--min-test-win-rate", type=float, default=0.0)
    parser.add_argument("--max-test-drawdown", type=float)
    parser.add_argument("--output")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mode.value != "backtest":
        raise ValueError("validation requires mode=backtest")

    if args.mode == "candidate-train-test":
        result = run_candidate_train_test_validation(
            args.config,
            config,
            candidate_names=args.candidate,
            train_months=args.train_months,
            test_months=args.test_months,
            min_train_trades=args.min_train_trades,
            min_test_trades=args.min_test_trades,
            min_test_profit=args.min_test_profit,
            min_test_win_rate=args.min_test_win_rate,
            max_test_drawdown=args.max_test_drawdown,
        )
    elif args.mode == "candidate-walk-forward":
        result = run_candidate_walk_forward_validation(
            args.config,
            config,
            candidate_names=args.candidate,
            train_months=args.train_months,
            test_months=args.test_months,
            step_months=args.step_months,
            min_train_trades=args.min_train_trades,
            min_test_trades=args.min_test_trades,
            min_test_profit=args.min_test_profit,
            min_test_win_rate=args.min_test_win_rate,
            max_test_drawdown=args.max_test_drawdown,
        )
    else:
        result = run_portfolio_walk_forward_validation(
            args.config,
            config,
            candidate_names=args.candidate,
            train_months=args.train_months,
            test_months=args.test_months,
            step_months=args.step_months,
            min_train_trades=args.min_train_trades,
            min_test_trades=args.min_test_trades,
            min_test_profit=args.min_test_profit,
            min_test_win_rate=args.min_test_win_rate,
            max_test_drawdown=args.max_test_drawdown,
        )

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
