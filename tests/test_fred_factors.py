from pathlib import Path

from kanekasegi.fred_factors import build_factor_rows, parse_fred_graph_csv, write_external_factors_csv


def test_parse_fred_graph_csv_skips_missing_values():
    payload = "DATE,DEXJPUS\n2026-01-01,0.0064\n2026-01-02,.\n2026-01-05,0.0065\n"

    observations = parse_fred_graph_csv(payload)

    assert len(observations) == 2
    assert observations[0].observed_on.isoformat() == "2026-01-01"
    assert observations[1].value == 0.0065


def test_build_factor_rows_assigns_to_next_business_day():
    observations = parse_fred_graph_csv(
        "DATE,DEXJPUS\n"
        "2026-01-01,0.0064\n"
        "2026-01-02,0.0065\n"
        "2026-01-05,0.0066\n"
    )

    rows = build_factor_rows(
        observations,
        factor_name="usd_jpy_change",
        assign_mode="next_business_day",
        value_mode="pct_change",
    )

    assert "2026-01-05" in rows
    assert "2026-01-06" in rows
    assert rows["2026-01-05"]["usd_jpy_change"] > 0


def test_write_external_factors_csv_merges_existing_columns(tmp_path: Path):
    output_path = tmp_path / "factors.csv"
    output_path.write_text(
        "trading_day,us_index_change\n"
        "2026-01-05,-0.31\n",
        encoding="utf-8",
    )

    write_external_factors_csv(
        output_path,
        {"2026-01-05": {"usd_jpy_change": 0.42}},
    )

    rendered = output_path.read_text(encoding="utf-8")
    assert "usd_jpy_change" in rendered
    assert "us_index_change" in rendered


def test_build_factor_rows_can_scale_diff_values():
    observations = parse_fred_graph_csv(
        "DATE,DGS10\n"
        "2026-01-01,4.20\n"
        "2026-01-02,4.25\n"
    )

    rows = build_factor_rows(
        observations,
        factor_name="us10y_change_bp",
        assign_mode="same_day",
        value_mode="diff",
        value_scale=100.0,
    )

    assert rows["2026-01-02"]["us10y_change_bp"] == 5.0
