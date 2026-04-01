from kanekasegi.config import AppConfig
from kanekasegi.doctor import run_doctor
from kanekasegi.execution import ExecutionEngine
from kanekasegi.risk import RiskEngine
from kanekasegi.storage import Storage
from kanekasegi.types import BotStatus, RunMode
from kanekasegi.bot import TradingBot


class DummyExchange:
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        return []

    def get_ticker(self, symbol: str) -> float:
        return 0.0

    def get_position(self, symbol: str):
        from kanekasegi.types import PositionState

        return PositionState(symbol=symbol)

    def get_balance(self) -> float:
        return 0.0

    def place_order(self, order_request):
        raise NotImplementedError

    def cancel_order(self, order_id: str) -> None:
        return None

    def list_open_orders(self, symbol: str):
        return []


class DummyNotifier:
    def send_info(self, message: str) -> None:
        return None

    def send_alert(self, message: str) -> None:
        return None


class DummyStrategy:
    def generate_signal(self, market_snapshot, portfolio_state):
        from kanekasegi.types import Signal, SignalAction

        return Signal(action=SignalAction.HOLD, reason="dummy")


def test_doctor_reports_csv_path_check(tmp_path):
    config = AppConfig.model_validate(
        {
            "mode": "backtest",
            "runtime": {
                "symbol": "BTCUSDT",
                "timeframe": "15m",
                "poll_seconds": 60,
                "max_order_failures": 3,
                "max_state_failures": 2,
                "candle_limit": 260,
                "data_source": "csv",
                "csv_path": str(tmp_path / "missing.csv"),
                "broker": "paper",
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
    storage = Storage(str(tmp_path / "test.db"), str(tmp_path / "bot.jsonl"), str(tmp_path / "health.json"), "MEMORY")
    bot = TradingBot(
        config=config,
        exchange=DummyExchange(),
        strategy=DummyStrategy(),
        risk_engine=RiskEngine(config.risk),
        execution_engine=ExecutionEngine(DummyExchange(), storage),
        storage=storage,
        notifier=DummyNotifier(),
        status=BotStatus(mode=RunMode.BACKTEST),
    )
    report = run_doctor(bot)
    assert report["ok"] is False
    assert any(check["name"] == "csv_path_exists" and check["ok"] is False for check in report["checks"])
