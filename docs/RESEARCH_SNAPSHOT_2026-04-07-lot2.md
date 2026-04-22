# Research Snapshot 2026-04-07 lot2

## Scope

This round checks the current portfolio family under a `2-lot` ceiling.

Assumptions:
- starting capital: `300,000`
- `per_contract_margin: 50,000`
- `min_cash_buffer: 50,000`
- `max_simultaneous_positions: 2`
- `max_position_notional: None`

Reference files:
- [portfolio-lot-sweep-2026-04-07.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-lot-sweep-2026-04-07.json)
- [portfolio-research-2026-04-07-lot2-family.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot2-family.json)
- [portfolio-research-2026-04-07-lot2-june-nov-tuning-summary.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot2-june-nov-tuning-summary.json)

## Current Best Under 2 Lots

Best candidate family:
- `lot2-best-v2`

Candidate set:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_midday_long_prev_night_up_trail_only_11_prev_range_above_75`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_60`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Result:
- `+191,550`
- `max_drawdown 10,800`
- `win_rate 55.52%`
- `24 profitable months / 2 losing months`
- `average_monthly_pnl 6,605.17`

Files:
- [portfolio-research-2026-04-07-lot2-best-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot2-best-v2.json)
- [portfolio-diagnostics-2026-04-07-lot2-best-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-07-lot2-best-v2.json)
- [validation-2026-04-07-lot2-best-v2-dd-gated.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-07-lot2-best-v2-dd-gated.json)

## Comparison Read

Top family ranking under `2 lots`:
- `lot2-best-v2`
  - `+191,550 / DD 10,800`
- `v5a_june60`
  - `+191,450 / DD 10,800`
- `v5_6_11`
  - `+189,300 / DD 10,800`
- `v5`
  - `+188,900 / DD 10,800`

Interpretation:
- `June 60-tick rescue` is still useful under `2 lots`.
- The small additional improvement came from loosening the `November` rescue from `90` to `75`.
- Existing `April fade split` variants did not beat this baseline.

## Robustness

Walk-forward read for the `2-lot` best:
- `accepted_both_windows 4/4`
- `total_test_profit 107,750`
- `average_test_win_rate 56.90%`
- `worst_test_drawdown 8,450`

Month-level read:
- worst month is still `2025-06`
- next drag is `2024-04`
- there are only `2 losing months`

## Current Read

This is still far below the long-term target of `50,000 yen per month`.

Even the current `2-lot` best is only about:
- `6,605 yen per month average`

Best next targets remain:
1. reduce the `April fade` drag
2. reduce the `June midday-long` drag
3. rerun the same family after real SBI costs are plugged in

## April Fade Sweep

Reference:
- [portfolio-research-2026-04-07-lot2-april-fade-sweep.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot2-april-fade-sweep.json)

Read:
- current `lot2_best_v2` still has the best raw profit
- `April-only` rescue variants all reduce profit
- `no April fade` is the best stability variant

Stability-leaning April read:
- `lot2_fade_no_april`
  - `+190,400 / DD 10,800 / 25 profitable months / 1 losing month`

Interpretation:
- `April fade` is still a real drag
- but existing `April-only` rescue candidates are not strong enough
- if the priority is pure profit, keep the current `lot2_best_v2`
- if the priority is smoother month distribution, `no April fade` is the cleaner defensive branch
