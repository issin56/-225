# Video Hypotheses 2026-05-04

## Accepted

- `video_micro_sparse_overlay_bias_refresh`
  - source: `JPX ２．日経225micro・ミニオプションとは？`
  - hypothesis: `micro products are best used as sparse and precise sleeves, not broad replacements`
  - local_test_mapping: `keep promotion work limited to single-sleeve swaps and tightly scoped bundle reruns`

- `video_parameterized_rule_bias_refresh`
  - source: `JPX 先物・オプション道場225 第1回`
  - hypothesis: `only parameterized session, month, range, and calendar ideas should enter the queue`
  - local_test_mapping: `continue rejecting non-deterministic commentary from the candidate lane`

- `video_sq_calendar_bias_refresh`
  - source: `JPX 先物・オプション道場225 第4回`
  - hypothesis: `SQ-specific behavior belongs in explicit calendar overlays only`
  - local_test_mapping: `keep ex_sq logic narrow and avoid spreading SQ handling into unrelated sleeves`

- `video_contract_month_failure_bias`
  - source: `JPX 先物・オプション道場225 第7回`
  - hypothesis: `contract-month weakness should be captured with explicit exclusions rather than narrative excuses`
  - local_test_mapping: `prefer excluded_months and calendar-filter tests when a weak-window pattern is persistent`

- `video_deterministic_multistep_bias`
  - source: `JPX 先物・オプション道場225 第8回`
  - hypothesis: `alternative scenario paths are acceptable only when converted into deterministic reruns`
  - local_test_mapping: `treat bundle reruns as the only valid way to express second-step or third-step ideas`

- `video_mini_margin_bias`
  - source: `JPX 北浜博士のデリバティブ教室 2025-06-16`
  - hypothesis: `mini and micro products should stay tied to capital-aware risk controls`
  - local_test_mapping: `preserve drawdown and minimum available balance guardrails when evaluating sparse overlays`

## Rejected

- `video_option_specific_trade_construction`
  - reason: `options-specific strategy construction is outside the current futures-only simulator`

- `video_manual_rescue_logic`
  - reason: `human discretionary recovery paths cannot be replayed reproducibly in the local harness`

- `video_general_product_education`
  - reason: `broad education without a deterministic trigger or filter does not belong in the candidate queue`

## Notes

- All accepted hypotheses reinforced the existing same-lane discipline rather than opening a new unrelated research branch.
