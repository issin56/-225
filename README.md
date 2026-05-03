# Kanekasegi Bot

This repository now contains two workstreams:

1. The original `kanekasegi` futures trading and research framework
2. A newer FX validation foundation for safe staged development

The intent is to keep live execution concerns isolated while building and validating strategy logic in safer layers first.

## Kanekasegi

The original project remains under `src/kanekasegi/`.

Main capabilities:

- Backtest, paper, and live-oriented modes
- Safety-first rule-based futures workflow
- Broker adapters and runtime checks
- Research utilities and batch scripts

Typical setup:

```powershell
py -m venv .venv
. .venv\Scripts\Activate.ps1
py -m pip install -e .[dev]
Copy-Item .env.example .env
```

Typical commands:

```powershell
py -m kanekasegi.main --config config.yaml --once
py -m kanekasegi.main --config config.yaml --validate-config
py -m kanekasegi.main --config config.backtest.yaml
```

Nikkei 225 walk-forward audit example:

```powershell
py -m kanekasegi.validation --config config.backtest-nk225micro.macro.lot3.yaml --mode portfolio-walk-forward --candidate <rule-id> --candidate <rule-id>
```

## FX Foundation

The FX validation foundation lives in the top-level `src/` packages:

```text
src/
  analysis/
  backtest/
  data/
  papertrade/
  strategy/
  utils/
config/
tests/
output/
```

Current scope:

1. Backtesting
2. Signal-only paper trade decisions
3. A structure that can later move toward small-size live execution

### Current Features

- Load OHLCV data from CSV
- Validate required columns: `timestamp, open, high, low, close, volume`
- Support `moving_average_cross` and `breakout` strategies
- Simulate fixed stop loss, take profit, spread, commission, and risk sizing
- Write trades, summary, equity curve, period summary, comparison, and walk-forward outputs
- Keep signal-only paper trade state and decision journals
- Scan multiple symbols from one config
- Run walk-forward validation with parameter search

### Main Commands

Run commands from the repository root.

Backtest:

```powershell
py -m src.backtest.runner --config config/backtest.sample.json
```

Breakout sample:

```powershell
py -m src.backtest.runner --config config/backtest.breakout.sample.json
```

Walk-forward validation:

```powershell
py -m src.analysis.walk_forward_runner --config config/backtest.sample.json
```

Compare multiple configs:

```powershell
py -m src.analysis.compare_runner --configs config/backtest.sample.json config/backtest.breakout.sample.json
```

Signal-only paper trade:

```powershell
py -m src.papertrade.runner --config config/backtest.sample.json
py -m src.papertrade.runner --config config/papertrade.multi.sample.json --all-symbols --reset-state
```

Run tests:

```powershell
py -m pytest tests
```

### FX Config Files

- `config/backtest.sample.json`
- `config/backtest.breakout.sample.json`
- `config/papertrade.multi.sample.json`

### FX Output Files

Generated files are written under `output/`. Only `output/.gitkeep` is tracked.

Examples:

- `output/trades.csv`
- `output/summary.json`
- `output/equity_curve.csv`
- `output/period_summary.json`
- `output/walk_forward_summary.json`
- `output/compare_summary.json`
- `output/signal_snapshot.json`
- `output/papertrade_state.json`
- `output/papertrade_journal.jsonl`
- `output/notifications.jsonl`

## Notes

- The original `kanekasegi` code is preserved as-is in this repository.
- The FX foundation is intentionally focused on validation and paper signals, not live order execution.
- Test CSV fixtures are stored under `tests/fixtures/`.
