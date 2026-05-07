# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the promoted `macro.lot3` lane and completed four targeted research batches: two night-sleeve fixed-bundle reruns, one opening-main defensive fixed-bundle rerun, and one opening-main sleeve rerank.

The first batch swapped only the night sleeve from `..._ex_sq` to plain `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` while keeping the current openingrange105 bundle unchanged. That challenger did improve portfolio walk-forward total test profit to `135100` from the incumbent's `134050`, and it still accepted `4/4` fixed windows with zero losing months. It is still not promotable because the improvement comes with the exact failure mode that earlier nightplain work warned about: full-sample profit falls to `232050` from `235600`, while full-sample drawdown widens sharply to `13850` from `10350` and worst test drawdown rises to `10550` from `7800`.

The second batch tested the closest defensive night sibling, `..._ex_sq_v020`, under the same fixed current bundle. That variant preserved the current leader's `10350` full-sample drawdown and `7800` worst test drawdown, but it only reached `235300` full-sample profit and `132550` total portfolio walk-forward test profit. That makes it cleaner than nightplain on risk, but still clearly behind the promoted leader on both headline profit and out-of-sample total.

The third batch checked whether the unrerun opening-main defensive sleeve `day_opening_short_range_fade_lb8_buf4_ex_1_2_6_7_8_10` could combine well with the promoted night and openingrange105 overlays. It could not. The bundle dropped to `215900` full-sample profit, added three losing months, and only produced `130650` total test profit despite keeping worst test drawdown at `7800`. This closes the remaining serious `buf4` rerun question for the current leader bundle.

The fourth batch reranked the opening-main family on candidate walk-forward rather than bundle interaction alone. The family is still live, but the tradeoff stayed the same: `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` led standalone total test profit at `29500` but carried the same `11950` worst test drawdown that already disqualified it as a bundle replacement, `..._ex_1_2_6_7_8_10` remained the best balanced standalone neighbor at `28700` with `4000` worst test drawdown, and `...buf4...` improved defensive averages but remained materially weaker on total train/test profit. That confirms the current opening-main sleeve is still the best portfolio-compatible choice once interaction effects are included.

No new video intake was added in this run because the daily `2026-05-03` quota had already been satisfied earlier with exactly six official-source videos, and adding more would violate the exact-six rule. The usable conclusion from this block is therefore narrowing, not expansion: the only challenger that beat the leader on portfolio walk-forward total was the nightplain swap, and it did so by paying too much additional drawdown.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `21` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after two current-bundle night reruns, one opening-main defensive rerun, and one opening-main sleeve rerank, the remaining reproducible queue inside the promoted macro.lot3 lane was exhausted: the only bundle that improved walk-forward total was the nightplain swap but it violated the incumbent drawdown advantage, the defensive night and opening buf4 swaps both trailed clearly, and the opening-main family still resolved to already-tested drawdown vs profit tradeoffs rather than a new clean promotion candidate`
- best candidate tested: `lot3-base10-june-t8-nightplain-openingrange105-rerun`
