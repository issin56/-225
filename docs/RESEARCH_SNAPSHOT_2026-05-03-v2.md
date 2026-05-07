# Research Snapshot 2026-05-03

Current strongest portfolio is now `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted-baseline lane, completed four targeted research batches, and used the already-complete `2026-05-03` six-video quota as a hard stop instead of reopening unrelated intake.

The first batch revisited the current tiny April opening sleeve versus the nearby `exclude_sq` controls. That lane stayed structurally sparse in standalone walk-forward terms. The plain `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` branch managed only `1/4` accepted test windows and `0/4` accepted both windows, while `..._ex_sq_range_above_105`, `..._110`, `..._115`, and the nearby `sp500_down_02` overlay were all one-window-only paths with `0/4` accepted both windows and single-window dependence. This means the opening replacement is not a standalone promotion candidate on its own.

The second batch rechecked the morning `ex_9_10` family with the previously unrefreshed `exclude_gotobi`, `exclude_sq`, and factor-gated controls. That lane closed again. The base and `exclude_sq` variants were exact-equivalent under the current source-of-truth data, `exclude_gotobi` reduced density too far to clear the train gate even though it stayed positive out of sample, and the `sp500_down` / `vix_up_02` controls remained either sparse or window-dependent. No morning neighbor justified a bundle rerun.

The third batch revisited the night `usdjpy_down` family with `exclude_gotobi` added to the current `exclude_sq` lane. The family still matters, but it did not overturn the current bundle choice by itself. The plain night sleeve posted the highest single-candidate total test profit at `53,400`, but it again paid for that with a wider `11,400` worst test drawdown. The promoted `exclude_sq` sleeve stayed cleaner at `51,550` total test profit, `4/4` accepted both windows, and `7,650` worst test drawdown, while the `exclude_gotobi` variants dropped to only `1/4` accepted both windows.

The fourth batch pushed the one unresolved opening candidate back into the current six-sleeve bundle. Replacing only `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` with `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_105` improved full-sample profit from `233,750` to `235,600` with the same `10,350` max drawdown, the same `0` losing months, and slightly fewer trades (`539` vs `543`). Portfolio walk-forward also improved from `133,100` to `134,050` total test profit while preserving `4/4` acceptance and the same `7,800` worst test drawdown. The only small giveback was `2024-04` slipping from `+1,450` to `+1,400`, but that was more than offset by `2025-04` improving from `+27,850` to `+29,750`.

Promotion is justified. The new information from this run is that the opening `exclude_sq_range_above_105` sleeve is too sparse to lead on its own, but it is still additive enough inside the already-promoted night `exclude_sq` plus midday-plain bundle to produce a cleaner like-for-like upgrade over the current leader. The daily video requirement for `2026-05-03` had already been satisfied earlier with exactly six official JPX videos in `docs/VIDEO_INGEST_2026-05-03.md`, so no seventh video was added in this run segment.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `16` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after three same-lane closure batches plus one successful openingrange105 bundle rerun, the remaining nearby work in this lane was exhausted because the opening 105/110/115 controls were standalone-sparse or exact-equivalent, the morning neighbors stayed below the train gate or matched the base path exactly, the night plain branch was already portfolio-closed on higher drawdown, and the daily 2026-05-03 video quota had already been met at exactly six items`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middayplain-openingrange105-rerun`
