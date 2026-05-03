# Research Snapshot 2026-05-01

Current strongest portfolio is now `lot3_base10_june_t8_night_exsq_middayplain_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed inside the promoted-baseline lane, completed four targeted same-lane research batches, and treated the already-complete `2026-05-01` six-video quota as a hard constraint rather than reopening unrelated intake.

The first batch reran the main midday sleeve neighbors around the promoted `...time_stop_10` branch. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` and its equivalent `..._t8` cleared `4/4` walk-forward windows, but that path had already been portfolio-closed earlier in the day because it cut too much full-sample profit when inserted into the live bundle. The fresh information here was that the untied plain `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11` and `..._looser_trail` variants remained dense enough to justify a full-bundle rerun, while `..._tighter_trail` and the shorter hold variants were weaker or window-dependent.

The second batch rechecked the June-only specialist sleeve on the same macro config. That branch is now locally exhausted. Every `only_6` neighbor stayed below the minimum train/test trade gates, several produced zero out-of-sample trades in the latest windows, and none delivered even one accepted walk-forward window. The existing June-only sleeve therefore remains in the bundle only because it is already a tiny additive contributor; it is not a live promotion path on its own and no nearby repair variant deserves a rerun.

The third and fourth batches pushed the two surviving midday main neighbors back into the current six-sleeve bundle. `lot3-base10-june-t8-night-exsq-middayplain-rerun` improved the promoted leader from `232900` to `233750` profit with the same `10350` max drawdown, the same `0` losing months, and stronger portfolio walk-forward totals at `133100` test profit versus the prior leader's `130200`, while keeping worst test drawdown unchanged at `7800`. `lot3-base10-june-t8-night-exsq-middaylooser-rerun` also improved the old leader, but only to `233350`, so it finished behind the plain midday swap on full-sample profit despite a nearly identical walk-forward profile.

Promotion is justified. The new information from this run is not just another closure result: the main midday sleeve had one unclosed same-lane replacement that cleanly beat the promoted leader without paying for the gain through wider drawdown or fresh losing months. By contrast, the June-only branch is now closed again as a sparse control lane, and the already-promoted night `ex_sq`, morning `ex_9_10`, and opening pair remain unchanged inside the new best bundle. The daily video requirement was already satisfied before this block with exactly six official-source videos in `docs/VIDEO_INGEST_2026-05-01.md`, so no additional intake was added.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after four same-lane batches, the remaining reproducible candidates were exhausted for this lane: the June-only midday family stayed below the train/test density gates, time_stop_8 had already been portfolio-closed earlier, and the only new full-bundle challengers plain vs looser were both resolved; the daily 2026-05-01 video quota was already met at exactly six items`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middayplain-rerun`
