from __future__ import annotations

from abc import ABC, abstractmethod

from src.backtest.models import BacktestConfig, Candle, SignalAction, SignalSnapshot


class StrategyRuntime(ABC):
    @abstractmethod
    def action_at(self, index: int) -> SignalAction | None:
        raise NotImplementedError

    @abstractmethod
    def snapshot_at(self, index: int) -> SignalSnapshot:
        raise NotImplementedError


class StrategyDefinition(ABC):
    name: str

    @abstractmethod
    def minimum_candles(self, config: BacktestConfig) -> int:
        raise NotImplementedError

    @abstractmethod
    def prepare(self, candles: list[Candle], config: BacktestConfig) -> StrategyRuntime:
        raise NotImplementedError
