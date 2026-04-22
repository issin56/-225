from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

from .types import RunMode


class RuntimeConfig(BaseModel):
    symbol: str
    timeframe: str = "15m"
    poll_seconds: int = 60
    max_order_failures: int = 3
    max_state_failures: int = 2
    candle_limit: int = 260
    data_source: str = "synthetic"
    csv_path: str | None = None
    zip_glob: str | None = None
    external_factors_csv: str | None = None
    broker: str = "paper"
    live_order_enabled: bool = False
    notify_on_blocked_live_signal: bool = True
    exchange_timezone: str = "Asia/Tokyo"
    session_filter: str = "both"
    contract_type: str = "current"
    specific_contract_month: str | None = None

    @model_validator(mode="after")
    def validate_data_source(self) -> "RuntimeConfig":
        if self.data_source not in {"synthetic", "csv", "jpx_zip"}:
            raise ValueError("runtime.data_source must be 'synthetic', 'csv', or 'jpx_zip'")
        if self.data_source == "csv" and not self.csv_path:
            raise ValueError("runtime.csv_path is required when runtime.data_source is 'csv'")
        if self.data_source == "jpx_zip" and not self.zip_glob:
            raise ValueError("runtime.zip_glob is required when runtime.data_source is 'jpx_zip'")
        if self.broker not in {"paper", "gmo", "sbi"}:
            raise ValueError("runtime.broker must be 'paper', 'gmo', or 'sbi'")
        if self.session_filter not in {"day", "night", "both"}:
            raise ValueError("runtime.session_filter must be 'day', 'night', or 'both'")
        if self.contract_type not in {"current", "next", "specific"}:
            raise ValueError("runtime.contract_type must be 'current', 'next', or 'specific'")
        if self.contract_type == "specific" and not self.specific_contract_month:
            raise ValueError("runtime.specific_contract_month is required when runtime.contract_type is 'specific'")
        return self


class StrategyConfig(BaseModel):
    breakout_lookback: int = 20
    ema_period: int = 200
    atr_period: int = 14
    atr_stop_multiplier: float = 2.0
    trailing_atr_multiplier: float = 2.5
    tick_size: float = 5.0
    strategy_ids: list[str] = Field(default_factory=lambda: ["rule1"])
    allowed_sessions: list[str] = Field(default_factory=lambda: ["day", "night"])
    direction_filter: str = "both"
    allowed_weekdays: list[int] = Field(default_factory=lambda: [0, 1, 2, 3, 4])
    calendar_filter: str = "all"
    prior_session_filter: str = "all"
    prior_session_min_move_ticks: int = 0
    external_factor_name: str | None = None
    external_factor_filter: str = "all"
    external_factor_min_value: float = 0.0
    entry_start_time: str | None = None
    entry_end_time: str | None = None
    skip_first_minutes: int = 0
    use_trend_filter: bool = True

    @model_validator(mode="after")
    def validate_filters(self) -> "StrategyConfig":
        allowed_sessions = set(self.allowed_sessions)
        if not allowed_sessions.issubset({"day", "night"}):
            raise ValueError("strategy.allowed_sessions must contain only 'day' or 'night'")
        if not self.allowed_sessions:
            raise ValueError("strategy.allowed_sessions must not be empty")
        if self.direction_filter not in {"both", "long_only", "short_only"}:
            raise ValueError("strategy.direction_filter must be 'both', 'long_only', or 'short_only'")
        if self.calendar_filter not in {"all", "gotobi_only", "exclude_gotobi", "sq_only", "exclude_sq"}:
            raise ValueError(
                "strategy.calendar_filter must be 'all', 'gotobi_only', 'exclude_gotobi', 'sq_only', or 'exclude_sq'"
            )
        if self.prior_session_filter not in {"all", "up", "down"}:
            raise ValueError("strategy.prior_session_filter must be 'all', 'up', or 'down'")
        if self.prior_session_min_move_ticks < 0:
            raise ValueError("strategy.prior_session_min_move_ticks must be non-negative")
        if self.external_factor_filter not in {"all", "positive", "negative"}:
            raise ValueError("strategy.external_factor_filter must be 'all', 'positive', or 'negative'")
        if self.external_factor_name is None and self.external_factor_filter != "all":
            raise ValueError("strategy.external_factor_name is required when strategy.external_factor_filter is not 'all'")
        if self.external_factor_min_value < 0:
            raise ValueError("strategy.external_factor_min_value must be non-negative")
        for weekday in self.allowed_weekdays:
            if weekday < 0 or weekday > 6:
                raise ValueError("strategy.allowed_weekdays must contain values from 0 to 6")
        for label, raw in {"entry_start_time": self.entry_start_time, "entry_end_time": self.entry_end_time}.items():
            if raw is None:
                continue
            if len(raw) != 5 or raw[2] != ":":
                raise ValueError(f"strategy.{label} must be in HH:MM format")
            hour = int(raw[:2])
            minute = int(raw[3:])
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError(f"strategy.{label} must be a valid HH:MM time")
        if self.skip_first_minutes < 0:
            raise ValueError("strategy.skip_first_minutes must be non-negative")
        if self.tick_size <= 0:
            raise ValueError("strategy.tick_size must be positive")
        return self


class RiskConfig(BaseModel):
    risk_per_trade_pct: float = 0.005
    max_daily_loss_pct: float = 0.02
    max_simultaneous_positions: int = 1
    max_position_notional: float | None = None
    initial_capital: float = 300000
    min_cash_buffer: float = 0.0
    per_contract_margin: float | None = None
    contract_point_value: float = 1.0

    @model_validator(mode="after")
    def validate_percentages(self) -> "RiskConfig":
        if not 0 < self.risk_per_trade_pct < 1:
            raise ValueError("risk.risk_per_trade_pct must be between 0 and 1")
        if not 0 < self.max_daily_loss_pct < 1:
            raise ValueError("risk.max_daily_loss_pct must be between 0 and 1")
        if self.max_simultaneous_positions < 1:
            raise ValueError("risk.max_simultaneous_positions must be at least 1")
        if self.max_position_notional is not None and self.max_position_notional <= 0:
            raise ValueError("risk.max_position_notional must be positive when set")
        if self.initial_capital <= 0:
            raise ValueError("risk.initial_capital must be positive")
        if self.min_cash_buffer < 0:
            raise ValueError("risk.min_cash_buffer must be non-negative")
        if self.per_contract_margin is not None and self.per_contract_margin <= 0:
            raise ValueError("risk.per_contract_margin must be positive when set")
        if self.contract_point_value <= 0:
            raise ValueError("risk.contract_point_value must be positive")
        return self


class PaperConfig(BaseModel):
    initial_balance: float = 1_000_000
    fee_rate: float = 0.0004
    slippage_bps: float = 3.0


class StorageConfig(BaseModel):
    sqlite_path: str = "data/trading.db"
    log_path: str = "logs/bot.jsonl"
    health_path: str = "logs/health.json"
    sqlite_journal_mode: str = "MEMORY"

    @model_validator(mode="after")
    def validate_storage(self) -> "StorageConfig":
        if self.sqlite_journal_mode not in {"DELETE", "MEMORY", "WAL"}:
            raise ValueError("storage.sqlite_journal_mode must be DELETE, MEMORY, or WAL")
        return self


class AppConfig(BaseModel):
    mode: RunMode = Field(default=RunMode.PAPER)
    runtime: RuntimeConfig
    strategy: StrategyConfig
    risk: RiskConfig
    paper: PaperConfig
    storage: StorageConfig


def load_config(path: str | Path) -> AppConfig:
    with Path(path).open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    return AppConfig.model_validate(raw)
