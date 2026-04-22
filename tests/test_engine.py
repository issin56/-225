from __future__ import annotations

import unittest

from src.backtest.engine import calculate_trade_pnl, run_backtest
from src.data.csv_loader import load_ohlcv_csv
from src.utils.config import load_backtest_config


class EngineTests(unittest.TestCase):
    def test_calculates_trade_pnl_with_commission(self) -> None:
        gross_pnl, net_pnl = calculate_trade_pnl(
            side="long",
            entry_price=1.1000,
            exit_price=1.1015,
            units=10000,
            commission=2.5,
        )

        self.assertAlmostEqual(gross_pnl, 15.0)
        self.assertAlmostEqual(net_pnl, 10.0)

    def test_runs_backtest_on_sample_data(self) -> None:
        config = load_backtest_config("config/backtest.sample.json")
        candles = load_ohlcv_csv(config.data_file)
        result = run_backtest(candles, config)

        self.assertGreaterEqual(len(result.trades), 1)
        self.assertGreater(result.final_capital, 0.0)


if __name__ == "__main__":
    unittest.main()

