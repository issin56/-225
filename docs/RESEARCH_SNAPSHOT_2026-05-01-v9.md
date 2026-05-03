# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_night_exsq_middaylooser_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed three targeted research batches plus reconciliation on the desktop source-of-truth tree. First, the night control batch re-opened the live `night_ex_sq` family against nearby variants. Plain `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` had the highest total walk-forward test profit at `53400`, but `..._ex_sq` remained the better bundle component because it kept `4/4` accepted windows with much lower worst test drawdown at `7650` versus `11400`.

Second, the April-only opening `ex_sq` branch was re-tested on the richer desktop registry where the missing names actually exist. That branch stayed structurally sparse rather than merely weak: all six variants, including `...ex_sq`, `...range_above_105`, `...range_above_110`, and the `sp500_down_02` overlay, finished with `0/4` accepted walk-forward windows, no usable recent out-of-sample trade flow, and only one small historical positive window. That closes the opening April `ex_sq` lane again.

Third, the run spent the remaining work budget on full recompositions around the structural baseline using only sleeves that are locally reproducible and already validated nearby. Four bundles were rerun and walk-forward validated. `lot3_base10_night_exsq_opening67810_rerun` reached `233150 / DD 10350 / wf test profit 132550`, `lot3_base10_night_exsq_opening67810_middaylooser_rerun` reached `232200 / DD 10350 / wf test profit 135500`, and `lot3_base10_night_exsq_opening67810_middaytime8_rerun` fell back to `208800`. The best balance was `lot3_base10_night_exsq_middaylooser_rerun` at `233350 / DD 10350 / win_rate 0.5838 / losing_months 0`, with `4/4` accepted portfolio windows and `133150` total walk-forward test profit.

Promotion is justified within the baseline lane. `lot3_base10_night_exsq_middaylooser_rerun` beats the structural baseline `lot3_base10_june_t8` on full-sample profit (`233350` vs `232850`), cuts max drawdown by `2950`, improves win rate, and preserves full portfolio walk-forward acceptance. The opening April `ex_sq` branch is still not promotable, so the gain comes from pairing the validated `night_ex_sq` sleeve with the looser primary midday replacement while keeping the rest of the baseline intact.

- promoted source-of-truth leader: `lot3_base10_night_exsq_middaylooser_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `10` minutes
- research batches completed: `3`
- stopped before 50 minutes: `yes`
- blocker: `the April-only opening ex_sq lane remained structurally too sparse with 0 accepted walk-forward windows, and after four full recompositions the remaining live baseline lane was locally reconciled`
- best candidate tested: `lot3_base10_night_exsq_middaylooser_rerun`
