# Research Snapshot 2026-05-08

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block paused daily video intake and shifted the work back to direct weak-month validation, focused on the current live weak months `2026-02`, `2023-09`, `2024-04`, `2024-01`, and `2024-06`.

The batch tested 22 existing weak-month-relevant candidates through the research report harness:

- output JSON: `results/weak-month-shift-20260508.json`
- checkpoint: `results/20260508-001816-weak-month-shift-20260508.json`
- report directory: `output/weak-month-20260508`

The only candidates that survived the robustness report were the existing morning short family:

- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
  - net profit `46000`
  - trades `64`
  - win rate `0.6719`
  - max drawdown `6900`
  - average monthly pnl `1586.21`
  - test-period net profit `6600`
  - slippage-stressed net profit `36238.02`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16`
  - net profit `40400`
  - trades `60`
  - win rate `0.65`
  - max drawdown `6900`
  - average monthly pnl `1393.10`
  - test-period net profit `6600`
  - slippage-stressed net profit `31210.08`

This did not create a new promotion path. The base morning sleeve is already part of the promoted leader, and the `t16` neighbor was already bundle-checked in the current macro lane and failed to beat the promoted source-of-truth bundle.

The April-only opening sleeve family still helps only in a narrow historical pocket. The best `only_4` variants stayed around `5700` standalone net profit with `1050` drawdown, but the research report rejected them for `one_month_dependency`, `test_period_negative`, and `slippage_sensitive`. The best two-year April gains still came mostly from `2025-04`, so this is not a robust standalone growth lane.

The June-only midday family remained too weak for promotion work. Most variants were rejected for low trade count, one-month dependency, negative test period behavior, or slippage sensitivity. The best-looking June filter was still too sparse, and several variants kept negative `2024-06` / `2025-06` contributions.

The January/July night specialist `both_fast_short_night_tue_fri_usdjpy_down_tp_only_1_7` had decent full-sample net profit at `35100`, but it was rejected for `test_period_negative` and `slippage_sensitive`. It also does not address `2026-02`, `2023-09`, or `2024-04`.

External factor and calendar probes did not uncover a hidden improvement. The SQ/roll exclusions generally removed profitable trades from the surviving morning sleeve: `exclude_sq_week` cut the base morning result from `46000` to `35000`, and `exclude_roll_week` cut it to `39800`. The report therefore does not support adding broad SQ-week or roll-week exclusions to the current morning sleeve.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `2` minutes for the targeted weak-month candidate report
- research batches completed: `1`
- stopped before 50 minutes: `yes`
- blocker: `the existing weak-month candidate set contains no new promotable branch: surviving candidates are already in or near the current bundle, while April/June specialists remain sparse or fragile`
- best candidate tested: `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
