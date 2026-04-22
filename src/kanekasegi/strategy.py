from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time, timedelta

from .config import StrategyConfig
from .indicators import atr, closing_prices, ema, highest_high, lowest_low
from .types import MarketCandle, PositionState, SessionType, Signal, SignalAction

GOTOBI_DAYS = frozenset({5, 10, 15, 20, 25, 30})


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

        if self._direction_allows(SignalAction.LONG) and long_trend_ok and last_close >= breakout_high:
            stop_price = last_close - (current_atr * self.config.atr_stop_multiplier)
            return Signal(
                action=SignalAction.LONG,
                reason="trend_breakout_long",
                entry_price=last_close,
                stop_price=stop_price,
                trailing_distance=current_atr * self.config.trailing_atr_multiplier,
                metadata={"ema": trend_ema, "atr": current_atr},
            )
        if self._direction_allows(SignalAction.SHORT) and short_trend_ok and last_close <= breakout_low:
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
            if (
                last_close < trend_ema
                or (position.stop_price is not None and last_close <= position.stop_price)
                or (trailing_stop is not None and last_close <= trailing_stop)
            ):
                return Signal(action=SignalAction.EXIT, reason="long_exit_signal", metadata={"ema": trend_ema, "atr": current_atr})
            return Signal(action=SignalAction.HOLD, reason="hold_long", trailing_distance=trailing_distance, metadata={"trailing_stop": trailing_stop})
        if position.side == SignalAction.SHORT:
            trailing_stop = min(position.trailing_stop or position.stop_price or last_close, last_close + trailing_distance)
            if (
                last_close > trend_ema
                or (position.stop_price is not None and last_close >= position.stop_price)
                or (trailing_stop is not None and last_close >= trailing_stop)
            ):
                return Signal(action=SignalAction.EXIT, reason="short_exit_signal", metadata={"ema": trend_ema, "atr": current_atr})
            return Signal(action=SignalAction.HOLD, reason="hold_short", trailing_distance=trailing_distance, metadata={"trailing_stop": trailing_stop})
        return Signal(action=SignalAction.HOLD, reason="position_unknown")

    def _entry_filters_pass(self, candles: list[MarketCandle]) -> bool:
        candle = candles[-1]
        if candle.session is not None and candle.session.value not in set(self.config.allowed_sessions):
            return False
        if candle.timestamp.weekday() not in set(self.config.allowed_weekdays):
            return False
        if not self._supports_calendar_filter(candle.timestamp.date()):
            return False
        if not self._supports_prior_session_filter(candles):
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

    def _direction_allows(self, side: SignalAction) -> bool:
        if self.config.direction_filter == "long_only":
            return side == SignalAction.LONG
        if self.config.direction_filter == "short_only":
            return side == SignalAction.SHORT
        return True

    def _parse_clock(self, raw: str | None) -> time | None:
        if raw is None:
            return None
        return time(hour=int(raw[:2]), minute=int(raw[3:]))

    def _supports_calendar_filter(self, current_date: date) -> bool:
        if self.config.calendar_filter == "all":
            return True

        is_gotobi = current_date in self._business_gotobi_days(current_date.year, current_date.month)
        if self.config.calendar_filter == "gotobi_only":
            return is_gotobi
        if self.config.calendar_filter == "exclude_gotobi":
            return not is_gotobi
        is_sq = self._is_sq_day(current_date)
        if self.config.calendar_filter == "sq_only":
            return is_sq
        if self.config.calendar_filter == "exclude_sq":
            return not is_sq
        return False

    def _supports_prior_session_filter(self, candles: list[MarketCandle]) -> bool:
        if self.config.prior_session_filter == "all":
            return True

        previous_change = self._previous_session_change(candles)
        if previous_change is None:
            return False

        required_move = self.config.prior_session_min_move_ticks * self.config.tick_size
        if self.config.prior_session_filter == "up":
            return previous_change >= required_move
        if self.config.prior_session_filter == "down":
            return previous_change <= -required_move
        return False

    def _previous_session_change(self, candles: list[MarketCandle]) -> float | None:
        if len(candles) < 2:
            return None

        current_session = candles[-1].session
        previous_index = len(candles) - 2
        while previous_index >= 0 and candles[previous_index].session == current_session:
            previous_index -= 1
        if previous_index < 0:
            return None

        previous_session = candles[previous_index].session
        session_end = previous_index
        while previous_index >= 0 and candles[previous_index].session == previous_session:
            previous_index -= 1
        session_start = previous_index + 1
        if session_start > session_end:
            return None
        return candles[session_end].close - candles[session_start].open

    def _business_gotobi_days(self, year: int, month: int) -> set[date]:
        gotobi_days: set[date] = set()
        for raw_day in GOTOBI_DAYS:
            try:
                current = date(year, month, raw_day)
            except ValueError:
                continue
            while current.weekday() >= 5:
                current -= timedelta(days=1)
            gotobi_days.add(current)
        return gotobi_days

    def _is_sq_day(self, current_date: date) -> bool:
        return current_date == self._second_friday(current_date.year, current_date.month)

    def _second_friday(self, year: int, month: int) -> date:
        current = date(year, month, 1)
        while current.weekday() != 4:
            current += timedelta(days=1)
        return current + timedelta(days=7)
