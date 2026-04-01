from __future__ import annotations

import argparse
import json
import os
from copy import deepcopy
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
            "allowed_sessions": ["day"],
            "entry_start_time": "09:00",
            "entry_end_time": "10:30",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_morning",
            "timeframe": "15m",
            "breakout_lookback": 12,
            "ema_period": 120,
            "allowed_sessions": ["day"],
            "entry_start_time": "09:15",
            "entry_end_time": "11:15",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "day_breakout_full",
            "timeframe": "15m",
            "breakout_lookback": 20,
            "ema_period": 200,
            "allowed_sessions": ["day"],
            "entry_start_time": "09:00",
            "entry_end_time": "14:45",
            "skip_first_minutes": 15,
            "use_trend_filter": True,
        },
        {
            "name": "night_breakout_early",
            "timeframe": "15m",
            "breakout_lookback": 10,
            "ema_period": 120,
            "allowed_sessions": ["night"],
            "entry_start_time": "17:15",
            "entry_end_time": "22:30",
            "skip_first_minutes": 0,
            "use_trend_filter": True,
        },
        {
            "name": "both_breakout_fast",
            "timeframe": "5m",
            "breakout_lookback": 12,
            "ema_period": 120,
            "allowed_sessions": ["day", "night"],
            "entry_start_time": None,
            "entry_end_time": None,
            "skip_first_minutes": 0,
            "use_trend_filter": True,
        },
        {
            "name": "both_breakout_no_trend",
            "timeframe": "30m",
            "breakout_lookback": 8,
            "ema_period": 80,
            "allowed_sessions": ["day", "night"],
            "entry_start_time": None,
            "entry_end_time": None,
            "skip_first_minutes": 0,
            "use_trend_filter": False,
        },
    ]


def _score_result(result: dict[str, object]) -> float:
    profit = float(result["profit"])
    max_drawdown = max(float(result["max_drawdown"]), 1.0)
    win_rate = float(result["win_rate"])
    trades = float(result["trades"])
    return round((profit / max_drawdown) * 1000 + win_rate * 100 + min(trades, 1000) * 0.01, 4)


def run_research_lab(config_path: str, base_config: AppConfig, *, top: int = 10, min_trades: int = 30) -> dict[str, object]:
    temp_dir = mkdtemp(prefix="kanekasegi-lab-")
    results: list[dict[str, object]] = []
    for index, params in enumerate(_candidate_rules(), start=1):
        candidate = deepcopy(base_config)
        candidate.runtime.timeframe = str(params["timeframe"])
        candidate.strategy.breakout_lookback = int(params["breakout_lookback"])
        candidate.strategy.ema_period = int(params["ema_period"])
        candidate.strategy.allowed_sessions = list(params["allowed_sessions"])
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
            "allowed_sessions": candidate.strategy.allowed_sessions,
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
    return {
        "runs": len(results),
        "min_trades_filter": min_trades,
        "top": ranked[:top],
        "all_results": results,
    }


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.backtest-nk225micro.yaml")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-trades", type=int, default=30)
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mode.value != "backtest":
        raise ValueError("research lab requires mode=backtest")
    result = run_research_lab(args.config, config, top=args.top, min_trades=args.min_trades)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
