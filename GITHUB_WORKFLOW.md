# GitHub Workflow

## Goal

このプロジェクトを「研究履歴が追える状態」で育てる。

## Repository Policy

- GitHub は `private repository` 前提
- コード、設定テンプレ、研究メモを管理する
- API キー、口座情報、生データ ZIP はコミットしない

## Ignore Policy

コミットしないもの:

- `.env`
- `logs/`
- `data/*.db`
- `results/` の一時出力
- `C:/Users/issin/Downloads/future_ohlc_minute_23_*.zip`
- 大きい CSV / ZIP

## Branch Strategy

- `main`: 安定版
- `codex/research-*`: ルール研究
- `codex/sbi-*`: SBI 接続
- `codex/docs-*`: ドキュメント整備

## Commit Examples

- `feat: add JPX zip research loader`
- `feat: add session/time filters for NK225Micro`
- `docs: add market intel notes`
- `test: cover research lab ranking`

## Recommended Loop

1. ルール仮説を 1 つ作る
2. ブランチを切る
3. バックテストを回す
4. 結果を `RESEARCH_NOTES.md` か `results/` に残す
5. 良ければ統合、悪ければ破棄する

## Decision Rule

- 勝率だけでマージしない
- `profit > 0`
- `max_drawdown` が許容内
- `min_available_balance` が危険域を割らない
- `trades` が少なすぎない
