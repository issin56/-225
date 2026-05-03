# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, extended the night / morning / opening neighbor queue with a few tight local variants, completed three new validation batches plus one source-truth bundle rerun, and found no promotable improvement.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after the opening finer-range batch reconfirmed structural sparsity, the morning ex_sq combos stayed below the trade floor, and the only credible night follow-up bundle rerun (ex_sq_v020) still trailed the promoted source-of-truth leader on profit at equal drawdown; the reproducible queue for this lane was exhausted`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`

## Batch 1: Opening EXSQ Fine Range Follow-Up

- file: `results/validation-2026-04-30-opening-exsq-finerange-batch64-wf-dd13300.json`
- result:
  - the new `range_above_108` and `range_above_112` variants collapsed into the same sparse April-only path as the existing `105/110/115` cluster
  - no opening candidate cleared a single combined walk-forward window
  - this lane remains closed unless a materially different but still testable opening gate is added later

## Batch 2: Morning EXSQ Combo Follow-Up

- file: `results/validation-2026-04-30-morning-exsq-combos-batch65-wf-dd13300.json`
- result:
  - adding `exclude_sq` on top of the live `ex_9_10`, `t16`, `usd_jpy_down`, and `vix_up_02` variants changed almost nothing in the accepted-window picture
  - `day_morning_short_tue_fri_prev_night_down_tight_stop` remained the only branch with `3/4` accepted windows, but it is already known and did not justify a portfolio swap into the current source-of-truth bundle
  - the new ex_sq combos stayed below the trade floor or too unstable to promote

## Batch 3: Night EXSQ Sensitivity Follow-Up

- file: `results/validation-2026-04-30-night-exsq-sensitivity-batch66-wf-dd13300.json`
- result:
  - the new `ex_sq_v020` variant stayed clean at `4/4` accepted windows with `+50050` total test profit and `7650` worst test drawdown
  - the added `ex_sq_ex_gotobi` branch improved some single-window train scores but only managed `1/4` accepted windows
  - the original `ex_sq` branch still dominated this neighborhood on risk-adjusted walk-forward quality

## Batch 4: Source-Truth Bundle Reconciliation

- file: `results/portfolio-research-2026-04-30-lot3-night-exsq-v020-source-truth-rerun.json`
- result:
  - swapping the promoted night sleeve to `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020` produced `+235750 / DD 10350`
  - that preserved drawdown but still trailed the promoted source-of-truth leader `+236300 / DD 10350`
  - keep `lot3_night_exsq_source_truth_rerun` as the promoted leader and keep `lot3_base10_june_t8` as the structural baseline

## Video Intake

- quota status for `2026-04-30`: `complete_exactly_6`
- no additional intake was required in this run because the daily quota had already been satisfied with official-source JPX videos
