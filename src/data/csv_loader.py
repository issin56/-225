from __future__ import annotations

import csv
from datetime import datetime
from math import isfinite
from pathlib import Path

from src.backtest.models import Candle
from src.utils.errors import DataValidationError


REQUIRED_COLUMNS = {"timestamp", "open", "high", "low", "close", "volume"}


def _parse_timestamp(value: str, row_number: int) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise DataValidationError(f"Row {row_number}: invalid timestamp '{value}'.") from error


def _parse_float(value: str, column_name: str, row_number: int) -> float:
    if value == "":
        raise DataValidationError(f"Row {row_number}: missing value in '{column_name}'.")
    try:
        numeric_value = float(value)
    except ValueError as error:
        raise DataValidationError(f"Row {row_number}: invalid numeric value in '{column_name}'.") from error
    if not isfinite(numeric_value):
        raise DataValidationError(f"Row {row_number}: non-finite numeric value in '{column_name}'.")
    return numeric_value


def load_ohlcv_csv(path: str | Path) -> list[Candle]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise DataValidationError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - fieldnames
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise DataValidationError(f"CSV is missing required columns: {missing}")

        candles: list[Candle] = []
        previous_timestamp: datetime | None = None

        for row_number, row in enumerate(reader, start=2):
            timestamp = _parse_timestamp(row["timestamp"], row_number)
            open_price = _parse_float(row["open"], "open", row_number)
            high_price = _parse_float(row["high"], "high", row_number)
            low_price = _parse_float(row["low"], "low", row_number)
            close_price = _parse_float(row["close"], "close", row_number)
            volume = _parse_float(row["volume"], "volume", row_number)

            if high_price < max(open_price, close_price) or low_price > min(open_price, close_price):
                raise DataValidationError(
                    f"Row {row_number}: OHLC values are inconsistent with candle high/low."
                )
            if previous_timestamp is not None and timestamp <= previous_timestamp:
                raise DataValidationError("Timestamps must be strictly increasing.")

            candles.append(
                Candle(
                    timestamp=timestamp,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=volume,
                )
            )
            previous_timestamp = timestamp

    if not candles:
        raise DataValidationError("CSV does not contain any rows.")
    return candles
