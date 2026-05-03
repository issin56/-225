# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_night_exsq_middaylooser_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed four targeted research batches and then four single-sleeve recompositions around the promoted leader lane. The night guardrail batch reconfirmed that the `night_ex_sq` family is still the only live defensive night branch worth carrying. `..._ex_sq_v020` stayed the best full-sample night variant at `60300`, but plain `..._ex_sq` remained slightly better for bundle use because it kept `4/4` accepted windows with `51550` total walk-forward test profit against `50050` for `v020`.

The midday guardrail batch showed the same split as before. Broad midday sleeves stayed alive, with plain `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11` and nearby `time_stop_10` both clearing `3/4` accepted windows, while the June-only VIX-gated sleeve again failed standalone validation with `0/4` accepted windows. That means the June t8 sleeve is still usable only as a sparse portfolio complement, not as a primary midday replacement.

The opening live batch stayed productive, but not cleanly superior. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` posted the highest single-candidate walk-forward total at `29500`, but it did so with far worse drawdown pressure, including `11950` worst test drawdown and a negative April contribution inside the bundle. `...ex_1_2_6_7_8_10` remained the cleaner live alternative at `28700` total test profit with only `4000` worst test drawdown. Separately, the April-only `ex_sq` control lane was re-closed again: all six variants finished with `0/4` accepted windows and no reproducible out-of-sample trade flow.

Four recompositions were then run against the current leader structure. `lot3_base10_night_exsqv020_middaylooser_rerun` reached `233100 / DD 10350 / wf test profit 131650`, `lot3_base10_night_exsq_opening6710_middaylooser_rerun` reached `223850 / DD 23900 / wf test profit 136300`, `lot3_base10_night_exsq_openingbuf4_middaylooser_rerun` fell to `215700 / DD 10350 / wf test profit 130700`, and `lot3_base10_night_exsq_middayplain_rerun` reached the highest raw profit at `233750 / DD 10350 / win_rate 0.5820 / wf test profit 133100`.

No promotion is justified. `lot3_base10_night_exsq_middayplain_rerun` improved full-sample profit by only `400` over the current leader, but it gave back walk-forward test profit (`133100` vs `133150`) and slightly worsened win rate (`0.5820` vs `0.5838`). The `opening6710` swap raised walk-forward profit, but the drawdown blowout to `23900` and the reintroduced losing month make it non-promotable. The leader therefore stays `lot3_base10_night_exsq_middaylooser_rerun`.

- promoted source-of-truth leader: `lot3_base10_night_exsq_middaylooser_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `12` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after four targeted single-sleeve batches plus four reproducible bundle recompositions, no locally validated candidate clearly beat the promoted leader on combined profit, drawdown, and walk-forward quality`
- best candidate tested: `lot3_base10_night_exsq_middayplain_rerun`
