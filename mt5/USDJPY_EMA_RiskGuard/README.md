# USDJPY EMA Risk Guard EA

Version: 1.04

## EAの目的

このEAは、OANDA JapanのMT5デモ口座でUSDJPYを安全に検証するための、低リスク寄りのルール型EAです。

最優先は次の3点です。

- 感情に左右されず、ルール通りに動くこと
- 損失制御と暴走防止を優先すること
- バックテストとデモ口座で検証しやすいこと

利益保証を目的にしたEAではありません。まずはバックテストとデモ口座で、1か月以上のフォワード検証を行ってください。

## 導入方法

1. `USDJPY_EMA_RiskGuard_EA.mq5` をMT5の `MQL5/Experts/` フォルダへコピーします。
2. MetaEditorでファイルを開きます。
3. コンパイルします。
4. MT5を再起動、またはナビゲータを更新します。
5. USDJPYチャートへEAを適用します。

コンパイル時にエラーが出た場合は、MetaEditor下部の `Errors` タブに出た行番号とメッセージを確認してください。このリポジトリ側では静的レビュー済みですが、最終確認は利用するMT5環境のMetaEditorで行います。

## ファイル構成

- `USDJPY_EMA_RiskGuard_EA.mq5`: EA本体
- `README.md`: 導入と設定説明
- `BACKTEST_CHECKLIST.md`: バックテスト確認項目
- `FINAL_REVIEW.md`: 安全設計の最終レビュー
- `X_RESEARCH_NOTES.md`: X由来の情報を検証候補として整理する研究メモ
- `presets/OANDA_JPY_Demo_Default.set`: OANDA Japan MT5デモ向け初期プリセット
- `presets/DryRun_NoEntry_Check.set`: 新規エントリーを止めた動作確認用プリセット
- `tools/static_check.ps1`: MetaEditor前の簡易静的チェック
- `tools/install_to_mt5.ps1`: MT5データフォルダへEAとプリセットをコピーする補助スクリプト

## MT5への入れ方

MT5で次の手順を使います。

1. `ファイル` -> `データフォルダを開く`
2. `MQL5`
3. `Experts`
4. このフォルダに `USDJPY_EMA_RiskGuard_EA.mq5` を保存
5. MetaEditorでコンパイル

PowerShellでコピーしたい場合は、MT5の `ファイル` -> `データフォルダを開く` で表示されたフォルダパスを使って、次のように実行できます。

```powershell
cd mt5\USDJPY_EMA_RiskGuard
powershell -ExecutionPolicy Bypass -File .\tools\install_to_mt5.ps1 -Mt5DataFolder "C:\Users\YOUR_NAME\AppData\Roaming\MetaQuotes\Terminal\YOUR_TERMINAL_ID"
```

事前確認だけしたい場合は、末尾に `-WhatIf` を付けてください。

## OANDA Japan MT5デモ口座での使い方

1. OANDA JapanのMT5デモ口座へログインします。
2. USDJPYチャートを開きます。
3. EAをチャートへドラッグします。
4. `自動売買を許可` を有効にします。
5. パラメータを初期値のままで開始し、まずは挙動確認を行います。

このEAはUSDJPY専用です。USDJPY以外のチャートでは安全処理により新規エントリーを行いません。
ブローカーが `USDJPY.a` のような接尾辞付きシンボルを使う場合も、安全側で取引しません。対象シンボルを広げたい場合は、実運用前にコード側の安全設計を見直してください。

## バックテストの始め方

1. MT5で `表示` -> `ストラテジーテスター` を開きます。
2. エキスパートに `USDJPY_EMA_RiskGuard_EA` を選びます。
3. 銘柄は `USDJPY` のみにします。
4. 時間足は `M15` を選びます。
5. 期間は最低2〜3年を指定します。
6. スプレッドは実運用に近い値、または変動スプレッドにします。
7. 口座通貨がJPYであることを確認します。
8. `JSTOffsetHours` をサーバー時間に合わせます。
9. テスト後、ログの `[ENTRY]`, `[CLOSE]`, `[BLOCK]`, `[NO_ENTRY]`, `[ORDER_FAIL]` を確認します。

`.set` プリセットを使う場合は、ストラテジーテスターの入力パラメータ画面から `読み込み` を押して、`presets/OANDA_JPY_Demo_Default.set` を選びます。まず発注なしでログ確認したい場合は `presets/DryRun_NoEntry_Check.set` を使います。

## 簡易静的チェック

MetaEditorでコンパイルする前に、PowerShellで最低限の構造チェックを実行できます。

```powershell
cd mt5\USDJPY_EMA_RiskGuard
powershell -ExecutionPolicy Bypass -File .\tools\static_check.ps1
```

このチェックはコンパイルの代替ではありません。USDJPY固定、pips計算、MagicNumber管理、損失制限、金曜決済、固定ロット、プリセットの入力名ズレなどを早めに見つけるための補助です。

## 推奨初期設定

- `LotSize = 0.01`
- `StopLossPips = 15`
- `TakeProfitPips = 22`
- `MaxSpreadPips = 0.5`
- `SpreadCooldownMinutes = 15`
- `MaxTradesPerDay = 2`
- `MaxConsecutiveLossesPerDay = 2`
- `DailyLossLimitJPY = 1000`
- `WeeklyLossLimitJPY = 3000`
- `MonthlyLossLimitJPY = 8000`
- `EmergencyFloatingLossLimitJPY = 1000`
- `MaxHoldingMinutes = 180`
- `TradeStartHourJST = 21`
- `TradeEndHourJST = 24`
- `FridayNoEntryAfterHourJST = 23`
- `ClosePositionsOnFriday = true`
- `FridayCloseHourJST = 23`
- `ManagementTimerSeconds = 30`
- `RequireJPYAccount = true`
- `EnableTrading = true`
- `NewsStopMode = false`

## 各パラメータの意味

- `EnableTrading`
  - 新規エントリーを許可するかどうか
- `NewsStopMode`
  - 重要指標やイベント時に手動で新規エントリーを止めるためのスイッチ
- `JSTOffsetHours`
  - サーバー時間から日本時間へ変換するための時差
  - 例: サーバー時間が冬時間のUTC+2相当なら、日本時間との差は `+7`
  - 例: サーバー時間が夏時間のUTC+3相当なら、日本時間との差は `+6`
- `RequireJPYAccount`
  - `true` の場合、口座通貨がJPY以外なら新規エントリーを止める
  - 損失上限入力はJPY口座前提のため、初期値の `true` を推奨します。
- `MagicNumber`
  - このEAが自分のポジションを識別するための番号
- `LotSize`
  - 固定ロット
- `StopLossPips`
  - 損切り幅
- `TakeProfitPips`
  - 利確幅
- `MaxSpreadPips`
  - この値を超えるスプレッドでは新規エントリーしない
- `SpreadCooldownMinutes`
  - スプレッド超過を検出した後、指定分数だけ新規エントリーを止める
  - `0` にするとクールダウンなし
- `MaxTradesPerDay`
  - 1日の新規エントリー上限
- `MaxConsecutiveLossesPerDay`
  - 当日連敗数の上限
- `DailyLossLimitJPY`
  - 日次の損失上限
  - 判定はMT5の口座通貨ベースで行います。JPY口座であればJPYとして扱えます。
- `WeeklyLossLimitJPY`
  - 週次の損失上限
  - 判定はMT5の口座通貨ベースで行います。JPY口座であればJPYとして扱えます。
- `MonthlyLossLimitJPY`
  - 月次の損失上限
  - 判定はMT5の口座通貨ベースで行います。JPY口座であればJPYとして扱えます。
- `EmergencyFloatingLossLimitJPY`
  - EA管理ポジションの含み損がこの金額を超えた場合に成行決済する緊急ブレーキ
  - `0` にすると無効
  - SLが基本の損失制御ですが、急変・約定ずれ・設定ミス検証のための追加安全弁です。
- `MaxHoldingMinutes`
  - この時間を超えて保有したら強制決済
- `TradeStartHourJST`
  - 日本時間での新規エントリー開始時刻
- `TradeEndHourJST`
  - 日本時間での新規エントリー終了時刻
- `FridayNoEntryAfterHourJST`
  - 金曜日に新規エントリーを止める時刻
  - 誤設定防止のため `0` から `23` の範囲で指定します
- `ClosePositionsOnFriday`
  - 金曜日に持ち越し回避決済をするか
- `FridayCloseHourJST`
  - 金曜日の強制決済時刻
  - 誤設定防止のため `0` から `23` の範囲で指定します
- `PullbackTolerancePips`
  - M15でEMA20付近とみなす許容幅
- `MinATRPips`
  - ATR14が低すぎる相場を除外するための最小値
- `MaxStrategyStopLossPips`
  - ストラテジーとして許容する損切り上限
- `SlippagePoints`
  - 成行発注・成行決済の許容スリッページ
- `ManagementTimerSeconds`
  - 最大保有時間と金曜決済を確認するタイマー間隔
- `OrderComment`
  - 発注コメント

## 稼働前チェック

- USDJPYチャートに適用しているか
- `Algo Trading` がONか
- `JSTOffsetHours` が正しいか
- 口座通貨がJPYか
- OANDA Japanデモ口座であるか
- `NewsStopMode` が意図通りか
- スプレッドが異常に広がる時間帯ではないか
- 金曜日の終盤ルールを理解しているか

## ログの見方

- `[INIT]`: EA起動、パラメータ、口座通貨警告
- `[ENTRY]`: 新規エントリー成功とエントリー理由
- `[CLOSE]`: EAによる成行決済と決済理由
- `[BLOCK]`: 新規エントリー禁止理由
- `[NO_ENTRY]`: 取引条件未成立の理由
- `[ORDER_FAIL]`: 注文失敗時のリターンコード、説明、最終エラー
- `[CLOSE_FAIL]`: 決済失敗時のリターンコード、説明、最終エラー
- `[SAFETY]`: 複数ポジション検出など、安全側の強制対応

## 停止条件

次のどれかに該当したら、新規エントリーを停止します。

- `EnableTrading = false`
- `NewsStopMode = true`
- USDJPY以外のチャート
- `RequireJPYAccount = true` かつ口座通貨がJPY以外
- 稼働時間外
- スプレッド超過
- スプレッド超過後のクールダウン中
- 既存ポジションあり
- 当日取引回数上限到達
- 当日連敗上限到達
- 日次損失上限到達
- 週次損失上限到達
- 月次損失上限到達
- 金曜23時以降の新規エントリー禁止時間帯
- 金曜の持ち越し回避決済時間帯

## 注意点

- このEAはナンピンしません。
- このEAはマーチンゲールしません。
- このEAは両建てしません。
- このEAは同時に1ポジションしか持ちません。
- ロット自動倍増はしません。
- 損切りと利確は必ず付与する設計です。
- 日本時間は `JSTOffsetHours` の設定に依存します。
- 損失上限をJPYとして扱うため、初期値ではJPY口座以外の新規エントリーを止めます。
- スプレッドや約定条件はデモ口座でも変動します。
- スプレッドが一瞬だけ戻った直後の荒い約定を避けるため、初期値では15分のクールダウンを入れています。
- 金曜の決済と最大保有時間は、ティック受信時とタイマー実行時に確認します。
- 日次、週次、月次損失制限は確定済みのDeal損益、スワップ、手数料を口座通貨ベースで集計します。保有中ポジションはSL、TP、緊急含み損ブレーキ、最大保有時間、金曜決済で管理します。

## リアル口座の前に必ず行うこと

- 最低2〜3年のバックテスト
- スプレッドを現実的にした検証
- デモ口座で1か月以上のフォワードテスト
- ログを確認し、停止条件・損切り・利確・時間制限がルール通り動いているかを確認

リアル口座でいきなり使わず、まずはデモ口座で十分に検証してください。
