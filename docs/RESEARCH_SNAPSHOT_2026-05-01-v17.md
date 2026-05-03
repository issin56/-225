# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This follow-up reopened the same baseline lane from the promoted six-sleeve bundle, completed three targeted candidate walk-forward batches, and then reran the only locally interesting non-sparse challenger as a fixed portfolio replacement.

The first batch revisited the morning primary family around `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`. The broader month-exclusion and time-stop neighbors all failed to improve the lane: the best headline summary was the ungated base sleeve with only `1/4` accepted windows, while `ex_9_10` kept positive OOS totals in every window but still finished `0/4` accepted because train or test trade counts stayed below the density gate. That means the morning lane still has no replacement that is both active enough and robust enough to justify a bundle rerun on its own.

The second batch expanded the same morning sleeve through macro gates. `...ex_9_10_usdjpy_down_v025` produced the cleanest OOS averages in the batch, but it still ended `0/4` accepted windows with only `29` total train trades across the whole walk-forward set. The other USDJPY, S&P 500, and VIX-gated variants were even sparser or turned negative in one side of the split, so the morning factor branch remains implementationally live but locally too thin for promotion work.

The third batch pushed the midday secondary lane outward. All `only_6 ... vix_up_02` variants stayed structurally sparse, repeatedly landing in `0` out-of-sample trades or single-digit total trades. The only non-sparse survivor was `day_midday_long_prev_night_up_sp500_up_trail`, which reached `2/4` accepted walk-forward windows with `4550` total test profit, enough to justify one full-bundle rerun but not enough to challenge the promoted leader by single-sleeve evidence alone.

That rerun closed the lane. `lot3-base10-june-t8-midday-sp500-up-rerun` preserved `4/4` accepted portfolio windows and a controlled `7800` worst test drawdown, but it dropped full-sample profit to `193500` from the promoted leader's `232900`, increased full-sample drawdown to `10450`, and reintroduced `4` losing months. Diagnostics make the failure mode clear: the inserted `day_midday_long_prev_night_up_sp500_up_trail` sleeve contributed only `18550` total profit and created fresh weak months in `2024-04`, `2025-06`, and `2025-09`, overwhelming the modest robustness it showed in the isolated single-candidate walk-forward.

No promotion is justified. The source-of-truth leader should remain `lot3_base10_june_t8_night_exsq_rerun`, and the next useful work in this lane should come from genuinely new implemented hypotheses rather than more expansion around the already-tested morning or sparse midday branches.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `11` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after three targeted same-lane expansion batches and one full-bundle rerun, the remaining implemented morning and midday branches were either too sparse to satisfy train/test density or materially worse than the promoted leader when inserted into the fixed bundle`
- best candidate tested: `lot3-base10-june-t8-midday-sp500-up-rerun`