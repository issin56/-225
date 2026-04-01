from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class RunMode(str, Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"


class SignalAction(str, Enum):
    LONG = "long"
    SHORT = "short"
    EXIT = "exit"
    HOLD = "hold"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class SessionType(str, Enum):
    DAY = "day"
    NIGHT = "night"


class ContractType(str, Enum):
    CURRENT = "current"
    NEXT = "next"
    SPECIFIC = "specific"


@dataclass(slots=True)
class MarketCandle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    session: SessionType | None = None
    contract_month: str | None = None
    trading_day: str | None = None


@dataclass(slots=True)
class Signal:
    action: SignalAction
    reason: str
    entry_price: float | None = None
    stop_price: float | None = None
    trailing_distance: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class OrderRequest:
    symbol: str
    side: OrderSide
    quantity: float
    order_type: str = "market"
    reduce_only: bool = False
    stop_price: float | None = None
    client_order_id: str | None = None


@dataclass(slots=True)
class OrderResult:
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    filled_price: float
    status: str
    timestamp: datetime
    realized_pnl: float = 0.0
    fee_paid: float = 0.0


@dataclass(slots=True)
class PositionState:
    symbol: str
    side: SignalAction | None = None
    strategy_id: str | None = None
    quantity: float = 0.0
    position_id: str | None = None
    entry_price: float = 0.0
    stop_price: float | None = None
    trailing_stop: float | None = None
    unrealized_pnl: float = 0.0
    opened_at: datetime | None = None

    @property
    def is_open(self) -> bool:
        return self.quantity > 0 and self.side in {SignalAction.LONG, SignalAction.SHORT}


@dataclass(slots=True)
class AccountState:
    equity: float
    available_balance: float
    margin_requirement: float = 0.0
    maintenance_margin: float = 0.0
    daily_realized_pnl: float = 0.0
    consecutive_losses: int = 0


@dataclass(slots=True)
class StrategyAllocation:
    strategy_id: str
    enabled: bool = True
    priority: int = 100
    max_contracts: int = 1
    allow_entry_session: SessionType | None = None


@dataclass(slots=True)
class MarginSnapshot:
    timestamp: datetime
    trading_day: str
    available_cash: float
    margin_requirement: float
    maintenance_margin: float
    excess_margin: float


@dataclass(slots=True)
class BotStatus:
    mode: RunMode
    halted: bool = False
    halt_reason: str | None = None
    order_failures: int = 0
    state_failures: int = 0
    last_heartbeat: datetime | None = None
