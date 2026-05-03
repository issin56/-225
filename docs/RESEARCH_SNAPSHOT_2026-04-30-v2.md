# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three targeted validation batches plus a structural bundle rerun/validation block, and ingested exactly six official JPX market videos for `2026-04-30` JST.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `58` minutes
- research batches completed: `4`
- stopped before 50 minutes: `no`
- blocker: `n/a`
- best candidate tested: `lot3-base10-night-exsq-rerun`

## Batch 1: Night Control Refresh

- files:
  - `results/validation-2026-04-30-night-control-batch58-wf-dd13300.json`
- result:
  - the live structural-baseline night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` again cleared `4/4` accepted walk-forward windows at `+53400` total test profit and `11400` worst test drawdown
  - the `ex_sq` control also cleared `4/4` windows at `+51550` total test profit while reducing worst walk-forward drawdown to `7650`, making it the strongest repair candidate for a structural bundle rerun
  - the `only_1_7` defensive control degraded to `3/4` accepted windows and the `ex_gotobi` / narrow month-mask controls were not reproducible enough to promote

## Batch 2: Opening `ex_sq` Neighbor Refresh

- files:
  - `results/validation-2026-04-30-opening-exsq-neighbors-batch59-wf-dd13300.json`
- result:
  - every opening-April `ex_sq` neighbor remained sparse and failed `0/4` accepted walk-forward windows
  - the best local branch reached only `+4600` total test profit across `8` total test trades with `950` worst test drawdown
  - this confirms the opening-April repair lane remains locally exhausted and should not displace the promoted opening sleeve already used by the source-of-truth leader

## Batch 3: Morning Macro Neighbor Refresh

- files:
  - `results/validation-2026-04-30-morning-macro-neighbors-batch60-wf-dd13300.json`
- result:
  - the current morning sleeve `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` again failed `0/4` accepted windows despite `+20200` aggregate test profit
  - the only acceptable standalone neighbor was `day_morning_short_tue_fri_prev_night_down_tight_stop` at `3/4` accepted windows, `+16800` total test profit, and `7700` worst test drawdown
  - prior bundle evidence still says the Tue/Fri swap weakens the combined portfolio, so no new morning replacement was promoted

## Batch 4: Structural Baseline Night `ex_sq` Rerun

- files:
  - `results/portfolio-research-2026-04-30-lot3-base10-night-exsq-rerun.json`
  - `results/validation-2026-04-30-lot3-base10-night-exsq-dd13300.json`
  - `results/portfolio-diagnostics-2026-04-30-lot3-base10-night-exsq-rerun.json`
  - `results/portfolio-research-2026-04-30-lot3-base10-night-only17-rerun.json`
- result:
  - swapping only the baseline night sleeve to `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` produced `lot3-base10-night-exsq-rerun` with `232900` profit, `10350` max drawdown, `0.58` win rate, and `0` losing months
  - versus `lot3_base10_june_t8`, this improved profit by `+50`, reduced drawdown by `2950`, improved validation total test profit from `129750` to `130200`, and reduced validation worst drawdown from `11500` to `7800`
  - the defensive `only_1_7` rerun preserved zero losing months but fell to `210350` profit, so it is not a promotable alternative
  - this is a validated structural-baseline-relative improvement, but it does not beat the current source-of-truth leader `lot3_night_exsq_source_truth_rerun` on full-sample profit

## Video Intake

- quota status for `2026-04-30`: `complete_exactly_6`
- intake files:
  - `docs/VIDEO_INGEST_2026-04-30.md`
  - `docs/VIDEO_HYPOTHESES_2026-04-30.md`

## Updated Decision

- Keep `lot3_night_exsq_source_truth_rerun` as the current strongest source-of-truth portfolio.
- Keep `lot3_base10_june_t8` as the promoted structural baseline reference.
- Record `lot3-base10-night-exsq-rerun` as the best candidate tested in this run and the new validated structural-baseline repair, but do not promote it over the source-of-truth leader.
- Treat the opening-April `ex_sq` neighbor lane as exhausted and the morning macro neighbor lane as non-promotable for now.
- No commit and no push because this run produced research artifacts and documentation, not a verified repo code improvement that needs publishing.
