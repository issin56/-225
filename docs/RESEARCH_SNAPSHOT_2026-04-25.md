# Research Snapshot 2026-04-25

Current strongest portfolio remains `lot3_opening_april_exsq110_baseline_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed four targeted source-truth validation batches, and ingested exactly six official JPX market videos for `2026-04-25` JST after the comparable SBI official page was unavailable due to maintenance.

- promoted source-of-truth leader: `lot3_opening_april_exsq110_baseline_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `27` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `the automation worktree lacked the macro factor data path, so validation had to be rerouted to the source-of-truth workspace; after that, the opening-April and midday-June queues were exhausted as sparse zero-acceptance lanes and the remaining night-session controls still trailed the live night sleeve`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- best new candidate tested: `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12`

## Batch 1: Opening-April SP500/VIX Neighbor Refresh

- files:
  - `results/validation-2026-04-25-opening-april-sp500vix-batch53-wf-dd13300.json`
- result:
  - the live April sleeve `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_110` and every nearby `vix_up_04/05/06` or `sp500_down_02` sibling still failed `4/4` combined walk-forward windows on trade-floor sparsity
  - the best branch remained the already-live `exsq110` sleeve at just `+4600` total test profit, `8` total test trades, and `950` worst test drawdown
  - this confirms the April lane is structurally sparse even after adding the extra SP500 gate, so no bundle rerun was justified

## Batch 2: Midday June Range Refresh

- files:
  - `results/validation-2026-04-25-midday-june-range-batch54-wf-dd13300.json`
- result:
  - the current June specialist `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8` stayed the least-bad variant at `+3000` total test profit, `5` total test trades, and `1350` worst test drawdown
  - wider `prev_range_above_60/75/90` controls either turned negative or remained fully inactive out of sample, while the `us10y_not_up` and `t16` controls stayed even sparser
  - the June-only lane remains too sparse to reopen source-truth bundle work

## Batch 3: Night USDJPY Neighbor Refresh

- files:
  - `results/validation-2026-04-25-night-usdjpy-neighbors-batch55-wf-dd13300.json`
- result:
  - the live night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` again led the group at `4/4` accepted windows, `+53400` total test profit, and `11400` worst test drawdown
  - the nearest month-mask neighbor `ex_2_5_6_8_10_11_12` was still acceptable at `4/4` but trailed at `+48900`, and `only_1_7` dropped to `3/4` accepted windows with much lower total test profit
  - the ungated and `v020` branches remained non-promotable because they flipped negative out of sample and widened drawdown materially

## Batch 4: Night Session Shape Refresh

- files:
  - `results/validation-2026-04-25-night-session-shape-batch56-wf-dd13300.json`
- result:
  - the live night sleeve again stayed best at `4/4` accepted windows and `+53400` total test profit
  - the best new shape was `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12`, which reached `2/4` accepted windows with `+19450` total test profit and `12900` worst test drawdown, but that still fell well short of the live sleeve's reproducibility
  - the front-half variants were not usable repairs: the pure front-half branch stayed at `0/4` accepted windows and the front-half USDJPY branch also failed combined acceptance despite positive pockets

## Video Intake

- quota status for `2026-04-25`: `complete_exactly_6`
- intake files:
  - `docs/VIDEO_INGEST_2026-04-25.md`
  - `docs/VIDEO_HYPOTHESES_2026-04-25.md`

## Updated Decision

- Keep `lot3_opening_april_exsq110_baseline_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Treat the refreshed opening-April SP500/VIX branch and the refreshed June-specialist range branch as locally exhausted because both remained sparse and cleared `0/4` walk-forward windows.
- Keep the live night sleeve as the only source-truth-relevant night branch; `ex_2_5_6_8_10_11_12` remains the closest acceptable neighbor, while the new US-overlap branch stays only as a secondary note because it reached just `2/4` accepted windows.
- No commit and no push because there was no real improvement and no code change.
