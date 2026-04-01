from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .types import MarketCandle, SessionType


def _parse_timestamp(raw: str) -> datetime:
    normalized = raw.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported timestamp format: {raw}") from exc


@dataclass(slots=True)
class CsvMarketDataProvider:
    symbol: str
    timeframe: str
    csv_path: str
    _candles: list[MarketCandle] = field(init=False, repr=False)
    _cursor: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._candles = self._load_csv(Path(self.csv_path))
        if not self._candles:
            raise ValueError("csv data source is empty")
        self._cursor = len(self._candles)

    def _load_csv(self, path: Path) -> list[MarketCandle]:
        if not path.exists():
            raise FileNotFoundError(path)
        candles: list[MarketCandle] = []
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            required = {"timestamp", "open", "high", "low", "close", "volume"}
            if not reader.fieldnames or not required.issubset({name.strip() for name in reader.fieldnames}):
                raise ValueError("csv must include timestamp, open, high, low, close, volume columns")
            for row in reader:
                session_raw = row.get("session")
                candles.append(
                    MarketCandle(
                        timestamp=_parse_timestamp(row["timestamp"]),
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                        session=SessionType(session_raw) if session_raw in {item.value for item in SessionType} else None,
                        contract_month=row.get("contract_month") or None,
                        trading_day=row.get("trading_day") or None,
                    )
                )
        return candles

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int) -> list[MarketCandle]:
        if symbol != self.symbol or timeframe != self.timeframe:
            raise ValueError("unsupported symbol or timeframe")
        return self._candles[max(0, self._cursor - limit) : self._cursor]

    def get_ticker(self, symbol: str) -> float:
        if symbol != self.symbol:
            raise ValueError("unsupported symbol")
        return self._candles[self._cursor - 1].close

    def reset_for_backtest(self, warmup: int) -> None:
        if warmup <= 0 or warmup > len(self._candles):
            raise ValueError("invalid warmup")
        self._cursor = warmup

    def has_next(self) -> bool:
        return self._cursor < len(self._candles)

    def advance(self) -> bool:
        if not self.has_next():
            return False
        self._cursor += 1
        return True

    def total_candles(self) -> int:
        return len(self._candles)

    def all_candles(self, symbol: str, timeframe: str) -> list[MarketCandle]:
        if symbol != self.symbol or timeframe != self.timeframe:
            raise ValueError("unsupported symbol or timeframe")
        return list(self._candles)

    def describe(self) -> dict[str, object]:
        return {
            "candles": len(self._candles),
            "first_timestamp": self._candles[0].timestamp.isoformat(),
            "last_timestamp": self._candles[-1].timestamp.isoformat(),
            "trading_days": len({candle.trading_day for candle in self._candles if candle.trading_day}),
            "contract_months": sorted({candle.contract_month for candle in self._candles if candle.contract_month}),
            "sessions": sorted({candle.session.value for candle in self._candles if candle.session}),
            "timeframe": self.timeframe,
        }
