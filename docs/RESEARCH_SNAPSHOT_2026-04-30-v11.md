# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run kept `lot3_base10_june_t8` as the structural baseline, completed three targeted single-sleeve validation batches plus two source-truth bundle reruns, and found only one credible follow-up: a source-truth bundle that replaced the primary midday sleeve with `..._looser_trail`. That variant improved walk-forward total test profit while preserving zero losing months and the same full-sample drawdown, but it still finished `1100` below the promoted source-truth full-sample profit, so it is not a promotion.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `9` minutes
- research batches completed: `5`
- stopped before 50 minutes: `yes`
- blocker: `exhausted reproducible work for the current opening/morning/midday neighbor lane after three validation batches and two source-truth bundle reruns`
- best candidate tested: `lot3_source_truth_midday_looser_rerun`

## Batch Notes

- opening neighbors:
  `range_above_100/108/110/112` stayed structurally too sparse, with `0/4` accepted windows across the batch and only `4550-4600` total test profit on the lone positive window.
- morning neighbors:
  the current `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` branch still led the nearby defensive gates; `ex_sq` matched it exactly, while `ex_sq_t16`, `ex_sq_vix_up_02`, and `ex_sq_usdjpy_down_v025` all remained too sparse or weaker on aggregate walk-forward acceptance.
- midday neighbors:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8` again held `4/4` accepted windows at `21550` total test profit, while `..._looser_trail` and `..._time_stop_10` both reached higher total test profit (`23950` and `22750`) but only `3/4` accepted windows.
- bundle reruns:
  `lot3-source-truth-midday-looser-rerun` finished at `235200 / DD 10350 / win_rate 58.63% / losing_months 0` with `134100` total test profit and `4/4` accepted windows, which improved walk-forward over the promoted source-truth bundle (`131150`) but still trailed its full-sample profit (`236300`) by `1100`.
  `lot3-source-truth-midday-t8-rerun` kept `4/4` accepted windows and `132800` total test profit, but full-sample profit collapsed to `211000`, so it is closed.

## Decision

- Keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Carry `lot3_source_truth_midday_looser_rerun` only as the best non-promoted midday follow-up because it still loses the like-for-like full-sample comparison.
- Treat the current opening and morning near-neighbor lane as locally exhausted for now.
- No commit and no push because there was no real improvement.
