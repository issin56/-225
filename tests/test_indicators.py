from datetime import datetime, timedelta

from kanekasegi.indicators import atr, ema
from kanekasegi.types import MarketCandle


def make_candles(count: int) -> list[MarketCandle]:
    candles = []
    now = datetime(2024, 1, 1)
    for i in range(count):
        price = 100 + i
        candles.append(
            MarketCandle(
                timestamp=now + timedelta(minutes=15 * i),
                open=price,
                high=price + 2,
                low=price - 1,
                close=price + 1,
                volume=10,
            )
        )
    return candles


def test_ema_is_deterministic():
    values = [float(v) for v in range(1, 250)]
    assert round(ema(values, 20), 6) == round(ema(values, 20), 6)


def test_atr_returns_positive_value():
    candles = make_candles(40)
    assert atr(candles, 14) > 0
