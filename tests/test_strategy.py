from datetime import datetime, timedelta

from kanekasegi.config import StrategyConfig
from kanekasegi.strategy import BreakoutTrendStrategy, MarketSnapshot
from kanekasegi.types import MarketCandle, PositionState, SessionType, SignalAction


def build_trending_candles(direction: str) -> list[MarketCandle]:
    candles = []
    now = datetime(2024, 1, 1)
    price = 100.0
    for i in range(260):
        drift = 1.2 if direction == "up" else -1.2 if direction == "down" else 0.0
        price += drift
        candles.append(
            MarketCandle(
                timestamp=now + timedelta(minutes=15 * i),
                open=price - 0.3,
                high=price + 1.0,
                low=price - 1.0,
                close=price,
                volume=100,
            )
        )
    return candles


def test_strategy_enters_long_in_uptrend_breakout():
    strategy = BreakoutTrendStrategy(StrategyConfig())
    candles = build_trending_candles("up")
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=candles[-1].close), PositionState(symbol="BTCUSDT"))
    assert signal.action == SignalAction.LONG


def test_strategy_enters_short_in_downtrend_breakout():
    strategy = BreakoutTrendStrategy(StrategyConfig())
    candles = build_trending_candles("down")
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=candles[-1].close), PositionState(symbol="BTCUSDT"))
    assert signal.action == SignalAction.SHORT


def test_strategy_respects_long_only_direction_filter():
    strategy = BreakoutTrendStrategy(StrategyConfig(direction_filter="long_only"))
    candles = build_trending_candles("down")
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=candles[-1].close), PositionState(symbol="BTCUSDT"))
    assert signal.action == SignalAction.HOLD
    assert signal.reason == "no_entry"


def test_strategy_respects_day_session_time_filter():
    strategy = BreakoutTrendStrategy(
        StrategyConfig(
            allowed_sessions=["day"],
            entry_start_time="09:00",
            entry_end_time="10:00",
        )
    )
    candles = build_trending_candles("up")
    adjusted = []
    base = datetime(2024, 1, 1, 11, 0)
    for index, candle in enumerate(candles):
        adjusted.append(
            MarketCandle(
                timestamp=base + timedelta(minutes=15 * index),
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
            )
        )
    adjusted[-1].session = None
    signal = strategy.generate_signal(MarketSnapshot(candles=adjusted, last_price=adjusted[-1].close), PositionState(symbol="NK225MICRO"))
    assert signal.action == SignalAction.HOLD
    assert signal.reason == "entry_filtered"


def test_strategy_respects_short_only_filter():
    strategy = BreakoutTrendStrategy(StrategyConfig(direction_filter="short_only"))
    candles = build_trending_candles("up")
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=candles[-1].close), PositionState(symbol="BTCUSDT"))
    assert signal.action == SignalAction.HOLD


def test_strategy_respects_gotobi_filter():
    strategy = BreakoutTrendStrategy(StrategyConfig(allowed_sessions=["day"], calendar_filter="gotobi_only"))
    candles = build_trending_candles("up")
    adjusted = []
    base = datetime(2024, 1, 8, 9, 0)
    for index, candle in enumerate(candles):
        adjusted.append(
            MarketCandle(
                timestamp=base + timedelta(minutes=15 * index),
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
                session=SessionType.DAY,
            )
        )
    signal = strategy.generate_signal(MarketSnapshot(candles=adjusted, last_price=adjusted[-1].close), PositionState(symbol="NK225MICRO"))
    assert signal.action == SignalAction.HOLD
    assert signal.reason == "entry_filtered"


def test_strategy_respects_sq_filter():
    strategy = BreakoutTrendStrategy(StrategyConfig(allowed_sessions=["day"], calendar_filter="sq_only"))
    candles = build_trending_candles("up")
    adjusted = []
    base = datetime(2024, 1, 8, 9, 0)
    for index, candle in enumerate(candles):
        adjusted.append(
            MarketCandle(
                timestamp=base + timedelta(minutes=15 * index),
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
                session=SessionType.DAY,
            )
        )
    signal = strategy.generate_signal(MarketSnapshot(candles=adjusted, last_price=adjusted[-1].close), PositionState(symbol="NK225MICRO"))
    assert signal.action == SignalAction.HOLD
    assert signal.reason == "entry_filtered"


def test_strategy_respects_prior_session_filter():
    strategy = BreakoutTrendStrategy(
        StrategyConfig(
            allowed_sessions=["day"],
            prior_session_filter="down",
            prior_session_min_move_ticks=2,
            tick_size=5.0,
        )
    )
    candles = [
        MarketCandle(
            timestamp=datetime(2024, 1, 5, 17, 0),
            open=30000,
            high=30005,
            low=29985,
            close=29995,
            volume=100,
            session=SessionType.NIGHT,
        ),
        MarketCandle(
            timestamp=datetime(2024, 1, 5, 17, 15),
            open=29995,
            high=30000,
            low=29970,
            close=29980,
            volume=100,
            session=SessionType.NIGHT,
        ),
    ]
    price = 29980.0
    day_start = datetime(2024, 1, 6, 9, 0)
    for index in range(260):
        price += 1.2
        candles.append(
            MarketCandle(
                timestamp=day_start + timedelta(minutes=15 * index),
                open=price - 0.3,
                high=price + 1.0,
                low=price - 1.0,
                close=price,
                volume=100,
                session=SessionType.DAY,
            )
        )
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=candles[-1].close), PositionState(symbol="NK225MICRO"))
    assert signal.action == SignalAction.LONG


def test_strategy_exits_long_on_trailing_stop():
    strategy = BreakoutTrendStrategy(StrategyConfig())
    candles = build_trending_candles("up")
    last_close = candles[-1].close
    position = PositionState(
        symbol="BTCUSDT",
        side=SignalAction.LONG,
        quantity=1,
        entry_price=last_close - 10,
        stop_price=last_close - 30,
        trailing_stop=last_close + 5,
    )
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=last_close), position)
    assert signal.action == SignalAction.EXIT


def test_strategy_exits_short_on_trailing_stop():
    strategy = BreakoutTrendStrategy(StrategyConfig())
    candles = build_trending_candles("down")
    last_close = candles[-1].close
    position = PositionState(
        symbol="BTCUSDT",
        side=SignalAction.SHORT,
        quantity=1,
        entry_price=last_close + 10,
        stop_price=last_close + 30,
        trailing_stop=last_close - 5,
    )
    signal = strategy.generate_signal(MarketSnapshot(candles=candles, last_price=last_close), position)
    assert signal.action == SignalAction.EXIT
