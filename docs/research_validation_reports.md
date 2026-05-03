# Research Validation Reports

日経225マイクロの研究候補を、利益額だけでなく実運用前の安定性で落とし込むための追加レポート。

## 実行コマンド

```powershell
py -m kanekasegi.research `
  --config config.backtest-nk225micro.macro.lot3.yaml `
  --top 10 `
  --min-trades 30 `
  --checkpoint-dir results `
  --batch-name nk225micro-research `
  --report-output-dir output
```

既存のJSON checkpointは維持しつつ、`output/` に以下を追加出力する。

- `research_candidates.csv`
- `research_candidates.json`
- `monthly_summary.csv`
- `session_summary.csv`
- `direction_summary.csv`
- `external_filter_summary.csv`
- `sq_filter_summary.csv`
- `rejected_candidates.csv`

## 採点方針

`research_candidates.csv` は総利益順ではなく、以下をまとめてスコア化する。

- `net_profit`
- `max_drawdown`
- `average_monthly_pnl`
- `profitable_months / losing_months`
- `max_consecutive_losing_months`
- `one_month_dependency_score`
- `trades`
- `min_available_balance`
- `test_period_net_profit`
- `slippage_test_net_profit`

`one_month_dependency_score` は、プラス月の利益合計に対して最大プラス月が占める比率。低いほど利益が分散していて、1か月依存が弱い。

## Rejection Reasons

`rejected_candidates.csv` には、候補を落とした理由を複数理由で出す。

- `too_few_trades`
- `one_month_dependency`
- `high_drawdown`
- `test_period_negative`
- `slippage_sensitive`
- `weak_monthly_stability`
- `low_available_balance`

## 外部要因プローブ

`external_filter_summary.csv` は上位候補に対して、以下の固定プローブを比較する。

- `night_short_sp500_down`
- `night_short_usdjpy_down`
- `night_short_usdjpy_down_us10y_up`
- `midday_long_sp500_up`
- `fade_off_vix_above_threshold`

外部要因CSVがない場合は `status=missing_external_factors` として空振りを明示する。

## SQ/限月プローブ

`sq_filter_summary.csv` は候補ごとに以下を比較する。

- `exclude_sq`
- `exclude_sq_week`
- `exclude_last_trading_window`
- `exclude_roll_week`
- `exclude_calendar_risk`

最終取引日前後とroll weekは、`MarketCandle.contract_month` がある場合はその限月からSQ日を推定する。これは研究用の決定論的近似であり、live発注ロジックには使わない。
