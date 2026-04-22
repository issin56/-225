from datetime import datetime, timedelta

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
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


def _cross_month_night_candles() -> list[MarketCandle]:
    specs = [
        (datetime(2026, 1, 30, 23, 45), "2026-01-30", 30000.0),
        (datetime(2026, 1, 30, 23, 50), "2026-01-30", 30006.0),
        (datetime(2026, 1, 30, 23, 55), "2026-01-30", 30012.0),
        (datetime(2026, 1, 31, 0, 0), "2026-01-30", 30018.0),
        (datetime(2026, 1, 31, 0, 5), "2026-01-30", 30024.0),
        (datetime(2026, 2, 2, 23, 45), "2026-02-02", 30000.0),
        (datetime(2026, 2, 2, 23, 50), "2026-02-02", 30006.0),
        (datetime(2026, 2, 2, 23, 55), "2026-02-02", 30012.0),
        (datetime(2026, 2, 3, 0, 0), "2026-02-02", 30018.0),
        (datetime(2026, 2, 3, 0, 5), "2026-02-02", 30024.0),
    ]
    candles: list[MarketCandle] = []
    for timestamp, trading_day, price in specs:
        candles.append(
            MarketCandle(
                timestamp=timestamp,
                open=price,
                high=price + 6,
                low=price - 2,
                close=price + 4,
                volume=100,
                session=SessionType.NIGHT,
                contract_month="202603",
                trading_day=trading_day,
            )
        )
    return candles


def test_simulate_portfolio_uses_priority_order_for_identical_entries():
    config = _build_config()
    candles = _candles()
    first = RuleCandidate(
        name="first_long",
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
    second = RuleCandidate(
        name="second_long",
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

    result = simulate_portfolio({"5m": candles}, config, [first, second])

    assert result.trades > 0
    assert result.strategy_stats["first_long"].trades > 0
    assert result.strategy_stats["second_long"].trades == 0
    assert result.profit > 0


def test_simulate_portfolio_supports_fade_candidates():
    config = _build_config()
    candles = _candles()
    fade_short = RuleCandidate(
        name="fade_short",
        timeframe="5m",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        entry_mode="fade",
        entry_buffer_ticks=1,
        session_filter="day",
        direction_filter="short_only",
        use_trailing_stop=False,
        fixed_stop_ticks=20,
        take_profit_ticks=4,
        tick_size=1.0,
        time_stop_bars=1,
    )

    result = simulate_portfolio({"5m": candles}, config, [fade_short])

    assert result.trades > 0
    assert result.strategy_stats["fade_short"].trades > 0


def test_simulate_portfolio_uses_trading_day_for_monthly_stats():
    config = _build_config()
    candidate = RuleCandidate(
        name="cross_month_portfolio",
        timeframe="5m",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        session_filter="night",
        direction_filter="long_only",
        allowed_weekdays=(4,),
        entry_start_time="23:45",
        entry_end_time="00:30",
        use_trend_filter=False,
        exit_on_trend_reversal=False,
        use_trailing_stop=False,
        fixed_stop_ticks=20,
        take_profit_ticks=4,
        tick_size=1.0,
        time_stop_bars=1,
    )

    result = simulate_portfolio({"5m": _cross_month_night_candles()}, config, [candidate])

    assert result.trades == 1
    assert result.active_months == 2
    assert list(result.monthly_pnl) == ["2026-01"]
    assert result.profit > 0
    assert result.average_monthly_pnl == result.profit / 2


def test_simulate_portfolio_tracks_strategy_monthly_pnl():
    config = _build_config()
    candles = _candles()
    candidate = RuleCandidate(
        name="monthly_long",
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

    result = simulate_portfolio({"5m": candles}, config, [candidate])

    strategy_monthly = result.strategy_stats["monthly_long"].monthly_pnl
    assert strategy_monthly
    assert sum(strategy_monthly.values()) == result.strategy_stats["monthly_long"].profit
