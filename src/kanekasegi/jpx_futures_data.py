from __future__ import annotations

import csv
import io
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .types import MarketCandle, SessionType


def _parse_timeframe_minutes(timeframe: str) -> int:
    normalized = timeframe.strip().lower()
    if not normalized.endswith("m"):
        raise ValueError(f"unsupported timeframe: {timeframe}")
    minutes = int(normalized[:-1])
    if minutes <= 0:
        raise ValueError(f"unsupported timeframe: {timeframe}")
    return minutes


def _expand_zip_paths(zip_glob: str) -> list[Path]:
    raw_parts = [part.strip() for part in zip_glob.replace("\n", ";").split(";") if part.strip()]
    paths: list[Path] = []
    for part in raw_parts:
        candidate = Path(part)
        if any(token in part for token in "*?[]"):
            paths.extend(sorted(Path().glob(part)))
            continue
        if candidate.exists():
            paths.append(candidate)
            continue
        raise FileNotFoundError(part)
    unique_paths: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique_paths.append(resolved)
    if not unique_paths:
        raise FileNotFoundError(f"no JPX ZIP files matched: {zip_glob}")
    return unique_paths


def _parse_timestamp(execution_date: str, interval_time: str) -> datetime:
    return datetime.strptime(f"{execution_date}{interval_time.zfill(4)}", "%Y%m%d%H%M")


def _map_session(session_id: str) -> SessionType | None:
    if session_id == "999":
        return SessionType.DAY
    if session_id == "003":
        return SessionType.NIGHT
    return None


@dataclass(slots=True)
class _MinuteRow:
    timestamp: datetime
    trading_day: str
    contract_month: str
    session: SessionType | None
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True)
class JpxDatasetSummary:
    zip_files: int
    source_rows: int
    selected_rows: int
    candles: int
    trade_days: int
    first_timestamp: datetime
    last_timestamp: datetime
    session_counts: dict[str, int]
    contract_months: dict[str, int]
    selected_contract_days: dict[str, str]


@dataclass(slots=True)
class JpxFuturesZipDataProvider:
    symbol: str
    timeframe: str
    zip_glob: str
    session_filter: str = "both"
    contract_type: str = "current"
    specific_contract_month: str | None = None
    _candles: list[MarketCandle] = field(init=False, repr=False)
    _cursor: int = field(init=False, repr=False)
    _summary: JpxDatasetSummary = field(init=False, repr=False)

    def __post_init__(self) -> None:
        minute_rows, summary = self._load_rows()
        self._candles = self._resample(minute_rows)
        if not self._candles:
            raise ValueError("JPX futures ZIP data source is empty after filtering")
        self._cursor = len(self._candles)
        self._summary = JpxDatasetSummary(
            zip_files=summary["zip_files"],
            source_rows=summary["source_rows"],
            selected_rows=summary["selected_rows"],
            candles=len(self._candles),
            trade_days=summary["trade_days"],
            first_timestamp=self._candles[0].timestamp,
            last_timestamp=self._candles[-1].timestamp,
            session_counts=summary["session_counts"],
            contract_months=summary["contract_months"],
            selected_contract_days=summary["selected_contract_days"],
        )

    def _iter_csv_rows(self, paths: Iterable[Path]) -> Iterable[dict[str, str]]:
        for path in paths:
            with zipfile.ZipFile(path) as zf:
                for name in zf.namelist():
                    if not name.lower().endswith(".csv"):
                        continue
                    with zf.open(name) as fh:
                        wrapper = io.TextIOWrapper(fh, encoding="utf-8")
                        reader = csv.DictReader(wrapper)
                        for row in reader:
                            yield row

    def _load_rows(self) -> tuple[list[_MinuteRow], dict[str, object]]:
        paths = _expand_zip_paths(self.zip_glob)
        raw_rows: list[_MinuteRow] = []
        source_rows = 0
        session_counts = {"day": 0, "night": 0, "unknown": 0}
        volume_by_day_month: dict[str, dict[str, float]] = {}
        for row in self._iter_csv_rows(paths):
            source_rows += 1
            session = _map_session(row["session_id"])
            if self.session_filter == "day" and session != SessionType.DAY:
                continue
            if self.session_filter == "night" and session != SessionType.NIGHT:
                continue
            if session == SessionType.DAY:
                session_counts["day"] += 1
            elif session == SessionType.NIGHT:
                session_counts["night"] += 1
            else:
                session_counts["unknown"] += 1
            minute_row = _MinuteRow(
                timestamp=_parse_timestamp(row["execution_date"], row["interval_time"]),
                trading_day=row["trade_date"],
                contract_month=row["contract_month"],
                session=session,
                open=float(row["open_price"]),
                high=float(row["high_price"]),
                low=float(row["low_price"]),
                close=float(row["close_price"]),
                volume=float(row["trade_volume"]),
            )
            raw_rows.append(minute_row)
            day_map = volume_by_day_month.setdefault(minute_row.trading_day, {})
            day_map[minute_row.contract_month] = day_map.get(minute_row.contract_month, 0.0) + minute_row.volume

        selected_contract_days = self._select_contract_days(volume_by_day_month)
        selected_rows = [
            row
            for row in raw_rows
            if selected_contract_days.get(row.trading_day) == row.contract_month
        ]
        contract_months: dict[str, int] = {}
        for row in selected_rows:
            contract_months[row.contract_month] = contract_months.get(row.contract_month, 0) + 1
        selected_rows.sort(key=lambda item: item.timestamp)
        return selected_rows, {
            "zip_files": len(paths),
            "source_rows": source_rows,
            "selected_rows": len(selected_rows),
            "trade_days": len(selected_contract_days),
            "session_counts": session_counts,
            "contract_months": contract_months,
            "selected_contract_days": selected_contract_days,
        }

    def _select_contract_days(self, volume_by_day_month: dict[str, dict[str, float]]) -> dict[str, str]:
        selected: dict[str, str] = {}
        for trading_day, month_map in volume_by_day_month.items():
            months = sorted(month_map)
            if self.contract_type == "specific":
                selected_month = self.specific_contract_month
                if selected_month not in month_map:
                    continue
            elif self.contract_type == "next":
                selected_month = months[1] if len(months) > 1 else months[0]
            else:
                selected_month = months[0]
            selected[trading_day] = selected_month
        return selected

    def _resample(self, rows: list[_MinuteRow]) -> list[MarketCandle]:
        minutes = _parse_timeframe_minutes(self.timeframe)
        if minutes == 1:
            return [
                MarketCandle(
                    timestamp=row.timestamp,
                    open=row.open,
                    high=row.high,
                    low=row.low,
                    close=row.close,
                    volume=row.volume,
                    session=row.session,
                    contract_month=row.contract_month,
                    trading_day=row.trading_day,
                )
                for row in rows
            ]

        candles: list[MarketCandle] = []
        current_bucket: tuple[str, str, str | None, datetime] | None = None
        current_candle: MarketCandle | None = None
        for row in rows:
            bucket_minute = row.timestamp.minute - (row.timestamp.minute % minutes)
            bucket_timestamp = row.timestamp.replace(minute=bucket_minute, second=0, microsecond=0)
            bucket_key = (
                row.trading_day,
                row.contract_month,
                row.session.value if row.session else None,
                bucket_timestamp,
            )
            if current_bucket != bucket_key:
                if current_candle is not None:
                    candles.append(current_candle)
                current_bucket = bucket_key
                current_candle = MarketCandle(
                    timestamp=bucket_timestamp,
                    open=row.open,
                    high=row.high,
                    low=row.low,
                    close=row.close,
                    volume=row.volume,
                    session=row.session,
                    contract_month=row.contract_month,
                    trading_day=row.trading_day,
                )
                continue
            assert current_candle is not None
            current_candle.high = max(current_candle.high, row.high)
            current_candle.low = min(current_candle.low, row.low)
            current_candle.close = row.close
            current_candle.volume += row.volume
        if current_candle is not None:
            candles.append(current_candle)
        return candles

    def describe(self) -> dict[str, object]:
        return {
            "zip_files": self._summary.zip_files,
            "source_rows": self._summary.source_rows,
            "selected_rows": self._summary.selected_rows,
            "candles": self._summary.candles,
            "trade_days": self._summary.trade_days,
            "first_timestamp": self._summary.first_timestamp.isoformat(),
            "last_timestamp": self._summary.last_timestamp.isoformat(),
            "session_counts": self._summary.session_counts,
            "contract_months": self._summary.contract_months,
            "contract_switch_days": self._summary.selected_contract_days,
        }

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int) -> list[MarketCandle]:
        if symbol != self.symbol or timeframe != self.timeframe:
            raise ValueError("unsupported symbol or timeframe")
        return self._candles[max(0, self._cursor - limit) : self._cursor]

    def get_ticker(self, symbol: str) -> float:
        if symbol != self.symbol:
            raise ValueError("unsupported symbol")
        return self._candles[self._cursor - 1].close

    def reset_for_backtest(self, warmup: int) -> None:
        if warmup <= 0 or warmup > len(self._candles):
            raise ValueError("invalid warmup")
        self._cursor = warmup

    def has_next(self) -> bool:
        return self._cursor < len(self._candles)

    def advance(self) -> bool:
        if not self.has_next():
            return False
        self._cursor += 1
        return True

    def total_candles(self) -> int:
        return len(self._candles)
