# Research Snapshot 2026-04-24

Current strongest portfolio remains `lot3_opening_april_exsq110_baseline_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three additional targeted parent-refresh validation batches, and left daily video intake unchanged because `2026-04-24` already had exactly six ingested market videos.

- promoted source-of-truth leader: `lot3_opening_april_exsq110_baseline_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `66` minutes
- research batches completed: `3`
- stopped before 50 minutes: `no`
- blocker: `none; the hour budget was used for three targeted parent-refresh batches plus reconciliation and mirroring`
- best candidate tested: `both_fast_short_night_prev_day_down_tp`

## Batch 1: Opening-April Parent Refresh Walk-Forward

- files:
  - `results/validation-2026-04-24-opening-april-parent-batch50-wf-dd13300.json`
- result:
  - the untested parent branch `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` also reproduced as `0` trades across all `4` walk-forward windows
  - that means the current April-only sleeve is structurally sparse at the parent level as well, not just at the already-checked threshold neighbors
  - no opening-April swap justified a bundle rerun

## Batch 2: Morning Hard-Gate Parent Refresh Walk-Forward

- files:
  - `results/validation-2026-04-24-morning-hardgate-batch51-wf-dd13300.json`
- result:
  - `day_morning_short_mon_thu_prev_night_down_tight_stop_t8` was the only live candidate in the family at `+3500` total test profit, `39` total test trades, and `3850` worst test drawdown
  - it still cleared only `1/4` combined walk-forward windows, while the two `usdjpy_down` hard-gate overlays both collapsed to `0` trades in every window
  - because the family remained unstable and mostly inactive, there was no basis for a source-of-truth rerun

## Batch 3: Night Prev-Day Parent Refresh Walk-Forward

- files:
  - `results/validation-2026-04-24-night-prevday-parents-batch52-wf-dd13300.json`
- result:
  - `both_fast_short_night_prev_day_down_tp` was the strongest new parent branch at `+8950` total test profit, `388` total test trades, and `6750` worst test drawdown
  - it still cleared only `1/4` combined walk-forward windows and lost money in the other three, while the `Tue-Fri` subset finished at `-4100` total test profit
  - that is not stable enough to challenge the already-live night sleeve or justify a bundle rerun

## Video Intake

- quota status for `2026-04-24`: `already_complete`
- intake files:
  - `docs/VIDEO_INGEST_2026-04-24.md`
  - `docs/VIDEO_HYPOTHESES_2026-04-24.md`

## Updated Decision

- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Treat the opening-April parent branch as structurally exhausted for now because even the ungated `vix_up_05` parent remained a zero-trade lane.
- Keep the parent-refresh morning and night candidates on record, but do not reopen bundle-level promotion work because their best branches still cleared only `1/4` walk-forward windows.
- No commit and no push because there was no real improvement and no code change.
