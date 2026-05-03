from __future__ import annotations

"""Research-grade candidate reports for Nikkei 225 micro validation.

These helpers are intentionally report-only. They do not touch broker adapters,
live execution, or order routing. The goal is to make rule promotion decisions
depend on stability and robustness, not headline profit alone.
"""

import csv
import json
import statistics
from copy import deepcopy
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import AppConfig
from .external_factors import ExternalFactors
from .observability import EnrichedTradeRecord
from .rule_lab import RuleCandidate, RuleLabResult, simulate_candidate
from .types import MarketCandle


RESEARCH_REPORT_FILES = {
    "research_candidates_csv": "research_candidates.csv",
    "research_candidates_json": "research_candidates.json",
    "monthly_summary": "monthly_summary.csv",
    "session_summary": "session_summary.csv",
    "direction_summary": "direction_summary.csv",
    "external_filter_summary": "external_filter_summary.csv",
    "sq_filter_summary": "sq_filter_summary.csv",
    "rejected_candidates": "rejected_candidates.csv",
}


@dataclass(slots=True)
class ResearchReportSettings:
    min_trades: int = 30
    test_months: int = 4
    slippage_bps_add: float = 1.0
    vix_threshold: float = 0.5
    probe_limit: int = 50
    max_drawdown: float | None = None


@dataclass(slots=True)
class _ExternalProbe:
    name: str
    session_filter: str
    direction_filter: str
    external_factor_name: str | None = None
    external_factor_filter: str = "all"
    external_factor_min_value: float = 0.0
    secondary_external_factor_name: str | None = None
    secondary_external_factor_filter: str = "all"
    secondary_external_factor_min_value: float = 0.0
    entry_start_time: str | None = None
    entry_end_time: str | None = None
    entry_mode: str | None = None


def write_research_report_outputs(
    *,
    output_dir: Path,
    config: AppConfig,
    candidates: list[RuleCandidate],
    results_by_name: dict[str, RuleLabResult],
    candles_by_timeframe: dict[str, list[MarketCandle]],
    external_factors: ExternalFactors | None,
    settings: ResearchReportSettings,
) -> dict[str, str]:
    """Write all research decision reports required for candidate promotion."""

    output_dir.mkdir(parents=True, exist_ok=True)
    all_months_by_timeframe = {
        timeframe: _ordered_months(candles)
        for timeframe, candles in candles_by_timeframe.items()
    }
    candidate_map = {candidate.name: candidate for candidate in candidates}
    ranked_names = _rank_names_for_probes(results_by_name)

    monthly_rows = [
        _monthly_summary_row(candidate_map[name], results_by_name[name], all_months_by_timeframe.get(candidate_map[name].timeframe, []))
        for name in sorted(results_by_name)
    ]
    session_rows = _session_summary_rows(results_by_name)
    direction_rows = _direction_summary_rows(results_by_name)
    candidate_rows, rejected_rows = _candidate_score_rows(
        config=config,
        candidates=candidates,
        results_by_name=results_by_name,
        candles_by_timeframe=candles_by_timeframe,
        all_months_by_timeframe=all_months_by_timeframe,
        settings=settings,
    )
    external_rows = _external_filter_rows(
        config=config,
        candidates=[candidate_map[name] for name in ranked_names[: settings.probe_limit] if name in candidate_map],
        results_by_name=results_by_name,
        candles_by_timeframe=candles_by_timeframe,
        external_factors=external_factors,
        settings=settings,
    )
    sq_rows = _sq_filter_rows(
        config=config,
        candidates=[candidate_map[name] for name in ranked_names[: settings.probe_limit] if name in candidate_map],
        results_by_name=results_by_name,
        candles_by_timeframe=candles_by_timeframe,
        external_factors=external_factors,
    )

    paths = {
        key: output_dir / filename
        for key, filename in RESEARCH_REPORT_FILES.items()
    }
    _write_csv(paths["monthly_summary"], monthly_rows, MONTHLY_HEADERS)
    _write_csv(paths["session_summary"], session_rows, SESSION_HEADERS)
    _write_csv(paths["direction_summary"], direction_rows, DIRECTION_HEADERS)
    _write_csv(paths["external_filter_summary"], external_rows, EXTERNAL_FILTER_HEADERS)
    _write_csv(paths["sq_filter_summary"], sq_rows, SQ_FILTER_HEADERS)
    _write_csv(paths["research_candidates_csv"], candidate_rows, CANDIDATE_HEADERS)
    _write_csv(paths["rejected_candidates"], rejected_rows, REJECTED_HEADERS)
    paths["research_candidates_json"].write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "settings": {
                    "min_trades": settings.min_trades,
                    "test_months": settings.test_months,
                    "slippage_bps_add": settings.slippage_bps_add,
                    "vix_threshold": settings.vix_threshold,
                    "probe_limit": settings.probe_limit,
                    "max_drawdown": settings.max_drawdown,
                },
                "accepted_candidates": candidate_rows,
                "rejected_candidates": rejected_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return {key: str(path) for key, path in paths.items()}


MONTHLY_HEADERS = [
    "rule_id",
    "monthly_pnl",
    "profitable_months",
    "losing_months",
    "worst_month",
    "worst_month_pnl",
    "best_month",
    "best_month_pnl",
    "average_monthly_pnl",
    "median_monthly_pnl",
    "max_consecutive_losing_months",
    "one_month_dependency_score",
]

SESSION_HEADERS = [
    "rule_id",
    "session",
    "profit",
    "trades",
    "win_rate",
    "max_drawdown",
    "average_trade_pnl",
    "profit_factor",
]

DIRECTION_HEADERS = [
    "rule_id",
    "direction",
    "profit",
    "trades",
    "win_rate",
    "max_drawdown",
]

EXTERNAL_FILTER_HEADERS = [
    "probe_name",
    "rule_id",
    "conditions",
    "status",
    "base_profit",
    "filtered_profit",
    "delta_profit",
    "base_trades",
    "filtered_trades",
    "base_win_rate",
    "filtered_win_rate",
    "base_max_drawdown",
    "filtered_max_drawdown",
]

SQ_FILTER_HEADERS = [
    "filter_name",
    "rule_id",
    "base_calendar_filter",
    "status",
    "base_profit",
    "filtered_profit",
    "delta_profit",
    "base_trades",
    "filtered_trades",
    "base_max_drawdown",
    "filtered_max_drawdown",
]

CANDIDATE_HEADERS = [
    "rank",
    "rule_id",
    "score",
    "net_profit",
    "gross_profit",
    "trades",
    "win_rate",
    "max_drawdown",
    "min_available_balance",
    "average_monthly_pnl",
    "median_monthly_pnl",
    "profitable_months",
    "losing_months",
    "max_consecutive_losing_months",
    "one_month_dependency_score",
    "test_period_net_profit",
    "slippage_test_net_profit",
    "session_filter",
    "direction_filter",
    "calendar_filter",
    "external_factor_name",
    "external_factor_filter",
    "secondary_external_factor_name",
    "secondary_external_factor_filter",
]

REJECTED_HEADERS = [
    "rule_id",
    "reasons",
    "score",
    "net_profit",
    "trades",
    "max_drawdown",
    "average_monthly_pnl",
    "profitable_months",
    "losing_months",
    "one_month_dependency_score",
    "test_period_net_profit",
    "slippage_test_net_profit",
]


def _monthly_summary_row(candidate: RuleCandidate, result: RuleLabResult, all_months: list[str]) -> dict[str, object]:
    metrics = _monthly_metrics(result, all_months)
    return {
        "rule_id": candidate.name,
        "monthly_pnl": _json_cell(metrics["monthly_pnl"]),
        "profitable_months": metrics["profitable_months"],
        "losing_months": metrics["losing_months"],
        "worst_month": metrics["worst_month"],
        "worst_month_pnl": metrics["worst_month_pnl"],
        "best_month": metrics["best_month"],
        "best_month_pnl": metrics["best_month_pnl"],
        "average_monthly_pnl": metrics["average_monthly_pnl"],
        "median_monthly_pnl": metrics["median_monthly_pnl"],
        "max_consecutive_losing_months": metrics["max_consecutive_losing_months"],
        "one_month_dependency_score": metrics["one_month_dependency_score"],
    }


def _candidate_score_rows(
    *,
    config: AppConfig,
    candidates: list[RuleCandidate],
    results_by_name: dict[str, RuleLabResult],
    candles_by_timeframe: dict[str, list[MarketCandle]],
    all_months_by_timeframe: dict[str, list[str]],
    settings: ResearchReportSettings,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    scored_rows: list[dict[str, object]] = []
    rejected_rows: list[dict[str, object]] = []
    for candidate in candidates:
        result = results_by_name[candidate.name]
        monthly = _monthly_metrics(result, all_months_by_timeframe.get(candidate.timeframe, []))
        test_net_profit = _test_period_net_profit(config, candidate, candles_by_timeframe[candidate.timeframe], settings.test_months)
        slippage_net_profit = _slippage_net_profit(config, candidate, candles_by_timeframe[candidate.timeframe], settings.slippage_bps_add)
        net_profit = _net_profit(result.trade_records)
        score = _candidate_score(
            config=config,
            result=result,
            monthly=monthly,
            net_profit=net_profit,
            test_net_profit=test_net_profit,
            slippage_net_profit=slippage_net_profit,
        )
        reasons = _rejection_reasons(
            config=config,
            result=result,
            monthly=monthly,
            net_profit=net_profit,
            test_net_profit=test_net_profit,
            slippage_net_profit=slippage_net_profit,
            min_trades=settings.min_trades,
            max_drawdown=settings.max_drawdown,
        )
        row = {
            "rank": 0,
            "rule_id": candidate.name,
            "score": score,
            "net_profit": round(net_profit, 2),
            "gross_profit": round(result.profit, 2),
            "trades": result.trades,
            "win_rate": round(result.win_rate, 4),
            "max_drawdown": round(result.max_drawdown, 2),
            "min_available_balance": round(result.min_available_balance, 2),
            "average_monthly_pnl": monthly["average_monthly_pnl"],
            "median_monthly_pnl": monthly["median_monthly_pnl"],
            "profitable_months": monthly["profitable_months"],
            "losing_months": monthly["losing_months"],
            "max_consecutive_losing_months": monthly["max_consecutive_losing_months"],
            "one_month_dependency_score": monthly["one_month_dependency_score"],
            "test_period_net_profit": "" if test_net_profit is None else round(test_net_profit, 2),
            "slippage_test_net_profit": round(slippage_net_profit, 2),
            "session_filter": candidate.session_filter,
            "direction_filter": candidate.direction_filter,
            "calendar_filter": candidate.calendar_filter,
            "external_factor_name": candidate.external_factor_name or "",
            "external_factor_filter": candidate.external_factor_filter,
            "secondary_external_factor_name": candidate.secondary_external_factor_name or "",
            "secondary_external_factor_filter": candidate.secondary_external_factor_filter,
        }
        if reasons:
            rejected = {
                "rule_id": candidate.name,
                "reasons": "|".join(reasons),
                "score": score,
                "net_profit": round(net_profit, 2),
                "trades": result.trades,
                "max_drawdown": round(result.max_drawdown, 2),
                "average_monthly_pnl": monthly["average_monthly_pnl"],
                "profitable_months": monthly["profitable_months"],
                "losing_months": monthly["losing_months"],
                "one_month_dependency_score": monthly["one_month_dependency_score"],
                "test_period_net_profit": "" if test_net_profit is None else round(test_net_profit, 2),
                "slippage_test_net_profit": round(slippage_net_profit, 2),
            }
            rejected_rows.append(rejected)
        else:
            scored_rows.append(row)

    scored_rows.sort(key=lambda item: (float(item["score"]), float(item["net_profit"])), reverse=True)
    for index, row in enumerate(scored_rows, start=1):
        row["rank"] = index
    rejected_rows.sort(key=lambda item: (float(item["score"]), float(item["net_profit"])), reverse=True)
    return scored_rows, rejected_rows


def _external_filter_rows(
    *,
    config: AppConfig,
    candidates: list[RuleCandidate],
    results_by_name: dict[str, RuleLabResult],
    candles_by_timeframe: dict[str, list[MarketCandle]],
    external_factors: ExternalFactors | None,
    settings: ResearchReportSettings,
) -> list[dict[str, object]]:
    probes = _external_probes(settings.vix_threshold)
    rows: list[dict[str, object]] = []
    for probe in probes:
        for candidate in candidates:
            if not _candidate_matches_probe(candidate, probe):
                continue
            base = results_by_name[candidate.name]
            if external_factors is None:
                rows.append(_external_probe_row(probe, candidate, base, None, status="missing_external_factors"))
                continue
            filtered_candidate = _clone_for_external_probe(candidate, probe)
            filtered_result = simulate_candidate(
                candles_by_timeframe[candidate.timeframe],
                config,
                filtered_candidate,
                external_factors=external_factors,
            )
            rows.append(_external_probe_row(probe, candidate, base, filtered_result, status="ok"))
    return rows


def _sq_filter_rows(
    *,
    config: AppConfig,
    candidates: list[RuleCandidate],
    results_by_name: dict[str, RuleLabResult],
    candles_by_timeframe: dict[str, list[MarketCandle]],
    external_factors: ExternalFactors | None,
) -> list[dict[str, object]]:
    filters = [
        "exclude_sq",
        "exclude_sq_week",
        "exclude_last_trading_window",
        "exclude_roll_week",
        "exclude_calendar_risk",
    ]
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        base = results_by_name[candidate.name]
        for calendar_filter in filters:
            filtered_candidate = replace(
                candidate,
                name=f"{candidate.name}__{calendar_filter}",
                calendar_filter=calendar_filter,
            )
            filtered_result = simulate_candidate(
                candles_by_timeframe[candidate.timeframe],
                config,
                filtered_candidate,
                external_factors=external_factors,
            )
            rows.append(
                {
                    "filter_name": calendar_filter,
                    "rule_id": candidate.name,
                    "base_calendar_filter": candidate.calendar_filter,
                    "status": "ok",
                    "base_profit": round(_net_profit(base.trade_records), 2),
                    "filtered_profit": round(_net_profit(filtered_result.trade_records), 2),
                    "delta_profit": round(_net_profit(filtered_result.trade_records) - _net_profit(base.trade_records), 2),
                    "base_trades": base.trades,
                    "filtered_trades": filtered_result.trades,
                    "base_max_drawdown": round(base.max_drawdown, 2),
                    "filtered_max_drawdown": round(filtered_result.max_drawdown, 2),
                }
            )
    return rows


def _session_summary_rows(results_by_name: dict[str, RuleLabResult]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rule_id, result in sorted(results_by_name.items()):
        for session in ["day", "night", "opening", "midday"]:
            trades = [trade for trade in result.trade_records if _trade_in_session_group(trade, session)]
            metrics = _trade_group_metrics(trades)
            rows.append({"rule_id": rule_id, "session": session, **metrics})
    return rows


def _direction_summary_rows(results_by_name: dict[str, RuleLabResult]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rule_id, result in sorted(results_by_name.items()):
        for direction in ["long", "short"]:
            trades = [trade for trade in result.trade_records if trade.side == direction]
            metrics = _trade_group_metrics(trades)
            rows.append(
                {
                    "rule_id": rule_id,
                    "direction": f"{direction}_only",
                    "profit": metrics["profit"],
                    "trades": metrics["trades"],
                    "win_rate": metrics["win_rate"],
                    "max_drawdown": metrics["max_drawdown"],
                }
            )
    return rows


def _monthly_metrics(result: RuleLabResult, all_months: list[str]) -> dict[str, object]:
    months = all_months or sorted(result.monthly_pnl)
    monthly = {month: round(result.monthly_pnl.get(month, 0.0), 2) for month in months}
    values = list(monthly.values())
    if not values:
        values = [0.0]
    profitable_months = sum(1 for value in values if value > 0)
    losing_months = sum(1 for value in values if value < 0)
    worst_month, worst_value = min(monthly.items(), key=lambda item: item[1]) if monthly else ("", 0.0)
    best_month, best_value = max(monthly.items(), key=lambda item: item[1]) if monthly else ("", 0.0)
    positive_values = [value for value in values if value > 0]
    total_positive = sum(positive_values)
    dependency = (max(positive_values) / total_positive) if total_positive > 0 else 1.0
    return {
        "monthly_pnl": monthly,
        "profitable_months": profitable_months,
        "losing_months": losing_months,
        "worst_month": worst_month,
        "worst_month_pnl": round(worst_value, 2),
        "best_month": best_month,
        "best_month_pnl": round(best_value, 2),
        "average_monthly_pnl": round(sum(values) / len(values), 2),
        "median_monthly_pnl": round(statistics.median(values), 2),
        "max_consecutive_losing_months": _max_consecutive_losing_months(values),
        "one_month_dependency_score": round(dependency, 4),
    }


def _candidate_score(
    *,
    config: AppConfig,
    result: RuleLabResult,
    monthly: dict[str, object],
    net_profit: float,
    test_net_profit: float | None,
    slippage_net_profit: float,
) -> float:
    initial_balance = max(float(config.paper.initial_balance), 1.0)
    drawdown_ratio = max(result.max_drawdown, 0.0) / initial_balance
    monthly_ratio = (
        float(monthly["profitable_months"]) / max(float(monthly["profitable_months"]) + float(monthly["losing_months"]), 1.0)
    )
    dependency = float(monthly["one_month_dependency_score"])
    score = 0.0
    score += _clamp(net_profit / 1000.0, -25.0, 35.0)
    score += _clamp((0.12 - drawdown_ratio) * 220.0, -25.0, 25.0)
    score += _clamp(float(monthly["average_monthly_pnl"]) / 600.0, -15.0, 20.0)
    score += monthly_ratio * 18.0
    score += max(0.0, 10.0 - float(monthly["max_consecutive_losing_months"]) * 3.0)
    score += max(0.0, (1.0 - dependency) * 14.0)
    score += min(result.trades / 10.0, 12.0)
    if result.min_available_balance >= _available_balance_floor(config):
        score += 8.0
    else:
        score -= 12.0
    score += 12.0 if test_net_profit is not None and test_net_profit > 0 else -18.0
    score += 10.0 if slippage_net_profit > 0 else -18.0
    return round(score, 4)


def _rejection_reasons(
    *,
    config: AppConfig,
    result: RuleLabResult,
    monthly: dict[str, object],
    net_profit: float,
    test_net_profit: float | None,
    slippage_net_profit: float,
    min_trades: int,
    max_drawdown: float | None,
) -> list[str]:
    reasons: list[str] = []
    drawdown_limit = max_drawdown if max_drawdown is not None else config.paper.initial_balance * 0.10
    if result.trades < min_trades:
        reasons.append("too_few_trades")
    if float(monthly["one_month_dependency_score"]) > 0.55 and net_profit > 0:
        reasons.append("one_month_dependency")
    if result.max_drawdown > drawdown_limit:
        reasons.append("high_drawdown")
    if test_net_profit is None or test_net_profit <= 0:
        reasons.append("test_period_negative")
    if slippage_net_profit <= 0 or (net_profit > 0 and slippage_net_profit < net_profit * 0.50):
        reasons.append("slippage_sensitive")
    if (
        float(monthly["average_monthly_pnl"]) <= 0
        or int(monthly["profitable_months"]) <= int(monthly["losing_months"])
        or int(monthly["max_consecutive_losing_months"]) >= 3
    ):
        reasons.append("weak_monthly_stability")
    if result.min_available_balance < _available_balance_floor(config):
        reasons.append("low_available_balance")
    return reasons


def _test_period_net_profit(
    config: AppConfig,
    candidate: RuleCandidate,
    candles: list[MarketCandle],
    test_months: int,
) -> float | None:
    months = _ordered_months(candles)
    if len(months) < test_months or test_months <= 0:
        return None
    target_months = set(months[-test_months:])
    test_candles = [candle for candle in candles if _month_key(candle) in target_months]
    if not test_candles:
        return None
    result = simulate_candidate(test_candles, config, candidate)
    return _net_profit(result.trade_records)


def _slippage_net_profit(
    config: AppConfig,
    candidate: RuleCandidate,
    candles: list[MarketCandle],
    slippage_bps_add: float,
) -> float:
    stressed_config = deepcopy(config)
    stressed_config.paper.slippage_bps = float(stressed_config.paper.slippage_bps) + slippage_bps_add
    result = simulate_candidate(candles, stressed_config, candidate)
    return _net_profit(result.trade_records)


def _external_probes(vix_threshold: float) -> list[_ExternalProbe]:
    return [
        _ExternalProbe(
            name="night_short_sp500_down",
            session_filter="night",
            direction_filter="short_only",
            external_factor_name="sp500_change",
            external_factor_filter="below",
            external_factor_min_value=0.0,
        ),
        _ExternalProbe(
            name="night_short_usdjpy_down",
            session_filter="night",
            direction_filter="short_only",
            external_factor_name="usd_jpy_change",
            external_factor_filter="below",
            external_factor_min_value=0.0,
        ),
        _ExternalProbe(
            name="night_short_usdjpy_down_us10y_up",
            session_filter="night",
            direction_filter="short_only",
            external_factor_name="usd_jpy_change",
            external_factor_filter="below",
            external_factor_min_value=0.0,
            secondary_external_factor_name="us10y_change_bp",
            secondary_external_factor_filter="above",
            secondary_external_factor_min_value=0.0,
        ),
        _ExternalProbe(
            name="midday_long_sp500_up",
            session_filter="day",
            direction_filter="long_only",
            entry_start_time="11:00",
            entry_end_time="13:30",
            external_factor_name="sp500_change",
            external_factor_filter="above",
            external_factor_min_value=0.0,
        ),
        _ExternalProbe(
            name="fade_off_vix_above_threshold",
            session_filter="both",
            direction_filter="both",
            entry_mode="fade",
            external_factor_name="vix_change",
            external_factor_filter="below",
            external_factor_min_value=vix_threshold,
        ),
    ]


def _clone_for_external_probe(candidate: RuleCandidate, probe: _ExternalProbe) -> RuleCandidate:
    return replace(
        candidate,
        name=f"{candidate.name}__{probe.name}",
        session_filter=probe.session_filter,
        direction_filter=probe.direction_filter,
        external_factor_name=probe.external_factor_name,
        external_factor_filter=probe.external_factor_filter,
        external_factor_min_value=probe.external_factor_min_value,
        secondary_external_factor_name=probe.secondary_external_factor_name,
        secondary_external_factor_filter=probe.secondary_external_factor_filter,
        secondary_external_factor_min_value=probe.secondary_external_factor_min_value,
        entry_start_time=probe.entry_start_time or candidate.entry_start_time,
        entry_end_time=probe.entry_end_time or candidate.entry_end_time,
    )


def _candidate_matches_probe(candidate: RuleCandidate, probe: _ExternalProbe) -> bool:
    if probe.entry_mode and candidate.entry_mode != probe.entry_mode:
        return False
    if probe.session_filter != "both" and candidate.session_filter not in {probe.session_filter, "both"}:
        return False
    if probe.direction_filter != "both" and candidate.direction_filter not in {probe.direction_filter, "both"}:
        return False
    return True


def _external_probe_row(
    probe: _ExternalProbe,
    candidate: RuleCandidate,
    base: RuleLabResult,
    filtered: RuleLabResult | None,
    *,
    status: str,
) -> dict[str, object]:
    base_profit = _net_profit(base.trade_records)
    filtered_profit = _net_profit(filtered.trade_records) if filtered is not None else None
    return {
        "probe_name": probe.name,
        "rule_id": candidate.name,
        "conditions": _json_cell(
            {
                "session_filter": probe.session_filter,
                "direction_filter": probe.direction_filter,
                "external_factor_name": probe.external_factor_name,
                "external_factor_filter": probe.external_factor_filter,
                "external_factor_min_value": probe.external_factor_min_value,
                "secondary_external_factor_name": probe.secondary_external_factor_name,
                "secondary_external_factor_filter": probe.secondary_external_factor_filter,
                "secondary_external_factor_min_value": probe.secondary_external_factor_min_value,
                "entry_start_time": probe.entry_start_time,
                "entry_end_time": probe.entry_end_time,
            }
        ),
        "status": status,
        "base_profit": round(base_profit, 2),
        "filtered_profit": "" if filtered_profit is None else round(filtered_profit, 2),
        "delta_profit": "" if filtered_profit is None else round(filtered_profit - base_profit, 2),
        "base_trades": base.trades,
        "filtered_trades": "" if filtered is None else filtered.trades,
        "base_win_rate": round(base.win_rate, 4),
        "filtered_win_rate": "" if filtered is None else round(filtered.win_rate, 4),
        "base_max_drawdown": round(base.max_drawdown, 2),
        "filtered_max_drawdown": "" if filtered is None else round(filtered.max_drawdown, 2),
    }


def _trade_group_metrics(trades: list[EnrichedTradeRecord]) -> dict[str, object]:
    wins = [trade.pnl_net for trade in trades if trade.pnl_net > 0]
    losses = [trade.pnl_net for trade in trades if trade.pnl_net <= 0]
    profit = sum(trade.pnl_net for trade in trades)
    gross_wins = sum(wins)
    gross_losses = abs(sum(losses))
    return {
        "profit": round(profit, 2),
        "trades": len(trades),
        "win_rate": round((len(wins) / len(trades)) if trades else 0.0, 4),
        "max_drawdown": round(_trade_drawdown(trades), 2),
        "average_trade_pnl": round((profit / len(trades)) if trades else 0.0, 2),
        "profit_factor": "" if gross_losses == 0 else round(gross_wins / gross_losses, 4),
    }


def _trade_drawdown(trades: list[EnrichedTradeRecord]) -> float:
    equity = 0.0
    peak = 0.0
    drawdown = 0.0
    for trade in sorted(trades, key=lambda item: item.exit_ts):
        equity += trade.pnl_net
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
    return drawdown


def _trade_in_session_group(trade: EnrichedTradeRecord, session: str) -> bool:
    if session == "day":
        return trade.session_bucket.startswith("day_")
    if session == "night":
        return trade.session_bucket.startswith("night_")
    if session == "opening":
        return "opening" in trade.session_bucket
    if session == "midday":
        return "midday" in trade.session_bucket
    return False


def _ordered_months(candles: list[MarketCandle]) -> list[str]:
    return sorted({_month_key(candle) for candle in candles})


def _month_key(candle: MarketCandle) -> str:
    if candle.trading_day:
        return candle.trading_day[:7]
    return candle.timestamp.strftime("%Y-%m")


def _max_consecutive_losing_months(values: list[float]) -> int:
    longest = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _net_profit(trades: list[EnrichedTradeRecord]) -> float:
    return sum(trade.pnl_net for trade in trades)


def _available_balance_floor(config: AppConfig) -> float:
    return float(config.risk.min_cash_buffer) + float(config.risk.per_contract_margin or 0.0)


def _rank_names_for_probes(results_by_name: dict[str, RuleLabResult]) -> list[str]:
    return [
        name
        for name, _result in sorted(
            results_by_name.items(),
            key=lambda item: (_net_profit(item[1].trade_records), -item[1].max_drawdown, item[1].trades),
            reverse=True,
        )
    ]


def _write_csv(path: Path, rows: list[dict[str, object]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def _json_cell(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(max(value, lower), upper)
