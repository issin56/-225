# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, detected and corrected a config mismatch against the stored lot3 source-of-truth lane, then completed three corrected validation batches plus three structural bundle reruns.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `19` minutes
- research batches completed: `6`
- stopped before 50 minutes: `yes`
- blocker: `initial reruns were executed against config.backtest-nk225micro.yaml instead of config.backtest-nk225micro.macro.lot3.yaml; after reconciling to the lot3 macro config and reproducing the saved baseline, the remaining corrected queue was exhausted without a promotable improvement`
- best candidate tested: `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail`

## Batch 1: Midday Neighbor Refresh Reconciled To Lot3 Macro Config

- files:
  - `results/validation-2026-04-30-midday-neighbors-batch61-macrolot3-wf-dd13300.json`
- result:
  - the corrected macro-lot3 rerun reproduced the midday lane as active and stable again after the initial config mismatch
  - `time_stop_8` and `t8` were the cleanest corrected neighbors at `4/4` accepted windows, `+21550` total test profit, and `3200` worst test drawdown
  - `looser_trail` and the live `time_stop_10` branch remained strong but slipped to `3/4` accepted windows, while the June-only specialist variants stayed too sparse to matter

## Batch 2: Morning Parent Refresh Reconciled To Lot3 Macro Config

- files:
  - `results/validation-2026-04-30-morning-parent-batch62-macrolot3-wf-dd13300.json`
- result:
  - the corrected macro-lot3 rerun preserved the earlier structure: no morning replacement cleared combined acceptance well enough to reopen promotion
  - `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` and `..._ex_sq` again produced positive OOS pockets but stayed at `0/4` accepted windows because of trade-floor sparsity
  - `ex_gotobi` reduced drawdown somewhat but remained too sparse, and the broader parent / `t8` variants still failed to produce a better replacement

## Batch 3: Opening Parent Refresh Reconciled To Lot3 Macro Config

- files:
  - `results/validation-2026-04-30-opening-parent-batch63-macrolot3-wf-dd13300.json`
- result:
  - the corrected macro-lot3 rerun confirmed the opening specialist branch is still structurally sparse
  - the best `vix_up_05_ex_sq` family members reached only `1` positive test window with `0/4` accepted windows and single-digit total trades
  - this keeps the opening repair lane locally closed unless a future hypothesis changes the structure more materially than threshold nudges

## Structural Bundle Reruns

- files:
  - `results/portfolio-research-2026-04-30-lot3-base10-current-control-macrolot3-rerun.json`
  - `results/portfolio-research-2026-04-30-lot3-base10-midday-time-stop8-macrolot3-rerun.json`
  - `results/portfolio-research-2026-04-30-lot3-base10-midday-looser-macrolot3-rerun.json`
  - `results/portfolio-research-2026-04-30-config-reconciled-midday-followup-summary.json`
- result:
  - the corrected control rerun exactly reproduced the stored structural baseline at `+232850 / DD 13300 / 0 losing months`, confirming the mismatch was purely configuration-related
  - swapping the live midday sleeve to `time_stop_8` cut profit to `+205000` while keeping drawdown only marginally lower, so it is not promotable
  - swapping to `looser_trail` was the least-bad corrected bundle change at `+229800 / DD 13850 / 0 losing months`, but it still trailed baseline profit and breached the baseline drawdown discipline

## Video Intake

- quota status for `2026-04-30`: `already_complete_exactly_6`
- intake files:
  - `docs/VIDEO_INGEST_2026-04-30.md`
  - `docs/VIDEO_HYPOTHESES_2026-04-30.md`

## Updated Decision

- Keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Record `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail` as the best corrected midday challenger tested in this run, but do not promote it because it lost `3050` profit versus baseline and widened drawdown to `13850`.
- Treat the opening parent refresh and the morning parent refresh as locally closed again under the corrected macro-lot3 lane.
- No commit and no push because there was no real improvement and no code change.
