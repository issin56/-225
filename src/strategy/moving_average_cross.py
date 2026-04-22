from __future__ import annotations

from dataclasses import dataclass

from src.backtest.models import BacktestConfig, Candle, SignalAction, SignalEvent, SignalSnapshot
from src.strategy.base import StrategyDefinition, StrategyRuntime


def moving_average_series(values: list[float], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("Moving average period must be positive.")

    result: list[float | None] = []
    rolling_sum = 0.0
    for index, value in enumerate(values):
        rolling_sum += value
        if index >= period:
            rolling_sum -= values[index - period]
        if index + 1 < period:
            result.append(None)
        else:
            result.append(rolling_sum / period)
    return result


def detect_cross_signal(
    short_prev: float | None,
    short_curr: float | None,
    long_prev: float | None,
    long_curr: float | None,
) -> SignalAction | None:
    if None in {short_prev, short_curr, long_prev, long_curr}:
        return None
    if short_prev <= long_prev and short_curr > long_curr:
        return "buy"
    if short_prev >= long_prev and short_curr < long_curr:
        return "sell"
    return None


@dataclass(slots=True)
class MovingAverageCrossRuntime(StrategyRuntime):
    candles: list[Candle]
    short_ma: list[float | None]
    long_ma: list[float | None]

    def action_at(self, index: int) -> SignalAction | None:
        if index <= 0 or index >= len(self.candles):
            return None
        return detect_cross_signal(
            short_prev=self.short_ma[index - 1],
            short_curr=self.short_ma[index],
            long_prev=self.long_ma[index - 1],
            long_curr=self.long_ma[index],
        )

    def snapshot_at(self, index: int) -> SignalSnapshot:
        if index < 0 or index >= len(self.candles):
            raise IndexError("Signal snapshot index is out of range.")

        candle = self.candles[index]
        short_ma = self.short_ma[index]
        long_ma = self.long_ma[index]

        if index == 0:
            return SignalSnapshot(
                timestamp=candle.timestamp,
                close_price=candle.close,
                short_ma=short_ma,
                long_ma=long_ma,
                signal=None,
                reason="insufficient_history",
            )

        action = self.action_at(index)
        if action is None:
            reason = "insufficient_history" if short_ma is None or long_ma is None else "no_cross"
            return SignalSnapshot(
                timestamp=candle.timestamp,
                close_price=candle.close,
                short_ma=short_ma,
                long_ma=long_ma,
                signal=None,
                reason=reason,
            )

        side = "long" if action == "buy" else "short"
        signal = SignalEvent(
            timestamp=candle.timestamp,
            action=action,
            side=side,
            price=candle.close,
            short_ma=short_ma,
            long_ma=long_ma,
            reason="moving_average_cross",
        )
        return SignalSnapshot(
            timestamp=candle.timestamp,
            close_price=candle.close,
            short_ma=short_ma,
            long_ma=long_ma,
            signal=signal,
            reason="signal_detected",
        )


class MovingAverageCrossStrategy(StrategyDefinition):
    name = "moving_average_cross"

    def minimum_candles(self, config: BacktestConfig) -> int:
        return config.strategy.long_ma_period + 2

    def prepare(self, candles: list[Candle], config: BacktestConfig) -> StrategyRuntime:
        closes = [candle.close for candle in candles]
        return MovingAverageCrossRuntime(
            candles=candles,
            short_ma=moving_average_series(closes, config.strategy.short_ma_period),
            long_ma=moving_average_series(closes, config.strategy.long_ma_period),
        )
