from pathlib import Path

from kanekasegi.research_dashboard import build_dashboard_markdown, write_dashboard


def test_build_dashboard_markdown_collects_latest_leader(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    results_dir = tmp_path / "results"
    output_path = docs_dir / "CURRENT_RESEARCH_STATUS.md"
    docs_dir.mkdir()
    results_dir.mkdir()

    (docs_dir / "RESEARCH_SNAPSHOT_2026-04-11.md").write_text(
        "# Research Snapshot 2026-04-11\n\nCurrent strongest portfolio remains `leader_x`.\n",
        encoding="utf-8",
    )
    (results_dir / "portfolio-research-2026-04-11-leader_x.json").write_text(
        """{
  "candidate_names": ["rule_a", "rule_b"],
  "profit": 12345,
  "max_drawdown": 678,
  "win_rate": 0.55,
  "trades": 99,
  "profitable_months": 10,
  "losing_months": 1,
  "average_monthly_pnl": 123.4
}""",
        encoding="utf-8",
    )
    (results_dir / "validation-2026-04-11-leader_x-dd-gated.json").write_text(
        """{
  "summary": {
    "tested_windows": 4,
    "accepted_both_windows": 4,
    "total_test_profit": 1000,
    "average_test_win_rate": 0.6,
    "worst_test_drawdown": 200
  }
}""",
        encoding="utf-8",
    )
    (results_dir / "portfolio-diagnostics-2026-04-11-leader_x.json").write_text(
        """{
  "worst_months": [
    {"month": "2024-04", "pnl": 100},
    {"month": "2024-06", "pnl": 250}
  ]
}""",
        encoding="utf-8",
    )
    (results_dir / "portfolio-research-2026-04-11-order-summary.json").write_text(
        """{
  "decision": "keep leader_x",
  "baseline": {"name": "leader_x"},
  "best_new_candidate": {"name": "candidate_y", "profit": 11000, "max_drawdown": 500, "win_rate": 0.58}
}""",
        encoding="utf-8",
    )

    rendered = build_dashboard_markdown(docs_dir, results_dir, output_path)

    assert "leader_x" in rendered
    assert "12345" in rendered
    assert "candidate_y" in rendered
    assert "2024-04" in rendered
    assert "accepted_both_windows" in rendered


def test_write_dashboard_creates_output_file(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    results_dir = tmp_path / "results"
    output_path = docs_dir / "CURRENT_RESEARCH_STATUS.md"
    docs_dir.mkdir()
    results_dir.mkdir()

    (docs_dir / "RESEARCH_SNAPSHOT_2026-04-11.md").write_text(
        "Current strongest portfolio remains `leader_z`.\n",
        encoding="utf-8",
    )
    (results_dir / "portfolio-research-2026-04-11-leader_z.json").write_text(
        """{
  "candidate_names": [],
  "profit": 1,
  "max_drawdown": 2,
  "win_rate": 0.3,
  "trades": 4,
  "profitable_months": 5,
  "losing_months": 0,
  "average_monthly_pnl": 6
}""",
        encoding="utf-8",
    )

    write_dashboard(docs_dir, results_dir, output_path)

    assert output_path.exists()
    assert "leader_z" in output_path.read_text(encoding="utf-8")


def test_dashboard_prefers_exact_date_bundle_over_newer_partial_files(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    results_dir = tmp_path / "results"
    output_path = docs_dir / "CURRENT_RESEARCH_STATUS.md"
    docs_dir.mkdir()
    results_dir.mkdir()

    (docs_dir / "RESEARCH_SNAPSHOT_2026-04-12.md").write_text(
        "Current strongest portfolio remains `leader_bundle`.\n",
        encoding="utf-8",
    )
    (results_dir / "portfolio-research-2026-04-09-leader_bundle.json").write_text(
        """{"candidate_names": [], "profit": 100, "max_drawdown": 10, "win_rate": 0.5, "trades": 1, "profitable_months": 1, "losing_months": 0, "average_monthly_pnl": 3.4}""",
        encoding="utf-8",
    )
    (results_dir / "validation-2026-04-09-leader_bundle-dd-gated.json").write_text(
        """{"summary": {"tested_windows": 4, "accepted_both_windows": 4, "total_test_profit": 10, "average_test_win_rate": 0.6, "worst_test_drawdown": 2}}""",
        encoding="utf-8",
    )
    (results_dir / "portfolio-diagnostics-2026-04-09-leader_bundle.json").write_text(
        """{"worst_months": [{"month": "2024-04", "pnl": 1}]}""",
        encoding="utf-8",
    )
    (results_dir / "portfolio-research-2026-04-10-leader_bundle.json").write_text(
        """{"candidate_names": [], "profit": 999, "max_drawdown": 99, "win_rate": 0.9, "trades": 9, "profitable_months": 9, "losing_months": 0, "average_monthly_pnl": 9.9}""",
        encoding="utf-8",
    )

    rendered = build_dashboard_markdown(docs_dir, results_dir, output_path)
    leader_section = rendered.split("## Leader Candidate Set", 1)[0]

    assert "bundle_date: `2026-04-09`" in leader_section
    assert "portfolio-research-2026-04-09-leader_bundle.json" in leader_section
    assert "portfolio-research-2026-04-10-leader_bundle.json" not in leader_section
