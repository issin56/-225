# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed three targeted baseline-lane research batches plus result reconciliation. First, the morning replacement lane swapped the base morning sleeve inside the locally reproducible `lot3_base10_june_t8` bundle for three close neighbors. `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16` was the only survivor, finishing `71500 / DD 4600 / losing_months 2` and validating `4/4` windows with `36000` total test profit. The `usdjpy_down_v025` and `vix_up_02` variants effectively killed the bundle by zero-trading the morning, night, and April sleeves and collapsing full-sample profit to `53100`.

Second, the run tested opening-primary replacements without changing the rest of the baseline bundle. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` improved the local baseline rerun to `77600 / DD 4000 / losing_months 2` and validated cleanly across `4/4` windows with `42800` total test profit and `4000` worst test drawdown. The stricter `...vix_not_up` neighbor was unusable in this harness: it produced `0` opening trades and dragged the bundle down to `48650`.

Third, the run checked whether the best morning and opening local improvements stacked cleanly and whether the nearby night `ex_sq_v020` branch could be reintroduced. The combined `lot3_base10_morningt16_opening67810_rerun` finished at `74800 / DD 4000 / losing_months 2`, which is worse than the opening-only swap and therefore not a promotion candidate. The attempted night follow-up hit a concrete reproducibility blocker: the historical result file references `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`, but that candidate name is not defined in the local registry, so the same-lane recomposition cannot be rerun in this worktree.

No promotion is justified. `lot3_base10_opening67810_full_rerun` is the best candidate tested in this run, but it still trails the structural baseline `lot3_base10_june_t8` by a very wide margin on the source-of-truth full sample (`77600` vs `232850`), and the local ex-SQ night follow-up remains blocked by a candidate-name mismatch.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `57` minutes
- research batches completed: `3`
- stopped before 50 minutes: `no`
- blocker: `night ex_sq_v020 candidate name mismatch in local registry after opening-primary and morning-neighbor lanes were exhausted`
- best candidate tested: `lot3_base10_opening67810_full_rerun`

## Batch Notes

- morning replacement bundle batch:
  `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16` held `4/4` windows at `71500 / DD 4600`, while `...usdjpy_down_v025` and `...vix_up_02` both collapsed to `53100` because the substituted sleeves went inert.
- opening primary replacement batch:
  `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` lifted the local baseline rerun to `77600 / DD 4000` with `42800` total walk-forward test profit, while `...vix_not_up` zero-traded and failed the bundle.
- recomposition and blocker batch:
  `lot3_base10_morningt16_opening67810_rerun` landed at `74800 / DD 4000`, below the opening-only improvement, and the night `ex_sq_v020` follow-up could not be rerun because the referenced candidate name is missing locally.
