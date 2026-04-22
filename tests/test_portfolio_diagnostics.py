from kanekasegi.portfolio_diagnostics import analyze_monthly_pnl, analyze_portfolio_result


def test_analyze_monthly_pnl_highlights_weak_month_numbers():
    monthly_pnl = {
        "2024-01": -1000.0,
        "2024-02": 2000.0,
        "2025-01": -500.0,
        "2025-02": 1500.0,
        "2025-10": -3000.0,
    }

    diagnostics = analyze_monthly_pnl(monthly_pnl)

    assert diagnostics["months"] == 5
    assert diagnostics["worst_months"][0]["month"] == "2025-10"
    weak_numbers = {item["month"] for item in diagnostics["weak_month_numbers"]}
    assert 1 in weak_numbers
    assert 10 in weak_numbers


def test_analyze_portfolio_result_keeps_header_fields():
    diagnostics = analyze_portfolio_result(
        {
            "candidate_names": ["a", "b"],
            "profit": 12345.0,
            "max_drawdown": 678.0,
            "active_months": 4,
            "monthly_pnl": {
                "2024-01": 100.0,
                "2024-02": -50.0,
            },
            "strategy_breakdown": {
                "a": {
                    "profit": 100.0,
                    "trades": 2,
                    "wins": 1,
                    "losses": 1,
                    "monthly_pnl": {
                        "2024-01": 120.0,
                        "2024-02": -20.0,
                    },
                },
                "b": {
                    "profit": 0.0,
                    "trades": 1,
                    "wins": 0,
                    "losses": 1,
                    "monthly_pnl": {
                        "2024-02": -30.0,
                    },
                },
            },
        }
    )

    assert diagnostics["candidate_names"] == ["a", "b"]
    assert diagnostics["profit"] == 12345.0
    assert diagnostics["max_drawdown"] == 678.0
    assert diagnostics["months_with_pnl_entries"] == 2
    assert diagnostics["reported_active_months"] == 4
    assert diagnostics["zero_pnl_months"] == 2
    assert diagnostics["longest_losing_streak"] == 1
    assert diagnostics["strategy_diagnostics"]["a"]["profit"] == 100.0
    assert diagnostics["worst_month_contributors"][0]["month"] == "2024-02"
    assert diagnostics["worst_month_contributors"][0]["contributors"][0]["strategy"] == "b"
