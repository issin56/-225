# Video Ingest 2026-05-04

## Status

- Intended daily target: `6` market-related videos in JST.
- Actual ingested in this run: `6`.
- Source mix: `6` JPX official videos/pages from OSE's Kitahama Investment School; SBI did not surface a clearer Nikkei 225 Micro research input than the JPX primary material during this run.

## Intake

1. `JPX` [２．日経225micro・ミニオプションとは？](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/242opdelta.html)
   - usable_hypothesis: `micro products should be used for precise sleeves and capital-efficient overlays, not broad always-on rewrites`
   - test_shape: `keep same-lane work focused on single-sleeve swaps and small bundle adjustments`
   - rejected: `options-specific usage examples remain outside the futures-only simulator`

2. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - episode: `第1回「知ってお得！先物・オプション」`
   - usable_hypothesis: `only ideas reducible to explicit month, session, range, or calendar rules should enter the research queue`
   - test_shape: `continue rejecting broad discretionary commentary that cannot become a reproducible candidate or bundle rerun`
   - rejected: `general beginner education without a deterministic trigger is not directly backtestable`

3. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - episode: `第4回「「SQ」を知る…バーチャル株価とリアル株価、一瞬の出会い」`
   - usable_hypothesis: `SQ behavior belongs in narrow calendar overlays only`
   - test_shape: `keep SQ handling limited to explicit ex_sq sleeves and avoid generalizing it into unrelated day-session rules`
   - rejected: `settlement-process explanation beyond existing calendar flags is outside the local futures harness`

4. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - episode: `第7回「7月限の失敗から学ぶ」`
   - usable_hypothesis: `contract-month failures should be modeled as explicit month or calendar exclusions, not as ex-post discretionary excuses`
   - test_shape: `continue preferring explicit excluded_months or calendar-filter candidates over narrative explanations for weak windows`
   - rejected: `manual judgement around why a specific trade failed is not reproducible by the backtester`

5. `JPX` [先物・オプション道場225](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html)
   - episode: `第8回「二手目、三手目を考える！」`
   - usable_hypothesis: `multi-step scenario thinking is only acceptable when reduced to fixed candidate-set or bundle rerun validation`
   - test_shape: `continue rejecting manual rescue logic and validate alternate paths only through deterministic reruns`
   - rejected: `human in-trade intervention trees cannot be replayed safely in automated research`

6. `JPX` [北浜博士のデリバティブ教室 in STOCKVOICE｜好評放映中！](https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/dr_kitahama.html)
   - episode: `2025年6月16日放送：デリバティブのミニ商品`
   - usable_hypothesis: `mini and micro products fit sparse capital-aware sleeves better than large broad exposures`
   - test_shape: `preserve hard drawdown and available-balance guardrails when evaluating sparse micro overlays`
   - rejected: `product-overview commentary alone does not justify a new unrelated rule family`

## Research Handling

- Accepted only ideas that map directly to existing local levers: `excluded_months`, `calendar_filter`, sparse sleeve replacement, and fixed-bundle validation.
- Rejected ideas that depend on discretionary trade rescue, option-specific mechanics, or general education that cannot be converted into deterministic research inputs.

## Result

- Daily quota for `2026-05-04` was met with exactly `6` official-source videos/pages.
- The accepted takeaways reinforced the current promoted-lane discipline:
  - keep micro usage sparse and capital-aware
  - keep SQ handling calendar-limited
  - model weak contract-month behavior explicitly
  - reject manual rescue logic in favor of reproducible reruns
