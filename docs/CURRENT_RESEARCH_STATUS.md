# Current Research Status

Generated: `2026-05-01T20:07:00+09:00`

## Current Leader
- name: `lot3_base10_june_t8_night_exsq_middayplain_rerun`
- bundle_date: `2026-05-01`
- bundle_mode: `matched result/validation/diagnostics set`
- result: [portfolio-research-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json](results/portfolio-research-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json)
- validation: [validation-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun-dd13300.json](results/validation-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun-dd13300.json)
- diagnostics: [portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json](results/portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json)
- profit: `233750.0`
- max_drawdown: `10350.0`
- win_rate: `0.582`
- trades: `543`
- profitable_months: `26`
- losing_months: `0`
- average_monthly_pnl: `8060.34`

## Leader Candidate Set
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail`

## Weak Months
- `2026-02`: `150.0`
- `2023-09`: `250.0`
- `2024-04`: `1450.0`
- `2024-01`: `1500.0`
- `2024-06`: `2500.0`

## Validation
- tested_windows: `4`
- accepted_both_windows: `4`
- total_test_profit: `133100.0`
- average_test_win_rate: `0.5919`
- worst_test_drawdown: `7800.0`

## Latest Snapshot
- snapshot: [RESEARCH_SNAPSHOT_2026-05-01-v21.md](docs/RESEARCH_SNAPSHOT_2026-05-01-v21.md)

```md
# Research Snapshot 2026-05-01

Current strongest portfolio is now `lot3_base10_june_t8_night_exsq_middayplain_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted-baseline lane, completed four targeted same-lane research batches, and treated the already-complete `2026-05-01` six-video quota as a hard constraint rather than reopening unrelated intake.

The first batch reran the main midday sleeve neighbors around the promoted `...time_stop_10` branch. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` and its equivalent `..._t8` cleared `4/4` walk-forward windows, but that path had already been portfolio-closed earlier in the day because it cut too much full-sample profit when inserted into the live bundle. The fresh information here was that the untied plain `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11` and `..._looser_trail` variants remained dense enough to justify a full-bundle rerun, while `..._tighter_trail` and the shorter hold variants were weaker or window-dependent.

The second batch rechecked the June-only specialist sleeve on the same macro config. That branch is now locally exhausted. Every `only_6` neighbor stayed below the minimum train/test trade gates, several produced zero out-of-sample trades in the latest windows, and none delivered even one accepted walk-forward window. The existing June-only sleeve therefore remains in the bundle only because it is already a tiny additive contributor; it is not a live promotion path on its own and no nearby repair variant deserves a rerun.

The third and fourth batches pushed the two surviving midday main neighbors back into the current six-sleeve bundle. `lot3-base10-june-t8-night-exsq-middayplain-rerun` improved the promoted leader from `232900` to `233750` profit with the same `10350` max drawdown, the same `0` losing months, and stronger portfolio walk-forward totals at `133100` test profit versus the prior leader's `130200`, while keeping worst test drawdown unchanged at `7800`. `lot3-base10-june-t8-night-exsq-middaylooser-rerun` also improved the old leader, but only to `233350`, so it finished behind the plain midday swap on full-sample profit despite a nearly identical walk-forward profile.

Promotion is justified. The new information from this run is not just another closure result: the main midday sleeve had one unclosed same-lane replacement that cleanly beat the promoted leader without paying for the gain through wider drawdown or fresh losing months. By contrast, the June-only branch is now closed again as a sparse control lane, and the already-promoted night `ex_sq`, morning `ex_9_10`, and opening pair remain unchanged inside the new best bundle. The daily video requirement was already satisfied before this block with exactly six official-source videos in `docs/VIDEO_INGEST_2026-05-01.md`, so no additional intake was added.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after four same-lane batches, the remaining reproducible candidates were exhausted for this lane: the June-only midday family stayed below the train/test density gates, time_stop_8 had already been portfolio-closed earlier, and the only new full-bundle challengers plain vs looser were both resolved; the daily 2026-05-01 video quota was already met at exactly six items`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middayplain-rerun`
```

## Recent Batch Summaries
- [portfolio-research-2026-05-01-midday-plain-promotion-summary.json](results/portfolio-research-2026-05-01-midday-plain-promotion-summary.json)
  decision: `promote lot3_base10_june_t8_night_exsq_middayplain_rerun as the new source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; four targeted same-lane batches showed that the plain midday main-sleeve swap cleanly beat the prior promoted night_exsq bundle on full-sample profit and portfolio walk-forward totals while preserving zero losing months and the same drawdown ceiling, whereas the June-only midday lane remained too sparse to reopen.`
  best_new_candidate: `lot3-base10-june-t8-night-exsq-middayplain-rerun` / profit `233750.0` / DD `10350.0` / win_rate `0.582`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-live-sleeve-neighbor-closure-summary.json](results/portfolio-research-2026-05-01-live-sleeve-neighbor-closure-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; three targeted live-sleeve neighbor batches found no promotable improvement because the opening vix_up_05 threshold ladder and the morning ex_9_10 neighbors stayed below trade-density gates while the current night ex_sq sleeve remained the cleanest accepted same-lane choice on the proper usdjpy config.`
  best_new_candidate: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020` / profit `18050.0` / DD `2600.0` / win_rate `0.5619`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-factor-config-refresh-summary.json](results/portfolio-research-2026-05-01-factor-config-refresh-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; six targeted validation batches including factor-config refreshes found no promotable improvement, because the corrected opening and midday factor branches stayed too sparse to clear acceptance while the corrected night fixed-set winner only reconfirmed an already-closed sleeve that prior full-bundle reruns failed to promote.`
  best_new_candidate: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` / profit `18900.0` / DD `3800.0` / win_rate `0.5667`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-leader-expansion-followup-summary.json](results/portfolio-research-2026-05-01-leader-expansion-followup-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; three targeted walk-forward batches plus a fixed-bundle rerun found no promotable improvement, because the opening and morning branches remained sparse or sub-threshold while the only 4/4-accepted midday time-stop swap cut too much full-sample profit without repairing the weakest month.`
  best_new_candidate: `lot3-base10-june-t8-night-exsq-middaytime8-rerun` / profit `208300` / DD `10350` / win_rate `0.5758`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-morning-midday-expansion-summary.json](results/portfolio-research-2026-05-01-morning-midday-expansion-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; three same-lane expansion batches plus a full-bundle rerun found no promotable replacement, because the morning expansions stayed below train/test density or flipped negative OOS while the only non-sparse midday challenger lost too much full-sample profit despite keeping 4/4 walk-forward acceptance.`
  best_new_candidate: `lot3-base10-june-t8-midday-sp500-up-rerun` / profit `193500` / DD `10450` / win_rate `0.5396`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-night-fixedset-reruns-summary.json](results/portfolio-research-2026-05-01-night-fixedset-reruns-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; eight fixed-portfolio reruns across the remaining same-lane night controls failed to produce a challenger that clearly beat the promoted ex_sq leader on combined full-sample drawdown, walk-forward profit, and monthly cleanliness.`
  best_new_candidate: `lot3-base10-june-t8-night-exsq-v020-rerun` / profit `232650.0` / DD `10350.0` / win_rate `0.5799`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-night-lane-closure-summary.json](results/portfolio-research-2026-05-01-night-lane-closure-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; the additional same-lane calendar, prior-session, time-window, and morning-support follow-ups did not produce a challenger that beat the promoted night ex_sq sleeve on combined walk-forward acceptance, profit, and drawdown.`
  best_new_candidate: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_gotobi` / profit `38750.0` / DD `8100.0` / win_rate `0.5719`
  baseline: `lot3_base10_june_t8`

## Recent Result Files
- `2026-05-01 20:06:44` [portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun.json](results/portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun.json)
- `2026-05-01 20:06:43` [validation-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun-dd13300.json](results/validation-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun-dd13300.json)
- `2026-05-01 20:06:37` [portfolio-research-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun.json](results/portfolio-research-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun.json)
- `2026-05-01 20:06:35` [portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json](results/portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json)
- `2026-05-01 20:06:35` [validation-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun-dd13300.json](results/validation-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun-dd13300.json)
- `2026-05-01 20:06:29` [portfolio-research-2026-05-01-midday-plain-promotion-summary.json](results/portfolio-research-2026-05-01-midday-plain-promotion-summary.json)
- `2026-05-01 20:04:42` [portfolio-research-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json](results/portfolio-research-2026-05-01-lot3-base10-june-t8-night-exsq-middayplain-rerun.json)
- `2026-05-01 20:02:36` [validation-2026-05-01-midday-june-neighbors-batch138-wf-dd13300.json](results/validation-2026-05-01-midday-june-neighbors-batch138-wf-dd13300.json)
- `2026-05-01 20:02:34` [validation-2026-05-01-midday-main-neighbors-batch137-wf-dd13300.json](results/validation-2026-05-01-midday-main-neighbors-batch137-wf-dd13300.json)
- `2026-05-01 18:40:41` [portfolio-research-2026-05-01-live-sleeve-neighbor-closure-summary.json](results/portfolio-research-2026-05-01-live-sleeve-neighbor-closure-summary.json)
- `2026-05-01 18:36:43` [validation-2026-05-01-opening-vix05-threshold-batch136-wf-dd13300.json](results/validation-2026-05-01-opening-vix05-threshold-batch136-wf-dd13300.json)
- `2026-05-01 18:36:41` [validation-2026-05-01-night-exsq-neighbors-batch136-wf-dd13300.json](results/validation-2026-05-01-night-exsq-neighbors-batch136-wf-dd13300.json)
- `2026-05-01 18:36:37` [validation-2026-05-01-morning-ex910-neighbors-batch136-wf-dd13300.json](results/validation-2026-05-01-morning-ex910-neighbors-batch136-wf-dd13300.json)
- `2026-05-01 17:38:42` [portfolio-research-2026-05-01-factor-config-refresh-summary.json](results/portfolio-research-2026-05-01-factor-config-refresh-summary.json)
- `2026-05-01 17:38:05` [validation-2026-05-01-midday-factor-refresh-batch135-wf-dd13300.json](results/validation-2026-05-01-midday-factor-refresh-batch135-wf-dd13300.json)
- `2026-05-01 17:38:04` [validation-2026-05-01-opening-sp500vix-range-batch135-wf-dd13300.json](results/validation-2026-05-01-opening-sp500vix-range-batch135-wf-dd13300.json)
- `2026-05-01 17:38:03` [validation-2026-05-01-night-fixedset-refresh-batch135-wf-dd13300.json](results/validation-2026-05-01-night-fixedset-refresh-batch135-wf-dd13300.json)
- `2026-05-01 17:36:42` [validation-2026-05-01-midday-only6-range-batch134-wf-dd13300.json](results/validation-2026-05-01-midday-only6-range-batch134-wf-dd13300.json)
- `2026-05-01 17:36:41` [validation-2026-05-01-opening-sp500vix-range-batch134-wf-dd13300.json](results/validation-2026-05-01-opening-sp500vix-range-batch134-wf-dd13300.json)
- `2026-05-01 17:36:41` [validation-2026-05-01-night-fixedset-refresh-batch134-wf-dd13300.json](results/validation-2026-05-01-night-fixedset-refresh-batch134-wf-dd13300.json)
- `2026-05-01 16:42:12` [portfolio-research-2026-05-01-leader-expansion-followup-summary.json](results/portfolio-research-2026-05-01-leader-expansion-followup-summary.json)
