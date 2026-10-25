# コアオントロジー・関係・根拠：論理モデル正規化リファレンス

この文書は `../design/01_architecture_and_data_model.md` に対する**基本テーブルの仕様補足**である。
初期データは `../catalog/` 配下のYAMLに格納する。分類所属は `concept_topic_assignments.yaml` が唯一の正本となり、`CONCEPT` レコード内には分類FKを持たない。

## 1. 一次要素とビューの設計原理

- **一次概念**：`CONCEPT`。データ不足・過学習・Shortcut Learningなど。分類が変化しても `concept_id UUID` は不変。
- **課題のインスタンス**：`PROBLEM = (requirement, context, observed_or_expected_gap)`。概念と問題の実例は同一ではない。
- **関係の主張**：`CLAIM` と、意味が異なる型付き辺。主張は成立条件・確信状態・エビデンスを持つ。
- **ビュー**：`TOPIC_AREA` / `TOPIC_AREA_VERSION` / `CONCEPT_TOPIC_ASSIGNMENT` の多対多分類。研究領域と因果役割は同義ではない。
- **介入／方法／指標**：`INTERVENTION`（改善操作）、`METHOD`（手法・アルゴリズム）、`METRIC`（測定概念）として別型で管理する。

## 2. 論理エンティティ一覧と1行の意味

| テーブル | 1行の単位 | 主要列（*必須） | 一意性・整合性 |
|---|---|---|---|
| `CONCEPT_KIND` | 主たる意味型 | `kind_code*`, `kind_name*`, description | `S/M/F/C/R`。原因／結果は固定しない |
| `CONCEPT` | 一つの概念の同一性 | `concept_id UUID PK`, `kind_code* FK`, `canonical_name*`, `label_ja`, `definition*`, `status` | 名前が同じでも意味が違えば別ID |
| `CONCEPT_ALIAS` | 同義名・訳語 | `concept_id*`, `alias_text*`, `language*` | UQ `(concept_id,alias_text,language)` |
| `CONCEPT_REVISION` | 定義・表記の改訂 | `revision_id PK`, `concept_id FK`, `revision_no`, `snapshot`, `reason` | UQ `(concept_id,revision_no)`；意味変更は新概念 |
| `CONCEPT_SUPERSESSION` | 概念の統合・置換・分割を記録 | `old_concept_id`, `new_concept_id`, `relation_kind`, `review_id` | 古いIDを削除せず後継関係を保持 |
| `TOPIC_AREA` | 研究領域の安定した識別 | `area_id PK`, `area_kind` | 初期20領域、M:N所属 |
| `TOPIC_AREA_VERSION` | 領域の版管理 | `topic_version_id PK`, `area_id FK`, `revision_no`, `name`, valid_from/to | 名称と階層の変更でもConcept IDは不変 |
| `CONCEPT_TOPIC_ASSIGNMENT` | 版付き領域への1所属 | `concept_id FK`, `topic_version_id FK`, status, valid_from/to, review_id | カタログ上の最初の領域以外にも所属可能 |
| `VIEW_DEFINITION` | 検索・集約ビュー定義の1版 | `view_id`, name, query_or_spec, revision_no | 分類コードをConcept IDへ埋め込まない |
| `REQUIREMENT` | 性能・品質・安全性の要件 | `requirement_id PK`, target_metric?, comparator?, target_value?, explanation | 例：Recall≥0.99 |
| `CONTEXT` | 問題の成立環境 | `context_id PK`, task?, domain?, condition_spec JSONB | 照明、製品、装置、期間、データ条件 |
| `PROBLEM` | 条件下の要求達成ギャップ | `problem_id PK`, `requirement_id FK`, `context_id FK`, observed_gap, status | 条件・要件・現象の区別必須 |
| `PROBLEM_CONCEPT` | 問題と概念のリンク | `problem_id FK`, `concept_id UUID FK`, role_in_problem | 原因候補と観測症状を混同しない |
| `RELATION_TYPE` | 主張の述語 | `predicate_code PK`, name, semantics, subject_types, object_types, transitive_flag?, symmetric_flag? | `is_a`と`can_cause`を区別 |
| `CLAIM` | 検証可能な命題 | `claim_id UUID PK`, claim_kind, condition_text, epistemic_status, review_status | 出典と条件がない場合は未確認として扱う |
| `CONCEPT_RELATION` | Concept→Concept主張の端点 | `claim_id PK/FK`, `subject_concept_id UUID FK`, `predicate_code FK`, `object_concept_id UUID FK` | 向きが必須。条件付き因果と共起を区別 |
| `INTERVENTION` | 介入の種類 | `intervention_id PK`, name, operation_description | 初期カタログの介入方法 |
| `METHOD_EFFECT` | 手法と概念の効果・検知に関する主張 | `claim_id UUID PK/FK`, `method_id UUID FK`, `concept_id UUID FK`, `predicate_code FK` | 手法カタログの効果候補の正式化先。介入履歴と混同しない |
| `INTERVENTION_EFFECT` | 介入と概念の効果の主張 | `claim_id PK/FK`, `intervention_id FK`, `concept_id UUID FK`, predicate_code FK | 軽減／悪化／検知の別を保持 |
| `METRIC` | 指標概念（系列） | `metric_id PK`, name, unit_family?, description | 初期データのECE等は**系列**、仕様は版管理 |
| `METRIC_LINK` | 概念と指標の評価関係 | `claim_id PK/FK`, `concept_id UUID FK`, `metric_id FK`, predicate_code FK | 評価指標が単独で問題を証明するとは限らない |
| `EVIDENCE` | 根拠の共通レコード | `evidence_id UUID PK`, evidence_kind, status, summary, created_at | 出典先は型付き子テーブル |
| `CLAIM_EVIDENCE` | 主張と根拠の意味付き接続 | `claim_id FK`, `evidence_id FK`, `stance`, notes | UQ `(claim_id,evidence_id)`；支持/反証/限定 |
| `PROBLEM_EVIDENCE` | 個別問題を裏付ける測定 | `problem_id FK`, `evidence_id FK`, role | 一般Claimの根拠と局所観測を区別 |
| `CONCEPT_EVIDENCE` | 概念定義・存在の出典 | `concept_id UUID FK`, `evidence_id FK`, role | 概念自体の根拠。因果を含意しない |

**CLAIMのサブタイプ**：`CLAIM` は上記の `CONCEPT_RELATION` / `METHOD_EFFECT` / `INTERVENTION_EFFECT` / `METRIC_LINK` のちょうど一つに属する。将来の型追加時は共通の排他制約も拡張する。アプリケーション制約または遅延制約トリガで保証する（FKだけでは保証できない）。

## 3. 関係の意味と根拠の状態

| 関係 | 何を表すか | 自動導出の扱い |
|---|---|---|
| `is_a` | 狭義の下位概念 | 明確な語義の下でのみ推移的 |
| `part_of` | 構成要素 | `is_a`として継承しない |
| `related_to` | 関連・共起 | 因果を推論しない |
| `distinct_from` | 概念上の区別 | 反対概念／排他性とは限らない |
| `can_contribute_to` | 条件次第で寄与 | 普遍的含意・推移性を仮定しない |
| `can_cause` | 条件を固定した因果命題 | 介入／交絡／根拠を個別確認 |
| `can_manifest_as` | 観測現象として現れ得る | 逆方向の推論を禁じる |
| `tradeoff_with` | 改善間の競合 | 設定や資源制約が前提 |

初期52件の述語と条件は `../catalog/concept_relations.yaml` に明示する。初期14件のMETHOD→CONCEPT効果・検知候補は `../catalog/method_concept_links.yaml` にあり、正式登録先は `METHOD_EFFECT`。述語ごとの端点許可型は `../catalog/relation_types.yaml` に従う。関係の初期行は**出典つき確定済みの論文主張ではない**。原典と対応できたもののみ `SOURCE_ASSERTION`・`EVIDENCE`・`REVIEW_DECISION` を関連付けて確定する。

## 4. 典型的な記録例

1. `CONCEPT`: Shortcut Learning。UUIDは `../catalog/concepts.yaml` の `concept_id` を参照。
2. `CONCEPT`: OOD汎化困難。UUIDは `../catalog/concepts.yaml` の `concept_id` を参照。
3. `CLAIM`: Shortcut LearningがOOD性能低下へ寄与し得る、ただし学習時の手がかりが運用で成立しない場合。
4. `CONCEPT_RELATION`: subject=Shortcut Learning、predicate=`can_contribute_to`、object=OOD汎化困難。
5. `REQUIREMENT`: 照明変更後の不良Recall≥0.99。`CONTEXT`: 製品群B、カメラA、照明変更条件。
6. `PROBLEM`: 実際の不良Recall=0.94という**架空の観測例**。`PROBLEM_CONCEPT`で関連概念とリンク。
7. `EVIDENCE`: 研究のTable 2、または自社実験結果に対応する根拠。`CLAIM_EVIDENCE.stance`で支持・反証・限定を判断。

一般的なCLAIMの採用は、局所問題の原因確定とは異なる。局所的な適用可能性は `CLAIM_APPLICABILITY`で別途評価する。

## 5. 更新・来歴のルール

- 語義が変わる場合は改名だけにせず、新 `CONCEPT` と後継関係を作成する。
- 初期の20領域は分類ビューであり、17〜20は応用分野の観点も混在する。所属を重ねることができる。
- 文献・実験・根拠が増えても同じ概念を新規作成せず、既存IDへ参照付ける。
- `EVIDENCE`と`CLAIM`は独立：支持と反証が同時に存在しても片方を削除しない。
- `EVIDENCE`へ文献・実験の原典を結びつける型付き子テーブルは `../design/01_architecture_and_data_model.md` と `../experiments/04_experiment_model_reference.md` で定義する。

## 6. 横断整合性

正式な `CLAIM`・`EVIDENCE`・`INTERVENTION`・`METRIC` の主キーはすべてUUID。文献、実験、統合ビューでも同じ型を使用する。確定した `EVIDENCE` は `LITERATURE_EVIDENCE` / `EXPERIMENT_EVIDENCE` のちょうど一方に出典を持つ。詳細は [`../design/06_integrity_and_model_contracts.md`](../design/06_integrity_and_model_contracts.md) を参照。
