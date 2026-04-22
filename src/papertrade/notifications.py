from __future__ import annotations

from src.backtest.models import NotificationEvent, PaperTradeDecision, SignalSnapshot


def build_notification(symbol: str, snapshot: SignalSnapshot, decision: PaperTradeDecision) -> NotificationEvent | None:
    if decision.action == "hold":
        return None

    signal_text = "no signal"
    if snapshot.signal is not None:
        signal_text = f"{snapshot.signal.action} @ {snapshot.signal.price:.5f}"

    return NotificationEvent(
        timestamp=decision.timestamp,
        symbol=symbol,
        severity="info",
        title=f"{symbol} {decision.action}",
        message=f"{decision.reason}; signal={signal_text}",
    )
