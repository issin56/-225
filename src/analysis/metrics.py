from __future__ import annotations

from math import inf

from src.backtest.models import BacktestResult, BacktestSummary, Trade


def calculate_drawdown(equity_values: list[float]) -> float:
    if not equity_values:
        return 0.0

    peak = equity_values[0]
    max_drawdown = 0.0
    for equity in equity_values:
        peak = max(peak, equity)
        if peak <= 0:
            continue
        max_drawdown = max(max_drawdown, (peak - equity) / peak)
    return max_drawdown


def calculate_streaks(trades: list[Trade]) -> tuple[int, int]:
    current_wins = 0
    current_losses = 0
    max_wins = 0
    max_losses = 0

    for trade in trades:
        if trade.net_pnl > 0:
            current_wins += 1
            current_losses = 0
            max_wins = max(max_wins, current_wins)
        elif trade.net_pnl < 0:
            current_losses += 1
            current_wins = 0
            max_losses = max(max_losses, current_losses)
        else:
            current_wins = 0
            current_losses = 0

    return max_wins, max_losses


def summarize_backtest(result: BacktestResult) -> BacktestSummary:
    profits = [trade.net_pnl for trade in result.trades if trade.net_pnl > 0]
    losses = [trade.net_pnl for trade in result.trades if trade.net_pnl < 0]
    gross_profit = sum(profits)
    gross_loss = abs(sum(losses))
    trade_count = len(result.trades)
    win_rate = len(profits) / trade_count if trade_count else 0.0
    average_profit = gross_profit / len(profits) if profits else 0.0
    average_loss = abs(sum(losses) / len(losses)) if losses else 0.0
    payoff_ratio = average_profit / average_loss if average_loss > 0 else inf if average_profit > 0 else 0.0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else inf if gross_profit > 0 else 0.0
    max_winning_streak, max_losing_streak = calculate_streaks(result.trades)
    max_drawdown = max((point.drawdown for point in result.equity_curve), default=0.0)

    return BacktestSummary(
        initial_capital=result.initial_capital,
        final_capital=result.final_capital,
        total_pnl=result.final_capital - result.initial_capital,
        win_rate=win_rate,
        payoff_ratio=payoff_ratio,
        profit_factor=profit_factor,
        max_drawdown=max_drawdown,
        trade_count=trade_count,
        average_profit=average_profit,
        average_loss=average_loss,
        max_winning_streak=max_winning_streak,
        max_losing_streak=max_losing_streak,
        stopped_early=result.stopped_early,
        stop_reason=result.stop_reason,
    )

