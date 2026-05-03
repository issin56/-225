# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_base10_june_t8_night_exsq_rerun`, with `lot3_base10_june_t8` retained as the structural baseline. This follow-up stayed in the promoted baseline lane, completed three targeted walk-forward batches, and escalated only the single midday variant that was robust enough to justify a fixed-bundle rerun.

The first batch extended the opening-range branch around `day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05`. Raising the prior-range threshold from `105` through `115` kept the family structurally thin: every candidate finished `0/4` accepted windows, and the few positive OOS slices came with too little train or test activity to survive density gating. That lane now looks locally exhausted unless a genuinely different opening hypothesis is implemented.

The second batch revisited the broader morning support family around `day_morning_short_mon_thu_prev_night_down_tight_stop`. The best ungated variant reached only `1/4` accepted windows with `10500` total test profit and `7700` worst test drawdown, while the `ex_9_10` macro-gated neighbors remained sparse despite occasional positive windows. In practical terms, the morning branch still has no replacement that is active enough and stable enough to justify changing the fixed bundle.

The third batch pushed the midday specialist through time-stop and trail-shape neighbors. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` stood out by reaching `4/4` accepted windows with `21550` total test profit and only `3200` worst test drawdown, clearly better than the nearby looser-trail and time-stop variants on walk-forward acceptance. That made it the only candidate in this block that earned a full bundle rerun.

The rerun did not clear the promotion bar. `lot3-base10-june-t8-night-exsq-middaytime8-rerun` kept `4/4` accepted portfolio windows and held full-sample drawdown at `10350`, but full-sample profit dropped to `208300` from the promoted leader's `232900`. Diagnostics also showed that the known weak month `2026-02` stayed at only `150`, so the time-stop swap improved neither the aggregate return profile nor the specific weakness it was supposed to help.

No promotion is justified. The promoted source-of-truth leader should remain `lot3_base10_june_t8_night_exsq_rerun`, and the best new information from this run is narrower: the midday `time_stop_8` sleeve is a valid local single-sleeve benchmark, but not a portfolio-level improvement once inserted into the current six-sleeve leader.

- promoted source-of-truth leader: `lot3_base10_june_t8_night_exsq_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `10` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `after three targeted batches and one fixed-bundle rerun, the current same-lane queue was exhausted: opening and morning expansions stayed sparse or sub-threshold, and the only viable midday swap degraded full-sample profit without fixing the weakest month`
- best candidate tested: `lot3-base10-june-t8-night-exsq-middaytime8-rerun`
