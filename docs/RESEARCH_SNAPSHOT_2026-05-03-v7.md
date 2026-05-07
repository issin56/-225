# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block completed four targeted `macro.lot3` research batches: two single-sleeve validations followed by two fixed-bundle reruns limited to the only midday neighbors that still deserved full-portfolio replay.

The first batch reopened only the current midday main family around `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11`. That lane is still live, but only in a narrow sense. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` and its equivalent `..._t8` sibling were the only `4/4` accepted both-window variants, each at `21,550` total walk-forward test profit with `3,200` worst test drawdown. The profit-oriented neighbor `..._looser_trail` reached the highest standalone total at `23,950`, slightly above the incumbent's `23,650`, but it slipped to `3/4` accepted both windows and widened worst test drawdown to `4,450`.

The second batch closed the current opening secondary sleeve neighborhood instead of reopening unrelated opening-main work. Every April-only `vix_up_05_ex_sq_range_above_100/105/108/110/112/115` variant stayed structurally too sparse. Each candidate finished `0/4` accepted both windows, and all but one test window across the set were simply zero-trade. The promoted `...range_above_105` sleeve therefore remains usable only as a tiny additive overlay inside the current leader, not as an expandable lane.

Those results left exactly two bundle reruns worth paying for. Replacing the current midday main sleeve with the robust `...time_stop_8` variant preserved `4/4` portfolio acceptance and the same `7,800` worst test drawdown, but it cut full-sample profit from `235,600` to `211,000` and reduced portfolio walk-forward total test profit from `134,050` to `132,800`. That is a clean rejection. Replacing the same sleeve with `...looser_trail` produced the closest challenger of the block: `235,200` full-sample profit, `10,350` full-sample drawdown, `134,100` total portfolio walk-forward test profit, `7,800` worst test drawdown, and zero losing months. It still is not promotable because it improves walk-forward total by only `50` while giving back `400` of full-sample profit, which is not a clear enough edge to dethrone the promoted openingrange105 bundle.

No new video intake was added in this run because the daily `2026-05-03` quota had already been satisfied earlier with exactly six JPX official videos; adding more would violate the exact-six rule. The usable conclusion from today's full block stays discipline-focused rather than branch-opening: midday still has neighbors worth measuring, but the current leader remains the best like-for-like bundle once full-sample profit, drawdown, zero-losing-month cleanliness, and fixed portfolio walk-forward acceptance are judged together.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `19` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after a midday-main neighbor batch, an opening-secondary threshold closure batch, and two fixed-bundle reruns, the remaining reproducible queue in the promoted macro.lot3 lane was exhausted: the opening secondary family was still too sparse, the robust midday time-stop swap lost too much full-sample profit, and the looser-trail bundle improved walk-forward total only marginally while still trailing on full-sample profit`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middayloosertrail-openingrange105-rerun`
