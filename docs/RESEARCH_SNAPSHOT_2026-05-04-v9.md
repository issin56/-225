# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed four targeted research batches, and still found no promotable improvement.

The first batch reopened the residual morning macro/calendar queue with a six-candidate walk-forward screen: `t16`, `usdjpy_down_v025`, `ex_sq_usdjpy_down_v025`, `sp500_down`, `vix_up_02`, and `ex_sq_vix_up_02`. None cleared the fixed density gate. The best OOS line was `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16` at `4/4` positive test windows and `17900` total test profit, but it still finished `0/4` accepted-both windows with only `30` total test trades. `...usdjpy_down_v025` and `...ex_sq_usdjpy_down_v025` were exact walk-forward twins at `10700` total test profit and `16` total test trades, confirming that the added morning `ex_sq` overlay remains operationally irrelevant even when paired with the USDJPY gate.

The second batch reran the current leader bundle with the night sleeve swapped from `...ex_sq` to `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12_ex_sq_v020`. This was the cleanest fresh bundle challenger of the block, but it still trailed the promoted leader. Full-sample profit slipped from `235600` to `235300`, walk-forward total test profit slipped from `134050` to `132550`, trade count rose from `539` to `546`, and the weakest live month, `2026-02`, stayed stuck at `150`. The v020 threshold therefore added activity without producing a better OOS bundle.

The third batch swapped only the morning sleeve to `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_usdjpy_down_v025`. That version failed decisively at the portfolio level. Full-sample profit fell to `190250`, max drawdown widened to `11350`, the portfolio introduced `2` losing months, walk-forward total test profit dropped to `124550`, and trade count fell to `493`. The weak `2025-02` month collapsed from `7050` to `1600`, so the apparent precision of the USDJPY gate came from stripping out too much profitable morning contribution.

The fourth batch reran the bundle with `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_tighter_trail` replacing the base midday sleeve. This preserved the clean `4/4` accepted-both windows and kept full-sample max drawdown at `10350`, but it still missed the promotion bar. Full-sample profit fell to `229950`, walk-forward total test profit fell to `132200`, and the live weak month `2026-02` again stayed at `150` while `2025-02` softened from `7050` to `5500`. The tighter midday trail improved some already-strong months, but not the ones that matter for promotion.

This closes the fresh same-lane follow-up queue around the promoted leader for now. The remaining untested ideas inside `macro.lot3` are either duplicates of already-proven no-op calendar overlays, stricter sparse gates that already failed density, or bundle swaps already dominated by the promoted source-of-truth leader on both full-sample and fixed-set OOS totals. `docs/VIDEO_INGEST_2026-05-04.md` already contains exactly `6` official-source market video/page intakes for the Tokyo calendar day, so no additional intake was required for this block.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `12` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after screening the remaining fresh morning macro neighbors and rerunning the only three non-duplicate current-bundle swaps with plausible upside, no reproducible macro.lot3 candidate remained that was not already rejected or strictly dominated by the promoted leader`
- best candidate tested: `lot3-base10-june-t8-night-exsqv020-middayplain-openingrange105-rerun`
