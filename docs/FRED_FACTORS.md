# FRED Factors

## Current Daily Set

- `DEXJPUS -> usd_jpy_change`
- `SP500 -> sp500_change`
- `VIXCLS -> vix_change`
- `DGS10 -> us10y_change_bp`

## Build

一括生成:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build-macro-factors.ps1 -StartDate 2023-01-01
```

既定の出力先:

- `data/external_factors.macro.fred.csv`

個別生成:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build-usdjpy-factors.ps1 -StartDate 2023-01-01
powershell -ExecutionPolicy Bypass -File scripts/build-sp500-factors.ps1 -StartDate 2023-01-01
powershell -ExecutionPolicy Bypass -File scripts/build-vix-factors.ps1 -StartDate 2023-01-01
powershell -ExecutionPolicy Bypass -File scripts/build-us10y-factors.ps1 -StartDate 2023-01-01
```

## Notes

- `assign_mode=next_business_day`
  - FRED の観測日を次の JPX 売買日へ寄せる

- `usd_jpy_change`
  - 日次の `% change`

- `sp500_change`
  - 日次の `% change`

- `vix_change`
  - 日次の絶対差分

- `us10y_change_bp`
  - 日次の差分を `100` 倍して basis points に変換

## Related Files

- [fred_factors.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\fred_factors.py)
- [config.backtest-nk225micro.macro.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\config.backtest-nk225micro.macro.yaml)
