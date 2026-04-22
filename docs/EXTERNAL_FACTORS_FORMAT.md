# External Factors CSV Format

## Purpose

- `USD/JPY`
- `米株先物`
- `米10年金利`

のような外部要因を、研究ラボとポートフォリオ研究で日次フィルタとして使うためのCSV形式。

## Required columns

- `trading_day`

## Optional columns

- `session`
  - `both`
  - `day`
  - `night`
- any numeric factor column
  - `usd_jpy_change`
  - `us_index_change`
  - `us10y_change_bp`
  - `es_futures_change`

## Example

```csv
trading_day,session,usd_jpy_change,us_index_change,us10y_change_bp
2026-01-05,both,0.18,-0.42,3.1
2026-01-05,night,-0.25,-0.61,4.4
2026-01-06,both,-0.33,0.55,-2.8
```

## Rule mapping

- `external_factor_name`
  - 使う列名
- `external_factor_filter`
  - `all`
  - `positive`
  - `negative`
- `external_factor_min_value`
  - 閾値

## Matching rule

- まず `trading_day + both`
- 次に `trading_day + session`

の順に評価し、`session` 側があれば上書きする。

## Important notes

- `trading_day` は `timestamp` ではなく、できるだけ JPX の取引日ベースに合わせる
- 夜間セッションは日付ずれが起きやすいので、CSVも `trading_day` 基準で作る
- 欠損値は空欄でよいが、その日は該当フィルタが通らない
