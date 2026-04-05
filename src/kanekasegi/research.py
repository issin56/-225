from __future__ import annotations

import argparse
import json
import os
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp

from .backtest import run_backtest
from .config import AppConfig, load_config
from .main import build_bot
from .runtime_env import load_dotenv


def _candidate_rules() -> list[dict[str, object]]:
    return [
        {
            "name": "day_breakout_opening",
            "timeframe": "15m",
            "breakout_lookback": 8,
            "ema_period": 120,
            "atr_stop_multiplier": 2.0,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [0, 1, 2, 3, 4],
            "direction_filter": "both",
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_opening_midweek",
            "timeframe": "15m",
            "breakout_lookback": 8,
            "ema_period": 120,
            "atr_stop_multiplier": 2.0,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "both",
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_opening_midweek_long_only",
            "timeframe": "15m",
            "breakout_lookback": 8,
            "ema_period": 120,
            "atr_stop_multiplier": 2.0,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "long_only",
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_opening_midweek_wide_stop",
            "timeframe": "15m",
            "breakout_lookback": 8,
            "ema_period": 120,
            "atr_stop_multiplier": 2.4,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "both",
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_morning_midweek",
            "timeframe": "15m",
            "breakout_lookback": 12,
            "ema_period": 120,
            "atr_stop_multiplier": 2.0,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "both",
            "entry_start_time": "09:15",
            "entry_end_time": "11:15",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_morning_midweek_long_only",
            "timeframe": "15m",
            "breakout_lookback": 12,
            "ema_period": 120,
            "atr_stop_multiplier": 2.0,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "long_only",
            "entry_start_time": "09:15",
            "entry_end_time": "11:15",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_morning_midweek_short_only",
            "timeframe": "15m",
            "breakout_lookback": 12,
            "ema_period": 120,
            "atr_stop_multiplier": 2.0,
            "trailing_atr_multiplier": 2.5,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "short_only",
            "entry_start_time": "09:15",
            "entry_end_time": "11:15",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_opening_midweek_tight_exit",
            "timeframe": "15m",
            "breakout_lookback": 8,
            "ema_period": 120,
            "atr_stop_multiplier": 1.6,
            "trailing_atr_multiplier": 2.0,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "both",
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_opening_midweek_wide_trail",
            "timeframe": "15m",
            "breakout_lookback": 8,
            "ema_period": 120,
            "atr_stop_multiplier": 2.2,
            "trailing_atr_multiplier": 3.0,
            "allowed_sessions": ["day"],
            "allowed_weekdays": [1, 2, 3],
            "direction_filter": "both",
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
    ]


def _select_candidates(candidate_names: list[str] | None = None) -> list[dict[str, object]]:
    candidates = _candidate_rules()
    if not candidate_names:
        return candidates
    candidate_map = {str(candidate["name"]): candidate for candidate in candidates}
    missing = [name for name in candidate_names if name not in candidate_map]
    if missing:
        raise ValueError(f"unknown candidate names: {', '.join(missing)}")
    return [candidate_map[name] for name in candidate_names]


def _score_result(result: dict[str, object]) -> float:
    profit = float(result["profit"])
    max_drawdown = max(float(result["max_drawdown"]), 1.0)
    win_rate = float(result["win_rate"])
    trades = float(result["trades"])
    return round((profit / max_drawdown) * 1000 + win_rate * 100 + min(trades, 1000) * 0.01, 4)


def _checkpoint_payload(
    config_path: str,
    results: list[dict[str, object]],
    ranked: list[dict[str, object]],
    *,
    min_trades: int,
    top: int,
) -> dict[str, object]:
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "config_path": config_path,
        "runs": len(results),
        "min_trades_filter": min_trades,
        "candidate_names": [str(item["name"]) for item in results],
        "top": ranked[:top],
        "all_results": results,
    }


def _write_checkpoint(checkpoint_dir: str | os.PathLike[str], payload: dict[str, object], *, batch_name: str | None = None) -> str:
    target_dir = Path(checkpoint_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = batch_name or "nk225micro-research"
    checkpoint_path = target_dir / f"{timestamp}-{name}.json"
    checkpoint_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(checkpoint_path)


def run_research_lab(
    config_path: str,
    base_config: AppConfig,
    *,
    top: int = 10,
    min_trades: int = 30,
    candidate_names: list[str] | None = None,
    checkpoint_dir: str | os.PathLike[str] | None = None,
    batch_name: str | None = None,
) -> dict[str, object]:
    temp_dir = mkdtemp(prefix="kanekasegi-lab-")
    results: list[dict[str, object]] = []
    for index, params in enumerate(_select_candidates(candidate_names), start=1):
        candidate = deepcopy(base_config)
        candidate.runtime.timeframe = str(params["timeframe"])
        candidate.strategy.breakout_lookback = int(params["breakout_lookback"])
        candidate.strategy.ema_period = int(params["ema_period"])
        candidate.strategy.atr_stop_multiplier = float(params["atr_stop_multiplier"])
        candidate.strategy.trailing_atr_multiplier = float(params["trailing_atr_multiplier"])
        candidate.strategy.allowed_sessions = list(params["allowed_sessions"])
        candidate.strategy.allowed_weekdays = list(params.get("allowed_weekdays", candidate.strategy.allowed_weekdays))
        candidate.strategy.direction_filter = str(params.get("direction_filter", candidate.strategy.direction_filter))
        candidate.strategy.entry_start_time = params["entry_start_time"]
        candidate.strategy.entry_end_time = params["entry_end_time"]
        candidate.strategy.skip_first_minutes = int(params["skip_first_minutes"])
        candidate.strategy.use_trend_filter = bool(params["use_trend_filter"])
        candidate.storage.sqlite_path = os.path.join(temp_dir, f"lab-{index}.db")
        candidate.storage.log_path = os.path.join(temp_dir, f"lab-{index}.jsonl")
        candidate.storage.health_path = os.path.join(temp_dir, f"lab-{index}-health.json")
        bot, market_data = build_bot(config_path, config=candidate, skip_live_credentials=True)
        summary = run_backtest(bot, market_data, candidate.runtime.candle_limit)
        result = {
            "name": params["name"],
            "timeframe": candidate.runtime.timeframe,
            "breakout_lookback": candidate.strategy.breakout_lookback,
            "ema_period": candidate.strategy.ema_period,
            "atr_stop_multiplier": candidate.strategy.atr_stop_multiplier,
            "trailing_atr_multiplier": candidate.strategy.trailing_atr_multiplier,
            "allowed_sessions": candidate.strategy.allowed_sessions,
            "allowed_weekdays": candidate.strategy.allowed_weekdays,
            "direction_filter": candidate.strategy.direction_filter,
            "entry_start_time": candidate.strategy.entry_start_time,
            "entry_end_time": candidate.strategy.entry_end_time,
            "skip_first_minutes": candidate.strategy.skip_first_minutes,
            "use_trend_filter": candidate.strategy.use_trend_filter,
            "ending_equity": round(summary.ending_equity, 2),
            "profit": round(summary.profit, 2),
            "trades": summary.trades,
            "wins": summary.wins,
            "losses": summary.losses,
            "win_rate": round(summary.win_rate, 4),
            "max_drawdown": round(summary.max_drawdown, 2),
            "min_available_balance": round(summary.min_available_balance, 2),
        }
        result["score"] = _score_result(result)
        results.append(result)

    filtered = [item for item in results if int(item["trades"]) >= min_trades]
    ranked = sorted(filtered or results, key=lambda item: (float(item["score"]), float(item["profit"])), reverse=True)
    payload = _checkpoint_payload(config_path, results, ranked, min_trades=min_trades, top=top)
    if checkpoint_dir is not None:
        payload["checkpoint_path"] = _write_checkpoint(checkpoint_dir, payload, batch_name=batch_name)
    return payload


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.backtest-nk225micro.yaml")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-trades", type=int, default=30)
    parser.add_argument("--candidate", action="append", default=None)
    parser.add_argument("--checkpoint-dir", default="results")
    parser.add_argument("--batch-name", default="nk225micro-research")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mode.value != "backtest":
        raise ValueError("research lab requires mode=backtest")
    result = run_research_lab(
        args.config,
        config,
        top=args.top,
        min_trades=args.min_trades,
        candidate_names=args.candidate,
        checkpoint_dir=args.checkpoint_dir,
        batch_name=args.batch_name,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
