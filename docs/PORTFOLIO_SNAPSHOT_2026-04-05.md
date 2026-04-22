# Portfolio Snapshot 2026-04-05

## Assumption

- single account
- single open position at a time
- candidate order is priority order
- same `config.backtest-nk225micro.yaml`

## Portfolio A: Two-Rule Core

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`

Result:

- ending_equity: `324600.0`
- profit: `24600.0`
- trades: `858`
- win_rate: `0.4359`
- max_drawdown: `23200.0`
- min_available_balance: `242950.0`
- profitable_months: `14/33`

## Portfolio B: Core + Night Fast Short

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`
- `both_fast_short_night_tp`

Result:

- ending_equity: `345350.0`
- profit: `45350.0`
- trades: `2261`
- win_rate: `0.4533`
- max_drawdown: `19300.0`
- min_available_balance: `237850.0`
- profitable_months: `17/33`

Breakdown:

- `day_midday_long_trail`: `+5300.0`
- `day_morning_short_mon_thu_tight_stop`: `+14200.0`
- `both_fast_short_night_tp`: `+25850.0`

Worst months:

- `2025-02`: `-10850.0`
- `2024-10`: `-6700.0`
- `2023-11`: `-6600.0`
- `2025-06`: `-6150.0`

## Portfolio B2: Core + Night Fast Short (Tue-Fri)

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`
- `both_fast_short_night_tue_fri_tp`

Result:

- ending_equity: `349550.0`
- profit: `49550.0`
- trades: `2026`
- win_rate: `0.4561`
- max_drawdown: `23300.0`
- min_available_balance: `232150.0`
- profitable_months: `17/33`

Breakdown:

- `day_midday_long_trail`: `+7600.0`
- `day_morning_short_mon_thu_tight_stop`: `+14200.0`
- `both_fast_short_night_tue_fri_tp`: `+27750.0`

Worst months:

- `2025-02`: `-8750.0`
- `2023-10`: `-8250.0`
- `2023-11`: `-7300.0`
- `2024-10`: `-7000.0`

## Portfolio B3: Core + Night Fast Short (Tight Stop)

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`
- `both_fast_short_night_tight_stop`

Result:

- ending_equity: `341350.0`
- profit: `41350.0`
- trades: `2277`
- win_rate: `0.4414`
- max_drawdown: `20400.0`
- min_available_balance: `236750.0`
- profitable_months: `17/33`

Breakdown:

- `day_midday_long_trail`: `+6050.0`
- `day_morning_short_mon_thu_tight_stop`: `+14200.0`
- `both_fast_short_night_tight_stop`: `+21100.0`

## Portfolio C: Core + Late-Day Fast Short

Candidates:

- `day_midday_long_trail`
- `day_morning_short_mon_thu_tight_stop`
- `both_fast_short_late_day_tp`

Result:

- ending_equity: `308800.0`
- profit: `8800.0`
- trades: `1315`
- win_rate: `0.4403`
- max_drawdown: `37050.0`
- min_available_balance: `240800.0`
- profitable_months: `11/33`

Breakdown:

- `day_midday_long_trail`: `+9450.0`
- `day_morning_short_mon_thu_tight_stop`: `+14200.0`
- `both_fast_short_late_day_tp`: `-14850.0`

## Takeaway

- `night` separation is the first portfolio version that clearly improves both profit and drawdown versus the previous 3-rule mix.
- `Tue-Fri night` is now the best raw-profit portfolio.
- plain `night tp` still has the best drawdown of the profitable 3-rule variants.
- `night tight stop` sits between them as a balanced compromise.
- `late day` separation does not work in the current form and should be dropped.
- The current best portfolio candidate is:
  - profit-focused: `day_midday_long_trail + day_morning_short_mon_thu_tight_stop + both_fast_short_night_tue_fri_tp`
  - drawdown-focused: `day_midday_long_trail + day_morning_short_mon_thu_tight_stop + both_fast_short_night_tp`

## Portfolio D: Overseas-Intel Hybrid

Candidates:

- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_tp`

Result:

- ending_equity: `369050.0`
- profit: `69050.0`
- trades: `1588`
- win_rate: `0.4685`
- max_drawdown: `13750.0`
- min_available_balance: `243100.0`
- profitable_months: `19/33`

Breakdown:

- `day_midday_long_prev_night_up_trail`: `+24500.0`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`: `+16800.0`
- `both_fast_short_night_tue_fri_tp`: `+27750.0`

Worst months:

- `2024-10`: `-6250.0`
- `2023-10`: `-4950.0`
- `2023-11`: `-4650.0`
- `2025-06`: `-3300.0`

## Portfolio E: Overseas-Intel All-Filtered

Candidates:

- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_prev_day_down_tue_fri_tp`

Result:

- ending_equity: `364000.0`
- profit: `64000.0`
- trades: `1016`
- win_rate: `0.4823`
- max_drawdown: `12000.0`
- min_available_balance: `247800.0`
- profitable_months: `21/33`

Breakdown:

- `day_midday_long_prev_night_up_trail`: `+24500.0`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`: `+16800.0`
- `both_fast_short_night_prev_day_down_tue_fri_tp`: `+22700.0`

Worst months:

- `2025-09`: `-5800.0`
- `2023-10`: `-4400.0`
- `2023-11`: `-3550.0`
- `2024-10`: `-3100.0`

## Updated Takeaway

- `前セッション地合い` フィルタは、海外材料をそのまま読むよりかなり効いた
- 新しい最有力は `Portfolio D`
- 安定性重視なら `Portfolio E` もかなり良い
- それでも月平均はまだ `2,000〜2,500円台` なので、月5万円目標には遠い
- 次は `USD/JPY` や `米株先物` を外部CSVで入れて、`前セッション地合い` の代替ではなく上乗せを狙う

## Portfolio F: USD/JPY Night Filter

Candidates:

- `day_midday_long_prev_night_up_trail`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`

Result:

- ending_equity: `365800.0`
- profit: `65800.0`
- trades: `860`
- win_rate: `0.4826`
- max_drawdown: `8400.0`
- min_available_balance: `248650.0`
- profitable_months: `21/33`

Breakdown:

- `day_midday_long_prev_night_up_trail`: `+24500.0`
- `day_morning_short_mon_thu_prev_night_down_tight_stop`: `+16800.0`
- `both_fast_short_night_tue_fri_usdjpy_down_tp`: `+24500.0`

Takeaway:

- 利益は `Portfolio D` より少し下がる
- ただし DD は `13750 -> 8400` まで改善
- `10月` の弱さがかなり薄れた
- `longest losing streak` も `2 -> 1` に改善
- 今のところ、`USD/JPY` は昼 long や朝 short より `night short` にだけ掛けるのが最も筋が良い

## Next Step

- compare `night tp` and `night tue-fri tp` month by month and find months where one clearly dominates
- test whether a small month-of-year exclusion around the recurring weak months is justified
