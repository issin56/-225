from __future__ import annotations

import csv
import io
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from glob import glob
from pathlib import Path

from .types import MarketCandle, SessionType


def _parse_trade_timestamp(execution_date: str, interval_time: str) -> datetime:
    return datetime.strptime(f"{execution_date}{interval_time.zfill(4)}", "%Y%m%d%H%M")


def _normalize_trading_day(trade_date: str) -> str:
    return datetime.strptime(trade_date, "%Y%m%d").date().isoformat()


def _parse_session(session_id: str) -> SessionType | None:
    mapping = {
        "003": SessionType.NIGHT,
        "999": SessionType.DAY,
    }
    return mapping.get(session_id)


def _timeframe_to_minutes(timeframe: str) -> int:
    normalized = timeframe.strip().lower()
    if not normalized.endswith("m"):
        raise ValueError(f"unsupported timeframe: {timeframe}")
    minutes = int(normalized[:-1])
    if minutes <= 0:
        raise ValueError("timeframe minutes must be positive")
    return minutes


def _bucket_start(timestamp: datetime, minutes: int) -> datetime:
    minute = (timestamp.minute // minutes) * minutes
    return timestamp.replace(minute=minute, second=0, microsecond=0)


@dataclass(slots=True)
class _RawMinuteCandle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    session: SessionType | None
    contract_month: str
    trading_day: str


@dataclass(slots=True)
class JpxMinuteZipMarketDataProvider:
    symbol: str
    timeframe: str
    zip_glob: str
    session_filter: str = "both"
    contract_type: str = "current"
    specific_contract_month: str | None = None
    _candles: list[MarketCandle] = field(init=False, repr=False)
    _cursor: int = field(init=False, repr=False)
    _summary: dict[str, object] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        minute_candles = self._load_minute_candles()
        if not minute_candles:
            raise ValueError("zip data source is empty after filtering")
        if self.timeframe == "1m":
            self._candles = [
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
                for row in minute_candles
            ]
        else:
            self._candles = self._resample(minute_candles, self.timeframe)
        self._cursor = len(self._candles)

    def _resolve_zip_paths(self) -> list[Path]:
        paths = sorted(Path(path) for path in glob(self.zip_glob))
        if not paths:
            raise FileNotFoundError(self.zip_glob)
        return paths

    def _load_minute_candles(self) -> list[_RawMinuteCandle]:
        paths = self._resolve_zip_paths()
        rows_by_day_contract: dict[tuple[str, str], list[_RawMinuteCandle]] = {}
        volume_by_day_contract: dict[tuple[str, str], float] = {}
        source_rows = 0
        session_counts = {"day": 0, "night": 0, "unknown": 0}
        for path in paths:
            with zipfile.ZipFile(path) as archive:
                for entry_name in archive.namelist():
                    if not entry_name.lower().endswith(".csv"):
                        continue
                    with archive.open(entry_name) as entry:
                        reader = csv.DictReader(io.TextIOWrapper(entry, encoding="utf-8"))
                        for record in reader:
                            source_rows += 1
                            raw = self._parse_record(record)
                            if raw is None:
                                continue
                            if raw.session == SessionType.DAY:
                                session_counts["day"] += 1
                            elif raw.session == SessionType.NIGHT:
                                session_counts["night"] += 1
                            else:
                                session_counts["unknown"] += 1
                            key = (raw.trading_day, raw.contract_month)
                            rows_by_day_contract.setdefault(key, []).append(raw)
                            volume_by_day_contract[key] = volume_by_day_contract.get(key, 0.0) + raw.volume

        selected_contracts = self._select_contracts(volume_by_day_contract)
        candles: list[_RawMinuteCandle] = []
        for key in sorted(rows_by_day_contract):
            if selected_contracts.get(key[0]) != key[1]:
                continue
            candles.extend(sorted(rows_by_day_contract[key], key=lambda row: row.timestamp))
        contract_months: dict[str, int] = {}
        for candle in candles:
            contract_months[candle.contract_month] = contract_months.get(candle.contract_month, 0) + 1
        self._summary = {
            "zip_files": len(paths),
            "source_rows": source_rows,
            "selected_rows": len(candles),
            "trade_days": len(selected_contracts),
            "session_counts": session_counts,
            "contract_months": contract_months,
            "selected_contract_days": selected_contracts,
        }
        return candles

    def _parse_record(self, record: dict[str, str]) -> _RawMinuteCandle | None:
        session = _parse_session(record["session_id"])
        if self.session_filter == "day" and session != SessionType.DAY:
            return None
        if self.session_filter == "night" and session != SessionType.NIGHT:
            return None
        return _RawMinuteCandle(
            timestamp=_parse_trade_timestamp(record["execution_date"], record["interval_time"]),
            open=float(record["open_price"]),
            high=float(record["high_price"]),
            low=float(record["low_price"]),
            close=float(record["close_price"]),
            volume=float(record["trade_volume"]),
            session=session,
            contract_month=record["contract_month"],
            trading_day=_normalize_trading_day(record["trade_date"]),
        )

    def _select_contracts(self, volume_by_day_contract: dict[tuple[str, str], float]) -> dict[str, str]:
        by_day: dict[str, list[tuple[str, float]]] = {}
        for (trading_day, contract_month), volume in volume_by_day_contract.items():
            by_day.setdefault(trading_day, []).append((contract_month, volume))

        selected: dict[str, str] = {}
        for trading_day, contracts in by_day.items():
            ranked = sorted(contracts, key=lambda item: (-item[1], item[0]))
            if self.contract_type == "current":
                selected[trading_day] = ranked[0][0]
            elif self.contract_type == "next":
                selected[trading_day] = ranked[1][0] if len(ranked) > 1 else ranked[0][0]
            elif self.contract_type == "specific":
                if self.specific_contract_month is None:
                    raise ValueError("runtime.specific_contract_month is required when contract_type is 'specific'")
                for contract_month, _ in ranked:
                    if contract_month == self.specific_contract_month:
                        selected[trading_day] = contract_month
                        break
                else:
                    raise ValueError(
                        f"specific contract month {self.specific_contract_month} not found for trading day {trading_day}"
                    )
            else:
                raise ValueError(f"unsupported contract_type: {self.contract_type}")
        return selected

    def _resample(self, candles: list[_RawMinuteCandle], timeframe: str) -> list[MarketCandle]:
        minutes = _timeframe_to_minutes(timeframe)
        if minutes == 1:
            raise ValueError("1m should not be resampled")
        aggregated: list[MarketCandle] = []
        bucket: list[_RawMinuteCandle] = []
        bucket_key: tuple[str, str, SessionType | None, datetime] | None = None

        for candle in candles:
            current_key = (
                candle.trading_day,
                candle.contract_month,
                candle.session,
                _bucket_start(candle.timestamp, minutes),
            )
            if bucket and current_key != bucket_key:
                aggregated.append(self._aggregate_bucket(bucket, bucket_key[3]))
                bucket = []
            bucket_key = current_key
            bucket.append(candle)

        if bucket and bucket_key is not None:
            aggregated.append(self._aggregate_bucket(bucket, bucket_key[3]))
        return aggregated

    def _aggregate_bucket(self, bucket: list[_RawMinuteCandle], bucket_timestamp: datetime) -> MarketCandle:
        first = bucket[0]
        last = bucket[-1]
        return MarketCandle(
            timestamp=bucket_timestamp,
            open=first.open,
            high=max(item.high for item in bucket),
            low=min(item.low for item in bucket),
            close=last.close,
            volume=sum(item.volume for item in bucket),
            session=first.session,
            contract_month=first.contract_month,
            trading_day=first.trading_day,
        )

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

    def all_candles(self, symbol: str, timeframe: str) -> list[MarketCandle]:
        if symbol != self.symbol or timeframe != self.timeframe:
            raise ValueError("unsupported symbol or timeframe")
        return list(self._candles)

    def describe(self) -> dict[str, object]:
        trading_days = sorted(self._summary["selected_contract_days"])
        calendar_months = sorted({trading_day[:7] for trading_day in trading_days})
        return {
            "zip_files": self._summary["zip_files"],
            "source_rows": self._summary["source_rows"],
            "selected_rows": self._summary["selected_rows"],
            "candles": len(self._candles),
            "trade_days": self._summary["trade_days"],
            "calendar_months": calendar_months,
            "calendar_month_count": len(calendar_months),
            "first_timestamp": self._candles[0].timestamp.isoformat(),
            "last_timestamp": self._candles[-1].timestamp.isoformat(),
            "session_counts": self._summary["session_counts"],
            "contract_months": self._summary["contract_months"],
            "selected_contract_days": self._summary["selected_contract_days"],
        }
