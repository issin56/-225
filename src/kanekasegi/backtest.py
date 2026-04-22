from __future__ import annotations

from dataclasses import dataclass

from .bot import TradingBot
from .types import SignalAction


@dataclass(slots=True)
class BacktestSummary:
    cycles: int
    starting_equity: float
    ending_equity: float
    daily_pnl: float
    profit: float
    trades: int
    wins: int
    losses: int
    win_rate: float
    max_drawdown: float
    min_equity: float
    min_available_balance: float


def _mark_to_market_equity(bot: TradingBot, ticker: float) -> tuple[float, float]:
    balance = bot.exchange.get_balance()
    position = bot.storage.load_position(bot.config.runtime.symbol)
    unrealized = 0.0
    point_value = bot.config.risk.contract_point_value
    if position.is_open:
        if position.side == SignalAction.LONG:
            unrealized = (ticker - position.entry_price) * position.quantity * point_value
        elif position.side == SignalAction.SHORT:
            unrealized = (position.entry_price - ticker) * position.quantity * point_value
    equity = balance + unrealized
    margin_requirement = (bot.config.risk.per_contract_margin or 0.0) * position.quantity
    available_balance = equity - margin_requirement
    return equity, available_balance


def run_backtest(bot: TradingBot, market_data, warmup: int) -> BacktestSummary:
    total_candles = market_data.total_candles()
    safe_warmup = min(warmup, max(1, total_candles - 1))
    market_data.reset_for_backtest(safe_warmup)
    cycles = 0
    trades = 0
    wins = 0
    losses = 0
    starting_equity = bot.exchange.get_balance()
    peak_equity = starting_equity
    min_equity = starting_equity
    min_available_balance = starting_equity
    max_drawdown = 0.0
    while market_data.has_next() and not bot.status.halted:
        before_pnl = bot.storage.load_total_realized_pnl()
        bot.run_cycle()
        after_pnl = bot.storage.load_total_realized_pnl()
        if after_pnl != before_pnl:
            trades += 1
            if after_pnl > before_pnl:
                wins += 1
            else:
                losses += 1
        ticker = market_data.get_ticker(bot.config.runtime.symbol)
        equity, available_balance = _mark_to_market_equity(bot, ticker)
        peak_equity = max(peak_equity, equity)
        min_equity = min(min_equity, equity)
        min_available_balance = min(min_available_balance, available_balance)
        max_drawdown = max(max_drawdown, peak_equity - equity)
        market_data.advance()
        cycles += 1
    ending_equity, _ = _mark_to_market_equity(bot, market_data.get_ticker(bot.config.runtime.symbol))
    total_trades = wins + losses
    return BacktestSummary(
        cycles=cycles,
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        daily_pnl=bot.storage.load_total_realized_pnl(),
        profit=ending_equity - starting_equity,
        trades=trades,
        wins=wins,
        losses=losses,
        win_rate=(wins / total_trades) if total_trades else 0.0,
        max_drawdown=max_drawdown,
        min_equity=min_equity,
        min_available_balance=min_available_balance,
    )
