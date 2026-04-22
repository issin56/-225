# Research Snapshot 2026-04-20

Current strongest portfolio remains `lot3_base10_june_t8_opening_april_vix05_exsq_range110`.

## Batch: Night prev_day_down Threshold Transfer

This follow-up stayed anchored to the promoted six-sleeve leader and only revisited the direct `prev_day_down` night-replacement hypothesis using the current-source threshold neighbors that still exist locally.

The tested replacements were:
- `both_fast_short_night_prev_day_down_tue_fri_tp_t16`
- `both_fast_short_night_prev_day_down_tue_fri_tp_t8`

Saved files:
- `results/portfolio-research-2026-04-20-lot3-night-prevday-t16-openingrange110-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-night-prevday-t8-openingrange110-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-night-prevday-threshold-transfer-current-summary.json`

Key outcomes:
- baseline remains `+236,250 / DD 13,300 / win_rate 57.95% / 2026-02 +150`
- best new candidate: `night_prevday_t16_openingrange110` at `+202,350 / DD 26,650 / win_rate 51.68% / 2026-02 +11,700`
- second candidate: `night_prevday_t8_openingrange110` at `+197,800 / DD 26,050 / win_rate 50.83% / 2026-02 +11,700`

Interpretation:
- the transfer confirmed the same trade-off as earlier `prev_day_down` work: February can be repaired strongly, but only by reintroducing broad autumn damage and unacceptable drawdown expansion
- `t16` was the less-bad neighbor, yet it still lost `33,900` versus the leader, created six losing months, and widened drawdown by `13,350`
- `t8` was weaker again, losing `38,450` with the same six losing months and no compensating stability gain
- the older `ex_9_10` seasonal-guarded `prev_day_down` variant could not be rerun directly because that candidate is no longer present in the current local source, so this batch closes the still-reproducible threshold-transfer branch instead of reviving stale artifacts

Video intake handling:
- `docs/VIDEO_INGEST_2026-04-20.md` already held exactly `6` JST videos before this batch, so no extra video was added

## Batch: April/June Add-On Closure

This follow-up stayed anchored to the promoted `lot3_base10_june_t8` path via the current six-sleeve leader `lot3_base10_june_t8_opening_april_vix05_exsq_range110` and closed the remaining additive branches instead of testing more replacements.

The tested add-ons were:
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16`
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16_range_above_130`
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16_range_above_180`
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t12 + day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t16`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_looser_trail`
- `day_midday_long_prev_night_up_trail_only_6_prev_range_above_75`
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16 + day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t16`

Saved files:
- `results/portfolio-research-2026-04-20-lot3-opening_april_addon_prevnightdown_t16-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-opening_april_addon_prevnightdown_t16_range130-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-opening_april_addon_prevnightdown_t16_range180-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-opening_april_addon_prevnightdown_t12_plus_t16-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-june_addon_monwed_vix02_t16-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-june_addon_monwed_vix02_loosertrail-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-june_addon_prev_range75-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-april_t16_plus_june_t16-current-macro.json`
- `results/validation-2026-04-20-lot3-opening-april-addon-prevnightdown-t16-current-dd-gated.json`
- `results/portfolio-diagnostics-2026-04-20-lot3-opening-april-addon-prevnightdown-t16-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-april-june-addon-closure-current-summary.json`

Key outcomes:
- `opening_april_addon_prevnightdown_t16`: `+237,650 / DD 13,300 / win_rate 57.92% / trades 568`
- delta vs leader: `+1,400 profit / flat DD / -0.03pt win_rate / +2 trades`
- month impact: only `2025-04` improved, moving from `25,700` to `27,100`; `2024-04`, both June months, and `2026-02` stayed unchanged
- dd-gated walk-forward: `3/4` accepted windows, `total_test_profit 131,400`, `average_test_win_rate 58.79%`, `worst_test_drawdown 11,450`

Interpretation:
- the plain `t16` April add-on was the strongest new branch, but it still came entirely from two trades in `2025-04`, so the edge is too narrow to promote
- `t16_range_above_130` and `t16_range_above_180` were exact-equivalence aliases of the plain `t16` branch, and stacking `t12+t16` merely fell back to the earlier weaker `t12` profile
- the June `mon_wed_vix02_t16` and `looser_trail` add-ons traded `0` times, while `prev_range_above_75` added `21` trades but lost `450` on the sleeve itself and worsened both June weak months
- the combined `April t16 + June t16` bundle exactly matched the plain April `t16` result because the June t16 sleeve was inert

Video intake handling:
- `docs/VIDEO_INGEST_2026-04-20.md` already held exactly `6` JST videos before this batch, so no extra video was added

## Batch: April Macro Add-On And Night Replacement Closure

This follow-up stayed anchored to the promoted `lot3_base10_june_t8` path and only checked two untested April add-ons plus four narrow replacements for the live night sleeve.

The tested additions/replacements were:
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16_vix_up`
- `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16_sp500_down_vix_up`
- `both_fast_short_night_tue_fri_usdjpy_down_us10y_up_tp_ex_2_5_6_8_9_10_11_12`
- `both_fast_short_night_front_half_usdjpy_down_tp_ex_2_6_10_11_12`
- `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12`
- `both_fast_short_night_prev_day_down_tue_fri_usdjpy_down_tp_v025_ex_2_6_10_11_12`

Saved files:
- `results/portfolio-research-2026-04-20-lot3-opening_april_addon_prevnightdown_t16_vixup-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-opening_april_addon_prevnightdown_t16_sp500vix-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-night-us10yup-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-night-fronthalf-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-night-usoverlap-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-night-prevdaydown-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-april-addon-macro-and-night-closure-current-summary.json`

Key outcomes:
- baseline remains `+236,250 / DD 13,300 / win_rate 57.95% / trades 566`
- the two April macro add-ons were identical at `+232,900 / DD 13,300 / win_rate 57.85% / trades 567`
- best night replacement was `prev_day_down` at `+204,450 / DD 15,750 / win_rate 56.96% / trades 553`
- lowest-drawdown replacement was `us10y_up` at `+187,500 / DD 10,350 / win_rate 58.99% / trades 456`

Interpretation:
- both April add-ons created one extra April 2025 trade and that trade lost `1,800`, so they reduced full-sample profit by `3,350` without changing weak months
- the night replacements could lift `2024-04` from `+1,400` to `+3,200`, but none moved `2026-02` off `+150` and every version gave up too much broad night exposure
- `us10y_up` improved drawdown but lost `48,750` of total profit; `prev_day_down` was less bad on profit but widened drawdown to `15,750`; `front_half` and `us_overlap` introduced losing months
- this closes the remaining obvious April macro add-on and narrow night-sleeve timing/filter neighbors around the promoted leader

Video intake handling:
- `docs/VIDEO_INGEST_2026-04-20.md` already held exactly `6` JST videos before this batch, so no extra video was added

## Batch: Morning ex_9_10 Macro Neighbor Check

This follow-up stayed on the promoted `lot3_base10_june_t8` path and only replaced the current `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` sleeve with four narrow macro-gated neighbors.

The tested replacements were:
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_t16`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_usdjpy_down_v025`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_sp500_down`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10_vix_up_02`

Saved files:
- `results/portfolio-research-2026-04-20-lot3-morning-ex910-t16-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-morning-ex910-usdjpyv025-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-morning-ex910-sp500-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-morning-ex910-vix02-current-macro.json`
- `results/portfolio-research-2026-04-20-lot3-morning-ex910-neighbors-current-summary.json`

Key outcomes:
- baseline remains `+236,250 / DD 13,300 / win_rate 57.95% / 2026-02 +150`
- best new candidate: `ex_9_10_t16` at `+226,150 / DD 13,300 / win_rate 57.65%`
- other candidates: `ex_9_10_vix_up_02` `+197,050 / DD 13,100`, `ex_9_10_sp500_down` `+192,350 / DD 13,100`, `ex_9_10_usdjpy_down_v025` `+187,900 / DD 14,100`

Interpretation:
- none of the four replacements improved `2026-02`; every variant stayed at `+150` or removed the month entirely by trading too little
- the least-bad neighbor, `ex_9_10_t16`, still lost `10,100` of full-sample profit and weakened `2023-12`, `2024-11`, `2025-01`, and `2025-06`
- the macro-gated versions cut trade count too aggressively, lost the current sleeve's broad contribution pattern, and did not create a new weak-month repair path
- reconciliation with the earlier June follow-up remains unchanged: `day_midday_long_prev_night_up_trail_only_6_mon_wed_prev_range_above_45_us10y_not_up_vix_up_02_t8` is still a `0`-trade alias of the live June sleeve, so there was no hidden June promotion branch to recover here

Video intake handling:
- `docs/VIDEO_INGEST_2026-04-20.md` already held exactly `6` JST videos before this batch, so no extra video was added
