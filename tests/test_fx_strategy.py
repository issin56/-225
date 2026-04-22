from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.backtest.models import BacktestConfig, Candle, OutputConfig, RiskConfig, StrategyConfig
from src.strategy.moving_average_cross import detect_cross_signal, moving_average_series
from src.strategy.registry import get_strategy


class FxStrategyTests(unittest.TestCase):
    def test_calculates_simple_moving_average(self) -> None:
        series = moving_average_series([1.0, 2.0, 3.0, 4.0], 2)

        self.assertEqual(series, [None, 1.5, 2.5, 3.5])

    def test_detects_buy_and_sell_crosses(self) -> None:
        self.assertEqual(detect_cross_signal(1.0, 3.0, 2.0, 2.5), "buy")
        self.assertEqual(detect_cross_signal(3.0, 1.0, 2.0, 2.5), "sell")
        self.assertIsNone(detect_cross_signal(None, 1.0, 2.0, 2.0))

    def test_registry_builds_runtime_snapshot(self) -> None:
        start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        candles = [
            Candle(
                timestamp=start + timedelta(hours=index),
                open=close,
                high=close + 0.1,
                low=close - 0.1,
                close=close,
                volume=1000.0,
            )
            for index, close in enumerate([10.0, 9.0, 8.0, 7.0, 8.0, 10.0])
        ]
        config = BacktestConfig(
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

        runtime = get_strategy("moving_average_cross").prepare(candles, config)
        snapshot = runtime.snapshot_at(len(candles) - 1)

        self.assertEqual(snapshot.reason, "signal_detected")
        self.assertIsNotNone(snapshot.signal)

    def test_breakout_strategy_detects_signal(self) -> None:
        start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        candles = [
            Candle(
                timestamp=start + timedelta(hours=index),
                open=close,
                high=high,
                low=low,
                close=close,
                volume=1000.0,
            )
            for index, (close, high, low) in enumerate(
                [
                    (1.1000, 1.1005, 1.0995),
                    (1.1002, 1.1006, 1.0998),
                    (1.1001, 1.1004, 1.0997),
                    (1.1003, 1.1007, 1.1000),
                    (1.1015, 1.1018, 1.1008),
                ]
            )
        ]
        config = BacktestConfig(
            data_file=Path("tests/fixtures/sample_ohlcv.csv"),
            strategy=StrategyConfig(
                name="breakout",
                short_ma_period=2,
                long_ma_period=3,
                allow_reversal=True,
                parameters={"lookback_period": 4},
            ),
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
            ),
        )

        runtime = get_strategy("breakout").prepare(candles, config)
        snapshot = runtime.snapshot_at(len(candles) - 1)

        self.assertEqual(snapshot.reason, "signal_detected")
        self.assertEqual(snapshot.signal.action if snapshot.signal else None, "buy")


if __name__ == "__main__":
    unittest.main()
