from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from src.analysis.periods import summarize_periods
from src.backtest.metrics import calculate_drawdown, summarize_backtest
from src.backtest.models import BacktestResult, EquityPoint, Trade


class MetricsTests(unittest.TestCase):
    def test_calculates_max_drawdown(self) -> None:
        max_drawdown = calculate_drawdown([10000.0, 10500.0, 10300.0, 9800.0, 11000.0])

        self.assertAlmostEqual(max_drawdown, (10500.0 - 9800.0) / 10500.0)

    def test_summarizes_trade_statistics(self) -> None:
        timestamp = datetime(2025, 1, 1, tzinfo=timezone.utc)
        result = BacktestResult(
            initial_capital=10000.0,
            final_capital=10090.0,
            trades=[
                Trade(
                    side="long",
                    entry_time=timestamp,
                    exit_time=timestamp,
                    entry_price=1.1,
                    exit_price=1.102,
                    units=10000,
                    gross_pnl=20.0,
                    net_pnl=15.0,
                    commission_paid=5.0,
                    exit_reason="take_profit",
                ),
                Trade(
                    side="short",
                    entry_time=timestamp,
                    exit_time=timestamp,
                    entry_price=1.102,
                    exit_price=1.104,
                    units=10000,
                    gross_pnl=-20.0,
                    net_pnl=-25.0,
                    commission_paid=5.0,
                    exit_reason="stop_loss",
                ),
                Trade(
                    side="short",
                    entry_time=timestamp,
                    exit_time=timestamp,
                    entry_price=1.104,
                    exit_price=1.096,
                    units=10000,
                    gross_pnl=80.0,
                    net_pnl=75.0,
                    commission_paid=5.0,
                    exit_reason="take_profit",
                ),
            ],
            equity_curve=[
                EquityPoint(timestamp=timestamp, equity=10000.0, drawdown=0.0),
                EquityPoint(timestamp=timestamp, equity=10015.0, drawdown=0.0),
                EquityPoint(timestamp=timestamp, equity=9990.0, drawdown=(10015.0 - 9990.0) / 10015.0),
                EquityPoint(timestamp=timestamp, equity=10090.0, drawdown=(10015.0 - 9990.0) / 10015.0),
            ],
            stopped_early=False,
            stop_reason=None,
        )

        summary = summarize_backtest(result)

        self.assertEqual(summary.trade_count, 3)
        self.assertAlmostEqual(summary.win_rate, 2 / 3)
        self.assertGreater(summary.profit_factor, 1.0)
        self.assertEqual(summary.max_winning_streak, 1)
        self.assertEqual(summary.max_losing_streak, 1)

    def test_summarizes_periods_by_month(self) -> None:
        january = datetime(2025, 1, 31, tzinfo=timezone.utc)
        february = datetime(2025, 2, 28, tzinfo=timezone.utc)
        result = BacktestResult(
            initial_capital=10000.0,
            final_capital=10150.0,
            trades=[
                Trade(
                    side="long",
                    entry_time=january - timedelta(days=1),
                    exit_time=january,
                    entry_price=1.1,
                    exit_price=1.101,
                    units=10000,
                    gross_pnl=10.0,
                    net_pnl=10.0,
                    commission_paid=0.0,
                    exit_reason="take_profit",
                ),
                Trade(
                    side="short",
                    entry_time=february - timedelta(days=1),
                    exit_time=february,
                    entry_price=1.101,
                    exit_price=1.099,
                    units=10000,
                    gross_pnl=20.0,
                    net_pnl=20.0,
                    commission_paid=0.0,
                    exit_reason="take_profit",
                ),
            ],
            equity_curve=[
                EquityPoint(timestamp=january - timedelta(days=2), equity=10000.0, drawdown=0.0),
                EquityPoint(timestamp=january, equity=10010.0, drawdown=0.0),
                EquityPoint(timestamp=february, equity=10030.0, drawdown=0.0),
            ],
            stopped_early=False,
            stop_reason=None,
        )

        periods = summarize_periods(result, period="month")

        self.assertEqual([item.period_key for item in periods], ["2025-01", "2025-02"])
        self.assertEqual(periods[0].trade_count, 1)
        self.assertAlmostEqual(periods[1].total_pnl, 20.0)


if __name__ == "__main__":
    unittest.main()
