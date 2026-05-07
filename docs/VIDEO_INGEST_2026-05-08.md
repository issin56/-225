# Video Ingest 2026-05-08

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official education videos/pages. No SBI official item with more directly testable Nikkei 225 Micro rule content surfaced above this JPX set during this run.

## Intake

1. `JPX` [２．日経225micro・ミニオプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/242opdelta.html)
   - usable_hypothesis: `new product structure should be translated into explicit rule scopes rather than broad portfolio rewrites`
   - test_shape: `keep new Nikkei 225 Micro ideas limited to deterministic sleeve swaps, month filters, calendar filters, and factor gates`
   - rejected: `product-overview commentary without a deterministic trigger is not directly backtestable`

2. `JPX` [３．日経225microの活用方法](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/243opdelta.html)
   - usable_hypothesis: `micro contracts are most useful as scenario-specific overlays, not as always-on replacements`
   - test_shape: `prefer sparse repair sleeves and narrow conditional replacements over broad six-sleeve redesigns`
   - rejected: `generic case-study narration without a parameterized entry condition is not sufficient for local testing`

3. `JPX` [日経225マイクロ先物を使った戦略その１](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga1.html)
   - usable_hypothesis: `one strategic thesis should map to one explicit rule family at a time`
   - test_shape: `continue running small single-family batches instead of mixing multiple new assumptions into one rerun`
   - rejected: `broad strategic framing without exact timing or gating logic is not promotable on its own`

4. `JPX` [日経225マイクロ先物を使った戦略その２](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga2.html)
   - usable_hypothesis: `different market scenarios should stay segmented into separate branches instead of one blended sleeve`
   - test_shape: `keep up/down, volatility, and calendar ideas isolated in separate validation batches`
   - rejected: `discretionary market-reading guidance without a hard rule boundary cannot be replayed reproducibly`

5. `JPX` [日経225マイクロ先物を使った戦略その３](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga3.html)
   - usable_hypothesis: `risk-hedge ideas should tighten downside controls, not merely add complexity`
   - test_shape: `continue rejecting same-lane challengers that widen drawdown or reduce balance safety for trivial OOS gain`
   - rejected: `manual hedge discretion is outside the current futures-only replay harness`

6. `JPX` [相場予想パターン別投資戦略厳選6選](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/260.html)
   - usable_hypothesis: `scenario-specific market views belong in explicit hypothesis buckets such as up, down, range, and high-volatility`
   - test_shape: `continue converting market-view ideas only into parameterized direction, range, and volatility filters that can be validated sleeve by sleeve`
   - rejected: `options-combination mechanics and IV-specific payoff shaping are outside the current futures-only simulator`

## Research Handling

- Accepted only hypotheses that map to local parameters or existing acceptance logic: sleeve isolation, calendar filters, drawdown controls, scenario segmentation, and sparse overlay design.
- Rejected ideas that depend on option pricing, discretionary hedge management, or payoff-shape mechanics that the current futures-only harness does not model directly.

## Result

- Daily quota for `2026-05-08` was met with exactly `6` official-source videos/pages.
- The accepted takeaways reinforced the current research discipline rather than opening a new unrelated branch:
  - keep hypotheses one-family-at-a-time
  - keep micro usage sparse and scenario-specific
  - keep downside guardrails above marginal OOS gains
  - keep directional and volatility ideas segregated into explicit test batches
