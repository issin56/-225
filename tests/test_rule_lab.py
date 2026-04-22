from datetime import datetime, timedelta

from kanekasegi.config import AppConfig, PaperConfig, RiskConfig, RuntimeConfig, StorageConfig, StrategyConfig
from kanekasegi.external_factors import ExternalFactors
from kanekasegi.rule_lab import (
    RuleCandidate,
    _in_entry_window,
    _is_gotobi_day,
    _is_sq_day,
    _supports_calendar_filter,
    _supports_month_filter,
    _position_size,
    _supports_external_factor_filter,
    _supports_prior_session_filter,
    _supports_prior_session_range_filter,
    generate_default_candidates,
    simulate_candidate,
)
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


def test_generate_default_candidates_builds_session_and_direction_variants():
    candidates = generate_default_candidates(_build_config())
    assert len(candidates) == 108
    names = {candidate.name for candidate in candidates}
    assert "breakout_day_long_only_opening_lb10_ema100" in names
    assert "breakout_night_short_only_full_lb20_ema200" in names


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


def test_simulate_candidate_uses_contract_point_value_and_take_profit():
    config = _build_config()
    config.risk.contract_point_value = 10
    candidate = RuleCandidate(
        name="take_profit",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="both",
        take_profit_ticks=2,
        fixed_stop_ticks=6,
    )
    result = simulate_candidate(_candles(SessionType.DAY), config, candidate)
    assert result.trades > 0
    assert result.profit != 0


def test_rule_lab_position_size_respects_notional_and_point_value():
    config = _build_config()
    config.risk.max_position_notional = 300000
    config.risk.contract_point_value = 10
    quantity = _position_size(config, equity=300000, entry_price=30000, stop_price=29950)
    assert quantity == 1


def test_simulate_candidate_respects_weekday_filter_with_saturday_timestamps():
    config = _build_config()
    candles = _candles(SessionType.DAY)
    for candle in candles:
        candle.timestamp = candle.timestamp.replace(day=11)  # Saturday
        candle.trading_day = "2026-01-10"
    candidate = RuleCandidate(
        name="mon_to_fri_only",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="both",
        allowed_weekdays=(0, 1, 2, 3, 4),
    )
    result = simulate_candidate(candles, config, candidate)
    assert result.trades == 0


def test_simulate_candidate_time_stop_closes_position():
    config = _build_config()
    candidate = RuleCandidate(
        name="time_stop",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="long_only",
        time_stop_bars=2,
        exit_on_trend_reversal=False,
        use_trailing_stop=False,
    )
    result = simulate_candidate(_candles(SessionType.DAY), config, candidate)
    assert result.trades > 0


def test_simulate_candidate_fixed_stop_tick_field_supported():
    config = _build_config()
    candidate = RuleCandidate(
        name="fixed_stop",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="long_only",
        fixed_stop_ticks=20,
        use_trailing_stop=False,
        exit_on_trend_reversal=False,
    )
    result = simulate_candidate(_candles(SessionType.DAY), config, candidate)
    assert result.ending_equity > 0


def test_simulate_candidate_with_empty_allowed_weekdays_does_not_trade():
    config = _build_config()
    candidate = RuleCandidate(
        name="weekday_only",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="both",
        allowed_weekdays=(),
    )
    result = simulate_candidate(_candles(SessionType.DAY), config, candidate)
    assert result.trades == 0


def test_gotobi_filter_treats_previous_business_day_as_gotobi():
    assert _is_gotobi_day(datetime(2026, 1, 9).date())
    assert not _is_gotobi_day(datetime(2026, 1, 8).date())


def test_sq_filter_marks_second_friday_only():
    assert _is_sq_day(datetime(2026, 1, 9).date())
    assert not _is_sq_day(datetime(2026, 1, 8).date())


def test_prior_session_filter_detects_previous_session_direction():
    candidate = RuleCandidate(
        name="prior_session_down_only",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        prior_session_filter="down",
        prior_session_min_move_ticks=2,
        tick_size=5.0,
    )
    candles = [
        MarketCandle(
            timestamp=datetime(2026, 1, 5, 17, 0),
            open=30000,
            high=30005,
            low=29985,
            close=29995,
            volume=100,
            session=SessionType.NIGHT,
            contract_month="202603",
            trading_day="2026-01-05",
        ),
        MarketCandle(
            timestamp=datetime(2026, 1, 5, 17, 5),
            open=29995,
            high=30000,
            low=29975,
            close=29980,
            volume=100,
            session=SessionType.NIGHT,
            contract_month="202603",
            trading_day="2026-01-05",
        ),
        MarketCandle(
            timestamp=datetime(2026, 1, 6, 9, 0),
            open=29980,
            high=29990,
            low=29970,
            close=29985,
            volume=100,
            session=SessionType.DAY,
            contract_month="202603",
            trading_day="2026-01-06",
        ),
    ]

    assert _supports_prior_session_filter(candidate, candles, 2)
    candidate.prior_session_filter = "up"
    assert not _supports_prior_session_filter(candidate, candles, 2)


def test_external_factor_filter_requires_matching_sign():
    candidate = RuleCandidate(
        name="usd_jpy_up_only",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        external_factor_name="usd_jpy_change",
        external_factor_filter="positive",
        external_factor_min_value=0.2,
    )
    candle = MarketCandle(
        timestamp=datetime(2026, 1, 5, 9, 0),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.DAY,
        contract_month="202603",
        trading_day="2026-01-05",
    )
    factors = ExternalFactors(by_trading_day={"2026-01-05": {"usd_jpy_change": 0.42}})

    assert _supports_external_factor_filter(candidate, candle, factors)
    candidate.external_factor_filter = "negative"
    assert not _supports_external_factor_filter(candidate, candle, factors)


def test_external_factor_filter_can_require_two_factors():
    candidate = RuleCandidate(
        name="dual_factor",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        external_factor_name="usd_jpy_change",
        external_factor_filter="negative",
        external_factor_min_value=0.2,
        secondary_external_factor_name="us10y_change_bp",
        secondary_external_factor_filter="positive",
        secondary_external_factor_min_value=2.0,
    )
    candle = MarketCandle(
        timestamp=datetime(2026, 1, 5, 9, 0),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.DAY,
        contract_month="202603",
        trading_day="2026-01-05",
    )
    factors = ExternalFactors(by_trading_day={"2026-01-05": {"usd_jpy_change": -0.42, "us10y_change_bp": 5.0}})

    assert _supports_external_factor_filter(candidate, candle, factors)
    candidate.secondary_external_factor_min_value = 6.0
    assert not _supports_external_factor_filter(candidate, candle, factors)


def test_prior_session_range_filter_detects_large_previous_session():
    candidate = RuleCandidate(
        name="prior_session_range_high_only",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        prior_session_range_filter="above",
        prior_session_min_range_ticks=4,
        tick_size=5.0,
    )
    candles = [
        MarketCandle(
            timestamp=datetime(2026, 1, 5, 17, 0),
            open=30000,
            high=30030,
            low=29980,
            close=29995,
            volume=100,
            session=SessionType.NIGHT,
            contract_month="202603",
            trading_day="2026-01-05",
        ),
        MarketCandle(
            timestamp=datetime(2026, 1, 5, 17, 5),
            open=29995,
            high=30025,
            low=29985,
            close=30010,
            volume=100,
            session=SessionType.NIGHT,
            contract_month="202603",
            trading_day="2026-01-05",
        ),
        MarketCandle(
            timestamp=datetime(2026, 1, 6, 9, 0),
            open=30010,
            high=30020,
            low=30000,
            close=30015,
            volume=100,
            session=SessionType.DAY,
            contract_month="202603",
            trading_day="2026-01-06",
        ),
    ]

    assert _supports_prior_session_range_filter(candidate, candles, 2)
    candidate.prior_session_range_filter = "below"
    candidate.prior_session_min_range_ticks = 12
    assert _supports_prior_session_range_filter(candidate, candles, 2)


def test_simulate_candidate_gotobi_only_filter_blocks_non_gotobi_days():
    config = _build_config()
    candles = _candles(SessionType.DAY)
    for candle in candles:
        candle.timestamp = candle.timestamp.replace(day=6)
        candle.trading_day = "2026-01-06"
    candidate = RuleCandidate(
        name="gotobi_only",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="long_only",
        calendar_filter="gotobi_only",
        use_trend_filter=False,
        exit_on_trend_reversal=False,
        use_trailing_stop=False,
        fixed_stop_ticks=20,
        time_stop_bars=1,
    )
    result = simulate_candidate(candles, config, candidate)
    assert result.trades == 0


def test_simulate_candidate_exclude_gotobi_filter_blocks_gotobi_days():
    config = _build_config()
    candles = _candles(SessionType.DAY)
    for candle in candles:
        candle.timestamp = candle.timestamp.replace(day=5)
        candle.trading_day = "2026-01-05"
    candidate = RuleCandidate(
        name="exclude_gotobi",
        breakout_lookback=10,
        ema_period=100,
        atr_period=14,
        atr_stop_multiplier=2.0,
        trailing_atr_multiplier=2.5,
        session_filter="day",
        direction_filter="long_only",
        calendar_filter="exclude_gotobi",
        use_trend_filter=False,
        exit_on_trend_reversal=False,
        use_trailing_stop=False,
        fixed_stop_ticks=20,
        time_stop_bars=1,
    )
    result = simulate_candidate(candles, config, candidate)
    assert result.trades == 0


def test_entry_window_supports_cross_midnight_ranges():
    candle = MarketCandle(
        timestamp=datetime(2026, 1, 6, 0, 15),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.NIGHT,
        contract_month="202603",
        trading_day="2026-01-05",
    )
    candidate = RuleCandidate(
        name="cross_midnight",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        session_filter="night",
        direction_filter="short_only",
        entry_start_time="21:00",
        entry_end_time="00:30",
    )
    assert _in_entry_window(candidate, candle)


def test_month_filter_blocks_excluded_trading_month():
    candidate = RuleCandidate(
        name="exclude_october",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        excluded_months=(10,),
    )
    october_candle = MarketCandle(
        timestamp=datetime(2026, 10, 6, 9, 0),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.DAY,
        contract_month="202612",
        trading_day="2026-10-06",
    )
    november_candle = MarketCandle(
        timestamp=datetime(2026, 11, 6, 9, 0),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.DAY,
        contract_month="202612",
        trading_day="2026-11-06",
    )

    assert not _supports_month_filter(candidate, october_candle)
    assert _supports_month_filter(candidate, november_candle)


def test_calendar_filter_uses_trading_day_for_after_midnight_session_bars():
    candidate = RuleCandidate(
        name="gotobi_after_midnight",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        calendar_filter="gotobi_only",
    )
    candle = MarketCandle(
        timestamp=datetime(2026, 1, 6, 0, 15),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.NIGHT,
        contract_month="202603",
        trading_day="2026-01-05",
    )

    assert _supports_calendar_filter(candidate, candle)


def test_sq_calendar_filter_uses_trading_day_for_after_midnight_session_bars():
    candidate = RuleCandidate(
        name="sq_after_midnight",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        calendar_filter="sq_only",
    )
    candle = MarketCandle(
        timestamp=datetime(2026, 1, 10, 0, 15),
        open=30000,
        high=30010,
        low=29990,
        close=30005,
        volume=100,
        session=SessionType.NIGHT,
        contract_month="202603",
        trading_day="2026-01-09",
    )

    assert _supports_calendar_filter(candidate, candle)


def test_simulate_candidate_uses_trading_day_months_for_active_month_average():
    config = _build_config()
    candidate = RuleCandidate(
        name="cross_month_friday_night",
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

    result = simulate_candidate(_cross_month_night_candles(), config, candidate)

    assert result.trades == 1
    assert result.active_months == 2
    assert result.profit > 0
    assert result.average_monthly_pnl == result.profit / 2


def test_simulate_candidate_supports_fade_entries():
    config = _build_config()
    candidate = RuleCandidate(
        name="opening_range_fade",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        entry_mode="fade",
        entry_buffer_ticks=1,
        session_filter="day",
        direction_filter="short_only",
        fixed_stop_ticks=20,
        take_profit_ticks=4,
        time_stop_bars=1,
        use_trailing_stop=False,
        tick_size=1.0,
    )
    result = simulate_candidate(_candles(SessionType.DAY, steps=40), config, candidate)
    assert result.trades > 0


def test_entry_buffer_ticks_can_block_small_fade_extensions():
    config = _build_config()
    candidate = RuleCandidate(
        name="buffered_fade",
        breakout_lookback=2,
        ema_period=2,
        atr_period=2,
        atr_stop_multiplier=1.0,
        trailing_atr_multiplier=1.0,
        entry_mode="fade",
        entry_buffer_ticks=3,
        session_filter="day",
        direction_filter="short_only",
        fixed_stop_ticks=20,
        time_stop_bars=1,
        use_trailing_stop=False,
        tick_size=1.0,
    )
    result = simulate_candidate(_candles(SessionType.DAY, steps=40), config, candidate)
    assert result.trades == 0
