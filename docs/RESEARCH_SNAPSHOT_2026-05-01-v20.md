# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the same promoted-baseline lane, completed three targeted same-sleeve walk-forward batches, and used the already-ingested `2026-05-01` six-video quota as a constraint rather than reopening unrelated research branches.

The first batch closed the live April opening sleeve neighbors on the correct macro config. `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` and its `ex_sq` / `range_above_105/108/110/112/115` ladder all stayed below the minimum train/test trade gates. The best OOS totals came from the thresholded `...ex_sq_range_above_105` cluster at `4600` total test profit with `950` worst test drawdown, but every variant remained a one-window, sub-density sleeve, so there is still no bundle-eligible replacement for the promoted opening pair.

The second batch revisited the live morning sleeve around `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`. The `ex_sq` form was functionally identical to the live sleeve on this data, confirming there is no hidden SQ edge to unlock there. `ex_gotobi` cut average test drawdown to `1587.5` and stayed positive in all four windows, but it still produced only `23` total test trades and zero accepted windows. The `vix_up_02` and `sp500_down` factor gates were even weaker, turning sparse or negative in sample, so the morning branch remains useful only as the existing in-bundle sleeve.

The third batch checked whether the promoted night `ex_sq` sleeve still dominates its direct ex_sq-family neighbors when run on the proper `usdjpy` config. It does. `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` finished with `4/4` accepted windows, `18550` total test profit, and only `2600` worst test drawdown. `...ex_sq_v020` also cleared `4/4` windows at `18050`, while `...ex_sq_ex_gotobi` dropped to only `1/4` accepted windows despite decent OOS profit. That leaves the current promoted night sleeve structurally preferred inside the bundle, and prior portfolio reruns already closed the `ex_sq_v020` full-bundle path.

No promotion is justified. The new information from this run is a closure result: the live opening and morning sleeves do not have a denser nearby replacement, and within the night ex_sq family the current promoted sleeve remains the cleanest same-lane choice once direct neighbors are tested on the matching factor config. The daily video requirement was already satisfied before this block with exactly six official-source videos in `docs/VIDEO_INGEST_2026-05-01.md`, so no additional intake was added.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `24` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `after three same-lane validation batches, the remaining live-sleeve neighbors were either exact-equivalent duplicates, too sparse to satisfy the train/test trade gates, or already portfolio-closed by prior fixed-bundle reruns; daily video quota for 2026-05-01 had already been met at exactly six items`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq`
