# Video Ingest 2026-04-23

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official videos. No SBI video with comparable Nikkei 225 Micro rule content surfaced in this run's accessible official-source review.

## Intake

1. `JPX` [１．先物・オプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/241opdelta.html)
   - usable_hypothesis: `new rule ideas must stay expressible as explicit contract, time-window, and risk-limit parameters`
   - test_shape: `reject discretionary market commentary and keep only reproducible range, month, weekday, and macro yes/no gates`
   - rejected: `broad educational explanation without a parameterized trigger is not directly testable`

2. `JPX` [２．日経225micro・ミニオプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/242opdelta.html)
   - usable_hypothesis: `micro contracts are most useful as size-granular overlays rather than whole-portfolio rewrites`
   - test_shape: `continue prioritizing single-sleeve replacements or narrow add-ons over multi-sleeve redesigns`
   - rejected: `option-specific mechanics are outside the current futures-only harness`

3. `JPX` [３．日経225microの活用方法](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/243opdelta.html)
   - usable_hypothesis: `micro use cases should remain case-limited and scenario-specific instead of always-on`
   - test_shape: `keep overlays tied to explicit months, SQ handling, or isolated weak-month repair attempts`
   - rejected: `narrative case studies without deterministic filters cannot be replayed locally`

4. `JPX` [225マイクロ先物を使った戦略①～チャートと板の見方について～](https://www.youtube.com/watch?v=XYl_gxam754)
   - usable_hypothesis: `entry logic should rely on pre-defined price structure rather than discretionary board reading`
   - test_shape: `preserve hard opening-range and prior-range gates when revisiting opening or midday sleeves`
   - rejected: `real-time tape interpretation and board nuance are not reproducible in the local simulator`

5. `JPX` [225マイクロ先物を使った戦略②～売り,買いで収益機会を狙う～](https://www.youtube.com/watch?v=1dKRaFO-vM0)
   - usable_hypothesis: `micro opportunity capture should stay directional and time-window specific`
   - test_shape: `continue testing sparse night-session timing splits and explicit directional sleeves instead of broadening session scope`
   - rejected: `general trading mindset advice without a fixed gate is not testable`

6. `JPX` [225マイクロ先物を使った戦略③～値下がりリスクをヘッジする～](https://www.youtube.com/watch?v=s0sez5-sJEo)
   - usable_hypothesis: `hedge-style micro sleeves should remain defensive, sparse, and regime-limited`
   - test_shape: `keep defensive night or April overlays bound to narrow month sets, prior-session filters, or explicit drawdown-aware gates`
   - rejected: `cash-equity hedge examples are outside the current futures-only portfolio harness`

## Research Handling

- Accepted only hypotheses that map cleanly to the local research harness: month exclusions, weekday filters, session windows, prior-range gates, prior-session direction, and explicit macro filters.
- Rejected ideas that depend on option pricing, discretionary tape reading, or a cash-equity inventory to hedge.

## Result

- Daily quota for `2026-04-23` was met with exactly `6` official-source videos.
- The accepted takeaways reinforced the current research discipline:
  - keep overlays sparse
  - keep night timing changes narrow and testable
  - keep defensive logic explicitly bounded
  - reject non-parameterized discretion
