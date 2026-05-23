# Final Review

## Status

- EA file: `USDJPY_SR_Breakout_RiskGuard_EA.mq5`
- Version: `1.03`
- Target symbol: `USDJPY`
- Strategy: D1/H4 body-based support/resistance breakout with M15 confirmed body break

## Safety Review

- USDJPY以外では稼働しない
- `RequireJPYAccount=true` の場合、JPY以外の口座では新規エントリーしない
- MagicNumberでEA管理ポジションを識別する
- USDJPYの既存ポジションがあれば新規エントリーしない
- 固定ロットのみで、ナンピン・マーチンゲール・ロット自動倍増なし
- SL/TPは発注時に必ず設定する
- SL幅は `MinStopLossPips` と `MaxStopLossPips` の範囲内だけ許可する
- TPはSL幅の `RewardRiskRatio` 倍で設定する
- スプレッド超過後は `SpreadCooldownMinutes` 分だけ新規エントリーを停止する
- 保有中の含み損が `EmergencyFloatingLossLimitJPY` に達したらEA管理ポジションを緊急決済する
- 日次、週次、月次損失制限は履歴Dealから再構築する
- 2連敗停止は手数料・スワップ込みのポジション単位損益で判定する
- 金曜新規停止、金曜決済、最大保有時間決済を実装済み
- ティックとタイマーの両方で管理決済を確認する

## Known Remaining Manual Step

この環境ではMetaEditorが見つからないため、最終コンパイルはMT5 MetaEditorで行う必要があります。

```powershell
cd mt5\USDJPY_SR_Breakout_RiskGuard
powershell -ExecutionPolicy Bypass -File .\tools\static_check.ps1
```

静的チェック後、MetaEditorでコンパイルしてください。
