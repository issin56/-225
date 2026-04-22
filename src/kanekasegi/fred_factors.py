from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import date, timedelta
from io import StringIO
from pathlib import Path

import requests

from .external_factors import ExternalFactors, load_external_factors


FRED_GRAPH_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
REQUEST_HEADERS = {"User-Agent": "kanekasegi-bot/0.1 (+research factor builder)"}


@dataclass(slots=True)
class FredObservation:
    observed_on: date
    value: float


def parse_fred_graph_csv(payload: str) -> list[FredObservation]:
    reader = csv.DictReader(StringIO(payload))
    if not reader.fieldnames:
        raise ValueError("FRED CSV must include a date column")

    date_column = "DATE"
    if "DATE" not in reader.fieldnames:
        if "observation_date" in reader.fieldnames:
            date_column = "observation_date"
        else:
            raise ValueError("FRED CSV must include DATE or observation_date column")

    value_columns = [field for field in reader.fieldnames if field != date_column]
    if not value_columns:
        raise ValueError("FRED CSV must include a value column")

    value_column = value_columns[0]
    observations: list[FredObservation] = []
    for row in reader:
        raw_date = (row.get(date_column) or "").strip()
        raw_value = (row.get(value_column) or "").strip()
        if not raw_date or not raw_value or raw_value == ".":
            continue
        observations.append(
            FredObservation(
                observed_on=date.fromisoformat(raw_date),
                value=float(raw_value),
            )
        )
    return observations


def fetch_fred_series(
    series_id: str,
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    timeout_seconds: int = 60,
) -> list[FredObservation]:
    params = {"id": series_id}
    if start_date:
        params["cosd"] = start_date
    if end_date:
        params["coed"] = end_date
    response = requests.get(
        FRED_GRAPH_CSV_URL,
        params=params,
        timeout=timeout_seconds,
        headers=REQUEST_HEADERS,
    )
    response.raise_for_status()
    return parse_fred_graph_csv(response.text)


def _next_business_day(current: date) -> date:
    next_day = current + timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    return next_day


def build_factor_rows(
    observations: list[FredObservation],
    *,
    factor_name: str,
    assign_mode: str = "next_business_day",
    value_mode: str = "pct_change",
    value_scale: float = 1.0,
) -> dict[str, dict[str, float]]:
    if assign_mode not in {"same_day", "next_business_day"}:
        raise ValueError("assign_mode must be 'same_day' or 'next_business_day'")
    if value_mode not in {"pct_change", "diff"}:
        raise ValueError("value_mode must be 'pct_change' or 'diff'")

    rows: dict[str, dict[str, float]] = {}
    previous: FredObservation | None = None
    for observation in observations:
        if previous is None:
            previous = observation
            continue

        if value_mode == "pct_change":
            if previous.value == 0:
                previous = observation
                continue
            factor_value = ((observation.value - previous.value) / previous.value) * 100.0
        else:
            factor_value = observation.value - previous.value
        factor_value *= value_scale

        trading_day = observation.observed_on if assign_mode == "same_day" else _next_business_day(observation.observed_on)
        rows.setdefault(trading_day.isoformat(), {})[factor_name] = round(factor_value, 6)
        previous = observation
    return rows


def write_external_factors_csv(path: str | Path, factor_rows: dict[str, dict[str, float]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    merged: dict[str, dict[str, float]] = {}
    if output_path.exists():
        existing = load_external_factors(output_path)
        merged = {trading_day: dict(values) for trading_day, values in existing.by_trading_day.items()}
    for trading_day, values in factor_rows.items():
        merged.setdefault(trading_day, {}).update(values)

    factor_names = sorted({name for values in merged.values() for name in values})
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["trading_day", *factor_names])
        for trading_day in sorted(merged):
            row = [trading_day]
            for factor_name in factor_names:
                value = merged[trading_day].get(factor_name)
                row.append("" if value is None else value)
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series-id", default="DEXJPUS")
    parser.add_argument("--factor-name", default="usd_jpy_change")
    parser.add_argument("--output", default="data/external_factors.usdjpy.csv")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--assign-mode", default="next_business_day")
    parser.add_argument("--value-mode", default="pct_change")
    parser.add_argument("--value-scale", type=float, default=1.0)
    args = parser.parse_args()

    observations = fetch_fred_series(
        args.series_id,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    factor_rows = build_factor_rows(
        observations,
        factor_name=args.factor_name,
        assign_mode=args.assign_mode,
        value_mode=args.value_mode,
        value_scale=args.value_scale,
    )
    write_external_factors_csv(args.output, factor_rows)
    summary = ExternalFactors(by_trading_day=factor_rows).describe()
    summary["series_id"] = args.series_id
    summary["factor_name"] = args.factor_name
    summary["output"] = str(Path(args.output))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
