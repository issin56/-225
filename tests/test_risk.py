from kanekasegi.config import RiskConfig
from kanekasegi.risk import RiskEngine
from kanekasegi.types import AccountState, PositionState, Signal, SignalAction


def test_position_size_respects_stop_distance():
    engine = RiskEngine(RiskConfig(risk_per_trade_pct=0.005, max_daily_loss_pct=0.02, max_simultaneous_positions=1))
    quantity = engine.size_position(entry_price=100, stop_price=95, equity=100000)
    assert quantity == 100.0


def test_daily_loss_limit_rejects_new_entries():
    engine = RiskEngine(RiskConfig(risk_per_trade_pct=0.005, max_daily_loss_pct=0.02, max_simultaneous_positions=1))
    approval = engine.validate(
        Signal(action=SignalAction.LONG, reason="test", entry_price=100, stop_price=95),
        AccountState(equity=100000, available_balance=100000, daily_realized_pnl=-2500),
        PositionState(symbol="BTCUSDT"),
    )
    assert approval.approved is False
    assert approval.reason == "daily_loss_limit"


def test_margin_buffer_rejects_when_cash_is_too_low():
    engine = RiskEngine(
        RiskConfig(
            risk_per_trade_pct=0.005,
            max_daily_loss_pct=0.02,
            max_simultaneous_positions=1,
            max_position_notional=100000,
            initial_capital=300000,
            min_cash_buffer=50000,
            per_contract_margin=260000,
        )
    )
    approval = engine.validate(
        Signal(action=SignalAction.LONG, reason="test", entry_price=100, stop_price=95),
        AccountState(equity=300000, available_balance=300000, daily_realized_pnl=0),
        PositionState(symbol="NK225MICRO"),
    )
    assert approval.approved is False
    assert approval.reason == "margin_buffer"


def test_position_size_is_capped_by_per_contract_margin():
    engine = RiskEngine(
        RiskConfig(
            risk_per_trade_pct=0.5,
            max_daily_loss_pct=0.02,
            max_simultaneous_positions=1,
            max_position_notional=1_000_000,
            initial_capital=300000,
            min_cash_buffer=50000,
            per_contract_margin=120000,
        )
    )
    quantity = engine.size_position(entry_price=100, stop_price=50, equity=300000)
    assert quantity == 2
