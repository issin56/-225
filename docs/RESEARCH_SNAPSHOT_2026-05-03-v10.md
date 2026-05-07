# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted `macro.lot3` lane, completed four targeted research batches, and used the remaining reproducible same-lane queues to close weak branches rather than opening a new family.

The first batch rechecked the fragile midday secondary family around the incumbent `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8`. The answer was negative. Every sibling finished `0/4` accepted-both walk-forward windows. The incumbent itself produced only one positive test window and only `3000` total OOS profit from `5` total OOS trades, while broader mon/wed and mon/thu repairs slid to flat or negative total test profit. That confirms this sleeve is usable only as a narrow historical add-on, not as an active optimization lane.

The second batch tested whether the opening April overlay could be rescued by requiring both `SP500 down` and `VIX up` before the existing SQ/range filters. It could not. Every variant from the plain SP500/VIX gate through `range_above_120` finished `0/4` accepted-both windows. The best threshold variant, `...ex_sq_range_above_110`, generated only `4050` total test profit across all windows and did so from a single positive window, with zero OOS trades in the other three windows. That closes the opening secondary queue again on the same sparsity grounds as before.

The third batch refreshed the credible night-family neighbors. The result stayed aligned with the current promoted bundle. `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` remained the best standalone sleeve at `4/4` accepted windows, `51550` total test profit, and `7650` worst test drawdown. The closest new challenger, `...ex_sq_v020`, also accepted `4/4` windows but finished lower at `50050` total test profit, while `...ex_sq_ex_gotobi` fell to only `1/4` accepted-both windows and `...only_1_7` reached only `3/4`. Because the full-bundle `nightv020` rerun had already trailed the source-of-truth leader earlier in the day, there was no justified promotion path left here.

The fourth batch retried morning precision repairs around `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`. That lane also remained closed. The base rule and all repair variants finished `0/4` accepted-both windows. Several variants posted positive OOS totals, but none met the train-density and OOS trade-count gates together; the base `...ex_9_10` reached `20200` total test profit yet accepted only one test window, and the filtered variants became even sparser. The usable conclusion is that morning precision still helps full-sample bundle diversification but is not currently a live standalone optimization branch.

No new video intake was added in this run because `docs/VIDEO_INGEST_2026-05-03.md` already recorded exactly six official-source videos for the JST day. The net result is further closure, not expansion: the remaining reproducible same-lane queues were exercised across four targeted batches, and none produced a promotable challenger to the current leader.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `55` minutes
- research batches completed: `4`
- stopped before 50 minutes: `no`
- blocker: `none; four reproducible same-lane queues were completed and none left a credible promotion path that justified another fixed-bundle rerun`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`
