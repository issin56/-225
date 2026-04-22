# Current Research Status

Generated: `2026-04-22T23:58:46+09:00`

## Current Leader
- name: `lot3_base10_june_t8`
- bundle_date: `2026-04-09`
- bundle_mode: `matched result/validation/diagnostics set`
- result: [portfolio-research-2026-04-09-lot3_base10_june_t8.json](results/portfolio-research-2026-04-09-lot3_base10_june_t8.json)
- validation: [validation-2026-04-09-lot3_base10_june_t8-dd-gated.json](results/validation-2026-04-09-lot3_base10_june_t8-dd-gated.json)
- diagnostics: [portfolio-diagnostics-2026-04-09-lot3_base10_june_t8.json](results/portfolio-diagnostics-2026-04-09-lot3_base10_june_t8.json)
- profit: `232850.0`
- max_drawdown: `13300.0`
- win_rate: `0.5772`
- trades: `570`
- profitable_months: `26`
- losing_months: `0`
- average_monthly_pnl: `8029.31`

## Leader Candidate Set
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_10`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`

## Weak Months
- `2026-02`: `150.0`
- `2023-09`: `250.0`
- `2024-04`: `1450.0`
- `2024-01`: `1500.0`
- `2024-06`: `2500.0`

## Validation
- tested_windows: `4`
- accepted_both_windows: `4`
- total_test_profit: `129750.0`
- average_test_win_rate: `0.586`
- worst_test_drawdown: `11500.0`

## Latest Snapshot
- snapshot: [RESEARCH_SNAPSHOT_2026-04-22.md](docs/RESEARCH_SNAPSHOT_2026-04-22.md)

```md
# Research Snapshot 2026-04-22

Current strongest portfolio remains `lot3_base10_june_t8`.

Because `lot3_base10_june_t8_opening_april_vix05_exsq_range110` still lacks a clearly better, like-for-like validated replacement over the promoted base path, this run reverted the comparison anchor to the promoted six-sleeve baseline instead of continuing to treat the April add-on branch as the default leader.

- baseline: `lot3_base10_june_t8`
- baseline file: `results/portfolio-research-2026-04-22-lot3_base10_june_t8-current-rerun-2.json`
- baseline result: `+232,850 / DD 13,300 / win_rate 57.72% / trades 570 / 2026-02 +150`
- baseline validation: `results/validation-2026-04-19-lot3_base10_june_t8-sq-dd-gated.json`

## Batch: Morning Sleeve Validation Closure

This batch kept the promoted baseline fixed and only re-ranked nearby `day_morning_short_mon_thu_prev_night_down...` definitions as single-sleeve candidates before considering any full-bundle rerun.

Validated candidates:
- `day_morning_short_tue_fri_prev_night_down_tight_stop`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_t8`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_t16`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_1_2_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_1_2_6_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`

Saved files:
```

## Recent Batch Summaries
- [portfolio-research-2026-04-22-lot3-night-and-morning-followup-baseline-summary.json](results/portfolio-research-2026-04-22-lot3-night-and-morning-followup-baseline-summary.json)
  decision: `keep lot3_base10_june_t8; replacing the morning sleeve to support the baseline night-profit challenger failed immediately in-bundle, and nearby night alternates ex_2_6_10_11_12 and usdjpy_down_us10y_up underperformed the promoted baseline without repairing the key weak month.`
  best_new_candidate: `lot3_night_ex26101112_baseline_rerun` / profit `217100.0` / DD `17000.0` / win_rate `0.5581`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-04-22-lot3-night-baseline-reconciliation-summary.json](results/portfolio-research-2026-04-22-lot3-night-baseline-reconciliation-summary.json)
  decision: `keep lot3_base10_june_t8; the ex_2_5_6_8_10_11_12 night swap out-earned the baseline but did so with worse drawdown, a new 2024-09 losing month, and no improvement to 2026-02, while the only_1_7 control preserved stability only by giving up too much profit.`
  best_new_candidate: `lot3_night_ex2568101112_baseline_rerun` / profit `236600.0` / DD `15450.0` / win_rate `0.5698`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-04-22-lot3-baseline-opening-neighbor-closure-summary.json](results/portfolio-research-2026-04-22-lot3-baseline-opening-neighbor-closure-summary.json)
  decision: `keep lot3_base10_june_t8; morning sleeve neighbors did not create a new February repair path, and the strongest opening-base standalone sleeves still underperformed or destabilized the promoted bundle when rerun in full.`
  best_new_candidate: `lot3_opening_base_ex126710_baseline_macro` / profit `229250.0` / DD `23900.0` / win_rate `0.5737`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-04-22-lot3-opening-base-and-night-neighbors-current-summary.json](results/portfolio-research-2026-04-22-lot3-opening-base-and-night-neighbors-current-summary.json)
  decision: `keep lot3_base10_june_t8_opening_april_vix05_exsq_range110; opening-base neighbors remained inferior, and the best night month-filter variant improved profit by only 1200 while worsening drawdown and leaving `2026-02` unchanged.`
  best_new_candidate: `lot3_night_ex2568101112_current_macro` / profit `237450.0` / DD `15450.0` / win_rate `0.5719`
  baseline: `lot3_base10_june_t8_opening_april_vix05_exsq_range110`
- [portfolio-research-2026-04-22-lot3-june-sleeve-neighbors-current-summary.json](results/portfolio-research-2026-04-22-lot3-june-sleeve-neighbors-current-summary.json)
  decision: `keep lot3_base10_june_t8_opening_april_vix05_exsq_range110; all reproducible June-sleeve neighbors under the promoted leader lost profit, none improved 2026-02 beyond +150, and stricter range filters introduced June weakness without any drawdown relief`
  baseline: `lot3_base10_june_t8_opening_april_vix05_exsq_range110`
- [portfolio-research-2026-04-22-lot3-opening-april-threshold-plateau-current-summary.json](results/portfolio-research-2026-04-22-lot3-opening-april-threshold-plateau-current-summary.json)
  decision: `keep lot3_base10_june_t8_opening_april_vix05_exsq_range110; the April opening near-neighbor sweep showed a threshold plateau around vix_up 0.04-0.06 and range_above 105-110, while looser range100, tighter range115, and adding sp500_down_02 all reduced profit without improving weak months or drawdown.`
  best_new_candidate: `lot3_opening_april_vix04_exsq_range110_current_macro` / profit `236250.0` / DD `13300.0` / win_rate `0.5795`

## Recent Result Files
- `2026-04-22 23:58:33` [portfolio-research-2026-04-22-lot3-night-and-morning-followup-baseline-summary.json](results/portfolio-research-2026-04-22-lot3-night-and-morning-followup-baseline-summary.json)
- `2026-04-22 23:56:51` [portfolio-research-2026-04-22-lot3-night-ex26101112-baseline-rerun.json](results/portfolio-research-2026-04-22-lot3-night-ex26101112-baseline-rerun.json)
- `2026-04-22 23:56:50` [portfolio-research-2026-04-22-lot3-night-us10yup-ex25689101112-baseline-rerun.json](results/portfolio-research-2026-04-22-lot3-night-us10yup-ex25689101112-baseline-rerun.json)
- `2026-04-22 23:55:34` [portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-vix02-baseline.json](results/portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-vix02-baseline.json)
- `2026-04-22 23:55:34` [portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-sp500down-baseline.json](results/portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-sp500down-baseline.json)
- `2026-04-22 23:54:18` [portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-tuefri-baseline.json](results/portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-tuefri-baseline.json)
- `2026-04-22 22:58:00` [portfolio-research-2026-04-22-lot3-night-baseline-reconciliation-summary.json](results/portfolio-research-2026-04-22-lot3-night-baseline-reconciliation-summary.json)
- `2026-04-22 22:55:55` [validation-2026-04-22-lot3-night-only17-baseline-dd13300.json](results/validation-2026-04-22-lot3-night-only17-baseline-dd13300.json)
- `2026-04-22 22:55:55` [validation-2026-04-22-lot3-night-ex2568101112-baseline-dd13300.json](results/validation-2026-04-22-lot3-night-ex2568101112-baseline-dd13300.json)
- `2026-04-22 22:54:36` [portfolio-research-2026-04-22-lot3-night-only17-baseline-rerun.json](results/portfolio-research-2026-04-22-lot3-night-only17-baseline-rerun.json)
- `2026-04-22 22:54:36` [portfolio-research-2026-04-22-lot3-night-ex2568101112-baseline-rerun.json](results/portfolio-research-2026-04-22-lot3-night-ex2568101112-baseline-rerun.json)
- `2026-04-22 22:54:36` [portfolio-research-2026-04-22-lot3_base10_june_t8-current-rerun-2.json](results/portfolio-research-2026-04-22-lot3_base10_june_t8-current-rerun-2.json)
