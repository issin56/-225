from datetime import datetime

from kanekasegi.storage import Storage
from kanekasegi.types import BotStatus, RunMode


def test_save_status_writes_health_file(tmp_path):
    storage = Storage(
        str(tmp_path / "test.db"),
        str(tmp_path / "bot.jsonl"),
        str(tmp_path / "health.json"),
        "MEMORY",
    )
    status = BotStatus(mode=RunMode.PAPER, last_heartbeat=datetime(2024, 1, 1, 0, 0, 0))
    storage.save_status(status)
    contents = (tmp_path / "health.json").read_text(encoding="utf-8")
    assert '"mode": "paper"' in contents
