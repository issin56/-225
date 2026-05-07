# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted `macro.lot3` lane, completed three targeted candidate batches plus one fixed-bundle rerun, and finished with the incumbent still ahead on promotion guardrails.

The first batch revisited the promoted-side midday specialist family around `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8`. That entire branch is now effectively closed under the current validation rules. The incumbent sleeve and every nearby variant finished `0/4` accepted-both windows because they remained structurally too sparse. Even the least-bad sibling, `..._t8`, produced only `5` total OOS trades and `3000` total test profit across all windows. This is now a density failure lane, not a near-promotion lane.

The second batch refreshed the night family around the promoted `...ex_sq` sleeve. Standalone, the broad parent `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` actually led on total OOS profit at `53400` with `4/4` accepted-both windows, beating the incumbent sleeve `...ex_sq` at `51550`. But that gain came with a materially wider worst OOS drawdown, `11400` versus `7650`. The `...ex_sq_v020` sibling again trailed both. So this batch reopened one legitimate bundle-swap check, but not a clean standalone promotion.

The third batch attempted to close the morning precision lane more decisively. It succeeded in the negative sense: no morning variant became promotable. `day_morning_short_mon_thu_prev_night_down_tight_stop_t8` reached only `1/4` accepted-both windows, while `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` and its `ex_sq`, `t16`, `usd_jpy`, and `vix` overlays all stayed at `0/4`. This family can still print positive OOS totals in isolated windows, but it does not survive the train-trade-density gate consistently enough to justify a leader-sleeve swap.

The fourth batch executed the only bundle-level rerun justified by the standalone results: replacing the leader's night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` with the broader non-`ex_sq` parent while leaving the other five sleeves unchanged. The fixed-set walk-forward total improved modestly from `134050` to `135100`, average OOS win rate rose from `0.5944` to `0.5957`, and the bundle still accepted `4/4` windows. But the tradeoff remained below promotion standard. Full-sample profit fell from `235600` to `232050`, max drawdown widened from `10350` to `13850`, and worst OOS drawdown worsened from `7800` to `10550`. Monthly cleanliness stayed at `0` losing months, but the drawdown giveback outweighed the small OOS gain, so the night-base swap is rejected.

This run also completed the daily `2026-05-04` video intake with `6` JPX official videos/pages. The accepted hypotheses reinforced the same-lane discipline already reflected in the research: keep micro usage sparse, keep SQ handling explicitly calendar-scoped, reject manual rescue logic, and only advance ideas that can be reduced to deterministic month, session, range, or bundle-level validation rules.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `16` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after three same-lane candidate batches, one justified bundle rerun, and six official video ingests, the remaining promoted-lane queue had no reproducible path that beat the incumbent without violating drawdown guardrails`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
