# Current Research Status

Generated: `2026-05-04T08:30:16+09:00`

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
- snapshot: [RESEARCH_SNAPSHOT_2026-05-04-v9.md](docs/RESEARCH_SNAPSHOT_2026-05-04-v9.md)

```md
# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed four targeted research batches, and still found no promotable improvement.

The first batch reopened the residual morning macro/calendar queue with a six-candidate walk-forward screen: `t16`, `usdjpy_down_v025`, `ex_sq_usdjpy_down_v025`, `sp500_down`, `vix_up_02`, and `ex_sq_vix_up_02`. None cleared the fixed density gate. The best OOS line was `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16` at `4/4` positive test windows and `17900` total test profit, but it still finished `0/4` accepted-both windows with only `30` total test trades. `...usdjpy_down_v025` and `...ex_sq_usdjpy_down_v025` were exact walk-forward twins at `10700` total test profit and `16` total test trades, confirming that the added morning `ex_sq` overlay remains operationally irrelevant even when paired with the USDJPY gate.

The second batch reran the current leader bundle with the night sleeve swapped from `...ex_sq` to `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`. This was the cleanest fresh bundle challenger of the block, but it still trailed the promoted leader. Full-sample profit slipped from `235600` to `235300`, walk-forward total test profit slipped from `134050` to `132550`, trade count rose from `539` to `546`, and the weakest live month, `2026-02`, stayed stuck at `150`. The v020 threshold therefore added activity without producing a better OOS bundle.

The third batch swapped only the morning sleeve to `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_usdjpy_down_v025`. That version failed decisively at the portfolio level. Full-sample profit fell to `190250`, max drawdown widened to `11350`, the portfolio introduced `2` losing months, walk-forward total test profit dropped to `124550`, and trade count fell to `493`. The weak `2025-02` month collapsed from `7050` to `1600`, so the apparent precision of the USDJPY gate came from stripping out too much profitable morning contribution.

The fourth batch reran the bundle with `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_tighter_trail` replacing the base midday sleeve. This preserved the clean `4/4` accepted-both windows and kept full-sample max drawdown at `10350`, but it still missed the promotion bar. Full-sample profit fell to `229950`, walk-forward total test profit fell to `132200`, and the live weak month `2026-02` again stayed at `150` while `2025-02` softened from `7050` to `5500`. The tighter midday trail improved some already-strong months, but not the ones that matter for promotion.

This closes the fresh same-lane follow-up queue around the promoted leader for now. The remaining untested ideas inside `macro.lot3` are either duplicates of already-proven no-op calendar overlays, stricter sparse gates that already failed density, or bundle swaps already dominated by the promoted source-of-truth leader on both full-sample and fixed-set OOS totals. `docs/VIDEO_INGEST_2026-05-04.md` already contains exactly `6` official-source market video/page intakes for the Tokyo calendar day, so no additional intake was required for this block.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `12` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after screening the remaining fresh morning macro neighbors and rerunning the only three non-duplicate current-bundle swaps with plausible upside, no reproducible macro.lot3 candidate remained that was not already rejected or strictly dominated by the promoted leader`
- best candidate tested: `lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun`
```

## Recent Batch Summaries
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
- [portfolio-research-2026-05-04-midday-overlay-and-opening-upper-threshold-summary.json](results/portfolio-research-2026-05-04-midday-overlay-and-opening-upper-threshold-summary.json)
  decision: `keep lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun as the promoted source-of-truth leader and keep lot3_base10_june_t8 as the structural baseline; three targeted macro.lot3 batches showed that the leader's live midday only_6 overlay family remains too sparse to stand on its own at 0/4 accepted-both windows across every tested neighbor, and the opening-secondary upper-threshold plus VIX-sensitivity ladder also stayed 0/4 accepted-both windows with only one positive OOS window each, so there is no reproducible same-lane promotion path worth a new bundle rerun.`
  best_new_candidate: `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` / profit `None` / DD `None` / win_rate `None`
  baseline: `lot3_base10_june_t8`

## Recent Result Files
- `2026-05-04 08:30:00` [portfolio-research-2026-05-04-macro-followup-rerun-summary.json](results/portfolio-research-2026-05-04-macro-followup-rerun-summary.json)
- `2026-05-04 08:27:21` [validation-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun-macrolot3-dd13300.json](results/validation-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun-macrolot3-dd13300.json)
- `2026-05-04 08:26:32` [portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json](results/portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json)
- `2026-05-04 08:26:32` [portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json](results/portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsq-middaytighter-openingrange105-rerun.json)
- `2026-05-04 08:25:29` [validation-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun-macrolot3-dd13300.json](results/validation-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun-macrolot3-dd13300.json)
- `2026-05-04 08:24:40` [portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun.json](results/portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun.json)
- `2026-05-04 08:24:40` [portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun.json](results/portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsq-middayplain-morningusdjpyv025-openingrange105-rerun.json)
- `2026-05-04 08:23:30` [validation-2026-05-04-lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun-macrolot3-dd13300.json](results/validation-2026-05-04-lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun-macrolot3-dd13300.json)
- `2026-05-04 08:22:41` [portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun.json](results/portfolio-diagnostics-2026-05-04-lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun.json)
- `2026-05-04 08:22:41` [portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun.json](results/portfolio-research-2026-05-04-lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun.json)
- `2026-05-04 08:20:38` [validation-2026-05-04-morning-macro-neighbors-batch184-macrolot3-wf-dd13300.json](results/validation-2026-05-04-morning-macro-neighbors-batch184-macrolot3-wf-dd13300.json)
- `2026-05-04 07:26:52` [portfolio-research-2026-05-04-morning-calendar-closure-summary.json](results/portfolio-research-2026-05-04-morning-calendar-closure-summary.json)
