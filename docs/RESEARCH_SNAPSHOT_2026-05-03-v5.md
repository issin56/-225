# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block completed three additional targeted research batches in the corrected `macro.lot3` lane and extended the same-lane queue beyond the earlier reconciliation work, but it still produced no promotable improvement.

The first batch expanded the night sleeve queue beyond the previously checked `...ex_sq` and `...v020` branches into `us10y_up`, `front_half`, `us_overlap`, and `prev_day_down` families. The best new shape was `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12`, but it still managed only `2/4` accepted both windows, `19,450` total test profit, and `12,900` worst test drawdown. That stays clearly below the already-tested night `ex_sq` sleeve, which had `4/4` accepted both windows, `51,550` total test profit, and `7,650` worst test drawdown, so there is no justification to reopen the bundle around this alternative.

The second batch probed the midday follow-up queue that remained adjacent to the promoted secondary sleeve: `us10y_not_up` without the added VIX gate plus higher prior-range variants at `75` and `90`. That lane stayed structurally too sparse. Every candidate finished `0/4` accepted both windows, aggregate total test profit for the batch was `-4,800`, and the few positive-looking train windows collapsed into zero-trade or sub-threshold OOS windows.

The third batch revisited the April opening branch from the opposite direction by lowering the prior-range threshold to `80`, `90`, and `100`, while keeping `115` as a looser upper control. That change raised isolated OOS profit windows slightly, but it did not change the promotion verdict: each candidate remained at `0/4` accepted both windows, only one test window was positive across the batch, and the best total test profit was just `4,600`. The opening add-on remains too single-window dependent to challenge the promoted bundle.

Promotion is not justified. The promoted source-of-truth leader stays `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, and the structural baseline stays `lot3_base10_june_t8`. The best candidate tested in this extension run was `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12`, but it remained materially below the incumbent night sleeve on both robustness and drawdown, so no bundle rerun was warranted.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `18` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `the worktree lacked the macro factor CSV, so reproducible validation had to move to the desktop source-of-truth repo; after that correction, the remaining same-lane queue was exhausted without any candidate clearing the promoted walk-forward bar`
- best candidate tested: `both_fast_short_us_overlap_usdjpy_down_tp_ex_2_6_10_11_12`
