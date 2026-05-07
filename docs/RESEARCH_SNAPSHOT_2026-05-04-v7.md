# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed four targeted research batches, and still found no promotable improvement.

The first batch tested the highest-upside dual swap left in the queue: replacing the current night sleeve with `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` and the opening-main sleeve with `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10`. That combination did push fixed-set walk-forward total test profit up to `136950`, above the promoted leader's `134050`, so it was the best fresh challenger on OOS headline profit. It still failed the quality gate decisively. Full-sample profit fell to `230800`, max drawdown exploded from `10350` to `23900`, `2024-04` turned into a `-2050` month, and the weakest live concern `2026-02` remained stuck at `150`. The added OOS profit therefore came from taking substantially more heat rather than improving stability.

The second batch asked whether the cleaner `nightbase` sleeve could work only when paired with the steadier `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_t8` midday branch, while keeping the current opening sleeves unchanged. That bundle was the cleanest of the block on stability: it preserved `0` losing months, kept `4/4` accepted portfolio windows, and reduced worst fixed-set OOS drawdown to `10550`. Even so, the profit damage was too large to justify promotion. Full-sample profit dropped to `206850`, total test profit slipped to `133850`, and the weakest month set was effectively unchanged because `2026-02` stayed at `150` and `2023-09` stayed at `250`.

The third batch paired the current night `ex_sq` sleeve with the same `middaytime8` plus `openingmain6710lite` dual swap. That path failed even harder on seasonality. Full-sample profit fell to `194300`, max drawdown widened to `24700`, losing months increased to `2`, and a new August problem appeared with `2024-08 = -6150`. Although fixed-set walk-forward total test profit remained acceptable at `135000`, the portfolio only got there by accepting a much worse weak-month profile than the promoted leader.

Because that left one meaningful same-lane combination unexplored, the fourth batch closed the queue with the full triple-swap bundle: `nightbase + middaytime8 + openingmain6710lite` alongside the unchanged morning and opening-secondary sleeves. That rerun also stayed `4/4` accepted both windows and reached `136050` total test profit, but it still underperformed the leader on every promotion-defining stability metric that mattered: full-sample profit was only `200950`, max drawdown widened to `23250`, `2024-04` fell to `-2050`, and `2026-02` again stayed at `150`. At this point the remaining reproducible pairwise and triple-swap bundle space around the promoted leader is exhausted.

The promoted leader therefore stays unchanged. The best candidate tested in this block was `lot3-base10-june-t8-nightbase-openingmain6710lite-openingrange105-rerun`, because it produced the highest fresh fixed-set OOS total, but it was still not close to promotable once drawdown, losing months, and weak-month behavior were included. No new video intake was needed: `docs/VIDEO_INGEST_2026-05-04.md` already contains exactly `6` market-related items for the Tokyo calendar day.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `31` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after exhausting the remaining reproducible pairwise and triple-swap bundle compositions around nightbase, middaytime8, and openingmain6710lite, every same-lane candidate either widened drawdown materially, introduced losing months, or left the weak 2026-02 month unrepaired`
- best candidate tested: `lot3-base10-june-t8-nightbase-openingmain6710lite-openingrange105-rerun`
