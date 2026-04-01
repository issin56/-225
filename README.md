# Kanekasegi Bot

安全装置を優先した、先物向けの自動売買フレームワークです。`backtest` / `paper` / `live` の3モードで同じ戦略ロジックを再利用できる構成にしています。

## できること

- ルールベースの順張り戦略
- ATRベースの初期ストップとトレーリング管理
- 日次損失上限、同時保有数制限、異常時停止
- SQLiteによる状態永続化
- Discord Webhook通知
- 合成データまたはCSV履歴データでのバックテスト
- Docker前提の実行環境

## セットアップ

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e .[dev]
copy .env.example .env
```

## 実行

紙上売買または合成データ実行:

```bash
python -m kanekasegi.main --config config.yaml --once
```

設定チェックだけ行う:

```bash
python -m kanekasegi.main --config config.yaml --validate-config
```

最新ヘルス状態を確認:

```bash
python -m kanekasegi.main --config config.yaml --status
```

GMOコイン live 接続チェック:

```bash
python -m kanekasegi.main --config config.live-gmo.yaml --check-broker
```

CSV履歴データでバックテスト:

1. `config.backtest.yaml` を使う
2. `runtime.csv_path` にCSVファイルのパスを設定
3. 次を実行する

```bash
python -m kanekasegi.main --config config.backtest.yaml
```

CSVは `timestamp,open,high,low,close,volume` の列を持つ必要があります。サンプルは `data/sample_ohlcv.csv` です。

## Docker常駐

```bash
docker compose up -d --build
```

ログは `logs/`、SQLite は `data/` に保持されます。

## テスト

```bash
pytest
```

## 補足

- `live` モードは現在 `GMOコイン` の公開データ取得と口座接続確認まで対応しています。
- GMOコインのAPI公式ドキュメントでは現物とレバレッジ取引が対象で、海外取引所の無期限先物とは商品性が異なります。
- GMOの新規成行注文は実装済みですが、クローズ注文は安全のためまだブロックしています。
- `paper` モードはバックテストと同じ戦略・リスクロジックを共有します。
- `.env` は起動時に自動読込されます。
- `logs/health.json` に最新のヘルス状態を書き出すので、外部監視から参照できます。
- この環境ではまだPython本体が未導入のため、コード生成後の実行確認は未実施です。
