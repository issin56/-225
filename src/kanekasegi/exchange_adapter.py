from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from .types import OrderRequest, OrderResult, OrderSide, PositionState


class ExchangeAdapter(ABC):
    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        raise NotImplementedError

    @abstractmethod
    def get_ticker(self, symbol: str) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_position(self, symbol: str) -> PositionState:
        raise NotImplementedError

    @abstractmethod
    def get_balance(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def place_order(self, order_request: OrderRequest) -> OrderResult:
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_open_orders(self, symbol: str):
        raise NotImplementedError


class PaperExchangeAdapter(ExchangeAdapter):
    def __init__(self, market_data_provider, initial_balance: float, fee_rate: float = 0.0004, slippage_bps: float = 3.0) -> None:
        self.market_data_provider = market_data_provider
        self.balance = initial_balance
        self.fee_rate = fee_rate
        self.slippage_bps = slippage_bps
        self.position = PositionState(symbol="")
        self.orders: list[OrderResult] = []

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        return self.market_data_provider.get_ohlcv(symbol, timeframe, limit)

    def get_ticker(self, symbol: str) -> float:
        return self.market_data_provider.get_ticker(symbol)

    def get_position(self, symbol: str) -> PositionState:
        return self.position if self.position.symbol == symbol else PositionState(symbol=symbol)

    def get_balance(self) -> float:
        return self.balance

    def place_order(self, order_request: OrderRequest) -> OrderResult:
        market_price = self.get_ticker(order_request.symbol)
        slippage = market_price * (self.slippage_bps / 10_000)
        fill_price = market_price + slippage if order_request.side == OrderSide.BUY else market_price - slippage
        notional = fill_price * order_request.quantity
        fee = notional * self.fee_rate
        realized_pnl = 0.0
        if order_request.reduce_only and self.position.is_open:
            if self.position.side.value == "long":
                realized_pnl = (fill_price - self.position.entry_price) * order_request.quantity
            else:
                realized_pnl = (self.position.entry_price - fill_price) * order_request.quantity
            self.balance += realized_pnl
        self.balance -= fee
        order = OrderResult(
            order_id=str(uuid4()),
            symbol=order_request.symbol,
            side=order_request.side,
            quantity=order_request.quantity,
            filled_price=fill_price,
            status="filled",
            timestamp=datetime.utcnow(),
            realized_pnl=realized_pnl,
            fee_paid=fee,
        )
        self.orders.append(order)
        return order

    def cancel_order(self, order_id: str) -> None:
        return None

    def list_open_orders(self, symbol: str):
        return []


class LiveExchangeAdapter(ExchangeAdapter):
    def __init__(self) -> None:
        self._message = "Live exchange adapter is intentionally unimplemented until a compliant broker is selected."

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        raise NotImplementedError(self._message)

    def get_ticker(self, symbol: str) -> float:
        raise NotImplementedError(self._message)

    def get_position(self, symbol: str) -> PositionState:
        raise NotImplementedError(self._message)

    def get_balance(self) -> float:
        raise NotImplementedError(self._message)

    def place_order(self, order_request: OrderRequest) -> OrderResult:
        raise NotImplementedError(self._message)

    def cancel_order(self, order_id: str) -> None:
        raise NotImplementedError(self._message)

    def list_open_orders(self, symbol: str):
        raise NotImplementedError(self._message)
