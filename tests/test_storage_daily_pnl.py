from kanekasegi.storage import Storage


def test_storage_tracks_daily_pnl_by_trading_day(tmp_path):
    storage = Storage(
        sqlite_path=str(tmp_path / "test.db"),
        log_path=str(tmp_path / "bot.jsonl"),
        health_path=str(tmp_path / "health.json"),
    )

    storage.save_daily_pnl(1000, "2023-06-01")
    storage.save_daily_pnl(-500, "2023-06-02")

    assert storage.load_daily_pnl("2023-06-01") == 1000
    assert storage.load_daily_pnl("20230602") == -500
    assert storage.load_total_realized_pnl() == 500
