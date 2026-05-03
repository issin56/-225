# Video Ingest 2026-04-25

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official education videos; the comparable SBI official futures page checked during this run was under maintenance, so no SBI video was usable.

## Intake

1. `JPX` [（１）日経225の指数と先物取引について](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga1.html)
   - usable_hypothesis: `index futures research should keep contract mechanics, session boundaries, and calendar handling explicit instead of blending day and night behavior into one generic rule`
   - test_shape: `continue evaluating day-session and night-session sleeves separately, and keep SQ or contract-calendar logic explicit on opening branches`
   - rejected: `broad introductory product explanations without a parameterized session or calendar rule do not add a new standalone trading edge`

2. `JPX` [（２）日経225や個別銘柄との関係について](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga2.html)
   - usable_hypothesis: `equity-index relationships should enter the harness only through reproducible index-level filters, not discretionary single-stock reading`
   - test_shape: `keep stock-specific discretion out of the queue and allow only explicit index, month, time, and external-factor gates`
   - rejected: `component-stock storytelling is not replayable in the current futures-only simulator`

3. `JPX` [（４）どんな人が日経225先物取引を始められるか？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga4.html)
   - usable_hypothesis: `for smaller-account use, sparse overlays with controlled drawdown are preferable to broad higher-frequency rewrites`
   - test_shape: `continue rejecting candidates that widen drawdown or require materially higher trade density just to add headline profit`
   - rejected: `general onboarding guidance is not a testable signal without an explicit rule parameter`

4. `JPX` [（５）日経225先物を始めると見えてくる世界](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga5.html)
   - usable_hypothesis: `participant-flow and overseas context should only be represented through explicit reproducible proxies already in the harness`
   - test_shape: `keep USDJPY, VIX, US10Y, and calendar filters as the only allowed external-state inputs instead of narrative investor-flow interpretation`
   - rejected: `qualitative discussion of overseas investors is not deterministic enough for direct rule insertion`

5. `JPX` [（６）一歩進んだ先物利用法](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga6.html)
   - usable_hypothesis: `night-session usage should be tested with explicit subwindow splits rather than assuming the whole night behaves uniformly`
   - test_shape: `check front-half and US-overlap night variants separately against the live night sleeve instead of broadening the entire session`
   - rejected: `advanced discretionary usage examples without explicit time slicing cannot be validated locally`

6. `JPX` [（９）他の商品を利用した方が良いケース](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga9.html)
   - usable_hypothesis: `if a setup is structurally more suitable for options or another product, the futures harness should reject it instead of forcing a futures rule`
   - test_shape: `keep rejecting options-shaped or cross-product ideas and stay within explicit futures-only session, month, and macro gates`
   - rejected: `options-choice decision rules are outside the current futures-only simulator`

## Research Handling

- Accepted only hypotheses that can be inferred from the official page descriptions and mapped to local parameters already represented in the harness: session windows, month masks, explicit calendar handling, and reproducible macro yes/no filters.
- Rejected ideas that rely on discretionary investor-flow interpretation, single-stock storytelling, leverage coaching, or product-selection logic outside the current futures-only rule set.

## Result

- Daily quota for `2026-04-25` was met with exactly `6` official-source videos.
- The accepted takeaways reinforced the current research discipline rather than opening an unrelated branch:
  - keep day and night logic explicitly separated
  - keep contract-calendar handling explicit
  - keep external context reproducible
  - keep options-shaped ideas out of the futures-only queue
