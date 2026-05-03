# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This follow-up stayed inside the same night-led lane and completed three fixed-portfolio rerun batches that covered the remaining implemented night controls still compatible with the promoted six-sleeve bundle.

The first fixed-set batch compared the promoted leader against the two nearest same-lane profit challengers inside the full bundle: `raw broad` and `ex_sq_v020`. `lot3-base10-june-t8-night-raw-rerun` came closest on walk-forward headline profit at `129750`, but it widened worst walk-forward drawdown to `11500` and full-sample drawdown to `13300`, erasing the promoted leader's main quality edge. `lot3-base10-june-t8-night-exsq-v020-rerun` was the cleanest challenger, matching the leader's `10350` full-sample drawdown and `0` losing months, but it still trailed by `250` full-sample profit and `1500` walk-forward test profit.

The second batch reinserted the calendar overlays as full-bundle controls. Both `ex_gotobi` and `ex_sq_ex_gotobi` collapsed to the same `219950` profit, `1` losing month, and `113950` total walk-forward test profit. That confirms the earlier single-sleeve density warning was not hiding a better bundle interaction: these overlays are simply weaker once the full promoted bundle is held fixed.

The final batch closed the remaining legacy night controls. `ex_2_5_6_8_10_11_12` again reproduced the old trade-off of slightly higher full-sample profit (`236600`) at the cost of a fresh losing month and a materially worse `15450` drawdown. `only_1_7` preserved the clean `10350` drawdown and `0` losing months but fell to only `210350` profit and `102250` total walk-forward test profit. The older `tp` controls did lift `2026-02` from `150` to `2250`, but they blew through drawdown guardrails, falling to only `2/4` accepted walk-forward windows with worst test drawdowns of `15500` and `29150`.

No promotion is justified. The source-of-truth leader should remain `lot3_base10_june_t8_night_exsq_rerun`, and the same-lane night queue is now locally exhausted after covering the remaining implemented fixed-portfolio controls. If this branch is revisited again, the next useful work should come from new implemented night hypotheses rather than another pass over the current control set.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `same-lane fixed-portfolio queue exhausted after rerunning all remaining implemented night controls that still fit the promoted bundle; no nearby reproducible candidate preserved 4/4 walk-forward acceptance while also improving drawdown and monthly cleanliness`
- best candidate tested: `lot3-base10-june-t8-night-raw-rerun`
