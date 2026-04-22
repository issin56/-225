from __future__ import annotations

import unittest

from src.analysis.compare import compare_backtests
from src.utils.config import load_backtest_config


class CompareTests(unittest.TestCase):
    def test_compares_multiple_configs(self) -> None:
        config_specs = [
            ("config/backtest.sample.json", load_backtest_config("config/backtest.sample.json")),
            ("config/backtest.breakout.sample.json", load_backtest_config("config/backtest.breakout.sample.json")),
        ]

        results = compare_backtests(config_specs)

        self.assertEqual(len(results), 2)
        self.assertIn(results[0].strategy_name, {"moving_average_cross", "breakout"})
        self.assertGreaterEqual(results[0].total_pnl, results[-1].total_pnl)

    def test_compares_specific_symbol(self) -> None:
        config_specs = [
            ("config/papertrade.multi.sample.json", load_backtest_config("config/papertrade.multi.sample.json")),
        ]

        results = compare_backtests(config_specs, symbol="GBP_USD")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].symbol, "GBP_USD")


if __name__ == "__main__":
    unittest.main()
