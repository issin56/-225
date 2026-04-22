# Video Ingest 2026-04-20

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official education videos; no SBI video with comparable Nikkei 225 Micro rule content surfaced in this run's accessible search results.

## Intake

1. `JPX` [日経225マイクロ先物を使った戦略その１](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga1.html)
   - usable_hypothesis: `opening specialists should keep a hard range/price-structure gate instead of firing on every day-open print`
   - test_shape: `retest tighter prior-session-range and opening-range thresholds on the April opening branch`
   - rejected: `order-book reading claims are not directly reproducible from the local OHLC + factor dataset`

2. `JPX` [日経225マイクロ先物を使った戦略その２](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga2.html)
   - usable_hypothesis: `buy-side and sell-side opening logic should stay directionally split and regime-gated rather than merged into a symmetric rule`
   - test_shape: `continue testing opening replacement legs as narrow short-side April overlays instead of broad both-direction swaps`

3. `JPX` [日経225マイクロ先物を使った戦略その３](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga3.html)
   - rejected: `spot-inventory downside hedge ideas are not directly testable in the current flat-to-flat micro-futures portfolio harness`

4. `JPX` [日経225micro・ミニオプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/242opdelta.html)
   - usable_hypothesis: `small-contract products are best used for sparse overlays where the core book stays untouched and the add-on only appears in narrow calendar windows`
   - test_shape: `keep favoring month-only or event-day specialists with strict walk-forward gating over broad always-on replacements`
   - rejected: `mini-option structure ideas are outside the current futures-only local simulator`

5. `JPX` [日経225microの活用方法](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/243opdelta.html)
   - usable_hypothesis: `micro sizing supports low-frequency weak-month repair legs, but only if the overlay is small enough not to distort the rest of the portfolio`
   - test_shape: `continue narrow weak-month probes like June-only or April-only swaps and reject portfolio-wide rewrites`

6. `JPX` [〖動画1〗個別株の長期投資におけるリスクをヘッジする戦略](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/261.html)
   - usable_hypothesis: `hedge-style overlays belong in explicit defensive regimes rather than permanent allocation`
   - test_shape: `when testing defensive opening or June swaps, prefer event-limited overlays such as SQ exclusion or month-only specialists`
   - rejected: `cash-equity inventory assumptions are not present in the current research harness`

## Research Handling

- Accepted only hypotheses that can map to local parameters already represented in the rule lab: month filters, calendar filters, direction splits, prior-session gates, and sparse overlay logic.
- Rejected all ideas that require live order-book state, option pricing/greeks, or an external cash-equity inventory.

## Result

- Daily quota for `2026-04-20` was met with `6` official-source videos.
- The accepted video takeaways reinforced the existing research direction rather than introducing a new unrelated branch:
  - keep overlays sparse
  - keep directionality split
  - keep range/regime gates explicit
  - reject non-reproducible discretionary inputs
