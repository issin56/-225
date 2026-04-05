$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 10 --min-trades 10 --checkpoint-dir results --batch-name nk225micro-research
