# Research Notes 2026-04-01

## Full Dataset Summary

- zip_files: `29`
- source_rows: `1,818,205`
- selected_rows: `730,448`
- candles(15m): `50,678`
- trade_days: `591`
- first_timestamp: `2023-05-31T16:30:00`
- last_timestamp: `2026-02-27T15:45:00`

## Baseline Result

Command:

```bash
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml
```

Observed result:

- ending_equity: `258165.73`
- profit: `-41834.27`
- trades: `64`
- win_rate: `20.31%`
- max_drawdown: `45945.89`
- min_available_balance: `97437.03`

## Grid Snapshot

Command:

```bash
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml --research-grid
```

Top profit candidate in the current small grid:

- timeframe: `5m`
- breakout_lookback: `12`
- ema_period: `120`
- profit: `62282.10`
- win_rate: `22.25%`
- max_drawdown: `35999.51`

## Practical Takeaway

- 汎用ブレイクアウト単体では勝率7割には届かない
- 先に時間帯、曜日、セッションの絞り込みを進めるべき
- 今後は `kanekasegi.research` を使って候補ルールを比較する
