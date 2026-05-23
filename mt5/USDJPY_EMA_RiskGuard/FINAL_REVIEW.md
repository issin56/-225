# Final Review

## Status

- EA file: `USDJPY_EMA_RiskGuard_EA.mq5`
- Version: `1.04`
- Target symbol: `USDJPY`
- Purpose: backtest and OANDA Japan MT5 demo verification before any real-account use

## Reviewed Safety Requirements

- USDJPY only: implemented by `TARGET_SYMBOL` and a startup safety lock.
- 2-digit and 3-digit USDJPY pips: `PipSize()` returns `_Point * 10` for 3/5 digits and `_Point` otherwise.
- JST trading window: server time is converted through `JSTOffsetHours`; default is 21:00 to 24:00 JST.
- JPY account guard: when `RequireJPYAccount` is true, non-JPY accounts are blocked from new entries.
- One position only: any existing USDJPY position blocks new entries.
- MagicNumber management: EA-managed positions and history are filtered by `MagicNumber`.
- Daily trade limit: today's entry deals are counted from account history.
- Consecutive loss stop: today's closed positions are grouped by position id and evaluated after fees and swap.
- Daily, weekly, monthly loss limits: rebuilt from deal history and evaluated in account currency.
- Spread guard: current ask-bid spread is converted to pips and compared with `MaxSpreadPips`.
- Spread cooldown: after a wide-spread event, entries are paused for `SpreadCooldownMinutes`.
- Emergency floating loss brake: managed positions are closed if unrealized loss reaches `EmergencyFloatingLossLimitJPY`.
- Friday guard: late Friday entries are blocked and managed positions are closed after the configured JST hour.
- Max holding time: managed positions are closed after `MaxHoldingMinutes`.
- Timer management: Friday close and max holding checks run on tick and on `ManagementTimerSeconds`.
- No martingale/nanpin: lot size is fixed from `LotSize`; no lot escalation logic is implemented.
- Logging: entries, closes, blocks, order failures, close failures, and safety events are printed.

## Known Remaining Manual Step

MetaEditor is not installed or not discoverable in this local environment, so final MQL5 compilation must be run in MT5 MetaEditor.

Recommended command before opening MetaEditor:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\static_check.ps1
```

Run it from `mt5/USDJPY_EMA_RiskGuard`.

## Demo Test Order

1. Compile in MetaEditor.
2. Run `DryRun_NoEntry_Check.set` on USDJPY M15 and confirm `[BLOCK] EnableTrading is false.`
3. Run `OANDA_JPY_Demo_Default.set` in Strategy Tester for at least 2 to 3 years.
4. Check spread, time window, Friday close, daily trade limit, two-loss stop, and max holding close in logs.
5. Forward test on OANDA Japan MT5 demo for at least 1 month.
