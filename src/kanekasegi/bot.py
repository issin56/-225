from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .config import AppConfig
from .execution import ExecutionEngine
from .exchange_adapter import ExchangeAdapter
from .notifier import Notifier
from .risk import RiskEngine
from .storage import Storage
from .strategy import BreakoutTrendStrategy, MarketSnapshot
from .types import AccountState, BotStatus, SignalAction


@dataclass(slots=True)
class TradingBot:
    config: AppConfig
    exchange: ExchangeAdapter
    strategy: BreakoutTrendStrategy
    risk_engine: RiskEngine
    execution_engine: ExecutionEngine
    storage: Storage
    notifier: Notifier
    status: BotStatus

    def _state_mismatch(self, stored_position, exchange_position) -> bool:
        return (
            stored_position.is_open != exchange_position.is_open
            or abs(stored_position.quantity - exchange_position.quantity) > 1e-9
            or stored_position.side != exchange_position.side
        )

    def run_cycle(self) -> None:
        symbol = self.config.runtime.symbol
        position = self.storage.load_position(symbol)
        exchange_position = self.exchange.get_position(symbol)
        if self._state_mismatch(position, exchange_position):
            self.status.state_failures += 1
            self.storage.append_log(
                "state_mismatch",
                {
                    "stored_position": {"side": getattr(position.side, "value", None), "quantity": position.quantity},
                    "exchange_position": {"side": getattr(exchange_position.side, "value", None), "quantity": exchange_position.quantity},
                    "failures": self.status.state_failures,
                },
            )
            if self.status.state_failures >= self.config.runtime.max_state_failures:
                self.halt("position state mismatch threshold exceeded")
            return
        self.status.state_failures = 0
        balance = self.exchange.get_balance()
        candles = self.exchange.get_ohlcv(symbol, self.config.runtime.timeframe, self.config.runtime.candle_limit)
        ticker = self.exchange.get_ticker(symbol)
        trading_day = candles[-1].trading_day or candles[-1].timestamp.date().isoformat()
        daily_pnl = self.storage.load_daily_pnl(trading_day)
        account = AccountState(equity=balance, available_balance=balance, daily_realized_pnl=daily_pnl)
        snapshot = MarketSnapshot(candles=candles, last_price=ticker)
        signal = self.strategy.generate_signal(snapshot, position)

        if (
            self.config.mode.value == "live"
            and not self.config.runtime.live_order_enabled
            and signal.action != SignalAction.HOLD
        ):
            payload = {
                "signal": signal.action.value,
                "reason": signal.reason,
                "symbol": symbol,
                "ticker": ticker,
            }
            self.storage.append_log("live_order_blocked", payload)
            self.status.last_heartbeat = datetime.utcnow()
            self.storage.save_status(self.status)
            if self.config.runtime.notify_on_blocked_live_signal:
                self.notifier.send_alert(
                    f"live signal blocked: symbol={symbol} signal={signal.action.value} reason={signal.reason}"
                )
            return

        approval = self.risk_engine.validate(signal, account, position)
        if not approval.approved and signal.action != SignalAction.EXIT:
            self.storage.append_log("risk_rejected", {"reason": approval.reason, "signal": signal.action.value})
            return

        if signal.action in {SignalAction.LONG, SignalAction.SHORT}:
            quantity = self.risk_engine.size_position(signal.entry_price or ticker, signal.stop_price or ticker, account.equity)
        else:
            quantity = position.quantity

        try:
            outcome = self.execution_engine.execute_signal(symbol, signal, quantity, position, trading_day=trading_day)
            self.status.order_failures = 0
        except Exception as exc:
            self.status.order_failures += 1
            self.storage.append_log(
                "order_failure",
                {"error": str(exc), "failures": self.status.order_failures, "signal": signal.action.value},
            )
            if self.status.order_failures >= self.config.runtime.max_order_failures:
                self.halt("order failure threshold exceeded")
            raise
        self.status.last_heartbeat = datetime.utcnow()
        self.storage.save_status(self.status)
        self.storage.append_log(
            "cycle",
            {
                "signal": signal.action.value,
                "reason": signal.reason,
                "position_open": outcome.position.is_open,
                "ticker": ticker,
                "realized_pnl": outcome.realized_pnl,
            },
        )
        self.notifier.send_info(f"cycle completed: signal={signal.action.value} reason={signal.reason}")

    def halt(self, reason: str) -> None:
        self.status.halted = True
        self.status.halt_reason = reason
        self.storage.save_status(self.status)
        self.notifier.send_alert(f"bot halted: {reason}")
