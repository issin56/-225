# Operations Guide

## Install

```bash
py -3.11 -m pip install -e .[dev]
copy .env.example .env
```

## Validate

```bash
py -3.11 -m kanekasegi.main --config config.yaml --validate-config
py -3.11 -m kanekasegi.main --config config.yaml --doctor
py -3.11 -m pytest
```

## Backtest

```bash
py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml
```

## Research

```bash
py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 10 --min-trades 10
```

- Current research note: `RESEARCH_NOTES.md`
- Brother handoff: `BROTHER_HANDOFF_JA.md`
- Brother request template: `BROTHER_REQUEST_TEMPLATE_JA.md`

## Paper

Single cycle:

```bash
py -3.11 -m kanekasegi.main --config config.yaml --once
```

Continuous:

```bash
py -3.11 -m kanekasegi.main --config config.yaml
```

## SBI Live

1. Set `SBI_API_KEY` and `SBI_API_SECRET` in `.env`
2. If your SBI API registration materials specify an endpoint or tool name, also set `SBI_API_ENDPOINT` and `SBI_API_TOOL_NAME`
2. Check broker connectivity

```bash
py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --doctor
py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --check-broker
```

3. Start in blocked-live mode first

```bash
py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --once
```

4. Only after checking logs and health, explicitly enable live orders

```bash
py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --enable-live-orders
```

## Health And Logs

- Health file: `logs/health.json`
- Paper log: `logs/bot.jsonl`
- Backtest log: `logs/backtest.jsonl`
- SBI live log: `logs/live-sbi.jsonl`

## Safety Notes

- `live` mode does not place orders unless `live_order_enabled` is turned on.
- In OneDrive environments, SQLite may fall back to a temp directory automatically.
- SBI live trading here is oriented to Nikkei 225 Micro via SBI先物・オプションAPI registration flow.
