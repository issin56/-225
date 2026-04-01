# Agent Market Intel

このファイルは、日経225マイクロ研究でエージェントが参照する共通知見メモです。
ネットで拾った情報は、できるだけ公式情報を優先し、出典URLと確認日を残します。

## Rules

- 勝率だけで評価しない
- まず `profit`, `max_drawdown`, `min_available_balance`, `trades` を確認する
- 研究メモには「観測」と「仮説」を分けて書く
- X や掲示板は一次情報ではないので、補助ヒント扱いにする
- 仕様に関わる情報は必ず JPX または SBI の公式ページで確認する

## Official Facts

### JPX

- 確認日: `2026-04-01`
- 日経225マイクロは JPX の国内指数先物商品
- 取引時間は日中立会と夜間立会がある
- 限月は複数あり、期近・期先のロールを意識する必要がある
- 研究では「どの限月を採用したか」を必ず記録する

### SBI

- 確認日: `2026-04-01`
- SBI証券では先物・オプション取引の提供がある
- 実運用時は手数料、必要証拠金、発注可能時間を公式ページで再確認する
- API 実装は仕様書が入手できるまで推測で埋めない

## Working Hypotheses

- 日経225マイクロは「終日フル参加」より、時間帯を絞った方が成績が安定しやすい
- 寄り直後はノイズが多いので `skip_first_minutes` が効く可能性が高い
- 日中とナイトは値動きの性質が違うので、同じルールをそのまま当てない方がよい
- 勝率7割を狙うには、順張り単体より「見送り条件」と「時間帯制限」が重要

## Research Priorities

1. 日中限定ルール
2. ナイト前半限定ルール
3. 曜日フィルタ
4. ボラティリティフィルタ
5. 利確・損切りの出口比較

## Source Log

- JPX 日経225マイクロ商品概要: `https://www.jpx.co.jp/derivatives/products/domestic/225micro-futures/`
- JPX 日経225マイクロ制度概要: `https://www.jpx.co.jp/derivatives/products/domestic/225micro-futures/01.html`
- SBI証券 先物・オプション案内: `https://site0.sbisec.co.jp/marble/derivative/top.do?_scpr=intpr`
