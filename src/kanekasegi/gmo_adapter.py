from __future__ import annotations

import hashlib
import hmac
import json
import time
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import requests

from .exchange_adapter import ExchangeAdapter
from .types import MarketCandle, OrderRequest, OrderResult, OrderSide, PositionState, SignalAction


class GmoCoinAdapter(ExchangeAdapter):
    public_base_url = "https://api.coin.z.com/public"
    private_base_url = "https://api.coin.z.com/private"

    def __init__(self, api_key: str, api_secret: str, timeout: int = 10) -> None:
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.timeout = timeout
        self.session = requests.Session()

    def _timestamp(self) -> str:
        return str(int(time.time() * 1000))

    def _sign(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        payload = f"{timestamp}{method}{path}{body}"
        return hmac.new(self.api_secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()

    def _private_request(self, method: str, path: str, *, params: dict[str, Any] | None = None, body: dict[str, Any] | None = None) -> dict[str, Any]:
        timestamp = self._timestamp()
        body_text = json.dumps(body, separators=(",", ":")) if body else ""
        sign = self._sign(timestamp, method, path, body_text)
        headers = {
            "API-KEY": self.api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign,
            "Content-Type": "application/json",
        }
        url = f"{self.private_base_url}{path}"
        response = self.session.request(
            method,
            url,
            headers=headers,
            params=params,
            data=body_text or None,
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != 0:
            raise ValueError(f"GMO private API error: {payload}")
        return payload["data"]

    def _public_request(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        response = self.session.get(f"{self.public_base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != 0:
            raise ValueError(f"GMO public API error: {payload}")
        return payload["data"]

    def _map_symbol_public(self, symbol: str) -> str:
        return symbol.replace("_JPY", "")

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        public_symbol = self._map_symbol_public(symbol)
        interval_map = {"15m": "15min", "1h": "1hour", "4h": "4hour", "1d": "1day"}
        interval = interval_map.get(timeframe, timeframe)
        candles: list[MarketCandle] = []
        current_jst = datetime.now(UTC) + timedelta(hours=9)
        for offset in range(5):
            trading_day = (current_jst - timedelta(days=offset)).strftime("%Y%m%d")
            chunk = self._public_request("/v1/klines", {"symbol": public_symbol, "interval": interval, "date": trading_day})
            for item in chunk:
                candles.append(
                    MarketCandle(
                        timestamp=datetime.fromtimestamp(int(item["openTime"]) / 1000, tz=UTC),
                        open=float(item["open"]),
                        high=float(item["high"]),
                        low=float(item["low"]),
                        close=float(item["close"]),
                        volume=float(item["volume"]),
                    )
                )
            if len(candles) >= limit:
                break
        candles.sort(key=lambda c: c.timestamp)
        return candles[-limit:]

    def get_ticker(self, symbol: str) -> float:
        public_symbol = self._map_symbol_public(symbol)
        data = self._public_request("/v1/ticker", {"symbol": public_symbol})
        ticker = data[0] if isinstance(data, list) else data
        return float(ticker["last"])

    def get_position(self, symbol: str) -> PositionState:
        positions = self._private_request("GET", "/v1/openPositions", params={"symbol": symbol, "page": 1, "count": 100})
        open_list = positions.get("list", []) if isinstance(positions, dict) else positions
        if not open_list:
            return PositionState(symbol=symbol)
        if len(open_list) > 1:
            raise ValueError(f"GMO adapter expected at most one open position for {symbol}, found {len(open_list)}")
        current = open_list[0]
        quantity = float(current.get("size", 0) or 0)
        side = SignalAction.LONG if current["side"] == "BUY" else SignalAction.SHORT
        return PositionState(
            symbol=current["symbol"],
            side=side,
            position_id=str(current["positionId"]),
            quantity=quantity,
            entry_price=float(current.get("price", 0) or 0),
            stop_price=float(current.get("losscutPrice", 0) or 0) or None,
            unrealized_pnl=float(current.get("lossGain", 0) or 0),
            opened_at=datetime.fromisoformat(current["timestamp"].replace("Z", "+00:00")) if current.get("timestamp") else None,
        )

    def get_balance(self) -> float:
        data = self._private_request("GET", "/v1/account/margin")
        return float(data["availableAmount"])

    def get_margin_status(self) -> dict[str, Any]:
        return self._private_request("GET", "/v1/account/margin")

    def place_order(self, order_request: OrderRequest) -> OrderResult:
        if order_request.reduce_only:
            current_position = self.get_position(order_request.symbol)
            if not current_position.is_open or not current_position.position_id:
                raise ValueError(f"no open GMO position found for {order_request.symbol}")
            body = {
                "symbol": order_request.symbol,
                "side": "BUY" if order_request.side == OrderSide.BUY else "SELL",
                "executionType": "MARKET",
                "timeInForce": "FAK",
                "settlePosition": [
                    {
                        "positionId": int(current_position.position_id),
                        "size": str(order_request.quantity),
                    }
                ],
            }
            data = self._private_request("POST", "/v1/closeOrder", body=body)
        else:
            body = {
                "symbol": order_request.symbol,
                "side": "BUY" if order_request.side == OrderSide.BUY else "SELL",
                "executionType": "MARKET",
                "size": str(order_request.quantity),
                "timeInForce": "FAK",
            }
            if order_request.stop_price is not None:
                body["losscutPrice"] = str(order_request.stop_price)
            data = self._private_request("POST", "/v1/order", body=body)
        order_id = str(data["orderId"])
        order_data = self._private_request("GET", "/v1/orders", params={"orderId": order_id})
        order_info = order_data["list"][0]
        execution_data = self._private_request("GET", "/v1/executions", params={"orderId": order_id})
        execution_info = execution_data["list"][0]
        return OrderResult(
            order_id=order_id,
            symbol=order_info["symbol"],
            side=order_request.side,
            quantity=float(execution_info["size"]),
            filled_price=float(execution_info["price"]),
            status=order_info["status"].lower(),
            timestamp=datetime.fromisoformat(execution_info["timestamp"].replace("Z", "+00:00")),
            realized_pnl=float(execution_info.get("lossGain", 0) or 0),
            fee_paid=float(execution_info.get("fee", 0) or 0),
        )

    def cancel_order(self, order_id: str) -> None:
        self._private_request("POST", "/v1/cancelOrder", body={"orderId": int(order_id)})

    def list_open_orders(self, symbol: str):
        data = self._private_request("GET", "/v1/activeOrders", params={"symbol": symbol, "page": 1, "count": 100})
        return data.get("list", [])

    def connectivity_check(self, symbol: str) -> dict[str, Any]:
        margin = self.get_margin_status()
        position = self.get_position(symbol)
        return {
            "ticker": self.get_ticker(symbol),
            "balance": float(margin["availableAmount"]),
            "margin_ratio": margin.get("marginRatio"),
            "margin_call_status": margin.get("marginCallStatus"),
            "open_orders": len(self.list_open_orders(symbol)),
            "position": {
                "symbol": position.symbol,
                "quantity": position.quantity,
                "side": getattr(position.side, "value", None),
                "position_id": position.position_id,
            },
        }
