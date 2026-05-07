# Research Snapshot 2026-05-08

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This full research block stayed inside the promoted `macro.lot3` lane, completed three targeted research batches, and then reconciled the nearest prior bundle rerun before closing with the required daily video intake.

The first batch revisited the morning sleeve's residual calendar overlays with `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`, `...ex_gotobi`, `...ex_sq`, and `...ex_sq_t16`. The base sleeve and `...ex_sq` again finished as exact walk-forward twins at `1/4` accepted-test windows, `0/4` accepted-both windows, `20200` total test profit, and `32` total test trades, confirming that the added SQ exclusion remains operationally irrelevant in this lane. `...ex_gotobi` lowered density further to `23` total test trades and `15300` total test profit, while `...ex_sq_t16` stayed weaker at `17900` total test profit. No morning overlay justified a bundle rerun.

The second batch reopened the night sleeve's gotobi/calendar neighbors with `...ex_2_5_6_8_9_10_11_12`, `...ex_gotobi`, `...ex_sq`, `...ex_sq_ex_gotobi`, and `...only_1_7`. The non-SQ base variant again topped raw sleeve OOS total at `53400`, but it still carried the wider `11400` worst test drawdown that already kept it below the promoted `...ex_sq` sleeve. `...ex_gotobi` and `...ex_sq_ex_gotobi` posted only `1/4` accepted-both windows despite positive OOS in every window, and `...only_1_7` reached only `30150` total test profit. This reconfirmed that the current `...ex_sq` night sleeve remains the cleanest accepted choice.

The third batch rechecked midday durability neighbors around the promoted main sleeve: `base`, `time_stop_8`, `time_stop_10`, and `looser_trail`. All four stayed positive across all OOS windows, but none opened a promotion path. `...looser_trail` was the closest fresh challenger at `23950` total test profit with `3/4` accepted-both windows, only narrowly ahead of the base sleeve's `23650` and still with a worse `4450` worst test drawdown versus `4250`. `...time_stop_10` reached `22750` total test profit and `...time_stop_8` reached `21550`. Because the prior full-bundle rerun for `...middayloosertrail...` already exists and still trails the promoted leader on full-sample profit (`235200` vs `235600`) while only adding `50` to fixed-set OOS total (`134100` vs `134050`), no new bundle rerun was warranted.

This block therefore closes the remaining same-lane calendar/gotobi/durability residue without changing the promoted source of truth. The only near-miss remained the previously known midday looser-trail family, and today's sleeve-level recheck again showed that its tiny OOS edge is not large enough to offset lower full-sample profit or justify a new promotion. `docs/VIDEO_INGEST_2026-05-08.md` now records exactly `6` official-source JPX video intakes for the Tokyo calendar day.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `58` minutes
- research batches completed: `3`
- stopped before 50 minutes: `no`
- blocker: `none; the run budget was used on three targeted batches, same-lane reconciliation, dashboard updates, and the daily 6-video intake`
- best candidate tested: `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail`
