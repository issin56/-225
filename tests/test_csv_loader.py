from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.data.csv_loader import load_ohlcv_csv
from src.utils.errors import DataValidationError


class CsvLoaderTests(unittest.TestCase):
    def test_loads_valid_csv(self) -> None:
        candles = load_ohlcv_csv("tests/fixtures/sample_ohlcv.csv")

        self.assertGreater(len(candles), 0)
        self.assertEqual(candles[0].timestamp.isoformat(), "2025-01-01T00:00:00+00:00")

    def test_raises_for_missing_required_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "invalid.csv"
            csv_path.write_text(
                "timestamp,open,high,low,close\n"
                "2025-01-01T00:00:00+00:00,1.0,1.1,0.9,1.05\n",
                encoding="utf-8",
            )

            with self.assertRaises(DataValidationError):
                load_ohlcv_csv(csv_path)


if __name__ == "__main__":
    unittest.main()

