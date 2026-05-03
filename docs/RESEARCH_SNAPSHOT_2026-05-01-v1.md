# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three targeted single-sleeve validation batches, three baseline bundle reruns, one structural control rerun, and one source-truth reproduction attempt. The best validated local follow-up was `lot3_base10_night_exsq_rerun`, which slightly improved full-sample profit and materially reduced drawdown versus the structural baseline, but it still trailed the promoted source-of-truth full-sample profit by `3400` and did not repair the weak `2026-02` month. A direct local rerun of the promoted source-truth candidate set remained behaviorally inconsistent, with the night `...ex_sq` sleeve and the opening `...range_above_110` sleeve collapsing to zero trades, so the current lane stops on a concrete configuration or reproducibility mismatch instead of promoting anything new.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `24` minutes
- research batches completed: `8`
- stopped before 50 minutes: `yes`
- blocker: `source-truth candidate set reran with severe local behavior drift, including zero-trade night ex_sq and opening ex_sq_range_above_110 sleeves, so further promotion work is blocked on reproducibility mismatch rather than candidate scarcity`
- best candidate tested: `lot3_base10_night_exsq_rerun`

## Batch Notes

- morning ex_sq follow-up:
  `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq` matched the incumbent exactly, while `..._t16`, `..._usdjpy_down_v025`, and `..._vix_up_02` all weakened acceptance or total test profit.
- night ex_sq follow-up:
  `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` remained the best night branch at `4/4` accepted windows and `51550` total test profit; `..._v020` was slightly weaker and gotobi exclusions degraded stability.
- sparse secondary midday follow-up:
  the secondary `only_6 ... vix_up_02` sleeve stayed structurally sparse, with no candidate reaching `accepted_both_windows > 0`; `..._t8` was the least-bad variant at `3000` total test profit.
- baseline bundle reruns:
  `lot3_base10_night_exsq_rerun` finished at `232900 / DD 10350 / win_rate 58.00% / losing_months 0` with `4/4` accepted windows and `130200` walk-forward total test profit, improving the structural baseline on both full-sample profit and drawdown.
  `lot3_base10_night_exsqv020_rerun` kept the same improved drawdown but slipped to `232650`, making it inferior to plain `ex_sq`.
  `lot3_base10_no_secondary_midday_rerun` collapsed to `221950` with no drawdown benefit, so removing the sparse midday sleeve is closed.
- source-truth local reproduction:
  after restoring missing candidate names and the local external-factors CSV, the promoted source-truth candidate set still reran to only `72200 / DD 4800 / losing_months 2` with `6/7` accepted windows because the night `...ex_sq`, the opening `...ex_sq_range_above_110`, and the secondary midday `..._t8` sleeves all produced zero trades locally.

## Decision

- Keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Carry `lot3_base10_night_exsq_rerun` only as the best locally validated non-promoted candidate.
- Treat the current lane as blocked by source-truth reproducibility mismatch, not by lack of nearby candidates.
- No commit and no push because there was no promotable improvement.
