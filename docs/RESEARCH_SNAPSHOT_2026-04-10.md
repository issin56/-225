# Research Snapshot 2026-04-10

## Baseline Still Leading

Current strongest portfolio remains `lot3_base10_june_t8`.

- profit: `+232,850`
- max_drawdown: `13,300`
- win_rate: `57.72%`
- trades: `570`
- profitable months: `26`
- losing months: `0`
- average_monthly_pnl: `8,029.31`

Weak months under the current leader:
- `2024-04`: `+1,450`
- `2024-06`: `+2,500`

## Batch 1: April and June Replacement Sweep

Saved file:
- `results/portfolio-research-2026-04-10-lot3-targeted-apr-jun.json`

Candidates tested against the baseline:
- `lot3_base10_june_t8_april_sp500`: `+231,750 / DD 13,300 / win_rate 57.64%`
- `lot3_base10_june_t8_april_prev_down`: `+229,100 / DD 13,300 / win_rate 57.73%`
- `lot3_base10_june_t16`: `+231,050 / DD 13,300 / win_rate 57.47%`
- `lot3_base10_june_looser_trail`: `+231,300 / DD 13,300 / win_rate 57.54%`
- `lot3_base10_june_t16_april_sp500`: `+229,950 / DD 13,300 / win_rate 57.39%`

Read:
- none of these exceeded the baseline on profit
- drawdown stayed flat at `13,300` for every candidate
- the targeted April and June swaps did not improve `2024-04` or `2024-06` at the portfolio level

## Batch 2: Night Filter and June Macro Sweep

Saved file:
- `results/portfolio-research-2026-04-10-lot3-targeted-night-june.json`

Candidates tested against the baseline:
- `lot3_base10_june_t8_night_us10y`: `+185,650 / DD 10,350 / win_rate 58.70%`
- `lot3_base10_june_t8_night_prevday`: `+202,600 / DD 15,750 / win_rate 56.73%`
- `lot3_base10_june_us10y_not_up`: `+228,450 / DD 13,300 / win_rate 57.39%`
- `lot3_base10_june_us10y_not_up_night_us10y`: `+182,550 / DD 10,350 / win_rate 58.28%`

Read:
- the `night_us10y` branch materially improved drawdown and win rate, but profit dropped too far to promote it
- the `night_prevday` branch worsened both drawdown and profit
- the June `us10y_not_up` filter also failed to beat the current rescue branch

## Batch 3: Night Variant Follow-Up

Saved file:
- `results/portfolio-research-2026-04-10-lot3-targeted-night-variant.json`

Candidates tested against the baseline:
- `lot3_night_ex_2_5_6_8_10_11_12`: `+236,600 / DD 15,450 / win_rate 56.98%`
- `lot3_night_ex_2_5_6_8_10_11_12_june_t16`: `+234,900 / DD 15,450 / win_rate 56.74%`
- `lot3_night_ex_2_5_6_8_10_11_12_april_sp500`: `+235,500 / DD 15,450 / win_rate 56.91%`
- `lot3_night_ex_2_5_6_8_10_11_12_june_us10y`: `+231,500 / DD 15,450 / win_rate 56.67%`
- `lot3_night_ex_2_5_6_8_10_11_12_april_prev_down`: `+230,300 / DD 15,450 / win_rate 56.97%`

Read:
- relaxing the night exclusion set to allow September lifted total profit by `+3,750`, but drawdown worsened by `+2,150` and introduced a losing month in `2024-09`
- the best follow-up also nudged the weak months only modestly: `2024-06` improved from `+2,500` to `+3,100`, while `2024-04` stayed flat at `+1,450`
- stacking the stronger night branch with June or April replacements did not recover the drawdown regression

## Decision

- Keep `lot3_base10_june_t8` as the promoted leader.
- Save all three batch outputs as useful negatives so the next pass does not repeat them.
- No validation rerun, no commit, and no push because no real improvement cleared the baseline.

## Batch 4: Alternate Night Replacement Sweep

Saved files:
- `results/portfolio-research-2026-04-10-lot3-targeted-night-only17.json`
- `results/portfolio-research-2026-04-10-lot3-targeted-night-front-half.json`
- `results/portfolio-research-2026-04-10-lot3-targeted-night-us10y-only34.json`
- `results/portfolio-research-2026-04-10-lot3-targeted-night-alt-summary.json`

Candidates tested against the baseline:
- `lot3_base10_june_t8_night_only_1_7`: `+210,350 / DD 10,350 / win_rate 57.60%`
- `lot3_base10_june_t8_night_front_half`: `+197,900 / DD 14,250 / win_rate 56.08%`
- `lot3_base10_june_t8_night_us10y_only_3_4`: `+168,400 / DD 10,350 / win_rate 58.04%`

Read:
- `night_only_1_7` was the best of this batch and did improve both weak months to `2024-04 = +3,250` and `2024-06 = +3,100`
- that branch also cut drawdown by `2,950`, but total profit still fell by `22,500`, so it is useful only as a defensive fallback
- `night_front_half` was clearly worse, adding three losing months and worse drawdown
- `night_us10y_only_3_4` had the best win rate of the batch, but profit collapsed too far to consider

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Carry forward `night_only_1_7` only as a reference branch for future defensive or capital-efficiency work.
- No validation rerun, no commit, and no push because no real improvement cleared the baseline.

## Batch 5: Night `us10y_up` Recovery Probe

Saved files:
- `results/portfolio-research-2026-04-10-lot3_base10_june_t8_night_us10yup.json`
- `results/portfolio-research-2026-04-10-lot3_base10_june_t8_night_us10yup_june_t16.json`
- `results/portfolio-research-2026-04-10-lot3_base10_june_t8_night_us10yup_june_looser_trail.json`
- `results/portfolio-research-2026-04-10-lot3_base10_june_t8_night_us10yup_june_us10y_not_up.json`
- `results/portfolio-research-2026-04-10-lot3-targeted-night-us10yup-summary.json`

Candidates tested against the baseline:
- `lot3_base10_june_t8_night_us10yup`: `+185,650 / DD 10,350 / win_rate 58.70%`
- `lot3_base10_june_t8_night_us10yup_june_looser_trail`: `+184,450 / DD 10,350 / win_rate 58.48%`
- `lot3_base10_june_t8_night_us10yup_june_t16`: `+183,300 / DD 10,350 / win_rate 58.39%`
- `lot3_base10_june_t8_night_us10yup_june_us10y_not_up`: `+182,550 / DD 10,350 / win_rate 58.28%`

Read:
- the plain `night_us10yup` replacement was the best of this batch, but it still trailed the leader by `47,200` profit despite improving drawdown by `2,950`
- all four variants improved `2024-04` to `+3,250`, but none recovered enough profit to challenge the baseline
- June overlays did not help the recovery path: `t16` and `looser_trail` left `2024-06` flat at `+2,500`, while `june_us10y_not_up` improved `2024-06` to `+4,200` but had the worst profit of the batch
- this confirms the `us10y_up` night branch is useful only as a defensive template, not as a promotable replacement for `lot3_base10_june_t8`

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Keep `night_only_1_7` and `night_us10yup` only as defensive reference branches because both improve weak months and drawdown but sacrifice too much profit.
- No validation rerun, no commit, and no push because no real improvement cleared the baseline.

## Batch 6: `night_only_1_7` Recovery Overlay Probe

Saved file:
- `results/portfolio-research-2026-04-10-lot3-targeted-night-only17-recovery.json`

Candidates tested against the baseline:
- `lot3_base10_june_t8_night_only17_april_t16`: `+209,800 / DD 10,350 / win_rate 57.69%`
- `lot3_base10_june_t8_night_only17_april_t16_range130`: `+207,350 / DD 10,350 / win_rate 57.64%`
- `lot3_base10_june_t8_night_only17_june_us10y_not_up`: `+206,400 / DD 10,350 / win_rate 57.23%`
- `lot3_base10_june_t8_night_only17_june_base_april_t16`: `+207,250 / DD 10,350 / win_rate 57.29%`
- `lot3_base10_june_t8_night_only17_june_us10y_not_up_april_t16`: `+205,850 / DD 10,350 / win_rate 57.31%`

Read:
- the best recovery overlay was `night_only17_april_t16`, which kept the defensive branch drawdown improvement and lifted `2024-04` to `+3,200` plus `2024-06` to `+3,100`
- even the best overlay still trailed the leader by `23,050`, so none of these recovery stacks are promotable
- `june_us10y_not_up` did improve `2024-06` further to `+4,850`, but the trade-off was even larger profit erosion and weaker later June performance in `2025-06`
- all five recovery variants stayed at `DD 10,350`, confirming this branch is capped by the defensive night replacement rather than by the April or June overlay

Updated decision:
- Keep `lot3_base10_june_t8` as the promoted leader.
- Treat the `night_only_1_7` branch as drawdown-defense only; adding April/June recovery overlays does not close the profit gap.
- No tests, commit, or push because there were no code changes and no real improvement to validate or promote.
