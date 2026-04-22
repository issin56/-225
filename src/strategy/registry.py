from __future__ import annotations

from src.strategy.base import StrategyDefinition
from src.strategy.breakout import BreakoutStrategy
from src.strategy.moving_average_cross import MovingAverageCrossStrategy


def get_strategy(name: str) -> StrategyDefinition:
    strategies: dict[str, StrategyDefinition] = {
        "breakout": BreakoutStrategy(),
        "moving_average_cross": MovingAverageCrossStrategy(),
    }
    try:
        return strategies[name]
    except KeyError as error:
        available = ", ".join(sorted(strategies))
        raise ValueError(f"Unknown strategy '{name}'. Available: {available}") from error
