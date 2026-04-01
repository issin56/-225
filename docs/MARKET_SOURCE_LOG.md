# Market Source Log

確認日: `2026-04-01`

## JPX

- 日経225マイクロ先物 商品概要
  - `https://www.jpx.co.jp/derivatives/products/domestic/225micro-futures/`
  - 取引単位は日経平均株価 × 10円
  - 呼値の単位は 5円
- 日経225マイクロ先物 制度概要
  - `https://www.jpx.co.jp/derivatives/products/domestic/225micro-futures/01.html`
  - 日中: 8:45 - 15:40、クロージング 15:45
  - 夜間: 17:00 - 翌5:55、クロージング 翌6:00
  - 取引最終日は各限月の第2金曜日の前営業日

## SBI

- SBI証券 先物・オプション案内
  - `https://site0.sbisec.co.jp/marble/derivative/top.do?_scpr=intpr`
  - 取引前に手数料、必要証拠金、発注可能時間を再確認する

## Notes

- 研究用ルールの設計では、JPXの立会時間をそのままフィルタ条件へ落とす
- 実運用時のコスト条件は SBI の最新情報で再確認する
- X や掲示板はヒントには使うが、仕様の根拠には使わない
