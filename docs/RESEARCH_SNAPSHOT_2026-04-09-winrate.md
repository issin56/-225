# Research Snapshot 2026-04-09 winrate

## Scope

This round focused on improving win rate from the current `3-lot` best without giving up too much profit.

Base portfolio before this round:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`

Base result:
- `+224,150`
- `max_drawdown 13,850`
- `win_rate 56.47%`
- `26 profitable months / 0 losing months`

## Main Read

Per-rule win rates in the base portfolio were uneven:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
  - `62 wins / 64 losses`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45`
  - `16 wins / 25 losses`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
  - `43 wins / 21 losses`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
  - `94 wins / 72 losses`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
  - `111 wins / 71 losses`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`
  - `10 wins / 6 losses`

Interpretation:
- the main drag is still the `midday long` block
- the `June rescue` is especially weak in raw win rate
- the `morning short` and `fade` legs are already strong and should be left alone unless needed

## Candidate Family

The following replacements were compared:
- `current_best`
- `no_june_rescue`
- `june_mon_wed_45`
- `june_mon_wed_vix02`

Summary:
- `current_best`
  - `+224,150 / DD 13,850 / win_rate 56.47%`
- `no_june_rescue`
  - `+222,500 / DD 13,850 / win_rate 57.76%`
- `june_mon_wed_45`
  - `+227,600 / DD 13,850 / win_rate 57.09%`
- `june_mon_wed_vix02`
  - `+227,800 / DD 13,850 / win_rate 57.55%`

## New Best Candidate

Current best after the win-rate pass:
- `june_mon_wed_vix02`

Candidate set:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02`

Result:
- `+227,800`
- `max_drawdown 13,850`
- `win_rate 57.55%`
- `26 profitable months / 0 losing months`
- `average_monthly_pnl 7,855.17`

Walk-forward:
- `accepted_both_windows 4/4`
- `total_test_profit 63,700`
- `average_test_win_rate 58.26%`
- `worst_test_drawdown 5,400`

Interpretation:
- narrowing the June rescue to `Mon-Wed` improved quality materially
- adding `VIX > 0.2` kept enough upside while avoiding weak June entries
- this is better than simply removing the June rescue, because it improved both raw profit and win rate

Files:
- `results/portfolio-research-2026-04-09-winrate-family.json`
- `results/portfolio-research-2026-04-09-june-mon-wed-vix02.json`
- `results/portfolio-diagnostics-2026-04-09-june-mon-wed-vix02.json`
- `results/validation-2026-04-09-june-mon-wed-vix02-dd-gated.json`
- `results/validation-2026-04-09-no-june-rescue-dd-gated.json`
