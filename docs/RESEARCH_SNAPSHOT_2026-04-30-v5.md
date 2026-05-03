# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three new targeted validation batches plus one night full-sample rerank, and found no locally validated candidate that clearly beats the promoted source-of-truth bundle.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `8` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after the midday retighten rerun only reproduced the prior ordering, the morning month-mask branch remained structurally sparse, and the night extension confirmed that ex_sq_v020 improved single-candidate full-sample profit but still trailed the promoted ex_sq branch on walk-forward total test profit, the reproducible queue for this lane was exhausted; the daily 6-video quota had already been met earlier on 2026-04-30 JST`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`

## Batch 1: Midday Retighten Reproduction

- file: `results/validation-2026-04-30-midday-retighten-batch67-macrolot3-wf-dd13300.json`
- result:
  - `time_stop_8` and `t8` exactly reproduced the earlier 4/4 walk-forward acceptance
  - the higher-profit midday neighbors still only cleared `3/4` accepted windows
  - this lane remains a validated structural neighbor set, not a promotable source-of-truth improvement

## Batch 2: Morning Month-Mask Refresh

- file: `results/validation-2026-04-30-morning-monthmask-batch68-macrolot3-wf-dd13300.json`
- result:
  - `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` kept positive out-of-sample profit but still failed the train trade floor
  - the broader parent and `t8` controls each accepted only `1/4` windows
  - the USDJPY, SP500, and VIX gated variants stayed too sparse to justify any bundle rerun

## Batch 3: Night EXSQ Extension

- file: `results/validation-2026-04-30-night-exsq-extension-batch69-macrolot3-wf-dd13300.json`
- result:
  - the plain month-mask control still led candidate-level walk-forward profit at `53400` with worse drawdown
  - `ex_sq` preserved the tighter walk-forward drawdown profile with `51550` total test profit and `7650` worst test drawdown
  - `ex_sq_ex_gotobi` improved win rate but only accepted `1/4` windows because the train side fell below the trade floor

## Batch 4: Night Full-Sample Rerank

- file: `results/20260430-170721-night-exsq-extension-batch70-macrolot3.json`
- result:
  - `ex_sq_v020` topped the single-candidate full-sample rerank at profit `60300`, max drawdown `9150`, and win rate `0.5752`
  - `ex_sq` followed at profit `57900` with the same `9150` drawdown
  - despite the full-sample edge, `ex_sq_v020` was not promoted because its walk-forward total test profit (`50050`) still trailed the already promoted `ex_sq` branch (`51550`)

## Decision

- keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader
- keep `lot3_base10_june_t8` as the structural baseline
- record `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020` as the best new single-candidate retest from this run, but do not promote it without a clearer walk-forward edge
