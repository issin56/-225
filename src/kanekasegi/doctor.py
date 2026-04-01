from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .gmo_adapter import GmoCoinAdapter
from .sbi_adapter import SbiFuturesAdapter


def run_doctor(bot) -> dict[str, Any]:
    config = bot.config
    report: dict[str, Any] = {
        "mode": config.mode.value,
        "symbol": config.runtime.symbol,
        "timeframe": config.runtime.timeframe,
        "broker": config.runtime.broker,
        "live_order_enabled": config.runtime.live_order_enabled,
        "checks": [],
    }

    checks = report["checks"]
    checks.append(_check("config_load", True, "config loaded"))
    checks.append(_check("storage_log_dir", bot.storage.log_path.parent.exists(), str(bot.storage.log_path.parent)))
    checks.append(_check("storage_db_parent", bot.storage.sqlite_path.parent.exists(), str(bot.storage.sqlite_path.parent)))
    checks.append(_check("health_path_parent", bot.storage.health_path.parent.exists(), str(bot.storage.health_path.parent)))

    if config.runtime.data_source == "csv":
        csv_path = Path(config.runtime.csv_path or "")
        checks.append(_check("csv_path_exists", csv_path.exists(), str(csv_path)))
    else:
        checks.append(_check("synthetic_data_source", True, "using synthetic candles"))

    if config.mode.value == "live" and config.runtime.broker == "gmo":
        api_key = os.getenv("GMO_API_KEY") or os.getenv("EXCHANGE_API_KEY")
        api_secret = os.getenv("GMO_API_SECRET") or os.getenv("EXCHANGE_API_SECRET")
        checks.append(_check("gmo_api_key_present", bool(api_key), "GMO_API_KEY or EXCHANGE_API_KEY"))
        checks.append(_check("gmo_api_secret_present", bool(api_secret), "GMO_API_SECRET or EXCHANGE_API_SECRET"))
        if isinstance(bot.exchange, GmoCoinAdapter):
            try:
                connectivity = bot.exchange.connectivity_check(config.runtime.symbol)
                checks.append(_check("broker_connectivity", True, "broker reachable"))
                report["broker_snapshot"] = connectivity
            except Exception as exc:
                checks.append(_check("broker_connectivity", False, str(exc)))
        else:
            checks.append(_check("broker_connectivity", False, "live broker adapter not initialized"))
    elif config.mode.value == "live" and config.runtime.broker == "sbi":
        api_key = os.getenv("SBI_API_KEY") or os.getenv("EXCHANGE_API_KEY")
        api_secret = os.getenv("SBI_API_SECRET") or os.getenv("EXCHANGE_API_SECRET")
        endpoint = os.getenv("SBI_API_ENDPOINT")
        checks.append(_check("sbi_api_key_present", bool(api_key), "SBI_API_KEY or EXCHANGE_API_KEY"))
        checks.append(_check("sbi_api_secret_present", bool(api_secret), "SBI_API_SECRET or EXCHANGE_API_SECRET"))
        checks.append(_check("sbi_api_endpoint_present", bool(endpoint), "SBI_API_ENDPOINT"))
        if isinstance(bot.exchange, SbiFuturesAdapter):
            report["broker_snapshot"] = bot.exchange.connectivity_check(config.runtime.symbol)
            checks.append(_check("broker_connectivity", True, "SBI adapter profile loaded"))
        else:
            checks.append(_check("broker_connectivity", False, "sbi adapter not initialized"))
    else:
        checks.append(_check("live_credentials", True, "not required for current mode"))

    report["ok"] = all(item["ok"] for item in checks)
    return report


def _check(name: str, ok: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "ok": ok, "detail": detail}
