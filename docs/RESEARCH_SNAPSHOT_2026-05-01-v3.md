# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed five meaningful research steps after the prior drift check: three targeted walk-forward batches for live opening, live midday, and dead night neighbors, plus two local alive-only portfolio recompositions. The live opening lane improved materially with `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` and `...ex_1_2_6_7_8_10`, the live midday lane improved on test profit with `...looser_trail` and on drawdown with `...time_stop_8`, and the entire non-`ex_sq` night family stayed at `0` trades in all four walk-forward windows. That means the current local lane is still blocked by the night reproducibility gap, so no promotion is justified even though the alive-only recompositions beat the degraded current-worktree baseline rerun.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `10` minutes
- research batches completed: `5`
- stopped before 50 minutes: `yes`
- blocker: `after three targeted validation batches and two portfolio recompositions, the reproducible local lane was exhausted because every non-ex_sq night neighbor still zero-traded locally; video intake was also blocked by lack of network access`
- best candidate tested: `lot3_base10_local_alive_a_rerun`

## Batch Notes

- opening live-neighbor rerank:
  `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` led the opening batch on total test profit at `20600`, while `...ex_1_2_6_7_8_10` followed at `19800`; both beat the current opening control's `13650`. The `vix_not_up` branches stayed fully dead with `0` trades.
- midday live-neighbor rerank:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail` posted the highest total test profit at `16150`, while `...time_stop_8` and `...t8` were the only variants to accept `4/4` windows with lower drawdown and `13800` total test profit. The current control `...time_stop_10` remained at `3/4` accepted windows.
- night reproducibility check:
  every tested non-`ex_sq` night neighbor returned `0` trades in all four walk-forward windows: `...tp_v020`, `...tp`, `...ex_2_6_10_11_12`, `...ex_2_5_6_8_10_11_12`, and `...ex_2_5_6_8_9_10_11_12`. The local drift is therefore still concentrated in the night lane.
- alive-only local recomposition A:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail` + `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` + `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` reran at `78500 / DD 11950 / losing_months 2` and validated `4/4` windows with `45700` total test profit, but it still trails the promoted source-truth bundle badly and inherits the opening sleeve's April/August weakness.
- alive-only local recomposition B:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` + `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` + `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` reran at `69350 / DD 4050 / losing_months 2` and validated `4/4` windows with `42050` total test profit. It is cleaner on drawdown than A, but weaker on profit and still well below the promoted source-truth bundle.
- video intake:
  no `2026-05-01` video intake was completed because this environment does not currently have network access, so the required six JPX/SBI/primary-source videos could not be retrieved and no new testable hypotheses were added.
