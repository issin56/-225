# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed five meaningful research steps: an opening-secondary ex-SQ ladder, a midday-secondary revival check, a night alternative batch, and two bundle recompositions that inserted the revived night sleeve into locally reproducible structures. The opening secondary family stayed completely dead with `0` trades across all four walk-forward windows, the midday secondary family also stayed dead except for a too-few-trades `mon_wed` stub, and the only real recovery came from `both_fast_short_night_tight_stop_mon_thu`, which validated `4/4` windows with `18750` total test profit. Adding that night sleeve into the live bundles improved local reproducibility, but the best balanced bundle still widened drawdown versus the promoted source-truth leader and reintroduced too many losing months, so no promotion is justified.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `54` minutes
- research batches completed: `5`
- stopped before 50 minutes: `no`
- blocker: `none`
- best candidate tested: `lot3_sourcetruth_primary_plus_nighttight_rerun`

## Batch Notes

- opening secondary ex-SQ ladder:
  every tested `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_*_ex_sq*` branch stayed at `0` trades in all four walk-forward windows, including `range_above_100/105/110/115/120` and `vix_up_04/05/06` variants. The source-truth opening secondary remains locally unrecoverable.
- midday secondary revival check:
  every `...mon_wed_vix_up_02*` or `...us10y_not_up_vix_up_02*` branch stayed at `0` trades. The only branch with any life was `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed`, but it produced just `14` total test trades and `250` total test profit, so it is still not usable.
- night alternative batch:
  `both_fast_short_night_tight_stop_mon_thu` was the only meaningful recovery, validating `4/4` windows with `18750` total test profit, `4950` average test drawdown, and `598` total test trades. Other night alternates were either zero-trade or flipped negative on test.
- alive-plus-nighttight recomposition:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_looser_trail` + `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` + `both_fast_short_night_tight_stop_mon_thu` + `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` reran at `98600 / DD 13300 / losing_months 6` and validated `4/4` windows with `64450` total test profit. It is locally strong but too coarse on drawdown and monthly stability.
- source-truth-primary-plus-nighttight recomposition:
  `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_10` + `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` + `both_fast_short_night_tight_stop_mon_thu` + `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10` reran at `92300 / DD 7850 / losing_months 6` and validated `4/4` windows with `55900` total test profit. It is the best balanced new bundle this run, but it still trails the promoted leader on drawdown discipline and monthly smoothness because the revived night sleeve drives weak February and October behavior.

## Video Intake

- `2026-05-01` daily quota was met with exactly `6` official JPX videos.
- accepted hypotheses reinforced the active lane:
  - keep overlays sparse
  - keep SQ logic explicit
  - keep volatility inputs reproducible
  - keep bundle edits local instead of switching leaders
