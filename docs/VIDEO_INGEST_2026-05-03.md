# Video Ingest 2026-05-03

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official education videos; no SBI official video with directly testable Nikkei 225 Micro rule content surfaced more clearly than the JPX set during this run.

## Intake

1. `JPX` [１．先物・オプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/241opdelta.html)
   - usable_hypothesis: `only ideas that can be parameterized as explicit time, direction, range, or calendar rules should enter the futures-only rule search`
   - test_shape: `continue rejecting discretionary commentary and keep same-lane work limited to explicit sleeve swaps and gate changes`
   - rejected: `broad product education without a parameterized trigger is not directly backtestable`

2. `JPX` [２．日経225micro・ミニオプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/242opdelta.html)
   - usable_hypothesis: `micro-sized products are best used for sparse, precise overlays rather than broad always-on rewrites`
   - test_shape: `prefer narrow repair sleeves and single-sleeve replacements over whole-portfolio redesigns`
   - rejected: `options-specific usage examples are outside the current futures-only simulator`

3. `JPX` [（３）値下がりリスクとの向き合い方](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/N225Futures_Fukunaga3.html)
   - usable_hypothesis: `downside control should be handled with explicit defensive filters or promotion guardrails, not by tolerating larger bundle drawdowns`
   - test_shape: `keep rejecting same-lane challengers that raise drawdown beyond the promoted leader even if test profit improves`
   - rejected: `investor-psychology advice without a deterministic trigger is not reproducible locally`

4. `JPX` [新証拠金計算方式（VaR: Value at Risk）の要点](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/varmargin.html)
   - usable_hypothesis: `margin-aware guardrails matter as much as headline profit when evaluating micro futures bundles`
   - test_shape: `continue requiring acceptable drawdown and minimum available balance before considering any promotion`
   - rejected: `clearing-specific margin mechanics are not modeled line-by-line in the local backtester`

5. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - episode: `第4回「「SQ」を知る…バーチャル株価とリアル株価、一瞬の出会い」`
   - usable_hypothesis: `SQ behavior belongs in explicit calendar handling, not in a generic daily sleeve`
   - test_shape: `keep using SQ exclusion only as a narrow calendar overlay and do not generalize it into unrelated sleeves`
   - rejected: `option-settlement detail beyond explicit SQ calendar flags is outside the current futures harness`

6. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - episode: `第9回「シナリオから外れた時の対処法を学ぶ」`
   - usable_hypothesis: `promotion should require robust multi-window behavior rather than a single attractive scenario`
   - test_shape: `keep multi-window validation as a hard gate and reject single-window-dependent same-lane challengers`
   - rejected: `manual scenario management steps are not directly executable in automated rule replay`

## Research Handling

- Accepted only hypotheses that map to local parameters or existing acceptance logic: calendar filters, month filters, drawdown limits, trade-density gates, and walk-forward robustness.
- Rejected ideas that depend on option greeks, discretionary scenario handling, or broker-specific margin implementation detail that the current futures-only harness does not simulate directly.

## Result

- Daily quota for `2026-05-03` was met with exactly `6` official-source videos.
- The accepted takeaways reinforced the current research discipline rather than opening a new unrelated branch:
  - keep same-lane work sparse and explicit
  - keep SQ handling calendar-limited
  - keep drawdown and margin guardrails hard
  - keep multi-window robustness above one-off scenario wins
