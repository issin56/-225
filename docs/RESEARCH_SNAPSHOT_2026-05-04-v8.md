# Research Snapshot 2026-05-04

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted `macro.lot3` lane, completed three targeted research batches, and still found no promotable improvement.

The first batch tested the narrowest possible morning calendar hypothesis: keep the promoted night `...ex_sq`, keep the promoted midday and opening sleeves unchanged, and replace only the morning sleeve with `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq`. That rerun came back bit-for-bit identical to the promoted leader on full-sample and fixed-set walk-forward metrics. Profit stayed `235600`, max drawdown stayed `10350`, accepted portfolio windows stayed `4/4`, and total test profit stayed `134050`. The practical conclusion is that the added morning SQ exclusion is a no-op inside this bundle because no morning trades survive on the dates it would remove.

The second batch tightened the same morning SQ branch with `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_sq_t16`, raising the prior-session down requirement from `12` to `16` ticks while leaving every other sleeve fixed. This was the best fresh challenger of the block, but it still failed the promotion gate. Full-sample profit dropped to `227850`, walk-forward total test profit fell to `131750`, and the weak month that matters most for current stability, `2026-02`, remained stuck at `150`. The stricter morning trigger mainly removed profitable contributions in `2023-12`, `2024-11`, and `2025-02` without repairing any weak month.

The third batch tried the other explicit calendar control recommended by the current video-intake hypothesis set: replacing only the morning sleeve with `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_ex_gotobi`. That version did trim full-sample max drawdown from `10350` to `9400`, but the cost was too large elsewhere. Full-sample profit fell to `207950`, walk-forward total test profit slipped to `129150`, trade count fell from `539` to `522`, and `2025-02` deteriorated from `7050` to `1600` while `2026-02` again stayed at `150`. The lower drawdown therefore came from discarding too much profitable morning activity, not from improving OOS stability.

This closes the remaining reproducible morning single-sleeve queue around the promoted leader for now. `morning ex_sq` is confirmed as operationally irrelevant in the current bundle, while the only two variants that materially changed outcomes, `morning ex_sq_t16` and `morning ex_gotobi`, both reduced full-sample profit and fixed-set walk-forward total without repairing the live weak-month problem. No new video intake was needed: `docs/VIDEO_INGEST_2026-05-04.md` already contains exactly `6` market-related items for the Tokyo calendar day.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `12` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `after closing the remaining reproducible morning single-sleeve queue, the SQ-only variant proved to be a bundle-level no-op and the only outcome-changing variants both reduced full-sample profit and fixed-set OOS profit while leaving 2026-02 unrepaired`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middayplain-morningexsqt16-openingrange105-rerun`
