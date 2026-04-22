# Research Snapshot 2026-04-11

## Leader

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

## Batch 1: Order Sensitivity Probe

Saved files:
- `results/portfolio-research-2026-04-11-lot3-order-april-before-night.json`
- `results/portfolio-research-2026-04-11-lot3-order-april-before-morning.json`
- `results/portfolio-research-2026-04-11-lot3-order-june-after-morning.json`
- `results/portfolio-research-2026-04-11-lot3-order-april-before-night-june-after-morning.json`

Candidates tested against the baseline:
- `lot3_order_april_before_night`
- `lot3_order_april_before_morning`
- `lot3_order_june_after_morning`
- `lot3_order_april_before_night_june_after_morning`

Read:
- all four order variants matched the baseline exactly on profit, win rate, drawdown, and monthly PnL
- this shows the weak `2024-04` and `2024-06` months are not caused by candidate priority collisions
- candidate ordering is not a useful lever for this portfolio family

## Batch 2: April Replacement Follow-Up

Saved files:
- `results/portfolio-research-2026-04-11-lot3-april-vix-not-up.json`
- `results/portfolio-research-2026-04-11-lot3-april-buf4.json`
- `results/portfolio-research-2026-04-11-lot3-april-prev-night-up-buf2.json`
- `results/portfolio-research-2026-04-11-lot3-april-prev-night-up-buf4.json`
- `results/portfolio-research-2026-04-11-lot3-order-april-summary.json`

Candidates tested against the baseline:
- `lot3_april_vix_not_up`: `+221,000 / DD 13,300 / win_rate 57.44% / 2024-04 -4,150`
- `lot3_april_buf4`: `+220,400 / DD 13,300 / win_rate 57.09% / 2024-04 -3,850`
- `lot3_april_prev_night_up_buf2`: `+222,100 / DD 13,300 / win_rate 57.59% / 2024-04 -4,150`
- `lot3_april_prev_night_up_buf4`: `+222,100 / DD 13,300 / win_rate 57.47% / 2024-04 -3,650`

Read:
- every April replacement preserved drawdown but materially reduced profit
- all four replacements turned `2024-04` from a small gain into a clear losing month
- none improved `2024-06`, which stayed flat at `+2,500`
- the current `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` April branch remains the least-bad option in the promoted portfolio

## Decision

- Keep `lot3_base10_june_t8` as the promoted leader.
- Save the order probe and April replacement batch as useful negatives.
- No validation rerun, no commit, and no push because there was no real improvement to promote.

## Next Direction

- stop spending more budget on April specialist swaps that only target the isolated April branch
- focus next on replacing or conditioning the negative `2024-06` June-only midday long branch, since order changes did nothing and April alternatives regressed harder
