from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .types import MarketCandle


def _normalize_trading_day(raw: str) -> str:
    raw = raw.strip()
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return raw


@dataclass(slots=True)
class ExternalFactors:
    by_day_session: dict[tuple[str, str], dict[str, float]] | None = None
    by_trading_day: dict[str, dict[str, float]] | None = None

    def __post_init__(self) -> None:
        normalized: dict[tuple[str, str], dict[str, float]] = {}
        for key, values in (self.by_day_session or {}).items():
            trading_day, session = key
            normalized[(_normalize_trading_day(trading_day), session)] = dict(values)
        for trading_day, values in (self.by_trading_day or {}).items():
            normalized[(_normalize_trading_day(trading_day), "both")] = dict(values)
        self.by_day_session = normalized
        self.by_trading_day = {
            trading_day: values
            for (trading_day, session), values in normalized.items()
            if session == "both"
        }

    @classmethod
    def from_csv(cls, path: str | Path) -> "ExternalFactors":
        csv_path = Path(path)
        rows: dict[tuple[str, str], dict[str, float]] = {}
        with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames or "trading_day" not in reader.fieldnames:
                raise ValueError("external factors csv must contain trading_day column")
            for raw_row in reader:
                if not raw_row:
                    continue
                raw_day = raw_row.get("trading_day")
                if not raw_day:
                    continue
                trading_day = _normalize_trading_day(raw_day)
                session = (raw_row.get("session") or "both").strip().lower()
                if session not in {"day", "night", "both"}:
                    raise ValueError("external factors csv session must be day, night, or both")
                values: dict[str, float] = {}
                for key, value in raw_row.items():
                    if key in {"trading_day", "session"} or value in {None, ""}:
                        continue
                    values[key] = float(value)
                rows[(trading_day, session)] = values
        return cls(by_day_session=rows)

    def values_for(self, candle: MarketCandle) -> dict[str, float]:
        trading_day = candle.trading_day or candle.timestamp.strftime("%Y-%m-%d")
        trading_day = _normalize_trading_day(trading_day)
        merged = dict(self.by_day_session.get((trading_day, "both"), {}))
        if candle.session:
            merged.update(self.by_day_session.get((trading_day, candle.session.value), {}))
        return merged

    def value_for(self, candle: MarketCandle, factor_name: str) -> float | None:
        return self.values_for(candle).get(factor_name)

    def get_value(self, trading_day: str, factor_name: str, session: str | None = None) -> float | None:
        trading_day = _normalize_trading_day(trading_day)
        merged = dict(self.by_day_session.get((trading_day, "both"), {}))
        if session:
            merged.update(self.by_day_session.get((trading_day, session), {}))
        return merged.get(factor_name)

    def describe(self) -> dict[str, object]:
        factor_names = sorted(
            {
                key
                for values in self.by_day_session.values()
                for key in values.keys()
            }
        )
        trading_days = {trading_day for trading_day, _ in self.by_day_session.keys()}
        return {
            "trading_days": len(trading_days),
            "rows": len(self.by_day_session),
            "factor_names": factor_names,
        }


ExternalFactorProvider = ExternalFactors


def load_external_factors(path: str | Path) -> ExternalFactors:
    return ExternalFactors.from_csv(path)
