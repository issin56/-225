# AGENTS.md

## Project goal
このリポジトリの日経225系バックテスト改善を、安全に、再現可能に進める。
目的は「見かけの利益最大化」ではなく、「過剰最適化を避けながら OOS 安定性を高める」こと。

## Current repository reality
このリポジトリには複数の workstream が存在する。
- 元の先物売買フレームワーク: `src/kanekasegi/`
- 新しい validation foundation: top-level の `src/analysis`, `src/backtest`, `src/data`, `src/papertrade`, `src/strategy`, `src/utils`

日経225系の主対象は次のとおり。
- `src/kanekasegi/`
- `config.backtest-nk225micro*.yaml`
- `config.backtest.yaml`
- `tests/`
- `docs/`

## Out of scope by default
明示的な依頼がない限り、次は編集しない。
- `config.live-gmo.yaml`
- `config.live-sbi.yaml`
- live 注文実行系
- 認証情報
- 無関係な FX validation foundation の大規模変更

## Working rules
- まず監査、次に実装
- 推測で断定しない
- すべての重要な判断にコード根拠を付ける
- 既存 runner がある場合は拡張を優先し、再実装を避ける
- 既存 CLI と既存出力の互換性を壊さない
- 変更ごとに docs を更新する
- 実験設定は再現可能にする
- ライブ系への影響がある変更は避ける

## Required outputs
変更時は必ず以下を提出する。
1. 変更ファイル一覧
2. 変更理由
3. 追加/変更した設定項目
4. 実行コマンド
5. 出力ファイル一覧
6. テスト結果
7. 残課題
8. リスク

## Evidence format
重要判断は次の形式で示す。
- File:
- Function/Class:
- Why it matters:
- Evidence:
- Unknowns:

## Quality gate
採用判断は総利益だけで行わない。
最低でも次を比較する。
- net pnl
- profit factor
- max drawdown
- trade count
- monthly stability
- OOS stability
- fee/slippage sensitivity

## Done definition
- 実装が動く
- テストが通る
- docs が更新されている
- 再現手順がある
- OOS または walk-forward の比較結果がある
- live 系に不要な変更が入っていない
