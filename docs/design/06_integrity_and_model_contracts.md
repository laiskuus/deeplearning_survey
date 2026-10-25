# 論理データモデルの横断整合性・状態制約（実装仕様）

この仕様は新規構築における**全ER図・API・カタログに共通する制約**を定める。PlantUMLの個々の図は同じスキーマの部分投影である。FK記号だけで検証できない業務ルールは、DBのCHECK／UNIQUE／FK／遅延制約トリガや、権限付きトランザクションで実現する。

## 1. 識別子・分類・一次概念

| 集約 | PK型 | 定義 |
|---|---|---|
| `CONCEPT` | UUID | 分類に依存しない語義の同一性 |
| `CLAIM` | UUID | 正規化された1命題 |
| `EVIDENCE` | UUID | 1つの型付き根拠 |
| `INTERVENTION` | UUID | 1種類の改善・検知介入 |
| `METRIC` | UUID | 指標系列の同一性 |
| `METHOD` | UUID | 手法・アルゴリズムの同一性 |
| `TOPIC_AREA` | TEXT | 分類カテゴリの安定識別 |
| `TOPIC_AREA_VERSION` | UUID | 1分類版の同一性 |

`CONCEPT`は**分野を含むコードを保持しない**。`catalog/concepts.yaml` と `catalog/concept_topic_assignments.yaml` が、それぞれ概念辞書と所属の唯一の正本。`CONCEPT_TOPIC_ASSIGNMENT`により多対多で所属を管理し、領域別件数は所属から計算する。未検証カタログ候補は公開済み知識へ直接投入しない。

## 2. 主張と根拠の排他・整合制約

**型付き関係の端点**：`METHOD`（研究上の手法）と`INTERVENTION`（具体的な改善・検知介入の種類）は別ID体系である。初期の `method_concept_links.yaml` は `METHOD_EFFECT` の候補を表し、`INTERVENTION_EFFECT` に直接登録しない。`RELATION_TYPE.subject_types/object_types` で `CONCEPT→CONCEPT`、`METHOD→CONCEPT`、`INTERVENTION→CONCEPT`、`CONCEPT→METRIC` を制約する。


1. 公開状態の`CLAIM`には、`CONCEPT_RELATION` / `METHOD_EFFECT` / `INTERVENTION_EFFECT` / `METRIC_LINK` の**ちょうど1種類・1行**の型付き子を持たせる。承認前の提案はステージング側に保存する。
2. 公開状態の`EVIDENCE`には `LITERATURE_EVIDENCE` / `EXPERIMENT_EVIDENCE` の**ちょうど一方**に出典を持たせる。文献出典内では`assertion_id`, `paper_result_id`, `paper_comparison_id`の非NULL数を1にし、実験出典内でも `evaluation_id`, `comparison_id`, `analysis_id`, `hypothesis_assessment_id`の非NULL数を1にする。
3. `CLAIM_EVIDENCE`は関係の評価（supports/refutes/qualifies）であり、`CLAIM`そのものの真偽の自動確定ではない。反対のエビデンスを削除してはならない。
4. 文献の `SOURCE_ASSERTION` と `PAPER_RESULT` の正式版には承認済み `approved_review_id`（NOT NULL）を要求する（下書き行は正式テーブルに作らずステージングで管理）。
5. `SOURCE_ASSERTION.document_version_id = SOURCE_EXCERPT.document_version_id` を保証する。`PAPER_RESULT` は `PAPER_ARM → PAPER_EXPERIMENT → DOCUMENT_VERSION` と `SOURCE_EXCERPT.document_version_id` の一致を保証し、他版の断片を参照させない。
6. `PAPER_COMPARISON`の2つの `PAPER_ARM` は同一 `PAPER_EXPERIMENT` に属する。 `PAPER_RESULT_INTERPRETATION`のresult/comparison参照は**ちょうど1つ**。
7. `SOURCE_ASSERTION_CLAIM` は引用と一般化の対応付けに人のレビューが必要。原著者が実際に述べた範囲を超える断定的な`CLAIM`へ自動変換しない。

### PostgreSQL実装時の制約例

```sql
-- 型付き出典の子行内ではCHECKで排他を担保できる。
ALTER TABLE literature_evidence
  ADD CONSTRAINT literature_evidence_one_source
  CHECK (num_nonnulls(assertion_id, paper_result_id, paper_comparison_id) = 1);
ALTER TABLE experiment_evidence
  ADD CONSTRAINT experiment_evidence_one_source
  CHECK (num_nonnulls(evaluation_id, comparison_id, analysis_id, hypothesis_assessment_id) = 1);
```

親`EVIDENCE`から複数の子テーブル全体を見渡した「ちょうど一方」は単一行CHECKでは保証できない。排他を遅延制約トリガ／出典型別のDB権限付き書込トランザクションで保証する。承認レビューは承認された提案の**内容ハッシュ・承認者・日時**と必ず照合する。

## 3. 実験の比較可能性

- `METRIC.metric_id`はUUID。論文中の`PAPER_RESULT.metric_id`も同型で、指標不明の場合はNULLを許す。自社評価の`METRIC_RESULT`は計算仕様を固定する`METRIC_SPEC_VERSION`を必ず参照する。
- `COMPARISON_METRIC_DELTA.baseline_metric_result_id`は当該`EXPERIMENT_COMPARISON.baseline_evaluation_id`由来で、`candidate_metric_result_id`はcandidate側由来とする。両方が同じ評価側から来たときは拒否。
- 同一指標系列に属しても、`metric_spec_id`、スライス定義、ラベル方針、評価閾値、母集団、サンプル対応付けが比較できるとは限らない。**同値または承認済みの変換規則**がなければ差分を計算しない。
- 対応のある検定／Bootstrapでは、少なくとも sample_id・評価splitの内容ハッシュ・対応集合・統計推定仕様を固定する。テストデータをモデル選択に使わない。
- `result_status=ok`で数値が未設定なら拒否、`undefined/insufficient_labels/not_reported`はNULLとし、0を代入しない。
- `DATASET_VERSION`、`DATA_SPLIT`、`IMPLEMENTATION_VERSION`、`EVALUATION_PROTOCOL`、`METRIC_SPEC_VERSION`の確定後上書きを禁止する。変更は新しい版として登録する。

## 4. 承認と実行要求のハッシュ固定

`EXECUTION_REQUEST` の immutable な署名対象は次の通り。

| 属性 | 保管値 |
|---|---|
| 計画 | `experiment_plan_id`, `plan_hash` |
| 入力 | `input_hash`（データ版・分割・manifestのdigest集合） |
| 実装 | `implementation_digest`（コードtree/containerの固定digest） |
| 設定 | `config_hash`（seed・実効パラメータを含む） |
| 計算資源 | `resource_budget_json`（GPU、時間、費用等を正規化） |
| 合成値 | `request_hash`（型・値・並びを規範化した上記内容のSHA-256） |

`EXECUTION_APPROVAL` は `request_hash` と承認予算・有効期限を、`EXECUTION_DISPATCH` は `approval_id` と照合済み `request_hash` を保持。提出後の要求内容を書き換えず、変更が生じたときは別要求と別承認を作る。

Dispatchの原子処理は、(a)権限と承認者、(b)承認決定がapprovedか、(c)期限、(d)予算、(e)要求ハッシュ一致、(f)二重投入防止を確認し、Dispatchと監査を同じトランザクションで作成する。外部GPUキューへの投入はtransactional outbox等で一度だけ扱えるようにする（外部システムが提供する冪等キーと組み合わせる）。

## 5. 知識更新のトランザクション

- `EXTRACTION_CANDIDATE`や`KNOWLEDGE_PROPOSAL`は未承認の作業領域。`CONCEPT` / `CLAIM` / `SOURCE_ASSERTION` / `PAPER_RESULT` の確定行を作成できるのはレビューを適用する専用のサービス権限のみ。
- 承認時は `KNOWLEDGE_PROPOSAL.payload_hash = REVIEW_DECISION.proposal_hash` を照合し、1トランザクションで正式行・出典・監査行を確定する。差戻し／否認は正式行を変更しない。
- 新根拠が加わっても `CLAIM`を自動的に`proven`へ更新せず、 `EVIDENCE_SYNTHESIS`→`SYNTHESIS_REVISION` と承認済み判断を別版にする。
- 概念の表記訂正は `CONCEPT_REVISION`、意味の違いは新しい `CONCEPT` を作り、関連概念として明示する。分類の変更でIDは変えない。

## 6. 受入テストの責務境界

静的な`../checks/validate_package.py`は、YAMLの参照、一意性、述語の型、ERの共通キー型、参照ドキュメントと配布物のチェックサムを検証する。**実DBを伴う**承認トランザクション、型付き子排他、複合文書版FK、スライスの比較適合、二重ジョブ投入は`../contracts/02_api_contracts_and_tests.md`のAT15〜20を実装フェーズで検証する必要がある。静的検証をDBの動作検証と誤認しない。
