# Current Research Status

Generated: `2026-05-08T00:20:34+09:00`

## Current Leader
- name: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- bundle_date: `2026-05-03`
- bundle_mode: `matched result/validation/diagnostics set`
- result: [portfolio-research-2026-05-03-lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun.json](results/portfolio-research-2026-05-03-lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun.json)
- validation: [validation-2026-05-03-lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun-macrolot3-dd13300.json](results/validation-2026-05-03-lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun-macrolot3-dd13300.json)
- diagnostics: [portfolio-diagnostics-2026-05-03-lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun.json](results/portfolio-diagnostics-2026-05-03-lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun.json)
- profit: `235600.0`
- max_drawdown: `10350.0`
- win_rate: `0.5844`
- trades: `539`
- profitable_months: `26`
- losing_months: `0`
- average_monthly_pnl: `8124.14`

## Leader Candidate Set
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105`

## Weak Months
- `2026-02`: `150.0`
- `2023-09`: `250.0`
- `2024-04`: `1400.0`
- `2024-01`: `1500.0`
- `2024-06`: `2500.0`

## Validation
- tested_windows: `4`
- accepted_both_windows: `4`
- total_test_profit: `134050.0`
- average_test_win_rate: `0.5944`
- worst_test_drawdown: `7800.0`

## Latest Snapshot
- snapshot: [RESEARCH_SNAPSHOT_2026-05-08-v1.md](docs/RESEARCH_SNAPSHOT_2026-05-08-v1.md)

```md
# Research Snapshot 2026-05-08

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block paused daily video intake and shifted the work back to direct weak-month validation, focused on the current live weak months `2026-02`, `2023-09`, `2024-04`, `2024-01`, and `2024-06`.

The batch tested 22 existing weak-month-relevant candidates through the research report harness:

- output JSON: `results/weak-month-shift-20260508.json`
- checkpoint: `results/20260508-001816-weak-month-shift-20260508.json`
- report directory: `output/weak-month-20260508`

The only candidates that survived the robustness report were the existing morning short family:

- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
  - net profit `46000`
  - trades `64`
  - win rate `0.6719`
  - max drawdown `6900`
  - average monthly pnl `1586.21`
  - test-period net profit `6600`
  - slippage-stressed net profit `36238.02`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16`
  - net profit `40400`
  - trades `60`
  - win rate `0.65`
```

## Recent Batch Summaries
- [portfolio-research-2026-05-08-calendar-gotobi-durability-summary.json](results/portfolio-research-2026-05-08-calendar-gotobi-durability-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; three targeted same-lane batches showed that the residual morning calendar overlays stay too sparse, the night gotobi overlays weaken acceptance relative to the current ex_sq sleeve, and the midday durability neighbors still fail to produce a bundle-level improvement large enough to justify promotion.`
  best_new_candidate: `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail` / profit `None` / DD `4450.0` / win_rate `0.5265`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-04-macro-followup-rerun-summary.json](results/portfolio-research-2026-05-04-macro-followup-rerun-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; one residual morning macro walk-forward screen plus three fresh same-lane bundle reruns showed that the remaining macro.lot3 follow-up queue is either too sparse, clearly weaker on OOS totals, or operationally duplicate of the promoted bundle.`
  best_new_candidate: `lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun` / profit `235300.0` / DD `10350.0` / win_rate `0.5842`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-04-morning-calendar-closure-summary.json](results/portfolio-research-2026-05-04-morning-calendar-closure-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; three targeted macro.lot3 morning single-sleeve reruns showed that the SQ-only variant is an exact bundle-level no-op, while the only outcome-changing variants reduced full-sample profit and fixed-set walk-forward total without repairing the weak 2026-02 month.`
  best_new_candidate: `lot3-base10-june-t8-night-exsq-middayplain-morningexsqt16-openingrange105-rerun` / profit `227850.0` / DD `10350.0` / win_rate `0.5813`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-04-pairwise-bundle-closure-summary.json](results/portfolio-research-2026-05-04-pairwise-bundle-closure-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; four targeted macro.lot3 bundle recomposition batches showed that the remaining credible pairwise and triple-swap replacements either widened drawdown materially, introduced losing months, or gave up too much full-sample profit while leaving the weakest 2026-02 month unrepaired.`
  best_new_candidate: `lot3-base10-june-t8-nightbase-openingmain6710lite-openingrange105-rerun` / profit `230800.0` / DD `23900.0` / win_rate `0.5754`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-04-opening-prevnightup-midday11-buf4-closure-summary.json](results/portfolio-research-2026-05-04-opening-prevnightup-midday11-buf4-closure-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; the only clean new bundle candidate replaced the opening-main sleeve with day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10, but that rerun lowered full-sample profit, lowered walk-forward total test profit, and introduced losing months, while the midday only_11 and opening prev_night_up only_4 lanes both died on density.`
  best_new_candidate: `lot3-base10-june-t8-night-exsq-middayplain-openingbuf4-openingrange105-rerun` / profit `215900.0` / DD `10350.0` / win_rate `0.5725`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-04-morning-night-opening-closure-summary.json](results/portfolio-research-2026-05-04-morning-night-opening-closure-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; the morning precision family again failed train/test trade-density at 0/4 accepted-both windows, while the only strong night and opening-main challengers merely re-confirmed already-rejected bundle swap candidates rather than producing a new promotable replacement.`
  best_new_candidate: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` / profit `53400.0` / DD `11400.0` / win_rate `0.5667`
  baseline: `lot3_base10_june_t8`

## Recent Result Files
- `2026-05-08 00:19:13` [weak-month-shift-20260508.json](results/weak-month-shift-20260508.json)
- `2026-05-08 00:18:16` [20260508-001816-weak-month-shift-20260508.json](results/20260508-001816-weak-month-shift-20260508.json)
- `2026-05-08 00:17:43` [portfolio-research-2026-05-08-calendar-gotobi-durability-summary.json](results/portfolio-research-2026-05-08-calendar-gotobi-durability-summary.json)
- `2026-05-08 00:14:52` [validation-2026-05-08-night-gotobi-overlays-batch186-macrolot3-wf-dd13300.json](results/validation-2026-05-08-night-gotobi-overlays-batch186-macrolot3-wf-dd13300.json)
- `2026-05-08 00:14:52` [validation-2026-05-08-midday-durability-neighbors-batch187-macrolot3-wf-dd13300.json](results/validation-2026-05-08-midday-durability-neighbors-batch187-macrolot3-wf-dd13300.json)
- `2026-05-08 00:14:48` [validation-2026-05-08-morning-calendar-overlays-batch185-macrolot3-wf-dd13300.json](results/validation-2026-05-08-morning-calendar-overlays-batch185-macrolot3-wf-dd13300.json)
- `2026-05-04 08:30:00` [portfolio-research-2026-05-04-macro-followup-rerun-summary.json](results/portfolio-research-2026-05-04-macro-followup-rerun-summary.json)
- `2026-05-04 08:27:21` [validation-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun-macrolot3-dd13300.json](results/validation-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun-macrolot3-dd13300.json)
- `2026-05-04 08:26:32` [portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json](results/portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json)
- `2026-05-04 08:26:32` [portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json](results/portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json)
- `2026-05-04 08:25:29` [validation-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun-macrolot3-dd13300.json](results/validation-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun-macrolot3-dd13300.json)
- `2026-05-04 08:24:40` [portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun.json](results/portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun.json)
