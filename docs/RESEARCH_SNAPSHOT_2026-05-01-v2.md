# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed six targeted research batches and confirmed a hard local reproducibility mismatch rather than a candidate-ranking problem. The day opening base sleeve `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10` and the primary midday sleeve still validate normally, but the sparse source-truth support sleeves and nearby exploratory branches collapse to zero trades in the current worktree: `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`, the entire `opening ex_sq` ladder, the secondary midday `...mon_wed_vix_up_02[_t8/_t16/_looser_trail]` lane, and the night `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` branch all returned zero trades on full-sample reruns. Because of that drift, even the current-worktree rerun of the structural baseline degraded to `72200 / DD 4800 / losing_months 2`, matching the previously observed source-truth failure shape instead of the promoted baseline artifact.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `26` minutes
- research batches completed: `6`
- stopped before 50 minutes: `yes`
- blocker: `current worktree reruns zero-trade the sparse opening, secondary-midday, and night source-truth sleeves, so bundle promotion is blocked on reproducibility mismatch; video intake was also blocked by lack of network access`
- best candidate tested: `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`

## Batch Notes

- opening ex_sq reproducibility check:
  the entire `opening ex_sq` branch stayed dead locally. `...ex_sq` itself and every tested range gate from `80` through `120`, including the `sp500_down_02` variants and the previously promoted `range_above_110` form, produced `0` trades in all four walk-forward windows.
- secondary midday rerank:
  the whole sparse secondary-midday family also produced `0` trades in all four walk-forward windows, including `...vix_up_02`, `_t8`, `_t16`, `_looser_trail`, and the `us10y_not_up` variants. This means the local drift is not isolated to the opening ex_sq sleeve.
- live sleeve sanity control:
  the current main opening sleeve `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10` still validated cleanly at `4/4` accepted windows with `13650` total test profit, and the primary midday sleeve stayed healthy at `3/4` accepted windows with `14900` total test profit. The morning sleeve remained positive but too sparse on its own.
- full-sample drift confirmation:
  a full-sample `lot3_base10_june_t8` rerun in this worktree dropped to `72200 / DD 4800 / losing_months 2` because `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`, `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`, and `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8` all contributed zero trades.
- video intake:
  no `2026-05-01` video intake was completed because this environment does not currently have network access, so no research-usable hypotheses could be extracted from JPX, SBI, or other market channels.
