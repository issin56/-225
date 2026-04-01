from __future__ import annotations

from dataclasses import dataclass
from datetime import time

from .config import StrategyConfig
from .indicators import atr, closing_prices, ema, highest_high, lowest_low
from .types import MarketCandle, PositionState, SessionType, Signal, SignalAction


@dataclass(slots=True)
class MarketSnapshot:
    candles: list[MarketCandle]
    last_price: float


class BreakoutTrendStrategy:
    def __init__(self, config: StrategyConfig) -> None:
        self.config = config
        self.entry_start_time = self._parse_clock(config.entry_start_time)
        self.entry_end_time = self._parse_clock(config.entry_end_time)

    def generate_signal(self, market_snapshot: MarketSnapshot, portfolio_state: PositionState) -> Signal:
        candles = market_snapshot.candles
        min_required = max(self.config.ema_period, self.config.breakout_lookback + 1, self.config.atr_period + 1)
        if len(candles) < min_required:
            return Signal(action=SignalAction.HOLD, reason="insufficient_data", metadata={"candles": len(candles)})
        prices = closing_prices(candles)
        trend_ema = ema(prices, self.config.ema_period)
        current_atr = atr(candles, self.config.atr_period)
        breakout_high = highest_high(candles[:-1], self.config.breakout_lookback)
        breakout_low = lowest_low(candles[:-1], self.config.breakout_lookback)
        last_close = candles[-1].close

        if portfolio_state.is_open:
            return self._manage_open_position(portfolio_state, last_close, current_atr, trend_ema)

        if not self._entry_filters_pass(candles):
            return Signal(action=SignalAction.HOLD, reason="entry_filtered", metadata={"ema": trend_ema, "atr": current_atr})

        long_trend_ok = (last_close > trend_ema) if self.config.use_trend_filter else True
        short_trend_ok = (last_close < trend_ema) if self.config.use_trend_filter else True

        if long_trend_ok and last_close >= breakout_high:
            stop_price = last_close - (current_atr * self.config.atr_stop_multiplier)
            return Signal(
                action=SignalAction.LONG,
                reason="trend_breakout_long",
                entry_price=last_close,
                stop_price=stop_price,
                trailing_distance=current_atr * self.config.trailing_atr_multiplier,
                metadata={"ema": trend_ema, "atr": current_atr},
            )
        if short_trend_ok and last_close <= breakout_low:
            stop_price = last_close + (current_atr * self.config.atr_stop_multiplier)
            return Signal(
                action=SignalAction.SHORT,
                reason="trend_breakout_short",
                entry_price=last_close,
                stop_price=stop_price,
                trailing_distance=current_atr * self.config.trailing_atr_multiplier,
                metadata={"ema": trend_ema, "atr": current_atr},
            )
        return Signal(action=SignalAction.HOLD, reason="no_entry", metadata={"ema": trend_ema, "atr": current_atr})

    def _manage_open_position(
        self,
        position: PositionState,
        last_close: float,
        current_atr: float,
        trend_ema: float,
    ) -> Signal:
        trailing_distance = current_atr * self.config.trailing_atr_multiplier
        if position.side == SignalAction.LONG:
            trailing_stop = max(position.trailing_stop or position.stop_price or 0.0, last_close - trailing_distance)
            if last_close < trend_ema or (position.stop_price is not None and last_close <= position.stop_price):
                return Signal(action=SignalAction.EXIT, reason="long_exit_signal", metadata={"ema": trend_ema, "atr": current_atr})
            return Signal(action=SignalAction.HOLD, reason="hold_long", trailing_distance=trailing_distance, metadata={"trailing_stop": trailing_stop})
        if position.side == SignalAction.SHORT:
            trailing_stop = min(position.trailing_stop or position.stop_price or last_close, last_close + trailing_distance)
            if last_close > trend_ema or (position.stop_price is not None and last_close >= position.stop_price):
                return Signal(action=SignalAction.EXIT, reason="short_exit_signal", metadata={"ema": trend_ema, "atr": current_atr})
            return Signal(action=SignalAction.HOLD, reason="hold_short", trailing_distance=trailing_distance, metadata={"trailing_stop": trailing_stop})
        return Signal(action=SignalAction.HOLD, reason="position_unknown")

    def _entry_filters_pass(self, candles: list[MarketCandle]) -> bool:
        candle = candles[-1]
        if candle.session is not None and candle.session.value not in set(self.config.allowed_sessions):
            return False
        if candle.timestamp.weekday() not in set(self.config.allowed_weekdays):
            return False
        if self.entry_start_time is not None and candle.timestamp.time() < self.entry_start_time:
            return False
        if self.entry_end_time is not None and candle.timestamp.time() > self.entry_end_time:
            return False
        if self.config.skip_first_minutes > 0 and candle.session == SessionType.DAY:
            session_start = time(hour=8, minute=45)
            current_minutes = candle.timestamp.hour * 60 + candle.timestamp.minute
            start_minutes = session_start.hour * 60 + session_start.minute
            if current_minutes - start_minutes < self.config.skip_first_minutes:
                return False
        return True

    def _parse_clock(self, raw: str | None) -> time | None:
        if raw is None:
            return None
        return time(hour=int(raw[:2]), minute=int(raw[3:]))
