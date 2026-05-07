# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed four targeted research batches, and still found no promotable improvement.

The first batch expanded the opening-main neighbor search around `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10` toward a previous-night-up gate and a wider opening buffer. That did produce one clean alternative: `day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10` finished `4/4` accepted-both windows with `24100` total OOS profit and the lowest worst-window drawdown in the batch at `3550`. Even so, the established `...lb8_buf2_ex_1_2_6_7_8_10` remained the stronger standalone sleeve at `28700` total OOS profit, so the only new bundle-worthy challenger from this lane was the cleaner but weaker `buf4` branch.

The second batch probed whether the sparse midday overlay could be rebuilt around a narrower November-only specialization. That lane failed decisively. All three `only_11_prev_range_above_*` variants and the incumbent `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8` control stayed `0/4` accepted-both windows, with only `300` to `3000` total test profit and too little train/test trade density to support promotion. This closes the idea that the leader's thin midday secondary sleeve can be rescued by moving from June-only to November-only specialization.

The third batch checked whether the opening-secondary family became viable once the previous-night-up gate was combined with the live `only_4` logic. That lane also stayed closed: both `prev_night_up ... only_4` variants and the live control `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` remained `0/4` accepted-both windows. The best total test profit in the batch was just `4600`, and the trade counts were still too sparse to justify any bundle rerun.

Because the first batch did surface one technically clean opening-main alternative, the fourth batch spent the remaining reproducible budget on a fresh fixed-bundle rerun replacing the promoted opening-main sleeve with `day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10`. That rerun failed clearly against the promoted leader. Full-sample profit fell to `215900` from `235600`, max drawdown stayed tied at `10350`, win rate slipped to `0.5725` from `0.5844`, and losing months worsened from `0` to `3`. Walk-forward acceptance remained `4/4`, but total test profit also dropped to `130650` from `134050`, so the cleaner opening sleeve did not convert into a better portfolio.

The promoted leader therefore stays unchanged. The best single candidate tested in this block was `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`, while the best fresh bundle-level candidate tested was `lot3-base10-june-t8-night-exsq-middayplain-openingbuf4-openingrange105-rerun`; neither beat the source-of-truth portfolio on the required quality gates.

The daily `2026-05-04` video quota was already complete before this block closed. `docs/VIDEO_INGEST_2026-05-04.md` still records exactly `6` official-source items, so no additional intake was added.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after expanding the same-lane queue to opening prev_night_up main and secondary neighbors, midday only_11 specialists, and a fresh opening buf4 bundle rerun, the remaining reproducible candidates were exhausted without producing a promotable replacement`
- best candidate tested: `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`
