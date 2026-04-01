from datetime import datetime, timedelta

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
from kanekasegi.rule_lab import RuleCandidate, generate_default_candidates, simulate_candidate
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
        ),
        paper=PaperConfig(initial_balance=300000, fee_rate=0.0, slippage_bps=0.0),
        storage=StorageConfig(sqlite_path="data/test.db", log_path="logs/test.jsonl", health_path="logs/test-health.json"),
    )


def _candles(session: SessionType, steps: int = 260) -> list[MarketCandle]:
    start = datetime(2026, 1, 5, 9, 0)
    price = 30000.0
    candles: list[MarketCandle] = []
    for index in range(steps):
        timestamp = start + timedelta(minutes=15 * index)
        candles.append(
            MarketCandle(
                timestamp=timestamp,
                open=price,
                high=price + 12,
                low=price - 6,
                close=price + 8,
                volume=100,
                session=session,
                contract_month="202603",
                trading_day="2026-01-05",
            )
        )
        price += 6
    return candles


def test_generate_default_candidates_builds_session_and_direction_variants():
    candidates = generate_default_candidates(_build_config())
    assert len(candidates) == 36
    names = {candidate.name for candidate in candidates}
    assert "breakout_day_long_only_lb10_ema100" in names
    assert "breakout_night_short_only_lb20_ema200" in names


def test_simulate_candidate_respects_session_filter():
    config = _build_config()
    candidate = RuleCandidate(
        name="day_only",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="both",
    )
    result = simulate_candidate(_candles(SessionType.NIGHT), config, candidate)
    assert result.trades == 0
    assert result.ending_equity == 300000
