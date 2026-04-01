from datetime import datetime

from kanekasegi.storage import Storage
from kanekasegi.types import MarginSnapshot, OrderResult, OrderSide, PositionState, SignalAction


def test_storage_persists_position(tmp_path):
    storage = Storage(str(tmp_path / "test.db"), str(tmp_path / "bot.jsonl"), sqlite_journal_mode="MEMORY")
    position = PositionState(
        symbol="BTCUSDT",
        side=SignalAction.LONG,
        quantity=1.5,
        position_id="pos-1",
        entry_price=100.0,
        stop_price=95.0,
        trailing_stop=96.0,
    )
    storage.save_position(position)
    loaded = storage.load_position("BTCUSDT")
    assert loaded.symbol == "BTCUSDT"
    assert loaded.quantity == 1.5
    assert loaded.position_id == "pos-1"


def test_storage_persists_order(tmp_path):
    storage = Storage(str(tmp_path / "test.db"), str(tmp_path / "bot.jsonl"), sqlite_journal_mode="MEMORY")
    order = OrderResult(
        order_id="ord-1",
        symbol="BTCUSDT",
        side=OrderSide.BUY,
        quantity=1.0,
        filled_price=100.0,
        status="filled",
        timestamp=datetime.utcnow(),
    )
    storage.save_order(order)
    storage.append_log("order_saved", {"order_id": "ord-1"})
    log_contents = (tmp_path / "bot.jsonl").read_text(encoding="utf-8")
    assert "ord-1" in log_contents


def test_storage_persists_margin_snapshot(tmp_path):
    storage = Storage(str(tmp_path / "test.db"), str(tmp_path / "bot.jsonl"), sqlite_journal_mode="MEMORY")
    storage.save_margin_snapshot(
        MarginSnapshot(
            timestamp=datetime(2024, 1, 1, 9, 0, 0),
            trading_day="2024-01-01",
            available_cash=300000,
            margin_requirement=100000,
            maintenance_margin=80000,
            excess_margin=200000,
        )
    )
    assert (tmp_path / "test.db").exists()
