# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed four targeted research batches, reconciled the best survivor against the already stored bundle evidence, and still found no promotable improvement.

The first two batches closed the April opening-secondary lane more decisively than before. Rechecking the live `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` sleeve against the lower `80/90/100` threshold ladder did not recover density: every variant finished `0/4` accepted-both windows, each with only one positive OOS window and `8-10` total OOS trades. The matching `sp500_down_02` branch also stayed closed. Its best shape, `...ex_sq_range_above_110`, still ended `0/4` accepted-both windows with just `7` total OOS trades. That means the current opening-secondary sleeve remains useful only as a sparse additive bundle component, and there is no lower-threshold or `sp500` reopen path worth carrying forward.

The third batch revisited the main midday family using the `6`-kept branch that had not been refreshed in the current `openingrange105` era. The standalone result was clean but not new. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8` again led on stability at `4/4` accepted-both windows with `21550` total OOS profit and `3200` worst OOS drawdown. Plain `..._ex_1_2_4_6_9_10_11` and `..._looser_trail` again reached slightly higher total OOS profit, `23650-23950`, but only `3/4` accepted-both windows. So the lane ranking is unchanged: `t8` is the cleanest standalone survivor, while the profit-first siblings remain too window-dependent.

The fourth step was result reconciliation rather than another rerun. That was the right stopping point. The same `t8` midday sleeve was already tested inside the current `openingrange105` source-of-truth bundle on `2026-05-03`, and it failed promotion there as well. The fixed-set walk-forward still accepted `4/4` windows, but total OOS profit was only `132800` versus the leader's `134050`, while full-sample profit fell sharply to `211000` from `235600`. Because the best surviving standalone candidate is already bundle-closed under the exact same lane definition, and both opening-secondary branches now re-collapsed to `0/4`, the remaining queue was exhausted without a reproducible promotion path.

The daily `2026-05-04` video quota was already complete before this block closed. `docs/VIDEO_INGEST_2026-05-04.md` still records exactly `6` JPX official videos/pages, so no additional intake was added in order to preserve the exact daily count.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after two low-threshold opening-secondary closure batches, one midday six-kept refresh, and a direct check against the already-rejected openingrange105 midday-t8 bundle rerun, the remaining promoted-lane queue had no untested reproducible path with promotion potential`
- best candidate tested: `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8`
