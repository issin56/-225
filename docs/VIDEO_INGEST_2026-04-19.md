# Video Ingest 2026-04-19

Source priority was satisfied with 6 JPX official archive videos from the Osaka Exchange education series:
- Series page: https://www.jpx.co.jp/ose-toshijuku/movie/futures_option/options_dojo_225.html

## Ingested Videos

1. `JPX / 先物・オプション道場225 第1回`
   - title: `知ってお得！先物・オプション`
   - aired: `2025-04-11`
   - research outcome: rejected
   - reason: introductory product education only; no rule-shaped trigger, filter, or risk parameter was extractable from the available metadata.

2. `JPX / 先物・オプション道場225 第2回`
   - title: `オプション取引の本質はボラティリティ取引だ`
   - aired: `2025-04-25`
   - research-usable hypothesis: `opening fade` and `midday breakout` should stay volatility-regime aware rather than all-weather.
   - testable translation in current harness: prefer `VIX` and prior-session-range filters when evaluating April opening or June breakout specialists.

3. `JPX / 先物・オプション道場225 第3回`
   - title: `裁定業者（アービトラージ）とは`
   - aired: `2025-05-16`
   - research outcome: rejected
   - reason: the available metadata implies microstructure discussion, but no clean, currently encodable rule was available without inventing a proxy.

4. `JPX / 先物・オプション道場225 第4回`
   - title: `「SQ」を知る…バーチャル株価とリアル株価、一瞬の出会い`
   - aired: `2025-05-30`
   - research-usable hypothesis: SQ day or SQ-adjacent sessions may distort opening behavior enough to warrant separate handling.
   - current status: logged but not tested because the present harness has no SQ calendar flag.

5. `JPX / 先物・オプション道場225 第7回`
   - title: `7月限の失敗から学ぶ`
   - aired: `2025-07-11`
   - research-usable hypothesis: expiry/roll-context mistakes cluster around scenario drift, so month/contract-regime handling matters more than broad all-month deployment.
   - current status: partially covered by existing month exclusions; no new isolated encoding was justified today.

6. `JPX / 先物・オプション道場225 第9回`
   - title: `シナリオから外れた時の対処法を学ぶ`
   - aired: `2025-08-08`
   - research-usable hypothesis: failed-scenario handling should bias toward stricter time/risk exits instead of wider opportunity windows.
   - testable translation in current harness: retry only the already-supported `prior_night_down + vix_up` April opening specialist rather than broadening entry windows.

## Test Run Triggered By Video Intake

- Baseline kept: `lot3_base10_june_t8`
- Tested candidate: `day_opening_short_range_fade_prev_night_down_lb8_buf2_only_4_t16_vix_up`
- Comparison files:
  - `results/portfolio-research-2026-04-19-lot3_base10_june_t8-video-regime-rerun.json`
  - `results/portfolio-research-2026-04-19-lot3-opening-april-prevnightdown-vix-current-macro.json`
  - `results/portfolio-research-2026-04-19-lot3-opening-april-prevnightdown-vix-current-summary.json`
- Decision: reject
- Why: profit dropped `232850.0 -> 229100.0`, drawdown stayed flat at `13300.0`, `2024-04` was effectively unchanged (`1450.0 -> 1400.0`), and `2025-04` weakened materially (`23800.0 -> 20100.0`).

## Next Video-Driven Research Queue

- `SQ` filter support is the cleanest untested official-source idea, but it needs explicit calendar support before backtesting.
- Until that exists, keep using volatility/range filters only where the harness already supports them.
