# Video Hypotheses 2026-04-30

## Accepted

- `video_april_gate_retention`
  - source: `日経225マイクロ先物を使った投資戦略その1`
  - hypothesis: `April opening overlays should remain tightly gated by explicit range or calendar structure`
  - local_test_mapping: `continue only near-neighbor checks around the current opening April sleeve such as range105/110 and adjacent SQ gates`

- `video_sparse_overlay_reinforcement`
  - source: `日経225マイクロ先物を使った投資戦略その2`
  - hypothesis: `micro sleeves add value more often as sparse repairs than as broad portfolio rewrites`
  - local_test_mapping: `prefer one-sleeve substitutions and month-limited overlays over unrelated portfolio reshuffles`

- `video_defensive_regime_limit`
  - source: `日経225マイクロ先物を使った投資戦略その3`
  - hypothesis: `defensive micro logic should stay tied to explicit regimes`
  - local_test_mapping: `keep prior-session, month, and macro filters narrow when revisiting defensive or repair branches`

- `video_parameterized_rule_intake`
  - source: `オプションと先物の基礎`
  - hypothesis: `only parameterized ideas should enter the local research queue`
  - local_test_mapping: `reject non-parameterized narration and admit only time/range/month/factor rules`

- `video_checklist_macro_bias`
  - source: `相場に関する情報収集について`
  - hypothesis: `macro context should be represented as explicit checklist gates`
  - local_test_mapping: `preserve VIX, USDJPY, US10Y, and calendar filters as the only allowed external inputs`

- `video_sq_calendar_scope`
  - source: `オプション道場 225`
  - hypothesis: `SQ behavior should remain calendar-local rather than becoming a generic daily rule`
  - local_test_mapping: `keep SQ exclusion and related contract-calendar logic only on narrow sleeves`

## Rejected

- `video_execution_style_discretion`
  - reason: `speaker-specific judgment without a parameterized trigger is not reproducible locally`

- `video_option_structure_edges`
  - reason: `options-greek and volatility-surface tactics are outside the futures-only simulator`

- `video_cash_inventory_hedges`
  - reason: `the current research harness does not model a standing cash-equity inventory book`
