from kanekasegi.csv_data import CsvMarketDataProvider


def test_csv_provider_loads_sample_data():
    provider = CsvMarketDataProvider(
        symbol="BTCUSDT",
        timeframe="15m",
        csv_path="data/sample_ohlcv.csv",
    )
    candles = provider.get_ohlcv("BTCUSDT", "15m", 3)
    assert len(candles) == 3
    assert candles[-1].close == 30480.0
