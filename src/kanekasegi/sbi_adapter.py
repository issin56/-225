from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .exchange_adapter import ExchangeAdapter
from .types import OrderRequest, OrderResult, PositionState


@dataclass(slots=True)
class SbiApiProfile:
    api_key: str | None
    api_secret: str | None
    endpoint: str | None
    tool_name: str | None


class SbiFuturesAdapter(ExchangeAdapter):
    def __init__(self, profile: SbiApiProfile, market_data_provider=None, initial_balance: float = 300000.0) -> None:
        self.profile = profile
        self.market_data_provider = market_data_provider
        self.initial_balance = initial_balance
        self.position = PositionState(symbol="")
        self._message = (
            "SBI futures adapter is configured, but concrete request wiring is not implemented. "
            "Official product support for Nikkei 225 Micro and SBI先物・オプションAPI existence are confirmed, "
            "but endpoint-level integration details must be mapped from your actual SBI API registration materials."
        )

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        if self.market_data_provider is None:
            raise NotImplementedError(self._message)
        return self.market_data_provider.get_ohlcv(symbol, timeframe, limit)

    def get_ticker(self, symbol: str) -> float:
        if self.market_data_provider is None:
            raise NotImplementedError(self._message)
        return self.market_data_provider.get_ticker(symbol)

    def get_position(self, symbol: str) -> PositionState:
        if self.market_data_provider is None:
            raise NotImplementedError(self._message)
        return self.position if self.position.symbol == symbol else PositionState(symbol=symbol)

    def get_balance(self) -> float:
        return self.initial_balance

    def place_order(self, order_request: OrderRequest) -> OrderResult:
        raise NotImplementedError(self._message)

    def cancel_order(self, order_id: str) -> None:
        raise NotImplementedError(self._message)

    def list_open_orders(self, symbol: str):
        raise NotImplementedError(self._message)

    def connectivity_check(self, symbol: str) -> dict[str, Any]:
        return {
            "broker": "sbi",
            "symbol": symbol,
            "api_key_present": bool(self.profile.api_key),
            "api_secret_present": bool(self.profile.api_secret),
            "endpoint_present": bool(self.profile.endpoint),
            "market_data_provider_present": self.market_data_provider is not None,
            "tool_name": self.profile.tool_name,
            "note": self._message,
        }
