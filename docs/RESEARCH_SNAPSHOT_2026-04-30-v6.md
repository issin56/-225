# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three new targeted validation batches plus one morning bundle rerun, and found no locally validated candidate that clearly beats the promoted source-of-truth bundle.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `17` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `the initial worktree was missing the required macro factor CSV and latest ex_sq candidate definitions, so the run had to move to the source-root environment; after that correction, the opening ex_sq low-range branch remained structurally empty, the alternative night lane stayed inferior to the promoted ex_sq sleeve, and the only credible morning replacement degraded both full-sample and walk-forward portfolio totals, exhausting the reproducible queue for this lane; the daily 6-video quota had already been met earlier on 2026-04-30 JST`
- best candidate tested: `day_morning_short_tue_fri_prev_night_down_tight_stop`

## Batch 1: Opening EXSQ Low-Range Sweep

- file: `results/validation-2026-04-30-opening-exsq-lowrange-batch71-macrolot3-wf-dd13300.json`
- result:
  - lowering the `exclude_sq` opening range gate from `110` down to `80/90/100` did not unlock usable walk-forward density
  - the paired `SP500 down + VIX up` versions stayed equally sparse
  - this opening branch remains non-promotable because every tested variant still accepted `0/4` windows

## Batch 2: Morning Weekday vs Month-Mask Sweep

- file: `results/validation-2026-04-30-morning-weekday-monthmask-batch72-macrolot3-wf-dd13300.json`
- result:
  - `day_morning_short_tue_fri_prev_night_down_tight_stop` led the batch with `3/4` accepted windows and `16800` total test profit
  - `day_morning_short_mon_thu_ex_gotobi_tight_stop` accepted `2/4` windows but finished with `-8050` total test profit and a `25250` worst test drawdown
  - the month-mask variants (`ex_9_10`, `ex_1_2_10`, `ex_1_2_6_10`) still failed train/test density or flipped negative in key windows

## Batch 3: Night Alternative Lane Sweep

- file: `results/validation-2026-04-30-night-altlane-batch73-macrolot3-wf-dd13300.json`
- result:
  - the promoted `ex_sq` sleeve still led this lane with `51550` total test profit and `4/4` accepted windows
  - `only_1_7` was the best fresh alternative but still reached only `3/4` accepted windows and `30150` total test profit
  - prior-session, front-half, overlap, and USDJPY+US10Y variants either breached drawdown, stayed too sparse, or lost outright

## Batch 4: Morning Bundle Swap Rerun

- files:
  - `results/portfolio-research-2026-04-30-lot3-night-exsq-morning-tuefri-rerun.json`
  - `results/validation-2026-04-30-lot3-night-exsq-morning-tuefri-rerun-dd13300.json`
- result:
  - replacing only the source-of-truth morning sleeve with `day_morning_short_tue_fri_prev_night_down_tight_stop` kept `4/4` accepted windows but reduced walk-forward total test profit from `131150` to `127950`
  - the same swap also cut full-sample profit from `236300` to `199350` and increased losing months from `0` to `5`
  - this confirmed that the stronger single-candidate morning control does not improve the current source-of-truth portfolio bundle

## Decision

- keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader
- keep `lot3_base10_june_t8` as the structural baseline
- record `day_morning_short_tue_fri_prev_night_down_tight_stop` as the best new candidate tested from this run, but do not promote it because the portfolio-level swap degraded both full-sample and walk-forward performance
