from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime
from math import isfinite
from pathlib import Path

from src.backtest.models import BacktestSummary, EquityPoint, NotificationEvent, PeriodPerformance, SignalEvent, SignalSnapshot, Trade


def _ensure_parent(path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def _sanitize_json_payload(payload):
    if isinstance(payload, dict):
        return {key: _sanitize_json_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [_sanitize_json_payload(item) for item in payload]
    if isinstance(payload, datetime):
        return payload.isoformat()
    if isinstance(payload, float):
        return payload if isfinite(payload) else None
    return payload


def write_trades_csv(path: str | Path, trades: list[Trade]) -> None:
    destination = _ensure_parent(path)
    fieldnames = [
        "side",
        "entry_time",
        "exit_time",
        "entry_price",
        "exit_price",
        "units",
        "gross_pnl",
        "net_pnl",
        "commission_paid",
        "exit_reason",
    ]
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for trade in trades:
            writer.writerow(
                {
                    "side": trade.side,
                    "entry_time": trade.entry_time.isoformat(),
                    "exit_time": trade.exit_time.isoformat(),
                    "entry_price": trade.entry_price,
                    "exit_price": trade.exit_price,
                    "units": trade.units,
                    "gross_pnl": trade.gross_pnl,
                    "net_pnl": trade.net_pnl,
                    "commission_paid": trade.commission_paid,
                    "exit_reason": trade.exit_reason,
                }
            )


def write_equity_curve_csv(path: str | Path, equity_curve: list[EquityPoint]) -> None:
    destination = _ensure_parent(path)
    fieldnames = ["timestamp", "equity", "drawdown"]
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for point in equity_curve:
            writer.writerow(
                {
                    "timestamp": point.timestamp.isoformat(),
                    "equity": point.equity,
                    "drawdown": point.drawdown,
                }
            )


def write_summary_json(path: str | Path, summary: BacktestSummary) -> None:
    destination = _ensure_parent(path)
    payload = _sanitize_json_payload(asdict(summary))
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_payload_json(path: str | Path, payload) -> None:
    destination = _ensure_parent(path)
    sanitized = _sanitize_json_payload(payload)
    destination.write_text(json.dumps(sanitized, ensure_ascii=False, indent=2), encoding="utf-8")


def write_period_summary_csv(path: str | Path, periods: list[PeriodPerformance]) -> None:
    destination = _ensure_parent(path)
    fieldnames = [
        "period_key",
        "trade_count",
        "total_pnl",
        "win_rate",
        "profit_factor",
        "average_trade_pnl",
        "max_drawdown",
    ]
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for period in periods:
            writer.writerow(_sanitize_json_payload(asdict(period)))


def write_period_summary_json(path: str | Path, periods: list[PeriodPerformance]) -> None:
    payload = [_sanitize_json_payload(asdict(period)) for period in periods]
    write_payload_json(path, payload)


def write_signal_snapshot_json(path: str | Path, snapshot: SignalSnapshot) -> None:
    destination = _ensure_parent(path)
    signal_payload = None
    if snapshot.signal is not None:
        signal_payload = {
            "timestamp": snapshot.signal.timestamp.isoformat(),
            "action": snapshot.signal.action,
            "side": snapshot.signal.side,
            "price": snapshot.signal.price,
            "short_ma": snapshot.signal.short_ma,
            "long_ma": snapshot.signal.long_ma,
            "reason": snapshot.signal.reason,
        }

    payload = _sanitize_json_payload(
        {
            "timestamp": snapshot.timestamp.isoformat(),
            "close_price": snapshot.close_price,
            "short_ma": snapshot.short_ma,
            "long_ma": snapshot.long_ma,
            "reason": snapshot.reason,
            "signal": signal_payload,
        }
    )
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_signal_history_csv(path: str | Path, signal: SignalEvent) -> None:
    destination = _ensure_parent(path)
    fieldnames = ["timestamp", "action", "side", "price", "short_ma", "long_ma", "reason"]
    file_exists = destination.exists()
    if file_exists:
        with destination.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if rows:
            last_row = rows[-1]
            if last_row["timestamp"] == signal.timestamp.isoformat() and last_row["action"] == signal.action:
                return
    with destination.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": signal.timestamp.isoformat(),
                "action": signal.action,
                "side": signal.side,
                "price": signal.price,
                "short_ma": signal.short_ma,
                "long_ma": signal.long_ma,
                "reason": signal.reason,
            }
        )


def append_notification_jsonl(path: str | Path, notification: NotificationEvent) -> None:
    destination = _ensure_parent(path)
    payload = {
        "timestamp": notification.timestamp.isoformat(),
        "symbol": notification.symbol,
        "severity": notification.severity,
        "title": notification.title,
        "message": notification.message,
    }
    with destination.open("a", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_scan_summary_json(path: str | Path, payload: list[dict[str, object]]) -> None:
    write_payload_json(path, payload)
