from __future__ import annotations

import argparse
import json
from pathlib import Path


def analyze_monthly_pnl(monthly_pnl: dict[str, float]) -> dict[str, object]:
    ordered_items = sorted(monthly_pnl.items())
    worst_months = [
        {"month": month, "pnl": round(pnl, 2)}
        for month, pnl in sorted(ordered_items, key=lambda item: item[1])[:5]
    ]
    best_months = [
        {"month": month, "pnl": round(pnl, 2)}
        for month, pnl in sorted(ordered_items, key=lambda item: item[1], reverse=True)[:5]
    ]

    by_month_of_year: dict[int, list[float]] = {}
    for month, pnl in ordered_items:
        month_number = int(month.split("-")[1])
        by_month_of_year.setdefault(month_number, []).append(pnl)

    month_of_year_summary = []
    for month_number in sorted(by_month_of_year):
        pnls = by_month_of_year[month_number]
        total = sum(pnls)
        average = total / len(pnls)
        month_of_year_summary.append(
            {
                "month": month_number,
                "count": len(pnls),
                "total_pnl": round(total, 2),
                "average_pnl": round(average, 2),
                "profitable_count": sum(1 for pnl in pnls if pnl > 0),
                "losing_count": sum(1 for pnl in pnls if pnl < 0),
            }
        )

    weak_month_numbers = [
        item
        for item in month_of_year_summary
        if item["average_pnl"] <= 0 or item["losing_count"] > item["profitable_count"]
    ]

    longest_losing_streak = 0
    current_losing_streak = 0
    for _, pnl in ordered_items:
        if pnl < 0:
            current_losing_streak += 1
            longest_losing_streak = max(longest_losing_streak, current_losing_streak)
        else:
            current_losing_streak = 0

    return {
        "months": len(ordered_items),
        "worst_months": worst_months,
        "best_months": best_months,
        "month_of_year_summary": month_of_year_summary,
        "weak_month_numbers": weak_month_numbers,
        "longest_losing_streak": longest_losing_streak,
    }


def analyze_strategy_breakdown(strategy_breakdown: dict[str, object], monthly_pnl: dict[str, float]) -> dict[str, object]:
    strategy_diagnostics: dict[str, object] = {}
    month_contributors: dict[str, list[dict[str, float | str]]] = {}
    for strategy_name, raw_stats in dict(strategy_breakdown).items():
        stats = dict(raw_stats)
        strategy_monthly_pnl = {
            month: float(pnl)
            for month, pnl in dict(stats.get("monthly_pnl", {})).items()
        }
        strategy_diagnostics[strategy_name] = {
            "profit": float(stats.get("profit", 0.0)),
            "trades": int(stats.get("trades", 0)),
            "wins": int(stats.get("wins", 0)),
            "losses": int(stats.get("losses", 0)),
            **analyze_monthly_pnl(strategy_monthly_pnl),
        }
        for month, pnl in strategy_monthly_pnl.items():
            month_contributors.setdefault(month, []).append(
                {
                    "strategy": strategy_name,
                    "pnl": round(pnl, 2),
                }
            )

    worst_month_contributors = []
    for month, pnl in sorted(monthly_pnl.items(), key=lambda item: item[1])[:5]:
        contributors = sorted(month_contributors.get(month, []), key=lambda item: float(item["pnl"]))
        worst_month_contributors.append(
            {
                "month": month,
                "portfolio_pnl": round(pnl, 2),
                "contributors": contributors,
            }
        )

    return {
        "strategy_diagnostics": strategy_diagnostics,
        "worst_month_contributors": worst_month_contributors,
    }


def analyze_portfolio_result(result: dict[str, object]) -> dict[str, object]:
    monthly_pnl = {
        month: float(pnl)
        for month, pnl in dict(result.get("monthly_pnl", {})).items()
    }
    diagnostics = analyze_monthly_pnl(monthly_pnl)
    reported_active_months = int(result.get("active_months", diagnostics["months"]))
    diagnostics["months_with_pnl_entries"] = diagnostics["months"]
    diagnostics["reported_active_months"] = reported_active_months
    diagnostics["zero_pnl_months"] = max(0, reported_active_months - diagnostics["months"])
    strategy_breakdown = dict(result.get("strategy_breakdown", {}))
    if strategy_breakdown:
        diagnostics.update(analyze_strategy_breakdown(strategy_breakdown, monthly_pnl))
    diagnostics["candidate_names"] = list(result.get("candidate_names", []))
    diagnostics["profit"] = float(result.get("profit", 0.0))
    diagnostics["max_drawdown"] = float(result.get("max_drawdown", 0.0))
    return diagnostics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    result = json.loads(Path(args.input).read_text(encoding="utf-8"))
    diagnostics = analyze_portfolio_result(result)
    rendered = json.dumps(diagnostics, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
