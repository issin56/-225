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

Latest batch:

```bash
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 6 --min-trades 30 --checkpoint-dir results --batch-name night-study-20260404
```

Checkpoint:

- `results/20260404-013403-night-study-20260404.json`

Direction split batch:

```bash
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 6 --min-trades 30 --candidate day_breakout_opening_midweek --candidate day_breakout_opening_midweek_long_only --candidate day_breakout_opening_midweek_short_only --candidate day_breakout_morning_midweek --candidate day_breakout_morning_midweek_long_only --candidate day_breakout_morning_midweek_short_only --checkpoint-dir results --batch-name night-study-20260404-direction
```

Checkpoint:

- `results/20260404-170655-night-study-20260404-direction.json`

Command:

```bash
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 6 --min-trades 30
```

### 1. day_breakout_opening

- timeframe: `15m`
- sessions: `day`
- weekdays: `Mon-Fri`
- entry window: `09:00-10:30`
- skip_first_minutes: `15`
- profit: `33355.90`
- win_rate: `25.44%`
- max_drawdown: `17717.67`

### 2. day_breakout_opening_midweek

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- entry window: `09:00-10:30`
- skip_first_minutes: `15`
- profit: `32192.82`
- win_rate: `26.39%`
- max_drawdown: `11810.33`
- min_available_balance: `136890.33`

### 3. day_breakout_opening_no_friday

- timeframe: `15m`
- sessions: `day`
- weekdays: `Mon-Thu`
- entry window: `09:00-10:30`
- skip_first_minutes: `15`
- profit: `29225.44`
- win_rate: `26.89%`
- max_drawdown: `14013.49`
- min_available_balance: `132580.09`

### 4. day_breakout_morning_midweek

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- entry window: `09:15-11:15`
- skip_first_minutes: `15`
- profit: `26473.50`
- win_rate: `29.03%`
- max_drawdown: `13816.59`
- min_available_balance: `140340.65`

### 5. both_breakout_fast

- timeframe: `5m`
- sessions: `day + night`
- weekdays: `Mon-Fri`
- profit: `59115.90`
- win_rate: `22.74%`
- max_drawdown: `34633.59`
- min_available_balance: `139666.51`

## Takeaway

- Day-session limited rules remain stronger and more stable than the tested early-night rule
- Weekday filters materially improved risk-adjusted results in the opening and morning windows
- `day_breakout_opening_midweek` is currently the strongest practical candidate because it kept profit near the all-week opening rule while cutting drawdown by roughly one third
- Direction split testing showed that the edge is not primarily coming from the short side; `opening_midweek_long_only` stayed decent, but both tested `short_only` variants were much weaker
- `opening_midweek_long_only` is the best fallback if the next round prioritizes lower drawdown over maximum profit, with profit `26680.86` and max drawdown `11653.88`
- `both_breakout_fast` still has the highest raw profit, but its trade count and drawdown make it less attractive for a 300k account than the tighter day-session variants
- The next work should focus on exit decomposition for the stronger opening-long and opening-both midweek variants rather than broadening sessions
- The immediate practical path is:
  - day-only
  - opening/morning windows
  - weekday filters
  - exit decomposition
  - opening-long vs opening-both comparison
