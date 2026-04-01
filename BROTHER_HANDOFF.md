# Brother Handoff

## 現状

- プロジェクトは `SBI / NK225MICRO` 前提に寄せ済み
- `paper` / `backtest` / `live` の入口あり
- `live` は安全のため既定で発注しない
- SBI 実 API 接続だけ未実装

## いま動くもの

- 設定検証
  - `py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --validate-config`
- 自己診断
  - `py -3.11 -m kanekasegi.main --config config.live-sbi.yaml --doctor`
- バックテスト入口
  - `py -3.11 -m kanekasegi.main --config config.backtest-nk225micro.yaml`

## 兄に確認したいこと

1. SBI の API 接続資料はあるか
2. API キー / シークレットの発行方法
3. 接続先 URL
4. 認証方式
5. 新規注文の仕様
6. 返済注文の仕様
7. 取消の仕様
8. 建玉照会 / 余力照会の仕様
9. 日経225マイクロの銘柄コード
10. 実際に使っているツール名や接続サービス名

## 兄に渡す短い説明

SBI と日経225マイクロ前提で、自動売買の骨格までは作成済みです。  
いま足りないのは、SBI先物・オプションAPIの具体的な接続仕様だけです。  
もし API 登録資料や注文仕様が分かれば、その内容をもとに live 発注部分を実装できます。

## 受け取りたい形式

- PDF / スクリーンショット
- API マニュアルのURL
- 注文・返済・照会のリクエスト例
- `.env` に入れる値の項目名
