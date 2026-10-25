# API契約・データ制約・受入テスト

新規構築を前提としたドメイン操作と検証仕様。研究データ・実験・承認・知識の更新履歴を業務ドメインとして管理します。

## 1. DB制約とトランザクション境界

- `concept_id` はUUID主キーで、分類への所属は `CONCEPT_TOPIC_ASSIGNMENT` のみで管理する。
- `CLAIM`, `EVIDENCE`, `INTERVENTION`, `METRIC` のIDは全ビューでUUID型に統一する。
- 承認後の文献主張・結果の出典断片は、参照中の文書版と同じ版でなければならない。
- `LITERATURE_EVIDENCE` は文献主張・論文測定・論文比較の**いずれか1つだけ**を参照する。PostgreSQLでは `CHECK (num_nonnulls(assertion_id, paper_result_id, paper_comparison_id) = 1)` を設定する。
- `SYNTHESIS_INPUT` は `(synthesis_revision_id, evidence_id)` を一意にする。
- `PAPER_RESULT` は `result_status=ok` の場合のみ数値必須とし、欠測値を0として扱わない。
- `PAPER_COMPARISON` の両群は同じ `PAPER_EXPERIMENT`に属する。
- `RUN_METHOD_USAGE` は対応する `METHOD_IMPLEMENTATION` の組合せと実装確認状態を検証する。
- `KNOWLEDGE_PROPOSAL` と `REVIEW_DECISION` の対象内容ハッシュを照合し、承認済みの値だけを確定知識へ反映する。
- ジョブ投入は要求に固定した計画・入力・コード・設定・予算の `request_hash` と承認の `request_hash` を照合してから行う。有効期限、権限、予算上限、冪等性も必須。
- 同じデータに依存する複数研究を独立した実験として多重計上しない。

## 2. API／ドメインコマンドの契約案

| Command / Query | 入力 | 結果／不変条件 |
|---|---|---|
| `IngestPublication` | DOI/arXiv ID/URL、権利情報 | `PUBLICATION`, `DOCUMENT_VERSION`；重複候補があれば自動統合を保留 |
| `ExtractPaperKnowledge` | document_version_id、抽出モデル・スキーマ版 | 未承認の`EXTRACTION_CANDIDATE`（主張・個別実験・結果候補）と原文アンカー |
| `SubmitKnowledgeProposal` | 候補の正規化差分、出典、hash | `KNOWLEDGE_PROPOSAL`。承認済み知識への変更なし |
| `ReviewKnowledgeProposal` | proposal_id、decision、reviewer_id、hash | 承認があれば単一トランザクションで確定データ・監査イベントを作成 |
| `RegisterMethodImplementation` | method_version_id、git/tree/container、差分 | 手法とコードの版対応。変更点の有無を明示 |
| `CreateExperimentProposal` | research_question/gap/hypothesis、比較設計 | 理由、実行コスト、期待情報量が紐付く提案 |
| `ApproveExecution` | execution_request_id、予算、承認者 | 有効期限付き承認。計画内容とハッシュにバインド |
| `DispatchApprovedExecution` | request_id、コード/入力digest | 承認条件を満たした場合だけ実行基盤に投入 |
| `RecordExperimentEvaluation` | run_id、model_version、split、metric_spec | 本版 `EVALUATION`→`METRIC_RESULT`。再測定は新レコード |
| `ReviewEvidenceSynthesis` | synthesis_revision_id、含めるevidence一覧、判定 | 承認済み統合判断の新しい固定版 |
| `FindEvidenceForProblem` | problem_id、任意のscope_profile | 条件一致を検査し、支持・反証・不明の出典と共に返す |
| `FindResearchGaps` | topic/scope/period | 調査未了・結果が食い違う条件・未検証仮説を返す |


## 3. 機械可読な関係と検索時の誤推論の防止

| 誤った振る舞い | 必要な制御 |
|---|---|
| 「AがBを生じ得る」「BがCを生じ得る」→「AがCを起こす」 | 因果関係は条件付き・原則非推移。関係到達を仮説候補として扱う |
| 「同じ名前の指標」→ 同一評価とみなす | `METRIC_SPEC_VERSION`とプロトコル差を比較し、欠落は比較不能にする |
| 「論文Aが支持、論文Bが反証」→ 論文同士が矛盾すると断定 | 適用条件、被験データ、母集団、手法、アウトカムを比較する |
| 「自社実験で性能改善」→ 因果機序を断定 | 無作為化／統制／交絡の有無をメタデータで記録する |
| 「分類を変えた」→ 別の一次概念IDを作る | 意味的同一性を保ち、`CONCEPT_TOPIC_ASSIGNMENT`のみ更新する |
| 「LLMがExtracted」→ 正本でAccepted | extract→review→approve→apply を強制する |
| 「承認済みPlan」→ 別コミットでも実行可能 | `input_hash`, `config_hash`, `git_commit`, `container_digest`と承認を照合する |
| 「検証不能」→ 効果なし | `inconclusive`, `not_reported`, `undefined`, `no_meaningful_effect`を区別する |


## 4. 受入テスト（Given / When / Then）

**T01: 概念IDの不変性**：ある概念の所属領域を変更しても `concept_id` は変わらず、既存の関係は同じUUIDを参照し続ける。

**T02: 論文5実験の粒度**：一論文から5つのPAPER_EXPERIMENTを登録。3比較で正の差、1比較で実質ゼロ、1比較で負の差とすると、5件の比較が個別に検索でき、論文全体を「成功」1件に潰さない。

**T03: 出典の整合性**：PAPER_RESULTの原典Table 2の位置を取得できる。出典位置不明の場合は承認不可。

**T04: 承認前の隔離**：候補は`EXTRACTION_CANDIDATE`／`KNOWLEDGE_PROPOSAL`だけに存在し、未承認のCLAIM／SOURCE_ASSERTION／PAPER_RESULTを正式検索で返さない。レビュアは候補を確認できる。

**T05: 同じ研究の重複計上**：共通評価セットに基づく3報告を統合するとき、independence_groupが同じなら独立な3研究として数えない。

**T06: 比較不能の検出**：原論文のECEのbin数が不明で、内製ECEが15binのとき、効果量の直接比較は`unknown_comparability`で留保する。

**T07: 再現試行の説明**：原論文と結果が異なる再現試行で、モデルコード・データ分割・閾値の差異を記録し、即座に「論文誤り」と判定しない。

**T08: 未知条件の扱い**：条件 `shift_type=lighting` が未報告のEVIDENCEは、照明変化に対する効果の証拠として自動採用しない。

**T09: 実行承認**：承認後にコードのハッシュが変更されるとジョブ投入が失敗し、新しい承認が必要になる。

**T10: 実験→根拠**：同じComparisonから生成したEvidenceが、特定Claimへの限定的な支持に紐付き、別のPROBLEMでの成立は自動保証されない。

**T11: 欠測の扱い**：paper_result数値が未掲載の場合は`result_status=not_reported`、value=NULL。0として集計しない。

**T12: 矛盾の状態**：相反するCLAIMが条件差で説明されたら`context_explained`になり、双方の元のCLAIMを削除しない。


## 5. 検索性能・スケールの留意点

- `SOURCE_ASSERTION(document_version_id)`, `PAPER_RESULT(paper_arm_id)`, `CLAIM_EVIDENCE(claim_id)`, `EXPERIMENT_RUN(external_tracking_key)` を検索しやすくする。
- 文献の全文検索はRDBのtsvectorや別索引を使うが、検索結果は必ず`DOCUMENT_VERSION`と`SOURCE_EXCERPT`の版へ戻す。
- Graph投影は条件と根拠をエッジ／再ificationノードに残す。直接 `CONCEPT → CONCEPT` の単純な辺に縮約した場合は確信度・成立条件が失われるため、本番診断にそのまま用いない。
- 将来的に削除要請や版差替えがある場合、監査と原文の権利処理を両立するポリシーが必要。


## 6. スコープ外／要決定事項

本合意で決定していない詳細は、(a)チームの承認権限とレビュー人数、(b)論文PDF／原文断片の保持ポリシー、(c)研究効果量の共通尺度と統計基準、(d)機密の製造データへのアクセス制御、(e)MLflow／ストレージの正本同期失敗時の再試行、とする。データモデルはこれらを後付け可能な境界で設計した。

## 追加受入条件：横断整合性

- **AT13**：ER図のどの投影でも共通IDの型が一致する。不一致があれば静的検査を失敗させる。
- **AT14**：分類所属は概念マスタに重複保持せず、215件の初期主概念すべてが実在する分類版を参照する。
- **AT15**：承認済み主張／文献評価値が他版の `SOURCE_EXCERPT` を参照した場合、正式登録を拒否する。
- **AT16**：未承認候補から正式 `SOURCE_ASSERTION` / `PAPER_RESULT` を登録しようとした場合に拒否する。
- **AT17**：baseline/candidateのmetric仕様・slice・評価母集団が対応しない比較値を自動生成しない。
- **AT18**：承認済み実行要求のコード・入力・設定・計画・予算のうち1つでも変化した場合、Dispatchを拒否する。
- **AT19**：正式な `EVIDENCE` の出典は文献由来か実験由来のちょうど一方。空欄・二重参照は拒否する。
- **AT20**：チェックサム一覧に載っていないファイル、更新されたファイル、削除されたファイルをパッケージ検証で検知する。
