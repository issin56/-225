# Market Source Log

更新日: `2026-04-06`

## 公式ソース

### JPX

- [Nikkei 225 Micro Futures Overview](https://www.jpx.co.jp/english/derivatives/products/domestic/225micro-futures/)
  - 商品概要と基本仕様の確認用

- [Nikkei 225 Micro Futures Contract Specifications](https://www.jpx.co.jp/english/derivatives/products/domestic/225micro-futures/01.html)
  - 最終取引日、最終決済日、呼値、価格制限の確認用

- [Trading Hours / Night Session](https://www.jpx.co.jp/english/derivatives/rules/trading-hours/01.html)
  - 夜間立会の正式な時間帯確認用

### FRED

- [DEXJPUS](https://fred.stlouisfed.org/series/DEXJPUS)
  - `USD/JPY` の日次系列生成に使用

- [SP500](https://fred.stlouisfed.org/series/SP500)
  - 米株地合いの前日代理変数として使用

- [VIXCLS](https://fred.stlouisfed.org/series/VIXCLS)
  - リスク回避局面の代理変数として使用

- [DGS10](https://fred.stlouisfed.org/series/DGS10)
  - 米10年金利変化の代理変数として使用

## 論文・研究

- [JPX Working Paper Summary: Analysis of Differences in Trading Behavior at Day and Night Sessions for Nikkei 225 Futures](https://www.jpx.co.jp/english/corporate/research-study/working-paper/b5b4pj000000i468-att/E_Summary_JPX_working_paper_No14.pdf)
  - 日中と夜間で売買行動に差があることの根拠

- [FIA: The Market Never Sleeps: The Success of Extended Trading Hours at JPX](https://www.fia.org/marketvoice/articles/market-never-sleeps-success-extended-trading-hours-jpx)
  - 夜間立会が海外参加者対応として重要であることの補強

- [Linkages among the Foreign Exchange, Stock, and Bond Markets in Japan and the United States](https://arxiv.org/abs/2310.16841)
  - 日本市場へ海外要因が波及する仮説の根拠

- [Forex Trading Strategy That Might Be Executed Due to the Popularity of Gotobi Anomaly](https://arxiv.org/abs/2301.13204)
  - Gotobi を補助条件として扱う際の参考

- [Realized and Range-Based Volatility Measures for the Nikkei Stock Average](https://arxiv.org/abs/2502.02695)
  - `prev_session_realized_range` のような内部ボラ要因を作る参考

## ここから取る実務仮説

- 夜間ルールは `USD/JPY`, `SP500`, `VIX` の前日変化で見送り判定を作る
- 朝の `fade` は `VIX` 上昇局面で切る価値がある
- `SQ / 最終取引日 / 限月切替週` は通常日と分けて扱う価値がある
- `Gotobi` は主ルールではなく補助フィルタとして試す

## 注意

- SNS やニュースは仮説の種に留める
- 実際に採用するのは、一次資料で意味づけできて、バックテストで残るものだけ
