from __future__ import annotations

from math import inf

from src.analysis.metrics import calculate_drawdown
from src.backtest.models import BacktestResult, PeriodPerformance, Trade


def _period_key(timestamp, period: str) -> str:
    if period == "month":
        return timestamp.strftime("%Y-%m")
    if period == "quarter":
        quarter = ((timestamp.month - 1) // 3) + 1
        return f"{timestamp.year}-Q{quarter}"
    if period == "year":
        return timestamp.strftime("%Y")
    raise ValueError("Period must be one of: month, quarter, year.")


def _summarize_trade_group(period_key: str, trades: list[Trade]) -> PeriodPerformance:
    profits = [trade.net_pnl for trade in trades if trade.net_pnl > 0]
    losses = [trade.net_pnl for trade in trades if trade.net_pnl < 0]
    trade_count = len(trades)
    gross_profit = sum(profits)
    gross_loss = abs(sum(losses))
    cumulative = 0.0
    equity_values = [0.0]
    for trade in trades:
        cumulative += trade.net_pnl
        equity_values.append(cumulative)

    return PeriodPerformance(
        period_key=period_key,
        trade_count=trade_count,
        total_pnl=sum(trade.net_pnl for trade in trades),
        win_rate=(len(profits) / trade_count) if trade_count else 0.0,
        profit_factor=(gross_profit / gross_loss) if gross_loss > 0 else inf if gross_profit > 0 else 0.0,
        average_trade_pnl=(sum(trade.net_pnl for trade in trades) / trade_count) if trade_count else 0.0,
        max_drawdown=calculate_drawdown(equity_values),
    )


def summarize_periods(result: BacktestResult, period: str = "month") -> list[PeriodPerformance]:
    grouped: dict[str, list[Trade]] = {}
    for trade in result.trades:
        key = _period_key(trade.exit_time, period)
        grouped.setdefault(key, []).append(trade)
    return [_summarize_trade_group(key, grouped[key]) for key in sorted(grouped)]
