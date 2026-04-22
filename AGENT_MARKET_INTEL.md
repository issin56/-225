# Agent Market Intel

更新日: `2026-04-06`

## 方針

- X やネットの話題は、そのまま売買判断に使わない
- 使うのは、一次資料や論文から引ける仮説だけ
- 仮説は必ず `rule candidate` に落として、実データで検証する

## 今回の主要ソースから取れること

### 1. 夜間は情報反応が強い

- JPX のワーキングペーパー要約では、日中と夜間で売買行動に差があり、夜間は情報反応の色が強い
- FIA の JPX 記事でも、夜間立会は海外参加者やグローバルイベント対応の意味合いが強い

使い方:
- `night short` は外部要因フィルタと相性が良い
- 候補: `usd_jpy_change`, `sp500_change`, `vix_change`

### 2. 日本株・為替・金利はつながっている

- 日米の株式・為替・債券の連関を扱う研究では、日本市場が海外要因の影響を受ける構図が確認できる

使い方:
- `USD/JPY` は継続採用
- 次に試すのは `SP500` と `米10年金利`

### 3. VIX は「入るか見送るか」の判定に向いていそう

- FRED の `VIXCLS` は米株の不安定さを表す代表的な日次系列
- これは JPX や論文からの直接結論ではなく、上の「夜間は情報反応が強い」「米市場要因が日本へ波及する」という資料からの推論

使い方:
- `opening fade` の ON/OFF 判定
- `night short` のリスク回避フィルタ

### 4. SQ / 限月まわりは別扱いにする価値が高い

- JPX の日経225マイクロ仕様では、最終取引日や最終決済日が明確に定義されている
- この周辺は値動きの性質が通常日とズレやすい可能性がある

使い方:
- `SQ week filter`
- `last trading day blackout`
- `roll week filter`

### 5. Gotobi は主役ではなく補助

- Gotobi 論文は `USD/JPY` 側の偏りを示すが、これだけで日経225マイクロの主戦略にするのは弱い

使い方:
- 朝ショートや寄り付き系の補助条件としてだけ試す

## 現時点の研究への落とし込み

### 継続優先

- `night short + usd_jpy_change`
- `midday long + 前夜地合い`
- `fade` は補助ルールとして扱う

### 次の本命仮説

- `night short + sp500_change < 0`
- `night short + usd_jpy_change < 0 + us10y_change_bp > 0`
- `midday long + sp500_change > 0`
- `fade off when vix_change > threshold`
- `prev_session_realized_range` を内部要因として追加
- `skip around SQ / final trading day`

### 研究の読み方

- `walk-forward 4/4 pass` は固定ルール群の時期ずらし耐性
- 再最適化付き walk-forward ではない
- 外部要因は「利益を増やす」より「崩れる月を減らす」目的で使う

## 優先順位

1. `SP500` を `night short` と `midday long` に当てる
2. `VIX` を `fade` の見送り条件として当てる
3. `us10y_change_bp` を `USD/JPY` と組み合わせて当てる
4. `SQ / 限月` フィルタをコード化する
