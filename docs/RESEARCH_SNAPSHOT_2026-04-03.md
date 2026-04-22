# Research Snapshot 2026-04-03

## Current Configuration Notes

- dataset: `JPX minute zip`
- period: `2023-06-01` to `2026-02-27`
- initial_balance: `300000`
- per_contract_margin: `50000`
- contract_point_value: `10`
- max_position_notional: `500000`

## Confirmed Stronger Candidates

### 1. day_midday_long_trail

- timeframe: `5m`
- window: `10:00-13:30`
- direction: `long_only`
- profit: `51500.0`
- trades: `188`
- win_rate: `0.4787`
- max_drawdown: `13600.0`
- min_available_balance: `250000.0`
- profitable_months: `17/33`

### 2. both_fast_short_tp

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- profit: `34100.0`
- trades: `4499`
- win_rate: `0.4605`
- max_drawdown: `29900.0`
- min_available_balance: `235750.0`
- profitable_months: `15/33`

### 3. day_midday_long_mon_thu_trail

- timeframe: `5m`
- window: `10:00-13:30`
- direction: `long_only`
- weekdays: `Mon-Thu`
- profit: `21500.0`
- trades: `534`
- win_rate: `0.4288`
- max_drawdown: `11950.0`
- min_available_balance: `243800.0`
- profitable_months: `15/33`

### 4. both_fast_short_time_stop

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- time_stop_bars: `6`
- profit: `18950.0`
- trades: `4630`
- win_rate: `0.4583`
- max_drawdown: `32250.0`
- min_available_balance: `223300.0`
- profitable_months: `12/33`

### 5. day_morning_short_tp

- timeframe: `15m`
- window: `09:15-11:15`
- direction: `short_only`
- profit: `14400.0`
- trades: `232`
- win_rate: `0.5345`
- max_drawdown: `15500.0`
- min_available_balance: `251900.0`
- profitable_months: `16/33`

### 6. day_morning_short_mon_thu_tight_stop

- timeframe: `15m`
- window: `09:15-11:15`
- direction: `short_only`
- weekdays: `Mon-Thu`
- fixed_stop_ticks: `14`
- profit: `14200.0`
- trades: `184`
- win_rate: `0.5109`
- max_drawdown: `17700.0`
- min_available_balance: `251900.0`
- profitable_months: `18/33`

### 7. day_morning_short_mon_thu_tp

- timeframe: `15m`
- window: `09:15-11:15`
- direction: `short_only`
- weekdays: `Mon-Thu`
- profit: `14050.0`
- trades: `183`
- win_rate: `0.5246`
- max_drawdown: `15900.0`
- min_available_balance: `251800.0`
- profitable_months: `18/33`

### 8. day_midday_long_looser_trail

- timeframe: `5m`
- window: `10:00-13:30`
- direction: `long_only`
- trailing_atr_multiplier: `2.4`
- profit: `20500.0`
- trades: `668`
- win_rate: `0.4356`
- max_drawdown: `14850.0`
- min_available_balance: `240150.0`
- profitable_months: `16/33`

### 9. day_midday_long_looser_trail_mon_thu

- timeframe: `5m`
- window: `10:00-13:30`
- direction: `long_only`
- weekdays: `Mon-Thu`
- trailing_atr_multiplier: `2.4`
- profit: `22100.0`
- trades: `533`
- win_rate: `0.4428`
- max_drawdown: `13000.0`
- min_available_balance: `246100.0`
- profitable_months: `15/33`

### 10. day_morning_short_trend_exit

- timeframe: `15m`
- window: `09:15-11:15`
- direction: `short_only`
- profit: `13200.0`
- trades: `133`
- win_rate: `0.4586`
- max_drawdown: `10700.0`
- min_available_balance: `251900.0`
- profitable_months: `15/33`

### 11. both_fast_short_wider_tp

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- take_profit_ticks: `10`
- profit: `19050.0`
- trades: `4355`
- win_rate: `0.4365`
- max_drawdown: `37050.0`
- min_available_balance: `231900.0`
- profitable_months: `15/33`

### 12. both_fast_short_tight_stop_mon_thu

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- weekdays: `Mon-Thu`
- fixed_stop_ticks: `8`
- take_profit_ticks: `8`
- profit: `17650.0`
- trades: `3494`
- win_rate: `0.4405`
- max_drawdown: `22650.0`
- min_available_balance: `247000.0`
- profitable_months: `19/33`

### 13. both_fast_short_mon_thu

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- weekdays: `Mon-Thu`
- profit: `12800.0`
- trades: `3458`
- win_rate: `0.4578`
- max_drawdown: `33700.0`
- min_available_balance: `242300.0`
- profitable_months: `15/33`

### 14. both_fast_short_tight_stop

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- fixed_stop_ticks: `8`
- take_profit_ticks: `8`
- profit: `30450.0`
- trades: `4554`
- win_rate: `0.4420`
- max_drawdown: `26450.0`
- min_available_balance: `239650.0`
- profitable_months: `14/33`

### 15. both_fast_short_mon_thu

- timeframe: `5m`
- sessions: `both`
- direction: `short_only`
- weekdays: `Mon-Thu`
- profit: `12800.0`
- trades: `3458`
- win_rate: `0.4578`
- max_drawdown: `33700.0`
- min_available_balance: `242300.0`
- profitable_months: `15/33`

### 16. day_opening_both_trail

- timeframe: `15m`
- window: `09:00-10:30`
- direction: `both`
- profit: `8650.0`
- trades: `329`
- win_rate: `0.4711`
- max_drawdown: `21200.0`
- min_available_balance: `239150.0`
- profitable_months: `16/33`

## Confirmed Weaker Candidates

- `day_midday_short_trail`: `profit=-9900.0`
- `day_opening_short_tp`: `profit=-6650.0`
- `day_opening_tue_fri_long`: `profit=-2350.0`
- `day_opening_tue_fri_short`: `profit=-1450.0`
- `night_early_short_tp`: `profit=-400.0`
- `both_fast_short_mon_thu_time_stop`: `profit=-1750.0`

## Immediate Takeaways

- `midday long` is currently the strongest family by profit and drawdown balance, and the base version still beats the tighter time-stop variant.
- `morning short` is the cleanest higher-win-rate family so far, and `Mon-Thu` filtering plus a slightly tighter stop is the best `15m` short variant at the moment.
- `fast short` on `5m` now splits into two useful profiles:
  - `both_fast_short_tp`: higher raw profit
  - `both_fast_short_tight_stop_mon_thu`: better drawdown and monthly consistency
- `opening` is mixed and should be deprioritized unless a stronger filter appears.
- `night` remains weak relative to day-session rules.

## Next Research Focus

- keep `day_midday_long_trail` as the 5m long benchmark and test smaller exit tweaks around it
- use `day_morning_short_mon_thu_tight_stop` as the current 15m short benchmark
- compare `both_fast_short_tp` against `both_fast_short_tight_stop_mon_thu` in a portfolio context
- compare `day_morning_short_mon_thu_tight_stop` against slightly wider take-profit or tighter time-stop only
