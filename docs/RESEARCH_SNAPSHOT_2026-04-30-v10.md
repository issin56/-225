# Research Snapshot 2026-04-30

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`.

This run treated `lot3_base10_june_t8` as the fixed structural baseline, restored the local macro inputs, completed five targeted research batches, and found two locally validated but still non-promotable bundle follow-ups: one that improved walk-forward while collapsing full-sample profit, and one that slightly beat the source-truth full-sample profit only by reintroducing a losing month and wider drawdown.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `59` minutes
- research batches completed: `5`
- stopped before 50 minutes: `no`
- blocker: `none`
- best candidate tested: `lot3_base10_nightex2568101112_opening105_rerun`

## Batch Notes

- opening neighbors:
  `range_above_105/110/115/120` and nearby `vix_up_04/06` variants all stayed too sparse on standalone walk-forward validation; the best group still finished at `0/4` accepted windows and `4600` total test profit.
- midday neighbors:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` and the equivalent `..._t8` both held `4/4` accepted windows with `21550` total test profit, while the live `time_stop_10` stayed slightly higher on test profit at `22750` but slipped to `3/4`.
- night neighbors:
  the current baseline night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` remained the cleanest candidate at `4/4` accepted windows and `53400` total test profit; `ex_2_5_6_8_10_11_12` held `4/4` but trailed at `48900`, and `only_1_7` dropped to `3/4`.
- bundle rerun, midday stability tilt:
  `lot3_base10_middayt8_opening105_rerun` improved walk-forward to `133850` total test profit with `4/4` accepted windows, but full-sample profit collapsed to `206850`, so it is not a promotion path.
- bundle rerun, night profit challenger plus opening105:
  `lot3_base10_nightex2568101112_opening105_rerun` reached `237450` full-sample profit, but drawdown widened to `15450`, it created `2024-09 -1050`, and walk-forward total test profit fell to `126200`, so it still does not clear the promoted source-of-truth bundle.

## Decision

- Keep `lot3_night_exsq_source_truth_rerun` as the promoted source-of-truth leader.
- Keep `lot3_base10_june_t8` as the structural baseline.
- Keep the opening `range105` April sleeve and the night `ex_2_5_6_8_10_11_12` branch as local challengers only; neither is promotable.
- No commit and no push because there was no real improvement.
