# Current Research Status

Generated: `2026-05-03T14:29:03+09:00`

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
- total_test_profit: `133100.0`
- average_test_win_rate: `0.5919`
- worst_test_drawdown: `7800.0`

## Latest Snapshot
- snapshot: [RESEARCH_SNAPSHOT_2026-05-03-v1.md](docs/RESEARCH_SNAPSHOT_2026-05-03-v1.md)

```md
# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted-baseline lane, completed four targeted research batches, and then used the required daily video intake to close the remaining reproducible questions instead of opening a new branch.

The first batch revisited the morning repair lane around `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`, focusing on whether adding `usd_jpy_change` and `exclude_sq` could improve the weak `2026-02` contribution without breaking density. That path remains closed. The base and `ex_sq` variants again produced only `1/4` accepted test windows and `0/4` accepted both windows, while the `usdjpy_down_v025` pair cut trade count even further and never met the train gate. The new information is that the omitted `ex_sq_usdjpy_down_v025` branch is effectively identical to the plain `usdjpy_down_v025` path under the current sample, so there is no hidden morning repair left in this narrow family.

The second batch rechecked the April opening additive sleeve around `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`. That lane is locally exhausted again. The `ex_sq_range_above_108/110/112` variants and the nearby `vix_up_04/06` controls all stayed at `0/4` accepted both windows, and most windows were simply `0` out-of-sample trades. Even the strongest secondary threshold shapes produced just one positive window on tiny samples. That means the current April sleeve remains in the bundle only as a small additive contributor, not as an expandable standalone family.

The third and fourth batches pushed the only reusable night alternatives back into the current six-sleeve leader bundle. `lot3-base10-june-t8-nightplain-middayplain-rerun` raised portfolio walk-forward total test profit to `133950`, above the promoted leader's `133100`, but it also widened full-sample drawdown from `10350` to `13850` and worst test drawdown from `7800` to `11500`, so it is not promotable. `lot3-base10-june-t8-nightv020-middayplain-rerun` stayed clean on drawdown at `10350` and kept `4/4` portfolio acceptance with `7800` worst test drawdown, but it finished at `233450` full-sample profit and `131600` total test profit, both below the promoted leader's `233750` and `133100`. The night `ex_sq` sleeve therefore remains the best like-for-like choice inside the current source-of-truth bundle.

The daily video requirement for `2026-05-03` was completed in this run with exactly six JPX official videos recorded in `docs/VIDEO_INGEST_2026-05-03.md`. The usable hypotheses were all discipline-reinforcing rather than branch-opening: keep rule ideas parameterized, keep micro usage sparse, keep drawdown and margin guardrails hard, keep SQ handling calendar-limited, and keep multi-window robustness above single-scenario wins.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `8` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after four targeted same-lane batches plus six official JPX videos, the remaining reproducible work in this lane was exhausted: morning neighbors still failed density, opening April controls stayed zero-trade or one-window only, night plain required too much extra drawdown, and night v020 remained slightly behind the current leader`
- best candidate tested: `lot3-base10-june-t8-nightv020-middayplain-rerun`
```

## Recent Batch Summaries
- [portfolio-research-2026-05-03-same-lane-followup-summary.json](results/portfolio-research-2026-05-03-same-lane-followup-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; four targeted same-lane batches found no promotable improvement because the morning ex_9_10 repair set still failed trade-density acceptance, the April opening additive controls remained mostly zero-trade out of sample, the night plain bundle improved walk-forward total profit only by accepting a materially wider drawdown, and the cleaner night v020 rerun still finished below the promoted leader on both full-sample profit and portfolio walk-forward totals.`
  best_new_candidate: `lot3-base10-june-t8-nightv020-middayplain-rerun` / profit `233450.0` / DD `10350.0` / win_rate `0.5818`
  baseline: `lot3_base10_june_t8`
- [portfolio-research-2026-05-01-midday-plain-promotion-summary.json](results/portfolio-research-2026-05-01-midday-plain-promotion-summary.json)
  decision: `promote lot3_base10_june_t8_night_exsq_middayplain_rerun as the new source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; four targeted same-lane batches showed that the plain midday main-sleeve swap cleanly beat the prior promoted night_exsq bundle on full-sample profit and portfolio walk-forward totals while preserving zero losing months and the same drawdown ceiling, whereas the June-only midday lane remained too sparse to reopen.`
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

## Recent Result Files
- `2026-05-03 14:28:51` [portfolio-research-2026-05-03-same-lane-followup-summary.json](results/portfolio-research-2026-05-03-same-lane-followup-summary.json)
- `2026-05-03 14:26:04` [portfolio-diagnostics-2026-05-03-lot3-base10-june-t8-nightplain-middayplain-rerun.json](results/portfolio-diagnostics-2026-05-03-lot3-base10-june-t8-nightplain-middayplain-rerun.json)
- `2026-05-03 14:26:04` [portfolio-diagnostics-2026-05-03-lot3-base10-june-t8-nightv020-middayplain-rerun.json](results/portfolio-diagnostics-2026-05-03-lot3-base10-june-t8-nightv020-middayplain-rerun.json)
- `2026-05-03 14:25:56` [validation-2026-05-03-lot3-base10-june-t8-nightplain-middayplain-rerun-dd13300.json](results/validation-2026-05-03-lot3-base10-june-t8-nightplain-middayplain-rerun-dd13300.json)
- `2026-05-03 14:25:56` [validation-2026-05-03-lot3-base10-june-t8-nightv020-middayplain-rerun-dd13300.json](results/validation-2026-05-03-lot3-base10-june-t8-nightv020-middayplain-rerun-dd13300.json)
- `2026-05-03 14:24:47` [portfolio-research-2026-05-03-lot3-base10-june-t8-nightv020-middayplain-rerun.json](results/portfolio-research-2026-05-03-lot3-base10-june-t8-nightv020-middayplain-rerun.json)
- `2026-05-03 14:24:46` [portfolio-research-2026-05-03-lot3-base10-june-t8-nightplain-middayplain-rerun.json](results/portfolio-research-2026-05-03-lot3-base10-june-t8-nightplain-middayplain-rerun.json)
- `2026-05-03 14:23:34` [validation-2026-05-03-opening-april-threshold-batch140-wf-dd13300.json](results/validation-2026-05-03-opening-april-threshold-batch140-wf-dd13300.json)
- `2026-05-03 14:23:29` [validation-2026-05-03-morning-ex910-usdjpy-batch139-wf-dd13300.json](results/validation-2026-05-03-morning-ex910-usdjpy-batch139-wf-dd13300.json)
- `2026-05-01 19:45:58` [portfolio-research-2026-05-01-midday-plain-promotion-summary.json](results/portfolio-research-2026-05-01-midday-plain-promotion-summary.json)
- `2026-05-01 19:42:52` [portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun.json](results/portfolio-diagnostics-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun.json)
- `2026-05-01 19:42:52` [validation-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun-dd13300.json](results/validation-2026-05-01-lot3-base10-june-t8-night-exsq-middaylooser-rerun-dd13300.json)
