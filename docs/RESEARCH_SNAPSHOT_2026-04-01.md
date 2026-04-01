# Research Snapshot 2026-04-01

## Dataset

- zip_files: `29`
- source_rows: `1,818,205`
- selected_rows: `730,448`
- candles(15m): `50,678`
- trade_days: `591`
- period: `2023-06-01` to `2026-02-27`

## Baseline

Command:

```bash
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml
```

Result:

- ending_equity: `258165.73`
- profit: `-41834.27`
- trades: `64`
- win_rate: `20.31%`
- max_drawdown: `45945.89`
- min_available_balance: `97437.03`

## Current Research Lab Top Candidates

Command:

```bash
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 6 --min-trades 30
```

### 1. day_breakout_opening

- timeframe: `15m`
- sessions: `day`
- entry window: `09:00-10:30`
- skip_first_minutes: `15`
- profit: `33355.90`
- win_rate: `25.44%`
- max_drawdown: `17717.67`

### 2. both_breakout_fast

- timeframe: `5m`
- sessions: `day + night`
- profit: `59115.90`
- win_rate: `22.74%`
- max_drawdown: `34633.59`

### 3. day_breakout_morning

- timeframe: `15m`
- sessions: `day`
- entry window: `09:15-11:15`
- skip_first_minutes: `15`
- profit: `24206.81`
- win_rate: `27.17%`
- max_drawdown: `21862.73`

## Takeaway

- Day-session limited rules are currently stronger than the tested early-night rule
- Win rate is still low, so the next work should focus on filtering, exits, and decomposition into smaller rule families
- The immediate practical path is:
  - day-only
  - opening/morning windows
  - weekday filters
  - direction split
