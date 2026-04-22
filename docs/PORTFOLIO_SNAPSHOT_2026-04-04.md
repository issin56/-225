# Portfolio Snapshot 2026-04-04

## Assumption

- single account
- single open position at a time
- candidate order is priority order
- same `config.backtest-nk225micro.yaml`

## Portfolio 1: Profit-Leaning Core + Fast Short

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`
- `both_fast_short_tp`

Result:

- ending_equity: `330200.0`
- profit: `30200.0`
- trades: `5128`
- win_rate: `0.4512`
- max_drawdown: `36500.0`
- min_available_balance: `220850.0`
- profitable_months: `13/33`

Breakdown:

- `day_midday_long_trail`: `+13750.0`
- `day_morning_short_mon_thu_tight_stop`: `+10050.0`
- `both_fast_short_tp`: `+6400.0`

## Portfolio 2: Stable Fast Short Variant

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`
- `both_fast_short_tight_stop_mon_thu`

Result:

- ending_equity: `308200.0`
- profit: `8200.0`
- trades: `4125`
- win_rate: `0.4320`
- max_drawdown: `34250.0`
- min_available_balance: `232850.0`
- profitable_months: `15/33`

Breakdown:

- `day_midday_long_trail`: `+14400.0`
- `day_morning_short_mon_thu_tight_stop`: `+5750.0`
- `both_fast_short_tight_stop_mon_thu`: `-11950.0`

## Portfolio 3: Two-Rule Core

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`

Result:

- ending_equity: `324600.0`
- profit: `24600.0`
- trades: `858`
- win_rate: `0.4359`
- max_drawdown: `23200.0`
- min_available_balance: `242950.0`
- profitable_months: `14/33`

Breakdown:

- `day_midday_long_trail`: `+10400.0`
- `day_morning_short_mon_thu_tight_stop`: `+14200.0`

## Takeaway

- The two-rule core is currently the cleanest balance of profit and drawdown.
- Adding `both_fast_short_tp` raises total profit, but drawdown worsens and monthly stability drops.
- Adding `both_fast_short_tight_stop_mon_thu` improves the idea on paper as a single rule, but hurts the combined portfolio in this priority model.
- Portfolio interaction matters enough that single-rule winners do not automatically improve the combined system.

## Next Step

- test a portfolio where `fast short` is allowed only when day-session rules are inactive by time window, not just by priority order
- compare portfolio results month by month instead of only aggregate totals
