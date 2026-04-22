# Video Ingest 2026-04-22

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official education videos; no SBI video with comparable Nikkei 225 Micro rule content surfaced in this run's accessible official-source search results.

## Intake

1. `JPX` [日経225マイクロ先物を使った戦略その１](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga1.html)
   - usable_hypothesis: `opening-side micro overlays should keep a hard price-structure gate instead of trading every April open`
   - test_shape: `retest only the closest opening-range and volatility-threshold neighbors around the promoted April sleeve`
   - rejected: `discretionary case-study interpretation without explicit range or calendar rules is not reproducible in the local harness`

2. `JPX` [日経225マイクロ先物を使った戦略その２](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga2.html)
   - usable_hypothesis: `micro contracts are better suited to sparse opportunity capture than broad always-on replacement logic`
   - test_shape: `continue preferring narrow month-only, event-only, or sleeve-only overlays over whole-portfolio rewrites`

3. `JPX` [日経225マイクロ先物を使った戦略その３](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga3.html)
   - usable_hypothesis: `hedge-style micro usage should stay explicitly defensive and limited to identifiable regimes`
   - test_shape: `keep defensive overlays tied to month windows, SQ exclusions, or explicit macro filters rather than permanent allocation`
   - rejected: `cash-equity inventory hedge examples are not directly testable in the current futures-only simulator`

4. `JPX` [１．先物・オプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/241opdelta.html)
   - usable_hypothesis: `researchable micro-futures ideas should be expressible with explicit contract, time-window, and range rules`
   - test_shape: `reject hypotheses that depend on discretionary execution detail and keep only time/range/month/macro gates`
   - rejected: `options-specific structure ideas are outside the current futures-only portfolio harness`

5. `JPX` [（７）先物取引に関連する情報収集について](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga7.html)
   - usable_hypothesis: `external information should enter the model as explicit checklist gates rather than narrative discretion`
   - test_shape: `continue only with reproducible factor gates already represented locally such as VIX, USDJPY, US10Y, and calendar filters`
   - rejected: `free-form macro commentary cannot be replayed deterministically in backtests`

6. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - usable_hypothesis: `SQ-related behavior belongs in explicit calendar handling, not in a generic daily sleeve`
   - test_shape: `keep using SQ exclusion or other narrow calendar-limited overlays when testing defensive April variants`
   - rejected: `option-price and volatility-surface tactics are outside the current futures-only simulator`

## Research Handling

- Accepted only hypotheses that map to local parameters already represented in the research harness: range thresholds, month windows, direction splits, macro yes/no filters, and explicit SQ handling.
- Rejected ideas that require option greeks, discretionary tape reading, or a cash-equity hedge book.

## Result

- Daily quota for `2026-04-22` was met with exactly `6` official-source videos.
- The accepted takeaways reinforced the existing promoted-leader discipline rather than opening a new unrelated branch:
  - keep overlays sparse
  - keep April opening logic explicitly gated
  - keep external information reproducible
  - keep SQ and defensive logic calendar-limited
