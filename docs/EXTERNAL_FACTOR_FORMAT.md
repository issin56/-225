# External Factor CSV Format

`runtime.external_factors_csv` には、次の形式の CSV を渡す。

```csv
trading_day,session,usd_jpy_change,us_index_change,us10y_change_bp
2026-01-05,both,0.42,-0.31,4.5
2026-01-05,night,0.28,-0.44,3.0
2026-01-06,both,-0.27,0.55,-2.0
```

ルール:

- `trading_day` は `YYYY-MM-DD` か `YYYYMMDD`
- `session` は省略可。省略時は `both`
- `session` を使う場合は `day` / `night` / `both`
- 数値列名は自由
- 空欄は欠損として扱う

使い方:

- `external_factor_name`: 参照する列名
- `external_factor_filter=positive`: 値が `external_factor_min_value` 以上のときだけ通す
- `external_factor_filter=negative`: 値が `-external_factor_min_value` 以下のときだけ通す

確認コマンド:

```bash
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml --factor-summary
```
