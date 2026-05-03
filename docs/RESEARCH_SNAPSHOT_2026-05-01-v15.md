# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This follow-up stayed inside the same night-led lane and completed four targeted walk-forward batches before stopping once the reproducible nearby queue was exhausted.

The night calendar batch extended the already-promoted `ex_sq` branch with `ex_gotobi` and `ex_sq_ex_gotobi` controls. Those new variants kept positive out-of-sample profit and acceptable drawdown, but each failed the in-sample trade-density gate and finished at only `1/4` accepted windows. The older raw control `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` again posted the highest walk-forward profit at `53400`, but it still carried the worse `11400` worst test drawdown, so the promoted `..._ex_sq` sleeve remained the cleaner live component at `51550` total walk-forward test profit and `7650` worst test drawdown.

The night prior-session batch locally closed that branch for now. Every candidate finished with `0/4` accepted windows. The best of the set, `both_fast_short_night_prev_day_down_tue_fri_usdjpy_down_tp_v025_ex_2_6_10_11_12`, managed `27200` total test profit, but it still broke the drawdown or profit gates in every train+test window and never approached the promoted night sleeve's robustness.

The time-window batch also failed to create a real challenger. `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12` was the only shape with some life, reaching `2/4` accepted windows, `19450` total test profit, and `12900` worst test drawdown, but that remains well below the promoted night sleeve on acceptance count, profit, and evidence depth. The broader tight-stop controls generated larger raw profit totals only by blowing through the drawdown ceiling.

The final morning support batch confirmed that the `ex_sq`-adjacent morning ideas are still too sparse to matter. Plain `ex_9_10` and `ex_9_10_ex_sq` both produced positive isolated windows and only `6900` worst test drawdown, but they topped out at `1/4` accepted test windows and `0/4` accepted train+test windows. The factor-gated morning add-ons were even sparser.

No promotion is justified. The source-of-truth leader should remain `lot3_base10_june_t8_night_exsq_rerun`, and the next lane should stay tightly focused on night candidates that can match `4/4` acceptance first rather than reopening sparse morning or secondary day branches.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `8` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `same-lane reproducible queue exhausted after four targeted batches; remaining nearby controls were either too sparse or already inferior on acceptance/drawdown`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
