from datetime import datetime, timedelta
from pathlib import Path

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
from kanekasegi.external_factors import ExternalFactors
from kanekasegi.research_reports import ResearchReportSettings, write_research_report_outputs
from kanekasegi.rule_lab import RuleCandidate, simulate_candidate
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
        paper=PaperConfig(initial_balance=300000, fee_rate=0.0, slippage_bps=0.0),
        storage=StorageConfig(sqlite_path="data/test.db", log_path="logs/test.jsonl", health_path="logs/test-health.json"),
    )


def _monthly_candles(month_count: int = 6, steps_per_month: int = 60) -> list[MarketCandle]:
    candles: list[MarketCandle] = []
    price = 30000.0
    for month_index in range(month_count):
        month = month_index + 1
        start = datetime(2026, month, 6, 9, 0)
        trading_day = f"2026-{month:02d}-06"
        for step in range(steps_per_month):
            timestamp = start + timedelta(minutes=5 * step)
            open_price = price
            close_price = price + 6
            candles.append(
                MarketCandle(
                    timestamp=timestamp,
                    open=open_price,
                    high=close_price + 2,
                    low=open_price - 2,
                    close=close_price,
                    volume=100,
                    session=SessionType.DAY,
                    contract_month="202606",
                    trading_day=trading_day,
                )
            )
            price = close_price
    return candles


def _simple_candidate() -> RuleCandidate:
    return RuleCandidate(
        name="simple_long",
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
        take_profit_ticks=6,
        tick_size=1.0,
        time_stop_bars=1,
    )


def test_write_research_report_outputs_creates_required_files(tmp_path):
    config = _build_config()
    candidate = _simple_candidate()
    candles = _monthly_candles()
    result = simulate_candidate(candles, config, candidate)
    factors = ExternalFactors(
        by_trading_day={
            f"2026-{month:02d}-06": {
                "sp500_change": 1.0,
                "usd_jpy_change": -1.0,
                "vix_change": 0.2,
                "us10y_change_bp": 1.0,
            }
            for month in range(1, 7)
        }
    )

    paths = write_research_report_outputs(
        output_dir=tmp_path,
        config=config,
        candidates=[candidate],
        results_by_name={candidate.name: result},
        candles_by_timeframe={"5m": candles},
        external_factors=factors,
        settings=ResearchReportSettings(min_trades=1, test_months=2, slippage_bps_add=0.1, probe_limit=10),
    )

    expected = {
        "research_candidates_csv",
        "research_candidates_json",
        "monthly_summary",
        "session_summary",
        "direction_summary",
        "external_filter_summary",
        "sq_filter_summary",
        "rejected_candidates",
    }
    assert expected.issubset(paths)
    for key in expected:
        assert Path(paths[key]).exists()

    monthly_text = tmp_path.joinpath("monthly_summary.csv").read_text(encoding="utf-8")
    assert "one_month_dependency_score" in monthly_text
    assert "max_consecutive_losing_months" in monthly_text

    session_text = tmp_path.joinpath("session_summary.csv").read_text(encoding="utf-8")
    assert "day" in session_text
    assert "opening" in session_text

    direction_text = tmp_path.joinpath("direction_summary.csv").read_text(encoding="utf-8")
    assert "long_only" in direction_text


def test_research_reports_reject_too_sparse_candidates(tmp_path):
    config = _build_config()
    candidate = _simple_candidate()
    candles = _monthly_candles(month_count=2, steps_per_month=12)
    result = simulate_candidate(candles, config, candidate)

    write_research_report_outputs(
        output_dir=tmp_path,
        config=config,
        candidates=[candidate],
        results_by_name={candidate.name: result},
        candles_by_timeframe={"5m": candles},
        external_factors=None,
        settings=ResearchReportSettings(min_trades=999, test_months=1),
    )

    rejected_text = tmp_path.joinpath("rejected_candidates.csv").read_text(encoding="utf-8")
    assert "too_few_trades" in rejected_text
