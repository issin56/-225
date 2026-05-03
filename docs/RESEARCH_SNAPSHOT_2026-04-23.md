# Research Snapshot 2026-04-23

Current strongest portfolio is `lot3_opening_april_exsq110_baseline_rerun`.

This run kept the promoted `lot3_base10_june_t8` structure intact except for one targeted April sleeve replacement. The new bundle swaps `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` for `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_110` and clears the same portfolio walk-forward gate with slightly better aggregate performance.

- prior baseline: `lot3_base10_june_t8`
- prior baseline file: `results/portfolio-research-2026-04-09-lot3_base10_june_t8.json`
- promoted candidate file: `results/portfolio-research-2026-04-23-lot3-opening-april-exsq110-baseline-rerun.json`
- promoted validation: `results/validation-2026-04-23-lot3-opening-april-exsq110-dd13300.json`
- promoted diagnostics: `results/portfolio-diagnostics-2026-04-23-lot3-opening-april-exsq110-baseline-rerun.json`

## Batch 1: Morning Neighbor Recheck

This batch revisited the month-2-capable morning sleeve because `2026-02` still depends entirely on `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`.

- validation file: `results/validation-2026-04-23-morning-ex910-neighbor-candidates-dd13300.json`

Key findings:
- the baseline morning sleeve remained the least-bad branch, but still failed full walk-forward acceptance because train windows stayed under the `30`-trade floor
- `t16`, `vix_up_02`, `sp500_down`, and `usdjpy_down_v025` all reduced trade count further and did not improve the weak `2026-02` dependency shape
- no morning neighbor justified a bundle replacement

## Batch 2: April Opening Neighbor Recheck

This batch targeted the sparse April-only opening sleeve because it is isolated, testable, and close to the existing leader.

- validation file: `results/validation-2026-04-23-opening-april-neighbors-dd13300.json`

Key findings:
- the best nearby branch was `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_110`
- standalone acceptance was still sparse, but it showed the cleanest April-only shape and the best follow-on bundle candidate
- nearby `ex_sq_range_above_105`, `ex_sq_range_above_115`, and `sp500_down_02` variants did not beat the `ex_sq_range_above_110` branch

## Batch 3: Full-Bundle Confirmation

The best April opening neighbor was inserted into the six-sleeve portfolio and rerun against the source-of-truth baseline configuration.

- result file: `results/portfolio-research-2026-04-23-lot3-opening-april-exsq110-baseline-rerun.json`
- diagnostics file: `results/portfolio-diagnostics-2026-04-23-lot3-opening-april-exsq110-baseline-rerun.json`
- validation file: `results/validation-2026-04-23-lot3-opening-april-exsq110-dd13300.json`
- summary file: `results/portfolio-research-2026-04-23-lot3-opening-april-promotion-summary.json`

Key findings:
- promoted candidate: `+236,250 / DD 13,300 / win_rate 57.95% / trades 566`
- prior baseline: `+232,850 / DD 13,300 / win_rate 57.72% / trades 570`
- delta vs prior baseline: `+3,400 profit / +0 drawdown / +0.23pp win_rate / -4 trades`
- walk-forward stayed `4/4` accepted windows and improved test summary from `129,750` to `130,700` total test profit
- average test win rate improved from `58.60%` to `58.82%`
- worst test drawdown improved from `11,500` to `10,550`
- `2026-02` stayed at `+150`, so the weakest month was not repaired, but the replacement still improved total portfolio quality without adding any losing month
- `2024-04` softened slightly from `+1,450` to `+1,400`, but `2025-04` improved from `+23,800` to `+25,700` and `2025-06` improved from `+5,800` to `+7,350`

Updated decision:
- Promote `lot3_opening_april_exsq110_baseline_rerun` over `lot3_base10_june_t8`.
- Treat `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_110` as the new April sleeve.
- Keep further exploration focused on true weak-month repair, especially `2026-02`, not on reopening the night sleeve.
- Keep the local worktree reproduction blocker in mind, but use the OneDrive research root as the source-of-truth environment for bundle promotion until that worktree drift is fixed.
- No commit and no push because there was no code change in this run.

Video intake handling:
- `docs/VIDEO_INGEST_2026-04-23.md` already records exactly `6` official-source videos for the JST day, so no extra intake was added in this run.

## Batch 4: Morning Replacement Recheck Under Bundle Drift

This batch revisited the `2026-02` repair path with a tighter focus on the morning sleeve family nearest to `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`.

- research checkpoint: `results/20260423-060010-2026-04-23-morning-ex910-neighbors-batch2.json`
- validation file: `results/validation-2026-04-23-morning-repair-batch2-dd13300.json`
- summary file: `results/portfolio-research-2026-04-23-lot3-morning-replacement-drift-closure-summary.json`

Key findings:
- raw single-candidate performance still favored `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`, but it again failed full acceptance because train windows stayed below the `30`-trade floor
- the only open-month variants that cleared `2/4` accepted windows were `day_morning_short_mon_thu_prev_night_down_tight_stop` and `day_morning_short_mon_thu_prev_night_down_tight_stop_t16`
- `ex_1_2_10` and `ex_1_2_6_10` are not February repair paths by construction, while `t8` widened losing-month exposure without improving walk-forward acceptance
- the closest local bundle rerun was `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16`, but that comparison stayed invalid for promotion because the OneDrive rerun still showed zero-trade drift in the night sleeve, the June-only midday sleeve, and the April-only opening sleeve
- because of that drift, none of the morning replacement reruns can be compared like-for-like against `lot3_opening_april_exsq110_baseline_rerun`

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted leader.
- Keep `lot3_base10_june_t8` as the structural baseline when evaluating narrow repairs.
- Treat the current blocker as bundle reproduction drift, not as a new local leader search.
- If the drift is fixed later, rerun only the nearest morning replacements first: `day_morning_short_mon_thu_prev_night_down_tight_stop_t16` and `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16`.

## Batch 5: Recent-Window Morning Repair Check and Drift Confirmation

This continuation used the latest train/test split that includes `2026-02` in the test segment and only tested close morning-family neighbors that might still repair the weak month without reopening unrelated sleeves.

- validation file: `results/validation-2026-04-23-morning-recent-window-batch3-dd13300.json`
- bundle rerun file: `results/portfolio-research-2026-04-23-lot3-morning-tuefri-replacement.json`
- leader rerun check: `results/portfolio-research-2026-04-23-lot3-opening-april-exsq110-baseline-rerun-check.json`
- summary file: `results/portfolio-research-2026-04-23-lot3-morning-recent-window-drift-summary.json`

Key findings:
- the best fresh recent-window candidate was `day_morning_short_tue_fri_prev_night_down_tight_stop`, but it still failed acceptance because the latest test window only produced `6` trades despite staying marginally positive at `+150`
- `day_morning_short_mon_thu_ex_gotobi` failed the same recent split outright with `-8000` test profit, so it is not a viable February repair path
- the ex-`9_10` morning branch remained cleaner on a per-trade basis, but it still failed both train and test trade floors on the latest split and did not remove the sparse-trade blocker
- the controlled portfolio insertion for the `tue_fri` candidate was not promotable because the same environment again reproduced `0` trades in the June-only midday sleeve, the promoted night sleeve, and the April-only opening sleeve
- rerunning the current promoted leader in that same environment produced the same zero-trade sleeves, confirming that this is a bundle reproduction blocker rather than evidence of a better morning replacement

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work.
- Do not promote `day_morning_short_tue_fri_prev_night_down_tight_stop`; it is only the least-bad fresh candidate on the latest split, not a validated improvement.
- Treat same-environment bundle drift as the hard blocker before any further portfolio-level replacement tests.

## Batch 6: Morning Tight-Stop Neighbor Expansion

This batch widened the same morning repair family just enough to test whether extra trades could be recovered without abandoning the `prior_night_down` idea.

- research checkpoint: `results/20260423-080214-2026-04-23-morning-tightstop-neighbors-batch4.json`
- validation file: `results/validation-2026-04-23-morning-tightstop-neighbors-batch4-dd13300.json`
- walk-forward file: `results/validation-2026-04-23-morning-tightstop-neighbors-batch4-wf-dd13300.json`

Key findings:
- `day_morning_short_mon_thu_prev_night_down_tight_stop` was the best newly rechecked open-month branch on walk-forward acceptance with `2/4` accepted windows, but it still failed the latest split with only `4` test trades and `+200`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` remained the cleanest per-trade branch and kept all four test windows positive, but it still failed the `30`-trade train floor and only produced `3` trades in the latest test window
- `day_morning_short_mon_thu_tight_stop`, `day_morning_short_mon_thu_ex_gotobi_tight_stop`, `day_morning_short_mon_thu_tight_stop_wider_tp`, and `day_morning_short_mon_thu_tight_stop_fast_exit` did add trades, but they all broke the latest validation window with clearly negative test PnL
- `day_morning_short_mon_thu_prev_night_down_tight_stop_t8` also failed to solve the sparse-trade problem, finishing the latest split at `-700` on `5` trades

## Batch 7: Morning Macro Neighbor Collapse Check

This batch checked whether a narrow macro overlay could rescue the prior-night-down morning family without reopening unrelated sleeves.

- research checkpoint: `results/20260423-080344-2026-04-23-morning-macro-neighbors-batch5.json`
- validation file: `results/validation-2026-04-23-morning-macro-neighbors-batch5-dd13300.json`
- walk-forward file: `results/validation-2026-04-23-morning-macro-neighbors-batch5-wf-dd13300.json`
- summary file: `results/portfolio-research-2026-04-23-lot3-morning-tightstop-macro-closure-summary.json`

Key findings:
- `usd_jpy`, `sp500`, and `vix` gated variants of the `prior_night_down` family all collapsed to `0` trades in both the full-history run and the latest validation split
- because those filters fully switched the sleeve off, they do not qualify as practical `2026-02` repair paths
- the only two surviving branches in this family were still the ungated `prior_night_down` base and the sparse `ex_9_10` branch, so the blocker remains trade density rather than missing macro confirmation

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair evaluation.
- Record `day_morning_short_mon_thu_prev_night_down_tight_stop` as the least-bad newly widened branch, but not a promotion candidate because the latest split still only produced `4` trades.
- Record `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` as the cleanest sparse branch, but not a promotion candidate because it still fails the train and test trade floors.
- Drop macro-gated morning follow-ups from the immediate queue unless the factor data or session logic changes materially.

## Batch 8: FX and Macro-Gated Morning Neighbor Sweep

This batch closed the remaining morning-family branches that were still close enough to the February repair path to justify source-of-truth validation.

- validation file: `results/validation-2026-04-23-morning-fx-macro-neighbors-batch6-dd13300.json`
- walk-forward file: `results/validation-2026-04-23-morning-fx-macro-neighbors-batch6-wf-dd13300.json`

Key findings:
- `day_morning_short_tue_fri_prev_night_down_tight_stop` was the only branch in this sweep to clear the latest `12/4` train-test gate and it also posted `3/4` accepted walk-forward windows with all four test windows positive
- the baseline `ex_9_10`, `ex_9_10_t16`, and `t16` branches still looked cleaner than the broader variants on per-trade quality, but all three remained below the `30`-trade train floor and the `10`-trade latest test floor
- `day_morning_short_mon_thu_prev_night_down_sp500_down_tight_stop`, `day_morning_short_mon_thu_prev_night_down_usd_jpy_down_tight_stop`, `day_morning_short_mon_thu_prev_night_down_usdjpy_down_tight_stop_t025`, and `day_morning_short_mon_thu_prev_night_down_usdjpy_down_tight_stop_v025` all stayed too sparse to qualify as practical repair paths
- because only the `tue_fri` branch was materially different from prior checks, it became the only candidate worth a controlled source-of-truth bundle insertion

## Batch 9: Source-of-Truth Bundle Check for the Tue/Fri Morning Candidate

This batch replaced only the morning sleeve inside the current promoted six-sleeve bundle and reran the portfolio in the OneDrive source-of-truth environment.

- result file: `results/portfolio-research-2026-04-23-lot3-morning-tuefri-source-truth-rerun.json`
- diagnostics file: `results/portfolio-diagnostics-2026-04-23-lot3-morning-tuefri-source-truth-rerun.json`
- validation file: `results/validation-2026-04-23-lot3-morning-tuefri-source-truth-dd13300.json`
- summary file: `results/portfolio-research-2026-04-23-lot3-morning-tuefri-source-truth-closure-summary.json`

Key findings:
- the controlled replacement was not promotable: `+199,700 / DD 13,300 / win_rate 56.64% / trades 602`
- versus the promoted leader, that is `-36,550 profit / +0 drawdown / -1.31pp win_rate / +36 trades`
- profitable months fell from `26` to `24` and losing months rose from `0` to `5`
- the supposed repair target got worse, with `2026-02` moving from `+150` in the leader to `-5,550` in the replacement
- the new morning sleeve introduced additional weak months such as `2023-10 -6,100`, `2024-09 -2,100`, and `2025-10 -150`
- portfolio walk-forward still passed `4/4`, but test summary softened from `130,700` to `128,700` total test profit and worst test drawdown worsened from `10,550` to `11,650`

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work, but do not replace the morning sleeve with `day_morning_short_tue_fri_prev_night_down_tight_stop`.
- Record `day_morning_short_tue_fri_prev_night_down_tight_stop` as a candidate-level pass that fails portfolio-level promotion because it degrades the source-of-truth bundle and worsens `2026-02`.

## Batch 10: Morning T8 Density Recovery Sweep

This follow-up added the smallest still-untested `t8` neighbors around the sparse `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` branch to see whether trade density could recover without reopening unrelated sleeves.

Saved files:
- `results/20260423-110743-2026-04-23-morning-ex910-t8-neighbors-batch8.json`
- `results/validation-2026-04-23-morning-ex910-t8-neighbors-batch8-dd13300.json`
- `results/validation-2026-04-23-morning-ex910-t8-neighbors-batch8-wf-dd13300.json`

Key findings:
- `day_morning_short_tue_fri_prev_night_down_tight_stop_ex_9_10_t8` was the best new branch in this sweep, but still only reached `1/4` accepted walk-forward windows
- `day_morning_short_tue_thu_prev_night_down_tight_stop_ex_9_10_t8` stayed locally cleaner on drawdown (`worst_test_drawdown 2,050`) but remained far too sparse with only `16` total test trades across all four windows
- the direct `ex_9_10_t8` branch improved local trade count versus the original `ex_9_10`, but still missed the train-floor gate badly enough to finish `0/4` accepted walk-forward windows
- `day_morning_short_mon_wed_prev_night_down_tight_stop_ex_9_10_t8` turned negative and is now closed

Interpretation:
- loosening the prior-night threshold to `8` helps local density, but not enough to produce a reliable February-capable morning sleeve
- because the best batch-8 branch still only managed `1/4` accepted windows, no source-of-truth bundle rerun was justified

## Batch 11: Morning Ex-9 / Ex-10 T8 Split Check

This last small batch isolated whether the sparse `ex_9_10` behavior was being driven more by dropping September, dropping October, or by the combined exclusion itself.

Saved files:
- `results/20260423-110906-2026-04-23-morning-ex9-ex10-t8-batch9.json`
- `results/validation-2026-04-23-morning-ex9-ex10-t8-batch9-dd13300.json`
- `results/validation-2026-04-23-morning-ex9-ex10-t8-batch9-wf-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-t8-density-closure-summary.json`

Key findings:
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_t8` was the least-bad new branch with `1/4` accepted walk-forward windows, `total_test_profit 8,100`, and `worst_test_drawdown 2,950`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_10_t8` also only reached `1/4` accepted windows and was materially weaker, including `average_test_win_rate 48.31%`
- neither split solved the structural blocker; both still failed three of four windows on either trade-floor or test-quality grounds
- neither branch justified a controlled portfolio rerun against `lot3_opening_april_exsq110_baseline_rerun`

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repairs.
- Record `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_t8` as the current least-bad unpromoted t8 density branch, but keep it out of the portfolio queue until it can clear more than `1/4` walk-forward windows.
- Treat the morning `t8` density-recovery hypothesis as locally closed for now.

## Batch 12: Weekday-Split Recheck for Ex-9 / Ex-10 T8 Branches

This follow-up reopened the morning `t8` density path only enough to test whether the recovered `ex_9_t8` and `ex_10_t8` branches become viable once the weekday set is narrowed.

Saved files:
- `results/validation-2026-04-23-morning-ex9-ex10-t8-weekdaysplit-batch10-dd13300.json`
- `results/validation-2026-04-23-morning-ex9-ex10-t8-weekdaysplit-batch10-wf-dd13300.json`

Key findings:
- `day_morning_short_tue_thu_prev_night_down_tight_stop_ex_9_t8` was the cleanest new weekday-split branch on drawdown and total test profit, finishing `+9,200` with `worst_test_drawdown 2,050`, but it still cleared `0/4` walk-forward windows because every train segment stayed under the `30`-trade floor
- `day_morning_short_tue_thu_prev_night_down_tight_stop_ex_10_t8` reached `1` accepted test window, but still failed all four windows overall on train sparsity and never became a practical bundle candidate
- both `Mon/Wed` variants degraded sharply and are now locally closed

Interpretation:
- weekday splitting can compress drawdown further, but it does so by collapsing trade density below the minimum needed for promotion
- because batch 12 produced no accepted walk-forward branch, no portfolio rerun was justified

## Batch 13: Tue/Fri Month-Split Recheck Around the Best T8 Branch

This last batch tested whether the previously best `Tue/Fri` density-recovery branch improves if September or October is excluded individually instead of together.

Saved files:
- `results/validation-2026-04-23-morning-tuefri-ex9-ex10-t8-batch11-dd13300.json`
- `results/validation-2026-04-23-morning-tuefri-ex9-ex10-t8-batch11-wf-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-tuefri-ex9-ex10-t8-closure-summary.json`

Key findings:
- `day_morning_short_tue_fri_prev_night_down_tight_stop_ex_9_t8` became the best new branch in this continuation, improving to `2/4` accepted walk-forward windows with `total_test_profit 9,100`, `average_test_win_rate 58.21%`, and `worst_test_drawdown 3,850`
- `day_morning_short_tue_fri_prev_night_down_tight_stop_ex_10_t8` also reached `2/4`, but it was materially weaker with only `4,100` total test profit and an average test win rate below `0.5`
- despite the local improvement, the best new branch still failed the latest `12/4` gate because the current test segment only produced `5` trades, so it remains too sparse for a source-of-truth bundle insertion
- the prior `Mon/Thu ex_9_t8` anchor stayed at `1/4`, so the new `Tue/Fri ex_9_t8` branch is a better local repair candidate but not yet a promotable one

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work.
- Record `day_morning_short_tue_fri_prev_night_down_tight_stop_ex_9_t8` as the current best unpromoted morning `t8` repair branch, but keep it out of the bundle queue until it can clear the latest split with at least `8` test trades.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 14: Source-of-Truth Open-Month Morning Recheck

This follow-up returned to the last two open-month morning candidates that had ever managed `2/4` accepted walk-forward windows and reran them directly in the OneDrive source-of-truth six-sleeve environment.

Saved files:
- `results/portfolio-research-2026-04-23-lot3-morning-base-source-truth-rerun.json`
- `results/portfolio-diagnostics-2026-04-23-lot3-morning-base-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-base-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-t16-source-truth-rerun.json`
- `results/portfolio-diagnostics-2026-04-23-lot3-morning-t16-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-t16-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-openmonth-source-truth-closure-summary.json`

Key findings:
- the earlier reproduction blocker is now resolved in the OneDrive environment, so these bundle reruns are comparable against the promoted leader
- `day_morning_short_mon_thu_prev_night_down_tight_stop` reran cleanly but still fell to `+221,550` with `2` losing months, introducing `2023-10 -6,100` and `2024-09 -2,100` while leaving `2026-02` stuck at `+150`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_t16` was weaker still at `+219,450`, also with `2` losing months, and it reduced `2025-02` from `+7,050` in the leader to `+6,100`
- both replacement bundles still cleared `4/4` portfolio walk-forward windows, but they materially trailed the promoted leader on full-sample profit and monthly stability, so the candidate-level `2/4` acceptance was not enough to justify promotion

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repair work.
- Treat the open-month morning recheck as locally closed for now: it now fails on true source-of-truth bundle quality rather than on reproduction drift.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 15: USDJPY-Gated Night Neighbor Reconciliation

This continuation kept the promoted six-sleeve leader fixed and revalidated only the closest reproducible `both_fast_short_night_tue_fri_usdjpy_down...` neighbors to confirm that the current night sleeve still deserves to stay live after the morning branch was closed again.

Saved files:
- `results/validation-2026-04-23-night-usdjpy-neighbors-dd13300.json`

Key findings:
- the current live night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` remained the best validated neighbor, clearing `4/4` walk-forward windows with `53,400` total test profit and `11,400` worst test drawdown
- the nearest prior challenger `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_10_11_12` also cleared `4/4`, but it trailed on test profit at `48,900` and kept the same `11,400` worst drawdown
- the sparse control `only_1_7` stayed cleaner on drawdown at `7,800`, but only managed `3/4` accepted windows and remained too weak on total test profit at `30,150`
- the open-month `ex_2_6_10_11_12` and plain unfiltered branches remained locally closed because they failed the DD gate or every walk-forward window outright

Interpretation:
- this batch is a reconciliation check, not a promotion branch: it confirms that the promoted leader is already carrying the strongest reproducible USDJPY-gated night sleeve
- because the best validated result is the live sleeve itself, no source-of-truth bundle rerun or promotion change was justified

## Batch 16: Remaining Prev-Day-Down Night Repair Closure

This last batch spent the remaining research block on the still-reproducible `prev_day_down` night repairs because they were the only nearby family that had ever shown a meaningful February-repair shape in earlier work.

Saved files:
- `results/validation-2026-04-23-night-prevday-neighbors-dd13300.json`
- `results/portfolio-research-2026-04-23-night-prevday-v025-ex26101112-single.json`
- `results/portfolio-research-2026-04-23-night-prevday-v025-ex26101112-portfolio.json`
- `results/portfolio-research-2026-04-23-lot3-night-neighbor-closure-summary.json`

Key findings:
- the best remaining reproducible branch was `both_fast_short_night_prev_day_down_tue_fri_usdjpy_down_tp_v025_ex_2_6_10_11_12`, but it still finished `0/4` accepted walk-forward windows, with only `1/4` test windows accepted and `14,250` worst test drawdown
- that same branch produced only `+31,050` on a full-sample single-sleeve rerun with `153` trades, `52.94%` win rate, and `8` losing months
- it did not trade at all in `2026-02`, so it no longer offers even a partial live weak-month repair in the current source-of-truth environment
- the broader `prev_day_down` neighbors were worse still, with lower test profit and even larger drawdown failure

Interpretation:
- the still-reproducible `prev_day_down` family is now locally closed again: it fails current walk-forward acceptance, exceeds the leader drawdown budget, and no longer contributes to the active `2026-02` weak-month problem
- future night work should stay with the current USDJPY-gated live sleeve unless a genuinely new source-of-truth candidate can improve February without reopening broad autumn damage

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repair work.
- Keep the live night sleeve fixed at `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`.
- Treat the remaining reproducible `prev_day_down` night branch as closed.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 17: Broad Macro Morning Source-of-Truth Closure

This follow-up reopened the last broad morning branches that still had any plausible path to improving the active weak month: the wider `usd_jpy_down` and `sp500_down` `Mon/Thu prev_night_down` sleeves rerun directly in the source-of-truth lot3 bundle.

Saved files:
- `results/portfolio-research-2026-04-23-lot3-morning-usdjpydown-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-usdjpydown-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-sp500down-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-sp500down-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-broad-macro-source-truth-closure-summary.json`

Key findings:
- `day_morning_short_mon_thu_prev_night_down_sp500_down_tight_stop` was the best new bundle by full-sample profit, but it still fell to `+191,950 / DD 13,100 / win_rate 57.04% / losing_months 4`
- that `sp500_down` branch did lift `2026-02` from `+150` to `+1,600`, yet it gave back `44,300` of total profit versus the leader and reopened additional weak months including `2023-10 -1,900`, `2024-06 -1,000`, and `2024-09 -400`
- `day_morning_short_mon_thu_prev_night_down_usd_jpy_down_tight_stop` was weaker at `+181,000 / DD 14,100 / win_rate 56.87% / losing_months 3`, exceeded the leader drawdown budget, and failed to trade in `2026-02`
- both replacement bundles still cleared `4/4` portfolio walk-forward windows, so the remaining blocker is true source-of-truth bundle quality rather than local reproducibility

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repair work.
- Treat the broader macro/FX-gated morning replacements as locally closed: they are now reproducible but still too expensive in full-sample profit and month stability for the small February improvement they deliver.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 18: Source-of-Truth Base-Opening Replacement Closure

This continuation used the remaining research block on the only opening-base sleeves that still looked close enough to the promoted leader to justify a direct bundle rerun in the OneDrive source-of-truth environment.

Saved files:
- `results/portfolio-research-2026-04-23-lot3-opening-base-ex1267810-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-opening-base-ex1267810-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-opening-base-buf4-ex1267810-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-opening-base-buf4-ex1267810-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-opening-base-alt-source-truth-closure-summary.json`

Key findings:
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` was the better of the two new bundle swaps at `+229,450 / DD 13,300 / win_rate 57.58% / losing_months 1`
- that `ex_1_2_6_7_8_10` bundle still cleared `4/4` portfolio walk-forward windows and slightly improved aggregate test profit to `131,750`, but it trailed the promoted leader by `6,800` full-sample profit and broke `2024-04` from `+1,400` to `-3,000`
- the same swap effectively crowded out the April-only sleeve, which realized `0` trades inside the combined bundle, so the apparent opening-base gain came from cannibalizing a better April overlay in a worse monthly shape
- `day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10` reduced full-sample drawdown to `11,850`, but it fell to `+219,850`, added `3` losing months, and also left `2026-02` unchanged at `+150`

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repair work.
- Treat broader base-opening replacements as locally closed unless a candidate can preserve April stability without crowding out the April-only sleeve.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 19: Gotobi Overlay Closure

This continuation used the next small targeted block on the remaining explicit calendar-gated overlays because they were still testable, bounded, and had not been reconciled against the current source-of-truth decision trail.

Saved files:
- `results/20260423-171352-2026-04-23-gotobi-overlay-batch12.json`
- `results/validation-2026-04-23-gotobi-overlay-batch12-wf-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-gotobi-overlay-closure-summary.json`

Key findings:
- `day_morning_short_mon_thu_ex_gotobi` and `day_morning_short_mon_thu_ex_gotobi_tight_stop` each managed only `1/4` accepted walk-forward windows and then collapsed badly in the latest `2025-07` to `2025-11` test segment at `-25,250` with `25,250` drawdown
- `day_morning_long_gotobi_tp` was the least-bad full-history branch at `+8,500 / DD 6,550 / win_rate 55.26%`, but it still finished `0/4` accepted walk-forward windows and never became a realistic source-of-truth insertion candidate
- `day_midday_long_gotobi_trail` stayed outright negative on full history at `-17,150`, failed every meaningful quality check, and is now locally closed
- because the best gotobi branch still failed walk-forward and none addressed the live `2026-02` weak month in a robust way, no bundle rerun was justified

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work.
- Treat gotobi overlays as locally closed unless a new candidate can clear walk-forward without reopening large late-2025 damage.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 20: April Neighbor Source-of-Truth Reconciliation

This follow-up spent the next targeted block on the nearest April overlay variants that could still matter in the current lot3 source-of-truth bundle without reopening unrelated local leaders.

Saved files:
- `results/portfolio-research-2026-04-23-lot3-opening-april-exsq105-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-opening-april-exsq105-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-opening-april-exsq115-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-opening-april-exsq115-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-opening-april-sp500down02-vix05-exsq110-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-opening-april-sp500down02-vix05-exsq110-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-opening-april-neighbor-rerun-closure-summary.json`

Key findings:
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` reproduced the promoted bundle exactly at `+236,250 / DD 13,300 / win_rate 57.95% / 566 trades`, with the same `4/4` portfolio walk-forward acceptance and no change to `2026-02 +150`
- that means the looser `105` gate is behaviorally equivalent inside the current bundle, not a genuine improvement, so it does not justify relabeling or promoting away from the already-established `exsq110` leader
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_115` kept `4/4` walk-forward acceptance but slipped to `+233,150`, reduced `2024-04` from `+1,400` to `+450`, cut `2025-01` by `600`, and weakened `2025-06` by `1,550`
- `day_opening_short_range_fade_lb8_buf2_only_4_sp500_down_02_vix_up_05_ex_sq_range_above_110` also kept `4/4` walk-forward acceptance but fell to `+233,600`, reduced `2025-04` from `+25,700` to `+24,600`, weakened `2025-06` by `1,550`, and still left `2026-02` unchanged at `+150`

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work.
- Treat the April `105` threshold as an equivalent duplicate of the promoted `110` bundle, not a new leader.
- Treat the tighter `115` gate and the `sp500_down_02` overlay as locally closed in the current source-of-truth bundle because they preserve validation but give back full-sample quality without repairing the active weak month.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 21: June-Only Midday Specialist Reopen Check

This final targeted block revisited the June-only midday specialist family with the VIX gate removed, because `2024-06` remains a live weak month and the prior specialist variants had mostly collapsed to zero trades.

Saved files:
- `results/20260423-191459-2026-04-23-midday-specialist-batch2.json`
- `results/validation-2026-04-23-midday-specialist-batch2-wf-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-midday-specialist-batch2-closure-summary.json`

Key findings:
- the reopened family did trade again, so the June-only branch is not inert by construction in the source-of-truth environment
- the best full-history branch was `day_midday_long_prev_night_up_trail_only_6_mon_wed_prev_range_above_45` at `+3,700 / DD 3,750 / win_rate 45.16% / 31 trades`
- that same candidate still failed `0/4` walk-forward windows, with `-50` aggregate test profit and no test trades at all in windows 1, 2, and 4
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_thu` behaved similarly but slightly worse, while the all-week and higher-range variants either stayed weaker or collapsed into losing-month behavior

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work.
- Treat the June-only midday specialist family as locally closed for promotion work until a new branch can show live June activity and at least one credible walk-forward acceptance window.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 22: Source-of-Truth Morning Ex-9/10 T8 Bundle Closure

This continuation restored the missing `ex_9_10_t8` morning weekday-split definitions in the local research code, then reran the nearest recovered bundle replacements directly in the OneDrive source-of-truth environment.

Saved files:
- `results/portfolio-research-2026-04-23-lot3-morning-ex910t8-monthu-source-truth-rerun.json`
- `results/portfolio-diagnostics-2026-04-23-lot3-morning-ex910t8-monthu-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-ex910t8-monthu-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-ex910t8-tuethu-source-truth-rerun.json`
- `results/portfolio-diagnostics-2026-04-23-lot3-morning-ex910t8-tuethu-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-ex910t8-tuethu-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-ex910t8-tuefri-source-truth-rerun.json`
- `results/portfolio-diagnostics-2026-04-23-lot3-morning-ex910t8-tuefri-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-morning-ex910t8-tuefri-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-morning-ex910t8-source-truth-closure-summary.json`

Key findings:
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t8` was the least-bad recovered bundle at `+225,550 / DD 13,300 / win_rate 57.75% / losing_months 0`, but it still trailed the promoted leader by `10,700` and left `2026-02` unchanged at `+150`
- `day_morning_short_tue_thu_prev_night_down_tight_stop_ex_9_10_t8` also kept `0` losing months and `4/4` portfolio walk-forward acceptance, but it fell further to `+214,150` and still left `2026-02` stuck at `+150`
- `day_morning_short_tue_fri_prev_night_down_tight_stop_ex_9_10_t8` stayed `4/4` accepted on portfolio walk-forward, yet it is clearly disqualified because it dropped to `+205,600`, created `3` losing months, and turned `2026-02` into `-5,550`
- all three reruns confirm the same point: the recovered `t8` weekday splits are reproducible and locally stable enough to test, but they still do not deliver a real weak-month repair worth promoting

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for narrow repair work.
- Treat the recovered `ex_9_10_t8` weekday-split morning family as source-of-truth validated but locally closed for promotion, because the best branch still loses too much full-sample profit without improving `2026-02`.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 23: June Midday Tail Closure

This continuation used the next targeted block on the only June-only midday specialist neighbors that still looked unresolved after batch 21: the dormant `us10y_not_up` family and the stricter `prev_range_above_60/75/90` thresholds.

Saved files:
- `results/validation-2026-04-23-midday-us10y-neighbors-batch3-dd13300.json`
- `results/validation-2026-04-23-midday-us10y-neighbors-batch3-wf-dd13300.json`
- `results/validation-2026-04-23-midday-range-neighbors-batch4-dd13300.json`
- `results/validation-2026-04-23-midday-range-neighbors-batch4-wf-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-midday-tail-closure-summary.json`

Key findings:
- `day_midday_long_prev_night_up_trail_only_6_mon_wed_prev_range_above_45_us10y_not_up` and its `vix_up_02` / `t8` variants were fully inert in the current source-of-truth environment, producing `0` trades in every train and test window and also `0` trades in the latest `12/4` split
- the stricter range-threshold reopen checks did trade occasionally, but none became viable: `prev_range_above_90` was the least-bad branch at `0/4` accepted walk-forward windows with only `2` total test trades and `-350` total test profit
- `prev_range_above_75` also finished `0/4`, managing only `9` total test trades and `-1,050` total test profit
- `prev_range_above_60` reached `10` total test trades, but only by losing `-1,950` in the `2025-03` to `2025-06` test window and then going back to `0` trades in the latest split
- because the remaining June-only tail neighbors are either inert or negative once they finally trade, no source-of-truth bundle rerun was justified

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repair work.
- Treat the remaining June-only midday tail neighbors as locally closed for promotion work unless factor inputs or the June session definition change materially.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.

## Batch 24: April VIX/Range Neighbor Closure

This continuation spent one targeted batch on the still-untested April-only opening neighbors nearest to the promoted sleeve: `vix_up_04`, `vix_up_06`, and the surrounding `range_above_100/120` controls around the live `range_above_110` path.

Saved files:
- `results/validation-2026-04-23-opening-april-vix-range-batch5-dd13300.json`
- `results/validation-2026-04-23-opening-april-vix-range-batch5-wf-dd13300.json`

Key findings:
- every candidate in this batch remained too sparse for promotion work, finishing `0/4` accepted walk-forward windows and failing the latest `12/4` split on either `no_trades` or the same trade-floor blocker
- `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_04_ex_sq_range_above_110`, the live `vix_up_05_ex_sq_range_above_110`, and `vix_up_06_ex_sq_range_above_110` were behaviorally identical in the source-of-truth candidate validation: each posted `4,600` total test profit, `8` total test trades, and `950` worst test drawdown
- the looser `range_above_100` control added one trade but still stayed below every acceptance floor, while `range_above_120` only reduced train-side activity without improving the live recent-window shape

Interpretation:
- the April-only sleeve remains too sparse for standalone promotion logic, and the nearby VIX threshold tweaks are effectively equivalent inside the currently accessible source-of-truth data
- because this batch produced no new differentiated candidate-level winner, no additional April bundle rerun was justified

## Batch 25: Source-of-Truth Midday Main Neighbor Closure

This follow-up reopened the live midday main sleeve only enough to test the nearest `ex_1_2_4_6_9_10_11` time-stop and trailing-stop neighbors, then reran the lone `4/4` candidate-level winner inside the current six-sleeve source-of-truth bundle.

Saved files:
- `results/validation-2026-04-23-midday-main-neighbors-batch5-dd13300.json`
- `results/validation-2026-04-23-midday-main-neighbors-batch5-wf-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-midday-main-t8-source-truth-rerun.json`
- `results/portfolio-diagnostics-2026-04-23-lot3-midday-main-t8-source-truth-rerun.json`
- `results/validation-2026-04-23-lot3-midday-main-t8-source-truth-dd13300.json`
- `results/portfolio-research-2026-04-23-lot3-midday-main-and-april-vix-closure-summary.json`

Key findings:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` and the equivalent `t8` branch were the only midday-main neighbors to reach `4/4` accepted walk-forward windows, versus `3/4` for the current live `time_stop_10` sleeve
- that apparent candidate-level improvement did not survive bundle interaction: replacing only the midday main sleeve inside the promoted lot3 portfolio cut full-sample profit from `236,250` to `206,850`, while drawdown only improved marginally from `13,300` to `13,250`
- the rerun kept `4/4` portfolio walk-forward acceptance, but total test profit still rose only to `133,850` because the full-sample bundle lost too much realized edge from the swapped midday main sleeve
- the weak live month stayed unchanged at `2026-02 = +150`, and the weaker full-sample result came mainly from the replaced midday sleeve itself falling from `49,800` profit in the leader to `29,050`

Updated decision:
- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline for future narrow repair work.
- Treat the April VIX/range threshold branch as locally closed because the tested neighbors are effectively identical but still too sparse to matter.
- Treat the midday main `time_stop_8` / `t8` rerun as source-of-truth validated but not promotable because the bundle-level profit drop is too large and `2026-02` remains unrepaired.
- Keep daily video intake unchanged because `docs/VIDEO_INGEST_2026-04-23.md` and `docs/VIDEO_HYPOTHESES_2026-04-23.md` already contain exactly `6` JST market videos for the day.
