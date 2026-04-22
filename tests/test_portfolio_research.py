from datetime import datetime, timedelta

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
import kanekasegi.portfolio_research as portfolio_research
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


def _candles(steps: int = 80) -> list[MarketCandle]:
    start = datetime(2026, 1, 5, 9, 0)
    price = 30000.0
    candles: list[MarketCandle] = []
    for index in range(steps):
        timestamp = start + timedelta(minutes=5 * index)
        candles.append(
            MarketCandle(
                timestamp=timestamp,
                open=price,
                high=price + 12,
                low=price - 4,
                close=price + 8,
                volume=100,
                session=SessionType.DAY,
                contract_month="202603",
                trading_day="2026-01-05",
            )
        )
        price += 6
    return candles


def test_run_portfolio_research_returns_breakdown(monkeypatch):
    candidate = RuleCandidate(
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

    monkeypatch.setattr(portfolio_research, "_select_candidates", lambda names: [candidate])
    monkeypatch.setattr(portfolio_research, "_load_candles", lambda config: _candles())

    result = portfolio_research.run_portfolio_research(
        "config.backtest-nk225micro.yaml",
        _build_config(),
        candidate_names=["simple_long"],
    )

    assert result["candidate_names"] == ["simple_long"]
    assert result["trades"] > 0
    assert result["profit"] > 0
    assert result["monthly_pnl"]
    assert result["strategy_breakdown"]["simple_long"]["trades"] > 0
    assert result["strategy_breakdown"]["simple_long"]["monthly_pnl"]
