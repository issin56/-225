# Research Snapshot 2026-04-22

Current strongest portfolio remains `lot3_base10_june_t8`.

Because `lot3_base10_june_t8_opening_april_vix05_exsq_range110` still lacks a clearly better, like-for-like validated replacement over the promoted base path, this run reverted the comparison anchor to the promoted six-sleeve baseline instead of continuing to treat the April add-on branch as the default leader.

- baseline: `lot3_base10_june_t8`
- baseline file: `results/portfolio-research-2026-04-22-lot3_base10_june_t8-current-rerun-2.json`
- baseline result: `+232,850 / DD 13,300 / win_rate 57.72% / trades 570 / 2026-02 +150`
- baseline validation: `results/validation-2026-04-19-lot3_base10_june_t8-sq-dd-gated.json`

## Batch: Morning Sleeve Validation Closure

This batch kept the promoted baseline fixed and only re-ranked nearby `day_morning_short_mon_thu_prev_night_down...` definitions as single-sleeve candidates before considering any full-bundle rerun.

Validated candidates:
- `day_morning_short_tue_fri_prev_night_down_tight_stop`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_t8`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_t16`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_1_2_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_1_2_6_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`

Saved files:
- `results/validation-2026-04-22-morning-neighbor-candidates-dd13300.json`

Key outcomes:
- best single-sleeve candidate by walk-forward acceptance: `day_morning_short_tue_fri_prev_night_down_tight_stop`
- Tue-Fri summary: `3/4` accepted windows, `total_test_profit 16,800`, `average_test_drawdown 6,350`
- current live morning sleeve `ex_9_10`: `0/4` accepted windows under the standalone sleeve thresholds because it is too sparse on its own, despite being acceptable inside the full promoted portfolio
- none of the standalone morning neighbors solved the promoted portfolio's weakest live month `2026-02`, and the prior full-bundle replacement evidence from `2026-04-15` still stands: the least-bad full replacement trailed the promoted path materially on total profit

Interpretation:
- the morning branch remains useful only as one contributing sleeve inside the bundle; its nearby standalone winners do not justify re-opening full-bundle promotion without a new February repair path
- `Tue-Fri` remains the cleanest fallback shape if the branch needs revisiting later, but it is not a new promotion candidate today

## Batch: Opening Base Reconciliation Against Promoted Baseline

This batch first validated nearby opening-base sleeves on their own and then reran only the strongest remaining shapes inside the promoted `lot3_base10_june_t8` bundle.

Standalone opening-base validation candidates:
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_10`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_10`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10`

Standalone validation file:
- `results/validation-2026-04-22-opening-base-neighbors-dd13300.json`

Strongest standalone opening sleeves:
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10`: `4/4` accepted windows, `total_test_profit 29,500`, `average_test_drawdown 5,062.5`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`: `4/4` accepted windows, `total_test_profit 28,700`, `average_test_drawdown 3,075`
- `day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10`: `4/4` accepted windows, `total_test_profit 24,100`, `average_test_drawdown 2,425`

Promoted-baseline bundle reruns:
- `results/portfolio-research-2026-04-22-lot3-opening-base-ex126710-baseline-macro.json`
- `results/portfolio-research-2026-04-22-lot3-opening-base-buf4-baseline-macro.json`
- `results/portfolio-research-2026-04-22-lot3-opening-base-ex1210-baseline-macro.json`
- `results/portfolio-research-2026-04-22-lot3-baseline-opening-neighbor-closure-summary.json`

Bundle outcomes versus promoted baseline:
- baseline `lot3_base10_june_t8`: `+232,850 / DD 13,300 / win_rate 57.72% / losing_months 0`
- `opening-base-ex126710-baseline-macro`: `+229,250 / DD 23,900 / win_rate 57.37% / losing_months 1`
- `opening-base-buf4-baseline-macro`: `+219,850 / DD 11,850 / win_rate 56.69% / losing_months 3`
- `opening-base-ex1210-baseline-macro`: `+221,550 / DD 23,900 / win_rate 56.89% / losing_months 2`

Interpretation:
- the strongest standalone opening sleeves still failed when returned to the promoted bundle, confirming that this branch is being limited by cross-sleeve interaction rather than by isolated sleeve quality
- `ex126710` preserved `2023-09 +250` but turned `2024-04` into `-3000` and nearly doubled drawdown
- `buf4` cut drawdown below baseline, but it lost `13,000` of profit and created three losing months including `2023-09 -1050`
- `ex1210` added trades but created `2025-06 -4700` and the same unacceptable `23,900` drawdown spike

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted baseline.
- Treat the opening-base near-neighbor branch as locally closed unless a future hypothesis explicitly addresses bundle-level overlap with the April-only sleeve.
- No commit and no push because there was no promotable improvement and no code change.

## Batch: Night Sleeve Reconciliation Against Promoted Baseline

This batch kept the six-sleeve promoted baseline fixed and revisited only the closest live night-sleeve alternates that still mattered after the baseline anchor was restored: the broader `ex_2_5_6_8_10_11_12` month set and the sparse `only_1_7` control.

Promoted-baseline reruns:
- `results/portfolio-research-2026-04-22-lot3-night-ex2568101112-baseline-rerun.json`
- `results/portfolio-research-2026-04-22-lot3-night-only17-baseline-rerun.json`
- `results/validation-2026-04-22-lot3-night-ex2568101112-baseline-dd13300.json`
- `results/validation-2026-04-22-lot3-night-only17-baseline-dd13300.json`
- `results/portfolio-research-2026-04-22-lot3-night-baseline-reconciliation-summary.json`

Bundle outcomes versus promoted baseline:
- baseline `lot3_base10_june_t8`: `+232,850 / DD 13,300 / win_rate 57.72% / losing_months 0 / 2026-02 +150`
- `night-ex2568101112-baseline-rerun`: `+236,600 / DD 15,450 / win_rate 56.98% / losing_months 1 / 2026-02 +150`
- `night-only17-baseline-rerun`: `+210,350 / DD 10,350 / win_rate 57.60% / losing_months 0 / 2026-02 +150`

Validation outcomes:
- `night-ex2568101112-baseline-rerun`: `4/4` accepted windows under the `DD<=13,300` test gate, `total_test_profit 125,250`, `average_test_win_rate 56.78%`, `worst_test_drawdown 12,800`
- `night-only17-baseline-rerun`: `4/4` accepted windows, `total_test_profit 102,250`, `average_test_win_rate 57.10%`, `worst_test_drawdown 7,800`

Interpretation:
- `ex_2_5_6_8_10_11_12` is a real, reproducible profit-up variant against the promoted baseline, not just an April-leader artifact, but its improvement comes with a wider full-sample drawdown and a fresh `2024-09 -1050` losing month
- the same rerun leaves `2026-02` unchanged at `+150`, so it still fails the weak-month-repair requirement that matters most for reopening promotion
- `only_1_7` stayed cleaner on drawdown and monthly stability, but it gave back `22,500` of headline profit and crushed `2025-04`, so it remains a control rather than a promotion path

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted baseline.
- Carry `ex_2_5_6_8_10_11_12` forward only as the closest night-sleeve profit challenger, not as a promoted replacement, until a follow-up can neutralize the new `2024-09` weakness without widening drawdown.
- No commit and no push because there was no promotable improvement and no code change.

Video intake handling:
- `docs/VIDEO_INGEST_2026-04-22.md` already held exactly `6` JST market videos before this run segment, so no extra video was added.

## Batch: Night Challenger Follow-Up and Morning Repair Check

This follow-up kept `lot3_base10_june_t8` fixed as the promoted baseline, then tested two narrow questions only:
- whether the strongest night profit-up variant `ex_2_5_6_8_10_11_12` could be rescued by swapping only the morning sleeve
- whether the next nearest night alternates were any cleaner on the promoted baseline than the existing `ex_2_5_6_8_10_11_12` challenger

Promoted-baseline reruns:
- `results/portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-tuefri-baseline.json`
- `results/portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-vix02-baseline.json`
- `results/portfolio-research-2026-04-22-lot3-night-ex2568101112-morning-sp500down-baseline.json`
- `results/portfolio-research-2026-04-22-lot3-night-ex26101112-baseline-rerun.json`
- `results/portfolio-research-2026-04-22-lot3-night-us10yup-ex25689101112-baseline-rerun.json`
- `results/portfolio-research-2026-04-22-lot3-night-and-morning-followup-baseline-summary.json`

Bundle outcomes versus promoted baseline:
- baseline `lot3_base10_june_t8`: `+232,850 / DD 13,300 / win_rate 57.72% / losing_months 0 / 2024-09 +2,700 / 2026-02 +150`
- `night-ex2568101112-morning-tuefri-baseline`: `+198,650 / DD 17,050 / win_rate 55.80% / losing_months 6 / 2024-09 -5,850 / 2026-02 -5,550`
- `night-ex2568101112-morning-vix02-baseline`: `+196,350 / DD 15,450 / win_rate 56.39% / losing_months 3 / 2024-09 -1,050 / 2026-02 +150`
- `night-ex2568101112-morning-sp500down-baseline`: `+192,450 / DD 15,450 / win_rate 56.15% / losing_months 3 / 2024-09 -1,050 / 2026-02 no trade`
- `night-ex26101112-baseline-rerun`: `+217,100 / DD 17,000 / win_rate 55.81% / losing_months 2 / 2024-09 -1,050 / 2026-02 +150`
- `night-us10yup-ex25689101112-baseline-rerun`: `+185,650 / DD 10,350 / win_rate 58.70% / losing_months 0 / 2024-09 +2,700 / 2026-02 +150`

Interpretation:
- the morning repair idea is locally closed for the promoted bundle: `Tue-Fri` collapses in-bundle and turns `2026-02` negative, while the `vix_up_02` and `sp500_down` morning filters preserve the February floor only by giving back roughly `36k-40k` of profit and leaving the `2024-09` night weakness unresolved
- `ex_2_6_10_11_12` is not a cleaner night alternative on the promoted baseline; it keeps the same `2024-09 -1050` problem and adds a fresh `2024-08 -2950` losing month while still trailing baseline profit by `15,750`
- the `usdjpy_down_us10y_up` night gate remains a valid low-drawdown control, but its `+185,650` profit is too sparse to matter for promotion despite preserving monthly cleanliness

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted baseline.
- Keep `ex_2_5_6_8_10_11_12` only as the closest night profit challenger and treat both the morning-repair branch and the nearby night-control branch as closed for now.
- No commit and no push because there was no promotable improvement and no code change.
