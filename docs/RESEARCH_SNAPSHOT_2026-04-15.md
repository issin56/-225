# Research Snapshot 2026-04-15

## Baseline For This Run

This run found that `config.backtest-nk225micro.yaml` currently has `runtime.external_factors_csv` unset.
Because `lot3_base10_june_t8` depends on macro filters, the comparable baseline for this run is the explicit macro-enabled rerun saved below, not the older 2026-04-11 snapshot numbers.

- baseline: `lot3_base10_june_t8`
- baseline file: `results/portfolio-research-2026-04-15-lot3_base10_june_t8-macro-rerun.json`
- profit: `+98,600`
- max_drawdown: `5,200`
- win_rate: `57.14%`
- trades: `553`
- `2024-04`: `+1,600`
- `2024-06`: `+1,250`

## Batch: June Branch Follow-Up

Saved files:
- `results/portfolio-research-2026-04-15-lot3_base10_june_t8-macro-rerun.json`
- `results/portfolio-research-2026-04-15-lot3-june-monwed-range45-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-us10y-not-up-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-range75-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-range90-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-macro-summary.json`

Candidates tested against the macro-enabled baseline:
- `lot3_june_monwed_range45_macro`: `+100,200 / DD 5,200 / win_rate 56.35% / 2024-06 +3,450`
- `lot3_june_us10y_not_up_macro`: `+98,100 / DD 5,200 / win_rate 56.81% / 2024-06 +3,850`
- `lot3_june_range75_macro`: `+93,700 / DD 5,200 / win_rate 56.26% / 2024-06 +650`
- `lot3_june_range90_macro`: `+94,450 / DD 5,200 / win_rate 56.83% / 2024-06 +1,050`

Read:
- the best raw profit candidate was `lot3_june_monwed_range45_macro`, which improved total profit by `+1,600` while keeping drawdown flat
- the best `2024-06` repair was `lot3_june_us10y_not_up_macro`, lifting June from `+1,250` to `+3,850`, but it gave back `500` profit versus the rerun baseline
- none of the June swaps improved `2024-04`; that month stayed flat at `+1,600`
- stricter prior-range filters (`75` and `90`) were clearly weaker and introduced worse follow-on June behavior in `2025-06`

## Validation Check

Saved files:
- `results/validation-2026-04-15-lot3_base10_june_t8-macro-dd-gated.json`
- `results/validation-2026-04-15-lot3-june-monwed-range45-macro-dd-gated.json`

Walk-forward summary:
- baseline: `test profit 61,900 / avg win_rate 57.70% / worst DD 5,200`
- best new candidate: `test profit 59,950 / avg win_rate 57.16% / worst DD 5,200`

Read:
- both portfolios passed the same four DD-gated windows
- the new candidate did not improve walk-forward profit or win rate
- the June repair is real in-sample, but not strong enough to justify promotion

## Decision

- Keep `lot3_base10_june_t8` as the promoted leader for now.
- Carry forward `lot3_june_monwed_range45_macro` as the strongest profit-preserving June repair reference.
- Carry forward `lot3_june_us10y_not_up_macro` as the strongest weak-month repair reference.
- No commit and no push because there were no code changes and no candidate beat the baseline on the combined profit/win-rate plus validation bar.

## Batch: Morning Short Replacement Follow-Up

This follow-up returned to the full promoted `lot3_base10_june_t8` bundle using the dedicated macro lot3 config.
The target was the `day_morning_short_mon_thu_prev_night_down...` branch because it already contributes to both `2024-04` and `2024-06`, so a better variant could have improved weak months without touching the rest of the stack.

Saved files:
- `results/portfolio-research-2026-04-15-lot3-morning-short-t8-macro.json`
- `results/portfolio-research-2026-04-15-lot3-morning-short-t16-macro.json`
- `results/portfolio-research-2026-04-15-lot3-morning-short-sp500-down-macro.json`
- `results/portfolio-research-2026-04-15-lot3-morning-short-usdjpy-down-t025-macro.json`
- `results/portfolio-research-2026-04-15-lot3-morning-short-tuefri-macro.json`
- `results/portfolio-research-2026-04-15-lot3-morning-short-summary.json`

Candidates tested against the promoted baseline:
- `lot3_morning_short_t16_macro`: `+217,600 / DD 13,300 / win_rate 56.85% / 2024-04 +1,450 / 2024-06 +2,500`
- `lot3_morning_short_t8_macro`: `+210,050 / DD 13,300 / win_rate 56.66% / 2024-04 +1,450 / 2024-06 +2,500`
- `lot3_morning_short_tuefri_macro`: `+197,850 / DD 13,800 / win_rate 56.44% / 2024-04 +3,250 / 2024-06 -200`
- `lot3_morning_short_sp500_down_macro`: `+190,100 / DD 13,800 / win_rate 56.80% / 2024-04 +1,250 / 2024-06 -1,000`
- `lot3_morning_short_usdjpy_down_t025_macro`: `+179,250 / DD 14,100 / win_rate 56.63% / 2024-04 -650 / 2024-06 -1,000`

Read:
- the best raw result was `lot3_morning_short_t16_macro`, but it still trailed the leader by `15,250` profit with no drawdown improvement
- loosening the prior-night threshold to `t8` only added trades and reduced both profit and win rate
- the Tue-Fri variant was the only one that materially helped `2024-04`, but it broke `2024-06` and worsened drawdown
- macro filters on the morning short branch were clearly too restrictive here; both `sp500_down` and `usdjpy_down_t025` turned June into a losing month

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Keep the morning short branch unchanged; this lever did not improve profit or win rate while preserving drawdown.
- No commit and no push because there were no code changes and no promotable improvement.

## Batch: Night Neighbor Retest

This follow-up revisited the night branch with three nearby definitions that had not been tested inside the full macro lot3 bundle: the plain `tp` version, the looser FX threshold `v020`, and the intermediate exclusion set `ex_2_6_10_11_12`.
The goal was to check whether a broader night branch could repair `2024-04` / `2024-06` without giving back too much of the leader's drawdown profile.

Saved files:
- `results/portfolio-research-2026-04-15-lot3-night-base-tp-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-v020-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-ex26101112-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-neighbors-summary.json`

Candidates tested against the promoted baseline:
- `lot3_night_ex_2_6_10_11_12_macro`: `+217,100 / DD 17,000 / win_rate 55.81% / 2024-04 +1,450 / 2024-06 +2,500`
- `lot3_night_base_tp_macro`: `+214,200 / DD 17,000 / win_rate 53.13% / 2024-04 +2,600 / 2024-06 +5,950`
- `lot3_night_v020_macro`: `+183,050 / DD 29,350 / win_rate 52.18% / 2024-04 +1,450 / 2024-06 +5,950`

Read:
- none of the three neighbors improved profit or win rate while preserving drawdown; all three were clearly dominated by the promoted leader
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_6_10_11_12` was the least bad of the new set, but it still gave back `15,750` profit and widened drawdown by `3,700`
- the plain `tp` branch did improve both target months, but it did so by reopening unstable night exposure and created five losing months, including fresh damage in `2024-08`, `2024-10`, and `2025-02`
- the looser `v020` threshold was decisively invalidated; it expanded max drawdown to `29,350` and pushed `2024-09` / `2024-10` deeply negative
- this confirms the prior result: if the night branch is relaxed for more gross profit, the next weak spot appears in late-2024 drawdown rather than April or June

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Keep `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_10_11_12` as the only night-side high-profit reference worth remembering, but do not promote it because drawdown still worsens.
- Exclude the plain `tp`, `v020`, and `ex_2_6_10_11_12` night neighbors from near-term follow-up unless a separate drawdown-control overlay is introduced.
- No commit and no push because there were no code changes and no promotable improvement.

## Batch: Night Control Narrowing Follow-Up

This follow-up tested whether a narrower night-control swap could keep more of the promoted leader's profit than `night_only_1_7` while still repairing the weak months.
The night branch was replaced with three middle-ground definitions: a `prev_day_down` gate, a front-half window, and a US-overlap window.

Saved files:
- `results/portfolio-research-2026-04-15-lot3-night-baseline-rerun-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-prevday-ex26101112-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-fronthalf-ex26101112-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-usoverlap-ex26101112-macro.json`
- `results/portfolio-research-2026-04-15-lot3-night-control-summary.json`

Candidates tested against the promoted baseline:
- `lot3_night_prevday_ex_2_6_10_11_12_macro`: `+202,600 / DD 15,750 / win_rate 56.73% / 2024-04 +3,250 / 2024-06 +2,500`
- `lot3_night_front_half_ex_2_6_10_11_12_macro`: `+197,900 / DD 14,250 / win_rate 56.08% / 2024-04 +1,450 / 2024-06 +2,500`
- `lot3_night_us_overlap_ex_2_6_10_11_12_macro`: `+196,150 / DD 15,300 / win_rate 56.64% / 2024-04 +1,900 / 2024-06 +2,500`

Read:
- the best of the three was `lot3_night_prevday_ex_2_6_10_11_12_macro`, but it still gave back `30,250` profit and widened drawdown by `2,450`
- only the `prev_day_down` version materially improved `2024-04`; none of the three improved `2024-06`
- the front-half and US-overlap cuts confirmed that simply narrowing the night trading window does not preserve enough of the branch's contribution
- this leaves the night branch with a clearer split: the promoted baseline remains the only balanced choice, while the night-control variants are useful only as defensive references

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Carry forward `lot3_night_prevday_ex_2_6_10_11_12_macro` only as the best middle-ground night-control reference.
- Deprioritize front-half and US-overlap night narrowing for now because both sharply reduced profit without fixing `2024-06`.
- No commit and no push because there were no code changes and no promotable improvement.

## Batch: June Near-Neighbor Rerun In Current Checkout

This follow-up re-ran the live `lot3_base10_june_t8` bundle in the current synced checkout before testing three untouched June-branch neighbors.
In this checkout, the same `config.backtest-nk225micro.macro.lot3.yaml` rerun matches the long-standing promoted baseline again, so that fresh rerun is the correct comparison point for this batch.

Saved files:
- `results/portfolio-research-2026-04-15-lot3_base10_june_t8-current-rerun.json`
- `results/portfolio-research-2026-04-15-lot3-june-monthu-range45-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-range60-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-plain45-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-neighbor-batch-summary.json`

Current rerun baseline:
- `lot3_base10_june_t8`: `+232,850 / DD 13,300 / win_rate 57.72% / 2024-04 +1,450 / 2024-06 +2,500 / 2025-06 +5,800`

Candidates tested against the fresh rerun:
- `lot3_june_mon_thu_range45_macro`: `+228,700 / DD 13,300 / win_rate 56.83% / 2024-06 +3,400 / 2025-06 +1,750`
- `lot3_june_range60_macro`: `+226,500 / DD 13,300 / win_rate 56.90% / 2024-06 +4,800 / 2025-06 -2,550`
- `lot3_june_plain45_macro`: `+226,450 / DD 13,300 / win_rate 56.31% / 2024-06 +2,050 / 2025-06 +350`

Read:
- the strongest overall candidate was `lot3_june_mon_thu_range45_macro`; it kept drawdown flat and improved `2024-06`, but still gave back `4,150` profit and `0.89pt` of win rate
- `lot3_june_range60_macro` was the strongest pure June repair, lifting `2024-06` to `+4,800`, but it broke `2025-06` to `-2,550` and still lost `6,350` profit
- `lot3_june_plain45_macro` confirmed that removing the VIX gate is not enough; it added trades but underperformed the leader on both profit and win rate
- none of the three touched the weak `2024-04` month, which stayed flat at `+1,450`

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Carry forward `lot3_june_mon_thu_range45_macro` only as the best nearby June reference in the current checkout.
- Exclude `range60` from promotion follow-up because the `2025-06` damage is too large relative to the `2024-06` repair.
- No validation rerun, commit, or push because there were no code changes and no real improvement over the rerun baseline.

## Batch: Additional June Near-Neighbors In Current Checkout

This follow-up stayed inside the same live `lot3_base10_june_t8` bundle and only re-tested three previously defined June-branch overlays that had not yet been rechecked against the current synced-checkout baseline.
The goal was to see whether the older `t16`, `looser_trail`, or `us10y_not_up` variants could repair `2024-06` without reopening the broader regressions seen in earlier defensive-night experiments.

Saved files:
- `results/portfolio-research-2026-04-15-lot3-june-t16-current-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-looser-trail-current-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-us10y-not-up-current-macro.json`
- `results/portfolio-research-2026-04-15-lot3-june-alt-neighbors-summary.json`

Current rerun baseline:
- `lot3_base10_june_t8`: `+232,850 / DD 13,300 / win_rate 57.72% / 2024-04 +1,450 / 2024-06 +2,500 / 2025-06 +5,800`

Candidates tested against the fresh rerun:
- `lot3_june_looser_trail_current_macro`: `+231,300 / DD 13,300 / win_rate 57.54% / 2024-06 +2,500 / 2025-06 +5,450`
- `lot3_june_t16_current_macro`: `+231,050 / DD 13,300 / win_rate 57.47% / 2024-06 +2,500 / 2025-06 +5,900`
- `lot3_june_us10y_not_up_current_macro`: `+228,450 / DD 13,300 / win_rate 57.39% / 2024-06 +4,200 / 2025-06 +1,100`

Read:
- the strongest overall candidate was `lot3_june_looser_trail_current_macro`, but it still lost `1,550` profit and `0.18pt` of win rate with no improvement in either weak month
- `lot3_june_t16_current_macro` behaved similarly and also failed to move `2024-04` or `2024-06`, so the longer time-stop branch looks exhausted in the live bundle
- `lot3_june_us10y_not_up_current_macro` did lift `2024-06` by `+1,700`, but it gave back `4,400` profit and cut `2025-06` from `+5,800` to `+1,100`
- none of the three variants changed `2024-04`, which remained flat at `+1,450`

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Carry forward `lot3_june_looser_trail_current_macro` only as the least-bad additional June reference from this rerun set.
- Deprioritize `june_t16` and `june_looser_trail` for now because both failed to improve the target months.
- Exclude `june_us10y_not_up` from promotion follow-up in the current bundle because the `2025-06` giveback is too large for the `2024-06` repair.
- No validation rerun, commit, or push because there were no code changes and no real improvement over the rerun baseline.
