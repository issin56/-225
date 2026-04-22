# Research Snapshot 2026-04-06

## Newer Update

This file has an older mixed history. The cleaner current summary is:
- [RESEARCH_SNAPSHOT_2026-04-06-v5.md](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\docs\RESEARCH_SNAPSHOT_2026-04-06-v5.md)

Current official best is now `stable_seasonal_v5`, not `v4`.

## Current Verified Basis

This file now mixes older `33-month` notes with the current `29 active months` JPX load.
For any current comparison, use the `stable_seasonal_v4` block below as the source of truth and treat older `19/33` or `21/33` style figures as legacy notes only.

Current verified benchmark:
- sample basis: `29 active months`
- portfolio: `stable_seasonal_v4`
- result: `+99,000 / max_drawdown 5,400 / win_rate 54.66% / 21 profitable months / 4 losing months`
- walk-forward read: `accepted_both_windows 4/4 / total_test_profit 67,000 / worst_test_drawdown 5,400`

Current benchmark files:
- [portfolio-research-2026-04-06-stable-seasonal-v4.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-stable-seasonal-v4.json)
- [validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v4.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v4.json)
- [portfolio-diagnostics-2026-04-06-stable-seasonal-v4.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-stable-seasonal-v4.json)

Macro factor pipeline added:
- [build-macro-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-macro-factors.ps1)
- [config.backtest-nk225micro.macro.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\config.backtest-nk225micro.macro.yaml)
- [external_factors.macro.csv](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\data\external_factors.macro.csv)
- factor set:
  - `usd_jpy_change`
  - `sp500_change`
  - `vix_change`
  - `us10y_change`

Latest replacement checks against `stable_seasonal_v4`:
- `fade prev_night_up` replacement: weaker at `+85,200 / DD 4,950`
- `midday late_window` replacement: weaker at `+85,350 / DD 5,950`
- `midday usdjpy_up` replacement: weaker at `+78,850 / DD 4,450`
- new `fade buf4 ex` replacement: weaker at `+88,700 / DD 5,650`

Reading notes:
- `active_months` means months with loaded data in the current sample.
- `months` in diagnostics means months that have a non-zero PnL entry.
- `walk-forward 4/4 pass` means fixed-rule robustness across rolling windows, not re-optimized walk-forward.

## Macro Expansion

Added external macro build path:
- [build-macro-factors.ps1](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\scripts\build-macro-factors.ps1)
- [config.backtest-nk225micro.macro.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\config.backtest-nk225micro.macro.yaml)
- [external_factors.macro.fred.csv](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\data\external_factors.macro.fred.csv)

Current macro set:
- `usd_jpy_change`
- `sp500_change`
- `vix_change`
- `us10y_change_bp`

Probe summary:
- [portfolio-research-2026-04-06-v4-macro-probes.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-v4-macro-probes.json)

Quick read:
- `midday_sp500_probe`
  - `+89,500 / DD 5,550 / 23 profitable months`
- `morning_sp500_probe`
  - `+85,150 / DD 5,400 / 22 profitable months`
- `fast_sp500_probe`
  - `+88,900 / DD 5,550 / 21 profitable months`
- `sp500_full_portfolio`
  - `+67,550 / DD 6,900 / 24 profitable months`

Interpretation:
- `SP500` 全面置換はまだ弱い
- ただし `midday long` の補助フィルタとしては再検討価値あり
- `VIX` と `us10y_change_bp` は次の局所プローブ候補

## Brother Repo Takeaways

Reference repo:
- [noob-matsunaga/nikkei225micro-share](https://github.com/noob-matsunaga/nikkei225micro-share)

Useful ideas we imported or adopted as process:
- `opening_range_fade` style entry family for day-session short research.
- Small nearby-variant family testing instead of jumping straight to a large optimizer.
- Freeze promising candidates into named seeds after they survive a family sweep.
- Promote ideas by robustness checks, not by one lucky backtest.

Notable local reference files from the brother repo:
- [day-short-opening-range-fade-2026-03-29.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\tmp_brother_repo\config\exact\day-short-opening-range-fade-2026-03-29.yaml)
- [day-session-high-overunder-core-2026-03-31.yaml](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\tmp_brother_repo\config\campaigns\day-session-high-overunder-core-2026-03-31.yaml)
- [walk-forward-runbook.md](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\tmp_brother_repo\docs\walk-forward-runbook.md)

## Fade Family Results

First-pass fade variants were weak:
- `day_opening_short_range_fade`: `-7,250`
- `day_opening_short_range_fade_mon_thu`: `-9,300`
- `day_opening_short_range_fade_prev_night_up`: `-6,350`

We then ran a nearby-variant family sweep around the same idea:
- [research-batch-2026-04-06-opening-fade-family.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\research-batch-2026-04-06-opening-fade-family.json)

Best fade candidates:
- `day_opening_short_range_fade_lb8_buf2`
  - `+12,650`
  - `472 trades`
  - `win_rate 53.81%`
  - `max_drawdown 17,000`
- `day_opening_short_range_fade_lb8_buf4`
  - `+6,900`
  - `339 trades`
  - `win_rate 53.39%`
  - `max_drawdown 15,550`

Reference batch:
- [research-batch-2026-04-06-opening-fade-shortlist.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\research-batch-2026-04-06-opening-fade-shortlist.json)

## Portfolio Impact

Stability-leaning portfolio plus fade:
- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`
- `day_opening_short_range_fade_lb8_buf2`
- Result:
  - `+81,050`
  - `max_drawdown 12,750`
  - `win_rate 50.88%`
  - `19/33 profitable months`
- Files:
  - [portfolio-research-2026-04-06-usdjpy-plus-fade.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-usdjpy-plus-fade.json)
  - [portfolio-diagnostics-2026-04-06-usdjpy-plus-fade.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-usdjpy-plus-fade.json)

Profit-leaning portfolio plus fade:
- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_tp`
- `day_opening_short_range_fade_lb8_buf2`
- Result:
  - `+84,300`
  - `max_drawdown 12,900`
  - `win_rate 48.79%`
  - `21/33 profitable months`
- Files:
  - [portfolio-research-2026-04-06-profit-plus-fade.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-profit-plus-fade.json)
  - [portfolio-diagnostics-2026-04-06-profit-plus-fade.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-profit-plus-fade.json)

## Weak-Month Notes

`USD/JPY + fade` version:
- Weak month numbers: `1`, `2`, `10`
- Longest losing streak: `2`

`Profit + fade` version:
- Weak month numbers: `1`, `2`, `6`, `10`
- Longest losing streak: `1`

## Current Read

What improved:
- The borrowed idea was useful once adapted as a family, not copied raw.
- Overall profit increased meaningfully.
- The stable portfolio finally moved above `50%` win rate.

What is still not enough:
- Even the better portfolios are still only around `2,900` to `3,000` yen per month on average over the full sample.
- This is far below the target of `50,000+` yen net per month.

## Validation Gate

New tooling:
- [validation.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\validation.py)
- [test_validation.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\tests\test_validation.py)

Portable rules adopted from the brother repo:
- reject in simple order: `no_trades` -> `too_few_trades` -> `non_positive_total_pnl`
- rank train/test rows by `pass both` -> `pass test` -> `pass train` -> better test PnL -> lower test DD -> more test trades
- rank walk-forward aggregates by `accepted_both_windows` -> `accepted_test_windows` -> `total_test_profit` -> lower `worst_test_drawdown` -> more `total_test_trades`

### Candidate Latest Train/Test

Reference:
- [validation-2026-04-06-candidate-train-test.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-candidate-train-test.json)

Latest split pass:
- `day_midday_long_prev_night_up_trail`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`

Latest split fail:
- `day_opening_short_range_fade_lb8_buf2`
  - latest test `-1,100`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
  - too sparse on both windows

### Candidate Walk-Forward

Reference:
- [validation-2026-04-06-candidate-walk-forward.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-candidate-walk-forward.json)

Promotion read:
- `day_midday_long_prev_night_up_trail`
  - `accepted_both_windows 4/4`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`
  - `accepted_both_windows 3/4`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
  - `accepted_both_windows 1/4`
- `day_opening_short_range_fade_lb8_buf2`
  - `accepted_both_windows 0/4`

### Portfolio Walk-Forward

References:
- [validation-2026-04-06-portfolio-walk-forward-usdjpy-base.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-usdjpy-base.json)
- [validation-2026-04-06-portfolio-walk-forward-usdjpy-plus-fade.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-usdjpy-plus-fade.json)
- [validation-2026-04-06-portfolio-walk-forward-profit-base.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-profit-base.json)
- [validation-2026-04-06-portfolio-walk-forward-profit-plus-fade.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-profit-plus-fade.json)

Stable family:
- `USD/JPY base`
  - `accepted_both_windows 4/4`
  - `total_test_profit 39,450`
  - `worst_test_drawdown 8,250`
- `USD/JPY + fade`
  - `accepted_both_windows 4/4`
  - `total_test_profit 43,400`
  - `worst_test_drawdown 15,450`

Profit family:
- `profit base`
  - `accepted_both_windows 4/4`
  - `total_test_profit 45,000`
  - `worst_test_drawdown 10,000`
- `profit + fade`
  - `accepted_both_windows 4/4`
  - `total_test_profit 46,400`
  - `worst_test_drawdown 13,100`

Current interpretation:
- `fade` is not a promoted core rule yet
- `fade` is still useful as an optional portfolio overlay
- current promoted core pair is:
  - `day_midday_long_prev_night_up_trail`
  - `both_fast_short_night_tue_fri_usdjpy_down_tp`

Next research priorities:
1. Run month-specific filters for `1`, `2`, `6`, and `10`.
2. Test whether `fade` should be disabled in weak months instead of always-on.
3. Keep `day_morning_short_mon_thu_prev_night_down_tight_stop` as a conditional overlay until it passes more windows.

## Seasonal Filter Round 2

New diagnostics added:
- [portfolio_diagnostics.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\portfolio_diagnostics.py)
- [test_portfolio_diagnostics.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\tests\test_portfolio_diagnostics.py)

What changed:
- portfolio outputs now include per-strategy monthly PnL
- weak months were traced to the actual contributing rules instead of only the total portfolio
- new filtered candidates were added for:
  - `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10`
  - `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
  - `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_6_10_11_12`
  - `both_fast_short_night_tue_fri_tp_ex_2_6_10_11_12`
  - `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Single-rule read:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10`
  - `+31,900 / DD 4,000`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
  - `+21,200 / DD 2,950 / win_rate 68.33%`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`
  - `+29,000 / DD 4,000 / win_rate 59.01%`

References:
- [research-batch-2026-04-06-targeted-month-filters.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\research-batch-2026-04-06-targeted-month-filters.json)

### New Best Stable Portfolio

Candidates:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_6_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Result:
- `+95,400`
- `max_drawdown 6,700`
- `win_rate 53.36%`
- `22 profitable months / 3 losing months`
- weak month numbers: none in month-of-year summary

Walk-forward:
- `accepted_both_windows 4/4`
- `total_test_profit 62,750`
- `average_test_win_rate 54.07%`
- `worst_test_drawdown 6,700`

Files:
- [portfolio-research-2026-04-06-stable-seasonal-v3.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-stable-seasonal-v3.json)
- [portfolio-diagnostics-2026-04-06-stable-seasonal-v3.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-stable-seasonal-v3.json)
- [validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v3.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v3.json)

### New Best Profit Portfolio

Candidates:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_tp_ex_2_6_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Result:
- `+95,700`
- `max_drawdown 7,050`
- `win_rate 50.04%`
- `21 profitable months / 4 losing months`

Walk-forward:
- `accepted_both_windows 4/4`
- `total_test_profit 61,150`
- `average_test_win_rate 51.70%`
- `worst_test_drawdown 7,050`

Files:
- [portfolio-research-2026-04-06-profit-seasonal-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-profit-seasonal-v2.json)
- [portfolio-diagnostics-2026-04-06-profit-seasonal-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-profit-seasonal-v2.json)
- [validation-2026-04-06-portfolio-walk-forward-profit-seasonal-v2.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-profit-seasonal-v2.json)

Current read:
- the new stable portfolio is the best balance so far
- the filtered morning short and filtered fade both moved from optional overlays to core-quality support rules
- the filtered night short improved the portfolio only after month exclusions were made explicit
- monthly income is still far below the final target, but this is the clearest jump in robustness so far

## Metric Correction And Recheck

We corrected two issues before continuing research:
- monthly PnL now uses `trading_day` month instead of raw timestamp month for overnight session accounting
- `average_monthly_pnl` now divides by `active_months`, not only months that happened to trade

Files touched:
- [rule_lab.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\rule_lab.py)
- [portfolio_lab.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\portfolio_lab.py)
- [research.py](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\src\kanekasegi\research.py)

Post-fix baseline recheck:
- `day_midday_long_prev_night_up_trail_ex_1_2_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_10`
- Result: `+74,850 / max_drawdown 12,350 / win_rate 50.61% / 4/4 walk-forward pass`
- Files:
  - [portfolio-research-2026-04-06-usdjpy-plus-fade-both-ex-postfix.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-usdjpy-plus-fade-both-ex-postfix.json)
  - [validation-2026-04-06-portfolio-walk-forward-usdjpy-plus-fade-both-ex-postfix.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-usdjpy-plus-fade-both-ex-postfix.json)

## Current Best After Recheck

Candidates:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10`

Result:
- `+86,250`
- `max_drawdown 12,350`
- `win_rate 51.09%`
- `21 profitable months / 7 losing months`

Walk-forward:
- `accepted_both_windows 4/4`
- `total_test_profit 49,450`
- `average_test_win_rate 49.98%`
- `worst_test_drawdown 12,350`

Diagnostics:
- weak month numbers are now mostly `2` and `10`
- worst month contributors are centered on the night short and the morning short, not the midday long anymore

## Current Best Residual Search

We pushed one more step from `stable_seasonal_v3` by trimming the remaining weak-month exposure on the USD/JPY-filtered night short.

Candidates:
- `day_midday_long_prev_night_up_trail_ex_1_2_4_9_10`
- `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
- `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
- `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_8_10`

Result:
- `+99,000`
- `max_drawdown 5,400`
- `win_rate 54.66%`
- `21 profitable months / 4 losing months`

Walk-forward:
- `accepted_both_windows 4/4`
- `total_test_profit 67,000`
- `average_test_win_rate 56.78%`
- `worst_test_drawdown 5,400`

What improved versus `stable_seasonal_v3`:
- profit improved from `95,400` to `99,000`
- drawdown improved from `6,700` to `5,400`
- walk-forward total test profit improved from `62,750` to `67,000`

Residual read:
- remaining negative months are `2024-04`, `2025-06`, `2023-11`, and a very small `2023-09`
- the largest remaining drag is still the fade rule in `2024-04`
- the next drag after that is the midday long in `2025-06`

Files:
- [portfolio-research-2026-04-06-stable-seasonal-v4.json](C:\Users\issin\OneDrive\繝・せ繧ｯ繝医ャ繝予kanekasegi\results\portfolio-research-2026-04-06-stable-seasonal-v4.json)
- [validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v4.json](C:\Users\issin\OneDrive\繝・せ繧ｯ繝医ャ繝予kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-stable-seasonal-v4.json)
- [portfolio-diagnostics-2026-04-06-stable-seasonal-v4.json](C:\Users\issin\OneDrive\繝・せ繧ｯ繝医ャ繝予kanekasegi\results\portfolio-diagnostics-2026-04-06-stable-seasonal-v4.json)
- [portfolio-research-2026-04-06-stable-seasonal-v3-residual-search.json](C:\Users\issin\OneDrive\繝・せ繧ｯ繝医ャ繝予kanekasegi\results\portfolio-research-2026-04-06-stable-seasonal-v3-residual-search.json)

Files:
- [portfolio-research-2026-04-06-stable-tightened.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-research-2026-04-06-stable-tightened.json)
- [validation-2026-04-06-portfolio-walk-forward-stable-tightened.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\validation-2026-04-06-portfolio-walk-forward-stable-tightened.json)
- [portfolio-diagnostics-2026-04-06-stable-tightened.json](C:\Users\issin\OneDrive\デスクトップ\kanekasegi\results\portfolio-diagnostics-2026-04-06-stable-tightened.json)
