from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta

from .config import AppConfig
from .external_factors import ExternalFactors
from .indicators import atr_series, closing_prices, ema_series, highest_high_series, lowest_low_series
from .observability import EnrichedTradeRecord, TradeSeed, build_trade_seed, finalize_trade_record
from .types import MarketCandle, SessionType, SignalAction

GOTOBI_DAYS = frozenset({5, 10, 15, 20, 25, 30})


@dataclass(slots=True)
class RuleCandidate:
    name: str
    breakout_lookback: int
    ema_period: int
    atr_period: int
    atr_stop_multiplier: float
    trailing_atr_multiplier: float
    timeframe: str = "15m"
    entry_mode: str = "breakout"
    entry_buffer_ticks: int = 0
    session_filter: str = "both"
    direction_filter: str = "both"
    allowed_weekdays: tuple[int, ...] = (0, 1, 2, 3, 4)
    excluded_months: tuple[int, ...] = ()
    calendar_filter: str = "all"
    prior_session_filter: str = "all"
    prior_session_min_move_ticks: int = 0
    prior_session_range_filter: str = "all"
    prior_session_min_range_ticks: int = 0
    external_factor_name: str | None = None
    external_factor_filter: str = "all"
    external_factor_min_value: float = 0.0
    secondary_external_factor_name: str | None = None
    secondary_external_factor_filter: str = "all"
    secondary_external_factor_min_value: float = 0.0
    entry_start_time: str | None = None
    entry_end_time: str | None = None
    skip_first_minutes: int = 0
    use_trend_filter: bool = True
    exit_on_trend_reversal: bool = True
    use_trailing_stop: bool = True
    fixed_stop_ticks: int | None = None
    take_profit_ticks: int | None = None
    time_stop_bars: int | None = None
    tick_size: float = 5.0


@dataclass(slots=True)
class RuleLabResult:
    name: str
    ending_equity: float
    profit: float
    trades: int
    wins: int
    losses: int
    win_rate: float
    max_drawdown: float
    min_available_balance: float
    profitable_months: int
    losing_months: int
    average_monthly_pnl: float
    active_months: int
    monthly_pnl: dict[str, float] = field(default_factory=dict)
    trade_records: list[EnrichedTradeRecord] = field(default_factory=list, repr=False)


def _parse_clock(raw: str | None) -> time | None:
    if raw is None:
        return None
    return time(hour=int(raw[:2]), minute=int(raw[3:]))


def _in_entry_window(candidate: RuleCandidate, candle: MarketCandle) -> bool:
    current_time = candle.timestamp.time()
    start_time = _parse_clock(candidate.entry_start_time)
    end_time = _parse_clock(candidate.entry_end_time)
    if start_time and end_time and start_time > end_time:
        return current_time >= start_time or current_time <= end_time
    if start_time and current_time < start_time:
        return False
    if end_time and current_time > end_time:
        return False
    return True


def _entry_date(candle: MarketCandle) -> date:
    if candle.trading_day:
        return date.fromisoformat(candle.trading_day)
    return candle.timestamp.date()


def _month_key(candle: MarketCandle) -> str:
    if candle.trading_day:
        return candle.trading_day[:7]
    return candle.timestamp.strftime("%Y-%m")


def _session_minutes_from_open(candle: MarketCandle) -> int | None:
    if candle.session == SessionType.DAY:
        session_open = time(hour=8, minute=45)
    elif candle.session == SessionType.NIGHT:
        session_open = time(hour=17, minute=0)
    else:
        return None
    return (candle.timestamp.hour * 60 + candle.timestamp.minute) - (session_open.hour * 60 + session_open.minute)


def _supports_calendar_filter(candidate: RuleCandidate, candle: MarketCandle) -> bool:
    if candidate.calendar_filter == "all":
        return True

    entry_date = _entry_date(candle)
    is_gotobi = _is_gotobi_day(entry_date)
    if candidate.calendar_filter == "gotobi_only":
        return is_gotobi
    if candidate.calendar_filter == "exclude_gotobi":
        return not is_gotobi
    is_sq = _is_sq_day(entry_date)
    if candidate.calendar_filter == "sq_only":
        return is_sq
    if candidate.calendar_filter == "exclude_sq":
        return not is_sq
    if candidate.calendar_filter == "exclude_sq_week":
        return not _is_sq_week(entry_date)
    if candidate.calendar_filter == "exclude_last_trading_window":
        return not _is_last_trading_window(candle)
    if candidate.calendar_filter == "exclude_roll_week":
        return not _is_roll_week(candle)
    if candidate.calendar_filter == "exclude_calendar_risk":
        return not (_is_sq_week(entry_date) or _is_last_trading_window(candle) or _is_roll_week(candle))
    raise ValueError(f"unsupported calendar_filter: {candidate.calendar_filter}")


def _supports_month_filter(candidate: RuleCandidate, candle: MarketCandle) -> bool:
    if not candidate.excluded_months:
        return True
    month = int(_month_key(candle)[5:7])
    return month not in candidate.excluded_months


def _business_gotobi_days(year: int, month: int) -> set[date]:
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


def _is_gotobi_day(current_date: date) -> bool:
    return current_date in _business_gotobi_days(current_date.year, current_date.month)


def _second_friday(year: int, month: int) -> date:
    current = date(year, month, 1)
    while current.weekday() != 4:
        current += timedelta(days=1)
    return current + timedelta(days=7)


def _is_sq_day(current_date: date) -> bool:
    return current_date == _second_friday(current_date.year, current_date.month)


def _business_day_before(current_date: date) -> date:
    previous = current_date - timedelta(days=1)
    while previous.weekday() >= 5:
        previous -= timedelta(days=1)
    return previous


def _is_sq_week(current_date: date) -> bool:
    sq_day = _second_friday(current_date.year, current_date.month)
    week_start = sq_day - timedelta(days=sq_day.weekday())
    week_end = week_start + timedelta(days=4)
    return week_start <= current_date <= week_end


def _contract_month_from_candle(candle: MarketCandle) -> tuple[int, int]:
    if candle.contract_month and len(candle.contract_month) >= 6:
        return int(candle.contract_month[:4]), int(candle.contract_month[4:6])
    entry_date = _entry_date(candle)
    return entry_date.year, entry_date.month


def _last_trading_day_for_contract(candle: MarketCandle) -> date:
    year, month = _contract_month_from_candle(candle)
    return _business_day_before(_second_friday(year, month))


def _is_last_trading_window(candle: MarketCandle, days: int = 1) -> bool:
    entry_date = _entry_date(candle)
    last_trading_day = _last_trading_day_for_contract(candle)
    return abs((entry_date - last_trading_day).days) <= days


def _is_roll_week(candle: MarketCandle) -> bool:
    last_trading_day = _last_trading_day_for_contract(candle)
    week_start = last_trading_day - timedelta(days=last_trading_day.weekday())
    week_end = week_start + timedelta(days=4)
    return week_start <= _entry_date(candle) <= week_end


def _previous_session_change(candles: list[MarketCandle], index: int) -> float | None:
    if index <= 0:
        return None

    current_session = candles[index].session
    previous_index = index - 1
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


def _previous_session_range(candles: list[MarketCandle], index: int) -> float | None:
    if index <= 0:
        return None

    current_session = candles[index].session
    previous_index = index - 1
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

    session_high = max(candles[item_index].high for item_index in range(session_start, session_end + 1))
    session_low = min(candles[item_index].low for item_index in range(session_start, session_end + 1))
    return session_high - session_low


def _supports_prior_session_filter(candidate: RuleCandidate, candles: list[MarketCandle], index: int) -> bool:
    if candidate.prior_session_filter == "all":
        return True

    previous_change = _previous_session_change(candles, index)
    if previous_change is None:
        return False

    required_move = candidate.prior_session_min_move_ticks * candidate.tick_size
    if candidate.prior_session_filter == "up":
        return previous_change >= required_move
    if candidate.prior_session_filter == "down":
        return previous_change <= -required_move
    raise ValueError(f"unsupported prior_session_filter: {candidate.prior_session_filter}")


def _supports_prior_session_range_filter(candidate: RuleCandidate, candles: list[MarketCandle], index: int) -> bool:
    if candidate.prior_session_range_filter == "all":
        return True

    previous_range = _previous_session_range(candles, index)
    if previous_range is None:
        return False

    required_range = candidate.prior_session_min_range_ticks * candidate.tick_size
    if candidate.prior_session_range_filter == "above":
        return previous_range >= required_range
    if candidate.prior_session_range_filter == "below":
        return previous_range <= required_range
    raise ValueError(f"unsupported prior_session_range_filter: {candidate.prior_session_range_filter}")


def _supports_named_external_factor_filter(
    trading_day: str,
    session: str | None,
    factor_name: str | None,
    factor_filter: str,
    min_value: float,
    external_factors: ExternalFactors | None,
) -> bool:
    if factor_filter == "all" or not factor_name:
        return True
    if external_factors is None:
        return False

    value = external_factors.get_value(trading_day, factor_name, session=session)
    if value is None:
        return False

    if factor_filter == "positive":
        return value >= min_value
    if factor_filter == "negative":
        return value <= -min_value
    if factor_filter == "above":
        return value > min_value
    if factor_filter == "below":
        return value < min_value
    raise ValueError(f"unsupported external_factor_filter: {factor_filter}")


def _supports_external_factor_filter(
    candidate: RuleCandidate,
    candle: MarketCandle,
    external_factors: ExternalFactors | None,
) -> bool:
    trading_day = candle.trading_day or candle.timestamp.strftime("%Y-%m-%d")
    session = candle.session.value if candle.session else None
    primary_ok = _supports_named_external_factor_filter(
        trading_day,
        session,
        candidate.external_factor_name,
        candidate.external_factor_filter,
        candidate.external_factor_min_value,
        external_factors,
    )
    if not primary_ok:
        return False
    return _supports_named_external_factor_filter(
        trading_day,
        session,
        candidate.secondary_external_factor_name,
        candidate.secondary_external_factor_filter,
        candidate.secondary_external_factor_min_value,
        external_factors,
    )


def _supports_entry(
    candidate: RuleCandidate,
    candles: list[MarketCandle],
    index: int,
    side: SignalAction,
    external_factors: ExternalFactors | None = None,
) -> bool:
    candle = candles[index]
    if candidate.session_filter != "both":
        if not candle.session or candle.session.value != candidate.session_filter:
            return False
    if candidate.direction_filter == "long_only" and side != SignalAction.LONG:
        return False
    if candidate.direction_filter == "short_only" and side != SignalAction.SHORT:
        return False
    if _entry_date(candle).weekday() not in candidate.allowed_weekdays:
        return False
    if not _supports_month_filter(candidate, candle):
        return False
    if not _supports_calendar_filter(candidate, candle):
        return False
    if not _supports_prior_session_filter(candidate, candles, index):
        return False
    if not _supports_prior_session_range_filter(candidate, candles, index):
        return False
    if not _supports_external_factor_filter(candidate, candle, external_factors):
        return False
    if not _in_entry_window(candidate, candle):
        return False
    if candidate.skip_first_minutes > 0:
        minutes_from_open = _session_minutes_from_open(candle)
        if minutes_from_open is not None and minutes_from_open < candidate.skip_first_minutes:
            return False
    return True


def _position_size(config: AppConfig, equity: float, entry_price: float, stop_price: float) -> int:
    point_value = config.risk.contract_point_value
    risk_per_unit = abs(entry_price - stop_price) * point_value
    if risk_per_unit <= 0:
        return 0
    risk_budget = equity * config.risk.risk_per_trade_pct
    risk_contracts = int(risk_budget // risk_per_unit)
    max_contracts = config.risk.max_simultaneous_positions
    if config.risk.max_position_notional is not None:
        entry_notional = entry_price * point_value
        notional_contracts = int(config.risk.max_position_notional // entry_notional)
        max_contracts = min(max_contracts, notional_contracts)
    if config.risk.per_contract_margin:
        available = max(0.0, equity - config.risk.min_cash_buffer)
        margin_contracts = int(available // config.risk.per_contract_margin)
        max_contracts = min(max_contracts, margin_contracts)
    return max(0, min(max_contracts, risk_contracts))


def _trade_pnl(config: AppConfig, side: SignalAction, entry_price: float, exit_price: float, quantity: int) -> float:
    point_value = config.risk.contract_point_value
    if side == SignalAction.LONG:
        return (exit_price - entry_price) * quantity * point_value
    return (entry_price - exit_price) * quantity * point_value


def _entry_trend_ok(candidate: RuleCandidate, side: SignalAction, last_close: float, trend_ema: float) -> bool:
    if not candidate.use_trend_filter:
        return True
    if candidate.entry_mode == "breakout":
        return last_close > trend_ema if side == SignalAction.LONG else last_close < trend_ema
    if candidate.entry_mode == "fade":
        return last_close < trend_ema if side == SignalAction.LONG else last_close > trend_ema
    raise ValueError(f"unsupported entry_mode: {candidate.entry_mode}")


def _entry_signal(
    candidate: RuleCandidate,
    side: SignalAction,
    last_close: float,
    trend_ema: float,
    breakout_high: float,
    breakout_low: float,
) -> bool:
    if not _entry_trend_ok(candidate, side, last_close, trend_ema):
        return False

    buffer_points = candidate.entry_buffer_ticks * candidate.tick_size
    if candidate.entry_mode == "breakout":
        if side == SignalAction.LONG:
            return last_close >= breakout_high + buffer_points
        return last_close <= breakout_low - buffer_points
    if candidate.entry_mode == "fade":
        if side == SignalAction.LONG:
            return last_close <= breakout_low - buffer_points
        return last_close >= breakout_high + buffer_points
    raise ValueError(f"unsupported entry_mode: {candidate.entry_mode}")


def _trend_reversal_exit(candidate: RuleCandidate, side: SignalAction, last_close: float, trend_ema: float) -> bool:
    if candidate.entry_mode == "breakout":
        return last_close < trend_ema if side == SignalAction.LONG else last_close > trend_ema
    if candidate.entry_mode == "fade":
        return last_close > trend_ema if side == SignalAction.LONG else last_close < trend_ema
    raise ValueError(f"unsupported entry_mode: {candidate.entry_mode}")


def run_rule_lab(
    candles: list[MarketCandle],
    config: AppConfig,
    candidates: list[RuleCandidate],
    external_factors: ExternalFactors | None = None,
) -> list[RuleLabResult]:
    return [simulate_candidate(candles, config, candidate, external_factors=external_factors) for candidate in candidates]


def generate_default_candidates(config: AppConfig) -> list[RuleCandidate]:
    base = config.strategy
    lookbacks = sorted({max(6, base.breakout_lookback // 2), base.breakout_lookback})
    ema_periods = sorted({max(80, base.ema_period // 2), base.ema_period})
    session_filters = ["day", "night", "both"]
    direction_filters = ["both", "long_only", "short_only"]
    time_windows = [
        ("opening", "09:00", "10:30", 15),
        ("morning", "09:15", "11:15", 15),
        ("full", base.entry_start_time, base.entry_end_time, base.skip_first_minutes),
    ]
    candidates: list[RuleCandidate] = []
    for session_filter in session_filters:
        for direction_filter in direction_filters:
            for lookback in lookbacks:
                for ema_period in ema_periods:
                    for label, start, end, skip in time_windows:
                        name = f"breakout_{session_filter}_{direction_filter}_{label}_lb{lookback}_ema{ema_period}"
                        candidates.append(
                            RuleCandidate(
                                name=name,
                                breakout_lookback=lookback,
                                ema_period=ema_period,
                                atr_period=base.atr_period,
                                atr_stop_multiplier=base.atr_stop_multiplier,
                                trailing_atr_multiplier=base.trailing_atr_multiplier,
                                session_filter=session_filter,
                                direction_filter=direction_filter,
                                allowed_weekdays=tuple(base.allowed_weekdays),
                                entry_start_time=start,
                                entry_end_time=end,
                                skip_first_minutes=skip,
                                use_trend_filter=base.use_trend_filter,
                            )
                        )
    return candidates


def simulate_candidate(
    candles: list[MarketCandle],
    config: AppConfig,
    candidate: RuleCandidate,
    external_factors: ExternalFactors | None = None,
) -> RuleLabResult:
    min_required = max(candidate.ema_period, candidate.breakout_lookback + 1, candidate.atr_period + 1)
    balance = config.paper.initial_balance
    peak_equity = balance
    max_drawdown = 0.0
    min_available_balance = balance
    monthly_pnl: dict[str, float] = {}
    trades = 0
    wins = 0
    losses = 0
    side: SignalAction | None = None
    quantity = 0
    entry_price = 0.0
    stop_price: float | None = None
    trailing_stop: float | None = None
    take_profit_price: float | None = None
    bars_in_trade = 0
    trade_seed: TradeSeed | None = None
    all_months = {_month_key(candle) for candle in candles}
    prices = closing_prices(candles)
    ema_values = ema_series(prices, candidate.ema_period)
    atr_values = atr_series(candles, candidate.atr_period)
    breakout_high_values = highest_high_series(candles, candidate.breakout_lookback)
    breakout_low_values = lowest_low_series(candles, candidate.breakout_lookback)
    trade_records: list[EnrichedTradeRecord] = []

    for index in range(min_required, len(candles)):
        current = candles[index]
        last_close = current.close
        trend_ema = ema_values[index]
        current_atr = atr_values[index]
        breakout_high = breakout_high_values[index - 1]
        breakout_low = breakout_low_values[index - 1]
        if trend_ema is None or current_atr is None or breakout_high is None or breakout_low is None:
            continue

        equity = balance
        if side == SignalAction.LONG:
            equity += _trade_pnl(config, side, entry_price, last_close, quantity)
        elif side == SignalAction.SHORT:
            equity += _trade_pnl(config, side, entry_price, last_close, quantity)
        peak_equity = max(peak_equity, equity)
        max_drawdown = max(max_drawdown, peak_equity - equity)
        margin_requirement = (config.risk.per_contract_margin or 0.0) * quantity
        min_available_balance = min(min_available_balance, equity - margin_requirement)

        if side == SignalAction.LONG:
            bars_in_trade += 1
            trailing_distance = current_atr * candidate.trailing_atr_multiplier
            if candidate.use_trailing_stop:
                trailing_stop = max(trailing_stop or stop_price or 0.0, last_close - trailing_distance)
            exit_now = (
                (candidate.exit_on_trend_reversal and _trend_reversal_exit(candidate, side, last_close, trend_ema))
                or (stop_price is not None and last_close <= stop_price)
                or (candidate.use_trailing_stop and trailing_stop is not None and last_close <= trailing_stop)
                or (take_profit_price is not None and last_close >= take_profit_price)
                or (candidate.time_stop_bars is not None and bars_in_trade >= candidate.time_stop_bars)
            )
            if exit_now:
                pnl = _trade_pnl(config, side, entry_price, last_close, quantity)
                balance += pnl
                trades += 1
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1
                monthly_key = _month_key(current)
                monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
                if trade_seed is not None:
                    trade_records.append(
                        finalize_trade_record(
                            config,
                            trade_seed,
                            exit_candle=current,
                            exit_market_price=last_close,
                        )
                    )
                side = None
                quantity = 0
                entry_price = 0.0
                stop_price = None
                trailing_stop = None
                take_profit_price = None
                bars_in_trade = 0
                trade_seed = None
            continue

        if side == SignalAction.SHORT:
            bars_in_trade += 1
            trailing_distance = current_atr * candidate.trailing_atr_multiplier
            if candidate.use_trailing_stop:
                trailing_stop = min(trailing_stop or stop_price or last_close, last_close + trailing_distance)
            exit_now = (
                (candidate.exit_on_trend_reversal and _trend_reversal_exit(candidate, side, last_close, trend_ema))
                or (stop_price is not None and last_close >= stop_price)
                or (candidate.use_trailing_stop and trailing_stop is not None and last_close >= trailing_stop)
                or (take_profit_price is not None and last_close <= take_profit_price)
                or (candidate.time_stop_bars is not None and bars_in_trade >= candidate.time_stop_bars)
            )
            if exit_now:
                pnl = _trade_pnl(config, side, entry_price, last_close, quantity)
                balance += pnl
                trades += 1
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1
                monthly_key = _month_key(current)
                monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
                if trade_seed is not None:
                    trade_records.append(
                        finalize_trade_record(
                            config,
                            trade_seed,
                            exit_candle=current,
                            exit_market_price=last_close,
                        )
                    )
                side = None
                quantity = 0
                entry_price = 0.0
                stop_price = None
                trailing_stop = None
                take_profit_price = None
                bars_in_trade = 0
                trade_seed = None
            continue

        if _entry_signal(candidate, SignalAction.LONG, last_close, trend_ema, breakout_high, breakout_low) and _supports_entry(
            candidate,
            candles,
            index,
            SignalAction.LONG,
            external_factors,
        ):
            atr_stop = last_close - (current_atr * candidate.atr_stop_multiplier)
            fixed_stop = last_close - (candidate.fixed_stop_ticks * candidate.tick_size) if candidate.fixed_stop_ticks else atr_stop
            proposed_stop = max(atr_stop, fixed_stop)
            contracts = _position_size(config, equity, last_close, proposed_stop)
            if contracts > 0:
                side = SignalAction.LONG
                quantity = contracts
                entry_price = last_close
                stop_price = proposed_stop
                trailing_stop = proposed_stop
                take_profit_price = (
                    last_close + (candidate.take_profit_ticks * candidate.tick_size)
                    if candidate.take_profit_ticks is not None
                    else None
                )
                bars_in_trade = 0
                trade_seed = build_trade_seed(
                    config,
                    rule_id=candidate.name,
                    strategy_name=candidate.name,
                    side=SignalAction.LONG,
                    entry_candle=current,
                    entry_market_price=last_close,
                    qty=contracts,
                    atr_value=current_atr,
                    trend_ema=trend_ema,
                    tick_size=candidate.tick_size,
                )
            continue

        if _entry_signal(candidate, SignalAction.SHORT, last_close, trend_ema, breakout_high, breakout_low) and _supports_entry(
            candidate,
            candles,
            index,
            SignalAction.SHORT,
            external_factors,
        ):
            atr_stop = last_close + (current_atr * candidate.atr_stop_multiplier)
            fixed_stop = last_close + (candidate.fixed_stop_ticks * candidate.tick_size) if candidate.fixed_stop_ticks else atr_stop
            proposed_stop = min(atr_stop, fixed_stop)
            contracts = _position_size(config, equity, last_close, proposed_stop)
            if contracts > 0:
                side = SignalAction.SHORT
                quantity = contracts
                entry_price = last_close
                stop_price = proposed_stop
                trailing_stop = proposed_stop
                take_profit_price = (
                    last_close - (candidate.take_profit_ticks * candidate.tick_size)
                    if candidate.take_profit_ticks is not None
                    else None
                )
                bars_in_trade = 0
                trade_seed = build_trade_seed(
                    config,
                    rule_id=candidate.name,
                    strategy_name=candidate.name,
                    side=SignalAction.SHORT,
                    entry_candle=current,
                    entry_market_price=last_close,
                    qty=contracts,
                    atr_value=current_atr,
                    trend_ema=trend_ema,
                    tick_size=candidate.tick_size,
                )

    if side is not None and quantity > 0:
        last_close = candles[-1].close
        pnl = _trade_pnl(config, side, entry_price, last_close, quantity)
        balance += pnl
        trades += 1
        if pnl > 0:
            wins += 1
        else:
            losses += 1
        monthly_key = _month_key(candles[-1])
        monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
        if trade_seed is not None:
            trade_records.append(
                finalize_trade_record(
                    config,
                    trade_seed,
                    exit_candle=candles[-1],
                    exit_market_price=last_close,
                )
            )

    profitable_months = sum(1 for value in monthly_pnl.values() if value > 0)
    losing_months = sum(1 for value in monthly_pnl.values() if value < 0)
    average_monthly_pnl = (sum(monthly_pnl.values()) / len(all_months)) if all_months else 0.0
    return RuleLabResult(
        name=candidate.name,
        ending_equity=balance,
        profit=balance - config.paper.initial_balance,
        trades=trades,
        wins=wins,
        losses=losses,
        win_rate=(wins / trades) if trades else 0.0,
        max_drawdown=max_drawdown,
        min_available_balance=min_available_balance,
        profitable_months=profitable_months,
        losing_months=losing_months,
        average_monthly_pnl=average_monthly_pnl,
        active_months=len(all_months),
        monthly_pnl=dict(sorted(monthly_pnl.items())),
        trade_records=trade_records,
    )
