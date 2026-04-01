import os

from kanekasegi.runtime_env import load_dotenv


def test_load_dotenv_sets_missing_values(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("DISCORD_WEBHOOK_URL=https://example.invalid/webhook\n", encoding="utf-8")
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    load_dotenv(env_file)
    assert os.environ["DISCORD_WEBHOOK_URL"] == "https://example.invalid/webhook"
