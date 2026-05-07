# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted-baseline lane, completed four targeted research batches, and did not reopen video intake because the `2026-05-03` daily quota had already been satisfied earlier with exactly six JPX videos.

The first batch revisited the opening April repair sleeve around the promoted `range_above_105` setting, using the nearby `108`, `110`, `112`, and `vix_up_04/06` controls. Under the current local rerun state, every candidate in that batch returned `0` train trades and `0` out-of-sample trades across all four walk-forward windows. That is not compatible with the source-of-truth leader bundle, which previously recorded `12` trades and `10,300` profit from the same opening sleeve inside the promoted portfolio.

The second batch rechecked the midday secondary sleeve family around the promoted `...mon_wed_vix_up_02_t8` branch. The plain variant, the promoted `t8`, the `t16` and looser-trail controls, and the `us10y_not_up` overlays all also returned `0` train trades and `0` out-of-sample trades in every window under the current local rerun state. Because the source-of-truth leader bundle previously carried `9` trades and `6,600` profit from the promoted midday secondary sleeve, this is another reproducibility mismatch rather than evidence that the sleeve has been cleanly invalidated.

The third batch stayed with the morning `ex_9_10` family because that lane still reproduced non-zero behavior locally. The base and `exclude_sq` variants remained exact-equivalent at `8,350` total test profit, `1/4` accepted test windows, `0/4` accepted both windows, and `2,950` worst test drawdown, while the `t16` variants slipped to `7,200` total test profit with the same `0/4` accepted both windows. The `usdjpy_down_v025` controls fully collapsed to `0` trades, so no morning neighbor justified a bundle rerun.

The fourth batch was a direct crosscheck: the promoted opening `range_above_105` sleeve was rerun again using the worktree code against the OneDrive source-of-truth data and config. It still produced `0` trades in all four walk-forward windows, which rules out "missing prior artifacts in the worktree" as the explanation. The opening and midday discrepancies therefore point to a current local data/factor/replay mismatch that needs to be reconciled before any same-lane promotion work on those sleeves can be trusted.

Promotion is not justified. The promoted leader stays `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, and the structural baseline stays `lot3_base10_june_t8`. The best reproducible candidate tested in this run was still the morning `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`, but it was far below the promoted bundle and failed the same walk-forward acceptance gate as before.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `24` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `opening and midday leader sleeves no longer reproduce under the current local rerun state even when cross-checked with the worktree code against the OneDrive source-of-truth config/data, so further same-lane promotion work would be comparing against an inconsistent replay environment rather than a stable baseline`
- best candidate tested: `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
