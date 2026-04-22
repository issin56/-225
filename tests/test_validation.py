from datetime import datetime, timedelta

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
import kanekasegi.validation as validation
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
        ),
        paper=PaperConfig(initial_balance=300000, fee_rate=0.0, slippage_bps=0.0),
        storage=StorageConfig(sqlite_path="data/test.db", log_path="logs/test.jsonl", health_path="logs/test-health.json"),
    )


def _monthly_candles(month_count: int = 8, steps_per_month: int = 30) -> list[MarketCandle]:
    candles: list[MarketCandle] = []
    price = 30000.0
    for month_index in range(month_count):
        month = month_index + 1
        start = datetime(2025, month, 6, 9, 0)
        trading_day = f"2025-{month:02d}-06"
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
                    contract_month="202503",
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
        tick_size=1.0,
        time_stop_bars=1,
    )


def test_candidate_train_test_validation_returns_ranked_results(monkeypatch):
    candidate = _simple_candidate()
    monkeypatch.setattr(validation, "_select_candidates", lambda names: [candidate])
    monkeypatch.setattr(validation, "_load_candles", lambda config: _monthly_candles())
    monkeypatch.setattr(validation, "_load_external_factors", lambda config: None)

    result = validation.run_candidate_train_test_validation(
        "config.backtest-nk225micro.yaml",
        _build_config(),
        candidate_names=["simple_long"],
        train_months=4,
        test_months=2,
        min_train_trades=1,
        min_test_trades=1,
    )

    assert result["mode"] == "candidate_train_test"
    assert result["train_months"] == ["2025-03", "2025-04", "2025-05", "2025-06"]
    assert result["test_months"] == ["2025-07", "2025-08"]
    assert result["results"][0]["name"] == "simple_long"
    assert result["results"][0]["accepted"] is True
    assert result["results"][0]["test"]["profit"] > 0


def test_candidate_walk_forward_validation_summarizes_windows(monkeypatch):
    candidate = _simple_candidate()
    monkeypatch.setattr(validation, "_select_candidates", lambda names: [candidate])
    monkeypatch.setattr(validation, "_load_candles", lambda config: _monthly_candles())
    monkeypatch.setattr(validation, "_load_external_factors", lambda config: None)

    result = validation.run_candidate_walk_forward_validation(
        "config.backtest-nk225micro.yaml",
        _build_config(),
        candidate_names=["simple_long"],
        train_months=3,
        test_months=2,
        step_months=1,
        min_train_trades=1,
        min_test_trades=1,
    )

    assert result["mode"] == "candidate_walk_forward"
    assert len(result["windows"]) == 4
    assert result["summary"][0]["name"] == "simple_long"
    assert result["summary"][0]["accepted_windows"] == 4


def test_portfolio_walk_forward_validation_returns_summary(monkeypatch):
    candidate = _simple_candidate()
    monkeypatch.setattr(validation, "_select_candidates", lambda names: [candidate])
    monkeypatch.setattr(validation, "_load_candles", lambda config: _monthly_candles())
    monkeypatch.setattr(validation, "_load_external_factors", lambda config: None)

    result = validation.run_portfolio_walk_forward_validation(
        "config.backtest-nk225micro.yaml",
        _build_config(),
        candidate_names=["simple_long"],
        train_months=3,
        test_months=2,
        step_months=1,
        min_train_trades=1,
        min_test_trades=1,
    )

    assert result["mode"] == "portfolio_walk_forward"
    assert result["summary"]["tested_windows"] == 4
    assert result["summary"]["accepted_windows"] == 4
    assert result["summary"]["average_test_profit"] > 0


def test_candidate_rejection_reasons_can_reject_large_drawdown():
    accepted, reason = validation._candidate_rejection_reasons(
        {
            "trades": 12,
            "profit": 1500.0,
            "win_rate": 0.55,
            "max_drawdown": 4200.0,
        },
        min_trades=1,
        min_profit=0.0,
        min_win_rate=0.0,
        max_drawdown=4000.0,
    )

    assert accepted is False
    assert reason == "drawdown_above_threshold"
