# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted-baseline lane, completed four targeted research batches, and then used the required daily video intake to close the remaining reproducible questions instead of opening a new branch.

The first batch revisited the morning repair lane around `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`, focusing on whether adding `usd_jpy_change` and `exclude_sq` could improve the weak `2026-02` contribution without breaking density. That path remains closed. The base and `ex_sq` variants again produced only `1/4` accepted test windows and `0/4` accepted both windows, while the `usdjpy_down_v025` pair cut trade count even further and never met the train gate. The new information is that the omitted `ex_sq_usdjpy_down_v025` branch is effectively identical to the plain `usdjpy_down_v025` path under the current sample, so there is no hidden morning repair left in this narrow family.

The second batch rechecked the April opening additive sleeve around `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`. That lane is locally exhausted again. The `ex_sq_range_above_108/110/112` variants and the nearby `vix_up_04/06` controls all stayed at `0/4` accepted both windows, and most windows were simply `0` out-of-sample trades. Even the strongest secondary threshold shapes produced just one positive window on tiny samples. That means the current April sleeve remains in the bundle only as a small additive contributor, not as an expandable standalone family.

The third and fourth batches pushed the only reusable night alternatives back into the current six-sleeve leader bundle. `lot3-base10-june-t8-nightplain-middayplain-rerun` raised portfolio walk-forward total test profit to `133950`, above the promoted leader's `133100`, but it also widened full-sample drawdown from `10350` to `13850` and worst test drawdown from `7800` to `11500`, so it is not promotable. `lot3-base10-june-t8-nightv020-middayplain-rerun` stayed clean on drawdown at `10350` and kept `4/4` portfolio acceptance with `7800` worst test drawdown, but it finished at `233450` full-sample profit and `131600` total test profit, both below the promoted leader's `233750` and `133100`. The night `ex_sq` sleeve therefore remains the best like-for-like choice inside the current source-of-truth bundle.

The daily video requirement for `2026-05-03` was completed in this run with exactly six JPX official videos recorded in `docs/VIDEO_INGEST_2026-05-03.md`. The usable hypotheses were all discipline-reinforcing rather than branch-opening: keep rule ideas parameterized, keep micro usage sparse, keep drawdown and margin guardrails hard, keep SQ handling calendar-limited, and keep multi-window robustness above single-scenario wins.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `8` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after four targeted same-lane batches plus six official JPX videos, the remaining reproducible work in this lane was exhausted: morning neighbors still failed density, opening April controls stayed zero-trade or one-window only, night plain required too much extra drawdown, and night v020 remained slightly behind the current leader`
- best candidate tested: `lot3-base10-june-t8-nightv020-middayplain-rerun`
