# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three targeted neighbor-validation batches plus one source-truth morning swap rerun, and found no locally validated candidate that clearly beats the promoted source-of-truth bundle.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `the reproducible queue for this lane was exhausted after three focused neighbor batches and one portfolio rerun: the new morning candidate improved its own walk-forward total slightly, the night neighbor branch still trailed the promoted ex_sq sleeve, the midday neighbors lost acceptance versus the already-validated retighten branch, and the daily 6-video quota had already been met earlier on 2026-04-30 JST`
- best candidate tested: `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq_t16`

## Batch 1: Morning T16 / EXSQ Neighbor Sweep

- files:
  - `results/20260430-190525-morning-timesweep-batch74-macrolot3.json`
  - `results/validation-2026-04-30-morning-timesweep-batch74-top1-wf-dd13300.json`
  - `results/validation-2026-04-30-morning-timesweep-batch74-top2-wf-dd13300.json`
- result:
  - `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq_t16` led the fresh morning branch on full-sample profit (`40400`) and walk-forward total test profit (`17900`)
  - the simpler `t16` neighbor stayed behind at `14600` total test profit and only `2/4` accepted windows
  - this lane became bundle-worthy for one controlled rerun, but not for direct promotion on single-candidate metrics alone

## Batch 2: Night EXSQ Neighbor Recheck

- files:
  - `results/20260430-190647-night-neighbor-batch75-macrolot3.json`
  - `results/validation-2026-04-30-night-neighbor-batch75-v020-wf-dd13300.json`
  - `results/validation-2026-04-30-night-neighbor-batch75-exgotobi-wf-dd13300.json`
- result:
  - the promoted night sleeve still led the lane at `51550` total test profit from the prior matched validation set
  - `ex_sq_v020` remained close but still lower at `50050` total test profit despite slightly higher full-sample profit (`60300`)
  - `ex_sq_ex_gotobi` accepted `4/4` windows but fell further to `38750`, so it is non-promotable

## Batch 3: Midday Neighbor Recheck

- files:
  - `results/20260430-190813-midday-neighbor-batch76-macrolot3.json`
  - `results/validation-2026-04-30-midday-neighbor-batch76-tight-wf-dd13300.json`
  - `results/validation-2026-04-30-midday-neighbor-batch76-loose-wf-dd13300.json`
- result:
  - the tighter and looser midday trail neighbors improved single-run score or profit, but both dropped to only `2/4` accepted windows
  - `looser_trail` was the best of the pair on walk-forward profit (`23950`) yet still trailed the already-validated retighten branch in acceptance quality
  - the sparse June-only secondary midday sleeve remained unchanged and too thin to justify promotion work

## Batch 4: Source-Truth Morning Swap Rerun

- files:
  - `results/portfolio-research-2026-04-30-lot3-night-exsq-morning-exsqt16-rerun.json`
  - `results/validation-2026-04-30-lot3-night-exsq-morning-exsqt16-rerun-dd13300.json`
- result:
  - replacing only the promoted bundle's morning sleeve with `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq_t16` kept `4/4` accepted windows and nudged walk-forward total test profit from `127950` to `128850` versus the prior morning rerun
  - that swap still failed the source-of-truth bar because full-sample profit landed at `228850`, below the promoted leader's `236300`
  - max drawdown stayed unchanged at `10350`, so the candidate improved neither the leader's profit edge nor its already-validated risk profile

## Decision

- keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader
- keep `lot3_base10_june_t8` as the structural baseline
- record `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq_t16` as the best new candidate tested in this run, but do not promote it because the bundle rerun still underperformed the source-of-truth leader on full-sample profit
