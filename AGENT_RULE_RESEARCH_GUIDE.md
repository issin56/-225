# Agent Rule Research Guide

## Objective

- Build rules that can plausibly support `50,000 - 100,000 JPY / month` on a `300,000 JPY` account.
- Do not promise this outcome. Treat it as a screening target.

## Acceptance Criteria

- Positive total profit
- Acceptable max drawdown for a 300k account
- Sufficient minimum available balance
- Positive average monthly PnL
- More profitable months than losing months
- Enough trades to avoid tiny-sample noise

## Preferred Research Order

1. Session filter
2. Entry time window
3. Skip minutes after day open
4. Breakout lookback
5. EMA trend filter on/off
6. Long-only vs short-only split

## Common Failure Modes

- Over-optimizing win rate
- Too few trades
- One market regime carrying the whole result
- Ignoring margin buffer
- Ignoring contract roll effects
- Mixing day and night behavior without checking separately

## Handling Network Ideas

- Official product facts go into this repo immediately with source links.
- X, forums, blogs, and videos are `UNVERIFIED`.
- `UNVERIFIED` ideas are allowed only as hypotheses for backtesting.
- Never turn a network claim directly into a live rule without a local test result.
