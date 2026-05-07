# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted `macro.lot3` lane, completed three targeted research batches, and finished with a fixed-bundle rerun only after the best new standalone opening candidate cleared walk-forward acceptance.

The first batch opened the untested midday broad-main branch around `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10_11` and `...ex_1_2_4_9_10`. The outcome was mixed but not promotable. Both main variants finished `3/4` accepted-both walk-forward windows with similar totals, `22000` and `22300` total OOS profit respectively, while the late-window variant also reached `3/4` but lower at `19950`. The range-threshold repairs immediately failed the density gate again, and the decisive problem was the final window: `...ex_1_2_4_9_10` turned negative in `wf_04`, while `..._9_10_11` fell to only `7` OOS trades there. That keeps this branch interesting historically but still below promoted-sleeve reliability.

The second batch revisited the opening family with lighter month exclusions rather than the already-tested wider `...67810` path. That branch produced the strongest standalone candidate of the run. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` finished `4/4` accepted-both windows with `29500` total OOS profit, `0.6196` average test win rate, and `11950` worst test drawdown. The nearby `...ex_1_2_6_10` and `...ex_1_2_10` variants both reached only `3/4`, and the `vix_not_up` / `sp500_down_02` overlays either weakened train acceptance or reduced total OOS materially. That left `...ex_1_2_6_7_10` as the only credible candidate for a bundle-level promotion check.

The third batch performed that bundle-level check by replacing the leader’s opening main sleeve `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10` with `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` while keeping the rest of the promoted set unchanged. The bundle did improve fixed-set walk-forward total test profit slightly, from `134050` to `136250`, and still accepted `4/4` windows. But the tradeoff was not acceptable. Full-sample profit dropped from `235600` to `228000`, losing months worsened from `0` to `1`, and max drawdown jumped from `10350` to `23900`. The worst OOS drawdown also widened from `7800` to `11950`. Under the existing promotion guardrails, that is a clear rejection.

No `2026-05-04` video intake was completed in this run because the environment had no network access, so no primary-source market videos could be retrieved or verified locally. The research lane itself was still reproducible and was carried through three targeted batches plus reconciliation, but video intake was concretely blocked by tooling constraints rather than skipped by choice.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `29` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `network access was unavailable for required video intake, and after three same-lane batches plus one fixed-bundle rerun there was no remaining reproducible promotion path stronger than the incumbent`
- best candidate tested: `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10`
