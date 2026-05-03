# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8`, and no same-lane neighbor tested in this run clearly beat that promoted baseline.

This run completed three targeted single-sleeve research batches and then two reproducible bundle reruns around the baseline lane. The morning batch reconfirmed that the current morning sleeve is usable inside the bundle but too sparse to promote standalone: `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10` led the group with `20200` total walk-forward test profit, but every morning neighbor finished `0/4` accepted windows because they repeatedly missed the `min_train_trades=30` guardrail. The `t16`, `usdjpy_down_v025`, `sp500_down`, and `vix_up_02` overlays all reduced trade density further, so that lane remains closed for replacement work.

The midday-primary batch was the only lane with a new signal worth carrying forward. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` and the equivalent `..._t8` variant both finished `4/4` accepted windows with `21550` total walk-forward test profit and only `3200` worst test drawdown. The current live sleeve `...time_stop_10` managed `22750` total walk-forward test profit but only `3/4` accepted windows, while the plain and `looser_trail` variants reached `23650-23950` total test profit with `3/4` accepted windows. That made midday `time_stop_8` the cleanest stability candidate and `looser_trail` the strongest profit-first candidate for bundle follow-up.

The April-only opening micro batch re-closed the weakest sleeve. Every tested variant around `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05` finished `0/4` accepted windows. The baseline sleeve itself managed only `3650` total walk-forward test profit, while the best ex-SQ/range-filtered variants reached `4600`, but all of them still failed on sparse training data and mostly produced zero out-of-sample trades. That confirms the April micro sleeve is still only a tiny bundle complement, not a branch worth expanding.

Two bundle reruns then checked whether the improved midday-primary neighbors could actually beat the promoted baseline. `lot3_base10_middaytime8_rerun` posted `205000 / DD 13250 / win_rate 0.5714 / wf total test profit 132900`, which kept `4/4` portfolio walk-forward acceptance but lost too much full-sample profit versus the baseline `232850 / DD 13300 / win_rate 0.5772 / wf 129750`. `lot3_base10_middayloosertrail_rerun` was better, reaching `229800 / DD 13850 / win_rate 0.5808 / wf total test profit 134000`, but it still trailed the baseline by `3050` full-sample profit and worsened full-sample drawdown by `550`.

No promotion is justified. `middaytime8` improved walk-forward profit and slightly lowered full-sample drawdown, but the full-sample profit drop to `205000` is too large. `middayloosertrail` improved walk-forward profit by `4250` and slightly improved win rate, but it still gave back profit and pushed drawdown above the promoted baseline. The source-of-truth therefore stays `lot3_base10_june_t8`.

- promoted source-of-truth leader: `lot3_base10_june_t8`
- approximate run duration: `9` minutes
- research batches completed: `5`
- stopped before 50 minutes: `yes`
- blocker: `after three targeted single-sleeve batches plus two reproducible midday-primary bundle reruns, no remaining same-lane candidate improved the promoted baseline on combined full-sample profit, drawdown, and walk-forward quality`
- best candidate tested: `lot3_base10_middayloosertrail_rerun`
