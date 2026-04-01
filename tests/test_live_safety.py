from datetime import datetime, timedelta

from kanekasegi.bot import TradingBot
from kanekasegi.config import AppConfig
from kanekasegi.execution import ExecutionEngine
from kanekasegi.risk import RiskEngine
from kanekasegi.storage import Storage
from kanekasegi.types import BotStatus, MarketCandle, PositionState, RunMode, Signal, SignalAction


class DummyExchange:
    def __init__(self):
        self.place_order_calls = 0

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        now = datetime(2024, 1, 1)
        candles = []
        for i in range(limit):
            candles.append(
                MarketCandle(
                    timestamp=now + timedelta(minutes=15 * i),
                    open=100 + i,
                    high=101 + i,
                    low=99 + i,
                    close=100 + i,
                    volume=10,
                )
            )
        return candles

    def get_ticker(self, symbol: str) -> float:
        return 200.0

    def get_position(self, symbol: str) -> PositionState:
        return PositionState(symbol=symbol)

    def get_balance(self) -> float:
        return 100000.0

    def place_order(self, order_request):
        self.place_order_calls += 1
        raise AssertionError("place_order should not be called when live_order_enabled is false")

    def cancel_order(self, order_id: str) -> None:
        return None

    def list_open_orders(self, symbol: str):
        return []


class DummyStrategy:
    def generate_signal(self, market_snapshot, portfolio_state):
        return Signal(
            action=SignalAction.LONG,
            reason="test_live_signal",
            entry_price=market_snapshot.last_price,
            stop_price=market_snapshot.last_price - 10,
        )


class DummyNotifier:
    def __init__(self):
        self.alerts = []
        self.infos = []

    def send_info(self, message: str) -> None:
        self.infos.append(message)

    def send_alert(self, message: str) -> None:
        self.alerts.append(message)


def test_live_signal_is_blocked_until_enabled(tmp_path):
    config = AppConfig.model_validate(
        {
            "mode": "live",
            "runtime": {
                "symbol": "BTC_JPY",
                "timeframe": "15m",
                "poll_seconds": 60,
                "max_order_failures": 3,
                "max_state_failures": 2,
                "candle_limit": 20,
                "data_source": "synthetic",
                "broker": "gmo",
                "live_order_enabled": False,
                "notify_on_blocked_live_signal": True,
            },
            "strategy": {
                "breakout_lookback": 20,
                "ema_period": 200,
                "atr_period": 14,
                "atr_stop_multiplier": 2.0,
                "trailing_atr_multiplier": 2.5,
            },
            "risk": {
                "risk_per_trade_pct": 0.005,
                "max_daily_loss_pct": 0.02,
                "max_simultaneous_positions": 1,
                "max_position_notional": 100000,
            },
            "paper": {
                "initial_balance": 1000000,
                "fee_rate": 0.0004,
                "slippage_bps": 3,
            },
            "storage": {
                "sqlite_path": str(tmp_path / "test.db"),
                "log_path": str(tmp_path / "bot.jsonl"),
                "health_path": str(tmp_path / "health.json"),
                "sqlite_journal_mode": "MEMORY",
            },
        }
    )
    exchange = DummyExchange()
    notifier = DummyNotifier()
    storage = Storage(
        str(tmp_path / "test.db"),
        str(tmp_path / "bot.jsonl"),
        str(tmp_path / "health.json"),
        "MEMORY",
    )
    bot = TradingBot(
        config=config,
        exchange=exchange,
        strategy=DummyStrategy(),
        risk_engine=RiskEngine(config.risk),
        execution_engine=ExecutionEngine(exchange=exchange, storage=storage),
        storage=storage,
        notifier=notifier,
        status=BotStatus(mode=RunMode.LIVE),
    )

    bot.run_cycle()

    assert exchange.place_order_calls == 0
    assert notifier.alerts
    assert "live signal blocked" in notifier.alerts[0]


def test_sbi_live_signal_is_blocked_until_enabled(tmp_path):
    config = AppConfig.model_validate(
        {
            "mode": "live",
            "runtime": {
                "symbol": "NK225MICRO",
                "timeframe": "15m",
                "poll_seconds": 60,
                "max_order_failures": 3,
                "max_state_failures": 2,
                "candle_limit": 20,
                "data_source": "synthetic",
                "broker": "sbi",
                "live_order_enabled": False,
                "notify_on_blocked_live_signal": True,
            },
            "strategy": {
                "breakout_lookback": 20,
                "ema_period": 200,
                "atr_period": 14,
                "atr_stop_multiplier": 2.0,
                "trailing_atr_multiplier": 2.5,
            },
            "risk": {
                "risk_per_trade_pct": 0.005,
                "max_daily_loss_pct": 0.02,
                "max_simultaneous_positions": 1,
                "max_position_notional": 100000,
            },
            "paper": {
                "initial_balance": 300000,
                "fee_rate": 0.0,
                "slippage_bps": 0,
            },
            "storage": {
                "sqlite_path": str(tmp_path / "test-sbi.db"),
                "log_path": str(tmp_path / "bot-sbi.jsonl"),
                "health_path": str(tmp_path / "health-sbi.json"),
                "sqlite_journal_mode": "MEMORY",
            },
        }
    )
    exchange = DummyExchange()
    notifier = DummyNotifier()
    storage = Storage(
        str(tmp_path / "test-sbi.db"),
        str(tmp_path / "bot-sbi.jsonl"),
        str(tmp_path / "health-sbi.json"),
        "MEMORY",
    )
    bot = TradingBot(
        config=config,
        exchange=exchange,
        strategy=DummyStrategy(),
        risk_engine=RiskEngine(config.risk),
        execution_engine=ExecutionEngine(exchange=exchange, storage=storage),
        storage=storage,
        notifier=notifier,
        status=BotStatus(mode=RunMode.LIVE),
    )

    bot.run_cycle()

    assert exchange.place_order_calls == 0
    assert notifier.alerts
    assert "live signal blocked" in notifier.alerts[0]
