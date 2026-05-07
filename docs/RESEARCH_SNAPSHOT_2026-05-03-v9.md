# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted `macro.lot3` lane, completed five targeted research batches, and used the results to close the remaining locally reproducible same-lane follow-ups rather than opening a new branch.

The first three batches were family-level walk-forward refreshes. The midday main family stayed live, but not in a promotable way: `..._t8` was the only sibling to accept `4/4` standalone windows, yet it finished at only `21550` total test profit versus the current midday main's `23650`, while `time_stop_10`, plain, looser, and tighter variants all slipped to `3/4` accepted windows. The morning precision family remained structurally below density gates, with the current `...ex_9_10` and `...ex_9_10_ex_sq` each producing only `0/4` accepted-both windows despite positive OOS totals, so that lane stays closed for bundle promotion work. The opening secondary threshold family also closed again: thresholds from `105` through `115` produced only `1` positive test window in total and `0/4` accepted-both windows for every variant, confirming that the April-only overlay is too sparse to justify further threshold refinement now.

The fourth batch pushed the best remaining new midday sibling back into the current six-sleeve bundle. `lot3-base10-june-t8-night-exsq-middaytime10-openingrange105-rerun` slightly improved full-sample profit to `236300` from the leader's `235600` while preserving the same `10350` full-sample drawdown and zero losing months, but it still fell short where promotion matters more: portfolio walk-forward total test profit dropped to `131150` from `134050`, with average test win rate easing to `0.5878` from `0.5944`. The fifth batch tested whether adding gotobi exclusion to the current promoted night sleeve could clean the weak months without hurting the rest of the bundle. It did not. `lot3-base10-june-t8-night-exsqexgotobi-middayplain-openingrange105-rerun` fell to `219150` full-sample profit, introduced one losing month via `2024-01 -600`, and cut portfolio walk-forward total test profit to `116600` while worsening worst test drawdown to `8400`.

No new video intake was added in this run because `docs/VIDEO_INGEST_2026-05-03.md` already recorded exactly six official-source videos for the JST day. The usable conclusion is therefore closure, not expansion: the three open family queues either stayed sparse or failed to beat the incumbent on OOS stability, and the two remaining credible current-bundle reruns both trailed the promoted leader where the quality gate is strictest.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `57` minutes
- research batches completed: `5`
- stopped before 50 minutes: `no`
- blocker: `none; the remaining reproducible same-lane queue was exhausted after three family walk-forward refreshes and two current-bundle reruns`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middaytime10-openingrange105-rerun`
