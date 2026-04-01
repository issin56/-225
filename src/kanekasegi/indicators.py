from __future__ import annotations

from .types import MarketCandle


def closing_prices(candles: list[MarketCandle]) -> list[float]:
    return [c.close for c in candles]


def ema(values: list[float], period: int) -> float:
    if len(values) < period:
        raise ValueError("not enough values for EMA")
    multiplier = 2 / (period + 1)
    current = sum(values[:period]) / period
    for value in values[period:]:
        current = (value - current) * multiplier + current
    return current


def atr(candles: list[MarketCandle], period: int) -> float:
    if len(candles) < period + 1:
        raise ValueError("not enough candles for ATR")
    true_ranges: list[float] = []
    for idx in range(1, len(candles)):
        current = candles[idx]
        previous = candles[idx - 1]
        true_ranges.append(
            max(
                current.high - current.low,
                abs(current.high - previous.close),
                abs(current.low - previous.close),
            )
        )
    sample = true_ranges[-period:]
    return sum(sample) / len(sample)


def highest_high(candles: list[MarketCandle], lookback: int) -> float:
    if len(candles) < lookback:
        raise ValueError("not enough candles for highest high")
    return max(c.high for c in candles[-lookback:])


def lowest_low(candles: list[MarketCandle], lookback: int) -> float:
    if len(candles) < lookback:
        raise ValueError("not enough candles for lowest low")
    return min(c.low for c in candles[-lookback:])
