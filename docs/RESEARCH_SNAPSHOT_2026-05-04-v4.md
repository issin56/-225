# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed three targeted research batches, and still found no promotable improvement.

The first two batches re-opened the live midday overlay lane from inside the current leader bundle. That check was necessary because the leader still carries `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8` as a sparse additive sleeve. The result was negative. Every `only_6` neighbor stayed `0/4` accepted-both windows. The exact live sleeve finished with only `5` total OOS trades and `3000` total OOS profit, while the broader `us10y_not_up` and range-threshold variants were even thinner or outright negative. That means the overlay remains bundle-usable only as already-known sparse structure; there is no standalone replacement or stronger same-lane specialist worth promoting.

The third batch revisited the opening-secondary sleeve from the opposite side of the threshold ladder. Lower thresholds had already failed earlier in the day, so this run tested `105/108/110/112/115/120` and VIX `0.4/0.6` sensitivity around the incumbent `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105`. The outcome was flat in the worst way: every upper-threshold and VIX variant again finished `0/4` accepted-both windows with just one positive OOS window and `8` total OOS trades. Several thresholds were effectively identical in OOS behavior, so there is no evidence that the current `openingrange105` sleeve is one parameter turn away from a cleaner promoted component.

Because all three batches collapsed on the validation gate, a new fixed-bundle rerun would have been noise rather than evidence. The promoted leader therefore stays unchanged. The best candidate tested in this block was still the incumbent opening-secondary sleeve `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105`, but it remained non-promotable at `0/4` accepted-both windows, `4600` total OOS profit, and only `8` total OOS trades. The current research queue is now narrower: the same-lane sparse overlay and sparse opening-secondary branches have both been expanded upward and downward without finding a reproducible promotion path.

The daily `2026-05-04` video quota was already complete before this block closed. `docs/VIDEO_INGEST_2026-05-04.md` still records exactly `6` official-source items, so no additional intake was added.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `22` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `after expanding the leader's live midday overlay sleeve and the opening-secondary sleeve across same-lane neighbors, every tested branch remained 0/4 accepted-both windows, leaving no reproducible promotion path worth a fresh bundle rerun`
- best candidate tested: `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105`
