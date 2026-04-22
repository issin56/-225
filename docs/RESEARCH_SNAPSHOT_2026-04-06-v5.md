# Research Snapshot 2026-04-06 v5

## Current Best

- portfolio: `stable_seasonal_v5`
- sample basis: `29 active months`
- result: `+101,300 / max_drawdown 5,400 / win_rate 55.30% / 22 profitable months / 3 losing months`
- average monthly pnl: `3,493.10`

Primary files:
- [portfolio-research-2026-04-06-stable-seasonal-v5.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-stable-seasonal-v5.json)
- [portfolio-diagnostics-2026-04-06-stable-seasonal-v5.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-stable-seasonal-v5.json)
- [validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v5-dd-gated.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v5-dd-gated.json)
- [portfolio-research-2026-04-06-v4-split-family.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-v4-split-family.json)

## Candidate Set

- `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10_11`
- `day_midday_long_prev_night_up_trail_only_11_prev_range_above_90`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

What changed versus `stable_seasonal_v4`:
- `midday long` was split instead of globally replaced.
- Base `midday` keeps the broader profitable months.
- `November` only is handled by a tighter rescue candidate using `prior_session_range_above_90`.

## Why It Won

The split fixed the main `November` drag without sacrificing the stronger `midday long` months.

Headline comparison versus `stable_seasonal_v4`:
- profit: `99,000 -> 101,300`
- win rate: `54.66% -> 55.30%`
- losing months: `4 -> 3`
- drawdown: `5,400 -> 5,400`

Month-level read:
- `2023-11`: `-400 -> +1,950`
- `2025-06`: unchanged weak month at `-1,000`
- `2024-04`: unchanged weak month at `-1,900`

## Validation Read

DD-gated walk-forward:
- `accepted_both_windows 4/4`
- `total_test_profit 66,950`
- `average_test_win_rate 56.86%`
- `worst_test_drawdown 5,400`

This keeps the same maximum drawdown gate as `v4` and still passes every window.

## Split Family Read

Main comparisons:
- `stable_seasonal_v5_midday_split_11`
  - `+101,300 / DD 5,400 / win_rate 55.30%`
- `stable_seasonal_v5_midday_split_6_11`
  - `+100,200 / DD 5,400 / win_rate 56.45%`
- `stable_seasonal_v5a_midday_split_11_june60`
  - `+100,550 / DD 5,400 / win_rate 55.87%`

Interpretation:
- `November-only rescue` is the best profit-preserving split.
- `June rescue` variants improve hit rate but do not beat `v5` on profit.
- `April fade VIX split` is still not useful enough.

## Next Target

The remaining weak months are now concentrated and clear:
- `2024-04`
  - main drag is still the `fade` rule
- `2025-06`
  - main drag is still the `midday long`
- `2023-09`
  - very small remaining loss

Best next research path:
1. improve the `fade` rule for `April` without losing the strong `2025-04` upside
2. test lighter `June-only` rescue logic for `midday long`
3. keep `v5` as the promotion baseline until a new candidate beats it on both profit and DD
