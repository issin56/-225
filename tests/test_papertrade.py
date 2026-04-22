from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.backtest.models import BacktestConfig, Candle, OutputConfig, PaperTradeState, RiskConfig, StrategyConfig
from src.papertrade.notifications import build_notification
from src.papertrade.service import (
    build_signal_snapshot,
    create_initial_paper_trade_state,
    evaluate_paper_trade_decision,
)
from src.papertrade.storage import load_paper_trade_state, save_paper_trade_state


def build_test_config() -> BacktestConfig:
    return BacktestConfig(
        data_file=Path("tests/fixtures/sample_ohlcv.csv"),
        strategy=StrategyConfig(name="moving_average_cross", short_ma_period=2, long_ma_period=3, allow_reversal=True),
        risk=RiskConfig(
            stop_loss=0.001,
            take_profit=0.002,
            spread=0.0002,
            commission=0.0,
            initial_capital=10000.0,
            risk_per_trade=0.01,
            max_consecutive_losses=None,
            max_drawdown=None,
        ),
        output=OutputConfig(
            directory=Path("output"),
            trades_file="trades.csv",
            summary_file="summary.json",
            equity_curve_file="equity_curve.csv",
            signal_snapshot_file="signal_snapshot.json",
            signal_history_file="signal_history.csv",
            papertrade_state_file="papertrade_state.json",
            papertrade_journal_file="papertrade_journal.jsonl",
        ),
    )


def build_candles(closes: list[float], *, start_offset_hours: int = 0) -> list[Candle]:
    start = datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(hours=start_offset_hours)
    candles: list[Candle] = []
    for index, close in enumerate(closes):
        candles.append(
            Candle(
                timestamp=start + timedelta(hours=index),
                open=close,
                high=close + 0.0005,
                low=close - 0.0005,
                close=close,
                volume=1000.0,
            )
        )
    return candles


class PaperTradeTests(unittest.TestCase):
    def test_builds_buy_signal_snapshot(self) -> None:
        snapshot = build_signal_snapshot(build_candles([10.0, 9.0, 8.0, 7.0, 8.0, 10.0]), build_test_config())

        self.assertEqual(snapshot.reason, "signal_detected")
        self.assertIsNotNone(snapshot.signal)
        assert snapshot.signal is not None
        self.assertEqual(snapshot.signal.action, "buy")
        self.assertEqual(snapshot.signal.side, "long")

    def test_returns_no_signal_snapshot(self) -> None:
        snapshot = build_signal_snapshot(build_candles([10.0, 10.1, 10.2, 10.3, 10.4]), build_test_config())

        self.assertEqual(snapshot.reason, "no_cross")
        self.assertIsNone(snapshot.signal)

    def test_decision_opens_then_skips_duplicate_then_flips(self) -> None:
        state = create_initial_paper_trade_state()
        opening_snapshot = build_signal_snapshot(build_candles([10.0, 9.0, 8.0, 7.0, 8.0, 10.0]), build_test_config())
        opening_decision, next_state = evaluate_paper_trade_decision(
            opening_snapshot,
            state,
            allow_reversal=True,
        )

        self.assertEqual(opening_decision.action, "open_long")
        self.assertEqual(next_state.current_side, "long")

        duplicate_decision, duplicate_state = evaluate_paper_trade_decision(
            opening_snapshot,
            next_state,
            allow_reversal=True,
        )

        self.assertEqual(duplicate_decision.action, "hold")
        self.assertEqual(duplicate_decision.reason, "duplicate_candle")
        self.assertEqual(duplicate_state.current_side, "long")

        flip_snapshot = build_signal_snapshot(
            build_candles([7.0, 8.0, 9.0, 10.0, 9.0, 7.0], start_offset_hours=10),
            build_test_config(),
        )
        flip_decision, flipped_state = evaluate_paper_trade_decision(
            flip_snapshot,
            next_state,
            allow_reversal=True,
        )

        self.assertEqual(flip_decision.action, "flip_to_short")
        self.assertEqual(flipped_state.current_side, "short")

    def test_decision_closes_only_when_reversal_disabled(self) -> None:
        opening_snapshot = build_signal_snapshot(build_candles([10.0, 9.0, 8.0, 7.0, 8.0, 10.0]), build_test_config())
        flip_snapshot = build_signal_snapshot(
            build_candles([7.0, 8.0, 9.0, 10.0, 9.0, 7.0], start_offset_hours=10),
            build_test_config(),
        )
        state = PaperTradeState(
            last_processed_timestamp=opening_snapshot.timestamp,
            current_side="long",
            last_action="open_long",
        )

        decision, next_state = evaluate_paper_trade_decision(
            flip_snapshot,
            state,
            allow_reversal=False,
        )

        self.assertEqual(decision.action, "close_long")
        self.assertIsNone(next_state.current_side)

    def test_saves_and_loads_paper_trade_state(self) -> None:
        state = PaperTradeState(
            last_processed_timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
            current_side="short",
            last_action="open_short",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "papertrade_state_test.json"
            save_paper_trade_state(temp_path, state)
            loaded = load_paper_trade_state(temp_path)

            self.assertEqual(loaded, state)

    def test_builds_notification_only_for_actionable_decision(self) -> None:
        snapshot = build_signal_snapshot(build_candles([10.0, 9.0, 8.0, 7.0, 8.0, 10.0]), build_test_config())
        decision, _ = evaluate_paper_trade_decision(
            snapshot,
            create_initial_paper_trade_state(),
            allow_reversal=True,
        )

        notification = build_notification("EUR_USD", snapshot, decision)

        self.assertIsNotNone(notification)
        assert notification is not None
        self.assertEqual(notification.symbol, "EUR_USD")
        self.assertIn("open_long", notification.title)


if __name__ == "__main__":
    unittest.main()
