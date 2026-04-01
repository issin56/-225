from pathlib import Path

from kanekasegi.config import load_config
from kanekasegi.main import build_bot
from kanekasegi.sbi_adapter import SbiFuturesAdapter


def test_build_bot_uses_sbi_adapter_for_live_config(monkeypatch):
    monkeypatch.delenv("SBI_API_KEY", raising=False)
    monkeypatch.delenv("SBI_API_SECRET", raising=False)
    monkeypatch.delenv("SBI_API_ENDPOINT", raising=False)
    bot, _ = build_bot(str(Path("config.live-sbi.yaml")), skip_live_credentials=True)
    assert isinstance(bot.exchange, SbiFuturesAdapter)
    assert bot.config.runtime.broker == "sbi"
    assert bot.config.runtime.symbol == "NK225MICRO"


def test_build_bot_reads_nk225micro_backtest_config():
    config = load_config(str(Path("config.backtest-nk225micro.yaml")))
    assert config.runtime.symbol == "NK225MICRO"
    assert config.runtime.broker == "paper"
    assert config.runtime.data_source == "jpx_zip"
    assert config.paper.initial_balance == 300000
