# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed five meaningful research steps: a midday primary-neighbor batch, an opening live-neighbor batch, a night tight-control rerun, and two low-drawdown bundle recompositions. The midday primary lane stayed alive and the best local shape shifted to `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8`, which validated `4/4` windows with `13800` total test profit and only `2000` worst test drawdown. The opening live lane also stayed alive: `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` posted the highest standalone walk-forward total at `20600`, while `...ex_1_2_6_7_8_10` was cleaner on average drawdown. The night control batch did not open a new branch; it only reconfirmed that `both_fast_short_night_tight_stop_mon_thu` remains the only nearby night-tight variant that validates `4/4`, while the Tue-Fri prior-day-down controls still flip negative on test.

Returning the strongest midday and opening sleeves to the baseline-style six-sleeve recompositions did not create a promotion path. `lot3_base10_middayt8_opening67810_rerun` finished as the best balanced new bundle at `69350 / DD 4050 / losing_months 2` with `42050` total test profit across `4/4` accepted windows, but it still trails the promoted source-truth leader on headline profit and trails the structural baseline by a very large margin because the baseline night branch again contributed `0` trades in this local recomposition. The more aggressive `lot3_base10_middayt8_opening6710_rerun` kept `4/4` walk-forward acceptance and slightly higher total test profit, but it widened drawdown to `11950` and introduced fresh August weakness inside the opening sleeve. No promotion is justified.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `58` minutes
- research batches completed: `5`
- stopped before 50 minutes: `no`
- blocker: `none`
- best candidate tested: `lot3_base10_middayt8_opening67810_rerun`

## Batch Notes

- midday primary neighbor batch:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8` and `...time_stop_8` were the only midday primary shapes that held `4/4` acceptance, both at `13800` total test profit and `1675` average test drawdown. The former is the cleaner label to carry forward.
- opening live neighbor batch:
  `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` led on raw standalone walk-forward profit at `20600`, but `...ex_1_2_6_7_8_10` stayed materially cleaner on drawdown at `3037.5` average and `4000` worst test drawdown. Macro-gated live neighbors stayed dead with `0` trades.
- night tight control rerun:
  `both_fast_short_night_tight_stop_mon_thu` again validated `4/4` windows with `18750` total test profit. `both_fast_short_night_tight_stop` was weaker at `3/4`, and the Tue-Fri prior-day-down controls remained negative on test.
- baseline recomposition with opening67810:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8` + `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` + `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` + `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` reran at `69350 / DD 4050 / losing_months 2` and validated `4/4` windows with `42050` total test profit. It is the best balanced new bundle this run, but it gives back too much full-sample profit and worsens `2024-04`.
- baseline recomposition with opening6710:
  swapping only the opening sleeve to `...ex_1_2_6_7_10` reran at `69150 / DD 11950 / losing_months 2` and validated `4/4` windows with `42850` total test profit. The extra sleeve-level test profit does not survive portfolio-level drawdown control.
- video intake:
  `2026-05-01` daily quota was already filled earlier today with exactly `6` official-source videos, so no additional video was added in this run segment.
