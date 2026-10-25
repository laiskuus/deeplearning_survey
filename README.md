# 深層学習研究プラットフォーム設計資料 (deep_learning_research_platform_Docs_2026)

深層学習の研究知識・実装・実験分析プラットフォームを新規構築するための**設計資料と初期データカタログ**をまとめたリポジトリです。

実装コードではなく、論理データモデル・オントロジー・API 契約・初期概念カタログ・ER 図・サンプル・静的検証スクリプトを収録しています。

## 概要

論文探索 → 主張・実験結果の構造化 → 課題・手法・根拠の統合 → 実装 → 実験・比較 → 新たな根拠として知識へフィードバックする研究サイクルを支える仕組みを設計しています。

## 主な内容

| ディレクトリ | 内容 |
|---|---|
| [`docs/design/`](docs/design/) | アーキテクチャ・論理データモデル・整合性/モデル契約 |
| [`docs/ontology/`](docs/ontology/) | 概念・課題・主張・根拠・関係のテーブル定義 |
| [`docs/experiments/`](docs/experiments/) | 研究計画・データ・学習 Run・評価・比較 |
| [`docs/contracts/`](docs/contracts/) | API の操作契約・制約・受入テスト |
| [`docs/references/`](docs/references/) | 参考研究と検証範囲 |
| [`docs/catalog/`](docs/catalog/) | 初期概念・手法・指標・関係のデータカタログ |
| [`docs/diagrams/`](docs/diagrams/) | PlantUML による ER 図 |
| [`docs/examples/`](docs/examples/) | 複数実験を分けて登録する架空例 |
| [`docs/checks/`](docs/checks/) | カタログ FK・型付き述語・共通列型・ハッシュの静的検証スクリプト |

詳細な全体説明と読み進める順番は [`docs/README.md`](docs/README.md) を参照してください。

## 検証方法

```bash
python docs/checks/validate_package.py
cd docs/checks && python -m unittest -v test_validation
```

## 注意点

論理設計と初期データの収録が目的であり、実行可能な DB スキーマ（DDL）、API 実装、GPU ジョブ実行、承認 UI、論文全文解析処理は含まれていません。初期概念や関係の学術的な正しさ・網羅性は個別に検証が必要です。

## ライセンス

TBD
