import zipfile
from pathlib import Path

from kanekasegi.config import load_config
from kanekasegi.main import run_research_grid
import kanekasegi.research as research
from kanekasegi.rule_lab import RuleCandidate


HEADER = (
    "trade_date,execution_date,index_type,security_code,session_id,interval_time,"
    "open_price,high_price,low_price,close_price,trade_volume,vwap,number_of_trade,record_no,contract_month\n"
)


def _write_zip(path: Path, rows: list[str]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("sample.csv", HEADER + "".join(rows))


def test_run_research_grid_returns_ranked_results(tmp_path):
    zip_path = tmp_path / "future_ohlc_minute_23_202306.zip"
    rows: list[str] = []
    price = 30000
    record_no = 1
    for minute in range(120):
        hh, mm = divmod(minute, 60)
        interval = f"{9 + hh:02d}{mm:02d}"
        open_price = price
        close_price = price + 5
        high_price = close_price + 3
        low_price = open_price - 3
        rows.append(
            f"20230601,20230601,23,168060023,999,{interval},{open_price},{high_price},{low_price},{close_price},10,0,0,{record_no},202306\n"
        )
        price += 5
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
                f"  sqlite_path: {tmp_path.joinpath('research.db').as_posix()}",
                f"  log_path: {tmp_path.joinpath('research.jsonl').as_posix()}",
                f"  health_path: {tmp_path.joinpath('research-health.json').as_posix()}",
                "  sqlite_journal_mode: MEMORY",
            ]
        ),
        encoding="utf-8",
    )

    result = run_research_grid(str(config_path), load_config(config_path))

    assert result["runs"] > 0
    assert result["timeframe"] == "15m"
    assert 1 <= len(result["best_by_win_rate"]) <= 5
    assert 1 <= len(result["best_by_profit"]) <= 5


def test_candidate_names_are_unique():
    names = [candidate.name for candidate in research._candidate_rules()]
    assert len(names) == len(set(names))


def test_select_candidates_rejects_duplicate_names(monkeypatch):
    duplicate_candidates = [
        RuleCandidate(
            name="dup",
            timeframe="5m",
            breakout_lookback=2,
            ema_period=2,
            atr_period=2,
            atr_stop_multiplier=1.0,
            trailing_atr_multiplier=1.0,
        ),
        RuleCandidate(
            name="dup",
            timeframe="15m",
            breakout_lookback=3,
            ema_period=3,
            atr_period=3,
            atr_stop_multiplier=1.0,
            trailing_atr_multiplier=1.0,
        ),
    ]
    monkeypatch.setattr(research, "_candidate_rules", lambda: duplicate_candidates)

    try:
        research._select_candidates(["dup"])
    except ValueError as exc:
        assert "duplicate candidate names" in str(exc)
    else:
        raise AssertionError("expected duplicate candidate names error")
