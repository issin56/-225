# Video Hypotheses 2026-05-03

## Accepted

- `video_parameterized_rule_bias`
  - source: `１．先物・オプションとは？`
  - hypothesis: `only parameterized rule shapes should enter the futures-only search lane`
  - local_test_mapping: `continue limiting same-lane probes to explicit sleeve swaps, month filters, calendar filters, and macro yes/no gates`

- `video_sparse_micro_overlay_bias`
  - source: `２．日経225micro・ミニオプションとは？`
  - hypothesis: `micro products are more useful for sparse overlays than for broad always-on rewrites`
  - local_test_mapping: `keep favoring targeted replacement reruns over unrelated portfolio redesigns`

- `video_drawdown_guardrail_bias`
  - source: `（３）値下がりリスクとの向き合い方`
  - hypothesis: `a candidate that improves one metric but expands downside meaningfully should stay rejected`
  - local_test_mapping: `preserve hard promotion guardrails on max drawdown and monthly cleanliness`

- `video_margin_buffer_bias`
  - source: `新証拠金計算方式（VaR: Value at Risk）の要点`
  - hypothesis: `margin-aware acceptance should stay part of bundle selection, not just raw PnL ranking`
  - local_test_mapping: `continue screening on min_available_balance and drawdown before promotion`

- `video_sq_calendar_bias_refresh`
  - source: `先物・オプション道場225 第4回`
  - hypothesis: `SQ-specific behavior belongs in narrow calendar overlays only`
  - local_test_mapping: `keep SQ exclusion limited to explicit overlay candidates instead of broad sleeve defaults`

- `video_multiwindow_scenario_bias`
  - source: `先物・オプション道場225 第9回`
  - hypothesis: `scenario wins that do not survive fixed multi-window validation should not be promoted`
  - local_test_mapping: `continue requiring like-for-like portfolio walk-forward confirmation before any source-of-truth change`

## Rejected

- `video_option_pricing_structures`
  - reason: `greeks, volatility-surface, and option-combination mechanics are outside the current futures-only simulator`

- `video_discretionary_trade_management`
  - reason: `manual in-trade scenario handling cannot be replayed deterministically in the local backtest harness`

- `video_margin_formula_replication`
  - reason: `the backtester does not implement broker or clearer margin formulas at the line-item level`
