from __future__ import annotations

import json
import os
import sqlite3
import tempfile
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path

from .types import BotStatus, MarginSnapshot, OrderResult, PositionState, SignalAction


class Storage:
    def __init__(self, sqlite_path: str, log_path: str, health_path: str | None = None, sqlite_journal_mode: str = "MEMORY") -> None:
        self.sqlite_path = Path(sqlite_path)
        self.log_path = Path(log_path)
        self.health_path = Path(health_path) if health_path else self.log_path.parent / "health.json"
        self.sqlite_journal_mode = sqlite_journal_mode
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.health_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._init_db()
        except sqlite3.OperationalError:
            self.sqlite_path = self._fallback_sqlite_path(self.sqlite_path.name)
            self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            self._init_db()

    def _fallback_sqlite_path(self, filename: str) -> Path:
        base = Path(tempfile.gettempdir()) / "kanekasegi"
        return base / filename

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute(f"PRAGMA journal_mode={self.sqlite_journal_mode}")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    filled_price REAL NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS fills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    price REAL NOT NULL,
                    timestamp TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS positions (
                    symbol TEXT PRIMARY KEY,
                    side TEXT,
                    strategy_id TEXT,
                    quantity REAL NOT NULL,
                    position_id TEXT,
                    entry_price REAL NOT NULL,
                    stop_price REAL,
                    trailing_stop REAL,
                    unrealized_pnl REAL NOT NULL,
                    opened_at TEXT
                );
                CREATE TABLE IF NOT EXISTS bot_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS daily_pnl (
                    trading_day TEXT PRIMARY KEY,
                    realized_pnl REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS margin_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    trading_day TEXT NOT NULL,
                    available_cash REAL NOT NULL,
                    margin_requirement REAL NOT NULL,
                    maintenance_margin REAL NOT NULL,
                    excess_margin REAL NOT NULL
                );
                """
            )
            columns = {row[1] for row in conn.execute("PRAGMA table_info(positions)").fetchall()}
            if "position_id" not in columns:
                conn.execute("ALTER TABLE positions ADD COLUMN position_id TEXT")
            if "strategy_id" not in columns:
                conn.execute("ALTER TABLE positions ADD COLUMN strategy_id TEXT")

    def _json_default(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        if hasattr(value, "value"):
            return value.value
        raise TypeError(f"unsupported value: {value!r}")

    def _normalize_trading_day_key(self, trading_day: date | str | None = None) -> str:
        if trading_day is None:
            return date.today().isoformat()
        if isinstance(trading_day, date):
            return trading_day.isoformat()
        text = trading_day.strip()
        if len(text) == 10 and text.count("-") == 2:
            return text
        if len(text) == 8 and text.isdigit():
            return datetime.strptime(text, "%Y%m%d").date().isoformat()
        raise ValueError(f"unsupported trading_day format: {trading_day}")

    def append_log(self, event_type: str, payload: dict) -> None:
        record = {
            "event_type": event_type,
            "payload": payload,
            "created_at": datetime.utcnow().isoformat(),
        }
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=True, default=self._json_default) + "\n")
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO bot_events (event_type, payload, created_at) VALUES (?, ?, ?)",
                (event_type, json.dumps(payload, default=self._json_default), record["created_at"]),
            )

    def save_order(self, order: OrderResult) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO orders (order_id, symbol, side, quantity, filled_price, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order.order_id,
                    order.symbol,
                    order.side.value,
                    order.quantity,
                    order.filled_price,
                    order.status,
                    order.timestamp.isoformat(),
                ),
            )
            conn.execute(
                "INSERT INTO fills (order_id, symbol, quantity, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                (order.order_id, order.symbol, order.quantity, order.filled_price, order.timestamp.isoformat()),
            )

    def save_position(self, position: PositionState) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO positions
                (symbol, side, strategy_id, quantity, position_id, entry_price, stop_price, trailing_stop, unrealized_pnl, opened_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    position.symbol,
                    position.side.value if isinstance(position.side, SignalAction) else position.side,
                    position.strategy_id,
                    position.quantity,
                    position.position_id,
                    position.entry_price,
                    position.stop_price,
                    position.trailing_stop,
                    position.unrealized_pnl,
                    position.opened_at.isoformat() if position.opened_at else None,
                ),
            )

    def load_position(self, symbol: str) -> PositionState:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT symbol, side, strategy_id, quantity, position_id, entry_price, stop_price, trailing_stop, unrealized_pnl, opened_at FROM positions WHERE symbol = ?",
                (symbol,),
            ).fetchone()
        if row is None:
            return PositionState(symbol=symbol)
        side = SignalAction(row[1]) if row[1] else None
        opened_at = datetime.fromisoformat(row[9]) if row[9] else None
        return PositionState(
            symbol=row[0],
            side=side,
            strategy_id=row[2],
            quantity=row[3],
            position_id=row[4],
            entry_price=row[5],
            stop_price=row[6],
            trailing_stop=row[7],
            unrealized_pnl=row[8],
            opened_at=opened_at,
        )

    def save_daily_pnl(self, realized_pnl: float, trading_day: date | str | None = None) -> None:
        key = self._normalize_trading_day_key(trading_day)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO daily_pnl (trading_day, realized_pnl) VALUES (?, ?)",
                (key, realized_pnl),
            )

    def save_margin_snapshot(self, snapshot: MarginSnapshot) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO margin_snapshots
                (timestamp, trading_day, available_cash, margin_requirement, maintenance_margin, excess_margin)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot.timestamp.isoformat(),
                    snapshot.trading_day,
                    snapshot.available_cash,
                    snapshot.margin_requirement,
                    snapshot.maintenance_margin,
                    snapshot.excess_margin,
                ),
            )

    def load_daily_pnl(self, trading_day: date | str | None = None) -> float:
        key = self._normalize_trading_day_key(trading_day)
        with self._connect() as conn:
            row = conn.execute("SELECT realized_pnl FROM daily_pnl WHERE trading_day = ?", (key,)).fetchone()
        return float(row[0]) if row else 0.0

    def load_total_realized_pnl(self) -> float:
        with self._connect() as conn:
            row = conn.execute("SELECT COALESCE(SUM(realized_pnl), 0) FROM daily_pnl").fetchone()
        return float(row[0]) if row else 0.0

    def save_status(self, status: BotStatus) -> None:
        self.append_log("status", asdict(status))
        payload = asdict(status)
        payload["mode"] = status.mode.value
        payload["last_heartbeat"] = status.last_heartbeat.isoformat() if status.last_heartbeat else None
        self.health_path.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")

    def read_health(self) -> dict:
        if not self.health_path.exists():
            return {}
        return json.loads(self.health_path.read_text(encoding="utf-8"))
