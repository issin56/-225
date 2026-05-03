# Video Hypotheses 2026-04-25

## Accepted

- `video_session_boundary_refresh`
  - source: `（１）日経225の指数と先物取引について`
  - hypothesis: `day-session and night-session behavior should remain explicitly separated, with contract-calendar handling preserved as a first-class rule gate`
  - local_test_mapping: `continue testing opening/day sleeves separately from night sleeves and keep explicit SQ or session-specific filters on sparse April branches`

- `video_index_level_only_bias`
  - source: `（２）日経225や個別銘柄との関係について`
  - hypothesis: `only index-level and parameterized relationships should enter the futures search; single-stock discretion should stay excluded`
  - local_test_mapping: `preserve month, time, prior-session, and external-factor gates while rejecting constituent-driven discretionary ideas`

- `video_small_account_sparse_overlay`
  - source: `（４）どんな人が日経225先物取引を始められるか？`
  - hypothesis: `sparse overlays with firm drawdown control are more suitable than high-frequency broad rewrites for the current account constraints`
  - local_test_mapping: `continue treating drawdown discipline and minimum-cash-buffer behavior as promotion gates, not optional afterthoughts`

- `video_reproducible_participant_proxy`
  - source: `（５）日経225先物を始めると見えてくる世界`
  - hypothesis: `macro or participant context should be encoded only through explicit reproducible proxies rather than narrative investor-flow interpretation`
  - local_test_mapping: `keep USDJPY, VIX, US10Y, and calendar filters as the only allowed external-state inputs`

- `video_night_subwindow_check`
  - source: `（６）一歩進んだ先物利用法`
  - hypothesis: `night-session logic should be split into explicit time windows such as front-half or US-overlap before considering any bundle-level change`
  - local_test_mapping: `validate night-session shape controls separately against the current live night sleeve instead of broadening full-session logic`

- `video_product_fit_rejection`
  - source: `（９）他の商品を利用した方が良いケース`
  - hypothesis: `setups that are structurally better expressed in options or other products should be rejected from the futures-only rule queue`
  - local_test_mapping: `reject options-shaped hypotheses and keep the current search limited to futures-native month, time, session, and macro toggles`

## Rejected

- `video_constituent_stock_storytelling`
  - reason: `single-stock or discretionary linkage ideas cannot be replayed deterministically in the current futures-only simulator`

- `video_leverage_coaching_without_rule`
  - reason: `account-preparation guidance does not create a testable signal unless it maps to an explicit risk or session parameter`

- `video_product_selection_branches`
  - reason: `rules that choose between futures and options products are outside the scope of the current Nikkei 225 micro futures harness`
