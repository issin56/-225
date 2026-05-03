# 日経225系システム監査

更新日: 2026-04-24  
監査対象: 日経225系バックテスト改善に関わる既存実装の棚卸しと改善優先順位付け  
監査方針: 既存 runner / validation / compare を再実装せず、既存コードの延長線で改善点を整理する

## 対象スコープ

### 主対象

- `src/kanekasegi/`
- `config.backtest-nk225micro*.yaml`
- `config.backtest.yaml`
- `README.md`
- `pyproject.toml`
- `tests/`
- `docs/`

### 参照のみ

- top-level の validation foundation
  - `src/analysis/`
  - `src/backtest/`
  - `src/data/`
  - `src/papertrade/`
  - `src/strategy/`
  - `src/utils/`

### 編集対象外として扱うもの

- `config.live-gmo.yaml`
- `config.live-sbi.yaml`
- live broker adapter 本体
- FX validation foundation の大規模改修

### スコープ確定メモ

- `README.md` は、このリポジトリが二つの workstream を持つと明記している。
  - `src/kanekasegi/` = 元の先物売買・研究フレームワーク
  - top-level `src/*` = 新しい FX validation foundation
- したがって、日経225系改善の主戦場は `src/kanekasegi/` だが、既存 compare / walk-forward / 出力スキーマの有無を確認するために top-level `src/*` は参照対象とする。

## 実行入口の整理

### 1. 実行系 backtest / paper / live 入口

- ファイル: `src/kanekasegi/main.py`
- 関数: `main`
- 役割:
  - `--config` で設定読込
  - `build_bot` で bot 構築
  - `mode=backtest` の場合は `run_backtest` を実行
  - `--research-grid` の場合は `run_research_grid`
- 根拠:
  - `main.py:142-207`
  - `main.py:198-207` で `run_backtest(bot, market_data, ...)`

### 2. 単体ルール研究入口

- ファイル: `src/kanekasegi/research.py`
- 関数: `main`
- 役割:
  - 候補ルール群を走らせてランキング JSON を出す
  - checkpoint JSON を `results/` に保存できる
- 根拠:
  - `research.py:3668-3697`
  - `research.py:3580-3665` の `run_research_lab`

### 3. ポートフォリオ研究入口

- ファイル: `src/kanekasegi/portfolio_research.py`
- 関数: `main`
- 役割:
  - 複数候補を同時運用したポートフォリオ結果を JSON 化する
- 根拠:
  - `portfolio_research.py:60-77`
  - `portfolio_research.py:14-57`

### 4. candidate / portfolio validation 入口

- ファイル: `src/kanekasegi/validation.py`
- 関数: `main`
- 役割:
  - `candidate-train-test`
  - `candidate-walk-forward`
  - `portfolio-walk-forward`
  の 3 モードで validation JSON を出す
- 根拠:
  - `validation.py:566-638`

### 5. ポートフォリオ診断入口

- ファイル: `src/kanekasegi/portfolio_diagnostics.py`
- 関数: `main`
- 役割:
  - portfolio result JSON を月別診断 JSON に変換する
- 根拠:
  - `portfolio_diagnostics.py:125-142`

### 6. 現在の研究ダッシュボード生成入口

- ファイル: `src/kanekasegi/research_dashboard.py`
- 関数: `main`
- 役割:
  - `docs/CURRENT_RESEARCH_STATUS.md` を results 群から生成する
- 根拠:
  - `research_dashboard.py:304-314`
  - `research_dashboard.py:185-300`

### 7. PowerShell wrapper

- ファイル: `scripts/run-research-nk225micro.ps1`
- 関数/クラス: 該当なし
- 役割:
  - `kanekasegi.research` を固定引数で起動する wrapper
- 根拠:
  - `py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml ...`

## config と実行入口の対応表

| config | 主な用途 | 入口 | 根拠 | 状態 |
|---|---|---|---|---|
| `config.backtest.yaml` | 汎用 csv backtest サンプル | `src/kanekasegi/main.py` | `README.md` の `py -m kanekasegi.main --config config.backtest.yaml`、`main.py:198-207` | 既存 |
| `config.backtest-nk225micro.yaml` | JPX ZIP を使う日経225マイクロ backtest / research 基本設定 | `main.py`, `research.py`, `validation.py`, `portfolio_research.py` | `research.py:3671`, `validation.py:569`, `portfolio_research.py:63` の default | 既存 |
| `config.backtest-nk225micro.macro.yaml` | 外部要因 CSV 付き variant | 上記と同じ | `runtime.external_factors_csv: data/external_factors.macro.fred.csv` | 既存 |
| `config.backtest-nk225micro.macro.lot3.yaml` | 3枚上限 variant | 上記と同じ | `risk.max_simultaneous_positions: 3` | 既存 |
| `config.backtest-nk225micro.fred.yaml` | FRED 系 factor CSV variant | 上記と同じ | `runtime.external_factors_csv: data/external_factors_fred.csv` | 既存 |
| `config.backtest-nk225micro-usdjpy.yaml` | USD/JPY factor CSV variant | 上記と同じ | `runtime.external_factors_csv: data/external_factors.usdjpy.csv` | 既存 |
| `config.backtest-nk225micro.usdjpy.yaml` | USD/JPY factor CSV variant の別名 | 上記と同じ | 同名機能の別ファイルとして共存 | 要整理 |
| `config.backtest-nk225micro-jpx.yaml` | JPX 証拠金寄りの variant | 上記と同じ | `per_contract_margin: 120000`, `max_position_notional: 100000` | 既存 |

## ファイル/関数対応表

| ファイル | 関数/クラス | 役割 | 根拠 | 状態 |
|---|---|---|---|---|
| `src/kanekasegi/main.py` | `build_bot` | config から provider / exchange / strategy / risk / execution / storage を組み立てる | `main.py:30-122` | 既存 |
| `src/kanekasegi/main.py` | `main` | 実行モード分岐。`backtest`, `research-grid`, `doctor`, `status` などを dispatch | `main.py:142-207` | 既存 |
| `src/kanekasegi/backtest.py` | `run_backtest` | `TradingBot.run_cycle()` を loop し `BacktestSummary` を返す | `backtest.py:41-87` | 既存 |
| `src/kanekasegi/bot.py` | `TradingBot.run_cycle` | 1 サイクル内で data取得 -> signal -> risk -> execution を結ぶ | `bot.py:34-115` | 既存 |
| `src/kanekasegi/jpx_data.py` | `JpxMinuteZipMarketDataProvider` | JPX ZIP CSV を読んで contract/sessions で絞り、timeframe リサンプルする | `jpx_data.py:58-280` | 既存 |
| `src/kanekasegi/csv_data.py` | `CsvMarketDataProvider` | CSV backtest 用 provider | `csv_data.py:20-100` | 既存 |
| `src/kanekasegi/strategy.py` | `BreakoutTrendStrategy.generate_signal` | runtime backtest / paper/live 用の signal 生成入口 | `strategy.py:25-66` | 既存 |
| `src/kanekasegi/strategy.py` | `_manage_open_position` | runtime path の stop / trailing / trend reversal exit | `strategy.py:68-94` | 既存 |
| `src/kanekasegi/risk.py` | `RiskEngine.validate` | daily loss / margin buffer / existing position をチェック | `risk.py:21-32` | 既存 |
| `src/kanekasegi/risk.py` | `RiskEngine.size_position` | runtime path のポジションサイズ計算 | `risk.py:34-46` | 既存 |
| `src/kanekasegi/exchange_adapter.py` | `PaperExchangeAdapter.place_order` | runtime path の fill / fee / slippage / realized PnL 計算 | `exchange_adapter.py:69-99` | 既存 |
| `src/kanekasegi/execution.py` | `ExecutionEngine.execute_signal` | signal を order / position / daily_pnl へ反映 | `execution.py:24-76` | 既存 |
| `src/kanekasegi/rule_lab.py` | `_supports_entry` | research path の entry filter 集約 | `rule_lab.py:291-324` | 既存 |
| `src/kanekasegi/rule_lab.py` | `_entry_signal` | research path の breakout/fade signal 判定 | `rule_lab.py:363-383` | 既存 |
| `src/kanekasegi/rule_lab.py` | `_position_size` | research path のサイズ計算 | `rule_lab.py:327-343` | 既存 |
| `src/kanekasegi/rule_lab.py` | `_trade_pnl` | research path の PnL 計算 | `rule_lab.py:346-350` | 既存 |
| `src/kanekasegi/rule_lab.py` | `simulate_candidate` | 単体候補の擬似約定・exit・月次集計 | `rule_lab.py:441-630` | 既存 |
| `src/kanekasegi/research.py` | `_load_candles` | research path の data load 入口 | `research.py:3542-3560` | 既存 |
| `src/kanekasegi/research.py` | `_load_external_factors` | external factor CSV 読込 | `research.py:3563-3566` | 既存 |
| `src/kanekasegi/research.py` | `_write_checkpoint` | research の checkpoint JSON 出力 | `research.py:3532-3539` | 既存 |
| `src/kanekasegi/research.py` | `run_research_lab` | 単体候補の batch 実行とランキング生成 | `research.py:3580-3665` | 既存 |
| `src/kanekasegi/portfolio_lab.py` | `_candidate_entry` | ポートフォリオ path の entry 生成 | `portfolio_lab.py:71-149` | 既存 |
| `src/kanekasegi/portfolio_lab.py` | `_should_exit` | ポートフォリオ path の stop / trailing / TP / time stop | `portfolio_lab.py:152-191` | 既存 |
| `src/kanekasegi/portfolio_lab.py` | `simulate_portfolio` | 複数候補の同時シミュレーション | `portfolio_lab.py:194-360` | 既存 |
| `src/kanekasegi/portfolio_research.py` | `run_portfolio_research` | ポートフォリオ結果 JSON ペイロード生成 | `portfolio_research.py:14-57` | 既存 |
| `src/kanekasegi/validation.py` | `run_candidate_train_test_validation` | 単体候補の train/test split 評価 | `validation.py:195-279` | 既存 |
| `src/kanekasegi/validation.py` | `run_candidate_walk_forward_validation` | 単体候補の WFO | `validation.py:281-438` | 既存 |
| `src/kanekasegi/validation.py` | `run_portfolio_walk_forward_validation` | ポートフォリオの WFO | `validation.py:441-563` | 既存 |
| `src/kanekasegi/portfolio_diagnostics.py` | `analyze_portfolio_result` | portfolio result から weak month / month-of-year を抽出 | `portfolio_diagnostics.py:106-122` | 既存 |
| `src/kanekasegi/research_dashboard.py` | `build_dashboard_markdown` | 最新 leader/result/validation/diagnostics を束ねて Markdown を生成 | `research_dashboard.py:185-296` | 既存 |

## バックテストのデータフロー

### A. `kanekasegi.main` 経由の runtime backtest

1. `load_config(path)` が YAML を `AppConfig` に変換する  
   根拠: `config.py:172-175`
2. `build_bot` が `runtime.data_source` を見て provider を選ぶ
   - `csv` -> `CsvMarketDataProvider`
   - `jpx_zip` -> `JpxMinuteZipMarketDataProvider`
   - それ以外 -> `InMemoryMarketDataProvider`
   根拠: `main.py:41-61`
3. `mode != live` なら `PaperExchangeAdapter` を構築し、`fee_rate`, `slippage_bps`, `contract_point_value` を注入する  
   根拠: `main.py:100-108`
4. `run_backtest` が `TradingBot.run_cycle()` を loop しながら equity / DD を集計する  
   根拠: `backtest.py:41-87`
5. `TradingBot.run_cycle` が以下を実行する
   - `exchange.get_ohlcv`
   - `exchange.get_ticker`
   - `BreakoutTrendStrategy.generate_signal`
   - `RiskEngine.validate`
   - `RiskEngine.size_position`
   - `ExecutionEngine.execute_signal`
   根拠: `bot.py:52-92`

### B. `kanekasegi.research` 経由の単体候補研究

1. `run_research_lab` が候補一覧を選ぶ  
   根拠: `research.py:3591-3593`
2. `_load_candles` が `runtime.data_source` を見て
   - `JpxMinuteZipMarketDataProvider`
   - `CsvMarketDataProvider`
   を使い、全 candle を list 化する  
   根拠: `research.py:3542-3560`
3. `run_rule_lab` -> `simulate_candidate` が各候補をバックテストする  
   根拠: `rule_lab.py:394-400`, `rule_lab.py:441-630`
4. `_checkpoint_payload` / `_write_checkpoint` が結果 JSON を `results/` に保存する  
   根拠: `research.py:3512-3539`

### C. `kanekasegi.portfolio_research` 経由のポートフォリオ研究

1. `run_portfolio_research` が candidate ごとの timeframe を見て `_load_candles` を呼ぶ  
   根拠: `portfolio_research.py:20-29`
2. `simulate_portfolio` が timestamp を横断して単一 open position 制約下で portfolio を評価する  
   根拠: `portfolio_research.py:30`, `portfolio_lab.py:194-360`
3. 出力は JSON ペイロード化され、`--output` で保存できる  
   根拠: `portfolio_research.py:41-57`, `portfolio_research.py:72-76`

### D. `kanekasegi.validation` 経由の train/test / walk-forward

1. `run_candidate_train_test_validation` は train/test split を 1 窓で評価する  
   根拠: `validation.py:195-279`
2. `run_candidate_walk_forward_validation` は rolling windows を生成し、候補別 summary を返す  
   根拠: `validation.py:281-438`
3. `run_portfolio_walk_forward_validation` は portfolio 単位で rolling windows を評価する  
   根拠: `validation.py:441-563`
4. いずれも `--output` で JSON 保存できる  
   根拠: `validation.py:629-633`

## コスト・サイズ・Exit の実装位置

### runtime backtest / paper / live path

#### 約定

- ファイル: `src/kanekasegi/exchange_adapter.py`
- 関数: `PaperExchangeAdapter.place_order`
- 役割:
  - ticker 取得
  - slippage 適用
  - fee 計算
  - reduce_only 時の realized PnL 計算
- 根拠:
  - `exchange_adapter.py:69-99`

#### 手数料・スリッページ

- ファイル: `src/kanekasegi/main.py`
- 関数: `build_bot`
- 役割:
  - `config.paper.fee_rate`, `config.paper.slippage_bps` を `PaperExchangeAdapter` に渡す
- 根拠:
  - `main.py:101-107`

#### stop / trailing exit

- ファイル: `src/kanekasegi/strategy.py`
- 関数:
  - `generate_signal`
  - `_manage_open_position`
- 役割:
  - entry 時に ATR stop を設定
  - 保有中は trailing stop / trend reversal / stop breach を判定
- 根拠:
  - `strategy.py:46-65`
  - `strategy.py:68-94`

#### ポジションサイズ

- ファイル: `src/kanekasegi/risk.py`
- 関数: `RiskEngine.size_position`
- 役割:
  - `risk_per_trade_pct`
  - `max_position_notional`
  - `per_contract_margin`
  - `min_cash_buffer`
 で上限をかける
- 根拠:
  - `risk.py:34-46`

### 研究 / ポートフォリオ path

#### signal / entry

- ファイル: `src/kanekasegi/rule_lab.py`
- 関数:
  - `_supports_entry`
  - `_entry_signal`
- 役割:
  - session / weekday / month / calendar / prior session / external factor / time window を通した上で breakout/fade を判定
- 根拠:
  - `rule_lab.py:291-324`
  - `rule_lab.py:363-383`

#### exit

- ファイル: `src/kanekasegi/rule_lab.py`
- 関数: `simulate_candidate`
- 役割:
  - stop
  - trailing stop
  - take profit
  - time stop
  - trend reversal exit
- 根拠:
  - long: `rule_lab.py:490-519`
  - short: `rule_lab.py:521-550`

- ファイル: `src/kanekasegi/portfolio_lab.py`
- 関数: `_should_exit`
- 役割:
  - portfolio path の exit 判定
- 根拠:
  - `portfolio_lab.py:152-191`

#### ポジションサイズ

- ファイル: `src/kanekasegi/rule_lab.py`
- 関数: `_position_size`
- 役割:
  - research path のサイズ計算
  - runtime path の `RiskEngine.size_position` とは別実装
- 根拠:
  - `rule_lab.py:327-343`

#### PnL 計算

- ファイル: `src/kanekasegi/rule_lab.py`
- 関数: `_trade_pnl`
- 役割:
  - side と entry/exit 価格から gross PnL を返す
- 根拠:
  - `rule_lab.py:346-350`

### 監査上の重要観察

1. runtime path には fee / slippage がある  
   根拠: `PaperExchangeAdapter.place_order`
2. research / portfolio path の `_trade_pnl` には fee / slippage が入っていない  
   根拠: `rule_lab.py:346-350` は価格差のみで、`config.paper.fee_rate` / `slippage_bps` を読まない
3. したがって、日経225の「研究結果」と `main.py` 経由の runtime backtest は、コストモデルが一致していない

## 既存出力の一覧

### `src/kanekasegi` 側で確認できた出力

| 出力 | 生成場所 | 根拠 | 状態 |
|---|---|---|---|
| `BacktestSummary` 標準出力 | `src/kanekasegi/main.py::main` | `main.py:198-207` | 既存 |
| SQLite `orders`, `fills`, `positions`, `daily_pnl`, `margin_snapshots` | `src/kanekasegi/storage.py` | `storage.py:79-99`, `133-234` | 既存 |
| JSONL log | `Storage.append_log` | `storage.py:119-132` | 既存 |
| health JSON | `Storage.save_status` | `storage.py:237-242` | 既存 |
| research checkpoint JSON | `research._write_checkpoint` | `research.py:3532-3539` | 既存 |
| research JSON | `research.main --output` | `research.py:3692-3696` | 既存 |
| portfolio research JSON | `portfolio_research.main --output` | `portfolio_research.py:72-76` | 既存 |
| validation JSON | `validation.main --output` | `validation.py:629-633` | 既存 |
| portfolio diagnostics JSON | `portfolio_diagnostics.main --output` | `portfolio_diagnostics.py:133-137` | 既存 |
| `docs/CURRENT_RESEARCH_STATUS.md` | `research_dashboard.write_dashboard` | `research_dashboard.py:297-300` | 既存 |

### top-level validation foundation に既にある出力

これは日経225主経路ではないが、「既存 compare / WFO があるか」を確認するために参照した。

| 出力 | 生成場所 | 根拠 | 状態 |
|---|---|---|---|
| `trades.csv` | `src/analysis/reporting.py::write_trades_csv` | `reporting.py:31-63` | 既存 |
| `equity_curve.csv` | `src/analysis/reporting.py::write_equity_curve_csv` | `reporting.py:65-78` | 既存 |
| `summary.json` | `src/analysis/reporting.py::write_summary_json` | `reporting.py:81-84` | 既存 |
| `period_summary.csv/json` | `src/analysis/reporting.py` | `reporting.py:93-113` | 既存 |
| `walk_forward_summary.json` | `src/analysis/walk_forward_runner.py` | `walk_forward_runner.py:36-39` | 既存 |
| `compare_summary.json` | `src/analysis/compare_runner.py` | `compare_runner.py:53-55` | 既存 |

### 監査上の重要観察

- Nikkei 主経路 (`src/kanekasegi`) は research / validation / diagnostics を JSON 中心で積み上げている
- 一方で top-level foundation には `trades.csv`, `equity_curve.csv`, `compare_summary.json`, `walk_forward_summary.json` が既にある
- したがって、日経225系の出力改善は「新規 compare/WFO 再実装」ではなく、「既存 schema をどう拡張・接続するか」で考えるべき

## walk-forward の実装有無と評価指標

### 実装有無

- `src/kanekasegi/validation.py` に実装あり
  - `run_candidate_train_test_validation`
  - `run_candidate_walk_forward_validation`
  - `run_portfolio_walk_forward_validation`
- top-level foundation にも実装あり
  - `src/analysis/walk_forward_runner.py`
  - `src/analysis/compare_runner.py`

### 日経225側の評価指標

`validation.py` の引数と summary から、以下を評価基準として使っている。

- `min_train_trades`
- `min_test_trades`
- `min_test_profit`
- `min_test_win_rate`
- `max_test_drawdown`

summary 出力には以下がある。

- `tested_windows`
- `accepted_windows`
- `accepted_both_windows`
- `accepted_test_windows`
- `positive_test_windows`
- `total_test_profit`
- `average_test_profit`
- `average_test_score`
- `average_test_win_rate`
- `average_test_drawdown`
- `worst_test_drawdown`
- `total_test_trades`

根拠:

- candidate WFO summary: `validation.py:390-438`
- portfolio WFO summary: `validation.py:534-562`

### 監査上の重要観察

- walk-forward は「未実装」ではない
- compare も top-level foundation 側には既にある
- 不足は「存在しないこと」ではなく、「日経225主経路と出力スキーマが分離していること」

## 既存テストの一覧

### 日経225主経路を直接支えるテスト

| テストファイル | 主な対象 | 根拠 | 状態 |
|---|---|---|---|
| `tests/test_backtest.py` | `run_backtest`, `build_bot` | `test_backtest_runs_and_returns_summary` | 既存 |
| `tests/test_config.py` | `AppConfig` validation | data_source / direction / external factor / calendar filter を検証 | 既存 |
| `tests/test_csv_data.py` | `CsvMarketDataProvider` | CSV 読込 | 既存 |
| `tests/test_jpx_data.py` | `JpxMinuteZipMarketDataProvider`, `build_bot` | current/specific contract, describe, jpx_zip build | 既存 |
| `tests/test_strategy.py` | `BreakoutTrendStrategy` | long/short entry, calendar/session filter, trailing exit | 既存 |
| `tests/test_risk.py` | `RiskEngine` | stop distance, point value, daily loss, margin cap, notional cap | 既存 |
| `tests/test_execution.py` | `ExecutionEngine` | exit 時 daily_pnl 更新 | 既存 |
| `tests/test_storage.py` / `tests/test_storage_daily_pnl.py` | `Storage` | position/order/margin/daily_pnl | 既存 |
| `tests/test_rule_lab.py` | `generate_default_candidates`, `simulate_candidate` | session, TP, time stop, month/calendar, external factors, fade, buffer | 既存 |
| `tests/test_research_lab.py` | `run_research_lab` | ranking, checkpoint, candidate filter, point value cap | 既存 |
| `tests/test_portfolio_lab.py` | `simulate_portfolio` | priority order, fade, trading_day, strategy monthly pnl | 既存 |
| `tests/test_portfolio_research.py` | `run_portfolio_research` | breakdown JSON 形状 | 既存 |
| `tests/test_validation.py` | `validation` | train/test, candidate WFO, portfolio WFO, drawdown rejection | 既存 |
| `tests/test_portfolio_diagnostics.py` | diagnostics | weak month / strategy attribution | 既存 |
| `tests/test_research_dashboard.py` | dashboard | latest leader / exact date bundle selection | 既存 |

### top-level validation foundation のテスト

- `tests/test_engine.py`
- `tests/test_walk_forward.py`
- `tests/test_compare.py`
- `tests/test_output.py`
- `tests/test_papertrade.py`
- `tests/test_csv_loader.py`
- `tests/test_fx_config.py`
- `tests/test_fx_strategy.py`
- `tests/test_metrics.py`

これらは存在するが、今回の主対象ではなく「既存機能が別 stack にもある」ことの確認材料として扱う。

## テストの不足点

1. `tests/test_backtest.py` は BTC の簡易 config を使っており、日経225 ZIP 実データ経路の end-to-end ではない  
   根拠: `tests/test_backtest.py:11-30`
2. `rule_lab.py` / `portfolio_lab.py` の research path には fee / slippage モデルがないため、その観点のテストも存在しない  
   根拠: `_trade_pnl` が gross PnL のみ
3. `validation.py::main` / `portfolio_research.py::main` の CLI 出力ファイル自体を確認する end-to-end テストは見当たらない
4. `JpxMinuteZipMarketDataProvider` の `contract_type=next` を直接確認するテストは見当たらない
5. `config.backtest-nk225micro.usdjpy.yaml` と `config.backtest-nk225micro-usdjpy.yaml` の二重管理を検知するテストはない
6. `config.backtest.yaml` にある `strategy.strategy_ids` は `config.py` に存在するが実行系で参照されておらず、その drift を検知するテストもない  
   根拠: `git grep "strategy_ids"` で `config.backtest.yaml`, `config.yaml`, `config.py` のみ

## 改善候補トップ10

### 1. 研究系に fee / slippage を入れる

- 優先度: 高
- 対象:
  - `src/kanekasegi/rule_lab.py`
  - `src/kanekasegi/portfolio_lab.py`
- 理由:
  - runtime path は `PaperExchangeAdapter.place_order` で fee/slippage を使うが、研究 path は `_trade_pnl` が gross PnL のみ
- 期待効果:
  - 研究結果と runtime backtest の前提差を縮める

### 2. 日経225主経路の canonical backtest 入口を明文化する

- 優先度: 高
- 対象:
  - `README.md`
  - `docs/`
- 理由:
  - 現在は `main.py`, `research.py`, `portfolio_research.py`, `validation.py` が並立しており、「改善対象の正本」が読み手に分かりづらい
- 期待効果:
  - 監査・実装・レビューのズレを減らす

### 3. 日経225系出力を既存 schema に寄せる

- 優先度: 高
- 対象:
  - `src/kanekasegi` 側の output 生成
  - top-level `src/analysis/reporting.py` の再利用方針
- 理由:
  - `trades.csv`, `equity_curve.csv`, `compare_summary.json`, `walk_forward_summary.json` は既に別 stack に存在する
- 期待効果:
  - compare / dashboard / downstream 分析の再利用性向上

### 4. 日経225 ZIP 経路の end-to-end backtest テスト追加

- 優先度: 高
- 対象:
  - `tests/test_backtest.py` 系
- 理由:
  - 現在の `test_backtest` は BTC 簡易 config であり、日経225の主経路をそのまま守っていない

### 5. `validation.py` / `portfolio_research.py` の CLI 出力テスト追加

- 優先度: 高
- 対象:
  - `tests/test_validation.py`
  - `tests/test_portfolio_research.py`
- 理由:
  - 関数テストはあるが、`--output` を含むファイル出力の end-to-end が薄い

### 6. `strategy_ids` の扱い整理

- 優先度: 中
- 対象:
  - `config.backtest.yaml`
  - `src/kanekasegi/config.py`
- 理由:
  - `strategy_ids` は config に存在するが、実行系では参照が確認できない
- 状態:
  - 未使用フィールドの可能性が高い

### 7. `config.backtest-nk225micro.usdjpy.yaml` と `config.backtest-nk225micro-usdjpy.yaml` の統合

- 優先度: 中
- 対象:
  - config 群
- 理由:
  - 同名目的の variant が二重に存在し、運用 drift の温床になる

### 8. `contract_type=next` のテスト追加

- 優先度: 中
- 対象:
  - `tests/test_jpx_data.py`
- 理由:
  - current/specific は見えるが next の保証が薄い

### 9. `run_research_grid` の位置付け整理

- 優先度: 中
- 対象:
  - `src/kanekasegi/main.py`
- 理由:
  - `run_research_grid` は `generate_default_candidates` ベースで、現在の大規模候補群を持つ `research.py::_candidate_rules()` 系と別ライン
- 期待効果:
  - 古い grid と現在の source-of-truth 候補群の混線を防ぐ

### 10. `CURRENT_RESEARCH_STATUS.md` と実行 config の対応を明示する

- 優先度: 中
- 対象:
  - `docs/CURRENT_RESEARCH_STATUS.md`
  - `docs/`
- 理由:
  - 現 leader 名は見えるが、どの config variant で再現するかは Markdown 単体では断定しづらい

## 不明点と追加確認項目

1. 現在の source-of-truth leader を再現する official config はどれか  
   - `CURRENT_RESEARCH_STATUS.md` から leader 名は読める
   - ただし、`config.backtest-nk225micro.macro.lot3.yaml` と整合的ではあるものの、コード上で leader -> config の固定マッピングは確認できていない

2. `docs/AUTOMATION_LATEST.md` の生成コードは repo 内で追い切れていない  
   - `CURRENT_RESEARCH_STATUS.md` は `research_dashboard.py` で生成元が明確
   - 一方 `AUTOMATION_LATEST.md` は外部 automation 依存の可能性が高い

3. 日経225系を top-level validation foundation へどこまで寄せたいか  
   - 既存 compare / WFO / reporting を「参照」に留めるのか
   - 出力スキーマだけ共有したいのか
   - runner まで寄せたいのか

4. `config.backtest.yaml` の位置付け  
   - Nikkei 用の旧サンプルとして残すのか
   - generic sample として README 上も切り分けるのか

## 要約表

| 区分 | ファイル | 関数/クラス | 役割 | 根拠 | 状態 |
|---|---|---|---|---|---|
| 実行入口 | `src/kanekasegi/main.py` | `main` | runtime backtest / paper / live の分岐入口 | `main.py:142-207` | 既存 |
| 実行入口 | `src/kanekasegi/research.py` | `main` / `run_research_lab` | 単体候補研究の主入口 | `research.py:3580-3697` | 既存 |
| 実行入口 | `src/kanekasegi/portfolio_research.py` | `main` / `run_portfolio_research` | ポートフォリオ研究の主入口 | `portfolio_research.py:14-77` | 既存 |
| 実行入口 | `src/kanekasegi/validation.py` | `main` / `run_*validation` | train/test / WFO 入口 | `validation.py:195-638` | 既存 |
| データ読込 | `src/kanekasegi/main.py` | `build_bot` | `runtime.data_source` に応じて provider を選ぶ | `main.py:41-61` | 既存 |
| データ読込 | `src/kanekasegi/jpx_data.py` | `JpxMinuteZipMarketDataProvider` | JPX ZIP 読込と contract/session/timeframe 整形 | `jpx_data.py:58-280` | 既存 |
| データ読込 | `src/kanekasegi/csv_data.py` | `CsvMarketDataProvider` | CSV 読込 | `csv_data.py:20-100` | 既存 |
| シグナル生成 | `src/kanekasegi/strategy.py` | `BreakoutTrendStrategy.generate_signal` | runtime path のシグナル生成 | `strategy.py:25-66` | 既存 |
| シグナル生成 | `src/kanekasegi/rule_lab.py` | `_entry_signal` / `_supports_entry` | research path の entry 判定 | `rule_lab.py:291-324`, `363-383` | 既存 |
| 約定/コスト | `src/kanekasegi/exchange_adapter.py` | `PaperExchangeAdapter.place_order` | fill / fee / slippage / realized PnL | `exchange_adapter.py:69-99` | 既存 |
| Exit | `src/kanekasegi/strategy.py` | `_manage_open_position` | runtime path の stop / trailing exit | `strategy.py:68-94` | 既存 |
| Exit | `src/kanekasegi/rule_lab.py` | `simulate_candidate` | research path の stop / TP / time stop / trailing | `rule_lab.py:490-550` | 既存 |
| Exit | `src/kanekasegi/portfolio_lab.py` | `_should_exit` | portfolio path の stop / TP / time stop / trailing | `portfolio_lab.py:152-191` | 既存 |
| サイズ計算 | `src/kanekasegi/risk.py` | `RiskEngine.size_position` | runtime path のサイズ計算 | `risk.py:34-46` | 既存 |
| サイズ計算 | `src/kanekasegi/rule_lab.py` | `_position_size` | research path のサイズ計算 | `rule_lab.py:327-343` | 既存 |
| 出力生成 | `src/kanekasegi/research.py` | `_write_checkpoint` | research checkpoint JSON | `research.py:3532-3539` | 既存 |
| 出力生成 | `src/kanekasegi/portfolio_research.py` | `main` | portfolio result JSON | `portfolio_research.py:72-76` | 既存 |
| 出力生成 | `src/kanekasegi/validation.py` | `main` | validation JSON | `validation.py:629-633` | 既存 |
| 出力生成 | `src/kanekasegi/portfolio_diagnostics.py` | `main` | diagnostics JSON | `portfolio_diagnostics.py:133-137` | 既存 |
| 出力生成 | `src/kanekasegi/research_dashboard.py` | `write_dashboard` | `CURRENT_RESEARCH_STATUS.md` 生成 | `research_dashboard.py:297-300` | 既存 |
| WFO | `src/kanekasegi/validation.py` | `run_candidate_walk_forward_validation` | candidate walk-forward | `validation.py:281-438` | 既存 |
| WFO | `src/kanekasegi/validation.py` | `run_portfolio_walk_forward_validation` | portfolio walk-forward | `validation.py:441-563` | 既存 |
| compare/WFO参照 | `src/analysis/walk_forward_runner.py` | `main` | 別 stack の walk-forward JSON 出力 | `walk_forward_runner.py:28-52` | 参照のみ |
| compare/WFO参照 | `src/analysis/compare_runner.py` | `main` | 別 stack の compare JSON 出力 | `compare_runner.py:32-65` | 参照のみ |
| 重要ギャップ | `src/kanekasegi/rule_lab.py` / `src/kanekasegi/portfolio_lab.py` | `_trade_pnl` / `simulate_portfolio` | research path に fee/slippage が未反映 | `rule_lab.py:346-350`, 研究 path から `fee_rate` / `slippage_bps` 未参照 | 要改善 |
| 重要ギャップ | `config.backtest.yaml` / `src/kanekasegi/config.py` | `strategy_ids` | config フィールドが実行系未接続 | `git grep \"strategy_ids\"` で config 以外未使用 | 要改善 |
