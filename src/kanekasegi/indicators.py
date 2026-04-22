from __future__ import annotations

from collections import deque

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


def ema_series(values: list[float], period: int) -> list[float | None]:
    if not values:
        return []
    result: list[float | None] = [None] * len(values)
    if len(values) < period:
        return result

    multiplier = 2 / (period + 1)
    current = sum(values[:period]) / period
    result[period - 1] = current
    for index in range(period, len(values)):
        current = (values[index] - current) * multiplier + current
        result[index] = current
    return result


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


def atr_series(candles: list[MarketCandle], period: int) -> list[float | None]:
    if not candles:
        return []
    result: list[float | None] = [None] * len(candles)
    if len(candles) < period + 1:
        return result

    window: deque[float] = deque()
    window_sum = 0.0
    for index in range(1, len(candles)):
        current = candles[index]
        previous = candles[index - 1]
        true_range = max(
            current.high - current.low,
            abs(current.high - previous.close),
            abs(current.low - previous.close),
        )
        window.append(true_range)
        window_sum += true_range
        if len(window) > period:
            window_sum -= window.popleft()
        if len(window) == period:
            result[index] = window_sum / period
    return result


def highest_high(candles: list[MarketCandle], lookback: int) -> float:
    if len(candles) < lookback:
        raise ValueError("not enough candles for highest high")
    return max(c.high for c in candles[-lookback:])


def highest_high_series(candles: list[MarketCandle], lookback: int) -> list[float | None]:
    result: list[float | None] = [None] * len(candles)
    if lookback <= 0:
        return result

    highs = [candle.high for candle in candles]
    window: deque[int] = deque()
    for index, high in enumerate(highs):
        while window and highs[window[-1]] <= high:
            window.pop()
        window.append(index)
        while window and window[0] <= index - lookback:
            window.popleft()
        if index + 1 >= lookback:
            result[index] = highs[window[0]]
    return result


def lowest_low(candles: list[MarketCandle], lookback: int) -> float:
    if len(candles) < lookback:
        raise ValueError("not enough candles for lowest low")
    return min(c.low for c in candles[-lookback:])


def lowest_low_series(candles: list[MarketCandle], lookback: int) -> list[float | None]:
    result: list[float | None] = [None] * len(candles)
    if lookback <= 0:
        return result

    lows = [candle.low for candle in candles]
    window: deque[int] = deque()
    for index, low in enumerate(lows):
        while window and lows[window[-1]] >= low:
            window.pop()
        window.append(index)
        while window and window[0] <= index - lookback:
            window.popleft()
        if index + 1 >= lookback:
            result[index] = lows[window[0]]
    return result
