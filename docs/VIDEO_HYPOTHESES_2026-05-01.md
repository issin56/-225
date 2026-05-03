# Video Hypotheses 2026-05-01

Only testable research hypotheses are kept below. Non-testable education-only content, discretionary option-structure details, and ideas that cannot be expressed with the current Nikkei 225 Micro research stack were rejected.

1. `overlay_not_replacement`
   - hypothesis: `new defensive or volatility-aware sleeves should be tested first as narrow overlays against the promoted six-sleeve leader, not as broad structural replacements`
   - test shape: `fixed-bundle reruns where exactly one sleeve is swapped or one sparse overlay is added`
   - status: `supported by current research discipline; keep using`
2. `bullish_time_bounded_exit_bias`
   - hypothesis: `bullish daytime sleeves are more likely to survive walk-forward if they use explicit short time stops than if they rely on looser trailing exits`
   - test shape: `compare midday long trail families across time_stop_8, time_stop_10, and looser-trail neighbors`
   - status: `supported locally in this run by time_stop_8 outperforming nearby variants on walk-forward acceptance`
3. `short_side_regime_gate_required`
   - hypothesis: `short opening and morning sleeves should remain tied to explicit prior-session or macro regime filters rather than broadened into always-on variants`
   - test shape: `reject broader short neighbors unless they improve both acceptance and trade density under the same drawdown gate`
   - status: `supported; opening and morning expansions stayed too sparse or too weak`
4. `range_regime_must_be_numeric`
   - hypothesis: `range-view ideas are only research-usable when encoded as numeric thresholds such as prior-range-above bands`
   - test shape: `threshold sweeps like 105, 108, 110, 112, 115 with fixed bundle context unchanged`
   - status: `supported methodologically; this run found no promotable threshold improvement`
5. `vol_event_sleeves_should_stay_sparse`
   - hypothesis: `volatility-sensitive ideas should be implemented as sparse event or calendar overlays, not as a new permanent portfolio core`
   - test shape: `small additive experiments with strict density review before any bundle promotion`
   - status: `kept for future implementation work`
6. `extra_guardrail_must_pay_for_itself`
   - hypothesis: `any added hedge, volatility, or protection guardrail is only worth keeping if post-guardrail walk-forward profit and trade density remain competitive`
   - test shape: `compare hedge-like variants against the promoted leader on profit, drawdown, density, and weak-month repair`
   - status: `supported; the midday time_stop_8 bundle stayed clean but still failed promotion on aggregate profit and weak-month repair`
