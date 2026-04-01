# Rule Design Notes

## Goal
- Build rule candidates that can be tested quickly on `日経225マイクロ`.
- Favor robustness over overfitted high win rate.

## Candidate Families
- Trend breakout
  - Use breakout of recent high/low with EMA trend filter.
  - Split by `day`, `night`, `both`.
  - Split by `both`, `long_only`, `short_only`.
- Time window breakout
  - Opening range breakout for `8:45-9:15`
  - Night opening breakout for `17:00-17:30`
- Mean reversion
  - Large deviation from EMA followed by return toward VWAP or EMA
  - Avoid during strong trend days

## What To Track
- `profit`
- `win_rate`
- `max_drawdown`
- `min_available_balance`
- `profitable_months`
- `average_monthly_pnl`
- number of trades

## Practical Filters Worth Testing
- Session filter: `day` / `night`
- Direction filter: `long_only` / `short_only`
- Volatility filter:
  - avoid low ATR
  - avoid extreme ATR spikes
- Day-of-week filter
- Gap filter at day session open
- No-entry windows near session close

## Current Implementation
- Fast candidate testing is in [rule_lab.py](/C:/Users/issin/OneDrive/デスクトップ/kanekasegi/src/kanekasegi/rule_lab.py).
- Default candidate generation is deliberately simple:
  - breakout lookback
  - EMA period
  - session filter
  - direction filter

## Next Extensions
- Add weekday filters
- Add explicit opening-range rules
- Add stop variants:
  - ATR stop
  - previous bar low/high stop
  - fixed tick stop
- Add exit variants:
  - trend exit
  - trailing ATR
  - time stop
- Add slippage and fee assumptions closer to SBI execution reality

## Anti-Patterns
- Optimizing only for win rate
- Choosing rules with very few trades
- Mixing different contract selection assumptions without labeling them
- Reusing a rule in live mode before checking monthly stability
