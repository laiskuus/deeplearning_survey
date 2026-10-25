# 深層学習の研究知識・実装・実験分析プラットフォーム

**用途：新規構築のための論理データモデル、初期概念カタログ、研究・実験のユースケース／契約仕様。**

> **配置方針**：この`Docs/`が配布物のルートです。全ての設計書・初期カタログ・ER図・サンプル・検証スクリプトをこのフォルダ内に収録しています。
> 設計書は役割別に`design/`・`ontology/`・`experiments/`・`contracts/`・`references/`へ分類しています。

## システムの目標

論文探索 → 主張・実験結果の構造化 → 課題・手法・根拠の統合 → 実装 → 実験・比較 → 新たな根拠として知識へフィードバックする。実運用の問題診断も同じ研究サイクルに接続する。

## 確定した方針

1. 概念・文献・手法の対象は深層学習全般。
2. 論文は文献版・原文断片・個別主張・実験・比較群・測定結果・適用条件まで分解する。
3. LLMによる抽出・マッピングは候補まで自動化し、確定知識は人の承認によって更新する。
4. GPUジョブの実行は承認された計画・コード・入力・予算と一致する場合に限る。

## 内容

| ファイル | 説明 |
|---|---|
| [design/01_architecture_and_data_model.md](design/01_architecture_and_data_model.md) | 研究サイクル全体、論理モデル、責務分離、不変条件 |
| [contracts/02_api_contracts_and_tests.md](contracts/02_api_contracts_and_tests.md) | APIの操作契約、制約、受入テスト |
| [ontology/03_core_ontology_reference.md](ontology/03_core_ontology_reference.md) | 概念／課題／主張／根拠／関係のテーブル定義 |
| [experiments/04_experiment_model_reference.md](experiments/04_experiment_model_reference.md) | 研究計画、データ、学習Run、評価、比較、分析 |
| [references/05_sources_and_validation.md](references/05_sources_and_validation.md) | 参考研究と検証範囲 |
| [design/06_integrity_and_model_contracts.md](design/06_integrity_and_model_contracts.md) | 全ビュー共通の型、出典・比較・承認の横断制約 |
| [catalog/README.md](catalog/README.md) | 初期データの構造・登録方法 |
| [catalog/concept_dictionary.md](catalog/concept_dictionary.md) | 全概念の人間向け辞書 |
| [catalog/relation_method_metric_dictionary.md](catalog/relation_method_metric_dictionary.md) | 関係・手法・指標の人間向け辞書 |
| [diagrams/knowledge_research_er.puml](diagrams/knowledge_research_er.puml) | 10図のPlantUML ER |
| [examples/example_paper_5_experiments.yaml](examples/example_paper_5_experiments.yaml) | 複数実験を分けて登録する架空例 |
| [checks/validate_package.py](checks/validate_package.py) | カタログFK・型付き述語・ER共通列型・リンク・ハッシュを検証 |
| [checks/test_validation.py](checks/test_validation.py) | 正常系と破損データを用いた9件の静的回帰テスト |

## 基本の識別・知識モデル

- `CONCEPT`：215の主概念と2つの補助概念。一次概念のIDはUUIDで不変。
- `TOPIC_AREA`：概念の分類ビュー。所属が変わっても概念IDは変わらない。
- `PROBLEM`：特定条件の要求と現実のギャップ。
- `CLAIM`：概念・手法・介入・指標などの間にある、検証可能な型付き関係の主張。
- `SOURCE_ASSERTION`：論文の著者が記述した個別主張。
- `PAPER_RESULT`と`METRIC_RESULT`：論文の報告値と内製実験の測定値を区別。
- `EVIDENCE`：出典を持つ測定・記述・分析と、その支持・反証・限定の位置付け。

## 読み進める順番

`ontology/03_core_ontology_reference.md` → `catalog` → `design/01_architecture_and_data_model.md` → `design/06_integrity_and_model_contracts.md` → `experiments/04_experiment_model_reference.md` → `contracts/02_api_contracts_and_tests.md` → `diagrams` → `examples`。

## 設計資料の限界

論理設計と初期データを収録しています。DBスキーマの実行可能なDDL、API実装、GPUジョブ、承認UI、論文の全文解析処理は含みません。初期概念と関係の学術的な正しさ・網羅性は個別に検証が必要です。

## 設計資料の検証方法

```bash
python checks/validate_package.py
cd checks && python -m unittest -v test_validation
```

カタログの分類所属は `concept_topic_assignments.yaml` だけで管理する。`CLAIM/EVIDENCE` の出典・承認、実験の比較可能性、GPU実行要求の固定条件は `design/06_integrity_and_model_contracts.md` を参照する。静的検証はDB制約の実動作やPlantUMLレンダラーの動作を保証しない。
