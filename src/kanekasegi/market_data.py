from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import Random

from .types import MarketCandle


@dataclass(slots=True)
class InMemoryMarketDataProvider:
    symbol: str
    timeframe: str
    seed: int = 7
    start_price: float = 30000.0
    _rng: Random = field(init=False, repr=False)
    _candles: list[MarketCandle] = field(init=False, repr=False)
    _cursor: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = Random(self.seed)
        self._candles = self._generate_candles(400)
        self._cursor = len(self._candles)

    def _generate_candles(self, count: int) -> list[MarketCandle]:
        candles: list[MarketCandle] = []
        price = self.start_price
        ts = datetime.utcnow() - timedelta(minutes=count * 15)
        for _ in range(count):
            drift = self._rng.uniform(-0.008, 0.012)
            open_price = price
            close_price = max(1.0, price * (1 + drift))
            high_price = max(open_price, close_price) * (1 + self._rng.uniform(0.0005, 0.003))
            low_price = min(open_price, close_price) * (1 - self._rng.uniform(0.0005, 0.003))
            volume = self._rng.uniform(10, 300)
            candles.append(
                MarketCandle(
                    timestamp=ts,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=volume,
                )
            )
            ts += timedelta(minutes=15)
            price = close_price
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

    def all_candles(self, symbol: str, timeframe: str) -> list[MarketCandle]:
        if symbol != self.symbol or timeframe != self.timeframe:
            raise ValueError("unsupported symbol or timeframe")
        return list(self._candles)

    def total_candles(self) -> int:
        return len(self._candles)
