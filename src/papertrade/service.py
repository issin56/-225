from __future__ import annotations

from src.backtest.models import (
    BacktestConfig,
    Candle,
    PaperTradeDecision,
    PaperTradeState,
    SignalSnapshot,
)
from src.strategy.registry import get_strategy


def build_signal_snapshot(candles: list[Candle], config: BacktestConfig) -> SignalSnapshot:
    if not candles:
        raise ValueError("At least one candle is required to build a signal snapshot.")

    strategy_runtime = get_strategy(config.strategy.name).prepare(candles, config)
    latest_index = len(candles) - 1
    return strategy_runtime.snapshot_at(latest_index)


def create_initial_paper_trade_state() -> PaperTradeState:
    return PaperTradeState(
        last_processed_timestamp=None,
        current_side=None,
        last_action=None,
    )


def evaluate_paper_trade_decision(
    snapshot: SignalSnapshot,
    state: PaperTradeState,
    *,
    allow_reversal: bool,
) -> tuple[PaperTradeDecision, PaperTradeState]:
    current_side_before = state.current_side
    if state.last_processed_timestamp is not None and snapshot.timestamp <= state.last_processed_timestamp:
        decision = PaperTradeDecision(
            timestamp=snapshot.timestamp,
            action="hold",
            reason="duplicate_candle",
            current_side_before=current_side_before,
            current_side_after=current_side_before,
            signal=snapshot.signal,
            processed_new_candle=False,
        )
        return decision, state

    if snapshot.signal is None:
        next_state = PaperTradeState(
            last_processed_timestamp=snapshot.timestamp,
            current_side=current_side_before,
            last_action="hold",
        )
        decision = PaperTradeDecision(
            timestamp=snapshot.timestamp,
            action="hold",
            reason=snapshot.reason,
            current_side_before=current_side_before,
            current_side_after=current_side_before,
            signal=None,
            processed_new_candle=True,
        )
        return decision, next_state

    if current_side_before is None:
        action = "open_long" if snapshot.signal.side == "long" else "open_short"
        current_side_after = snapshot.signal.side
        reason = "new_signal_open"
    elif current_side_before == snapshot.signal.side:
        action = "hold"
        current_side_after = current_side_before
        reason = "already_in_same_direction"
    elif allow_reversal:
        action = "flip_to_long" if snapshot.signal.side == "long" else "flip_to_short"
        current_side_after = snapshot.signal.side
        reason = "reversal_signal"
    else:
        action = "close_long" if current_side_before == "long" else "close_short"
        current_side_after = None
        reason = "opposite_signal_close_only"

    next_state = PaperTradeState(
        last_processed_timestamp=snapshot.timestamp,
        current_side=current_side_after,
        last_action=action,
    )
    decision = PaperTradeDecision(
        timestamp=snapshot.timestamp,
        action=action,
        reason=reason,
        current_side_before=current_side_before,
        current_side_after=current_side_after,
        signal=snapshot.signal,
        processed_new_candle=True,
    )
    return decision, next_state
