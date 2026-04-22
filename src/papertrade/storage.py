from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.backtest.models import PaperTradeDecision, PaperTradeState, SignalSnapshot


def _ensure_parent(path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def load_paper_trade_state(path: str | Path) -> PaperTradeState | None:
    state_path = Path(path)
    if not state_path.exists():
        return None

    payload = json.loads(state_path.read_text(encoding="utf-8"))
    raw_timestamp = payload.get("last_processed_timestamp")
    return PaperTradeState(
        last_processed_timestamp=None if raw_timestamp is None else datetime.fromisoformat(raw_timestamp),
        current_side=payload.get("current_side"),
        last_action=payload.get("last_action"),
    )


def save_paper_trade_state(path: str | Path, state: PaperTradeState) -> None:
    destination = _ensure_parent(path)
    payload = {
        "last_processed_timestamp": None
        if state.last_processed_timestamp is None
        else state.last_processed_timestamp.isoformat(),
        "current_side": state.current_side,
        "last_action": state.last_action,
    }
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_paper_trade_journal(
    path: str | Path,
    *,
    snapshot: SignalSnapshot,
    decision: PaperTradeDecision,
) -> None:
    destination = _ensure_parent(path)
    signal_payload = None
    if snapshot.signal is not None:
        signal_payload = {
            "timestamp": snapshot.signal.timestamp.isoformat(),
            "action": snapshot.signal.action,
            "side": snapshot.signal.side,
            "price": snapshot.signal.price,
            "short_ma": snapshot.signal.short_ma,
            "long_ma": snapshot.signal.long_ma,
            "reason": snapshot.signal.reason,
        }

    payload = {
        "timestamp": snapshot.timestamp.isoformat(),
        "snapshot_reason": snapshot.reason,
        "close_price": snapshot.close_price,
        "short_ma": snapshot.short_ma,
        "long_ma": snapshot.long_ma,
        "signal": signal_payload,
        "decision": {
            "action": decision.action,
            "reason": decision.reason,
            "current_side_before": decision.current_side_before,
            "current_side_after": decision.current_side_after,
            "processed_new_candle": decision.processed_new_candle,
        },
    }
    with destination.open("a", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
