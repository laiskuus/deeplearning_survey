# 深層学習の課題概念辞書

この辞書は`catalog/concepts.yaml`の人間向け表示です。**概念の同一性はUUIDで管理**し、研究領域への所属は `concept_topic_assignments.yaml` の参照関係で管理される分類ビューです。

概念の型：`S` 状態、`M` 機構、`F` 失敗現象、`C` 制約、`R` 要求・性質。原因・結果は概念の固定型ではなく、関係の中で扱います。

## 01. 問題定義・学習目標（8概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Objective Misalignment | 目的不整合 | `F` | 学習目的と本来達成したい目的が一致しない |
| Surrogate Loss Gap | 代理損失と評価の乖離 | `F` | 損失関数の改善が実用評価に結び付かない |
| Cost-sensitive Learning | 誤判定コストの非対称性 | `C` | 誤りの種類ごとに損失が異なり一律の最適化が不適切 |
| Multi-objective Conflict | 複数目的の競合 | `C` | 精度・速度・安全性などの同時最適化が困難 |
| Task Ambiguity | タスク・正解の曖昧さ | `S` | 正解や判定基準が文脈・専門家により異なる |
| Specification Incompleteness | 仕様不完全性 | `C` | 望ましい挙動の要求が十分に定義されていない |
| Delayed Feedback | 正解フィードバック遅延 | `C` | 結果や報酬の観測が遅れる |
| Underspecification | 学習パイプラインの過少特定 | `F` | 同等の検証性能でも運用時の振る舞いが大きく異なる予測器が残る |

## 02. データ品質・データ分布（14概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Data Scarcity | データ不足 | `C` | 学習に必要なサンプルが不足する |
| Class Imbalance | クラス不均衡 | `S` | クラスごとのサンプル頻度が偏る |
| Long-tailed Distribution | ロングテール分布 | `S` | 少数クラスが多数あり頻度分布の裾が長い |
| Rare-event Learning | 希少事象の学習困難 | `F` | 出現頻度の低い事象の学習・評価が困難 |
| Coverage Gap | 条件カバレッジ不足 | `C` | 重要な条件・組合せが訓練データにない |
| Sampling Bias | 標本抽出バイアス | `S` | 標本抽出により母集団との分布差が生じる |
| Selection Bias | 選択バイアス | `S` | 収集・観測対象の選択が分布を歪める |
| Measurement Noise | 測定ノイズ | `S` | センサー・入力に雑音が含まれる |
| Missing Data | 欠損データ | `S` | 入力やメタデータの一部が欠落する |
| Data Heterogeneity | データ異質性 | `S` | ソースごとに形式・特徴・品質が異なる |
| Data Duplication | データ重複 | `S` | 同一・類似サンプルが重複して存在する |
| Data Contamination | データ汚染 | `S` | 本来分離されるべき情報などが意図せず混入する |
| Synthetic Data Gap | 合成-実データ差 | `S` | 合成分布と実世界分布に差がある |
| Spurious Correlation | 疑似相関 | `S` | 非本質的な特徴と正解が偶然相関する |

## 03. 教師信号・アノテーション（11概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Label Scarcity | ラベル不足 | `C` | ラベル付きサンプルが十分に得られない |
| Label Noise | ラベルノイズ | `S` | 付与された正解ラベルに誤りがある |
| Annotation Disagreement | アノテータ間不一致 | `S` | 専門家間で判定が一致しない |
| Weak Supervision | 弱教師信号 | `C` | 間接的・不完全な教師情報しかない |
| Partial Label Learning | 部分ラベル | `C` | 複数の候補から正解が確定できていない |
| Incomplete Multi-label | 不完全マルチラベル | `S` | 同時に成立するラベルの一部しか付与されない |
| Positive-Unlabeled Learning | 正例・未ラベル問題 | `C` | 正例と未ラベルデータのみが観測できる |
| Hierarchical Labeling | 階層ラベル構造 | `S` | クラス間に階層・包含関係がある |
| Label Dependency | ラベル間依存 | `S` | 複数ラベルに相関・論理・因果依存がある |
| Annotation Granularity | ラベル粒度の差 | `S` | 画像単位・物体単位・画素単位などの単位が違う |
| Subjective Ground Truth | 主観的な正解 | `S` | 評価者や用途によって正解が異なり得る |

## 04. 表現学習・モデル容量（11概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Insufficient Capacity | モデル容量不足 | `C` | 必要な関数を十分に表現できない |
| Excessive Capacity | 過剰なモデル自由度 | `C` | 不要なパターンも適合できる自由度がある |
| Representation Bias | 表現・帰納バイアス | `S` | アーキテクチャの構造的な選好がタスクに不適切 |
| Feature Entanglement | 潜在因子の混合 | `S` | 分けたい特徴・因子が表現に混ざる |
| Representation Collapse | 表現崩壊 | `F` | 異なる入力の表現が区別しにくくなる |
| Invariance Failure | 不変性の不足 | `F` | 無視すべき変換に予測が影響される |
| Equivariance Failure | 同変性の不足 | `F` | 入力と出力の変換対応が保てない |
| Local–Global Trade-off | 局所と大域の競合 | `C` | 微細特徴と大局的文脈の両立が難しい |
| Resolution Bottleneck | 解像度ボトルネック | `C` | 縮小・集約によって重要な細部情報が失われる |
| Compositional Generalization | 組合せ汎化の不足 | `F` | 既知要素の未知の組合せに対応できない |
| Representation Misalignment | 下流目的と表現の不整合 | `F` | 学習した特徴が下流タスクに適さない |

## 05. 最適化・学習安定性（10概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Optimization Difficulty | 最適化困難 | `F` | 目的関数を十分に低減できない |
| Vanishing / Exploding Gradients | 勾配消失・爆発 | `S` | 勾配の大きさが極端になり更新が阻害される |
| Training Instability | 学習不安定性 | `F` | 損失やパラメータ更新が不安定になる |
| Initialization Sensitivity | 初期値依存性 | `S` | パラメータ初期値で結果が大きく変動する |
| Hyperparameter Sensitivity | ハイパーパラメータ依存性 | `S` | 学習率などの設定差で性能が変わる |
| Gradient Conflict | 勾配競合 | `S` | 異なるタスクの更新方向が衝突する |
| Loss Imbalance | 損失寄与の偏り | `S` | 一部のタスク・サンプルが学習を支配する |
| Numerical Instability | 数値不安定性 | `F` | 低精度演算や丸め誤差により計算が不安定になる |
| Optimization–Generalization Gap | 最適化と汎化の乖離 | `F` | 訓練損失改善が未知データ性能につながらない |
| Run-to-run Variability | 試行間変動 | `S` | 同一条件でも乱数・実装で結果がばらつく |

## 06. 汎化・分布シフト（13概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Overfitting | 過学習 | `F` | 訓練への適合に対して未知データへの汎化が不足する |
| Underfitting | 学習不足 | `F` | 訓練分布上の構造さえ十分に捉えられない |
| Covariate Shift | 共変量シフト | `S` | P(X)が変わりP(Y｜X)が維持される分布変化 |
| Label Shift | ラベルシフト | `S` | P(Y)が変わりP(X｜Y)が維持される分布変化 |
| Concept Shift | 概念シフト | `S` | P(Y｜X)が変化する |
| Domain Generalization | ドメイン汎化困難 | `F` | 未観測ドメインで要求性能を維持できない |
| Domain Adaptation | ドメイン適応困難 | `F` | 対象ドメインへの適切な適応ができない |
| Out-of-Distribution Generalization | 分布外汎化困難 | `F` | 訓練分布外で予測性能が低下する |
| Shortcut Learning | ショートカット学習 | `M` | 本質とは限らない簡単な手がかりでタスクを解く |
| Spurious Feature Reliance | 非本質特徴への依存 | `M` | 分布を越えて安定しない特徴に予測が依存する |
| Few-shot Generalization | 少数例汎化困難 | `F` | 少数の教師例から新概念を扱えない |
| Zero-shot Transfer | ゼロショット転移困難 | `F` | タスクの教師例なしで転用できない |
| Worst-group Performance | 最悪条件群の性能不足 | `F` | 平均性能が良くても特定群で性能が低い |

## 07. 不確実性・未知検知（9概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Aleatoric Uncertainty | 偶然的不確実性 | `S` | 観測ノイズ・本質的曖昧さによる不確実性がある |
| Epistemic Uncertainty | 認識論的不確実性 | `S` | モデルの知識不足に起因する不確実性がある |
| Miscalibration | 確率校正不良 | `F` | 予測確率と実際の正解頻度が対応しない |
| Overconfidence | 過信 | `F` | 誤予測でも高い信頼度を出す |
| OOD Detection | 分布外検知困難 | `F` | 学習分布と異なる入力を識別できない |
| Open-set Recognition | 未知クラス認識困難 | `F` | 未知クラスを既知として処理する |
| Selective Prediction | 予測保留判断の不足 | `F` | 予測しない方が安全な入力を選別できない |
| Distribution-free Coverage | 被覆保証の困難 | `F` | 弱い仮定下で予測集合の被覆率を保ちにくい |
| Risk Estimation | 予測リスク推定の不足 | `F` | 運用下の実際の誤判定リスクを見積もれない |

## 08. 継続学習・環境適応（10概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Data Drift | データドリフト | `S` | 入力分布などのデータ特性が時間で変化する |
| Concept Drift | コンセプトドリフト | `S` | 時間経過で入力と正解の関係が変化する |
| Catastrophic Forgetting | 破滅的忘却 | `F` | 新しい学習により既存タスク性能が失われる |
| Stability–Plasticity Dilemma | 安定性と可塑性のジレンマ | `C` | 既存知識維持と新知識獲得が競合する |
| Online Adaptation | オンライン適応困難 | `F` | 逐次入力に対して安定して適応できない |
| Test-time Adaptation | 推論時適応困難 | `F` | 推論時の未ラベルデータを用いた更新が難しい |
| Negative Transfer | 負の転移 | `F` | 転移・適応で対象性能が低下する |
| Error Accumulation | 誤りの累積 | `M` | 誤った擬似ラベルや予測が後続の学習へ伝播する |
| Feedback Loop | 予測-データのフィードバック | `M` | 予測や介入が将来の観測データに影響する |
| Non-stationary Learning | 非定常学習困難 | `F` | 継続変化する環境下での学習が不安定になる |

## 09. 頑健性・攻撃耐性（9概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Corruption Robustness | 入力劣化への頑健性不足 | `F` | ノイズ・ぼけ・圧縮等で性能が低下する |
| Perturbation Sensitivity | 入力摂動感度 | `S` | 小さな入力変化で予測が大きく変わる |
| Adversarial Examples | 敵対的入力への脆弱性 | `F` | 意図的な入力摂動で誤予測する |
| Data Poisoning | データポイズニングリスク | `R` | 学習データへの悪意ある混入で挙動が変わる |
| Backdoor Attacks | バックドアリスク | `R` | トリガーによって意図しない挙動を誘発される |
| Model Extraction | モデル抽出リスク | `R` | 外部からモデルの機能を複製される |
| Robustness–Accuracy Trade-off | 頑健性と通常精度の競合 | `C` | 頑健性対策と通常性能の両立が難しい場合がある |
| Certified Robustness | 頑健性保証困難 | `F` | 摂動範囲に対する出力の保証が与えにくい |
| Compound Shift | 複合分布シフト | `S` | 複数の環境変化が同時に起こる |

## 10. 評価・再現性（12概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Data Leakage | データリーク | `F` | 学習・評価で利用不能な情報が混入する |
| Benchmark Contamination | ベンチマーク汚染 | `F` | 評価問題が学習情報に含まれる |
| Benchmark Saturation | ベンチマーク飽和 | `C` | 指標が上限に近づき性能差を測れない |
| Metric Misalignment | 評価指標の不整合 | `F` | 評価指標が実務目的を表さない |
| Evaluation Bias | 評価標本バイアス | `S` | テスト集合が評価対象を代表しない |
| Subgroup Blindness | 部分集団の見落とし | `F` | 全体平均によって弱い群が隠れる |
| Statistical Uncertainty | 推定値の統計的不確実性 | `S` | 有限標本による指標の推定誤差がある |
| Reproducibility | 再現可能性不足 | `F` | 同一手順で結果を再現できない |
| Reproducibility of Comparisons | 研究比較の再現性不足 | `F` | 条件・予算・実装の不一致で公平な比較が難しい |
| Benchmark Overfitting | ベンチマークへの過適合 | `F` | 公開評価条件に合わせすぎ一般性能を測れない |
| Real-world Validity | 実環境妥当性不足 | `F` | 評価環境と実運用で性能が一致しない |
| Evaluation Cost | 評価コスト | `C` | 評価に多大な時間・費用・専門判断が必要 |

## 11. 計算効率・スケーリング（13概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Training Compute | 学習計算コスト | `C` | 学習に必要な演算資源が大きい |
| Inference Latency | 推論遅延 | `C` | 意思決定に必要な応答時間を満たせない |
| Memory Footprint | メモリ消費 | `C` | 重み・活性・状態が多量のメモリを要する |
| Memory Bandwidth | メモリ帯域制約 | `C` | 転送速度が処理能力を律速する |
| Communication Bottleneck | 通信ボトルネック | `C` | 分散計算時の通信が性能を律速する |
| Energy Efficiency | エネルギー効率不足 | `F` | 性能当たりのエネルギー消費が大きい |
| Data Efficiency | データ効率不足 | `F` | 十分な性能に多量の訓練例を要する |
| Compute-optimal Scaling | 計算資源配分問題 | `C` | パラメータ・データ・計算予算の最適配分が難しい |
| Quantization Degradation | 量子化による劣化 | `F` | 低ビット化により精度や安定性が低下する |
| Compression Trade-off | 圧縮に伴う競合 | `C` | 軽量化・精度・速度が競合する |
| Hardware Portability | ハードウェア移植性不足 | `F` | 特定演算器への依存で移植が難しい |
| Edge Deployment | エッジ展開困難 | `F` | 端末の電力・メモリ・遅延制約を満たせない |
| Sustainability | 環境負荷 | `R` | 学習・推論の資源利用が環境に影響する |

## 12. 解釈性・因果理解（9概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Black-box Behavior | ブラックボックス性 | `C` | 判断根拠や内部計算が理解しにくい |
| Explanation Faithfulness | 説明忠実性不足 | `F` | 提示する説明が実際の推論を反映しない |
| Explanation Stability | 説明安定性不足 | `F` | 軽微な入力変化で説明が変わる |
| Feature Attribution | 特徴寄与の特定困難 | `F` | 予測に対する各特徴の寄与を特定できない |
| Disentangled Representation | 因子分離の困難 | `F` | 潜在変数が独立した意味を持つ形に分かれない |
| Causal Identification | 因果識別困難 | `F` | 観測から因果効果・構造を特定できない |
| Counterfactual Reasoning | 反事実推論困難 | `F` | 介入条件下の結果を妥当に推定できない |
| Mechanistic Interpretability | 内部機構の解釈困難 | `F` | 計算回路とモデル能力の対応がわからない |
| Actionable Explanation | 実行可能な説明の不足 | `F` | 説明を改善・判断へ接続できない |

## 13. 運用・MLOps（12概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Data / Model Versioning | データ・モデルの版管理不足 | `F` | データとモデルの対応を追跡できない |
| Data Lineage | データ来歴の不透明性 | `F` | 由来・加工・利用経路を追跡できない |
| Training–Serving Skew | 学習・提供時の乖離 | `S` | 前処理や特徴量が学習時と運用時で異なる |
| Model Monitoring | モデル監視不足 | `F` | 劣化・異常な挙動を継続観測できない |
| Label Feedback Delay | 運用ラベルの取得遅延 | `C` | 運用時の正解取得が遅れる |
| Retraining Strategy | 再学習方針の不備 | `F` | いつ・何を・どの条件で再学習するか決めにくい |
| Deployment Validation | 導入前検証不足 | `F` | 実環境下の挙動を事前に確認できない |
| Reproducible Pipeline | 再実行可能なパイプライン不足 | `F` | 学習実行条件・成果物を再構築できない |
| Model Rollback | ロールバック困難 | `F` | 問題発生時に安全なモデルへ戻せない |
| Model / Data Contract | モデル・データ契約不備 | `F` | 入出力定義や品質制約が保たれない |
| Human-in-the-loop | 人間関与の組込み困難 | `F` | 修正・承認・再学習への人の参加が難しい |
| Operational Technical Debt | 運用上の技術的負債 | `C` | データ・コード・モデルの依存が複雑化する |

## 14. 公平性・安全性・倫理（10概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Algorithmic Bias | アルゴリズム的偏り | `S` | 一部の群・条件への系統的な偏りがある |
| Group Fairness | 集団公平性不足 | `F` | 集団別の機会や誤判定率に不公平がある |
| Individual Fairness | 個人公平性不足 | `F` | 類似する個人を不合理に異なる扱いにする |
| Fairness under Shift | シフト下の公平性低下 | `F` | 環境変化で集団間格差が悪化する |
| Harmful Outputs | 有害出力 | `R` | モデル出力が実害を生じ得る |
| Safety Assurance | 安全性保証困難 | `F` | 事故・損害を防ぐ根拠が不十分 |
| Human Oversight | 人間監督不足 | `F` | 異常時の理解・介入・停止が困難 |
| Value / Preference Misalignment | 価値・選好との不整合 | `F` | 出力・行動が人間の目的に合わない |
| Dual-use Risk | デュアルユースのリスク | `R` | 技術が悪用にも用いられる |
| Societal Externalities | 社会的外部性 | `R` | 社会・労働・情報環境へ波及する |

## 15. プライバシー・ガバナンス（11概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Membership Inference | 学習参加の推定リスク | `R` | あるデータが訓練に含まれたか推定される |
| Model Inversion | モデル反転リスク | `R` | 学習情報や入力の一部を復元される |
| Training Data Extraction | 学習データ抽出リスク | `R` | 記憶された訓練データが出力される |
| Federated Learning Security | 連合学習の安全性 | `R` | 更新情報から漏えい・不正更新が起きる |
| Privacy–Utility Trade-off | プライバシーと有用性の競合 | `C` | 保護措置がモデル有用性と競合する場合がある |
| Machine Unlearning | 機械的忘却の困難 | `F` | 指定データの学習影響を除去しにくい |
| Data Provenance | データ来歴・出自不足 | `F` | 出自・権利・利用条件を追跡できない |
| Copyright / Licensing | 著作権・ライセンス課題 | `C` | 学習・生成・再配布の権利処理が難しい |
| Accountability | 説明責任の不明確さ | `C` | 結果に対する責任主体・手順が曖昧 |
| Auditability | 監査可能性不足 | `F` | モデルの変更・判断を監査できない |
| Regulatory Compliance | 規制適合困難 | `F` | 法令・業界要件と設計を整合できない |

## 16. 理論的理解・保証（10概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Generalization Theory | 汎化理論の未解明点 | `F` | なぜ未知データに汎化できるか十分に説明できない |
| Double Descent | ダブルディセント | `S` | 容量と誤差の関係が非単調になる現象 |
| Implicit Bias | 最適化の暗黙バイアス | `M` | 最適化器が特定種の解を選好する |
| Feature Learning Dynamics | 特徴形成の動態 | `M` | 学習中の内部特徴の形成・変化のメカニズム |
| Scaling Law Validity | スケーリング則の適用限界 | `C` | 性能外挿が状況・規模で破綻し得る |
| Identifiability | 識別可能性の限界 | `C` | 観測から潜在構造が一意に定まらない |
| Formal Verification | 形式的検証困難 | `F` | 複雑なモデルの性質を数学的に証明しにくい |
| Certified Guarantees | 保証付与の困難 | `F` | 安全性・誤差などに適用条件付き保証しか与えにくい |
| Fundamental Limits | 本質的な達成限界 | `C` | 情報量・データ・計算などの限界がある |
| Emergent Behavior | 能力の非連続的出現・見かけ | `S` | 規模の変化で能力が突如現れるように見える場合がある |

## 17. 生成AI・基盤モデル（12概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Hallucination | 幻覚・非根拠生成 | `F` | 事実や入力に基づかない内容を生成する |
| Factual Grounding | 事実根拠への接続不足 | `F` | 生成結果の根拠が資料・事実に結び付かない |
| Knowledge Staleness | 知識の陳腐化 | `S` | 学習後に更新された情報を持たない |
| Long-context Degradation | 長文脈性能低下 | `F` | 入力が長いと必要な情報を活用できない |
| Memorization | 訓練例の記憶・再現 | `M` | 訓練内容を不必要に再生できる状態になる |
| Generation Diversity | 生成多様性不足 | `F` | 出力が似通い多様な候補を得られない |
| Controllability | 生成制御困難 | `F` | 指定条件・形式・制約を守れない |
| Temporal Consistency | 生成の時間的一貫性不足 | `F` | 連続画像・音声・動画の連続性が崩れる |
| Reasoning Reliability | 推論の信頼性不足 | `F` | 論理・数値・計画タスクが安定しない |
| Alignment Failure | 整合性の失敗 | `F` | モデルの振る舞いが意図する目標に適合しない |
| Reward Hacking | 報酬ハッキング | `M` | 評価や報酬の抜け道を利用する |
| Knowledge Editing | 知識編集の困難 | `F` | 特定知識の変更が周辺知識に悪影響を与える |

## 18. マルチモーダル学習（9概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Cross-modal Alignment | モダリティ間対応の不足 | `F` | 画像・音声・文字などの表現を対応させられない |
| Modality Imbalance | モダリティ寄与の偏り | `S` | 特定の入力種に過度に依存する |
| Missing Modality | モダリティ欠損 | `S` | 利用可能な入力種が一部欠ける |
| Fusion Strategy | モダリティ融合の困難 | `F` | 統合のタイミング・方式を決められない |
| Cross-modal Grounding | モダリティ間根拠の不足 | `F` | 言語と視覚・音声内の対象が結び付かない |
| Spatial Reasoning | 空間推論困難 | `F` | 位置・距離・幾何関係を正しく扱えない |
| Temporal Synchronization | 時間同期困難 | `F` | 動画・音声などの時刻対応が崩れる |
| Cross-modal Contradiction | モダリティ間矛盾 | `S` | 異種入力間で相反する情報が存在する |
| Modality-specific Robustness | 特定モダリティ劣化への弱さ | `F` | 一部入力の劣化が全体性能を下げる |

## 19. 強化学習・エージェント（12概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Exploration–Exploitation | 探索と活用の競合 | `C` | 探索行動と既知の高報酬行動のバランスが難しい |
| Sample Inefficiency | 試行効率不足 | `F` | 大量の相互作用が必要 |
| Sparse Rewards | 疎な報酬 | `S` | 学習を導く報酬の観測が少ない |
| Reward Misspecification | 報酬仕様不備 | `C` | 報酬定義と本来目標が一致しない |
| Partial Observability | 部分観測 | `S` | 環境の全状態を観測できない |
| Long-horizon Planning | 長期計画困難 | `F` | 長期にわたる計画・実行が不安定 |
| Credit Assignment | 寄与割当困難 | `F` | どの行動が結果に貢献したか特定しにくい |
| Sim-to-real Gap | シミュレーションと現実の差 | `S` | シミュレータと現実の力学・観測に差がある |
| Safe Exploration | 安全な探索の困難 | `F` | 危険行動を避けつつ学習できない |
| Tool-use Reliability | ツール利用の信頼性不足 | `F` | 選択・呼出・引数・結果解釈が失敗する |
| Agent Security | エージェントの安全保障リスク | `R` | ツールや外部入力から権限逸脱が起きる |
| Multi-agent Coordination | 複数主体の協調困難 | `F` | 複数エージェントの協調・競争が難しい |

## 20. 科学AI・物理世界（10概念）

| 概念（English） | 日本語 | 型 | 定義 |
|---|---|:---:|---|
| Physical Consistency | 物理整合性の欠如 | `F` | 予測が支配方程式・幾何拘束などと矛盾する |
| Conservation Laws | 保存則違反 | `F` | エネルギー・質量などの保存が守られない |
| Extrapolation | 外挿困難 | `F` | 観測範囲外の条件で推定性能が低下する |
| Sparse Observation | 観測の疎性 | `C` | 利用可能な観測点・観測頻度が少ない |
| Inverse Problem Ill-posedness | 逆問題の不適切性 | `C` | 解の一意性・安定性・存在が保証されない |
| Multi-scale Modeling | マルチスケールモデル化困難 | `F` | 複数の空間・時間スケールを同時に扱えない |
| Numerical Stability | 予測計算の数値不安定性 | `F` | 長時間積分などで誤差が増幅する |
| Sim-to-real Validation | 実環境への移行検証困難 | `F` | シミュレーションから実機性能を検証しにくい |
| Scientific Plausibility | 科学的妥当性の欠如 | `F` | もっともらしくても科学的に誤った予測をする |
| Experimental Validation | 実験検証の負担 | `C` | 検証実験に多大な費用・時間が必要 |

## 補助的な総称概念

| 概念名 | 定義 |
|---|---|
| 分布シフト（総称）（Distribution Shift） | P_train(X,Y) と P_target(X,Y) など関心のある分布が異なること |
| 時間方向の分布変化（総称）（Temporal Distribution Change） | 時刻tごとに確率分布などの性質が変化すること |

## 識別と知識管理

- 主キーは`concept_id`（UUID）。全文の一覧と厳密なIDは`concepts.yaml`を参照。
- トピックへの所属は`CONCEPT_TOPIC_ASSIGNMENT`で管理する。名称や所属が変わっても同じ概念ならIDは変更しない。
- `record_status=unreviewed_seed`は、個々の原典に対する承認をまだ行っていない初期候補を意味する。
- 研究文献の根拠が確認できるまでは、概念と概念間の関係を確定した因果事実として扱わない。
