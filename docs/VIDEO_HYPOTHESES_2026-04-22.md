# Video Hypotheses 2026-04-22

## Accepted

- `video_april_gate_plateau_check`
  - source: `日経225マイクロ先物を使った戦略その１`
  - hypothesis: `the live April opening sleeve should stay hard-gated on range structure rather than broadened slightly`
  - local_test_mapping: `range_above 100/105/110/115 and nearby vix-up thresholds on the promoted opening branch`

- `video_sparse_overlay_bias_refresh`
  - source: `日経225マイクロ先物を使った戦略その２`
  - hypothesis: `micro overlays add more value as sparse repairs than as broad portfolio rewrites`
  - local_test_mapping: `keep month-only, event-only, and single-sleeve probes prioritized over wholesale replacement branches`

- `video_defensive_micro_limit`
  - source: `日経225マイクロ先物を使った戦略その３`
  - hypothesis: `defensive micro usage should be calendar-limited or regime-limited`
  - local_test_mapping: `continue SQ exclusion, month-only, and explicit macro-gated defensive overlays`

- `video_reproducible_rule_shape`
  - source: `１．先物・オプションとは？`
  - hypothesis: `only rule ideas expressible as time, range, and contract-mechanics filters should enter the portfolio search`
  - local_test_mapping: `reject non-parameterized ideas and keep the search anchored to explicit rule toggles`

- `video_external_checklist_bias`
  - source: `（７）先物取引に関連する情報収集について`
  - hypothesis: `macro context should be encoded as explicit checklist gates instead of discretionary narrative`
  - local_test_mapping: `preserve explicit VIX, USDJPY, US10Y, and calendar filters as the only allowed external-state inputs`

- `video_sq_calendar_bias`
  - source: `先物・オプション道場225`
  - hypothesis: `SQ behavior belongs in explicit calendar handling rather than broad day-to-day logic`
  - local_test_mapping: `keep SQ exclusion or other explicit contract-calendar handling on April and defensive branches`

## Rejected

- `video_discretionary_case_studies`
  - reason: `speaker judgment without a parameterized trigger cannot be reproduced locally`

- `video_option_structure_edges`
  - reason: `option-price, greek, and volatility-surface tactics are outside the current futures-only simulator`

- `video_cash_inventory_hedges`
  - reason: `the current research harness does not model a standing cash-equity inventory to hedge`
