from kanekasegi.execution import ExecutionEngine
from kanekasegi.exchange_adapter import PaperExchangeAdapter
from kanekasegi.market_data import InMemoryMarketDataProvider
from kanekasegi.storage import Storage
from kanekasegi.types import PositionState, Signal, SignalAction


def test_exit_updates_daily_pnl(tmp_path):
    storage = Storage(str(tmp_path / "test.db"), str(tmp_path / "bot.jsonl"), sqlite_journal_mode="MEMORY")
    market_data = InMemoryMarketDataProvider(symbol="BTCUSDT", timeframe="15m", seed=1, start_price=100.0)
    exchange = PaperExchangeAdapter(market_data_provider=market_data, initial_balance=100000.0)
    engine = ExecutionEngine(exchange=exchange, storage=storage)

    open_signal = Signal(action=SignalAction.LONG, reason="open", entry_price=100.0, stop_price=95.0)
    opened = engine.execute_signal("BTCUSDT", open_signal, 1.0, PositionState(symbol="BTCUSDT"))
    assert opened.position.is_open is True

    exit_signal = Signal(action=SignalAction.EXIT, reason="close")
    closed = engine.execute_signal("BTCUSDT", exit_signal, opened.position.quantity, opened.position)
    assert closed.position.is_open is False
    assert storage.load_daily_pnl() == closed.realized_pnl - closed.fee_paid
