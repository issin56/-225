# Video Hypotheses 2026-05-08

## Accepted

- `video_explicit_scope_bias`
  - source: `JPX ２．日経225micro・ミニオプションとは？`
  - hypothesis: `new product ideas should enter research only as explicit rule scopes`
  - local_test_mapping: `continue limiting same-lane work to deterministic sleeve swaps, factor gates, and calendar filters`

- `video_sparse_micro_overlay_bias_refresh`
  - source: `JPX ３．日経225microの活用方法`
  - hypothesis: `micro contracts are more useful as sparse overlays than broad always-on replacements`
  - local_test_mapping: `keep favoring targeted repair sleeves over full-portfolio redesigns`

- `video_single_thesis_batching_bias`
  - source: `JPX 日経225マイクロ先物を使った戦略その１`
  - hypothesis: `each research batch should test one strategic thesis at a time`
  - local_test_mapping: `keep batch construction narrow so the winner/loser signal is attributable to one hypothesis family`

- `video_scenario_segmentation_bias`
  - source: `JPX 日経225マイクロ先物を使った戦略その２`
  - hypothesis: `bullish, bearish, range, and volatility views should remain separated into explicit branches`
  - local_test_mapping: `continue isolating direction, volatility, and calendar ideas in separate walk-forward batches`

- `video_risk_hedge_guardrail_bias`
  - source: `JPX 日経225マイクロ先物を使った戦略その３`
  - hypothesis: `added complexity is acceptable only if downside control or robustness improves materially`
  - local_test_mapping: `keep rejecting same-lane challengers that add complexity while failing to improve drawdown safety or reproducibility`

- `video_market_view_bucket_bias`
  - source: `JPX 相場予想パターン別投資戦略厳選6選`
  - hypothesis: `market-view ideas should be translated into explicit direction/range/volatility buckets before testing`
  - local_test_mapping: `admit only parameterized direction, range, or volatility gates; reject narrative market calls`

## Rejected

- `video_product_overview_without_trigger`
  - reason: `basic product explanation is useful context but not a testable rule without a deterministic trigger`

- `video_discretionary_hedge_management`
  - reason: `manual hedge adjustments cannot be replayed consistently in the current backtest harness`

- `video_option_payoff_shape_mechanics`
  - reason: `option combination and IV payoff mechanics are outside the current futures-only simulator`
