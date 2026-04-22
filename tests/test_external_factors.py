from pathlib import Path

from kanekasegi.external_factors import load_external_factors


def test_load_external_factors_reads_values(tmp_path: Path):
    csv_path = tmp_path / "factors.csv"
    csv_path.write_text(
        "trading_day,usd_jpy_change,us_index_change\n"
        "2026-01-05,0.42,-0.31\n"
        "2026-01-06,-0.27,0.55\n",
        encoding="utf-8",
    )

    factors = load_external_factors(csv_path)

    assert factors.get_value("2026-01-05", "usd_jpy_change") == 0.42
    assert factors.get_value("2026-01-06", "us_index_change") == 0.55
    assert factors.get_value("2026-01-07", "usd_jpy_change") is None


def test_external_factors_describe_lists_columns(tmp_path: Path):
    csv_path = tmp_path / "factors.csv"
    csv_path.write_text(
        "trading_day,usd_jpy_change,us_index_change\n"
        "2026-01-05,0.42,-0.31\n",
        encoding="utf-8",
    )

    factors = load_external_factors(csv_path)
    summary = factors.describe()

    assert summary["trading_days"] == 1
    assert summary["factor_names"] == ["us_index_change", "usd_jpy_change"]


def test_external_factors_support_session_specific_override(tmp_path: Path):
    csv_path = tmp_path / "factors.csv"
    csv_path.write_text(
        "trading_day,session,usd_jpy_change\n"
        "2026-01-05,both,0.10\n"
        "2026-01-05,night,-0.45\n",
        encoding="utf-8",
    )

    factors = load_external_factors(csv_path)

    assert factors.get_value("2026-01-05", "usd_jpy_change") == 0.10
    assert factors.get_value("2026-01-05", "usd_jpy_change", session="night") == -0.45
