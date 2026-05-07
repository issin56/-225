# Research Snapshot 2026-05-03

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This block completed four targeted research batches in the promoted-baseline lane and resolved the main reproducibility question from the prior run: the apparent collapse of the promoted opening and midday secondary sleeves was a config-lane mismatch, not a source-of-truth leader failure.

The first batch reran the opening April `range_above_105` family under `config.backtest-nk225micro.macro.lot3.yaml`, which is the lane that actually supplies the factor set used by the promoted bundle. The zero-trade failure from the prior plain-config crosscheck disappeared immediately. The `105`, `108`, `110`, `112`, `vix_up_04`, and `vix_up_06` controls all replayed again, but they remained far too sparse for promotion: `0/4` accepted both windows, only `1/4` positive test windows, and just `8` total test trades at `4,600` test profit for the best shapes.

The second batch repeated the same reconciliation for the midday secondary sleeve family. Under the macro lot3 lane, the promoted `...mon_wed_vix_up_02_t8` branch also replayed again instead of staying at zero, which confirms that the previous all-zero result was likewise a config mismatch. But the sleeve stayed too thin to reopen: the promoted `t8` path delivered only `5` total test trades, `3,000` total test profit, and `0/4` accepted both windows, while the us10y-plus-vix overlays were even thinner.

The third batch stayed with the only still-reproducible same-lane candidate family around the morning `ex_9_10` repair sleeve, expanding into the `ex_gotobi`, `vix_up_02`, `ex_sq_vix_up_02`, and `sp500_down` supports. The base and `ex_sq` variants remained the best of that group at `20,200` total test profit with `1/4` accepted test windows and `0/4` accepted both windows. `ex_gotobi` reduced drawdown somewhat but also cut test profit to `15,300`, while the vix and sp500 overlays became single-window dependent or weaker in-sample, so none justified a bundle rerun as a replacement sleeve.

The fourth batch reran the full promoted six-sleeve portfolio under the corrected macro lot3 config. That rerun fully matched the source-of-truth validation profile: `4/4` accepted both windows, `134,050` total test profit, `0.5944` average test win rate, and `7,800` worst test drawdown. This confirms that the promoted bundle remains valid and that the prior zero-trade crosscheck should be interpreted as a lane-selection mistake rather than evidence against the leader.

Promotion is not justified. The promoted source-of-truth leader stays `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`, and the structural baseline stays `lot3_base10_june_t8`. The best new candidate tested in this run was still the morning `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`, but it remained well below the portfolio acceptance bar and did not threaten the promoted bundle.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- prior promoted leader: `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `23` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after correcting the config lane, the remaining opening and midday factor sleeves were still too sparse to clear the walk-forward gates and the morning support family still failed portfolio-level acceptance, so reproducible same-lane work for this branch was exhausted`
- best candidate tested: `day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10`
