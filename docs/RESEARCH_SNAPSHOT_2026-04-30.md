# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run resumed source-of-truth research from `lot3_opening_april_exsq110_baseline_rerun` and tested a narrow event-filter family on the live morning and live night sleeves. The only promotable branch was the night `exclude_sq` variant, which was strong enough as a standalone candidate to justify a bundle rerun.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- replaced sleeve: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- promoted replacement: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq`

## Batch 1: Event Filter Candidate Walk-Forward

- files:
  - `results/validation-2026-04-30-event-filter-batch57-wf-dd13300.json`
- result:
  - the live morning branch and its `exclude_sq` sibling stayed functionally identical on acceptance and remained too sparse to promote
  - the `exclude_gotobi` morning branch reduced drawdown locally but still failed all combined acceptance gates
  - the live night branch remained strong, and the `exclude_sq` night sibling preserved `4/4` accepted windows while reducing worst OOS drawdown from `11400` to `7650`
  - the `exclude_gotobi` night branch stayed positive but lost too much train stability and finished at only `1/4` accepted windows

## Batch 2: Source-of-Truth Bundle Rerun

- files:
  - `results/portfolio-research-2026-04-30-lot3-night-exsq-source-truth-rerun.json`
  - `results/validation-2026-04-30-lot3-night-exsq-source-truth-dd13300.json`
  - `results/portfolio-diagnostics-2026-04-30-lot3-night-exsq-source-truth-rerun.json`
  - `results/portfolio-research-2026-04-30-event-filter-source-truth-summary.json`
- result:
  - full-sample profit improved from `236250` to `236300`
  - full-sample max drawdown improved from `13300` to `10350`
  - win rate improved from `0.5795` to `0.5824`
  - zero losing months were preserved
  - walk-forward total test profit improved from `130700` to `131150`
  - walk-forward worst test drawdown improved from `10550` to `7800`

## Updated Decision

- Promote `lot3_night_exsq_source_truth_rerun` as the new source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Treat the night `exclude_sq` event filter as a valid improvement because it preserved reproducibility and materially improved drawdown at both the full-sample and OOS levels.
- Drop the current morning `exclude_sq` and `exclude_gotobi` event-filter branches from the immediate queue because they did not clear the acceptance gates.
- Return next to `regime split` and `asymmetric lot` work, since the sparse `April / June` repair lanes remain locally exhausted.
