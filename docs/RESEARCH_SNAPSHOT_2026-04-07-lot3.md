# Research Snapshot 2026-04-07 lot3

## Scope

This round checks the current portfolio family under a `3-lot` ceiling.

Assumptions:
- starting capital: `300,000`
- `per_contract_margin: 50,000`
- `min_cash_buffer: 50,000`
- `max_simultaneous_positions: 3`
- `max_position_notional: None`

Reference files:
- [portfolio-research-2026-04-07-lot3-family.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot3-family.json)
- [portfolio-research-2026-04-07-lot3-november-sweep.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot3-november-sweep.json)
- [config.backtest-nk225micro.macro.lot3.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\config.backtest-nk225micro.macro.lot3.yaml)

## Current Best Under 3 Lots

Best candidate family:
- `lot3_best_v2`

Candidate set:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_midday_long_prev_night_up_trail_only_11_prev_range_above_75`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Result:
- `+219,100`
- `max_drawdown 13,850`
- `win_rate 55.00%`
- `25 profitable months / 1 losing month`
- `average_monthly_pnl 7,555.17`

Files:
- [portfolio-research-2026-04-07-lot3-best-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot3-best-v2.json)
- [portfolio-diagnostics-2026-04-07-lot3-best-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-07-lot3-best-v2.json)
- [validation-2026-04-07-lot3-best-v2-dd-gated.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-07-lot3-best-v2-dd-gated.json)

## Family Read

Top ranking under `3 lots`:
- `lot3_best_v2`
  - `+219,100 / DD 13,850`
- `lot3_best_v1`
  - `+217,850 / DD 13,850`
- `lot2_v5_base`
  - `+217,750 / DD 13,850`
- `lot2_best_v2`
  - `+216,300 / DD 13,850`
- `lot2_v5a_base`
  - `+216,200 / DD 13,850`

Interpretation:
- `June rescue` helps again when the threshold is loosened to `45`.
- `November rescue` still helps, and `75` beats both `90` and `60`.
- the raw profit branch still keeps the original April fade.

## Robustness

Walk-forward read for the `3-lot` best:
- `accepted_both_windows 4/4`
- `total_test_profit 132,100`
- `average_test_win_rate 56.85%`
- `worst_test_drawdown 11,500`

Month-level read:
- worst month: `2024-04` at `-2,050`
- next worst months are already positive
- only `1` losing month remains

## April Rebuild

Rebuilt April-specific `fade` candidates were tested against the current `3-lot` best by replacing the April portion of:
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Comparison summary:
- `lot3_best_base`
  - `+219,100 / DD 13,850 / 25 profitable months / 1 losing month`
- `lot3_best_no_april_fade`
  - `+211,250 / DD 13,850 / 26 profitable months / 0 losing months`
- `lot3_best_april_prevdown12_t12`
  - `+217,950 / DD 13,850 / 26 profitable months / 0 losing months`
- `lot3_best_april_prevdown16_t16`
  - `+218,050 / DD 13,850 / 26 profitable months / 0 losing months`
- `lot3_best_april_vixup05`
  - `+218,600 / DD 13,850 / 26 profitable months / 0 losing months`

Best April rebuild branch:
- `lot3_best_april_vixup05`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`

Result:
- `+218,600`
- `max_drawdown 13,850`
- `win_rate 55.06%`
- `26 profitable months / 0 losing months`
- `2024-04 pnl +1,450`
- `2025-04 pnl +23,800`

Interpretation:
- profit is still slightly below `lot3_best_v2` (`+219,100`)
- the April-specific `VIX>0.5` branch removes the remaining losing month without adding drawdown
- `prev_night_down t16` and `t12` are also viable, but both land below `april_vixup05`
- this is now the best stable branch under `3 lots`

Files:
- [portfolio-research-2026-04-07-lot3-april-rebuild-summary.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot3-april-rebuild-summary.json)
- [portfolio-research-2026-04-07-lot3-april-vixup05.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-07-lot3-april-vixup05.json)
- [portfolio-diagnostics-2026-04-07-lot3-april-vixup05.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-07-lot3-april-vixup05.json)
- [validation-2026-04-07-lot3-april-vixup05-dd-gated.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-07-lot3-april-vixup05-dd-gated.json)

## November Follow-up

The April-stable branch was then re-tested by removing or replacing the November rescue:
- `day_midday_long_prev_night_up_trail_only_11_prev_range_above_75`

Comparison summary:
- `lot3_april_vix05_no_nov_rescue`
  - `+224,150 / DD 13,850 / win_rate 56.47% / 26 profitable months / 0 losing months`
- `lot3_april_vix05_nov75`
  - `+219,350 / DD 13,850 / win_rate 55.13% / 26 profitable months / 0 losing months`
- `lot3_april_vix05_nov90`
  - `+219,250 / DD 13,850 / win_rate 55.18% / 26 profitable months / 0 losing months`
- `lot3_april_vix05_nov60`
  - `+218,700 / DD 13,850 / win_rate 54.94% / 26 profitable months / 0 losing months`

Current best under `3 lots`:
- `lot3_april_vix05_no_nov_rescue`

Candidate set:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`

Interpretation:
- the November rescue was hurting the new April-stable branch
- removing it improved both raw profit and win rate
- the strategy now keeps `26 profitable months / 0 losing months`
- the weakest remaining months are all still positive, with `2025-06` at `+350`

Files:
- `results/portfolio-research-2026-04-07-lot3-november-aprilvix05.json`
- `results/portfolio-research-2026-04-07-lot3_april_vix05_no_nov_rescue.json`
- `results/portfolio-diagnostics-2026-04-07-lot3_april_vix05_no_nov_rescue.json`
- `results/validation-2026-04-08-lot3_april_vix05_no_nov_rescue-dd-gated.json`

## Position Usage

For the `3-lot` best:
- trades: `640`
- quantity histogram:
  - `1 lot`: `140`
  - `2 lots`: `270`
  - `3 lots`: `230`
- average contracts per trade: `2.141`

Meaning:
- the strategy does not simply pin to `3 lots`
- but it spends a large part of the sample at `2-3 lots`

## Current Read

This still does not solve the long-term target.

Even the current `3-lot` best is only:
- `7,555 yen per month average`

The best stable branch is now:
- `lot3_best_april_vixup05`
- `7,537.93 yen per month average`
- `0 losing months`

Best next targets remain:
1. reduce the `June midday-long` drag without hurting the good June years
2. revisit the negative `November rescue` branch
3. rerun after real SBI costs are plugged in

## Exit Follow-up

Exit variants were then tested on the current best branch, focused on:
- the June rescue `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02`
- the base long `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`

Best result:
- `lot3_june_t8`
  - `+230,200 / DD 13,850 / win_rate 57.90% / 26 profitable months / 0 losing months`

Compared with the previous best:
- previous best
  - `+227,800 / DD 13,850 / win_rate 57.55%`
- `june_t8`
  - `+230,200 / DD 13,850 / win_rate 57.90%`
- `june_looser_trail`
  - `+228,300 / DD 13,850 / win_rate 57.73%`
- `base_looser_trail`
  - `+227,400 / DD 13,850 / win_rate 57.73%`
- `base_t8`
  - `+203,800 / DD 13,250 / win_rate 56.80%`

Interpretation:
- the strongest improvement came from tightening the June rescue `time_stop` from `12` to `8`
- the base long exit variants did not beat the June rescue exit tweak
- the new June rescue variant improved both profit and win rate without worsening drawdown

Files:
- `results/portfolio-research-2026-04-09-lot3_june_t8.json`
- `results/portfolio-diagnostics-2026-04-09-lot3_june_t8.json`
- `results/validation-2026-04-09-lot3_june_t8-dd-gated.json`
- `results/portfolio-research-2026-04-09-exit-variants.json`

## Win-Rate Follow-up

Using the new `lot3_april_vix05_no_nov_rescue` branch, the June rescue was swept again with:
- no June rescue
- `prev_range_above_45`
- `prev_range_above_60`
- `prev_range_above_75`
- `prev_range_above_90`

Best win-rate branch:
- `lot3_best_no_nov_no_june_rescue`
  - `+222,500 / DD 13,850 / win_rate 57.76% / 25 profitable months / 0 losing months`

Best balance branch:
- `lot3_april_vix05_no_nov_june90`
  - `+223,950 / DD 13,850 / win_rate 57.60% / 26 profitable months / 0 losing months`

Interpretation:
- removing the June rescue gives the highest raw win rate
- keeping a stricter June rescue at `90` keeps profit almost intact while still lifting win rate above `57.5%`
- compared with `lot3_april_vix05_no_nov_rescue`, the `june90` branch gives up only `200` yen of profit while improving June month balance and retaining `26 profitable months`

Validation:
- `lot3_april_vix05_no_nov_june90` walk-forward: `4/4 pass`
- `total_test_profit 61,150`
- `average_test_win_rate 58.01%`
- `worst_test_drawdown 5,400`

Files:
- `results/portfolio-research-2026-04-09-lot3-winrate-june-sweep.json`
- `results/portfolio-research-2026-04-09-lot3_april_vix05_no_nov_june90.json`
- `results/validation-2026-04-09-lot3_april_vix05_no_nov_june90-dd-gated.json`

## Combined Exit Promotion

The June rescue `t8` branch was then combined with the stronger base-long `time_stop_10` branch.

New promoted best:
- `lot3_base10_june_t8`
  - `+232,850 / DD 13,300 / win_rate 57.72% / 26 profitable months / 0 losing months`

Compared with the previous promoted best:
- `lot3_june_t8`
  - `+230,200 / DD 13,850 / win_rate 57.90%`
- `lot3_base10_june_t8`
  - `+232,850 / DD 13,300 / win_rate 57.72%`

Interpretation:
- combining the `base long time_stop_10` branch with the `June rescue t8` branch improved profit by `+2,650`
- drawdown also improved from `13,850` to `13,300`
- win rate dipped slightly, but stayed above `57.7%`
- month structure remained clean at `26 profitable months / 0 losing months`

Validation:
- DD-gated walk-forward: `4/4 pass`
- `total_test_profit 129,750`
- `average_test_win_rate 58.60%`
- `worst_test_drawdown 11,500`

Files:
- `results/portfolio-research-2026-04-09-lot3_base10_june_t8.json`
- `results/portfolio-diagnostics-2026-04-09-lot3_base10_june_t8.json`
- `results/validation-2026-04-09-lot3_base10_june_t8-dd-gated.json`
