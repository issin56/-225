# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, repaired the local macro-lot3 runtime path mismatch, completed three targeted neighbor batches plus one baseline bundle rerun, and found no locally defined candidate that beat either the structural baseline or the promoted source-of-truth bundle.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `9` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `the first batch failed on a missing local data path, and after restoring the local macro data files the reproducible queue for this lane was exhausted after three focused candidate batches plus one opening-sleeve bundle rerun; no remaining locally defined near-neighbor beat both the structural baseline and the promoted source-of-truth bundle`
- best candidate tested: `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

## Batch 1: Morning Live Macro Neighbors

- files:
  - `results/20260430-200756-morning-live-macro-batch77-macrolot3.json`
  - `results/validation-2026-04-30-morning-live-macro-batch77-ex910-wf-dd13300.json`
  - `results/validation-2026-04-30-morning-live-macro-batch77-ex910t16-wf-dd13300.json`
- result:
  - `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` led the local morning branch on full-sample profit (`46000`) and slightly beat the prior `ex_9_10_t16` walk-forward total (`20200` vs `17900`)
  - both `ex_9_10` and `ex_9_10_t16` still accepted only `2/4` windows because the sparse OOS windows again fell below the trade floor
  - the macro-gated variants (`usd_jpy_down_v025`, `sp500_down`, `vix_up_02`) all lost too much density to matter for bundle promotion work

## Batch 2: Midday Omitted Neighbor Recheck

- files:
  - `results/20260430-200759-midday-omitted-neighbor-batch78-macrolot3.json`
  - `results/validation-2026-04-30-midday-omitted-batch78-time10-wf-dd13300.json`
  - `results/validation-2026-04-30-midday-omitted-batch78-base-wf-dd13300.json`
- result:
  - the omitted parent `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11` slightly beat `time_stop_10` on walk-forward total test profit (`23650` vs `22750`) with the same `2/4` accepted windows
  - neither variant improved enough to reopen promotion because both still failed two windows and trailed the already-promoted full bundle on portfolio-level stability
  - the specialist `only_6...vix_up_02` branch remained structurally sparse at just `9` trades full-sample

## Batch 3: Opening Base Follow-Up

- files:
  - `results/20260430-200758-opening-base-followup-batch79-macrolot3.json`
  - `results/validation-2026-04-30-opening-followup-batch79-ex1267810-wf-dd13300.json`
  - `results/validation-2026-04-30-opening-followup-batch79-ex12467810-wf-dd13300.json`
- result:
  - `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` was the strongest standalone opening sleeve with `38350` full-sample profit, `4/4` accepted windows, `28700` total test profit, and `4000` worst test drawdown
  - the current structural-baseline opening sleeve `ex_1_2_4_6_7_8_10` also stayed `4/4` accepted, but with a weaker `22550` total test profit
  - this was the only branch strong enough to justify a fresh bundle rerun

## Batch 4: Baseline Bundle Rerun With Opening Ex1267810

- files:
  - `results/portfolio-research-2026-04-30-lot3-base10-opening-ex1267810-followup-rerun.json`
  - `results/validation-2026-04-30-lot3-base10-opening-ex1267810-followup-rerun-dd13300.json`
- result:
  - swapping only the opening sleeve to `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` produced `229450` profit, `13300` max drawdown, `1` losing month, and `2024-04 = -3000`
  - the bundle still validated `4/4` windows with `131750` total test profit and `11500` worst test drawdown, but it failed the structural baseline on full-sample profit (`232850`) and monthly cleanliness
  - it remained further behind the promoted source-of-truth leader `lot3_night_exsq_source_truth_rerun` (`236300` profit, `10350` max drawdown)

## Decision

- keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader
- keep `lot3_base10_june_t8` as the structural baseline
- record `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` as the best candidate tested this run, but not promoted because it degraded full-bundle profit and reintroduced a losing month despite strong standalone walk-forward results

## Video Intake Handling

- `CURRENT_RESEARCH_STATUS.md` already indicated that the daily `2026-04-30 JST` quota of `6` market videos had been satisfied earlier, so this run did not ingest additional videos
- no new video-driven hypotheses were added in this run segment because the quota was already met before this worktree session
