# Improvement Report

## Summary

今回の対応では、日経225系バックテストの「利益を盛る」方向ではなく、`なぜ勝ったか / どこで負けたか / どの条件が効いているか` を追えるようにするための可観測性と再現性を追加しました。

既存 CLI や既存 JSON 出力は残したまま、以下を additive に拡張しています。

- enrich された trade 出力
- ルール別 / 時間帯別 / side 別 / regime 別などの損益分解 CSV
- Markdown ダッシュボード
- SVG 可視化
- walk-forward 窓別 OOS レビュー

## Changed Files

- `src/kanekasegi/observability.py`
  - 観測用の trade schema、CSV writer、Markdown writer、SVG writer を追加
- `src/kanekasegi/portfolio_lab.py`
  - ポートフォリオ研究 path で enriched trade record を収集する処理を追加
- `src/kanekasegi/portfolio_research.py`
  - 研究結果に対して observability 出力を書き出す導線を追加
- `src/kanekasegi/validation.py`
  - walk-forward OOS trade の enriched 出力と review 生成を追加
- `tests/test_observability.py`
  - 新規 observability 機能の単体テストを追加
- `tests/test_portfolio_research.py`
  - trade record 返却の確認テストを追加
- `tests/test_validation.py`
  - walk-forward OOS trade record の返却テストを追加
- `docs/pnl_dashboard.md`
  - portfolio research 実行時に生成される Markdown ダッシュボード
- `docs/walk_forward_review.md`
  - walk-forward 実行時に生成される Markdown レビュー

## Added Trade Columns

以下の列を `output/trades_enriched.csv` と `output/wfo_trades_enriched.csv` に追加しました。
値の根拠が現在のコードにないものは、推測せず空欄にしています。

| 列名 | 説明 | 由来 |
|---|---|---|
| `trade_id` | trade ごとの安定 ID | entry/exit/rule/side 等から決定的生成 |
| `rule_id` | 候補ルール ID | candidate 名 |
| `strategy_name` | 表示用戦略名 | 現状は `rule_id` と同値 |
| `side` | `long` / `short` | entry side |
| `entry_ts` | entry timestamp | entry candle |
| `exit_ts` | exit timestamp | exit candle |
| `hold_minutes` | 保有時間(分) | `exit_ts - entry_ts` |
| `entry_price` | entry price | 約定価格 |
| `exit_price` | exit price | 決済価格 |
| `qty` | 枚数 | portfolio lab の position size |
| `pnl_gross` | コスト控除前損益 | point value 反映後の raw PnL |
| `pnl_net` | コスト控除後損益 | commission/slippage 控除後 |
| `commission` | 手数料コスト | `paper.fee_rate` に基づく |
| `spread_cost` | spread コスト | 現行 Nikkei research path に spread 設定がないため空欄 |
| `slippage_cost` | slippage コスト | `paper.slippage_bps` に基づく |
| `weekday` | 曜日 | entry timestamp |
| `session_bucket` | 時間帯バケット | day/night と時刻帯から導出 |
| `vol_bucket` | ボラティリティ区分 | ATR と価格の比率から導出 |
| `regime_id` | regime ID | trend + vol の組み合わせ |
| `regime_name` | regime 表示名 | `regime_id` の説明名 |
| `config_hash` | 設定ハッシュ | config dump の決定的 hash |
| `wf_window_id` | WFO 窓 ID | walk-forward 実行時のみ設定 |

## Added Output Files

### CSV

- `output/trades_enriched.csv`
  - portfolio research の trade 明細
- `output/wfo_trades_enriched.csv`
  - walk-forward OOS trade 明細
- `output/pnl_by_rule.csv`
  - ルール別損益
- `output/pnl_by_session.csv`
  - 時間帯別損益
- `output/pnl_by_side.csv`
  - buy/sell 別損益
- `output/pnl_by_weekday.csv`
  - 曜日別損益
- `output/pnl_by_vol_bucket.csv`
  - vol bucket 別損益
- `output/pnl_by_regime.csv`
  - regime 別損益
- `output/pnl_by_holding.csv`
  - 保有時間帯別損益
- `output/pnl_by_wf_window.csv`
  - walk-forward OOS 窓別損益

### Markdown

- `docs/pnl_dashboard.md`
  - 現在の portfolio backtest の要約、列説明、CSV 一覧、可視化を集約
- `docs/walk_forward_review.md`
  - walk-forward の OOS 要約、WFO 専用出力、図を集約

### SVG

- `output/equity_curve.svg`
  - equity curve
- `output/rule_pnl.svg`
  - rule 別損益 bar
- `output/session_heatmap.svg`
  - session x weekday の heatmap
- `output/wfo_oos_windows.svg`
  - WFO 窓別 OOS PnL

## New Tests

- `tests/test_observability.py::test_simulate_portfolio_emits_enriched_trade_records`
  - trade schema が埋まることを確認
- `tests/test_observability.py::test_observability_writers_create_csv_markdown_and_svg`
  - CSV / Markdown / SVG が生成されることを確認
- `tests/test_portfolio_research.py::test_run_portfolio_research_can_return_trade_records`
  - portfolio research から trade record を返せることを確認
- `tests/test_validation.py::test_portfolio_walk_forward_validation_can_return_oos_trade_records`
  - walk-forward から OOS trade record を返せることを確認

## Sample Commands

### Portfolio observability

```bash
py -3.11 -m kanekasegi.portfolio_research ^
  --config config.backtest-nk225micro.macro.lot3.yaml ^
  --candidate day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_10 ^
  --candidate day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8 ^
  --candidate day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10 ^
  --candidate both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12 ^
  --candidate day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10 ^
  --candidate day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_110 ^
  --output results/portfolio-research-2026-04-24-observability.json
```

### Walk-forward observability

```bash
py -3.11 -m kanekasegi.validation ^
  --config config.backtest-nk225micro.macro.lot3.yaml ^
  --mode portfolio-walk-forward ^
  --candidate day_midday_long_prev_night_up_trail_ex_1_2_4_6_9_10_11_time_stop_10 ^
  --candidate day_midday_long_prev_night_up_trail_only_6_prev_range_above_45_mon_wed_vix_up_02_t8 ^
  --candidate day_morning_short_mon_thu_prev_night_down_tight_stop_ex_9_10 ^
  --candidate both_fast_short_night_tue_fri_usdjpy_down_tp_ex_2_5_6_8_9_10_11_12 ^
  --candidate day_opening_short_range_fade_lb8_buf2_ex_1_2_4_6_7_8_10 ^
  --candidate day_opening_short_range_fade_lb8_buf2_only_4_vix_up_05_ex_sq_range_above_110 ^
  --train-months 12 ^
  --test-months 4 ^
  --step-months 4 ^
  --min-train-trades 30 ^
  --min-test-trades 10 ^
  --min-test-profit 0 ^
  --min-test-win-rate 0 ^
  --max-test-drawdown 13300 ^
  --output results/validation-2026-04-24-observability.json
```

## Compatibility Impact

- 既存 CLI は維持
- 既存 JSON 出力は維持
- 既存研究 path / validation path の返り値は additive に拡張
- trade 明細は `include_trade_records=True` のときだけ内部 payload を追加
- 既存出力を上書きせず、追加ファイルとして observability artifacts を生成

## What This Improves

今回の変更で、以下を見やすくなりました。

- ルール別に勝ち負けが分かる
- 時間帯別に差が見える
- 買い売り別の偏りが分かる
- regime 別に有効/無効が見える
- WFO 窓別に OOS 成績を比較できる

## Current Known Limits

- `spread_cost`
  - 現行 Nikkei research path に spread 設定がないため空欄
- regime
  - 価格 vs EMA と ATR の簡易定義であり、JPX microstructure 固有の regime ではない
- commission/slippage
  - research path の additive observability では反映済みだが、別経路との完全統一は今後の課題
- CSV comment
  - CSV 自体にコメント行は入れず、Markdown 側で列説明とファイル説明を持たせている

## Future Improvements

1. `spread_cost` を埋められるように Nikkei backtest config に spread parameter を追加
2. regime 定義を `prev_session_range` や event day と統合して強化
3. `pnl_by_rule.csv` に train/OOS 別列を追加し、walk-forward 比較をさらに追いやすくする
4. portfolio research と validation で同一 schema の summary JSON を出す
5. `docs/pnl_dashboard.md` を最新 run 自動選択だけでなく複数 run 比較対応に拡張
6. real broker cost が確定したら commission/slippage assumptions を再調整
