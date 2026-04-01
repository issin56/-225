from pathlib import Path

from kanekasegi.main import build_bot
from kanekasegi.sbi_adapter import SbiFuturesAdapter


def test_build_bot_returns_sbi_adapter_when_skip_live_credentials(tmp_path):
    config_path = tmp_path / "live-sbi.yaml"
    config_path.write_text(
        """
mode: live
runtime:
  symbol: NK225MICRO
  timeframe: 15m
  poll_seconds: 60
  max_order_failures: 3
  max_state_failures: 2
  candle_limit: 20
  data_source: synthetic
  csv_path:
  broker: sbi
  live_order_enabled: false
  notify_on_blocked_live_signal: true
strategy:
  breakout_lookback: 20
  ema_period: 200
  atr_period: 14
  atr_stop_multiplier: 2.0
  trailing_atr_multiplier: 2.5
risk:
  risk_per_trade_pct: 0.005
  max_daily_loss_pct: 0.02
  max_simultaneous_positions: 1
  max_position_notional: 100000
paper:
  initial_balance: 300000
  fee_rate: 0.0
  slippage_bps: 0
storage:
  sqlite_path: """
        + str((tmp_path / "test.db").as_posix())
        + """
  log_path: """
        + str((tmp_path / "bot.jsonl").as_posix())
        + """
  health_path: """
        + str((tmp_path / "health.json").as_posix())
        + """
  sqlite_journal_mode: MEMORY
""",
        encoding="utf-8",
    )
    bot, _ = build_bot(str(config_path), skip_live_credentials=True)
    assert isinstance(bot.exchange, SbiFuturesAdapter)


def test_sbi_config_file_has_expected_defaults():
    config_text = Path("config.live-sbi.yaml").read_text(encoding="utf-8")
    assert "symbol: NK225MICRO" in config_text
    assert "broker: sbi" in config_text
    assert "initial_balance: 300000" in config_text
