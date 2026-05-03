from datetime import datetime, timedelta
from pathlib import Path

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
from kanekasegi.observability import (
    write_pnl_breakdown_csvs,
    write_pnl_dashboard,
    write_trade_csv,
    write_walk_forward_review,
)
from kanekasegi.portfolio_lab import simulate_portfolio
from kanekasegi.rule_lab import RuleCandidate
from kanekasegi.types import MarketCandle, RunMode, SessionType


def _build_config() -> AppConfig:
    return AppConfig(
        mode=RunMode.BACKTEST,
        runtime=RuntimeConfig(symbol="NK225MICRO", data_source="synthetic", broker="paper"),
        strategy=StrategyConfig(breakout_lookback=20, ema_period=200, atr_period=14),
        risk=RiskConfig(
            risk_per_trade_pct=0.01,
            max_daily_loss_pct=0.02,
            max_simultaneous_positions=1,
            initial_capital=300000,
            min_cash_buffer=50000,
            per_contract_margin=50000,
            contract_point_value=10,
        ),
        paper=PaperConfig(initial_balance=300000, fee_rate=0.0004, slippage_bps=3.0),
        storage=StorageConfig(sqlite_path="data/test.db", log_path="logs/test.jsonl", health_path="logs/test-health.json"),
    )


def _candles(steps: int = 80) -> list[MarketCandle]:
    start = datetime(2026, 1, 5, 9, 0)
    price = 30000.0
    candles: list[MarketCandle] = []
    for index in range(steps):
        timestamp = start + timedelta(minutes=5 * index)
        close_price = price + 8
        candles.append(
            MarketCandle(
                timestamp=timestamp,
                open=price,
                high=close_price + 2,
                low=price - 4,
                close=close_price,
                volume=100,
                session=SessionType.DAY,
                contract_month="202603",
                trading_day="2026-01-05",
            )
        )
        price += 6
    return candles


def _candidate() -> RuleCandidate:
    return RuleCandidate(
        name="observable_long",
        timeframe="5m",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        session_filter="day",
        direction_filter="long_only",
        use_trend_filter=False,
        exit_on_trend_reversal=False,
        use_trailing_stop=False,
        fixed_stop_ticks=4,
        tick_size=1.0,
        time_stop_bars=1,
    )


def test_simulate_portfolio_emits_enriched_trade_records():
    result = simulate_portfolio({"5m": _candles()}, _build_config(), [_candidate()], wf_window_id="wf_01")

    assert result.trade_records
    trade = result.trade_records[0]
    assert trade.rule_id == "observable_long"
    assert trade.strategy_name == "observable_long"
    assert trade.trade_id
    assert trade.session_bucket.startswith("day_")
    assert trade.vol_bucket in {"low", "mid", "high"}
    assert trade.regime_id
    assert trade.config_hash
    assert trade.wf_window_id == "wf_01"


def test_observability_writers_create_csv_markdown_and_svg(tmp_path: Path):
    result = simulate_portfolio({"5m": _candles()}, _build_config(), [_candidate()], wf_window_id="wf_01")
    output_dir = tmp_path / "output"
    docs_dir = tmp_path / "docs"
    trade_csv_path = output_dir / "trades_enriched.csv"

    write_trade_csv(trade_csv_path, result.trade_records)
    breakdown_paths = write_pnl_breakdown_csvs(output_dir, result.trade_records)
    pnl_dashboard = write_pnl_dashboard(
        docs_dir,
        output_dir,
        portfolio_name="observable_long",
        trades=result.trade_records,
        profit=result.profit,
        max_drawdown=result.max_drawdown,
        win_rate=result.win_rate,
        trade_csv_path=trade_csv_path,
        breakdown_paths=breakdown_paths,
    )
    wf_outputs = write_walk_forward_review(
        docs_dir,
        output_dir,
        mode="portfolio_walk_forward",
        candidate_names=["observable_long"],
        windows=[
            {
                "window_index": 1,
                "window_id": "wf_01",
                "window_mode": "rolling",
                "train_months": ["2025-01", "2025-02"],
                "test_months": ["2025-03"],
                "train_start": "2025-01-06T09:00:00",
                "train_end": "2025-02-28T15:00:00",
                "test_start": "2025-03-03T09:00:00",
                "test_end": "2025-03-31T15:00:00",
                "accepted": True,
                "optimization_method": "fixed_candidate_set",
                "best_params": {"candidate_names": ["observable_long"]},
                "parameter_stability_warning": False,
                "single_window_dependency_flag": True,
                "is_oos_ratio": 1.2,
                "is_metrics": {
                    "net_pnl": result.profit * 1.2,
                    "profit_factor": 1.6,
                    "max_drawdown": result.max_drawdown * 0.8,
                    "trades": result.trades,
                    "average_hold_time": 5.0,
                    "side_imbalance": 1.0,
                    "regime_distribution": {"trend_up_mid": 2},
                },
                "oos_metrics": {
                    "net_pnl": result.profit,
                    "profit_factor": 1.4,
                    "max_drawdown": result.max_drawdown,
                    "trades": result.trades,
                    "average_hold_time": 5.0,
                    "side_imbalance": 1.0,
                    "regime_distribution": {"trend_up_mid": 1},
                },
                "test": {
                    "profit": result.profit,
                    "win_rate": result.win_rate,
                    "max_drawdown": result.max_drawdown,
                    "trades": result.trades,
                },
            }
        ],
        summary={
            "tested_windows": 1,
            "accepted_windows": 1,
            "total_test_profit": result.profit,
            "average_test_win_rate": result.win_rate,
            "worst_test_drawdown": result.max_drawdown,
        },
        trade_records=result.trade_records,
        settings={
            "window_mode": "rolling",
            "train_months": 2,
            "test_months": 1,
            "step_months": 1,
            "selection_metric": "score",
            "neighbor_count": 3,
        },
        optimization_method="fixed_candidate_set",
    )

    assert trade_csv_path.exists()
    assert Path(breakdown_paths["pnl_by_rule"]).exists()
    assert Path(pnl_dashboard).exists()
    assert Path(wf_outputs["walk_forward_review"]).exists()
    assert Path(wf_outputs["walk_forward_windows_csv"]).exists()
    assert Path(wf_outputs["walk_forward_summary_json"]).exists()
    assert (output_dir / "equity_curve.svg").exists()
    assert (output_dir / "rule_pnl.svg").exists()
    assert (output_dir / "session_heatmap.svg").exists()
    assert (output_dir / "wfo_oos_windows.svg").exists()
    assert "Enriched Trade Columns" in Path(pnl_dashboard).read_text(encoding="utf-8")
    assert "Walk Forward Review" in Path(wf_outputs["walk_forward_review"]).read_text(encoding="utf-8")
    assert "Window Settings" in Path(wf_outputs["walk_forward_review"]).read_text(encoding="utf-8")
