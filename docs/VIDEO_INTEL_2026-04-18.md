# Video Intel 2026-04-18

## Sources

- [SBI証券公式チャンネル: 【切り抜き】"生涯利益50億円"有名個人投資家テスタ氏「先物取引をする理由とは？」](https://www.youtube.com/watch?v=Lc5faIuUIlI)
- [JPX公式: 【日経225マイクロ先物・日経225ミニオプション1周年】個別株の長期投資におけるリスクをヘッジする戦略 with 守屋史章](https://www.youtube.com/watch?v=_xghTJJKTj0)
- [JPX Overview | Nikkei 225 micro Futures](https://www.jpx.co.jp/english/derivatives/products/domestic/225micro-futures/)
- [JPX Contract Specifications | Nikkei 225 micro Futures](https://www.jpx.co.jp/english/derivatives/products/domestic/225micro-futures/01.html)

## Useful Takeaways

### 1. 先物は「レバレッジを上げる道具」だけではなく「市場リスクを打ち消す道具」として使える

- SBI動画では、テスタ氏が「先物はギャンブル性を上げるためではなく、持っている株の市場全体下落リスクを打ち消すために使う」と説明している。
- これは今の研究にそのまま売買ルールとして入る話ではないが、運用思想としてはかなり重要。
- つまり、日経225マイクロは「方向を当てるためだけの商品」ではなく、「ベータを調整するための商品」としても扱える。

### 2. 日経225マイクロはサイズ調整に向いている

- JPX公式では、日経225マイクロ先物の契約単位は `Nikkei 225 × JPY 10` とされている。
- たとえば日経平均が `40,000` のとき、1枚の想定元本は `400,000円` 規模になる。
- JPX公式では、これは `mini` の 10分の1、ラージの 100分の1のサイズと説明されている。
- 研究側では「少額口座でも段階的にロットを増やしやすい」という意味でかなり相性がいい。

### 3. マイクロは長期株ポジションのヘッジ用途と相性がいい

- JPX動画では、個別株を長期で持ちながら、地合い悪化時だけマイクロ先物売りで市場全体の下落を和らげる考え方が中心。
- これは、将来あなたが個別株と先物を併用するならかなり実務的。
- 今の自動売買研究は「先物単独で稼ぐ」前提だが、別ラインで「株保有時のヘッジモード」を作る価値はある。

### 4. 証拠金は固定値として信じない

- JPX動画では、当時の説明として「1枚あたり2万円前後で扱える」といった趣旨の話が出ている。
- ただし、JPX公式の契約仕様ページでは証拠金は `Margin Calculated by VaR Method` とされていて、固定ではない。
- つまり、動画の金額は参考にはなるが、本番設定のハードコード値には使わない。

## How We Should Use This In Our Project

### A. 売買ルールそのものには直結採用しない

- この2本の動画は、エントリー条件や利確条件の具体ルールを与える動画ではない。
- だから「この動画を見たから新しいシグナルが増える」というタイプではない。

### B. 運用設計とリスク設計に採用する

- 今後の live 前チェックでは、以下を必ず明示する。
- `1枚の想定元本 = 日経平均 × 10円`
- `発注枚数ごとの想定元本`
- `現在の必要証拠金`
- `余力に対する安全率`

### C. 研究の新しい枝として「ヘッジモード」を追加候補にする

- 将来の研究候補として、次の枝は価値がある。
- 個別株保有時の `short hedge overlay`
- 強いロング系ルールを残しつつ、地合い悪化時だけ小さくショートを重ねる `beta-control mode`
- これは今の「利益最大化ライン」とは別に、「守り重視ライン」として研究するのが自然

## Concrete Decisions

- 日経225マイクロを「少額で細かくサイズ調整しやすい商品」として扱う方針は維持する。
- 本番前の証拠金設定は、動画ベースではなく broker の最新値で上書きする。
- 研究ノート上では、今後「先物単独アルファ」と「株ヘッジ用途」を分けて考える。
- 今の主研究は引き続き「先物単独アルファ」を優先する。

## Not Adopted Directly

- 動画中の個別の証拠金目安は、そのまま本番数値には使わない。
- 「ヘッジとして便利」という話を、そのまま方向性ルールの優位性だと解釈しない。
- 切り抜き動画の説明は補助情報として扱い、仕様は JPX 公式を優先する。

## Next Video Queue

優先度高めの候補を次の探索対象として残す。

### Priority A: JPX official, strategy framing

- [225マイクロ先物を使った戦略①～チャートと板の見方について～](https://www.youtube.com/watch?v=XYl_gxam754)
- [225マイクロ先物を使った戦略②～売り,買いで収益機会を狙う～](https://www.youtube.com/watch?v=1dKRaFO-vM0)
- [225マイクロ先物を使った戦略③～値下がりリスクをヘッジする～](https://www.youtube.com/watch?v=s0sez5-sJEo)
- [相場予想パターン別 投資戦略 厳選6選 with 守屋史章](https://www.youtube.com/watch?v=hXy28TiHyCY)

### Priority B: JPX official, scenario-specific tactics

- [日経平均が上がると予想するときに取りうる戦略](https://www.youtube.com/watch?v=bRhv5x2Sn0M)
- [日経平均が下がると予想するときに取りうる戦略](https://www.youtube.com/watch?v=CwGsVxYg31o)
- [日経平均が大きく動くと予想するときに取りうる戦略](https://www.youtube.com/watch?v=ta-SwDwrUh4)
- [日経平均が動かないと予想するときに取りうる戦略](https://www.youtube.com/watch?v=Ten3p7ANIiM)

### Priority C: Secondary / idea source only

- [日経225 デイトレ 失敗｜初心者が陥りやすい3つの罠！](https://www.youtube.com/watch?v=upBU0G91P9k)
- [これを知らないとヤバイ！日経225先物取引にかかるリスクとは](https://www.youtube.com/watch?v=GY7H6kWiY3I)

### Intake Rule

- `JPX / SBI / 公式一次情報` を最優先
- 非公式動画は `アイデア源` としてだけ使う
- ルールに落とす前に、必ず既存本命との比較バックテストを通す
