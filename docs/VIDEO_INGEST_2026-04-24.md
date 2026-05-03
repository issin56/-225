# Video Ingest 2026-04-24

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` official JPX videos. No SBI video with comparably usable Nikkei 225 micro rule content surfaced in the accessible official search results for this run.

## Intake

1. `JPX` [１．先物・オプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/241opdelta.html)
   - usable_hypothesis: `researchable ideas must reduce to explicit time, session, calendar, and direction rules rather than narrative trade judgment`
   - test_shape: `continue accepting only month filters, session windows, macro yes/no gates, and explicit SQ handling in the local harness`
   - rejected: `broad educational explanation of derivatives mechanics is not itself a parameterized signal`

2. `JPX` [２．日経225micro・ミニオプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/242opdelta.html)
   - usable_hypothesis: `micro-sized contracts are best used for smaller, targeted overlays rather than for broad always-on portfolio rewrites`
   - test_shape: `keep prioritizing sparse sleeve-level repairs over unrelated full-bundle replacements`
   - rejected: `product-overview commentary without a rule toggle does not create a new backtest branch`

3. `JPX` [日経225マイクロ先物を使った戦略その１](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga1.html)
   - usable_hypothesis: `micro overlays should keep a hard structural gate before entry instead of trading every nominal opportunity`
   - test_shape: `continue testing only narrow opening-range and calendar-gated overlays around the live opening sleeves`
   - rejected: `speaker-specific discretionary examples are not reproducible in the local harness`

4. `JPX` [日経平均VIコンテンツ（2）「日経平均VI買い＋日経225マイクロ先物買い戦略」](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/255opdelta.html)
   - usable_hypothesis: `defensive overlays belong in explicit stress or regime filters, not in generic daily sleeves`
   - test_shape: `keep defensive micro-futures ideas limited to explicit calendar or macro states such as SQ handling and narrow VIX-style gates`
   - rejected: `options-and-vi package trades that require instruments outside the futures-only simulator are not testable locally`

5. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - usable_hypothesis: `SQ-driven behavior should stay in explicit contract-calendar handling rather than leaking into broad session logic`
   - test_shape: `continue treating SQ exclusion and other expiry-adjacent behavior as narrow calendar toggles only`
   - rejected: `episode-level options tactics and volatility-structure judgment are outside the current futures-only portfolio harness`

6. `JPX` [〖動画1〗個別株の長期投資におけるリスクをヘッジする戦略](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/261.html)
   - usable_hypothesis: `hedge-style micro usage should remain sparse, purpose-built, and size-aware rather than permanently allocated`
   - test_shape: `keep hedge-like ideas limited to identifiable weak-month or event windows instead of turning them into broad replacements`
   - rejected: `cash-equity inventory hedging examples are not directly testable in the current futures-only simulator`

## Research Handling

- Accepted only hypotheses that map to parameters already represented in the local research harness: session windows, weekday/month masks, prior-session filters, external-factor yes/no gates, and explicit SQ or contract-calendar handling.
- Rejected ideas that depend on option greeks, implied-volatility surface management, discretionary commentary, or a standing cash-equity inventory.

## Result

- Daily quota for `2026-04-24` was met with exactly `6` official-source videos.
- The accepted takeaways reinforced the current promoted-leader discipline rather than opening a new unrelated branch:
  - keep overlays sparse
  - keep calendar handling explicit
  - keep defensive logic regime-limited
  - keep only parameterized ideas in the local harness
