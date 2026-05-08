# Brother Research Gap Analysis 2026-05-08

## 結論

兄側の研究に比べて、こちらに一番足りないのは「新しい小技」ではなく、複数レーンを同時に組み合わせたときの資金効率を測る仕組みです。

こちらの現リーダーは `lot3_base10_june_t8_night_exsq_middayplain_openingrange105_rerun` で、30万円前提の利益は `+235,600`、最大DDは `10,350`、26ヶ月中26ヶ月プラスです。安定性はかなり強いです。

一方、兄側の共有 repo では、30万円・6レーン・最大同時4ポジションの portfolio review で `+639,350`、最大DD `79,500`、最低リスク余力 `66,500`、見送り `1` が記録されています。こちらより利益は大きいですが、DDと資金余力の圧迫も大きいです。

つまり、兄側との差は「勝てるルールを1本見つける力」だけではなく、複数ルールを同時運用したときに、どこまで建ててよいか、どこで見送るか、どのレーンを優先するかを検証する資金管理レイヤーにあります。

## 比較対象

### 兄側 repo

- Repo: `https://github.com/noob-matsunaga/nikkei225micro-share`
- 一時 clone: `C:\Users\issin\AppData\Local\Temp\nikkei225micro-share-codex-audit`
- 主な実装:
  - `src/nikkei225_micro_bot/`
  - `config/campaigns/`
  - `config/exact/`
  - `config/portfolio/`
  - `docs/research-*.md`
  - `docs/review-*.md`

### こちらの repo

- Repo: `C:\Users\issin\OneDrive\デスクトップ\kanekasegi`
- 主な実装:
  - `src/kanekasegi/`
  - `config.backtest-nk225micro*.yaml`
  - `docs/CURRENT_RESEARCH_STATUS.md`
  - `docs/RESEARCH_SNAPSHOT_*.md`
  - `results/*.json`

## 兄側にあって、こちらに不足しているもの

### 1. 複数レーン同時保有の portfolio review

兄側は、各ルールを「lane」として別々に走らせたあと、同時発生した売買を口座全体で突き合わせます。

- File: `src/nikkei225_micro_bot/app/run_portfolio_review.py`
- Function/Class: `run_portfolio_review`, `PortfolioReviewSpec`, `PortfolioLaneSpec`
- Why it matters: 30万円口座で複数ルールを同時運用したとき、証拠金・リスク余力・同時建玉制限・見送り回数を評価できる。
- Evidence: `portfolio.starting_capital_jpy`, `margin_per_position_jpy`, `max_total_positions`, `lanes` を YAML から読み、各 lane の trade をまとめて `review_portfolio` に渡している。
- Unknowns: 兄側の fill/cost/data とこちらの fill/cost/data が完全一致しているかは未確認。

こちらは `simulate_portfolio` の中で `open_position: _OpenPosition | None` を1つだけ持ちます。複数レーンが同時にシグナルを出しても、先に採用された1本だけが建ちます。

- File: `src/kanekasegi/portfolio_lab.py`
- Function/Class: `simulate_portfolio`
- Why it matters: 兄側の `最大同時4ポジション` の利益構造を、こちらの現行 simulator では再現できない。
- Evidence: `open_position` が単一変数で、ポジション保有中は他候補の entry を見ない。entry 時も候補順に見て最初の1件で `break` する。
- Unknowns: 現在の `max_simultaneous_positions: 3` は同時保有数ではなく、実質的には1トレード内の枚数上限として働いている。

### 2. lane priority と見送り理由の分解

兄側は lane に `priority` を持たせ、同時刻の entry を優先順位順に処理します。また、見送り理由を `margin`, `risk`, `position_limit` に分けています。

- File: `src/nikkei225_micro_bot/reporting/portfolio_review.py`
- Function/Class: `_review_portfolio_internal`, `_entry_rejection_reason`
- Why it matters: 「利益は出るが同時建玉で危ない」候補と「資金に余裕を残して運用できる」候補を分けられる。
- Evidence: `events.sort(... lane_priority ...)`, `skipped_due_to_margin_count`, `skipped_due_to_risk_count`, `skipped_due_to_position_limit_count`, `min_margin_headroom_jpy`, `min_risk_headroom_jpy` がある。
- Unknowns: 優先順位の決め方が現在の兄側 docs では一部文字化けしているため、実際の採用基準は config と結果から読む必要がある。

こちらは `min_available_balance` は持っていますが、証拠金余力・リスク余力・建玉上限見送りの内訳は portfolio result の中心指標になっていません。

### 3. exact config と campaign config の凍結運用

兄側は、良さそうなルールを `config/exact/*.yaml` に凍結し、その近傍探索を `config/campaigns/*.yaml` で管理しています。

- File: `config/exact/*.yaml`, `config/campaigns/*.yaml`
- Function/Class: `load_family_campaign_spec`
- Why it matters: 「どの条件を試したか」「どれが採用・保留・却下か」を YAML と report で追跡しやすい。
- Evidence: `FamilyCampaignSpec` に `train_test`, `walk_forward`, `monthly`, `acceptance_profiles`, `candidates` が入っている。
- Unknowns: 兄側 repo は共有用なので、実際に全 experiment output が残っているとは限らない。

こちらは多くの候補が `src/kanekasegi/research.py` の `_candidate_rules()` に直接定義されています。探索は速いですが、候補が巨大な Python 定義に埋もれやすいです。

- File: `src/kanekasegi/research.py`
- Function/Class: `_candidate_rules`
- Why it matters: 採用候補、近傍候補、却下候補のライフサイクルがコード内に混ざり、兄側の `exact/campaign/portfolio` のような階層管理が弱い。
- Evidence: `_candidate_rules()` に多数の `RuleCandidate(...)` が直書きされている。
- Unknowns: こちらも `docs/RESEARCH_SNAPSHOT_*` と `results/*.json` で履歴は残しているが、候補定義の正本化はまだ弱い。

### 4. 専門的な price-action entry style の幅

兄側は `entry_style` として多くの相場パターンを実装しています。

代表例:

- `day_session_high_overunder_failure`
- `day_session_low_overunder_reclaim`
- `day_session_midpoint_reject`
- `night_session_mean_reject`
- `night_balance_upthrust_failure`
- `night_open_drive_failure`
- `night_round_trip_failure`
- `night_gap_fade`
- `night_session_high_reclaim`
- `pullback_recovery`

- File: `src/nikkei225_micro_bot/strategy/moving_average_trend.py`
- Function/Class: `MovingAverageTrendConfig`, `MovingAverageTrendStrategy`
- Why it matters: ただのブレイクアウト/逆張りでは拾えない「日中高値失敗」「夜間平均線戻り失敗」「圧縮上抜け失敗」などの distinct family を試せる。
- Evidence: `MovingAverageTrendConfig.__post_init__` が多数の `entry_style` を許可し、`MovingAverageTrendStrategy` 内で各 style の判定に分岐している。
- Unknowns: 全 entry style が現在も有効とは限らない。docs では keep/watch/kill に分けて運用している。

こちらの `RuleCandidate.entry_mode` は基本 `breakout` と `fade` です。

- File: `src/kanekasegi/rule_lab.py`
- Function/Class: `_entry_signal`, `_supports_entry`
- Why it matters: こちらは外部要因・曜日・月・SQ・前セッション条件は強いが、ローソク足/セッション構造ベースの entry family は兄側より粗い。
- Evidence: `candidate.entry_mode` の分岐は `breakout` と `fade` が中心。
- Unknowns: 一部の兄側 style は、こちらの `prior_session_filter` や `calendar_filter` で近似できる可能性がある。

### 5. 30万円口座での exposure 設計

兄側の記録では、30万円・6レーン・最大同時4ポジションで `+639,350` が出ています。

- File: `docs/research-300k-portfolio-comparison-2026-03-29.md`
- Function/Class: ドキュメント結果
- Why it matters: ユーザーが最初に共有した「最終資金 93万9350円」に対応する中核結果。
- Evidence: `core-plus-support + both night longs max_total_positions=4` が `total_pnl_jpy +639,350`, `max_drawdown_jpy 79,500`, `min_risk_headroom_jpy 66,500`, `skipped_due_to_position_limit_count 1`。
- Unknowns: 兄側の検証期間・手数料・スリッページ・データ仕様をこちらと完全一致させる必要がある。

こちらの現リーダーは `+235,600`、最大DD `10,350` です。

- File: `docs/CURRENT_RESEARCH_STATUS.md`
- Function/Class: Current Leader
- Why it matters: こちらは安定性に強いが、目標の月5万から見ると利益不足。
- Evidence: `profit: 235600.0`, `max_drawdown: 10350.0`, `trades: 539`, `profitable_months: 26`, `losing_months: 0`。
- Unknowns: 同時保有を許可した場合、利益が伸びる一方でDDと余力がどこまで悪化するかは未検証。

### 6. baseline と challenger の二本立て

兄側は安定重視の `validated baseline` と、利益重視の `profit challenger` を分けています。

- File: `docs/current-consensus.md`, `docs/review-combined-portfolio-300k-refresh-2026-04-01.md`
- Function/Class: ドキュメント結果
- Why it matters: 本番候補と研究候補を混ぜずに、リスク許容度に応じて比較できる。
- Evidence: 30万円口座で `validated baseline` と `profit challenger` の2系統を残し、DD・余力・weak zone・rolling を比較している。
- Unknowns: `docs/current-consensus.md` は文字化けしているが、数値と config 名は読める。

こちらも `structural baseline` と `promoted leader` は持っていますが、兄側ほど「安定版」と「利益挑戦版」を明確に分けた運用ドキュメントにはなっていません。

### 7. family campaign runner

兄側には、候補群を一括で train/test、walk-forward、monthly に通す runner があります。

- File: `src/nikkei225_micro_bot/app/run_family_campaign.py`
- Function/Class: `run_family_campaign`, `rank_family_campaign_results`, `decide_campaign_candidate`
- Why it matters: 1つの family を「近傍探索 -> OOS確認 -> 月別確認 -> 採用判断」まで同じ型で回せる。
- Evidence: `FamilyCampaignResult` が `train_test`, `walk_forward`, `monthly`, `decision`, `decision_reason` をまとめる。
- Unknowns: こちらの `kanekasegi.validation` と `research_reports` で類似機能はあるが、campaign YAML から一気通貫で回す形は弱い。

### 8. live/SBI read-only 準備の厚み

兄側には SBI read-only snapshot、reconciliation、restart recovery gate の docs と tests がかなりあります。

- File: `src/nikkei225_micro_bot/app/run_sbi_readonly_smoke.py`, `src/nikkei225_micro_bot/live/*`, `docs/live-sbi-*.md`
- Function/Class: `run_sbi_readonly_smoke`, `reconciliation`, `restart_recovery`
- Why it matters: 研究から本番前の照合・復旧判断に進みやすい。
- Evidence: README に `SBI read-only`, `broker snapshot`, `reconciliation`, `restart recovery gate` が標準手順として書かれている。
- Unknowns: 今回は live 系を編集対象外としているため、機能差の確認だけに留める。

こちらにも `config.live-sbi.yaml`, `tests/test_sbi_integration.py` はありますが、現時点の主戦場は研究・検証で、SBI 本番前 read-only 運用の完成度比較はまだ不足しています。

## こちらが兄側より強いところ

### 1. enriched trade schema と損益分解

こちらは `trade_id`, `rule_id`, `session_bucket`, `vol_bucket`, `regime_id`, `config_hash`, `wf_window_id` などの enriched trade schema を持っています。

- File: `src/kanekasegi/observability.py`
- Function/Class: `EnrichedTradeRecord`, `write_pnl_breakdown_csvs`, `write_pnl_dashboard`
- Why it matters: ルール別、時間帯別、方向別、曜日別、vol/regime別の原因調査がしやすい。
- Evidence: `OBSERVABILITY_OUTPUT_FILES` と各 breakdown writer がある。
- Unknowns: 兄側にもレポートは多いが、こちらの enriched CSV の方が後分析には向いている。

### 2. 外部要因/SQ/限月フィルタの研究出力

こちらは `external_filter_summary.csv`, `sq_filter_summary.csv`, `rejected_candidates.csv` を出す仕組みがあります。

- File: `src/kanekasegi/research_reports.py`
- Function/Class: `_external_filter_rows`, `_sq_filter_rows`, `_candidate_score_rows`
- Why it matters: S&P500、USD/JPY、VIX、米10年金利、SQ週、roll week などの効果を候補ごとに比較できる。
- Evidence: `sp500_change`, `usd_jpy_change`, `vix_change`, `us10y_change_bp`, `exclude_sq_week`, `exclude_roll_week` 等の probe がある。
- Unknowns: 現リーダーの採用判断にどこまで自動反映するかはまだ改善余地あり。

### 3. 月別安定性スコア

こちらは `one_month_dependency_score`, `max_consecutive_losing_months`, `median_monthly_pnl` を持っています。

- File: `src/kanekasegi/research_reports.py`
- Function/Class: `_monthly_summary_row`, `_candidate_score_rows`
- Why it matters: 利益が1ヶ月だけに偏った候補を落としやすい。
- Evidence: `rejected_candidates.csv` に `one_month_dependency`, `weak_monthly_stability`, `test_period_negative`, `slippage_sensitive` などの理由が出る。
- Unknowns: portfolio 全体の one-month dependency は、さらに強化した方がよい。

## 優先して埋めるべきギャップ

1. `portfolio_review` 型の複数レーン同時保有 simulator をこちらに追加する。
2. `max_total_positions`, `lane_priority`, `margin_headroom`, `risk_headroom`, `skipped_due_to_position_limit` を出力する。
3. 現リーダーの6ルールを、単一ポジション型と最大同時2/3/4ポジション型で比較する。
4. 兄側の `6レーン max4` と同じ前提に寄せた apples-to-apples 検証を作る。
5. `exact` 相当の YAML を作り、採用候補を Python の巨大 `_candidate_rules()` から分離する。
6. `campaign` 相当の YAML runner を作り、family 単位で train/test + WFO + monthly + rejected reason をまとめる。
7. `day_session_high_overunder_failure`, `day_session_midpoint_reject`, `night_session_mean_reject`, `night_balance_upthrust_failure`, `pullback_recovery` をこちらの `RuleCandidate` に移植候補として検証する。
8. `validated baseline` と `profit challenger` の二本立てを dashboard に明示する。
9. slippage/手数料を `0` だけでなく、保守的ケースで leader を再評価する。
10. SBI read-only/paper 運用に進む前に、実際の証拠金・SPAN・必要資金を current config に反映する。

## 次の実装案

最初にやるべきは、戦略を増やすことではなく、こちらの portfolio simulator を兄側と同じ土俵に近づけることです。

最小実装:

1. `src/kanekasegi/portfolio_review.py` を追加する。
2. 各 candidate の trades を先に生成し、entry/exit event に展開する。
3. `max_total_positions` と `lane_priority` で採用/見送りを判定する。
4. `min_margin_headroom`, `min_risk_headroom`, `skipped_by_reason` を出す。
5. 現リーダーを `max_total_positions=1/2/3/4` で比較する。

これで、兄側の `30万円・6レーン・最大4ポジション・+639,350` に対して、こちらのルール群が「単に安全すぎて利益が伸びていない」のか、「ルール自体の edge が足りない」のかを切り分けられます。
