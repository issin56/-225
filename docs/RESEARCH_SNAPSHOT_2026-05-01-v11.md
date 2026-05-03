# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8`, and no locally validated neighbor in this run clearly beat that promoted baseline for the automation.

This run completed three targeted single-sleeve research batches and then five reproducible bundle checks around the `lot3_base10_june_t8` lane. The June-only midday specialist batch reconfirmed the same closure as before: all four nearby `mon_wed` June variants were too sparse, finished with `0/4` accepted windows, and produced only `950-3000` total test profit across the full walk-forward stack. That keeps the June t8 sleeve in the portfolio only as a tiny complement, not as a candidate for expansion.

The opening-range batch stayed productive. `day_opening_short_range_fade_lb8_buf2_ex_1_2_6_7_10` again posted the highest single-candidate walk-forward total at `29500`, but it did so with the same drawdown pressure as before, including `11950` worst test drawdown. `...ex_1_2_6_7_8_10` remained the cleaner neighbor with `28700` total test profit and only `4000` worst test drawdown. `...buf4_ex_1_2_6_7_8_10` was calmer still at `24100 / worst test DD 3550`, but the profit gap stayed large.

The night batch did not open a new replacement. The baseline night sleeve `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` stayed strongest on combined acceptance and walk-forward profit at `53400` total test profit with `4/4` accepted windows. The nearby `...ex_2_5_6_8_10_11_12` lagged at `48900`, `...ex_2_6_10_11_12` kept a drawdown failure branch, and `...v020` remained non-viable with negative aggregate walk-forward profit.

Five bundle reruns then checked whether the live single-sleeve neighbors improved the promoted baseline. The control rerun for `lot3_base10_june_t8` came back at `232850 / DD 13300 / win_rate 0.5772 / wf test profit 129750`. `lot3_base10_june_t8_opening67810_rerun` reached `229450 / DD 13300 / win_rate 0.5758 / wf test profit 131750`. `lot3_base10_june_t8_opening6710_rerun` reached `229250 / DD 23900 / wf test profit 132550`. `lot3_base10_june_t8_openingbuf4_rerun` fell to `219850 / DD 11850 / wf test profit 129150`. `lot3_base10_june_t8_nojunespecialist_rerun` reached `221950 / DD 13300 / wf test profit 124950`.

No promotion is justified. `opening67810` improved walk-forward test profit by `2000`, but it gave back `3400` of full-sample profit, reintroduced a losing month, and did not improve drawdown. `opening6710` improved walk-forward slightly more, but the drawdown blowout to `23900` makes it non-promotable. `openingbuf4` and `nojunespecialist` both weakened the baseline too much on profit. The source-of-truth therefore returns to the promoted baseline bundle `lot3_base10_june_t8`.

- promoted source-of-truth leader: `lot3_base10_june_t8`
- approximate run duration: `8` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `after three targeted single-sleeve batches plus five reproducible june_t8 bundle reruns, the current lane had no remaining locally reproducible neighbor that clearly justified another same-lane promotion attempt`
- best candidate tested: `lot3_base10_june_t8_opening67810_rerun`
