from __future__ import annotations

import argparse
import sys

from src.analysis.reporting import (
    append_notification_jsonl,
    append_signal_history_csv,
    write_scan_summary_json,
    write_signal_snapshot_json,
)
from src.data.csv_loader import load_ohlcv_csv
from src.papertrade.notifications import build_notification
from src.papertrade.service import (
    build_signal_snapshot,
    create_initial_paper_trade_state,
    evaluate_paper_trade_decision,
)
from src.papertrade.storage import append_paper_trade_journal, load_paper_trade_state, save_paper_trade_state
from src.utils.config import load_backtest_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export signal-only paper trade snapshots.")
    parser.add_argument(
        "--config",
        default="config/backtest.sample.json",
        help="Path to the config JSON file.",
    )
    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="Ignore previous paper-trade state and start from a flat state.",
    )
    parser.add_argument(
        "--symbol",
        help="Optional symbol from data.sources to process.",
    )
    parser.add_argument(
        "--all-symbols",
        action="store_true",
        help="Process every symbol listed in data.sources.",
    )
    return parser


def _resolve_sources(config, symbol: str | None, all_symbols: bool):
    if all_symbols:
        return config.data_sources
    if symbol is None:
        return [config.data_sources[0]]
    for source in config.data_sources:
        if source.symbol.lower() == symbol.lower():
            return [source]
    raise ValueError(f"Symbol '{symbol}' was not found in config data.sources.")


def _symbol_output_directory(config, symbol: str, multi_symbol_mode: bool):
    if multi_symbol_mode:
        return config.output.directory / "papertrade" / symbol
    return config.output.directory


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_backtest_config(args.config)
        sources = _resolve_sources(config, args.symbol, args.all_symbols)
        multi_symbol_mode = len(sources) > 1
        notifications_path = config.output.directory / config.output.notifications_file
        scan_summary_path = config.output.directory / config.output.scan_summary_file
        scan_summary: list[dict[str, object]] = []

        for source in sources:
            candles = load_ohlcv_csv(source.file_path)
            snapshot = build_signal_snapshot(candles, config)
            output_directory = _symbol_output_directory(config, source.symbol, multi_symbol_mode)
            state_path = output_directory / config.output.papertrade_state_file
            journal_path = output_directory / config.output.papertrade_journal_file
            previous_state = create_initial_paper_trade_state() if args.reset_state else load_paper_trade_state(state_path)
            state = previous_state or create_initial_paper_trade_state()
            decision, next_state = evaluate_paper_trade_decision(
                snapshot,
                state,
                allow_reversal=config.strategy.allow_reversal,
            )

            snapshot_path = output_directory / config.output.signal_snapshot_file
            history_path = output_directory / config.output.signal_history_file
            write_signal_snapshot_json(snapshot_path, snapshot)
            if snapshot.signal is not None and decision.processed_new_candle:
                append_signal_history_csv(history_path, snapshot.signal)
            save_paper_trade_state(state_path, next_state)
            append_paper_trade_journal(journal_path, snapshot=snapshot, decision=decision)

            notification = build_notification(source.symbol, snapshot, decision)
            if notification is not None:
                append_notification_jsonl(notifications_path, notification)

            scan_summary.append(
                {
                    "symbol": source.symbol,
                    "data_file": str(source.file_path),
                    "timestamp": snapshot.timestamp.isoformat(),
                    "decision_action": decision.action,
                    "decision_reason": decision.reason,
                    "signal_action": None if snapshot.signal is None else snapshot.signal.action,
                    "signal_reason": snapshot.reason,
                    "output_directory": str(output_directory),
                }
            )

            print(f"[{source.symbol}] Signal snapshot JSON: {snapshot_path}")
            print(f"[{source.symbol}] Paper trade state JSON: {state_path}")
            print(f"[{source.symbol}] Paper trade journal JSONL: {journal_path}")
            print(f"[{source.symbol}] Decision: {decision.action} ({decision.reason})")
            if snapshot.signal is None:
                print(f"[{source.symbol}] No signal detected. Reason: {snapshot.reason}")
            else:
                print(f"[{source.symbol}] Signal detected: {snapshot.signal.action} at {snapshot.signal.price:.5f}")
                print(f"[{source.symbol}] Signal history CSV: {history_path}")

        write_scan_summary_json(scan_summary_path, scan_summary)
        print(f"Scan summary JSON: {scan_summary_path}")
        if any(item["decision_action"] != "hold" for item in scan_summary):
            print(f"Notifications JSONL: {notifications_path}")
        return 0
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"Signal export failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
