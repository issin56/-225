$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
py -3.11 -m kanekasegi.main --config config.backtest.yaml
