from __future__ import annotations

from pathlib import Path

from src.analysis.metrics import summarize_backtest
from src.backtest.engine import run_backtest
from src.backtest.models import BacktestConfig, CompareResult
from src.data.csv_loader import load_ohlcv_csv


def resolve_data_source(config: BacktestConfig, symbol: str | None) -> tuple[Path, str | None]:
    if symbol is None:
        return config.data_file, None
    for source in config.data_sources:
        if source.symbol.lower() == symbol.lower():
            return source.file_path, source.symbol
    raise ValueError(f"Symbol '{symbol}' was not found in config data.sources.")


def compare_backtests(config_specs: list[tuple[str, BacktestConfig]], symbol: str | None = None) -> list[CompareResult]:
    results: list[CompareResult] = []
    for config_path, config in config_specs:
        data_file, resolved_symbol = resolve_data_source(config, symbol)
        candles = load_ohlcv_csv(data_file)
        result = run_backtest(candles, config)
        summary = summarize_backtest(result)
        results.append(
            CompareResult(
                label=Path(config_path).stem,
                config_path=config_path,
                symbol=resolved_symbol,
                strategy_name=config.strategy.name,
                total_pnl=summary.total_pnl,
                win_rate=summary.win_rate,
                profit_factor=summary.profit_factor,
                max_drawdown=summary.max_drawdown,
                trade_count=summary.trade_count,
                stopped_early=summary.stopped_early,
            )
        )

    return sorted(
        results,
        key=lambda item: (
            0 if item.stopped_early else 1,
            item.total_pnl,
            item.profit_factor,
            item.win_rate,
            -item.max_drawdown,
        ),
        reverse=True,
    )

