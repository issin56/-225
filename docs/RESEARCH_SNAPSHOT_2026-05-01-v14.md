# Research Snapshot 2026-05-01

Current strongest portfolio is `lot3_base10_june_t8_night_exsq_rerun`, and this run stayed inside that promoted lane while treating `lot3_base10_june_t8` as the structural comparison baseline. It completed three targeted same-lane factor-aware walk-forward batches plus one diagnostic batch after an initial configuration mistake was detected and corrected.

The first pass accidentally used `config.backtest-nk225micro.yaml`, which leaves `runtime.external_factors_csv` unset. That disabled every `usd_jpy_change` and `vix_change` gate, so the night `ex_sq` family and the sparse factor-gated midday and opening families all collapsed to zero-trade results. A follow-up diagnostic batch confirmed the issue was configuration-specific rather than a broader data outage: core day sleeves still reproduced nonzero results, while the promoted night `usd_jpy_change` sleeve stayed dead until the run switched back to `config.backtest-nk225micro.macro.lot3.yaml`.

Once rerun under the correct macro-lot3 config, the night follow-up batch produced the only meaningful live challenger. The current raw profit leader `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` stayed on top at `53400` total walk-forward test profit, but it again carried `11400` worst test drawdown. The promoted live sleeve `..._ex_sq` remained the cleaner bundle component at `51550` total walk-forward test profit with `4/4` accepted windows and only `7650` worst test drawdown. The new `..._ex_sq_v020` retune also finished `4/4` accepted windows and matched the `7650` worst test drawdown, but its walk-forward profit slipped further to `50050`, so it did not justify a bundle rerun.

The midday-secondary batch around `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8` failed on density rather than drawdown. Every variant produced only `2-5` total walk-forward test trades across four windows, and none reached a single accepted window. Even the best OOS profit shape, the current `..._t8` variant, only generated `3000` total walk-forward test profit on `5` trades, which is too sparse to challenge the promoted portfolio.

The opening-secondary batch around `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` failed for the same reason. The cleanest neighbors `..._ex_sq_range_above_105`, `...108`, `...110`, and `...112` showed slightly better sparse-window profit than the plain sleeve, but each stayed at `0/4` accepted windows with only `8` total walk-forward test trades. The plain `...only_4_vix_up_05` variant managed just `1/4` accepted test windows and also remained far too sparse to justify a six-sleeve rerun.

No promotion is justified. The only live same-lane challenger worth considering was `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`, and it failed to beat the current promoted night sleeve on walk-forward profit while offering no drawdown improvement. The source-of-truth leader should remain `lot3_base10_june_t8_night_exsq_rerun`, and the next same-lane research should keep focusing on night variants with comparable acceptance and drawdown rather than reopening the sparse midday-secondary or opening-secondary branches.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `56` minutes
- research batches completed: `4`
- stopped before 50 minutes: `no`
- blocker: `none`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`
