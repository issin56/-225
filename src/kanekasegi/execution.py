from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from .exchange_adapter import ExchangeAdapter, PaperExchangeAdapter
from .storage import Storage
from .types import OrderRequest, OrderSide, PositionState, Signal, SignalAction


@dataclass(slots=True)
class ExecutionOutcome:
    position: PositionState
    realized_pnl: float = 0.0
    fee_paid: float = 0.0
    order_executed: bool = False


class ExecutionEngine:
    def __init__(self, exchange: ExchangeAdapter, storage: Storage) -> None:
        self.exchange = exchange
        self.storage = storage

    def execute_signal(
        self,
        symbol: str,
        signal: Signal,
        quantity: float,
        position: PositionState,
        trading_day: date | str | None = None,
    ) -> ExecutionOutcome:
        if signal.action == SignalAction.HOLD:
            if "trailing_stop" in signal.metadata and position.is_open:
                position.trailing_stop = float(signal.metadata["trailing_stop"])
                self.storage.save_position(position)
            return ExecutionOutcome(position=position)

        if signal.action == SignalAction.EXIT and position.is_open:
            order = self.exchange.place_order(
                OrderRequest(
                    symbol=symbol,
                    side=OrderSide.SELL if position.side == SignalAction.LONG else OrderSide.BUY,
                    quantity=position.quantity,
                    reduce_only=True,
                )
            )
            self.storage.save_order(order)
            current_daily_pnl = self.storage.load_daily_pnl(trading_day)
            self.storage.save_daily_pnl(current_daily_pnl + order.realized_pnl - order.fee_paid, trading_day)
            flat = PositionState(symbol=symbol)
            if isinstance(self.exchange, PaperExchangeAdapter):
                self.exchange.position = flat
            self.storage.save_position(flat)
            return ExecutionOutcome(
                position=flat,
                realized_pnl=order.realized_pnl,
                fee_paid=order.fee_paid,
                order_executed=True,
            )

        order_side = OrderSide.BUY if signal.action == SignalAction.LONG else OrderSide.SELL
        order = self.exchange.place_order(OrderRequest(symbol=symbol, side=order_side, quantity=quantity))
        self.storage.save_order(order)
        new_position = PositionState(
            symbol=symbol,
            side=signal.action,
            quantity=quantity,
            entry_price=order.filled_price,
            stop_price=signal.stop_price,
            trailing_stop=signal.stop_price,
            opened_at=datetime.utcnow(),
        )
        if isinstance(self.exchange, PaperExchangeAdapter):
            self.exchange.position = new_position
        self.storage.save_position(new_position)
        return ExecutionOutcome(position=new_position, fee_paid=order.fee_paid, order_executed=True)
