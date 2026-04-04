import zipfile
from pathlib import Path

from kanekasegi.config import load_config
from kanekasegi.research import run_research_lab


HEADER = (
    "trade_date,execution_date,index_type,security_code,session_id,interval_time,"
    "open_price,high_price,low_price,close_price,trade_volume,vwap,number_of_trade,record_no,contract_month\n"
)


def _write_zip(path: Path, rows: list[str]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("sample.csv", HEADER + "".join(rows))


def test_research_lab_returns_ranked_candidates(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows: list[str] = []
    price = 30000
    record_no = 1
    for minute in range(480):
        hh, mm = divmod(minute, 60)
        interval = f"{9 + hh:02d}{mm:02d}"
        open_price = price
        close_price = price + (5 if minute % 2 == 0 else -2)
        high_price = max(open_price, close_price) + 3
        low_price = min(open_price, close_price) - 3
        rows.append(
            f"20230601,20230601,23,168060023,999,{interval},{open_price},{high_price},{low_price},{close_price},10,0,0,{record_no},202306\n"
        )
        price = close_price
        record_no += 1
    _write_zip(zip_path, rows)

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "mode: backtest",
                "runtime:",
                "  symbol: NK225MICRO",
                "  timeframe: 15m",
                "  poll_seconds: 60",
                "  max_order_failures: 3",
                "  max_state_failures: 2",
                "  candle_limit: 20",
                "  data_source: jpx_zip",
                f"  zip_glob: {zip_path.as_posix()}",
                "  broker: paper",
                "  live_order_enabled: false",
                "  notify_on_blocked_live_signal: true",
                "  session_filter: both",
                "  contract_type: current",
                "strategy:",
                "  breakout_lookback: 20",
                "  ema_period: 30",
                "  atr_period: 14",
                "  atr_stop_multiplier: 2.0",
                "  trailing_atr_multiplier: 2.5",
                "risk:",
                "  risk_per_trade_pct: 0.005",
                "  max_daily_loss_pct: 0.02",
                "  max_simultaneous_positions: 1",
                "  initial_capital: 300000",
                "paper:",
                "  initial_balance: 300000",
                "  fee_rate: 0.0",
                "  slippage_bps: 0.0",
                "storage:",
                f"  sqlite_path: {tmp_path.joinpath('lab.db').as_posix()}",
                f"  log_path: {tmp_path.joinpath('lab.jsonl').as_posix()}",
                f"  health_path: {tmp_path.joinpath('lab-health.json').as_posix()}",
                "  sqlite_journal_mode: MEMORY",
            ]
        ),
        encoding="utf-8",
    )

    result = run_research_lab(str(config_path), load_config(config_path), top=3, min_trades=1)

    assert result["runs"] == 14
    assert len(result["top"]) == 3
    assert "score" in result["top"][0]
    assert "allowed_weekdays" in result["top"][0]
    assert "direction_filter" in result["top"][0]
    assert len(result["candidate_names"]) == 14


def test_research_lab_writes_checkpoint(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows: list[str] = []
    price = 30000
    record_no = 1
    for minute in range(480):
        hh, mm = divmod(minute, 60)
        interval = f"{9 + hh:02d}{mm:02d}"
        open_price = price
        close_price = price + (4 if minute % 3 else -1)
        high_price = max(open_price, close_price) + 2
        low_price = min(open_price, close_price) - 2
        rows.append(
            f"20230601,20230601,23,168060023,999,{interval},{open_price},{high_price},{low_price},{close_price},10,0,0,{record_no},202306\n"
        )
        price = close_price
        record_no += 1
    _write_zip(zip_path, rows)

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "mode: backtest",
                "runtime:",
                "  symbol: NK225MICRO",
                "  timeframe: 15m",
                "  poll_seconds: 60",
                "  max_order_failures: 3",
                "  max_state_failures: 2",
                "  candle_limit: 20",
                "  data_source: jpx_zip",
                f"  zip_glob: {zip_path.as_posix()}",
                "  broker: paper",
                "  live_order_enabled: false",
                "  notify_on_blocked_live_signal: true",
                "  session_filter: both",
                "  contract_type: current",
                "strategy:",
                "  breakout_lookback: 20",
                "  ema_period: 30",
                "  atr_period: 14",
                "  atr_stop_multiplier: 2.0",
                "  trailing_atr_multiplier: 2.5",
                "risk:",
                "  risk_per_trade_pct: 0.005",
                "  max_daily_loss_pct: 0.02",
                "  max_simultaneous_positions: 1",
                "  initial_capital: 300000",
                "paper:",
                "  initial_balance: 300000",
                "  fee_rate: 0.0",
                "  slippage_bps: 0.0",
                "storage:",
                f"  sqlite_path: {tmp_path.joinpath('lab.db').as_posix()}",
                f"  log_path: {tmp_path.joinpath('lab.jsonl').as_posix()}",
                f"  health_path: {tmp_path.joinpath('lab-health.json').as_posix()}",
                "  sqlite_journal_mode: MEMORY",
            ]
        ),
        encoding="utf-8",
    )

    checkpoint_dir = tmp_path / "results"
    result = run_research_lab(
        str(config_path),
        load_config(config_path),
        top=2,
        min_trades=1,
        checkpoint_dir=checkpoint_dir,
        batch_name="smoke",
    )

    assert "checkpoint_path" in result
    checkpoint_path = Path(result["checkpoint_path"])
    assert checkpoint_path.exists()
    assert checkpoint_path.parent == checkpoint_dir
    assert checkpoint_path.name.endswith("-smoke.json")


def test_research_lab_can_filter_candidate_names(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows: list[str] = []
    price = 30000
    record_no = 1
    for minute in range(480):
        hh, mm = divmod(minute, 60)
        interval = f"{9 + hh:02d}{mm:02d}"
        open_price = price
        close_price = price + (4 if minute % 2 == 0 else -2)
        high_price = max(open_price, close_price) + 2
        low_price = min(open_price, close_price) - 2
        rows.append(
            f"20230601,20230601,23,168060023,999,{interval},{open_price},{high_price},{low_price},{close_price},10,0,0,{record_no},202306\n"
        )
        price = close_price
        record_no += 1
    _write_zip(zip_path, rows)

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "mode: backtest",
                "runtime:",
                "  symbol: NK225MICRO",
                "  timeframe: 15m",
                "  poll_seconds: 60",
                "  max_order_failures: 3",
                "  max_state_failures: 2",
                "  candle_limit: 20",
                "  data_source: jpx_zip",
                f"  zip_glob: {zip_path.as_posix()}",
                "  broker: paper",
                "  live_order_enabled: false",
                "  notify_on_blocked_live_signal: true",
                "  session_filter: both",
                "  contract_type: current",
                "strategy:",
                "  breakout_lookback: 20",
                "  ema_period: 30",
                "  atr_period: 14",
                "  atr_stop_multiplier: 2.0",
                "  trailing_atr_multiplier: 2.5",
                "risk:",
                "  risk_per_trade_pct: 0.005",
                "  max_daily_loss_pct: 0.02",
                "  max_simultaneous_positions: 1",
                "  initial_capital: 300000",
                "paper:",
                "  initial_balance: 300000",
                "  fee_rate: 0.0",
                "  slippage_bps: 0.0",
                "storage:",
                f"  sqlite_path: {tmp_path.joinpath('lab.db').as_posix()}",
                f"  log_path: {tmp_path.joinpath('lab.jsonl').as_posix()}",
                f"  health_path: {tmp_path.joinpath('lab-health.json').as_posix()}",
                "  sqlite_journal_mode: MEMORY",
            ]
        ),
        encoding="utf-8",
    )

    result = run_research_lab(
        str(config_path),
        load_config(config_path),
        top=2,
        min_trades=1,
        candidate_names=["day_breakout_opening_midweek_long_only", "day_breakout_morning_midweek_short_only"],
    )

    assert result["runs"] == 2
    assert result["candidate_names"] == ["day_breakout_opening_midweek_long_only", "day_breakout_morning_midweek_short_only"]
