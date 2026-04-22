from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

from src.analysis.compare import compare_backtests
from src.analysis.reporting import write_payload_json
from src.utils.config import load_backtest_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare multiple backtest configs.")
    parser.add_argument(
        "--configs",
        nargs="+",
        required=True,
        help="List of config JSON files to compare.",
    )
    parser.add_argument(
        "--symbol",
        help="Optional symbol from data.sources to compare across all configs.",
    )
    parser.add_argument(
        "--out",
        help="Optional output path for the comparison JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config_specs = [(config_path, load_backtest_config(config_path)) for config_path in args.configs]
        if args.symbol is not None:
            filtered_specs = []
            skipped_configs = []
            for config_path, config in config_specs:
                has_symbol = any(source.symbol.lower() == args.symbol.lower() for source in config.data_sources)
                if has_symbol:
                    filtered_specs.append((config_path, config))
                else:
                    skipped_configs.append(config_path)
            config_specs = filtered_specs
            if skipped_configs:
                print(f"Skipped configs without symbol {args.symbol}: {', '.join(skipped_configs)}")
            if not config_specs:
                raise ValueError(f"No configs matched symbol '{args.symbol}'.")

        results = compare_backtests(config_specs, symbol=args.symbol)
        out_path = Path(args.out) if args.out else config_specs[0][1].output.directory / config_specs[0][1].output.compare_summary_file
        write_payload_json(out_path, [asdict(result) for result in results])

        print(f"Compared {len(results)} configs.")
        print(f"Comparison JSON: {out_path}")
        for index, result in enumerate(results, start=1):
            print(
                f"{index}. {result.label} "
                f"strategy={result.strategy_name} pnl={result.total_pnl:.2f} "
                f"win_rate={result.win_rate:.2%} max_dd={result.max_drawdown:.2%}"
            )
        return 0
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"Config comparison failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
