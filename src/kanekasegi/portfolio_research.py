from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from .config import AppConfig, load_config
from .portfolio_lab import simulate_portfolio
from .research import _load_candles, _load_external_factors, _select_candidates
from .runtime_env import load_dotenv


def run_portfolio_research(
    config_path: str,
    base_config: AppConfig,
    *,
    candidate_names: list[str],
) -> dict[str, object]:
    selected_candidates = _select_candidates(candidate_names)
    external_factors = _load_external_factors(base_config)
    candles_by_timeframe: dict[str, list] = {}
    for candidate in selected_candidates:
        if candidate.timeframe in candles_by_timeframe:
            continue
        config = deepcopy(base_config)
        config.runtime.timeframe = candidate.timeframe
        candles_by_timeframe[candidate.timeframe] = _load_candles(config)

    result = simulate_portfolio(candles_by_timeframe, base_config, selected_candidates, external_factors=external_factors)
    strategy_breakdown = {
        name: {
            "trades": stats.trades,
            "wins": stats.wins,
            "losses": stats.losses,
            "profit": round(stats.profit, 2),
            "monthly_pnl": {month: round(pnl, 2) for month, pnl in sorted(stats.monthly_pnl.items())},
        }
        for name, stats in result.strategy_stats.items()
    }
    return {
        "candidate_names": result.candidate_names,
        "ending_equity": round(result.ending_equity, 2),
        "profit": round(result.profit, 2),
        "trades": result.trades,
        "wins": result.wins,
        "losses": result.losses,
        "win_rate": round(result.win_rate, 4),
        "max_drawdown": round(result.max_drawdown, 2),
        "min_available_balance": round(result.min_available_balance, 2),
        "profitable_months": result.profitable_months,
        "losing_months": result.losing_months,
        "average_monthly_pnl": round(result.average_monthly_pnl, 2),
        "active_months": result.active_months,
        "monthly_pnl": {month: round(pnl, 2) for month, pnl in result.monthly_pnl.items()},
        "strategy_breakdown": strategy_breakdown,
    }


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.backtest-nk225micro.yaml")
    parser.add_argument("--candidate", action="append", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mode.value != "backtest":
        raise ValueError("portfolio research requires mode=backtest")
    result = run_portfolio_research(args.config, config, candidate_names=args.candidate)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
