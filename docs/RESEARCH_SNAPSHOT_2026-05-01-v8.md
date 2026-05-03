# Research Snapshot 2026-05-01

Current strongest portfolio remains `lot3_night_exsq_source_truth_rerun`, while `lot3_base10_june_t8` stays the structural baseline.

This run completed four targeted baseline-lane batches plus result reconciliation. First, the midday-primary neighbor lane revalidated three close single-sleeve replacements around the baseline `time_stop_10` branch. `day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_8` was the cleanest walk-forward survivor at `7/7` accepted windows with `50100` total portfolio-level test profit once later bundled, while `...looser_trail` produced the strongest standalone candidate-level test profit but only `1/7` accepted single-sleeve windows and `...tighter_trail` never cleared a full accepted window set.

Second, the run re-opened the April opening add-on lane only at the closest registered neighbors around the dead local `...ex_sq_range_above_110` sleeve. All three variants, `...vix_up_04_ex_sq_range_above_110`, `...vix_up_06_ex_sq_range_above_110`, and `...sp500_down_02_vix_up_05_ex_sq_range_above_110`, produced `0` trades across every train and test window, so that entire local branch remains fully inert rather than merely underperforming.

Third, the run returned the midday-primary neighbors to the locally reproducible `lot3_base10_june_t8` bundle. `lot3_base10_middaylooser_full_rerun` was the best full-sample bundle at `75650 / DD 4700 / losing_months 2 / win_rate 0.5819`, `lot3_base10_middaytighter_full_rerun` followed at `73700 / DD 4700`, and `lot3_base10_middaytime8_full_rerun` stayed cleanest on later validation but only reached `66050 / DD 4050`. None came remotely close to the structural baseline's source-of-truth full-sample result of `232850 / DD 13300`.

Fourth, the run closed the bundle-level validation comparison for the two surviving midday recompositions. `lot3_base10_middaylooser_full_rerun` validated `6/7` windows with `57950` total test profit and a single `2025-01` to `2025-03` win-rate miss, while `lot3_base10_middaytime8_full_rerun` validated `7/7` windows with `50100` total test profit and `4000` worst test drawdown. That cleaner walk-forward profile still does not offset the much lower full-sample profit, and both bundles remain far below the structural baseline because the local harness still zero-trades the secondary midday, night, and April-only opening sleeves.

No promotion is justified. `lot3_base10_middaylooser_full_rerun` is the best candidate tested in this run on full-sample output, but it still trails the structural baseline `lot3_base10_june_t8` by `157200` profit on the source-of-truth full sample (`75650` vs `232850`). The current lane is locally exhausted for now because the closest April opening add-on neighbors are completely inert and the remaining midday family members have now been closed both standalone and in-bundle.

- promoted source-of-truth leader: `lot3_night_exsq_source_truth_rerun`
- structural baseline: `lot3_base10_june_t8`
- approximate run duration: `9` minutes
- research batches completed: `4`
- stopped before 50 minutes: `yes`
- blocker: `exhausted reproducible work in the current baseline lane after the April opening ex_sq neighbors all zero-traded locally and the midday-primary family was closed both standalone and in-bundle`
- best candidate tested: `lot3_base10_middaylooser_full_rerun`

## Batch Notes

- midday primary standalone closure:
  `time_stop_8` was the cleanest survivor with `7/7` accepted bundle-level windows after follow-up, `looser_trail` carried more isolated profit but only `1/7` accepted single-sleeve windows, and `tighter_trail` stayed unstable.
- April opening add-on closure:
  `...vix_up_04_ex_sq_range_above_110`, `...vix_up_06_ex_sq_range_above_110`, and `...sp500_down_02_vix_up_05_ex_sq_range_above_110` all zero-traded in every train and test window, confirming the whole local branch is dead.
- midday bundle rerun closure:
  `lot3_base10_middaylooser_full_rerun` led the reruns at `75650 / DD 4700`, but `lot3_base10_middaytime8_full_rerun` delivered the cleaner walk-forward shape at `7/7` accepted windows and `50100` total test profit.
