# Video Hypotheses 2026-04-23

## Accepted

- `video_parameterized_rule_discipline_refresh`
  - source: `１．先物・オプションとは？`
  - hypothesis: `only rule ideas that can be encoded as explicit contract, time, and risk parameters should enter the search`
  - local_test_mapping: `continue restricting new research to month, weekday, range, prior-session, and macro filter toggles`

- `video_micro_overlay_bias`
  - source: `２．日経225micro・ミニオプションとは？`
  - hypothesis: `micro contracts add more value as small overlays than as broad portfolio rewrites`
  - local_test_mapping: `prioritize single-sleeve replacements and small add-ons over unrelated six-sleeve redesigns`

- `video_case_limited_micro_usage`
  - source: `３．日経225microの活用方法`
  - hypothesis: `micro usage should stay scenario-limited and explicit`
  - local_test_mapping: `keep testing month-only, SQ-aware, and weak-month-repair branches instead of always-on variants`

- `video_structure_over_tape`
  - source: `225マイクロ先物を使った戦略①～チャートと板の見方について～`
  - hypothesis: `entry logic should be based on fixed price structure rather than discretionary board reading`
  - local_test_mapping: `preserve hard opening-range and prior-range gates on opening and midday sleeves`

- `video_directional_time_window_bias`
  - source: `225マイクロ先物を使った戦略②～売り,買いで収益機会を狙う～`
  - hypothesis: `micro opportunity capture should remain directional and session-specific`
  - local_test_mapping: `continue with narrow night timing splits and explicit directional sleeves only`

- `video_defensive_overlay_limit`
  - source: `225マイクロ先物を使った戦略③～値下がりリスクをヘッジする～`
  - hypothesis: `defensive micro sleeves should stay sparse and regime-limited`
  - local_test_mapping: `keep hedge-like overlays bound to narrow month filters, prior-session filters, and drawdown-aware selection`

## Rejected

- `video_discretionary_board_reading`
  - reason: `real-time board and tape interpretation cannot be reproduced deterministically in local backtests`

- `video_option_structure_mechanics`
  - reason: `mini-option pricing and option-specific mechanics are outside the current futures-only simulator`

- `video_cash_equity_hedge_inventory`
  - reason: `the harness does not model a standing cash-equity inventory to hedge with micro futures`
