# Video Hypotheses 2026-04-20

## Accepted

- `video_range_gate_refresh`
  - source: `日経225マイクロ先物を使った戦略その１`
  - hypothesis: `the April opening short specialist should remain tightly range-gated; loosened open participation is unlikely to improve robustness`
  - local_test_mapping: `prior-session-range and opening-window gate retests on opening replacements`

- `video_sparse_overlay_bias`
  - source: `日経225micro・ミニオプションとは？`, `日経225microの活用方法`
  - hypothesis: `micro products add the most value as sparse overlays, not as broad replacement engines`
  - local_test_mapping: `continue month-only, SQ-only, or event-only probes with walk-forward gating`

- `video_directional_split_bias`
  - source: `日経225マイクロ先物を使った戦略その２`
  - hypothesis: `opening logic should stay directionally split by regime instead of reverting to symmetric both-side templates`
  - local_test_mapping: `keep testing short-only April overlays rather than broad opening rewrites`

- `video_defensive_overlay_bias`
  - source: `〖動画1〗個別株の長期投資におけるリスクをヘッジする戦略`
  - hypothesis: `defensive overlays should be explicitly calendar-limited or regime-limited`
  - local_test_mapping: `continue SQ exclusion and month-only defensive probes`

## Rejected

- `video_order_book_discretion`
  - reason: `the local dataset does not contain reproducible board-depth state`

- `video_option_structure_edges`
  - reason: `mini-option spreads, IV trades, and greek-driven ideas are outside the current futures-only simulator`

- `video_cash_equity_hedge_overlay`
  - reason: `the current harness does not model a standing cash-equity inventory to hedge`
