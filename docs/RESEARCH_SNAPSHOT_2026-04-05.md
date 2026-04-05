# Research Snapshot 2026-04-05

## Dataset

- zip_files: `29`
- source_rows: `1,818,205`
- selected_rows: `730,448`
- candles(15m): `50,678`
- trade_days: `591`
- period: `2023-06-01` to `2026-02-27`

## Baseline

Command:

```powershell
$env:PYTHONPATH = "src"
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml
```

Result:

- ending_equity: `274645.79`
- profit: `-25354.21`
- trades: `757`
- win_rate: `19.15%`
- max_drawdown: `51598.20`
- min_available_balance: `97274.78`

## Current Research Lab Top Candidates

Latest batch:

```powershell
$env:PYTHONPATH = "src"
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 6 --min-trades 30 --checkpoint-dir results --batch-name night-study-20260405
```

Checkpoint:

- `results/20260405-012848-night-study-20260405.json`

Follow-up batch:

```powershell
$env:PYTHONPATH = "src"
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 8 --min-trades 30 --candidate day_breakout_opening_midweek --candidate day_breakout_opening_midweek_wide_trail --candidate day_breakout_opening_midweek_tight_exit --candidate day_breakout_opening_midweek_wide_stop --candidate day_breakout_opening_midweek_long_only --candidate day_breakout_morning_midweek --checkpoint-dir results --batch-name night-study-20260405-exit-fixed
```

Checkpoint:

- `results/20260405-113523-night-study-20260405-exit-fixed.json`

Batch focus:

- day-only
- opening and morning windows
- Tue-Thu filter
- direction split
- tighter vs wider ATR exits

### 1. day_breakout_opening_midweek_wide_stop

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- direction: `both`
- entry window: `09:00-10:30`
- atr_stop_multiplier: `2.4`
- trailing_atr_multiplier: `2.5`
- profit: `36964.37`
- win_rate: `27.44%`
- max_drawdown: `11576.90`
- min_available_balance: `136161.74`

### 2. day_breakout_opening_midweek_wide_trail

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- direction: `both`
- entry window: `09:00-10:30`
- atr_stop_multiplier: `2.2`
- trailing_atr_multiplier: `3.0`
- profit: `36242.29`
- win_rate: `27.07%`
- max_drawdown: `11758.96`
- min_available_balance: `136410.41`

### 3. day_breakout_opening_midweek

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- direction: `both`
- entry window: `09:00-10:30`
- atr_stop_multiplier: `2.0`
- trailing_atr_multiplier: `2.5`
- profit: `32192.82`
- win_rate: `26.39%`
- max_drawdown: `11810.33`
- min_available_balance: `136890.33`

### 4. day_breakout_opening_midweek_tight_exit

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- direction: `both`
- entry window: `09:00-10:30`
- atr_stop_multiplier: `1.6`
- trailing_atr_multiplier: `2.0`
- profit: `28790.33`
- win_rate: `25.00%`
- max_drawdown: `11146.95`
- min_available_balance: `138058.81`

### 5. day_breakout_opening_midweek_long_only

- timeframe: `15m`
- sessions: `day`
- weekdays: `Tue-Thu`
- direction: `long_only`
- entry window: `09:00-10:30`
- atr_stop_multiplier: `2.0`
- trailing_atr_multiplier: `2.5`
- profit: `26680.86`
- win_rate: `27.21%`
- max_drawdown: `11653.88`
- min_available_balance: `137580.17`

## Takeaway

- `day_breakout_opening_midweek_wide_stop` is the new leader. It beat the prior `wide_trail` winner on both profit and drawdown in the follow-up batch.
- `day_breakout_opening_midweek_wide_trail` remains strong, but widening the initial ATR stop mattered more than changing trailing distance in this rule family.
- Direction split was informative but not superior. `long_only` kept most of the edge, while `short_only` underperformed badly and is not a live candidate.
- Tightening exits reduced drawdown slightly, but the profit giveback was larger than the risk benefit.
- After fixing trailing-stop exits in strategy code, the tested trailing variants still did not separate meaningfully from the baseline when the initial stop was unchanged. That points to stop width, not trailing distance, as the more important lever here.
- The current practical shortlist is:
  - `day_breakout_opening_midweek_wide_stop`
  - `day_breakout_opening_midweek_wide_trail`
  - `day_breakout_opening_midweek`
- The next research step should stay inside the opening Tue-Thu regime and test wider-stop neighbors or alternative trend-exit logic instead of more trailing-distance tuning.
