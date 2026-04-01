from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict

from .bot import TradingBot
from .backtest import run_backtest
from .config import AppConfig, load_config
from .csv_data import CsvMarketDataProvider
from .doctor import run_doctor
from .execution import ExecutionEngine
from .exchange_adapter import LiveExchangeAdapter, PaperExchangeAdapter
from .gmo_adapter import GmoCoinAdapter
from .jpx_data import JpxMinuteZipMarketDataProvider
from .market_data import InMemoryMarketDataProvider
from .notifier import DiscordNotifier
from .risk import RiskEngine
from .rule_lab import generate_default_candidates, run_rule_lab
from .runtime_env import load_dotenv
from .sbi_adapter import SbiApiProfile, SbiFuturesAdapter
from .storage import Storage
from .strategy import BreakoutTrendStrategy
from .types import BotStatus


def build_bot(config_path: str, *, config: AppConfig | None = None, skip_live_credentials: bool = False) -> tuple[TradingBot, object]:
    config = config or load_config(config_path)
    storage = Storage(
        config.storage.sqlite_path,
        config.storage.log_path,
        config.storage.health_path,
        config.storage.sqlite_journal_mode,
    )
    notifier = DiscordNotifier(os.getenv("DISCORD_WEBHOOK_URL"))
    strategy = BreakoutTrendStrategy(config.strategy)
    risk_engine = RiskEngine(config.risk)
    if config.runtime.data_source == "csv":
        if not config.runtime.csv_path:
            raise ValueError("runtime.csv_path is required when runtime.data_source=csv")
        market_data = CsvMarketDataProvider(
            symbol=config.runtime.symbol,
            timeframe=config.runtime.timeframe,
            csv_path=config.runtime.csv_path,
        )
    elif config.runtime.data_source == "jpx_zip":
        if not config.runtime.zip_glob:
            raise ValueError("runtime.zip_glob is required when runtime.data_source=jpx_zip")
        market_data = JpxMinuteZipMarketDataProvider(
            symbol=config.runtime.symbol,
            timeframe=config.runtime.timeframe,
            zip_glob=config.runtime.zip_glob,
            session_filter=config.runtime.session_filter,
            contract_type=config.runtime.contract_type,
            specific_contract_month=config.runtime.specific_contract_month,
        )
    else:
        market_data = InMemoryMarketDataProvider(symbol=config.runtime.symbol, timeframe=config.runtime.timeframe)

    if config.mode.value == "live":
        if config.runtime.broker == "gmo":
            api_key = os.getenv("GMO_API_KEY") or os.getenv("EXCHANGE_API_KEY")
            api_secret = os.getenv("GMO_API_SECRET") or os.getenv("EXCHANGE_API_SECRET")
            if skip_live_credentials:
                exchange = LiveExchangeAdapter()
            elif not api_key or not api_secret:
                raise ValueError("GMO_API_KEY and GMO_API_SECRET are required for live mode")
            else:
                exchange = GmoCoinAdapter(api_key=api_key, api_secret=api_secret)
        elif config.runtime.broker == "sbi":
            api_key = os.getenv("SBI_API_KEY") or os.getenv("EXCHANGE_API_KEY")
            api_secret = os.getenv("SBI_API_SECRET") or os.getenv("EXCHANGE_API_SECRET")
            endpoint = os.getenv("SBI_API_ENDPOINT")
            tool_name = os.getenv("SBI_API_TOOL_NAME")
            if skip_live_credentials:
                exchange = SbiFuturesAdapter(
                    SbiApiProfile(None, None, endpoint, tool_name),
                    market_data_provider=market_data,
                    initial_balance=config.paper.initial_balance,
                )
            elif not api_key or not api_secret:
                if config.runtime.live_order_enabled:
                    raise ValueError("SBI_API_KEY and SBI_API_SECRET are required for live mode when live_order_enabled=true")
                exchange = SbiFuturesAdapter(
                    SbiApiProfile(api_key, api_secret, endpoint, tool_name),
                    market_data_provider=market_data,
                    initial_balance=config.paper.initial_balance,
                )
            else:
                exchange = SbiFuturesAdapter(
                    SbiApiProfile(api_key, api_secret, endpoint, tool_name),
                    market_data_provider=market_data,
                    initial_balance=config.paper.initial_balance,
                )
        else:
            exchange = LiveExchangeAdapter()
    else:
        exchange = PaperExchangeAdapter(
            market_data_provider=market_data,
            initial_balance=config.paper.initial_balance,
            fee_rate=config.paper.fee_rate,
            slippage_bps=config.paper.slippage_bps,
        )
        exchange.position = storage.load_position(config.runtime.symbol)

    execution_engine = ExecutionEngine(exchange=exchange, storage=storage)
    status = BotStatus(mode=config.mode)
    bot = TradingBot(
        config=config,
        exchange=exchange,
        strategy=strategy,
        risk_engine=risk_engine,
        execution_engine=execution_engine,
        storage=storage,
        notifier=notifier,
        status=status,
    )
    return bot, market_data


def run_startup_checks(bot: TradingBot) -> None:
    if bot.config.mode.value != "live":
        return
    if isinstance(bot.exchange, GmoCoinAdapter):
        summary = bot.exchange.connectivity_check(bot.config.runtime.symbol)
        bot.storage.append_log("startup_check", summary)
        bot.notifier.send_info(
            f"startup check: broker=gmo symbol={bot.config.runtime.symbol} balance={summary['balance']}"
        )
    if isinstance(bot.exchange, SbiFuturesAdapter):
        summary = bot.exchange.connectivity_check(bot.config.runtime.symbol)
        bot.storage.append_log("startup_check", summary)
        bot.notifier.send_info(
            f"startup check: broker=sbi symbol={bot.config.runtime.symbol} api_key_present={summary['api_key_present']}"
        )


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--validate-config", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--check-broker", action="store_true")
    parser.add_argument("--enable-live-orders", action="store_true")
    parser.add_argument("--doctor", action="store_true")
    parser.add_argument("--research-summary", action="store_true")
    parser.add_argument("--research-grid", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.validate_config:
        print(f"config valid: mode={config.mode.value} symbol={config.runtime.symbol} data_source={config.runtime.data_source}")
        return

    bot, market_data = build_bot(
        args.config,
        config=config,
        skip_live_credentials=args.status or args.doctor,
    )
    if args.enable_live_orders:
        if bot.config.mode.value != "live":
            raise ValueError("--enable-live-orders can only be used with mode=live")
        bot.config.runtime.live_order_enabled = True
    if args.status:
        print(json.dumps(bot.storage.read_health(), ensure_ascii=False, indent=2))
        return
    if args.doctor:
        print(json.dumps(run_doctor(bot), ensure_ascii=False, indent=2))
        return
    if args.research_summary:
        if not hasattr(market_data, "describe"):
            raise ValueError("--research-summary requires a market data provider with describe() support")
        print(json.dumps(market_data.describe(), ensure_ascii=False, indent=2))
        return
    if args.check_broker:
        if not hasattr(bot.exchange, "connectivity_check"):
            raise ValueError("--check-broker requires a broker adapter with connectivity_check support")
        print(json.dumps(bot.exchange.connectivity_check(bot.config.runtime.symbol), ensure_ascii=False, indent=2))
        return
    if args.research_grid:
        if config.mode.value != "backtest":
            raise ValueError("--research-grid requires mode=backtest")
        print(json.dumps(run_research_grid(args.config, config), ensure_ascii=False, indent=2))
        return
    if bot.config.mode.value == "backtest":
        summary = run_backtest(bot, market_data, bot.config.runtime.candle_limit)
        print(
            f"backtest completed cycles={summary.cycles} "
            f"ending_equity={summary.ending_equity:.2f} daily_pnl={summary.daily_pnl:.2f} "
            f"trades={summary.trades} wins={summary.wins} losses={summary.losses} "
            f"win_rate={summary.win_rate:.2%} profit={summary.profit:.2f} "
            f"max_drawdown={summary.max_drawdown:.2f} min_equity={summary.min_equity:.2f} "
            f"min_available={summary.min_available_balance:.2f}"
        )
        return
    if args.once:
        run_startup_checks(bot)
        bot.run_cycle()
        return

    run_startup_checks(bot)
    while not bot.status.halted:
        try:
            bot.run_cycle()
        except Exception as exc:  # pragma: no cover
            bot.halt(str(exc))
            raise
        time.sleep(bot.config.runtime.poll_seconds)


def run_research_grid(config_path: str, base_config: AppConfig) -> dict[str, object]:
    _, market_data = build_bot(config_path, config=base_config, skip_live_credentials=True)
    if not hasattr(market_data, "all_candles"):
        raise ValueError("--research-grid requires a market data provider with all_candles() support")
    candles = market_data.all_candles(base_config.runtime.symbol, base_config.runtime.timeframe)
    results = [asdict(result) for result in run_rule_lab(candles, base_config, generate_default_candidates(base_config))]
    by_win_rate = sorted(results, key=lambda item: (item["win_rate"], item["profit"], -item["max_drawdown"]), reverse=True)
    by_profit = sorted(results, key=lambda item: item["profit"], reverse=True)
    return {
        "runs": len(results),
        "timeframe": base_config.runtime.timeframe,
        "best_by_win_rate": by_win_rate[:5],
        "best_by_profit": by_profit[:5],
    }


if __name__ == "__main__":
    main()
