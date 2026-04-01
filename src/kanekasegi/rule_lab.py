from __future__ import annotations

from dataclasses import dataclass

from .config import AppConfig
from .indicators import atr, closing_prices, ema, highest_high, lowest_low
from .types import MarketCandle, SessionType, SignalAction


@dataclass(slots=True)
class RuleCandidate:
    name: str
    breakout_lookback: int
    ema_period: int
    atr_period: int
    atr_stop_multiplier: float
    trailing_atr_multiplier: float
    session_filter: str = "both"
    direction_filter: str = "both"


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


def _supports_entry(candidate: RuleCandidate, candle: MarketCandle, side: SignalAction) -> bool:
    if candidate.session_filter != "both":
        if not candle.session or candle.session.value != candidate.session_filter:
            return False
    if candidate.direction_filter == "long_only" and side != SignalAction.LONG:
        return False
    if candidate.direction_filter == "short_only" and side != SignalAction.SHORT:
        return False
    return True


def _position_size(config: AppConfig, equity: float, entry_price: float, stop_price: float) -> int:
    risk_per_unit = abs(entry_price - stop_price)
    if risk_per_unit <= 0:
        return 0
    risk_budget = equity * config.risk.risk_per_trade_pct
    risk_contracts = int(risk_budget // risk_per_unit)
    max_contracts = max(1, config.risk.max_simultaneous_positions)
    if config.risk.per_contract_margin:
        available = max(0.0, equity - config.risk.min_cash_buffer)
        margin_contracts = int(available // config.risk.per_contract_margin)
        max_contracts = min(max_contracts, margin_contracts)
    return max(0, min(max_contracts, risk_contracts if risk_contracts > 0 else 1))


def run_rule_lab(candles: list[MarketCandle], config: AppConfig, candidates: list[RuleCandidate]) -> list[RuleLabResult]:
    return [simulate_candidate(candles, config, candidate) for candidate in candidates]


def generate_default_candidates(config: AppConfig) -> list[RuleCandidate]:
    base = config.strategy
    lookbacks = sorted({max(6, base.breakout_lookback // 2), base.breakout_lookback})
    ema_periods = sorted({max(80, base.ema_period // 2), base.ema_period})
    session_filters = ["both", "day", "night"]
    direction_filters = ["both", "long_only", "short_only"]
    candidates: list[RuleCandidate] = []
    for session_filter in session_filters:
        for direction_filter in direction_filters:
            for lookback in lookbacks:
                for ema_period in ema_periods:
                    name = f"breakout_{session_filter}_{direction_filter}_lb{lookback}_ema{ema_period}"
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
                        )
                    )
    return candidates


def simulate_candidate(candles: list[MarketCandle], config: AppConfig, candidate: RuleCandidate) -> RuleLabResult:
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

    for index in range(min_required, len(candles)):
        window = candles[: index + 1]
        current = window[-1]
        last_close = current.close
        prices = closing_prices(window)
        trend_ema = ema(prices, candidate.ema_period)
        current_atr = atr(window, candidate.atr_period)

        equity = balance
        if side == SignalAction.LONG:
            equity += (last_close - entry_price) * quantity
        elif side == SignalAction.SHORT:
            equity += (entry_price - last_close) * quantity
        peak_equity = max(peak_equity, equity)
        max_drawdown = max(max_drawdown, peak_equity - equity)
        margin_requirement = (config.risk.per_contract_margin or 0.0) * quantity
        min_available_balance = min(min_available_balance, equity - margin_requirement)

        if side == SignalAction.LONG:
            trailing_distance = current_atr * candidate.trailing_atr_multiplier
            trailing_stop = max(trailing_stop or stop_price or 0.0, last_close - trailing_distance)
            exit_now = (
                last_close < trend_ema
                or (stop_price is not None and last_close <= stop_price)
                or (trailing_stop is not None and last_close <= trailing_stop)
            )
            if exit_now:
                pnl = (last_close - entry_price) * quantity
                balance += pnl
                trades += 1
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1
                monthly_key = current.timestamp.strftime("%Y-%m")
                monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
                side = None
                quantity = 0
                entry_price = 0.0
                stop_price = None
                trailing_stop = None
            continue

        if side == SignalAction.SHORT:
            trailing_distance = current_atr * candidate.trailing_atr_multiplier
            trailing_stop = min(trailing_stop or stop_price or last_close, last_close + trailing_distance)
            exit_now = (
                last_close > trend_ema
                or (stop_price is not None and last_close >= stop_price)
                or (trailing_stop is not None and last_close >= trailing_stop)
            )
            if exit_now:
                pnl = (entry_price - last_close) * quantity
                balance += pnl
                trades += 1
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1
                monthly_key = current.timestamp.strftime("%Y-%m")
                monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
                side = None
                quantity = 0
                entry_price = 0.0
                stop_price = None
                trailing_stop = None
            continue

        breakout_high = highest_high(window[:-1], candidate.breakout_lookback)
        breakout_low = lowest_low(window[:-1], candidate.breakout_lookback)

        if last_close > trend_ema and last_close >= breakout_high and _supports_entry(candidate, current, SignalAction.LONG):
            proposed_stop = last_close - (current_atr * candidate.atr_stop_multiplier)
            contracts = _position_size(config, equity, last_close, proposed_stop)
            if contracts > 0:
                side = SignalAction.LONG
                quantity = contracts
                entry_price = last_close
                stop_price = proposed_stop
                trailing_stop = proposed_stop
            continue

        if last_close < trend_ema and last_close <= breakout_low and _supports_entry(candidate, current, SignalAction.SHORT):
            proposed_stop = last_close + (current_atr * candidate.atr_stop_multiplier)
            contracts = _position_size(config, equity, last_close, proposed_stop)
            if contracts > 0:
                side = SignalAction.SHORT
                quantity = contracts
                entry_price = last_close
                stop_price = proposed_stop
                trailing_stop = proposed_stop

    if side is not None and quantity > 0:
        last_close = candles[-1].close
        pnl = (last_close - entry_price) * quantity if side == SignalAction.LONG else (entry_price - last_close) * quantity
        balance += pnl
        trades += 1
        if pnl > 0:
            wins += 1
        else:
            losses += 1
        monthly_key = candles[-1].timestamp.strftime("%Y-%m")
        monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl

    profitable_months = sum(1 for value in monthly_pnl.values() if value > 0)
    losing_months = sum(1 for value in monthly_pnl.values() if value < 0)
    average_monthly_pnl = (sum(monthly_pnl.values()) / len(monthly_pnl)) if monthly_pnl else 0.0
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
    )
