# Brother Handoff

## 現状

- プロジェクトは `SBI / NK225MICRO` 前提で組み替え済み
- `paper` / `backtest` / `live` の入口はある
- `live` は既定で発注しない安全弁つき
- JPX の分足 ZIP をそのまま読んでバックテストできる
- SBI の実注文 API 配線だけ未実装

## すぐ確認できること

- 設定チェック
  - `py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --validate-config`
- 自己診断
  - `py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --doctor`
- 日経225マイクロのバックテスト
  - `py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml`
- 簡易パラメータ探索
  - `py -3.11 -m kanekasegi.research --config config.backtest-nk225micro.yaml --top 10 --min-trades 10`

## 不足しているもの

1. SBI の API 接続資料
2. API キー / シークレット
3. 接続先 URL
4. 認証方式
5. 新規注文 API の仕様
6. 返済注文 API の仕様
7. 取消 API の仕様
8. 建玉 / 余力照会 API の仕様
9. 日経225マイクロの銘柄コード
10. 実際に使っている資料やサンプル

## 注意点

- SBI と日経225マイクロ前提の土台はあるが、実発注はまだ未接続
- 未接続の理由は、SBI のエンドポイント単位の一次資料がまだないため
- API 仕様が分かれば `src/kanekasegi/sbi_adapter.py` にそのまま差し込める
