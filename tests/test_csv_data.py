from pathlib import Path

from kanekasegi.csv_data import CsvMarketDataProvider


def test_csv_provider_loads_sample_data(tmp_path: Path):
    csv_path = tmp_path / "sample_ohlcv.csv"
    csv_path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume,session,contract_month,trading_day",
                "2026-04-01T09:00:00+09:00,30300,30320,30290,30310,12,day,202406,2026-04-01",
                "2026-04-01T09:15:00+09:00,30310,30420,30305,30400,14,day,202406,2026-04-01",
                "2026-04-01T09:30:00+09:00,30400,30510,30390,30480,16,day,202406,2026-04-01",
            ]
        ),
        encoding="utf-8",
    )
    provider = CsvMarketDataProvider(
        symbol="BTCUSDT",
        timeframe="15m",
        csv_path=str(csv_path),
    )
    candles = provider.get_ohlcv("BTCUSDT", "15m", 3)
    assert len(candles) == 3
    assert candles[-1].close == 30480.0
