# Agent NK225Micro Facts

## Official Facts

- Osaka Exchange launched Nikkei 225 micro futures on `2023-05-29`.
  - Source: [JPX news release](https://www.jpx.co.jp/english/corporate/news/news-releases/0060/20230529-02.html)
- SBI Securities publicly explains that Nikkei 225 futures come in `large`, `mini`, and `micro` sizes and positions micro as the smallest-size product for smaller capital.
  - Source: [SBI product introduction](https://www.sbisec.co.jp/ETGate/?OutSide=on&_ActionID=DefaultAID&_ControlID=WPLETmgR001Control&_DataStoreID=DSWPLETmgR001Control&_PageID=WPLETmgR001Mdtl30&_scpr=intpr%3Dfuture_debut_jc_top&burl=search_op&cat1=op&cat2=info&dir=info&file=future_debut.html&getFlg=on)

## Local Modeling Assumptions

- Data source is JPX minute ZIP data under `C:/Users/issin/Downloads`.
- `session_id=999` is mapped to `day`.
- `session_id=003` is mapped to `night`.
- Current contract selection uses the highest-volume contract for each trade day.
- Baseline live broker target remains `SBI`, but live order wiring still needs broker-side request specs.

## Implications For Research

- Small account research must track margin buffer, not just PnL.
- Time-of-day filtering is likely material because JPX day and night behavior differ.
- Contract-roll handling matters because the selected dominant month changes across the sample.
- Any rule candidate should be judged by both total profit and monthly stability.

## Do Not Assume

- Do not assume a high win rate means a good rule.
- Do not assume a rule that works on one quarter generalizes.
- Do not assume social-media heuristics are valid without backtesting.
