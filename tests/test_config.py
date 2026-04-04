import pytest

from kanekasegi.config import AppConfig


def test_config_rejects_unknown_data_source():
    with pytest.raises(ValueError):
        AppConfig.model_validate(
            {
                "mode": "paper",
                "runtime": {
                    "symbol": "BTCUSDT",
                    "timeframe": "15m",
                    "poll_seconds": 60,
                    "max_order_failures": 3,
                    "max_state_failures": 2,
                    "candle_limit": 260,
                    "data_source": "unknown",
                },
                "strategy": {
                    "breakout_lookback": 20,
                    "ema_period": 200,
                    "atr_period": 14,
                    "atr_stop_multiplier": 2.0,
                    "trailing_atr_multiplier": 2.5,
                },
                "risk": {
                    "risk_per_trade_pct": 0.005,
                    "max_daily_loss_pct": 0.02,
                    "max_simultaneous_positions": 1,
                    "max_position_notional": 100000,
                },
                "paper": {
                    "initial_balance": 100000,
                    "fee_rate": 0.0004,
                    "slippage_bps": 0,
                },
                "storage": {
                    "sqlite_path": "data/trading.db",
                    "log_path": "logs/bot.jsonl",
                    "health_path": "logs/health.json",
                    "sqlite_journal_mode": "MEMORY",
                },
            }
        )


def test_config_rejects_non_positive_max_position_notional():
    with pytest.raises(ValueError):
        AppConfig.model_validate(
            {
                "mode": "paper",
                "runtime": {
                    "symbol": "BTCUSDT",
                    "timeframe": "15m",
                    "poll_seconds": 60,
                    "max_order_failures": 3,
                    "max_state_failures": 2,
                    "candle_limit": 260,
                    "data_source": "synthetic",
                    "broker": "paper",
                },
                "strategy": {
                    "breakout_lookback": 20,
                    "ema_period": 200,
                    "atr_period": 14,
                    "atr_stop_multiplier": 2.0,
                    "trailing_atr_multiplier": 2.5,
                },
                "risk": {
                    "risk_per_trade_pct": 0.005,
                    "max_daily_loss_pct": 0.02,
                    "max_simultaneous_positions": 1,
                    "max_position_notional": 0,
                },
                "paper": {
                    "initial_balance": 100000,
                    "fee_rate": 0.0004,
                    "slippage_bps": 0,
                },
                "storage": {
                    "sqlite_path": "data/trading.db",
                    "log_path": "logs/bot.jsonl",
                    "health_path": "logs/health.json",
                    "sqlite_journal_mode": "MEMORY",
                },
            }
        )


def test_config_rejects_unknown_direction_filter():
    with pytest.raises(ValueError):
        AppConfig.model_validate(
            {
                "mode": "paper",
                "runtime": {
                    "symbol": "BTCUSDT",
                    "timeframe": "15m",
                    "poll_seconds": 60,
                    "max_order_failures": 3,
                    "max_state_failures": 2,
                    "candle_limit": 260,
                    "data_source": "synthetic",
                    "broker": "paper",
                },
                "strategy": {
                    "breakout_lookback": 20,
                    "ema_period": 200,
                    "atr_period": 14,
                    "atr_stop_multiplier": 2.0,
                    "trailing_atr_multiplier": 2.5,
                    "direction_filter": "invalid",
                },
                "risk": {
                    "risk_per_trade_pct": 0.005,
                    "max_daily_loss_pct": 0.02,
                    "max_simultaneous_positions": 1,
                    "max_position_notional": 100000,
                },
                "paper": {
                    "initial_balance": 100000,
                    "fee_rate": 0.0004,
                    "slippage_bps": 0,
                },
                "storage": {
                    "sqlite_path": "data/trading.db",
                    "log_path": "logs/bot.jsonl",
                    "health_path": "logs/health.json",
                    "sqlite_journal_mode": "MEMORY",
                },
            }
        )
