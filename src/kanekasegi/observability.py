from __future__ import annotations

"""Observability helpers for Nikkei 225 micro research backtests.

This module intentionally extends existing outputs instead of replacing them.
All CSV/Markdown/SVG artifacts are additive and are written beside the
pre-existing JSON research outputs.
"""

import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from typing import Any, Iterable

from .config import AppConfig
from .types import MarketCandle, SessionType, SignalAction


OBSERVABILITY_OUTPUT_FILES = {
    "trades_csv": "trades_enriched.csv",
    "wfo_trades_csv": "wfo_trades_enriched.csv",
    "pnl_by_rule": "pnl_by_rule.csv",
    "pnl_by_session": "pnl_by_session.csv",
    "pnl_by_side": "pnl_by_side.csv",
    "pnl_by_weekday": "pnl_by_weekday.csv",
    "pnl_by_vol_bucket": "pnl_by_vol_bucket.csv",
    "pnl_by_regime": "pnl_by_regime.csv",
    "pnl_by_holding": "pnl_by_holding.csv",
    "pnl_by_wf_window": "pnl_by_wf_window.csv",
    "walk_forward_windows_csv": "walk_forward_windows.csv",
    "walk_forward_summary_json": "walk_forward_summary.json",
    "equity_curve_svg": "equity_curve.svg",
    "rule_pnl_svg": "rule_pnl.svg",
    "session_heatmap_svg": "session_heatmap.svg",
    "wfo_windows_svg": "wfo_oos_windows.svg",
}


@dataclass(slots=True)
class TradeSeed:
    """Entry-side metadata captured when a position is opened."""

    rule_id: str
    strategy_name: str
    side: SignalAction
    entry_ts: datetime
    entry_market_price: float
    entry_price: float
    qty: int
    weekday: str
    session_bucket: str
    vol_bucket: str
    regime_id: str
    regime_name: str
    config_hash: str


@dataclass(slots=True)
class EnrichedTradeRecord:
    """Machine-readable enriched trade schema for Nikkei research outputs.

    Notes:
    - `spread_cost` stays empty because the current Nikkei research config has
      no explicit spread parameter in code.
    - `wf_window_id` stays empty outside walk-forward OOS aggregation.
    """

    trade_id: str
    rule_id: str
    strategy_name: str
    side: str
    entry_ts: str
    exit_ts: str
    hold_minutes: float
    entry_price: float
    exit_price: float
    qty: int
    pnl_gross: float
    pnl_net: float
    commission: float | None
    spread_cost: float | None
    slippage_cost: float | None
    weekday: str
    session_bucket: str
    vol_bucket: str
    regime_id: str
    regime_name: str
    config_hash: str
    wf_window_id: str | None = None

    @classmethod
    def csv_headers(cls) -> list[str]:
        # Header order is intentionally fixed so downstream diffs stay stable.
        return [
            "trade_id",
            "rule_id",
            "strategy_name",
            "side",
            "entry_ts",
            "exit_ts",
            "hold_minutes",
            "entry_price",
            "exit_price",
            "qty",
            "pnl_gross",
            "pnl_net",
            "commission",
            "spread_cost",
            "slippage_cost",
            "weekday",
            "session_bucket",
            "vol_bucket",
            "regime_id",
            "regime_name",
            "config_hash",
            "wf_window_id",
        ]

    def to_csv_row(self) -> dict[str, object]:
        return {
            "trade_id": self.trade_id,
            "rule_id": self.rule_id,
            "strategy_name": self.strategy_name,
            "side": self.side,
            "entry_ts": self.entry_ts,
            "exit_ts": self.exit_ts,
            "hold_minutes": round(self.hold_minutes, 2),
            "entry_price": round(self.entry_price, 4),
            "exit_price": round(self.exit_price, 4),
            "qty": self.qty,
            "pnl_gross": round(self.pnl_gross, 2),
            "pnl_net": round(self.pnl_net, 2),
            "commission": "" if self.commission is None else round(self.commission, 2),
            "spread_cost": "" if self.spread_cost is None else round(self.spread_cost, 2),
            "slippage_cost": "" if self.slippage_cost is None else round(self.slippage_cost, 2),
            "weekday": self.weekday,
            "session_bucket": self.session_bucket,
            "vol_bucket": self.vol_bucket,
            "regime_id": self.regime_id,
            "regime_name": self.regime_name,
            "config_hash": self.config_hash,
            "wf_window_id": self.wf_window_id or "",
        }


def build_config_hash(config: AppConfig) -> str:
    payload = json.dumps(config.model_dump(mode="json"), ensure_ascii=True, sort_keys=True)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def build_trade_seed(
    config: AppConfig,
    *,
    rule_id: str,
    strategy_name: str,
    side: SignalAction,
    entry_candle: MarketCandle,
    entry_market_price: float,
    qty: int,
    atr_value: float,
    trend_ema: float,
    tick_size: float,
) -> TradeSeed:
    return TradeSeed(
        rule_id=rule_id,
        strategy_name=strategy_name,
        side=side,
        entry_ts=entry_candle.timestamp,
        entry_market_price=entry_market_price,
        entry_price=_apply_slippage(entry_market_price, side, config.paper.slippage_bps, is_entry=True),
        qty=qty,
        weekday=entry_candle.timestamp.strftime("%a"),
        session_bucket=_session_bucket(entry_candle),
        vol_bucket=_vol_bucket(entry_market_price, atr_value),
        regime_id=_regime_id(entry_market_price, trend_ema, atr_value, tick_size),
        regime_name=_regime_name(entry_market_price, trend_ema, atr_value, tick_size),
        config_hash=build_config_hash(config),
    )


def finalize_trade_record(
    config: AppConfig,
    seed: TradeSeed,
    *,
    exit_candle: MarketCandle,
    exit_market_price: float,
    wf_window_id: str | None = None,
) -> EnrichedTradeRecord:
    exit_price = _apply_slippage(exit_market_price, seed.side, config.paper.slippage_bps, is_entry=False)
    market_pnl = _price_pnl(
        seed.side,
        seed.entry_market_price,
        exit_market_price,
        seed.qty,
        config.risk.contract_point_value,
    )
    pnl_gross = _price_pnl(
        seed.side,
        seed.entry_price,
        exit_price,
        seed.qty,
        config.risk.contract_point_value,
    )
    slippage_cost = market_pnl - pnl_gross
    commission = _round_trip_commission(config, seed.entry_price, exit_price, seed.qty)
    pnl_net = pnl_gross - commission
    hold_minutes = max((exit_candle.timestamp - seed.entry_ts).total_seconds() / 60.0, 0.0)
    trade_id = _trade_id(seed, exit_candle.timestamp, exit_price, wf_window_id)
    return EnrichedTradeRecord(
        trade_id=trade_id,
        rule_id=seed.rule_id,
        strategy_name=seed.strategy_name,
        side=seed.side.value,
        entry_ts=seed.entry_ts.isoformat(),
        exit_ts=exit_candle.timestamp.isoformat(),
        hold_minutes=hold_minutes,
        entry_price=seed.entry_price,
        exit_price=exit_price,
        qty=seed.qty,
        pnl_gross=pnl_gross,
        pnl_net=pnl_net,
        commission=commission,
        spread_cost=None,
        slippage_cost=slippage_cost,
        weekday=seed.weekday,
        session_bucket=seed.session_bucket,
        vol_bucket=seed.vol_bucket,
        regime_id=seed.regime_id,
        regime_name=seed.regime_name,
        config_hash=seed.config_hash,
        wf_window_id=wf_window_id,
    )


def write_trade_csv(path: Path, trades: Iterable[EnrichedTradeRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    trade_rows = list(trades)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EnrichedTradeRecord.csv_headers())
        writer.writeheader()
        for trade in trade_rows:
            writer.writerow(trade.to_csv_row())
    return path


def write_pnl_breakdown_csvs(output_dir: Path, trades: list[EnrichedTradeRecord]) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "pnl_by_rule": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_rule"],
        "pnl_by_session": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_session"],
        "pnl_by_side": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_side"],
        "pnl_by_weekday": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_weekday"],
        "pnl_by_vol_bucket": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_vol_bucket"],
        "pnl_by_regime": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_regime"],
        "pnl_by_holding": output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_holding"],
    }
    _write_group_csv(paths["pnl_by_rule"], "rule_id", _aggregate_trades(trades, lambda trade: trade.rule_id))
    _write_group_csv(paths["pnl_by_session"], "session_bucket", _aggregate_trades(trades, lambda trade: trade.session_bucket))
    _write_group_csv(paths["pnl_by_side"], "side", _aggregate_trades(trades, lambda trade: trade.side))
    _write_group_csv(paths["pnl_by_weekday"], "weekday", _aggregate_trades(trades, lambda trade: trade.weekday))
    _write_group_csv(paths["pnl_by_vol_bucket"], "vol_bucket", _aggregate_trades(trades, lambda trade: trade.vol_bucket))
    _write_group_csv(
        paths["pnl_by_regime"],
        "regime_id",
        _aggregate_trades(trades, lambda trade: trade.regime_id, label_fn=lambda trade: trade.regime_name),
    )
    _write_group_csv(paths["pnl_by_holding"], "holding_bucket", _aggregate_trades(trades, lambda trade: _holding_bucket(trade.hold_minutes)))
    return {key: str(path) for key, path in paths.items()}


def write_wf_window_csv(output_dir: Path, windows: list[dict[str, object]]) -> str:
    """Backward-compatible compact WFO CSV kept for existing consumers."""

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / OBSERVABILITY_OUTPUT_FILES["pnl_by_wf_window"]
    headers = [
        "wf_window_id",
        "train_months",
        "test_months",
        "accepted",
        "test_profit",
        "test_win_rate",
        "test_max_drawdown",
        "test_trades",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for window in windows:
            oos_metrics = dict(window.get("oos_metrics", {}))
            test_summary = dict(window.get("test", {}))
            writer.writerow(
                {
                    "wf_window_id": window.get("window_id") or _window_id(window),
                    "train_months": ",".join(window.get("train_months", [])),
                    "test_months": ",".join(window.get("test_months", [])),
                    "accepted": window.get("accepted", False),
                    "test_profit": round(float(oos_metrics.get("net_pnl", test_summary.get("profit", 0.0))), 2),
                    "test_win_rate": round(float(test_summary.get("win_rate", 0.0)), 4),
                    "test_max_drawdown": round(float(oos_metrics.get("max_drawdown", test_summary.get("max_drawdown", 0.0))), 2),
                    "test_trades": int(oos_metrics.get("trades", test_summary.get("trades", 0))),
                }
            )
    return str(path)


def write_walk_forward_windows_csv(output_dir: Path, windows: list[dict[str, object]]) -> str:
    """Detailed per-window WFO CSV for auditability and reproducibility."""

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / OBSERVABILITY_OUTPUT_FILES["walk_forward_windows_csv"]
    headers = [
        "window_id",
        "window_mode",
        "train_start",
        "train_end",
        "test_start",
        "test_end",
        "best_params",
        "is_net_pnl",
        "oos_net_pnl",
        "is_oos_ratio",
        "is_profit_factor",
        "oos_profit_factor",
        "is_max_drawdown",
        "oos_max_drawdown",
        "is_trades",
        "oos_trades",
        "is_average_hold_time",
        "oos_average_hold_time",
        "oos_side_imbalance",
        "oos_regime_distribution",
        "accepted",
        "optimization_method",
        "single_window_dependency_flag",
        "parameter_stability_warning",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for window in windows:
            is_metrics = dict(window.get("is_metrics", {}))
            oos_metrics = dict(window.get("oos_metrics", {}))
            writer.writerow(
                {
                    "window_id": window.get("window_id") or _window_id(window),
                    "window_mode": window.get("window_mode", ""),
                    "train_start": window.get("train_start", ""),
                    "train_end": window.get("train_end", ""),
                    "test_start": window.get("test_start", ""),
                    "test_end": window.get("test_end", ""),
                    "best_params": _json_cell(window.get("best_params")),
                    "is_net_pnl": _round_or_blank(is_metrics.get("net_pnl")),
                    "oos_net_pnl": _round_or_blank(oos_metrics.get("net_pnl")),
                    "is_oos_ratio": _round_or_blank(window.get("is_oos_ratio")),
                    "is_profit_factor": _round_or_blank(is_metrics.get("profit_factor")),
                    "oos_profit_factor": _round_or_blank(oos_metrics.get("profit_factor")),
                    "is_max_drawdown": _round_or_blank(is_metrics.get("max_drawdown")),
                    "oos_max_drawdown": _round_or_blank(oos_metrics.get("max_drawdown")),
                    "is_trades": int(is_metrics.get("trades", 0)),
                    "oos_trades": int(oos_metrics.get("trades", 0)),
                    "is_average_hold_time": _round_or_blank(is_metrics.get("average_hold_time")),
                    "oos_average_hold_time": _round_or_blank(oos_metrics.get("average_hold_time")),
                    "oos_side_imbalance": _round_or_blank(oos_metrics.get("side_imbalance")),
                    "oos_regime_distribution": _json_cell(oos_metrics.get("regime_distribution")),
                    "accepted": bool(window.get("accepted", False)),
                    "optimization_method": window.get("optimization_method", ""),
                    "single_window_dependency_flag": bool(window.get("single_window_dependency_flag", False)),
                    "parameter_stability_warning": bool(window.get("parameter_stability_warning", False)),
                }
            )
    return str(path)


def write_walk_forward_summary_json(output_dir: Path, payload: dict[str, object]) -> str:
    """Structured WFO summary JSON for reproducible reruns."""

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / OBSERVABILITY_OUTPUT_FILES["walk_forward_summary_json"]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def write_pnl_dashboard(
    docs_dir: Path,
    output_dir: Path,
    *,
    portfolio_name: str,
    trades: list[EnrichedTradeRecord],
    profit: float,
    max_drawdown: float,
    win_rate: float,
    trade_csv_path: Path,
    breakdown_paths: dict[str, str],
) -> str:
    docs_dir.mkdir(parents=True, exist_ok=True)
    equity_svg = output_dir / OBSERVABILITY_OUTPUT_FILES["equity_curve_svg"]
    rule_svg = output_dir / OBSERVABILITY_OUTPUT_FILES["rule_pnl_svg"]
    heatmap_svg = output_dir / OBSERVABILITY_OUTPUT_FILES["session_heatmap_svg"]
    _write_equity_curve_svg(equity_svg, trades)
    _write_rule_pnl_svg(rule_svg, trades)
    _write_session_heatmap_svg(heatmap_svg, trades)
    path = docs_dir / "pnl_dashboard.md"
    lines = [
        "<!-- Generated by kanekasegi.portfolio_research observability extension. -->",
        "# PnL Dashboard",
        "",
        "This dashboard extends the Nikkei 225 backtest outputs with additive observability artifacts.",
        "It keeps the existing JSON outputs intact and adds trade detail, pnl decomposition, and charts.",
        "",
        "## Current Run",
        f"- portfolio_name: `{portfolio_name}`",
        f"- profit: `{profit:.2f}`",
        f"- max_drawdown: `{max_drawdown:.2f}`",
        f"- win_rate: `{win_rate:.4f}`",
        f"- trades_csv: `{trade_csv_path.as_posix()}`",
        "",
        "## Enriched Trade Columns",
        "- `trade_id`: deterministic trade identifier for reproducible reruns.",
        "- `rule_id` / `strategy_name`: current Nikkei research path uses candidate names.",
        "- `commission`: round-trip cost computed from `paper.fee_rate`.",
        "- `spread_cost`: blank because the Nikkei research path has no explicit spread parameter yet.",
        "- `slippage_cost`: computed from `paper.slippage_bps` on entry and exit.",
        "- `session_bucket`: entry timestamp grouped into day/night session buckets.",
        "- `vol_bucket`: low / mid / high bucket based on ATR versus entry price.",
        "- `regime_id` / `regime_name`: simple regime label from trend and volatility at entry.",
        "- `config_hash`: reproducibility hash derived from the config payload.",
        "- `wf_window_id`: walk-forward window identifier for OOS aggregation.",
        "",
        "## Added CSV Files",
        f"- `pnl_by_rule.csv`: `{Path(breakdown_paths['pnl_by_rule']).as_posix()}`",
        f"- `pnl_by_session.csv`: `{Path(breakdown_paths['pnl_by_session']).as_posix()}`",
        f"- `pnl_by_side.csv`: `{Path(breakdown_paths['pnl_by_side']).as_posix()}`",
        f"- `pnl_by_weekday.csv`: `{Path(breakdown_paths['pnl_by_weekday']).as_posix()}`",
        f"- `pnl_by_vol_bucket.csv`: `{Path(breakdown_paths['pnl_by_vol_bucket']).as_posix()}`",
        f"- `pnl_by_regime.csv`: `{Path(breakdown_paths['pnl_by_regime']).as_posix()}`",
        f"- `pnl_by_holding.csv`: `{Path(breakdown_paths['pnl_by_holding']).as_posix()}`",
        "",
        "## Charts",
        f"![Equity Curve](../output/{OBSERVABILITY_OUTPUT_FILES['equity_curve_svg']})",
        "",
        f"![Rule PnL](../output/{OBSERVABILITY_OUTPUT_FILES['rule_pnl_svg']})",
        "",
        f"![Session Heatmap](../output/{OBSERVABILITY_OUTPUT_FILES['session_heatmap_svg']})",
        "",
        "## Notes",
        "- `spread_cost` is intentionally blank because the current Nikkei config has no code-backed spread value.",
        "- regime is an observability axis, not a direct rule-selection signal by itself.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def build_walk_forward_summary_payload(
    *,
    mode: str,
    settings: dict[str, object],
    optimization_method: str,
    windows: list[dict[str, object]],
    summary: dict[str, object],
) -> dict[str, object]:
    oos_pnls = [float(window.get("oos_metrics", {}).get("net_pnl", 0.0)) for window in windows]
    dependency = _single_window_dependency(windows)
    overfit_signals = _overfit_signals(windows)
    return {
        "mode": mode,
        "settings": settings,
        "optimization_method": optimization_method,
        "summary": summary,
        "oos_distribution": {
            "count": len(oos_pnls),
            "mean": _safe_stat(oos_pnls, "mean"),
            "median": _safe_stat(oos_pnls, "median"),
            "min": min(oos_pnls) if oos_pnls else None,
            "max": max(oos_pnls) if oos_pnls else None,
            "stddev": _safe_stat(oos_pnls, "pstdev"),
        },
        "single_window_dependency": dependency,
        "overfit_signals": overfit_signals,
        "next_minimal_change": _next_minimal_change(windows, overfit_signals),
        "windows": windows,
    }


def write_walk_forward_review(
    docs_dir: Path,
    output_dir: Path,
    *,
    mode: str,
    candidate_names: list[str],
    windows: list[dict[str, object]],
    summary: dict[str, object],
    trade_records: list[EnrichedTradeRecord],
    settings: dict[str, object],
    optimization_method: str,
) -> dict[str, str]:
    docs_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    wfo_trade_csv = write_trade_csv(output_dir / OBSERVABILITY_OUTPUT_FILES["wfo_trades_csv"], trade_records)
    compact_wf_window_csv = write_wf_window_csv(output_dir, windows)
    detailed_wf_window_csv = write_walk_forward_windows_csv(output_dir, windows)
    summary_json_payload = build_walk_forward_summary_payload(
        mode=mode,
        settings=settings,
        optimization_method=optimization_method,
        windows=windows,
        summary=summary,
    )
    wf_summary_json = write_walk_forward_summary_json(output_dir, summary_json_payload)
    wfo_svg = output_dir / OBSERVABILITY_OUTPUT_FILES["wfo_windows_svg"]
    _write_wfo_bar_svg(wfo_svg, windows)
    path = docs_dir / "walk_forward_review.md"
    oos_distribution = summary_json_payload["oos_distribution"]
    dependency = summary_json_payload["single_window_dependency"]
    overfit_signals = summary_json_payload["overfit_signals"]
    next_minimal_change = summary_json_payload["next_minimal_change"]
    lines = [
        "<!-- Generated by kanekasegi.validation observability extension. -->",
        "# Walk Forward Review",
        "",
        "This report audits Nikkei 225 walk-forward behavior without replacing the normal backtest flow.",
        "It preserves time order and focuses on out-of-sample behavior and overfitting detection.",
        "",
        "## Window Settings",
        f"- mode: `{settings.get('window_mode', 'rolling')}`",
        f"- train_months: `{settings.get('train_months')}`",
        f"- test_months: `{settings.get('test_months')}`",
        f"- step_months: `{settings.get('step_months')}`",
        "",
        "## Optimization Method",
        f"- method: `{optimization_method}`",
        f"- selection_metric: `{settings.get('selection_metric', 'score')}`",
        f"- neighbor_count: `{settings.get('neighbor_count', 0)}`",
        "",
        "## Candidate Set",
    ]
    for name in candidate_names:
        lines.append(f"- `{name}`")
    lines.extend(
        [
            "",
            "## Summary",
            f"- tested_windows: `{summary.get('tested_windows', 0)}`",
            f"- accepted_windows: `{summary.get('accepted_windows', 0)}`",
            f"- total_test_profit: `{float(summary.get('total_test_profit', 0.0)):.2f}`",
            f"- average_test_win_rate: `{float(summary.get('average_test_win_rate', 0.0)):.4f}`",
            f"- worst_test_drawdown: `{float(summary.get('worst_test_drawdown', 0.0)):.2f}`",
            "",
            "## OOS Distribution",
            f"- count: `{oos_distribution.get('count', 0)}`",
            f"- mean: `{_round_or_blank(oos_distribution.get('mean'))}`",
            f"- median: `{_round_or_blank(oos_distribution.get('median'))}`",
            f"- min: `{_round_or_blank(oos_distribution.get('min'))}`",
            f"- max: `{_round_or_blank(oos_distribution.get('max'))}`",
            f"- stddev: `{_round_or_blank(oos_distribution.get('stddev'))}`",
            "",
            "## Single Window Dependency",
            f"- dominant_window_id: `{dependency.get('window_id', '')}`",
            f"- dominant_share: `{_round_or_blank(dependency.get('share'))}`",
            f"- warning: `{dependency.get('warning', False)}`",
            "",
            "## Overfitting Signals",
        ]
    )
    if overfit_signals:
        for signal in overfit_signals:
            lines.append(f"- {signal}")
    else:
        lines.append("- no strong overfitting signal detected from the current window audit")
    lines.extend(
        [
            "",
            "## Added Files",
            f"- `wfo_trades_enriched.csv`: `{wfo_trade_csv.as_posix()}`",
            f"- `pnl_by_wf_window.csv`: `{compact_wf_window_csv}`",
            f"- `walk_forward_windows.csv`: `{detailed_wf_window_csv}`",
            f"- `walk_forward_summary.json`: `{wf_summary_json}`",
            "",
            "## WFO OOS Chart",
            f"![WFO OOS Windows](../output/{OBSERVABILITY_OUTPUT_FILES['wfo_windows_svg']})",
            "",
            "## Next Smallest Change To Try",
            f"- {next_minimal_change}",
            "",
            "## Notes",
            "- `best_params` is selected from train-side information only. Test-side metrics are not used for selection.",
            "- `walk_forward_windows.csv` is the primary per-window audit CSV, not just an aggregate summary.",
            "- `regime_distribution` stores entry-regime counts as a JSON string.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "wfo_trades_csv": str(wfo_trade_csv),
        "pnl_by_wf_window": compact_wf_window_csv,
        "walk_forward_windows_csv": detailed_wf_window_csv,
        "walk_forward_summary_json": wf_summary_json,
        "wfo_windows_svg": str(wfo_svg),
        "walk_forward_review": str(path),
    }


def summarize_trade_records(trades: list[EnrichedTradeRecord]) -> dict[str, object]:
    if not trades:
        return {
            "net_pnl": 0.0,
            "profit_factor": None,
            "max_drawdown": 0.0,
            "trades": 0,
            "average_hold_time": None,
            "side_imbalance": None,
            "regime_distribution": {},
        }

    pnl_values = [trade.pnl_net for trade in trades]
    gross_profit = sum(value for value in pnl_values if value > 0)
    gross_loss = abs(sum(value for value in pnl_values if value < 0))
    equity = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for trade in sorted(trades, key=lambda item: item.exit_ts):
        equity += trade.pnl_net
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, peak - equity)
    long_count = sum(1 for trade in trades if trade.side == SignalAction.LONG.value)
    short_count = sum(1 for trade in trades if trade.side == SignalAction.SHORT.value)
    total_count = len(trades)
    regime_counts: dict[str, int] = defaultdict(int)
    for trade in trades:
        regime_counts[trade.regime_id] += 1
    return {
        "net_pnl": sum(pnl_values),
        "profit_factor": None if gross_loss == 0 and gross_profit == 0 else (math.inf if gross_loss == 0 else gross_profit / gross_loss),
        "max_drawdown": max_drawdown,
        "trades": total_count,
        "average_hold_time": sum(trade.hold_minutes for trade in trades) / total_count,
        "side_imbalance": abs(long_count - short_count) / total_count if total_count else None,
        "regime_distribution": dict(sorted(regime_counts.items())),
    }


def _apply_slippage(price: float, side: SignalAction, slippage_bps: float, *, is_entry: bool) -> float:
    if slippage_bps <= 0:
        return price
    slip = price * (slippage_bps / 10_000)
    if side == SignalAction.LONG:
        return price + slip if is_entry else price - slip
    return price - slip if is_entry else price + slip


def _price_pnl(side: SignalAction, entry_price: float, exit_price: float, qty: int, point_value: float) -> float:
    if side == SignalAction.LONG:
        return (exit_price - entry_price) * qty * point_value
    return (entry_price - exit_price) * qty * point_value


def _round_trip_commission(config: AppConfig, entry_price: float, exit_price: float, qty: int) -> float:
    fee_rate = config.paper.fee_rate
    if fee_rate <= 0:
        return 0.0
    point_value = config.risk.contract_point_value
    entry_notional = abs(entry_price * qty * point_value)
    exit_notional = abs(exit_price * qty * point_value)
    return (entry_notional + exit_notional) * fee_rate


def _trade_id(seed: TradeSeed, exit_ts: datetime, exit_price: float, wf_window_id: str | None) -> str:
    raw = "|".join(
        [
            seed.rule_id,
            seed.side.value,
            seed.entry_ts.isoformat(),
            exit_ts.isoformat(),
            f"{seed.entry_price:.6f}",
            f"{exit_price:.6f}",
            str(seed.qty),
            wf_window_id or "base",
        ]
    )
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _session_bucket(candle: MarketCandle) -> str:
    timestamp = candle.timestamp.time()
    if candle.session == SessionType.DAY:
        if timestamp < time(9, 30):
            return "day_opening"
        if timestamp < time(11, 30):
            return "day_morning"
        if timestamp < time(13, 30):
            return "day_midday"
        return "day_afternoon"
    if candle.session == SessionType.NIGHT:
        if timestamp < time(0, 0):
            if timestamp < time(19, 0):
                return "night_opening"
            return "night_evening"
        return "night_overnight"
    return "unknown"


def _vol_bucket(price: float, atr_value: float) -> str:
    if price <= 0 or atr_value <= 0:
        return "unknown"
    atr_bps = (atr_value / price) * 10_000
    if atr_bps < 20:
        return "low"
    if atr_bps < 45:
        return "mid"
    return "high"


def _regime_id(price: float, trend_ema: float, atr_value: float, tick_size: float) -> str:
    return f"{_trend_label(price, trend_ema, atr_value, tick_size)}_{_vol_bucket(price, atr_value)}"


def _regime_name(price: float, trend_ema: float, atr_value: float, tick_size: float) -> str:
    trend_label = _trend_label(price, trend_ema, atr_value, tick_size)
    return f"{trend_label.replace('_', ' ')} / {_vol_bucket(price, atr_value)} vol"


def _trend_label(price: float, trend_ema: float, atr_value: float, tick_size: float) -> str:
    neutral_band = max(atr_value * 0.25, tick_size)
    if abs(price - trend_ema) <= neutral_band:
        return "range"
    if price > trend_ema:
        return "trend_up"
    return "trend_down"


def _aggregate_trades(
    trades: list[EnrichedTradeRecord],
    key_fn,
    *,
    label_fn=None,
) -> list[dict[str, object]]:
    grouped: dict[str, list[EnrichedTradeRecord]] = defaultdict(list)
    labels: dict[str, str] = {}
    for trade in trades:
        key = key_fn(trade) or "unknown"
        grouped[str(key)].append(trade)
        if label_fn is not None:
            labels[str(key)] = label_fn(trade) or str(key)
    rows: list[dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        wins = sum(1 for trade in group if trade.pnl_net > 0)
        losses = sum(1 for trade in group if trade.pnl_net <= 0)
        rows.append(
            {
                "group": key,
                "label": labels.get(key, key),
                "trades": len(group),
                "wins": wins,
                "losses": losses,
                "win_rate": round((wins / len(group)) if group else 0.0, 4),
                "pnl_gross": round(sum(trade.pnl_gross for trade in group), 2),
                "pnl_net": round(sum(trade.pnl_net for trade in group), 2),
                "commission": round(sum(trade.commission or 0.0 for trade in group), 2),
                "slippage_cost": round(sum(trade.slippage_cost or 0.0 for trade in group), 2),
                "avg_hold_minutes": round(sum(trade.hold_minutes for trade in group) / len(group), 2),
            }
        )
    return rows


def _write_group_csv(path: Path, key_header: str, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        key_header,
        "label",
        "trades",
        "wins",
        "losses",
        "win_rate",
        "pnl_gross",
        "pnl_net",
        "commission",
        "slippage_cost",
        "avg_hold_minutes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            payload = dict(row)
            payload[key_header] = payload.pop("group")
            writer.writerow(payload)


def _holding_bucket(hold_minutes: float) -> str:
    if hold_minutes <= 15:
        return "00_15m"
    if hold_minutes <= 60:
        return "16_60m"
    if hold_minutes <= 240:
        return "61_240m"
    return "241m_plus"


def _write_equity_curve_svg(path: Path, trades: list[EnrichedTradeRecord]) -> None:
    points = []
    equity = 0.0
    for index, trade in enumerate(sorted(trades, key=lambda item: item.exit_ts)):
        equity += trade.pnl_net
        points.append((index, equity))
    _write_line_svg(path, points, title="Equity Curve", color="#0a7f5a")


def _write_rule_pnl_svg(path: Path, trades: list[EnrichedTradeRecord]) -> None:
    rows = _aggregate_trades(trades, lambda trade: trade.rule_id)
    _write_bar_svg(path, [(row["group"], float(row["pnl_net"])) for row in rows], title="PnL By Rule")


def _write_session_heatmap_svg(path: Path, trades: list[EnrichedTradeRecord]) -> None:
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    session_order = [
        "day_opening",
        "day_morning",
        "day_midday",
        "day_afternoon",
        "night_opening",
        "night_evening",
        "night_overnight",
        "unknown",
    ]
    matrix: dict[tuple[str, str], float] = defaultdict(float)
    for trade in trades:
        matrix[(trade.weekday, trade.session_bucket)] += trade.pnl_net
    cell_width = 110
    cell_height = 28
    width = 160 + (len(session_order) * cell_width)
    height = 80 + (len(weekdays) * cell_height)
    values = list(matrix.values()) or [0.0]
    min_value = min(values)
    max_value = max(values)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<style>text{font-family:Segoe UI, Arial, sans-serif;font-size:12px;fill:#111827}</style>',
        '<text x="12" y="24" font-size="16" font-weight="700">Session Heatmap</text>',
    ]
    for column, session_bucket in enumerate(session_order):
        x = 150 + (column * cell_width)
        lines.append(f'<text x="{x + 4}" y="48">{session_bucket}</text>')
    for row_index, weekday in enumerate(weekdays):
        y = 64 + (row_index * cell_height)
        lines.append(f'<text x="12" y="{y + 18}">{weekday}</text>')
        for column, session_bucket in enumerate(session_order):
            x = 150 + (column * cell_width)
            value = matrix.get((weekday, session_bucket), 0.0)
            color = _heat_color(value, min_value, max_value)
            lines.append(f'<rect x="{x}" y="{y}" width="{cell_width - 6}" height="{cell_height - 4}" rx="4" fill="{color}" />')
            lines.append(f'<text x="{x + 6}" y="{y + 18}">{value:.0f}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_wfo_bar_svg(path: Path, windows: list[dict[str, object]]) -> None:
    bars = [(_window_id(window), float(window.get("oos_metrics", {}).get("net_pnl", window.get("test", {}).get("profit", 0.0)))) for window in windows]
    _write_bar_svg(path, bars, title="WFO OOS Profit By Window")


def _write_line_svg(path: Path, points: list[tuple[int, float]], *, title: str, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width = 840
    height = 260
    if not points:
        path.write_text(
            "\n".join(
                [
                    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
                    '<text x="24" y="32" font-family="Segoe UI, Arial, sans-serif" font-size="18">No data</text>',
                    "</svg>",
                ]
            ),
            encoding="utf-8",
        )
        return
    max_x = max(point[0] for point in points) or 1
    values = [point[1] for point in points]
    min_y = min(values)
    max_y = max(values)
    if math.isclose(min_y, max_y):
        min_y -= 1.0
        max_y += 1.0
    chart_left = 56
    chart_top = 32
    chart_width = width - 80
    chart_height = height - 72

    def _x(value: int) -> float:
        return chart_left + (value / max_x) * chart_width

    def _y(value: float) -> float:
        return chart_top + chart_height - ((value - min_y) / (max_y - min_y)) * chart_height

    polyline = " ".join(f"{_x(index):.2f},{_y(value):.2f}" for index, value in points)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<style>text{font-family:Segoe UI, Arial, sans-serif;font-size:12px;fill:#111827}</style>',
        f'<text x="16" y="22" font-size="16" font-weight="700">{title}</text>',
        f'<rect x="{chart_left}" y="{chart_top}" width="{chart_width}" height="{chart_height}" fill="#ffffff" stroke="#d1d5db" />',
        f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{polyline}" />',
        f'<text x="16" y="{height - 20}">min={min_y:.2f}</text>',
        f'<text x="{width - 140}" y="{height - 20}">max={max_y:.2f}</text>',
        "</svg>",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_bar_svg(path: Path, bars: list[tuple[str, float]], *, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width = 920
    height = max(220, 70 + (len(bars) * 28))
    if not bars:
        path.write_text(
            "\n".join(
                [
                    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
                    '<text x="24" y="32" font-family="Segoe UI, Arial, sans-serif" font-size="18">No data</text>',
                    "</svg>",
                ]
            ),
            encoding="utf-8",
        )
        return
    values = [value for _, value in bars]
    max_abs = max(abs(value) for value in values) or 1.0
    zero_x = width / 2
    scale = (width / 2 - 180) / max_abs
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<style>text{font-family:Segoe UI, Arial, sans-serif;font-size:12px;fill:#111827}</style>',
        f'<text x="16" y="24" font-size="16" font-weight="700">{title}</text>',
        f'<line x1="{zero_x}" y1="44" x2="{zero_x}" y2="{height - 18}" stroke="#9ca3af" stroke-width="1" />',
    ]
    for index, (label, value) in enumerate(bars):
        top = 46 + (index * 28)
        bar_width = abs(value) * scale
        x = zero_x if value >= 0 else zero_x - bar_width
        color = "#0a7f5a" if value >= 0 else "#b42318"
        lines.append(f'<text x="16" y="{top + 14}">{label}</text>')
        lines.append(f'<rect x="{x:.2f}" y="{top}" width="{bar_width:.2f}" height="18" rx="3" fill="{color}" />')
        lines.append(f'<text x="{zero_x + 8}" y="{top + 14}">{value:.2f}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def _heat_color(value: float, min_value: float, max_value: float) -> str:
    if math.isclose(min_value, max_value):
        return "#e5e7eb"
    midpoint = 0.0
    if value >= midpoint:
        intensity = 0.0 if max_value <= midpoint else min((value - midpoint) / max(max_value - midpoint, 1e-9), 1.0)
        red = int(232 - (120 * intensity))
        green = int(245 - (40 * intensity))
        blue = int(233 - (120 * intensity))
    else:
        intensity = 0.0 if min_value >= midpoint else min((midpoint - value) / max(midpoint - min_value, 1e-9), 1.0)
        red = int(254 - (20 * intensity))
        green = int(226 - (140 * intensity))
        blue = int(226 - (140 * intensity))
    return f"#{red:02x}{green:02x}{blue:02x}"


def _window_id(window: dict[str, object]) -> str:
    index = int(window.get("window_index", 0))
    return f"wf_{index:02d}"


def _json_cell(payload: Any) -> str:
    if payload in (None, "", {}):
        return ""
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _round_or_blank(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float) and not math.isfinite(value):
        return "inf" if value > 0 else "-inf"
    if isinstance(value, (int, float)):
        return round(float(value), 4)
    return value


def _safe_stat(values: list[float], mode: str) -> float | None:
    if not values:
        return None
    if mode == "mean":
        return statistics.mean(values)
    if mode == "median":
        return statistics.median(values)
    if mode == "pstdev":
        return statistics.pstdev(values) if len(values) > 1 else 0.0
    raise ValueError(f"unsupported stat mode: {mode}")


def _single_window_dependency(windows: list[dict[str, object]]) -> dict[str, object]:
    positive_windows = [
        (
            window.get("window_id") or _window_id(window),
            float(window.get("oos_metrics", {}).get("net_pnl", 0.0)),
        )
        for window in windows
        if float(window.get("oos_metrics", {}).get("net_pnl", 0.0)) > 0
    ]
    total_positive = sum(value for _, value in positive_windows)
    if not positive_windows or total_positive <= 0:
        return {"window_id": None, "share": None, "warning": False}
    window_id, value = max(positive_windows, key=lambda item: item[1])
    share = value / total_positive
    return {"window_id": window_id, "share": share, "warning": share >= 0.5}


def _overfit_signals(windows: list[dict[str, object]]) -> list[str]:
    signals: list[str] = []
    negative_after_positive = [
        window for window in windows if float(window.get("is_metrics", {}).get("net_pnl", 0.0)) > 0 and float(window.get("oos_metrics", {}).get("net_pnl", 0.0)) < 0
    ]
    if negative_after_positive:
        signals.append(
            f"{len(negative_after_positive)} windows had positive IS pnl but negative OOS pnl."
        )
    high_ratio = [
        window
        for window in windows
        if isinstance(window.get("is_oos_ratio"), (int, float)) and float(window["is_oos_ratio"]) > 3.0
    ]
    if high_ratio:
        signals.append(
            f"{len(high_ratio)} windows showed IS/OOS ratio above 3.0, which can indicate fragile fit."
        )
    sharp_windows = [window for window in windows if window.get("parameter_stability_warning")]
    if sharp_windows:
        signals.append(
            f"{len(sharp_windows)} windows flagged parameter sensitivity versus nearby candidates."
        )
    return signals


def _next_minimal_change(windows: list[dict[str, object]], overfit_signals: list[str]) -> str:
    if any(window.get("parameter_stability_warning") for window in windows):
        return "Probe only the nearest in-sample neighbors to confirm the parameter surface is not too sharp."
    if any(window.get("single_window_dependency_flag") for window in windows):
        return "Recheck only the conditions that dominate the single largest OOS window contribution."
    if overfit_signals:
        return "Keep entries fixed and make the smallest possible exit-only change, such as stop or time-stop."
    return "Run the same candidate set in both rolling and expanding modes and inspect only the windows that diverge."
