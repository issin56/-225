# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed three targeted research batches from the baseline lane. First, the April-only opening `ex_sq` branch was retested as a standalone sleeve, and `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`, `...ex_sq_range_above_105`, and `...ex_sq_range_above_110` all failed `0/4` walk-forward windows with `0` trades in every train and test slice. That closes the idea that the April sleeve can justify itself independently in the current harness.

Second, those same April `ex_sq` variants were returned to the locally reproducible `lot3_base10_june_t8` bundle. All three reruns collapsed to the exact same output: `72200 / DD 4800 / losing_months 2` with `37150` total test profit across `4/4` accepted windows. The reason is straightforward: the swapped April sleeve again contributed `0` trades, so `plain`, `range_above_105`, and `range_above_110` are operationally identical in this worktree.

Third, the run re-opened the living midday lane by pushing `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8` back into the baseline bundle. `lot3_base10_middayt8_only_rerun` landed at `66050 / DD 4050 / losing_months 2` with `36400` total walk-forward test profit. Pairing that sleeve with the cleaner opening live neighbor `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` produced the best reproducible candidate of the run: `lot3_base10_middayt8_opening67810_rerun` at `69350 / DD 4050 / losing_months 2`, validating `4/4` windows with `42050` total test profit and `4000` worst test drawdown. Replacing the April sleeve with `...ex_sq_range_above_110` did not change the bundle at all because the sleeve stayed inert.

No promotion is justified. `lot3_base10_middayt8_opening67810_rerun` remains far below the structural baseline `lot3_base10_june_t8` on full-sample profit (`69350` vs `232850`) despite clean walk-forward behavior, and the local worktree still cannot reproduce the stored `night_exsq` branch because the candidate name `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` is missing from the local registry. That name mismatch is the concrete blocker that stopped further same-lane recomposition work before a longer run budget.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `14` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `night_exsq candidate name mismatch in local worktree, followed by exhausted reproducible April ex_sq branch with all-zero sleeves`
- best candidate tested: `lot3_base10_middayt8_opening67810_rerun`

## Batch Notes

- opening April ex_sq standalone batch:
  `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`, `...ex_sq_range_above_105`, and `...ex_sq_range_above_110` all failed `0/4` walk-forward windows with `0` total test profit and `0` trades.
- baseline opening ex_sq control batch:
  all three baseline bundle reruns with `plain`, `range_above_105`, and `range_above_110` finished identically at `72200 / DD 4800 / losing_months 2` with `37150` total test profit, confirming that the April sleeve stayed inactive.
- baseline midday t8 recomposition batch:
  `lot3_base10_middayt8_only_rerun` held `4/4` windows at `66050 / DD 4050`, while `lot3_base10_middayt8_opening67810_rerun` improved walk-forward to `42050` total test profit and remained the best balanced reproducible bundle of this run.
