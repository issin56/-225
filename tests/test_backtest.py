from kanekasegi.backtest import run_backtest
from kanekasegi.main import build_bot


def test_backtest_runs_and_returns_summary(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
mode: backtest
runtime:
  symbol: BTCUSDT
  timeframe: 15m
  poll_seconds: 60
  max_order_failures: 3
  max_state_failures: 2
  candle_limit: 260
strategy:
  breakout_lookback: 20
  ema_period: 200
  atr_period: 14
  atr_stop_multiplier: 2.0
  trailing_atr_multiplier: 2.5
risk:
  risk_per_trade_pct: 0.005
  max_daily_loss_pct: 0.5
  max_simultaneous_positions: 1
paper:
  initial_balance: 100000
  fee_rate: 0.0004
  slippage_bps: 0
storage:
  sqlite_path: """
        + str((tmp_path / "test.db").as_posix())
        + """
  log_path: """
        + str((tmp_path / "bot.jsonl").as_posix())
        + """
""",
        encoding="utf-8",
    )
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    bot, market_data = build_bot(str(config_path))
    summary = run_backtest(bot, market_data, bot.config.runtime.candle_limit)
    assert summary.cycles > 0
    assert summary.ending_equity > 0
    assert summary.starting_equity == 100000
    assert summary.max_drawdown >= 0
    assert summary.min_equity > 0
