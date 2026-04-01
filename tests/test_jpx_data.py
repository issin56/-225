import zipfile
from pathlib import Path

from kanekasegi.main import build_bot
from kanekasegi.jpx_data import JpxMinuteZipMarketDataProvider
from kanekasegi.types import SessionType


HEADER = (
    "trade_date,execution_date,index_type,security_code,session_id,interval_time,"
    "open_price,high_price,low_price,close_price,trade_volume,vwap,number_of_trade,record_no,contract_month\n"
)


def _write_zip(path: Path, rows: list[str]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("sample.csv", HEADER + "".join(rows))


def test_jpx_zip_provider_resamples_and_filters_current_contract(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows = [
        "20230601,20230531,23,168060023,003,1630,30860,30930,30860,30910,100,0,0,1,202306\n",
        "20230601,20230531,23,168060023,003,1631,30910,30920,30900,30905,50,0,0,2,202306\n",
        "20230601,20230531,23,168090023,003,1630,30800,30810,30790,30805,10,0,0,3,202309\n",
        "20230601,20230531,23,168090023,003,1631,30805,30815,30800,30810,10,0,0,4,202309\n",
        "20230601,20230601,23,168060023,999,0900,30920,30950,30910,30940,200,0,0,5,202306\n",
        "20230601,20230601,23,168060023,999,0901,30940,30960,30930,30950,180,0,0,6,202306\n",
    ]
    _write_zip(zip_path, rows)

    provider = JpxMinuteZipMarketDataProvider(
        symbol="NK225MICRO",
        timeframe="15m",
        zip_glob=str(zip_path),
        session_filter="both",
        contract_type="current",
    )

    candles = provider.get_ohlcv("NK225MICRO", "15m", 10)
    assert len(candles) == 2
    assert candles[0].session == SessionType.NIGHT
    assert candles[0].contract_month == "202306"
    assert candles[0].timestamp.hour == 16
    assert candles[0].timestamp.minute == 30
    assert candles[0].open == 30860
    assert candles[0].close == 30905
    assert candles[0].volume == 150
    assert candles[1].session == SessionType.DAY
    assert candles[1].volume == 380
    assert candles[1].trading_day == "2023-06-01"


def test_jpx_zip_provider_supports_specific_contract_and_day_filter(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows = [
        "20230601,20230531,23,168060023,003,1630,30860,30930,30860,30910,100,0,0,1,202306\n",
        "20230601,20230601,23,168090023,999,0900,31000,31030,30990,31020,220,0,0,2,202309\n",
        "20230601,20230601,23,168090023,999,0901,31020,31040,31010,31030,200,0,0,3,202309\n",
    ]
    _write_zip(zip_path, rows)

    provider = JpxMinuteZipMarketDataProvider(
        symbol="NK225MICRO",
        timeframe="1m",
        zip_glob=str(zip_path),
        session_filter="day",
        contract_type="specific",
        specific_contract_month="202309",
    )

    candles = provider.get_ohlcv("NK225MICRO", "1m", 10)
    assert len(candles) == 2
    assert all(c.session == SessionType.DAY for c in candles)
    assert all(c.contract_month == "202309" for c in candles)


def test_jpx_zip_provider_describe_returns_summary(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows = [
        "20230601,20230531,23,168060023,003,1630,30860,30930,30860,30910,100,0,0,1,202306\n",
        "20230601,20230601,23,168060023,999,0900,30920,30950,30910,30940,200,0,0,2,202306\n",
    ]
    _write_zip(zip_path, rows)

    provider = JpxMinuteZipMarketDataProvider(
        symbol="NK225MICRO",
        timeframe="1m",
        zip_glob=str(zip_path),
        session_filter="both",
        contract_type="current",
    )

    summary = provider.describe()
    assert summary["zip_files"] == 1
    assert summary["selected_rows"] == 2
    assert summary["candles"] == 2
    assert summary["trade_days"] == 1
    assert summary["session_counts"]["day"] == 1
    assert summary["session_counts"]["night"] == 1


def test_build_bot_supports_jpx_zip_data_source(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows = [
        "20230601,20230531,23,168060023,003,1630,30860,30930,30860,30910,100,0,0,1,202306\n",
        "20230601,20230531,23,168060023,003,1631,30910,30920,30900,30905,50,0,0,2,202306\n",
        "20230601,20230531,23,168060023,003,1632,30905,30925,30900,30920,40,0,0,3,202306\n",
    ]
    _write_zip(zip_path, rows)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        f"""
mode: backtest
runtime:
  symbol: NK225MICRO
  timeframe: 1m
  poll_seconds: 60
  max_order_failures: 3
  max_state_failures: 2
  candle_limit: 2
  data_source: jpx_zip
  zip_glob: {zip_path.as_posix()}
  broker: paper
strategy:
  breakout_lookback: 2
  ema_period: 2
  atr_period: 2
  atr_stop_multiplier: 2.0
  trailing_atr_multiplier: 2.5
risk:
  risk_per_trade_pct: 0.005
  max_daily_loss_pct: 0.5
  max_simultaneous_positions: 1
paper:
  initial_balance: 300000
  fee_rate: 0.0
  slippage_bps: 0
storage:
  sqlite_path: {(tmp_path / "test.db").as_posix()}
  log_path: {(tmp_path / "bot.jsonl").as_posix()}
  health_path: {(tmp_path / "health.json").as_posix()}
  sqlite_journal_mode: MEMORY
""",
        encoding="utf-8",
    )

    bot, market_data = build_bot(str(config_path))
    candles = market_data.get_ohlcv("NK225MICRO", "1m", 2)
    assert bot.config.runtime.data_source == "jpx_zip"
    assert len(candles) == 2
