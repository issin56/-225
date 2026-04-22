import zipfile
from pathlib import Path

from kanekasegi.config import load_config
import kanekasegi.research as research
from kanekasegi.research import run_research_lab
from kanekasegi.rule_lab import RuleCandidate


HEADER = (
    "trade_date,execution_date,index_type,security_code,session_id,interval_time,"
    "open_price,high_price,low_price,close_price,trade_volume,vwap,number_of_trade,record_no,contract_month\n"
)


def _write_zip(path: Path, rows: list[str]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("sample.csv", HEADER + "".join(rows))


def _write_config(
    path: Path,
    zip_path: Path,
    *,
    max_position_notional: int | None = None,
    contract_point_value: int | None = None,
) -> None:
    lines = [
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
    ]
    if max_position_notional is not None:
        lines.append(f"  max_position_notional: {max_position_notional}")
    if contract_point_value is not None:
        lines.append(f"  contract_point_value: {contract_point_value}")
    lines.extend(
        [
            "paper:",
            "  initial_balance: 300000",
            "  fee_rate: 0.0",
            "  slippage_bps: 0.0",
            "storage:",
            f"  sqlite_path: {path.parent.joinpath('lab.db').as_posix()}",
            f"  log_path: {path.parent.joinpath('lab.jsonl').as_posix()}",
            f"  health_path: {path.parent.joinpath('lab-health.json').as_posix()}",
            "  sqlite_journal_mode: MEMORY",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


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
    _write_config(config_path, zip_path)

    result = run_research_lab(str(config_path), load_config(config_path), top=3, min_trades=1)

    assert result["runs"] == len(result["all_results"])
    assert result["runs"] >= 13
    assert len(result["top"]) == 3
    assert "score" in result["top"][0]
    assert "profitable_month_ratio" in result["top"][0]
    assert len(result["candidate_names"]) == result["runs"]


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
    _write_config(config_path, zip_path)

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


def test_research_lab_can_filter_candidates(tmp_path):
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
    _write_config(config_path, zip_path)

    result = run_research_lab(
        str(config_path),
        load_config(config_path),
        top=2,
        min_trades=1,
        candidate_names=["day_opening_long_tp", "day_morning_short_tp"],
    )

    assert result["runs"] == 2
    assert result["candidate_names"] == ["day_opening_long_tp", "day_morning_short_tp"]
    assert {item["name"] for item in result["all_results"]} == {"day_opening_long_tp", "day_morning_short_tp"}


def test_research_lab_respects_point_value_through_position_caps(tmp_path, monkeypatch):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows: list[str] = []
    price = 30000
    record_no = 1
    for minute in range(480):
        hh, mm = divmod(minute, 60)
        interval = f"{9 + hh:02d}{mm:02d}"
        open_price = price
        close_price = price + 10
        high_price = close_price + 2
        low_price = open_price - 2
        rows.append(
            f"20230601,20230601,23,168060023,999,{interval},{open_price},{high_price},{low_price},{close_price},10,0,0,{record_no},202306\n"
        )
        price = close_price
        record_no += 1
    _write_zip(zip_path, rows)

    monkeypatch.setattr(
        research,
        "_candidate_rules",
        lambda: [
            RuleCandidate(
                name="simple_breakout",
                timeframe="15m",
                breakout_lookback=2,
                ema_period=2,
                atr_period=2,
                atr_stop_multiplier=1.0,
                trailing_atr_multiplier=1.0,
                session_filter="both",
                direction_filter="long_only",
                use_trend_filter=False,
                exit_on_trend_reversal=False,
                use_trailing_stop=False,
                fixed_stop_ticks=5,
                tick_size=1.0,
                time_stop_bars=1,
            )
        ],
    )

    config_lo = tmp_path / "config-lo.yaml"
    config_hi = tmp_path / "config-hi.yaml"
    _write_config(config_lo, zip_path, max_position_notional=100000, contract_point_value=1)
    _write_config(config_hi, zip_path, max_position_notional=100000, contract_point_value=10)

    result_lo = run_research_lab(str(config_lo), load_config(config_lo), top=13, min_trades=1)
    result_hi = run_research_lab(str(config_hi), load_config(config_hi), top=13, min_trades=1)

    trades_lo = {item["name"]: item["trades"] for item in result_lo["all_results"]}
    trades_hi = {item["name"]: item["trades"] for item in result_hi["all_results"]}

    assert trades_lo["simple_breakout"] > 0
    assert trades_hi["simple_breakout"] == 0
