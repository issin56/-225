from __future__ import annotations

import argparse
import sys

from src.analysis.periods import summarize_periods
from src.backtest.engine import run_backtest
from src.analysis.metrics import summarize_backtest
from src.analysis.reporting import (
    write_equity_curve_csv,
    write_period_summary_csv,
    write_period_summary_json,
    write_summary_json,
    write_trades_csv,
)
from src.data.csv_loader import load_ohlcv_csv
from src.utils.config import load_backtest_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the minimal FX backtest tool.")
    parser.add_argument(
        "--config",
        default="config/backtest.sample.json",
        help="Path to the backtest config JSON file.",
    )
    parser.add_argument(
        "--symbol",
        help="Optional symbol from data.sources to backtest.",
    )
    parser.add_argument(
        "--period",
        default="month",
        choices=["month", "quarter", "year"],
        help="Aggregation period for comparison output.",
    )
    return parser


def _resolve_data_file(config, symbol: str | None):
    if symbol is None:
        return config.data_file, None
    for source in config.data_sources:
        if source.symbol.lower() == symbol.lower():
            return source.file_path, source.symbol
    raise ValueError(f"Symbol '{symbol}' was not found in config data.sources.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_backtest_config(args.config)
        data_file, resolved_symbol = _resolve_data_file(config, args.symbol)
        candles = load_ohlcv_csv(data_file)
        result = run_backtest(candles, config)
        summary = summarize_backtest(result)
        period_summary = summarize_periods(result, period=args.period)

        trades_path = config.output.directory / config.output.trades_file
        summary_path = config.output.directory / config.output.summary_file
        equity_curve_path = config.output.directory / config.output.equity_curve_file
        period_summary_csv_path = config.output.directory / config.output.period_summary_csv_file
        period_summary_json_path = config.output.directory / config.output.period_summary_json_file
        write_trades_csv(trades_path, result.trades)
        write_summary_json(summary_path, summary)
        write_equity_curve_csv(equity_curve_path, result.equity_curve)
        write_period_summary_csv(period_summary_csv_path, period_summary)
        write_period_summary_json(period_summary_json_path, period_summary)

        if resolved_symbol is not None:
            print(f"Symbol: {resolved_symbol}")
        print(f"Backtest completed. Trades: {summary.trade_count}")
        print(f"Total PnL: {summary.total_pnl:.2f}")
        print(f"Win rate: {summary.win_rate:.2%}")
        print(f"Max drawdown: {summary.max_drawdown:.2%}")
        print(f"Trades CSV: {trades_path}")
        print(f"Summary JSON: {summary_path}")
        print(f"Equity curve CSV: {equity_curve_path}")
        print(f"Period summary CSV: {period_summary_csv_path}")
        print(f"Period summary JSON: {period_summary_json_path}")
        return 0
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"Backtest failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
