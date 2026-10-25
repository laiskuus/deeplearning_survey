# 初期概念・手法・評価指標カタログ

## 構成

| データ | 件数 | 用途 |
|---|---:|---|
| `topics.yaml` | 20 | 研究領域の分類ビュー |
| `concepts.yaml` | 217 | 主概念215件と補助概念2件のUUID・定義・意味型 |
| `topic_area_versions.yaml` | 20 | 分類領域の初期版（安定IDと版IDを分離） |
| `concept_topic_assignments.yaml` | 215 | 主概念の初期分類所属（正式なM:N所属） |
| `concept_relations.yaml` | 52 | 条件付きの概念間関係（未個別検証の候補） |
| `relation_types.yaml` | 語彙一式 | 関係述語と推論時の注意 |
| `methods.yaml` | 12 | 介入・手法の基本カテゴリ |
| `method_concept_links.yaml` | 14 | `METHOD_EFFECT` 用の未承認候補（METHOD→CONCEPT） |
| `metrics.yaml` | 12 | 評価指標系列 |
| `concept_metric_links.yaml` | 12 | 概念と評価指標の対応 |

`concept_dictionary.md`と`relation_method_metric_dictionary.md`は上記YAMLの人間向け一覧です。

## 識別子と参照規則

- `concept_id`、`relation_id`、`method_id`、`metric_id`には分類に依存しない**UUID**を使用する。
- 関係の主体・客体、施策・指標の対応先はUUIDのFKとして保持し、名称・表示順・分類コードには依存させない。
- `concepts.yaml` には所属領域の列を持たせない。分類は `concept_topic_assignments.yaml` → `topic_area_versions.yaml` → `topics.yaml` から導出する。
- 分類別件数は `CONCEPT_TOPIC_ASSIGNMENT` から算出する派生情報であり、マスタに重複保存しない。
- `record_status=unreviewed_seed`の概念や`review_status=curated_initial_candidate`の関係は、十分な根拠に基づく確定済み知識ではない。必ず出典とレビュー結果を確認する。
- `RELATION_TYPE` の `subject_types/object_types` でリンクの両端型を検証する。手法（METHOD）と介入（INTERVENTION）を同一視しない。
- `METRIC`は指標系列であり、指標の計算式・単位・改善方向は`METRIC_SPEC_VERSION`で確定する。

## 初期データ登録の順序

`TOPIC_AREA` → `TOPIC_AREA_VERSION` → `CONCEPT` / `METHOD` / `METRIC` → `CONCEPT_TOPIC_ASSIGNMENT` → 関係の抽出候補／レビュー → 承認された `CLAIM` および型付き関係。

`concept_relations.yaml`の候補行を承認なしに`CLAIM`へ確定登録しない。
