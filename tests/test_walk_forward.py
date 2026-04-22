from __future__ import annotations

import unittest

from src.analysis.walk_forward import run_walk_forward_validation
from src.data.csv_loader import load_ohlcv_csv
from src.utils.config import load_backtest_config


class WalkForwardTests(unittest.TestCase):
    def test_runs_walk_forward_validation(self) -> None:
        config = load_backtest_config("config/backtest.sample.json")
        candles = load_ohlcv_csv(config.data_file)

        report = run_walk_forward_validation(candles, config)

        self.assertEqual(report.total_windows, 2)
        self.assertEqual(len(report.windows), 2)
        self.assertGreaterEqual(report.pass_rate, 0.0)
        self.assertTrue(report.search_enabled)
        self.assertEqual(report.selection_metric, "total_pnl")
        self.assertEqual(report.windows[0].candidate_count, 6)
        self.assertIn("short_ma_period", report.windows[0].selected_parameters)
        self.assertEqual(len(report.windows[0].top_training_candidates), 3)
        self.assertEqual(report.windows[0].top_training_candidates[0].rank, 1)

    def test_runs_walk_forward_on_breakout_sample(self) -> None:
        config = load_backtest_config("config/backtest.breakout.sample.json")
        candles = load_ohlcv_csv(config.data_file)

        report = run_walk_forward_validation(candles, config)

        self.assertGreaterEqual(report.total_windows, 1)
        self.assertEqual(report.strategy_name, "breakout")
        self.assertIn("parameters.lookback_period", report.windows[0].selected_parameters)
        self.assertEqual(report.windows[0].candidate_count, 2)
        self.assertEqual(len(report.windows[0].top_training_candidates), 2)


if __name__ == "__main__":
    unittest.main()
