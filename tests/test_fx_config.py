from __future__ import annotations

import unittest

from src.utils.config import load_backtest_config


class FxConfigTests(unittest.TestCase):
    def test_loads_multi_source_and_strategy_parameters(self) -> None:
        config = load_backtest_config("config/papertrade.multi.sample.json")

        self.assertEqual(len(config.data_sources), 2)
        self.assertEqual(config.data_sources[1].symbol, "GBP_USD")
        self.assertEqual(config.walk_forward.test_bars, 8)
        self.assertEqual(config.walk_forward.top_candidates_per_window, 3)
        self.assertEqual(config.walk_forward.search_space["short_ma_period"]["radius"], 1)

    def test_loads_breakout_parameters(self) -> None:
        config = load_backtest_config("config/backtest.breakout.sample.json")

        self.assertEqual(config.strategy.name, "breakout")
        self.assertEqual(config.strategy.parameters["lookback_period"], 4)
        self.assertEqual(config.walk_forward.training_bars, 6)
        self.assertEqual(config.walk_forward.top_candidates_per_window, 2)
        self.assertTrue(config.walk_forward.search_space["parameters.lookback_period"]["around_current"])


if __name__ == "__main__":
    unittest.main()
