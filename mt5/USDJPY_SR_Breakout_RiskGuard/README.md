# USDJPY SR Breakout Risk Guard EA

Version: 1.03

## 目的

このEAは、Xで得た「日足・4時間足の重要水平線を15分足の実体でブレイクした方向を狙う」という考え方を、USDJPY専用・低リスク検証用に落とし込んだ別戦略EAです。

既存の `USDJPY_EMA_RiskGuard_EA` とは混ぜません。EMA押し目戦略とは別に、水平線ブレイク戦略としてバックテストします。

## 戦略概要

- 対象はUSDJPYのみ
- 日足と4時間足のローソク足実体から水平線候補を探す
- 実体が一定pips以内に3回以上集まった価格帯を重要水平線候補にする
- M15確定足がその水平線を実体で明確にブレイクした場合だけシグナルにする
- ヒゲ抜け、小さい実体、微妙な抜けは見送る
- 損切りはブレイクラインの反対側、またはブレイク足の高値/安値の外側
- 利確は損切り幅の `RewardRiskRatio` 倍
- ナンピン、マーチンゲール、ロット自動倍増はしない

## 主な初期設定

- `LotSize = 0.01`
- `RequireJPYAccount = true`
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
- `D1LineLookbackBars = 160`
- `H4LineLookbackBars = 240`
- `MinLineTouches = 3`
- `LineTolerancePips = 5`
- `BreakoutBufferPips = 1`
- `MinBreakoutBodyPips = 6`
- `BigCandleAtrMultiplier = 1.2`
- `MaxStopLossPips = 20`
- `RewardRiskRatio = 2`

## バックテスト手順

1. `USDJPY_SR_Breakout_RiskGuard_EA.mq5` をMT5の `MQL5/Experts/` にコピーします。
2. MetaEditorでコンパイルします。
3. ストラテジーテスターでEAを選びます。
4. 銘柄はUSDJPY、時間足はM15にします。
5. 最低2〜3年でバックテストします。
6. まず `presets/DryRun_NoEntry_Check.set` で発注なしログを確認します。
7. 次に `presets/OANDA_JPY_Demo_Default.set` で検証します。

## ログ

- `[ENTRY]`: 新規エントリー成功と水平線ブレイク理由
- `[CLOSE]`: EAによる成行決済
- `[BLOCK]`: 新規エントリー禁止理由
- `[NO_ENTRY]`: 水平線ブレイク条件未成立
- `[ORDER_FAIL]`: 注文失敗
- `[CLOSE_FAIL]`: 決済失敗
- `[SAFETY]`: 複数ポジション検出など

## 注意点

- 水平線の自動判定は裁量ラインの完全再現ではありません。
- `LineTolerancePips` と `MinLineTouches` は過剰最適化しやすいので、まず初期値で検証してください。
- ブレイク戦略はダマシが多くなる可能性があります。
- スプレッド超過後は `SpreadCooldownMinutes` 分だけ新規エントリーを止め、荒い約定直後の飛び乗りを避けます。
- 保有中の含み損が `EmergencyFloatingLossLimitJPY` に達した場合は、EA管理ポジションを緊急決済します。
- 損失上限はJPY口座前提のため、初期値では `RequireJPYAccount=true` でJPY以外の新規エントリーを止めます。
- 指標時の急変に弱い可能性があるため、`NewsStopMode` の手動停止も検証してください。
- リアル口座ではなく、必ずバックテストとデモ口座で確認してください。

## 簡易静的チェック

```powershell
cd mt5\USDJPY_SR_Breakout_RiskGuard
powershell -ExecutionPolicy Bypass -File .\tools\static_check.ps1
```

このチェックはMetaEditorコンパイルの代替ではありません。
