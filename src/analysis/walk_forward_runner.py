from __future__ import annotations

import argparse
import sys
from dataclasses import asdict

from src.analysis.compare import resolve_data_source
from src.analysis.reporting import write_payload_json
from src.analysis.walk_forward import run_walk_forward_validation
from src.data.csv_loader import load_ohlcv_csv
from src.utils.config import load_backtest_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run walk-forward validation for one config.")
    parser.add_argument(
        "--config",
        default="config/backtest.sample.json",
        help="Path to the backtest config JSON file.",
    )
    parser.add_argument(
        "--symbol",
        help="Optional symbol from data.sources to validate.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_backtest_config(args.config)
        data_file, resolved_symbol = resolve_data_source(config, args.symbol)
        candles = load_ohlcv_csv(data_file)
        report = run_walk_forward_validation(candles, config, symbol=resolved_symbol)

        out_path = config.output.directory / config.output.walk_forward_summary_file
        write_payload_json(out_path, asdict(report))

        if resolved_symbol is not None:
            print(f"Symbol: {resolved_symbol}")
        print(f"Search enabled: {report.search_enabled}")
        print(f"Selection metric: {report.selection_metric}")
        print(f"Walk-forward windows: {report.total_windows}")
        print(f"Passing windows: {report.passing_windows}")
        print(f"Pass rate: {report.pass_rate:.2%}")
        if report.windows:
            print(f"Candidates per window: {report.windows[0].candidate_count}")
            print(f"First selected parameters: {report.windows[0].selected_parameters}")
        print(f"Walk-forward JSON: {out_path}")
        return 0
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"Walk-forward validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
