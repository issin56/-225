# MT5 Expert Advisors

このフォルダには、USDJPY検証用のMT5 EAを戦略別に分けて配置しています。

リアル口座でいきなり使うためのものではありません。まずMetaEditorでコンパイルし、ストラテジーテスターとOANDA Japan MT5デモ口座で検証します。

## EA一覧

### USDJPY_EMA_RiskGuard

- 戦略: H1のEMA20/EMA50で方向判定し、M15のEMA20付近の押し目・戻り売りを狙う
- 特徴: 低リスク、シンプル、トレンドフォロー寄り
- 入口: `USDJPY_EMA_RiskGuard/README.md`

### USDJPY_SR_Breakout_RiskGuard

- 戦略: D1/H4の実体ベース水平線を、M15確定足が明確にブレイクした方向を狙う
- 特徴: X研究メモから分離した別戦略。EMA版とは混ぜずに比較する
- 入口: `USDJPY_SR_Breakout_RiskGuard/README.md`

## 共通安全設計

- USDJPY以外では取引しない
- 初期設定ではJPY口座以外の新規エントリーを止める
- 固定ロットのみ
- ナンピン禁止
- マーチンゲール禁止
- ロット自動倍増なし
- 同時保有は1ポジションのみ
- MagicNumberでEA管理ポジションを識別
- SL/TPを必ず設定
- 1日最大2回まで
- 2連敗で当日停止
- 日次、週次、月次損失制限
- 保有中ポジションの緊急含み損ブレーキ
- スプレッド制限
- スプレッド超過後のクールダウン
- 金曜深夜の新規停止
- 金曜の週末持ち越し防止決済
- 最大保有時間決済

## 推奨検証順

1. `tools/run_all_static_checks.ps1` を実行する
2. MetaEditorで各EAをコンパイルする
3. `DryRun_NoEntry_Check.set` で発注なしログを確認する
4. `OANDA_JPY_Demo_Default.set` で2〜3年バックテストする
5. EMA版とSRブレイク版を別々に評価する
6. 良さそうな方だけOANDA Japan MT5デモ口座で1ヶ月以上フォワードテストする

## 一括静的チェック

```powershell
cd mt5
powershell -ExecutionPolicy Bypass -File .\tools\run_all_static_checks.ps1
```

このチェックはMetaEditorコンパイルの代替ではありません。入力パラメータ、プリセット整合性、安全ガードの実装漏れを早期に見つけるための補助です。

## 検証用テンプレート

- `TEST_MATRIX.md`: 安全テストと戦略別テストの一覧
- `backtest_results_template.csv`: バックテスト結果を同じ形式で記録するCSV

## 比較で見る指標

- 総損益
- プロフィットファクター
- 最大ドローダウン
- 勝率
- 平均利益
- 平均損失
- 最大連敗
- 月別損益
- 取引回数
- 損益カーブ

## 採用基準

- 取引回数が少なすぎない
- 最大ドローダウンが許容範囲
- 月別損益が一部期間だけに偏りすぎない
- 指標時やスプレッド拡大時に異常な負け方をしない
- デモ口座でもバックテストと大きく違わない
