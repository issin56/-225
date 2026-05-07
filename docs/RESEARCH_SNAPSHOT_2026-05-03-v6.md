# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block completed five targeted research batches in the same `macro.lot3` promotion lane: three single-sleeve validation batches followed by two fixed-bundle reruns around the only opening-main challengers that survived the single-sleeve gate.

The first batch revisited the opening main sleeve itself rather than the already-thin April secondary add-on. That proved to be the only lane with live same-family movement. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` delivered the highest standalone walk-forward profit at `29,500` with `4/4` accepted both windows, but it did so with `11,950` worst test drawdown. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` was the cleaner challenger: `28,700` total test profit, `4/4` accepted both windows, and only `4,000` worst test drawdown, improving on the incumbent opening main sleeve's `22,550` total test profit at the same `4,000` worst test drawdown.

The second batch narrowed the morning repair lane around `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` to the remaining precision variants: `t16`, `ex_sq_t16`, `usdjpy_down_v025`, and `ex_sq_usdjpy_down_v025`. That family remains closed. Every candidate finished `0/4` accepted both windows. The base sleeve still led the group on total test profit at `20,200`, while the added USDJPY and calendar gates only reduced density further without changing the promotion verdict.

The third batch rechecked the promoted night sleeve against its nearest already-legible neighbors. The raw `...ex_2_5_6_8_9_10_11_12` variant again led on walk-forward profit at `53,400`, but it preserved the same structural problem as before by widening worst test drawdown to `11,400`. The current promoted night `...ex_sq` sleeve stayed the best risk-adjusted choice with `51,550` total test profit, `4/4` accepted both windows, and `7,650` worst test drawdown, while the `v020` retune remained slightly below it and the gotobi exclusions accepted only `1/4` both-window outcomes.

Those results left only two credible bundle-level reruns worth doing. Replacing the current opening main sleeve with `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10` produced the closest challenger: `232,600` full-sample profit, `10,350` full-sample drawdown, `135,450` total portfolio walk-forward test profit, and `7,800` worst test drawdown. That is not promotable because it cuts full-sample profit from `235,600` to `232,600` and reintroduces a losing month (`2024-04` at `-3,000`) even though the walk-forward total ticks slightly higher. The more aggressive `...ex_1_2_6_7_10` bundle pushed walk-forward total test profit to `136,250`, but it failed the downside guardrail outright with `23,900` full-sample drawdown and `11,950` worst test drawdown.

Promotion is not justified. The promoted source-of-truth leader stays `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, and the structural baseline stays `lot3_base10_june_t8`. The best candidate tested in this block was `lot3-base10-june-t8-night-exsq-middayplain-openingmain67810-rerun`, but it remained below the incumbent on full-sample profit and monthly cleanliness, so the leader should not change.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `5`
- stopped before 50 minutes: `yes`
- blocker: `after three same-lane validation batches and two fixed-bundle reruns, the remaining reproducible queue in the promoted macro.lot3 lane was exhausted: the morning precision family still failed density, the night neighbors still lost on risk-adjusted acceptance, and the only viable opening-main swaps failed either full-sample profit or drawdown guardrails`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middayplain-openingmain67810-rerun`
