from __future__ import annotations

from dataclasses import dataclass, field

from .config import AppConfig
from .external_factors import ExternalFactors
from .indicators import atr_series, closing_prices, ema_series, highest_high_series, lowest_low_series
from .rule_lab import (
    RuleCandidate,
    _entry_signal,
    _month_key,
    _position_size,
    _supports_entry,
    _trade_pnl,
    _trend_reversal_exit,
)
from .types import MarketCandle, SignalAction


@dataclass(slots=True)
class StrategyStats:
    name: str
    trades: int = 0
    wins: int = 0
    losses: int = 0
    profit: float = 0.0
    monthly_pnl: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class PortfolioLabResult:
    candidate_names: list[str]
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
    monthly_pnl: dict[str, float]
    strategy_stats: dict[str, StrategyStats] = field(default_factory=dict)


@dataclass(slots=True)
class _OpenPosition:
    candidate: RuleCandidate
    side: SignalAction
    quantity: int
    entry_price: float
    stop_price: float
    trailing_stop: float | None
    take_profit_price: float | None
    bars_in_trade: int = 0
    last_price: float = 0.0


@dataclass(slots=True)
class _CandidateSeries:
    prices: list[float]
    ema_values: list[float | None]
    atr_values: list[float | None]
    breakout_high_values: list[float | None]
    breakout_low_values: list[float | None]


def _candidate_entry(
    candles: list[MarketCandle],
    series: _CandidateSeries,
    index: int,
    config: AppConfig,
    candidate: RuleCandidate,
    equity: float,
    external_factors: ExternalFactors | None = None,
) -> _OpenPosition | None:
    min_required = max(candidate.ema_period, candidate.breakout_lookback + 1, candidate.atr_period + 1)
    if index < min_required:
        return None

    current = candles[index]
    last_close = current.close
    trend_ema = series.ema_values[index]
    current_atr = series.atr_values[index]
    breakout_high = series.breakout_high_values[index - 1]
    breakout_low = series.breakout_low_values[index - 1]
    if trend_ema is None or current_atr is None or breakout_high is None or breakout_low is None:
        return None

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
            take_profit_price = (
                last_close + (candidate.take_profit_ticks * candidate.tick_size)
                if candidate.take_profit_ticks is not None
                else None
            )
            return _OpenPosition(
                candidate=candidate,
                side=SignalAction.LONG,
                quantity=contracts,
                entry_price=last_close,
                stop_price=proposed_stop,
                trailing_stop=proposed_stop,
                take_profit_price=take_profit_price,
                last_price=last_close,
            )

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
            take_profit_price = (
                last_close - (candidate.take_profit_ticks * candidate.tick_size)
                if candidate.take_profit_ticks is not None
                else None
            )
            return _OpenPosition(
                candidate=candidate,
                side=SignalAction.SHORT,
                quantity=contracts,
                entry_price=last_close,
                stop_price=proposed_stop,
                trailing_stop=proposed_stop,
                take_profit_price=take_profit_price,
                last_price=last_close,
            )

    return None


def _should_exit(
    candles: list[MarketCandle],
    series: _CandidateSeries,
    index: int,
    config: AppConfig,
    position: _OpenPosition,
) -> tuple[bool, float]:
    candidate = position.candidate
    last_close = candles[index].close
    trend_ema = series.ema_values[index]
    current_atr = series.atr_values[index]
    if trend_ema is None or current_atr is None:
        return False, last_close
    position.last_price = last_close
    position.bars_in_trade += 1

    if position.side == SignalAction.LONG:
        trailing_distance = current_atr * candidate.trailing_atr_multiplier
        if candidate.use_trailing_stop:
            position.trailing_stop = max(position.trailing_stop or position.stop_price, last_close - trailing_distance)
        exit_now = (
            (candidate.exit_on_trend_reversal and _trend_reversal_exit(candidate, position.side, last_close, trend_ema))
            or last_close <= position.stop_price
            or (candidate.use_trailing_stop and position.trailing_stop is not None and last_close <= position.trailing_stop)
            or (position.take_profit_price is not None and last_close >= position.take_profit_price)
            or (candidate.time_stop_bars is not None and position.bars_in_trade >= candidate.time_stop_bars)
        )
        return exit_now, last_close

    trailing_distance = current_atr * candidate.trailing_atr_multiplier
    if candidate.use_trailing_stop:
        position.trailing_stop = min(position.trailing_stop or position.stop_price, last_close + trailing_distance)
    exit_now = (
        (candidate.exit_on_trend_reversal and _trend_reversal_exit(candidate, position.side, last_close, trend_ema))
        or last_close >= position.stop_price
        or (candidate.use_trailing_stop and position.trailing_stop is not None and last_close >= position.trailing_stop)
        or (position.take_profit_price is not None and last_close <= position.take_profit_price)
        or (candidate.time_stop_bars is not None and position.bars_in_trade >= candidate.time_stop_bars)
    )
    return exit_now, last_close


def simulate_portfolio(
    candles_by_timeframe: dict[str, list[MarketCandle]],
    config: AppConfig,
    candidates: list[RuleCandidate],
    external_factors: ExternalFactors | None = None,
) -> PortfolioLabResult:
    timestamps = sorted(
        {
            candle.timestamp
            for candles in candles_by_timeframe.values()
            for candle in candles
        }
    )
    timestamp_index_by_timeframe = {
        timeframe: {candle.timestamp: index for index, candle in enumerate(candles)}
        for timeframe, candles in candles_by_timeframe.items()
    }
    candidate_series = {
        candidate.name: _CandidateSeries(
            prices=closing_prices(candles_by_timeframe[candidate.timeframe]),
            ema_values=ema_series(closing_prices(candles_by_timeframe[candidate.timeframe]), candidate.ema_period),
            atr_values=atr_series(candles_by_timeframe[candidate.timeframe], candidate.atr_period),
            breakout_high_values=highest_high_series(candles_by_timeframe[candidate.timeframe], candidate.breakout_lookback),
            breakout_low_values=lowest_low_series(candles_by_timeframe[candidate.timeframe], candidate.breakout_lookback),
        )
        for candidate in candidates
    }

    balance = config.paper.initial_balance
    peak_equity = balance
    max_drawdown = 0.0
    min_available_balance = balance
    monthly_pnl: dict[str, float] = {}
    strategy_stats = {candidate.name: StrategyStats(name=candidate.name) for candidate in candidates}
    active_months = {
        _month_key(candle)
        for candles in candles_by_timeframe.values()
        for candle in candles
    }
    open_position: _OpenPosition | None = None
    trades = 0
    wins = 0
    losses = 0

    for timestamp in timestamps:
        if open_position is not None:
            owner_timeframe = open_position.candidate.timeframe
            owner_index = timestamp_index_by_timeframe[owner_timeframe].get(timestamp)
            if owner_index is not None:
                owner_candles = candles_by_timeframe[owner_timeframe]
                owner_series = candidate_series[open_position.candidate.name]
                exit_now, exit_price = _should_exit(owner_candles, owner_series, owner_index, config, open_position)
                equity = balance + _trade_pnl(
                    config,
                    open_position.side,
                    open_position.entry_price,
                    exit_price,
                    open_position.quantity,
                )
                peak_equity = max(peak_equity, equity)
                max_drawdown = max(max_drawdown, peak_equity - equity)
                margin_requirement = (config.risk.per_contract_margin or 0.0) * open_position.quantity
                min_available_balance = min(min_available_balance, equity - margin_requirement)
                if exit_now:
                    pnl = _trade_pnl(
                        config,
                        open_position.side,
                        open_position.entry_price,
                        exit_price,
                        open_position.quantity,
                    )
                    balance += pnl
                    trades += 1
                    stats = strategy_stats[open_position.candidate.name]
                    stats.trades += 1
                    stats.profit += pnl
                    if pnl > 0:
                        wins += 1
                        stats.wins += 1
                    else:
                        losses += 1
                        stats.losses += 1
                    monthly_key = _month_key(owner_candles[owner_index])
                    monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
                    stats.monthly_pnl[monthly_key] = stats.monthly_pnl.get(monthly_key, 0.0) + pnl
                    open_position = None
                continue

            equity = balance + _trade_pnl(
                config,
                open_position.side,
                open_position.entry_price,
                open_position.last_price,
                open_position.quantity,
            )
            peak_equity = max(peak_equity, equity)
            max_drawdown = max(max_drawdown, peak_equity - equity)
            margin_requirement = (config.risk.per_contract_margin or 0.0) * open_position.quantity
            min_available_balance = min(min_available_balance, equity - margin_requirement)
            continue

        equity = balance
        peak_equity = max(peak_equity, equity)
        max_drawdown = max(max_drawdown, peak_equity - equity)
        min_available_balance = min(min_available_balance, equity)
        for candidate in candidates:
            candidate_index = timestamp_index_by_timeframe[candidate.timeframe].get(timestamp)
            if candidate_index is None:
                continue
            candidate_candles = candles_by_timeframe[candidate.timeframe]
            proposed_position = _candidate_entry(
                candidate_candles,
                candidate_series[candidate.name],
                candidate_index,
                config,
                candidate,
                equity,
                external_factors,
            )
            if proposed_position is not None:
                open_position = proposed_position
                break

    if open_position is not None:
        pnl = _trade_pnl(
            config,
            open_position.side,
            open_position.entry_price,
            open_position.last_price,
            open_position.quantity,
        )
        balance += pnl
        trades += 1
        stats = strategy_stats[open_position.candidate.name]
        stats.trades += 1
        stats.profit += pnl
        if pnl > 0:
            wins += 1
            stats.wins += 1
        else:
            losses += 1
            stats.losses += 1
        owner_candles = candles_by_timeframe[open_position.candidate.timeframe]
        monthly_key = _month_key(owner_candles[-1])
        monthly_pnl[monthly_key] = monthly_pnl.get(monthly_key, 0.0) + pnl
        stats.monthly_pnl[monthly_key] = stats.monthly_pnl.get(monthly_key, 0.0) + pnl

    profitable_months = sum(1 for value in monthly_pnl.values() if value > 0)
    losing_months = sum(1 for value in monthly_pnl.values() if value < 0)
    average_monthly_pnl = (sum(monthly_pnl.values()) / len(active_months)) if active_months else 0.0
    return PortfolioLabResult(
        candidate_names=[candidate.name for candidate in candidates],
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
        active_months=len(active_months),
        monthly_pnl=dict(sorted(monthly_pnl.items())),
        strategy_stats=strategy_stats,
    )
