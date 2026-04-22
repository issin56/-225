from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.analysis.reporting import (
    append_notification_jsonl,
    append_signal_history_csv,
    write_period_summary_csv,
    write_period_summary_json,
    write_signal_snapshot_json,
    write_summary_json,
)
from src.backtest.models import BacktestSummary, NotificationEvent, PeriodPerformance, SignalEvent, SignalSnapshot


class OutputTests(unittest.TestCase):
    def test_writes_json_safe_summary(self) -> None:
        summary = BacktestSummary(
            initial_capital=10000.0,
            final_capital=10100.0,
            total_pnl=100.0,
            win_rate=1.0,
            payoff_ratio=float("inf"),
            profit_factor=float("inf"),
            max_drawdown=0.0,
            trade_count=1,
            average_profit=100.0,
            average_loss=0.0,
            max_winning_streak=1,
            max_losing_streak=0,
            stopped_early=False,
            stop_reason=None,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "summary.json"
            write_summary_json(path, summary)
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertIsNone(payload["payoff_ratio"])
        self.assertIsNone(payload["profit_factor"])

    def test_writes_signal_snapshot_and_deduplicates_history(self) -> None:
        timestamp = datetime(2025, 1, 1, tzinfo=timezone.utc)
        signal = SignalEvent(
            timestamp=timestamp,
            action="buy",
            side="long",
            price=1.101,
            short_ma=1.1,
            long_ma=1.099,
            reason="moving_average_cross",
        )
        snapshot = SignalSnapshot(
            timestamp=timestamp,
            close_price=1.101,
            short_ma=1.1,
            long_ma=1.099,
            signal=signal,
            reason="signal_detected",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            snapshot_path = Path(temp_dir) / "signal_snapshot.json"
            history_path = Path(temp_dir) / "signal_history.csv"
            write_signal_snapshot_json(snapshot_path, snapshot)
            append_signal_history_csv(history_path, signal)
            append_signal_history_csv(history_path, signal)

            snapshot_payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
            history_rows = history_path.read_text(encoding="utf-8").strip().splitlines()

        self.assertEqual(snapshot_payload["signal"]["action"], "buy")
        self.assertEqual(len(history_rows), 2)

    def test_writes_period_summary_and_notifications(self) -> None:
        periods = [
            PeriodPerformance(
                period_key="2025-01",
                trade_count=2,
                total_pnl=100.0,
                win_rate=0.5,
                profit_factor=2.0,
                average_trade_pnl=50.0,
                max_drawdown=0.1,
            )
        ]
        notification = NotificationEvent(
            timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
            symbol="EUR_USD",
            severity="info",
            title="EUR_USD open_long",
            message="new_signal_open; signal=buy @ 1.10000",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "periods.csv"
            json_path = Path(temp_dir) / "periods.json"
            notification_path = Path(temp_dir) / "notifications.jsonl"
            write_period_summary_csv(csv_path, periods)
            write_period_summary_json(json_path, periods)
            append_notification_jsonl(notification_path, notification)

            csv_lines = csv_path.read_text(encoding="utf-8").strip().splitlines()
            json_payload = json.loads(json_path.read_text(encoding="utf-8"))
            notification_lines = notification_path.read_text(encoding="utf-8").strip().splitlines()

        self.assertEqual(len(csv_lines), 2)
        self.assertEqual(json_payload[0]["period_key"], "2025-01")
        self.assertEqual(len(notification_lines), 1)


if __name__ == "__main__":
    unittest.main()
