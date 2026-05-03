# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block stayed in the same promoted-baseline lane, completed six targeted validation batches, and used corrected factor configs before deciding whether any branch deserved a new bundle rerun.

The first pair of batches revisited factor-dependent opening and night families and immediately exposed a reproducible config issue: running `sp500/vix` and `usdjpy` candidates on the plain backtest config collapsed them to zero trades. Re-running those lanes on the proper factor configs fixed the mismatch and showed the actual picture. The corrected opening `sp500_down_02_vix_up_05` range ladder was still too sparse for promotion: the best variants, `...ex_sq_range_above_110` and `...120`, reached only one positive test window with `4050` total test profit and `950` worst test drawdown, but they never reached the minimum train or test trade density.

The second pair of batches pushed the midday `only_6` family across plain and factor-aware neighbors. The non-factor range ladder remained thin, with the best `mon_thu` and `mon_wed` variants producing only `250` total test profit over `14` test trades and zero accepted windows. The factor-aware refresh around `mon_wed_vix_up_02` and `us10y_not_up` was no better: `...vix_up_02_t8` led that subset with `3000` total test profit and only `5` total test trades, which is directionally positive but far too sparse to justify any bundle-level follow-up.

The corrected night fixed-set refresh simply reconfirmed what the source of truth already implied. `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12` again finished as the strongest standalone night sleeve with `4/4` accepted windows, `18900` total test profit, and `3800` worst test drawdown, ahead of `ex_2_5_6_8_10_11_12` at `17400`. That is useful as a consistency check, but it is not a promotion path because prior portfolio reruns already showed the non-`ex_sq` night branch failing to beat the promoted `night_exsq` leader on full-sample profit, drawdown, and monthly cleanliness.

No promotion is justified. The new information from this run is narrower than a new leader change: factor-dependent candidate batches must continue to be run on the matching macro or usdjpy configs, and once that mismatch is fixed, the remaining opening and midday sub-branches are still too sparse while the corrected night winner remains portfolio-closed by existing rerun evidence.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `13` minutes
- research batches completed: `6`
- stopped before 50 minutes: `yes`
- blocker: `the first factor-dependent opening and night batches exposed a concrete config mismatch, and after rerunning with the correct macro/usdjpy configs the remaining same-lane candidates were either too sparse to satisfy the train/test trade gates or already portfolio-closed by prior fixed-bundle reruns`
- best candidate tested: `both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12`
