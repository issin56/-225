# External Factors

## Recommended Macro Set

推奨する日次外部要因:

- `usd_jpy_change`
- `sp500_change`
- `vix_change`
- `us10y_change_bp`

推奨生成コマンド:

```powershell
.\scripts\build-macro-factors.ps1 -StartDate 2023-01-01
```

生成先:

- `data/external_factors.macro.fred.csv`

## Purpose

JPX の `trading_day` に合わせて、外部の前日要因を日次CSVへ落とし、研究ラボとポートフォリオ研究の両方で使う。

## CSV Format

必須列:

- `trading_day`

追加列の例:

- `usd_jpy_change`
- `sp500_change`
- `vix_change`
- `us10y_change_bp`

例:

```csv
trading_day,usd_jpy_change,sp500_change,vix_change,us10y_change_bp
2026-01-05,0.42,-0.31,1.8,5.0
2026-01-06,-0.27,0.55,-2.1,-3.0
```

## Candidate Fields

- `external_factor_name`
- `external_factor_filter`
  - `all`
  - `positive`
  - `negative`
- `external_factor_min_value`

## First-Use Mapping

- `usd_jpy_change`
  - first target: `night short`

- `sp500_change`
  - first target: `night short`, `midday long`

- `vix_change`
  - first target: `opening fade` の見送り条件

- `us10y_change_bp`
  - first target: `usd_jpy_change` と組み合わせた補助条件

## Related Files

- [fred_factors.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\fred_factors.py)
- [build-macro-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-macro-factors.ps1)
- [build-usdjpy-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-usdjpy-factors.ps1)
- [build-sp500-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-sp500-factors.ps1)
- [build-vix-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-vix-factors.ps1)
- [build-us10y-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-us10y-factors.ps1)
- [config.backtest-nk225micro.macro.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\config.backtest-nk225micro.macro.yaml)

## Quick Start

```powershell
.\scripts\build-macro-factors.ps1 -StartDate 2023-01-01
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.macro.yaml --factor-summary
```
