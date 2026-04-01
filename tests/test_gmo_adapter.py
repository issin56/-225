from datetime import datetime, timezone

from kanekasegi.gmo_adapter import GmoCoinAdapter
from kanekasegi.types import OrderRequest, OrderSide, SignalAction


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class DummySession:
    def __init__(self):
        self.calls = []

    def request(self, method, url, headers=None, params=None, data=None, timeout=None):
        self.calls.append((method, url, params, data))
        if url.endswith("/v1/openPositions"):
            return DummyResponse(
                {
                    "status": 0,
                    "data": {
                        "list": [
                            {
                                "positionId": 123,
                                "symbol": "BTC_JPY",
                                "side": "BUY",
                                "size": "0.01",
                                "price": "100",
                                "lossGain": "5",
                                "losscutPrice": "90",
                                "timestamp": "2024-01-01T00:00:00.000Z",
                            }
                        ]
                    },
                }
            )
        if url.endswith("/v1/closeOrder"):
            assert '"positionId":123' in data
            return DummyResponse({"status": 0, "data": {"orderId": 555}})
        if url.endswith("/v1/orders"):
            return DummyResponse(
                {
                    "status": 0,
                    "data": {
                        "list": [
                            {
                                "orderId": 555,
                                "symbol": "BTC_JPY",
                                "status": "EXECUTED",
                            }
                        ]
                    },
                }
            )
        if url.endswith("/v1/executions"):
            return DummyResponse(
                {
                    "status": 0,
                    "data": {
                        "list": [
                            {
                                "size": "0.01",
                                "price": "101",
                                "timestamp": "2024-01-01T00:01:00.000Z",
                                "lossGain": "1",
                                "fee": "0.1",
                            }
                        ]
                    },
                }
            )
        raise AssertionError(f"unexpected request: {url}")


def test_gmo_get_position_reads_single_open_position():
    adapter = GmoCoinAdapter("key", "secret")
    adapter.session = DummySession()
    position = adapter.get_position("BTC_JPY")
    assert position.side == SignalAction.LONG
    assert position.position_id == "123"
    assert position.opened_at == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)


def test_gmo_close_order_uses_close_order_endpoint():
    adapter = GmoCoinAdapter("key", "secret")
    adapter.session = DummySession()
    result = adapter.place_order(
        OrderRequest(symbol="BTC_JPY", side=OrderSide.SELL, quantity=0.01, reduce_only=True)
    )
    assert result.order_id == "555"
    assert result.realized_pnl == 1.0
