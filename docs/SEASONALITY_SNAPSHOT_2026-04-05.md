# Seasonality Snapshot 2026-04-05

## Target

- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_tp`

## Hybrid Result

- profit: `+69,050`
- max_drawdown: `13,750`
- profitable_months: `19/33`

Worst months:

- `2024-10`: `-6,250`
- `2023-10`: `-4,950`
- `2023-11`: `-4,650`
- `2024-01`: `-3,650`
- `2025-06`: `-3,300`

Weak month numbers:

- `10月`
  - `3年中2回マイナス`
  - 平均 `-2,533`
- `6月`
  - `3年中2回マイナス`
  - 平均はわずかにプラスだが不安定
- `1月`
  - サンプルは少ないが弱め
- `2月`
  - 現時点では 1 回だけでマイナス

## Filtered Result

- profit: `+64,000`
- max_drawdown: `12,000`
- profitable_months: `21/33`

Worst months:

- `2025-09`: `-5,800`
- `2023-10`: `-4,400`
- `2023-11`: `-3,550`
- `2024-10`: `-3,100`
- `2024-01`: `-1,500`

Weak month numbers:

- `10月`
  - 平均 `-1,166`
- `9月`
  - 平均 `-766`
- `6月`
  - 平均はプラスだが、`3年中2回マイナス`

## Practical Read

- `10月` は両ポートフォリオで共通して弱い
- `6月` は収益ゼロ近辺でブレが大きい
- `9月` は filtered 側で新たな弱点
- `3月`, `4月`, `7月`, `12月` はかなり強い

## Next Experiments

1. `10月` だけ夜間 short の条件を厳しくする
2. `6月` と `9月` に `prior_session_filter` か `external_factor_filter` を追加して守りを厚くする
3. `10月` の負けを作っているのが昼 long なのか夜 short なのかを、戦略別月次で切る
4. `USD/JPY` と `米株先物` の CSV を入れて、`10月` と `9月` の risk-off 判定に使えるかを見る

## USD/JPY Night Filter Update

Target:

- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`

Result:

- profit: `+65,800`
- max_drawdown: `8,400`
- profitable_months: `21/33`
- longest_losing_streak: `1`

Read:

- `10月` は平均マイナスから平均プラスへ改善
- `6月` と `9月` の弱さも軽くなった
- 新しい主な弱点は `1月` と `2月`
- `USD/JPY` は、今のところ `night short` にだけ掛けるのが最適
