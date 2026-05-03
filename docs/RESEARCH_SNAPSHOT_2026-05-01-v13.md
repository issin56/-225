# Research Snapshot 2026-05-01

Current strongest portfolio is `lot3_base10_june_t8_night_exsq_rerun`, and this run finally produced a same-lane replacement that clearly beat the promoted structural baseline `lot3_base10_june_t8`.

This run completed three targeted single-sleeve research batches and one justified baseline-lane bundle rerun from the OneDrive source-of-truth workspace. The night batch reopened the live challenger lane: the current night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` remained the top raw walk-forward profit sleeve at `53400` total test profit with `4/4` accepted windows, but the `..._ex_sq` variant also finished `4/4` accepted windows while trimming worst test drawdown from `11400` to `7650`. The `ex_gotobi` and `ex_sq_ex_gotobi` variants stayed positive in all test windows but only managed `1/4` accepted windows because they repeatedly fell under the `min_train_trades=30` guardrail.

The midday-primary batch confirmed the earlier shape ranking without producing a cleaner promotion path than the already tested reruns. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail` led the single-sleeve group with `23950` total walk-forward test profit, and the plain `..._ex_1_2_4_6_9_10_11` variant followed at `23650`, but both remained `3/4` accepted and therefore still trailed the bundle-ready quality bar set by the structural baseline path. The current sleeve `...time_stop_10` stayed the cleanest live member of that lane at `22750` total walk-forward test profit with the lowest average drawdown among the accepted variants.

The opening-primary batch revalidated the same tradeoff seen in older snapshots. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` again led raw single-sleeve walk-forward profit at `29500`, but it also carried `11950` worst test drawdown. The current opening sleeve `...ex_1_2_4_6_7_8_10` remained the cleaner bundle candidate with `22550` total walk-forward test profit, `4/4` accepted windows, and only `4000` worst test drawdown. The broader `ex_1_2_10` and `ex_1_2_6_10` shapes still looked too unstable around the drawdown edge to justify another expensive bundle rerun.

That left one justified full-bundle follow-up: swap only the night sleeve to `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq` while keeping the other five sleeves fixed. The rerun `lot3_base10_june_t8_night_exsq_rerun` reached `232900 / DD 10350 / win_rate 0.58 / trades 550`, versus the structural baseline `232850 / DD 13300 / win_rate 0.5772 / trades 570`. Portfolio walk-forward validation also improved slightly, moving from `129750` to `130200` total test profit while keeping `4/4` accepted windows and cutting worst test drawdown from `11500` to `7800`.

Promotion is justified. The profit gain is only `50`, but it comes with a materially lower full-sample drawdown (`-2950`), a slightly higher walk-forward total (`+450`), the same `4/4` portfolio acceptance, and no new losing month. The source-of-truth leader should therefore advance to `lot3_base10_june_t8_night_exsq_rerun`, while `lot3_base10_june_t8` remains the structural comparison baseline for future same-lane work.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `12` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after three targeted single-sleeve batches, the only justified same-lane bundle rerun produced a promotable night_exsq improvement and no additional unreconciled same-lane rerun remained without repeating already closed opening, morning, or midday branches`
- best candidate tested: `lot3_base10_june_t8_night_exsq_rerun`
