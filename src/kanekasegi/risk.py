from __future__ import annotations

from dataclasses import dataclass
import math

from .config import RiskConfig
from .types import AccountState, PositionState, Signal, SignalAction


@dataclass(slots=True)
class RiskApproval:
    approved: bool
    reason: str
    quantity: float = 0.0


class RiskEngine:
    def __init__(self, config: RiskConfig) -> None:
        self.config = config

    def validate(self, signal: Signal, account_state: AccountState, market_state: PositionState) -> RiskApproval:
        if signal.action == SignalAction.HOLD:
            return RiskApproval(False, "no_action")
        if account_state.daily_realized_pnl <= -(account_state.equity * self.config.max_daily_loss_pct):
            return RiskApproval(False, "daily_loss_limit")
        if self.config.per_contract_margin is not None:
            available_after_buffer = account_state.available_balance - self.config.min_cash_buffer
            if available_after_buffer < self.config.per_contract_margin:
                return RiskApproval(False, "margin_buffer")
        if market_state.is_open and signal.action in {SignalAction.LONG, SignalAction.SHORT}:
            return RiskApproval(False, "existing_position")
        return RiskApproval(True, "approved")

    def size_position(self, entry_price: float, stop_price: float, equity: float) -> float:
        risk_amount = equity * self.config.risk_per_trade_pct
        stop_distance = abs(entry_price - stop_price)
        if stop_distance <= 0:
            raise ValueError("stop distance must be positive")
        quantity = risk_amount / stop_distance
        if self.config.max_position_notional is not None:
            quantity = min(quantity, self.config.max_position_notional / entry_price)
        if self.config.per_contract_margin is not None:
            available_after_buffer = max(equity - self.config.min_cash_buffer, 0.0)
            quantity = min(quantity, math.floor(available_after_buffer / self.config.per_contract_margin))
        return max(quantity, 0.0)
