# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run treated `lot3_base10_june_t8` as the fixed structural baseline, restored the missing local macro inputs again, completed three targeted research batches, and found one narrowly better locally reproducible baseline swap without enough evidence to promote it over either the structural baseline or the stored source-of-truth bundle.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `16` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `after restoring the local macro data files, the next direct source-truth rerun was blocked because the worktree does not define the stored night candidate both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq`
- best candidate tested: `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105`

## Batch 1: Opening Source-Truth Threshold Sweep

- files:
  - `results/20260430-210916-opening-source-truth-threshold-batch80-macrolot3.json`
  - `results/validation-2026-04-30-opening-source-truth-batch80-range105-wf-dd13300.json`
  - `results/validation-2026-04-30-opening-source-truth-batch80-range110-wf-dd13300.json`
- result:
  - `range_above_105` and the current source-truth `range_above_110` tied on standalone full-sample profit at `5700` with `12` trades and `1050` max drawdown
  - both variants remained structurally sparse with only `1` positive OOS window and `0/4` accepted windows, so the opening source-truth branch still behaves as a bundle-only sleeve
  - tighter `115/120` thresholds gave back profit immediately and did not improve robustness

## Batch 2: Baseline Midday Tighter-Trail Bundle Rerun

- files:
  - `results/portfolio-research-2026-04-30-lot3-base10-midday-tighttrail-rerun.json`
  - `results/validation-2026-04-30-lot3-base10-midday-tighttrail-rerun-dd13300.json`
- result:
  - replacing only the midday sleeve with `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_tighter_trail` kept `4/4` accepted walk-forward windows and lifted total test profit to `132100`
  - the same rerun cut full-sample profit to `227100` and widened drawdown to `13850`, which is worse than the `lot3_base10_june_t8` full-sample baseline on both core axes
  - this lane remains a useful control for OOS stability, but not a promotion path

## Batch 3: Baseline Opening Range105 Bundle Rerun

- files:
  - `results/portfolio-research-2026-04-30-lot3-base10-opening-range105-rerun.json`
  - `results/validation-2026-04-30-lot3-base10-opening-range105-rerun-dd13300.json`
- result:
  - swapping only the opening sleeve to `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` produced the best locally reproducible bundle of the run: `236250` profit, `13300` max drawdown, `0` losing months, and `4/4` accepted windows
  - this beat the structural baseline's full-sample profit by `3400` with the same drawdown, but it slightly trailed the baseline walk-forward total test profit (`130700` vs `131150`) and raised worst test drawdown (`10550` vs `7800`)
  - it also remained just below the stored source-of-truth leader at `236300` profit and `10350` max drawdown, so the evidence was not strong enough for promotion

## Reproducibility Blocker

- a direct source-truth bundle rerun could not be executed in this worktree because `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` is referenced by the source-of-truth artifacts but is not present in the local candidate registry
- until that definition mismatch is reconciled, locally reproducible work should continue to treat `lot3_base10_june_t8` as the anchor and compare any near-neighbor swaps against both the structural baseline metrics and the stored source-of-truth bundle

## Decision

- keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader
- keep `lot3_base10_june_t8` as the structural baseline
- record `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` as the best candidate tested this run, but not promoted because the improvement was too marginal and less robust than the existing anchors

## Video Intake Handling

- the daily `2026-04-30 JST` quota of `6` market videos had already been satisfied earlier, so this run did not add a seventh video
- no new video-driven hypotheses were added in this run segment because no new videos were ingested
