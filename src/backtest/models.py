from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal


Side = Literal["long", "short"]
SignalAction = Literal["buy", "sell"]
PaperAction = Literal[
    "hold",
    "open_long",
    "open_short",
    "close_long",
    "close_short",
    "flip_to_long",
    "flip_to_short",
]


@dataclass(frozen=True, slots=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True, slots=True)
class DataSource:
    symbol: str
    file_path: Path


@dataclass(frozen=True, slots=True)
class StrategyConfig:
    name: str
    short_ma_period: int
    long_ma_period: int
    allow_reversal: bool
    parameters: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RiskConfig:
    stop_loss: float
    take_profit: float
    spread: float
    commission: float
    initial_capital: float
    risk_per_trade: float
    max_consecutive_losses: int | None
    max_drawdown: float | None


@dataclass(frozen=True, slots=True)
class OutputConfig:
    directory: Path
    trades_file: str
    summary_file: str
    equity_curve_file: str = "equity_curve.csv"
    signal_snapshot_file: str = "signal_snapshot.json"
    signal_history_file: str = "signal_history.csv"
    papertrade_state_file: str = "papertrade_state.json"
    papertrade_journal_file: str = "papertrade_journal.jsonl"
    notifications_file: str = "notifications.jsonl"
    scan_summary_file: str = "scan_summary.json"
    period_summary_csv_file: str = "period_summary.csv"
    period_summary_json_file: str = "period_summary.json"
    walk_forward_summary_file: str = "walk_forward_summary.json"
    compare_summary_file: str = "compare_summary.json"


@dataclass(frozen=True, slots=True)
class WalkForwardConfig:
    training_bars: int = 12
    test_bars: int = 6
    step_bars: int = 6
    minimum_test_trades: int = 1
    selection_metric: str = "total_pnl"
    search_space: dict[str, object] = field(default_factory=dict)
    top_candidates_per_window: int = 3


@dataclass(frozen=True, slots=True)
class BacktestConfig:
    data_file: Path
    strategy: StrategyConfig
    risk: RiskConfig
    output: OutputConfig
    data_sources: list[DataSource] = field(default_factory=list)
    walk_forward: WalkForwardConfig = field(default_factory=WalkForwardConfig)


@dataclass(slots=True)
class Position:
    side: Side
    entry_time: datetime
    entry_price: float
    units: int
    stop_price: float
    take_profit_price: float


@dataclass(frozen=True, slots=True)
class Trade:
    side: Side
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    units: int
    gross_pnl: float
    net_pnl: float
    commission_paid: float
    exit_reason: str


@dataclass(frozen=True, slots=True)
class EquityPoint:
    timestamp: datetime
    equity: float
    drawdown: float


@dataclass(frozen=True, slots=True)
class BacktestResult:
    initial_capital: float
    final_capital: float
    trades: list[Trade]
    equity_curve: list[EquityPoint]
    stopped_early: bool
    stop_reason: str | None


@dataclass(frozen=True, slots=True)
class BacktestSummary:
    initial_capital: float
    final_capital: float
    total_pnl: float
    win_rate: float
    payoff_ratio: float
    profit_factor: float
    max_drawdown: float
    trade_count: int
    average_profit: float
    average_loss: float
    max_winning_streak: int
    max_losing_streak: int
    stopped_early: bool
    stop_reason: str | None


@dataclass(frozen=True, slots=True)
class PendingAction:
    close_position: bool
    open_side: Side | None
    exit_reason: str


@dataclass(frozen=True, slots=True)
class SignalEvent:
    timestamp: datetime
    action: SignalAction
    side: Side
    price: float
    short_ma: float
    long_ma: float
    reason: str


@dataclass(frozen=True, slots=True)
class SignalSnapshot:
    timestamp: datetime
    close_price: float
    short_ma: float | None
    long_ma: float | None
    signal: SignalEvent | None
    reason: str


@dataclass(frozen=True, slots=True)
class PaperTradeState:
    last_processed_timestamp: datetime | None
    current_side: Side | None
    last_action: PaperAction | None


@dataclass(frozen=True, slots=True)
class PaperTradeDecision:
    timestamp: datetime
    action: PaperAction
    reason: str
    current_side_before: Side | None
    current_side_after: Side | None
    signal: SignalEvent | None
    processed_new_candle: bool


@dataclass(frozen=True, slots=True)
class PeriodPerformance:
    period_key: str
    trade_count: int
    total_pnl: float
    win_rate: float
    profit_factor: float
    average_trade_pnl: float
    max_drawdown: float


@dataclass(frozen=True, slots=True)
class NotificationEvent:
    timestamp: datetime
    symbol: str
    severity: str
    title: str
    message: str


@dataclass(frozen=True, slots=True)
class WalkForwardWindowResult:
    window_index: int
    training_start: datetime
    training_end: datetime
    testing_start: datetime
    testing_end: datetime
    candidate_count: int
    selected_parameters: dict[str, object]
    top_training_candidates: list["WalkForwardCandidateResult"]
    training_summary: BacktestSummary
    testing_summary: BacktestSummary
    passed: bool
    fail_reasons: list[str]


@dataclass(frozen=True, slots=True)
class WalkForwardReport:
    symbol: str | None
    strategy_name: str
    training_bars: int
    test_bars: int
    step_bars: int
    selection_metric: str
    search_enabled: bool
    total_windows: int
    passing_windows: int
    pass_rate: float
    windows: list[WalkForwardWindowResult]


@dataclass(frozen=True, slots=True)
class WalkForwardCandidateResult:
    rank: int
    parameters: dict[str, object]
    selection_metric_value: float
    training_summary: BacktestSummary


@dataclass(frozen=True, slots=True)
class CompareResult:
    label: str
    config_path: str
    symbol: str | None
    strategy_name: str
    total_pnl: float
    win_rate: float
    profit_factor: float
    max_drawdown: float
    trade_count: int
    stopped_early: bool
