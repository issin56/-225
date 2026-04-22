from __future__ import annotations

from dataclasses import dataclass

from src.backtest.models import BacktestConfig, Candle, SignalAction, SignalEvent, SignalSnapshot
from src.strategy.base import StrategyDefinition, StrategyRuntime


def _lookback_period(config: BacktestConfig) -> int:
    raw_value = config.strategy.parameters.get("lookback_period", 5)
    if not isinstance(raw_value, int) or raw_value < 2:
        raise ValueError("'strategy.parameters.lookback_period' must be an integer >= 2 for breakout strategy.")
    return raw_value


@dataclass(slots=True)
class BreakoutRuntime(StrategyRuntime):
    candles: list[Candle]
    lookback_period: int

    def action_at(self, index: int) -> SignalAction | None:
        if index < self.lookback_period or index >= len(self.candles):
            return None

        current = self.candles[index]
        previous_window = self.candles[index - self.lookback_period : index]
        highest_high = max(candle.high for candle in previous_window)
        lowest_low = min(candle.low for candle in previous_window)

        if current.close > highest_high:
            return "buy"
        if current.close < lowest_low:
            return "sell"
        return None

    def snapshot_at(self, index: int) -> SignalSnapshot:
        if index < 0 or index >= len(self.candles):
            raise IndexError("Signal snapshot index is out of range.")

        candle = self.candles[index]
        action = self.action_at(index)
        if action is None:
            reason = "insufficient_history" if index < self.lookback_period else "no_breakout"
            return SignalSnapshot(
                timestamp=candle.timestamp,
                close_price=candle.close,
                short_ma=None,
                long_ma=None,
                signal=None,
                reason=reason,
            )

        side = "long" if action == "buy" else "short"
        signal = SignalEvent(
            timestamp=candle.timestamp,
            action=action,
            side=side,
            price=candle.close,
            short_ma=float(self.lookback_period),
            long_ma=float(self.lookback_period),
            reason="price_breakout",
        )
        return SignalSnapshot(
            timestamp=candle.timestamp,
            close_price=candle.close,
            short_ma=None,
            long_ma=None,
            signal=signal,
            reason="signal_detected",
        )


class BreakoutStrategy(StrategyDefinition):
    name = "breakout"

    def minimum_candles(self, config: BacktestConfig) -> int:
        return _lookback_period(config) + 1

    def prepare(self, candles: list[Candle], config: BacktestConfig) -> StrategyRuntime:
        return BreakoutRuntime(candles=candles, lookback_period=_lookback_period(config))
