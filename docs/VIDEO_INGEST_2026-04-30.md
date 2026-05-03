# Video Ingest 2026-04-30

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official education videos; no SBI official video with equally direct Nikkei 225 Micro rule content surfaced in the accessible official-source set used for this run.

## Intake

1. `JPX` [日経225マイクロ先物を使った投資戦略その1](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga1.html)
   - usable_hypothesis: `April opening overlays should stay hard-gated by explicit structure instead of widening into a generic opening sleeve`
   - test_shape: `keep only near-neighbor range or calendar gates around the current opening April branch`
   - rejected: `speaker-specific execution nuance without a parameterized trigger is not reproducible locally`

2. `JPX` [日経225マイクロ先物を使った投資戦略その2](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga2.html)
   - usable_hypothesis: `micro overlays are most useful as sparse opportunity capture rather than full portfolio replacement`
   - test_shape: `continue prioritizing sleeve swaps and month-limited add-ons over whole-bundle rewrites`

3. `JPX` [日経225マイクロ先物を使った投資戦略その3](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/Micro_N225Futures_Fukunaga3.html)
   - usable_hypothesis: `defensive micro usage should remain regime-limited and explicit`
   - test_shape: `keep calendar, prior-session, and macro gates narrow when testing defensive overlays`
   - rejected: `cash-equity hedge examples do not map to the current futures-only simulator`

4. `JPX` [オプションと先物の基礎](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/241opdelta.html)
   - usable_hypothesis: `only ideas expressible as explicit time, range, or contract-mechanics rules should enter the queue`
   - test_shape: `reject narrative-only hypotheses and keep rule intake parameterized`
   - rejected: `options-specific greek or surface concepts are outside the local research harness`

5. `JPX` [相場に関する情報収集について](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga7.html)
   - usable_hypothesis: `external context should enter the model as checklist-like factor gates, not discretionary commentary`
   - test_shape: `continue using only reproducible factors such as VIX, USDJPY, US10Y, and explicit calendar filters`
   - rejected: `free-form market narrative cannot be replayed deterministically`

6. `JPX` [オプション道場 225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - usable_hypothesis: `SQ behavior belongs in explicit calendar handling rather than broad all-month logic`
   - test_shape: `keep SQ exclusion and other contract-calendar rules as narrow overlays only`
   - rejected: `option-structure trade selection is outside the futures-only rule set`

## Research Handling

- Accepted only hypotheses that map to local parameters already represented in the harness: range thresholds, month windows, SQ handling, prior-session filters, and explicit macro yes/no gates.
- Rejected ideas that depend on discretionary execution, option greeks, or non-futures inventory assumptions.

## Result

- Daily quota for `2026-04-30` was met with exactly `6` official-source videos.
- The accepted takeaways reinforced the current research lane rather than opening a new unrelated branch:
  - keep April opening logic sparse
  - keep external-state inputs explicit
  - keep defensive logic regime-limited
  - keep SQ handling calendar-specific
