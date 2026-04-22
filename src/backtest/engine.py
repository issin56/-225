from __future__ import annotations

from math import floor

from src.backtest.metrics import calculate_drawdown
from src.backtest.models import (
    BacktestConfig,
    BacktestResult,
    Candle,
    EquityPoint,
    PendingAction,
    Position,
    Side,
    Trade,
)
from src.strategy.registry import get_strategy


def calculate_trade_pnl(
    side: Side,
    entry_price: float,
    exit_price: float,
    units: int,
    commission: float,
) -> tuple[float, float]:
    if side == "long":
        gross_pnl = (exit_price - entry_price) * units
    else:
        gross_pnl = (entry_price - exit_price) * units
    net_pnl = gross_pnl - (commission * 2.0)
    return gross_pnl, net_pnl


def calculate_position_size(config: BacktestConfig, equity: float) -> int:
    risk_amount = equity * config.risk.risk_per_trade
    available_risk = max(risk_amount - (config.risk.commission * 2.0), 0.0)
    risk_per_unit = config.risk.stop_loss + config.risk.spread
    if available_risk <= 0.0 or risk_per_unit <= 0.0:
        return 0
    return max(floor(available_risk / risk_per_unit), 0)


def _entry_fill_price(side: Side, market_open: float, spread: float) -> float:
    half_spread = spread / 2.0
    return market_open + half_spread if side == "long" else market_open - half_spread


def _exit_fill_price(side: Side, raw_price: float, spread: float) -> float:
    half_spread = spread / 2.0
    return raw_price - half_spread if side == "long" else raw_price + half_spread


def _open_position(candle: Candle, side: Side, config: BacktestConfig, equity: float) -> Position | None:
    units = calculate_position_size(config, equity)
    if units <= 0:
        return None

    entry_price = _entry_fill_price(side, candle.open, config.risk.spread)
    if side == "long":
        stop_price = entry_price - config.risk.stop_loss
        take_profit_price = entry_price + config.risk.take_profit
    else:
        stop_price = entry_price + config.risk.stop_loss
        take_profit_price = entry_price - config.risk.take_profit

    return Position(
        side=side,
        entry_time=candle.timestamp,
        entry_price=entry_price,
        units=units,
        stop_price=stop_price,
        take_profit_price=take_profit_price,
    )


def _close_position(
    position: Position,
    candle: Candle,
    exit_price: float,
    config: BacktestConfig,
    exit_reason: str,
) -> Trade:
    gross_pnl, net_pnl = calculate_trade_pnl(
        side=position.side,
        entry_price=position.entry_price,
        exit_price=exit_price,
        units=position.units,
        commission=config.risk.commission,
    )
    return Trade(
        side=position.side,
        entry_time=position.entry_time,
        exit_time=candle.timestamp,
        entry_price=position.entry_price,
        exit_price=exit_price,
        units=position.units,
        gross_pnl=gross_pnl,
        net_pnl=net_pnl,
        commission_paid=config.risk.commission * 2.0,
        exit_reason=exit_reason,
    )


def _intrabar_exit(position: Position, candle: Candle, config: BacktestConfig) -> tuple[float, str] | None:
    if position.side == "long":
        hit_stop = candle.low <= position.stop_price
        hit_target = candle.high >= position.take_profit_price
        if hit_stop and hit_target:
            return _exit_fill_price(position.side, position.stop_price, config.risk.spread), "stop_loss"
        if hit_stop:
            return _exit_fill_price(position.side, position.stop_price, config.risk.spread), "stop_loss"
        if hit_target:
            return _exit_fill_price(position.side, position.take_profit_price, config.risk.spread), "take_profit"
    else:
        hit_stop = candle.high >= position.stop_price
        hit_target = candle.low <= position.take_profit_price
        if hit_stop and hit_target:
            return _exit_fill_price(position.side, position.stop_price, config.risk.spread), "stop_loss"
        if hit_stop:
            return _exit_fill_price(position.side, position.stop_price, config.risk.spread), "stop_loss"
        if hit_target:
            return _exit_fill_price(position.side, position.take_profit_price, config.risk.spread), "take_profit"
    return None


def run_backtest(candles: list[Candle], config: BacktestConfig) -> BacktestResult:
    strategy_definition = get_strategy(config.strategy.name)
    if len(candles) < strategy_definition.minimum_candles(config):
        raise ValueError(f"Not enough candles to run the '{config.strategy.name}' backtest.")

    strategy_runtime = strategy_definition.prepare(candles, config)

    trades: list[Trade] = []
    equity = config.risk.initial_capital
    equity_curve = [EquityPoint(timestamp=candles[0].timestamp, equity=equity, drawdown=0.0)]

    position: Position | None = None
    pending_action: PendingAction | None = None
    stopped_early = False
    stop_reason: str | None = None
    consecutive_losses = 0

    def register_trade(trade: Trade) -> None:
        nonlocal equity
        nonlocal consecutive_losses
        nonlocal stopped_early
        nonlocal stop_reason

        trades.append(trade)
        equity += trade.net_pnl
        drawdown = calculate_drawdown([point.equity for point in equity_curve] + [equity])
        equity_curve.append(EquityPoint(timestamp=trade.exit_time, equity=equity, drawdown=drawdown))

        if trade.net_pnl < 0:
            consecutive_losses += 1
        else:
            consecutive_losses = 0

        if config.risk.max_consecutive_losses is not None and consecutive_losses >= config.risk.max_consecutive_losses:
            stopped_early = True
            stop_reason = "max_consecutive_losses"
            return

        if config.risk.max_drawdown is not None and drawdown >= config.risk.max_drawdown:
            stopped_early = True
            stop_reason = "max_drawdown"

    for index in range(1, len(candles)):
        candle = candles[index]

        if pending_action is not None:
            if pending_action.close_position and position is not None:
                exit_price = _exit_fill_price(position.side, candle.open, config.risk.spread)
                register_trade(_close_position(position, candle, exit_price, config, pending_action.exit_reason))
                position = None
                if stopped_early:
                    break

            if pending_action.open_side is not None and position is None and not stopped_early:
                position = _open_position(candle, pending_action.open_side, config, equity)

            pending_action = None

        if position is not None:
            intrabar_exit = _intrabar_exit(position, candle, config)
            if intrabar_exit is not None:
                exit_price, exit_reason = intrabar_exit
                register_trade(_close_position(position, candle, exit_price, config, exit_reason))
                position = None
                if stopped_early:
                    break

        if stopped_early or index >= len(candles) - 1:
            continue

        signal = strategy_runtime.action_at(index)
        if signal is None:
            continue

        desired_side: Side = "long" if signal == "buy" else "short"
        if position is None:
            pending_action = PendingAction(close_position=False, open_side=desired_side, exit_reason="signal_entry")
            continue

        if position.side == desired_side:
            continue

        pending_action = PendingAction(
            close_position=True,
            open_side=desired_side if config.strategy.allow_reversal else None,
            exit_reason="reversal" if config.strategy.allow_reversal else "signal_close",
        )

    if position is not None and not stopped_early:
        final_candle = candles[-1]
        final_exit_price = _exit_fill_price(position.side, final_candle.close, config.risk.spread)
        register_trade(_close_position(position, final_candle, final_exit_price, config, "end_of_data"))

    return BacktestResult(
        initial_capital=config.risk.initial_capital,
        final_capital=equity,
        trades=trades,
        equity_curve=equity_curve,
        stopped_early=stopped_early,
        stop_reason=stop_reason,
    )
