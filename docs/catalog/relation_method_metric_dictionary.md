# 概念間リレーション・手法・評価指標辞書

**関係の成立条件と根拠の状態を必ず区別**します。以下の関係は初期候補であり、論文単位のエビデンスを個別に確認したものではありません。

## 関係型

| 述語 | 主体→客体 | 意味 | 推論上の注意 |
|---|---|---|---|
| `is_a` | CONCEPT → CONCEPT | AはBの下位概念 | 原則として推移的。`is_a`だけを階層化する。 |
| `part_of` | CONCEPT → CONCEPT | AはBの構成要素である | is_aとは別の関係。通常は性質の継承を自動推論しない。 |
| `related_to` | CONCEPT → CONCEPT | 研究上の関連がある | 因果性や方向を含まない。 |
| `distinct_from` | CONCEPT → CONCEPT | 混同すべきでない概念 | 共通点を否定するものではない。 |
| `can_contribute_to` | CONCEPT → CONCEPT | AがBを生じさせる要因になり得る | 条件付き。必然・十分条件を含意しない。 |
| `can_cause` | CONCEPT → CONCEPT | 文脈を固定した因果的主張 | 介入・反事実などの根拠が望ましい。 |
| `can_enable` | CONCEPT → CONCEPT | AがBの発生可能性を高める土壌を作る | 発生自体は保証しない。 |
| `can_manifest_as` | CONCEPT → CONCEPT | AがBという観測現象として現れ得る | 原因の一意性を意味しない。 |
| `can_hide` | CONCEPT → CONCEPT | AがBの発見を妨げる | 観測上の関係。Bの発生原因とは異なる。 |
| `can_hinder` | CONCEPT → CONCEPT | AがBの遂行・改善を妨げる | 直接の性能劣化と区別。 |
| `can_invalidate` | CONCEPT → CONCEPT | AがBの評価や妥当性を損なう | 対象指標・検証設計を明記。 |
| `frames` | CONCEPT → CONCEPT | AがBの解釈枠・競合構造となる | 因果性を含まない。 |
| `tradeoff_with` | CONCEPT → CONCEPT | AとBの改善が競合し得る | 設定依存であり普遍的対立ではない。 |
| `may_mitigate` | METHOD/INTERVENTION → CONCEPT | 手法が条件付きで課題を軽減する可能性がある | METHOD → CONCEPT の候補。改善保証ではなく、成立条件と実験根拠が必要。 |
| `may_exacerbate` | METHOD/INTERVENTION → CONCEPT | 手法が条件付きで課題を悪化させる可能性がある | METHOD → CONCEPT の候補。副作用・トレードオフの可能性を示す。 |
| `evaluated_with` | CONCEPT → METRIC | 課題・概念を所定の評価指標で測定する | CONCEPT → METRIC。指標だけで原因や現象を一意に特定できるわけではない。 |
| `helps_detect` | METHOD → CONCEPT | 手法が課題・異常の検知に役立つ可能性がある | METHOD → CONCEPT。対処する効果と検知する機能を区別する。 |

## 概念間の52関係

| 主体 | 関係 | 客体 | 成立条件 | 注記 |
|---|---|---|---|---|
| Data Scarcity | `can_contribute_to` | Overfitting | 十分なモデル自由度・訓練データへの強い適合がある場合 | 条件付き：データ不足だけで過学習が必然となるわけではない |
| Coverage Gap | `can_contribute_to` | Domain Generalization | 重要な撮影条件が訓練集合から欠落 | 条件付き：学習時の条件カバレッジが未知ドメイン評価へ影響 |
| Spurious Correlation | `can_enable` | Shortcut Learning | 訓練分布中で非本質特徴がラベルを予測できる | 一般的傾向：疑似相関がショートカットになり得る |
| Shortcut Learning | `can_cause` | Spurious Feature Reliance | 学習された予測則が非本質特徴を利用 | 条件付き：Shortcut Learningは過度な非本質特徴依存を形成し得る |
| Spurious Feature Reliance | `can_contribute_to` | Out-of-Distribution Generalization | 非本質特徴の相関が運用時に消失 | 条件付き：OOD性能低下をもたらす一経路 |
| Shortcut Learning | `can_contribute_to` | Out-of-Distribution Generalization | 学習時のショートカットが運用環境で成立しない | 条件付き：常にOODで失敗するわけではない |
| Class Imbalance | `can_contribute_to` | Worst-group Performance | クラス別の重み調整や評価設計がない | 条件付き：平均性能は良好でも少数クラスの性能が劣り得る |
| Label Noise | `can_contribute_to` | Overfitting | 誤ラベルにネットワークが適合 | 条件付き：誤ラベルの学習が汎化を劣化させ得る |
| Label Noise | `can_contribute_to` | Miscalibration | 誤ラベルによる確率学習の偏り | 条件付き：影響の方向や大きさはノイズ機構による |
| Insufficient Capacity | `can_contribute_to` | Underfitting | 表現不足が主要なボトルネック | 条件付き：容量不足と学習不足は同一概念ではない |
| Vanishing / Exploding Gradients | `can_contribute_to` | Training Instability | 勾配問題への対策が不十分 | 一般的傾向：勾配消失/爆発は不安定化要因 |
| Gradient Conflict | `can_contribute_to` | Training Instability | マルチタスクの重み・勾配調整が不十分 | 条件付き：勾配衝突の影響はタスク構成依存 |
| Overfitting | `can_manifest_as` | Out-of-Distribution Generalization | テストが訓練範囲外で実施される場合 | 条件付き：過学習とOOD汎化困難は同義でない |
| Covariate Shift | `is_a` | 分布シフト（総称）（Distribution Shift） | 分布シフトの類型 | 定義/論理：P(Y/X)不変という追加条件あり |
| Label Shift | `is_a` | 分布シフト（総称）（Distribution Shift） | 分布シフトの類型 | 定義/論理：P(X/Y)不変という追加条件あり |
| Concept Shift | `is_a` | 分布シフト（総称）（Distribution Shift） | 分布シフトの類型 | 定義/論理：P(Y/X)が変化 |
| Data Drift | `is_a` | 時間方向の分布変化（総称）（Temporal Distribution Change） | 時間変化として観測 | 定義/論理：対象とする変数・統計量を必ず指定する |
| Concept Drift | `is_a` | 時間方向の分布変化（総称）（Temporal Distribution Change） | 時間変化として観測 | 定義/論理：P_t(Y/X)の変化を想定 |
| Data Drift | `related_to` | 分布シフト（総称）（Distribution Shift） | 時間をまたぐ入力等の分布変化 | 定義/論理：Data DriftとDistribution Shiftは時間軸の指定が異なる |
| Concept Drift | `related_to` | Concept Shift | 時間軸を明示したときの概念変化 | 定義/論理：静的ドメイン間と時間経過の区別 |
| Stability–Plasticity Dilemma | `frames` | Catastrophic Forgetting | 逐次学習で古い知識と新しい知識が競合 | 一般的傾向：ジレンマは忘却そのものではない |
| Error Accumulation | `can_contribute_to` | Negative Transfer | 誤った擬似ラベルを反復利用 | 条件付き：自己学習に起因する負の転移の一経路 |
| Feedback Loop | `can_contribute_to` | Data Drift | 出力を用いて次回のデータが収集される | 条件付き：データ分布がモデルによって内生的に変わる |
| Miscalibration | `can_manifest_as` | Overconfidence | 誤答サンプルに高信頼度を付与 | 条件付き：過信はミスキャリブレーションの一形態になり得る |
| OOD Detection | `related_to` | Open-set Recognition | 未知分布と未知クラスの境界が重なる場合 | 一般的傾向：OODとOpen-setは等価ではない |
| Aleatoric Uncertainty | `distinct_from` | Epistemic Uncertainty | 不確実性の由来 | 定義/論理：AleatoricとEpistemicは概念的に区別する |
| Compound Shift | `can_contribute_to` | Out-of-Distribution Generalization | 同時発生する分布変化が表現に影響 | 条件付き：単一シフトより複雑になり得る |
| Data Leakage | `can_invalidate` | Real-world Validity | 学習と評価データの独立性が壊れる場合 | 条件付き：観測性能が実環境妥当性を保証しなくなる |
| Benchmark Contamination | `is_a` | Data Leakage | 評価問題が訓練情報へ混入 | 定義/論理：評価情報リークの特定ケース |
| Subgroup Blindness | `can_hide` | Worst-group Performance | 平均値しか報告しないとき | 一般的傾向：サブグループ別の評価が必要 |
| Benchmark Overfitting | `related_to` | Benchmark Contamination | 公開ベンチマークへ最適化 | 一般的傾向：汚染と過適合は別概念 |
| Training–Serving Skew | `can_contribute_to` | Out-of-Distribution Generalization | 学習・提供間で入力統計や前処理が異なる | 条件付き：一般的な分布シフト要因のひとつ |
| Model Monitoring | `can_hide` | Data Drift | 監視対象・粒度が不足 | 条件付き：監視欠如はシフトそのものの原因ではない |
| Label Feedback Delay | `can_hinder` | Retraining Strategy | 再学習の妥当性判断に教師信号が必要 | 一般的傾向：ラベル取得遅延による意思決定遅延 |
| Data / Model Versioning | `can_hinder` | Reproducibility | 成果物・データ・環境が追跡不能 | 一般的傾向：再現の失敗経路 |
| Memory Footprint | `can_contribute_to` | Edge Deployment | 端末搭載時のメモリ制限 | 条件付き：軽量化が必要となる |
| Memory Bandwidth | `can_contribute_to` | Inference Latency | メモリ律速の推論処理 | 条件付き：モデルサイズだけで速度は決まらない |
| Quantization Degradation | `related_to` | Memory Footprint | 量子化施策によって精度とメモリを同時評価する場合 | 条件付き：トレードオフは介入M07において生じ得るもので、2つの課題の必然的な因果関係ではない |
| Explanation Faithfulness | `can_hinder` | Actionable Explanation | 誤った説明が対応策につながる | 条件付き：説明の可視性と忠実性は別 |
| Algorithmic Bias | `can_contribute_to` | Group Fairness | 保護集団に関連したバイアスが予測に反映 | 条件付き：不公平性指標と社会的文脈に依存 |
| Fairness under Shift | `related_to` | Worst-group Performance | 性能と公平性を集団別に評価 | 一般的傾向：公平性指標は単なる精度と同一ではない |
| Model Inversion | `related_to` | Training Data Extraction | 学習内容の復元・抽出 | 一般的傾向：攻撃モデルの前提が異なる |
| Memorization | `can_contribute_to` | Training Data Extraction | 生成モデルが訓練例を再現できる場合 | 条件付き：記憶は漏えいの必要十分条件ではない |
| Knowledge Editing | `can_contribute_to` | Catastrophic Forgetting | 継続的なパラメータ更新で既存知識が変わる | 条件付き：知識編集の副作用は忘却と一部重なる |
| Reward Hacking | `can_contribute_to` | Alignment Failure | 報酬設計が元の目的に一致しない | 条件付き：モデルが高報酬でも目標に不一致 |
| Reward Misspecification | `can_enable` | Reward Hacking | 評価可能な報酬の抜け道がある | 一般的傾向：報酬ハックは特定の学習設定で起き得る |
| Missing Modality | `can_contribute_to` | Modality-specific Robustness | 入力欠損を想定せず学習した場合 | 条件付き：欠損モダリティに頑健な設計も存在 |
| Partial Observability | `can_contribute_to` | Long-horizon Planning | 履歴や記憶機構が不十分 | 条件付き：部分観測は長期計画を難しくし得る |
| Sim-to-real Gap | `can_contribute_to` | Safe Exploration | 実世界で探索の安全性要件が厳しい場合 | 条件付き：実環境での探索に制限が必要 |
| Conservation Laws | `is_a` | Physical Consistency | 保存則は物理的一貫性の一種 | 定義/論理：より具体的な失敗条件 |
| Sparse Observation | `can_contribute_to` | Inverse Problem Ill-posedness | 逆問題で観測情報が不足している場合 | 条件付き：不適切性は観測量だけで決まらない |
| Numerical Stability | `can_contribute_to` | Scientific Plausibility | 長期間の数値シミュレーションで誤差が拡大 | 条件付き：数値的不安定は科学的妥当性を阻害し得る |

## 手法・介入（12件）

| 手法 | 操作・狙い |
|---|---|
| データ拡張（Data Augmentation） | 学習中の変動条件と不変性の誘導 |
| 再重み付け・費用感応損失（Reweighting / Cost-sensitive Loss） | 誤判定コストと学習勾配の調整 |
| 正則化（Regularization） | 関数・パラメータ空間への制約 |
| ドメイン適応手法（Domain Adaptation Method） | 対象ドメイン情報で予測器を適応 |
| 確率校正手法（Calibration Method） | スコアと頻度・リスクの対応調整 |
| 継続学習手法（Continual Learning Method） | 更新と知識保持の両立 |
| 量子化（Quantization） | 推論・学習時の数値ビット幅低減 |
| 監視手法（Model Monitoring） | 性能・特徴・挙動の継続計測 |
| 自己教師あり学習（Self-supervised Learning） | 未ラベルデータからの表現獲得 |
| アンサンブル（Ensemble Method） | 複数モデルの予測を統合 |
| 予測棄却・保留（Selective Prediction / Abstention） | リスク高の入力で自動判定を保留 |
| 条件別評価（Group-conditional Evaluation） | サブグループごとの性能を測定 |

## 手法と概念の関係（14件）

| 手法 | 関係 | 概念 | 条件 |
|---|---|---|---|
| データ拡張（Data Augmentation） | `may_mitigate` | Overfitting | 変換の妥当性と教師ラベルの保存が必要 |
| データ拡張（Data Augmentation） | `may_mitigate` | Invariance Failure | 目的の不変性を誘導できる変換の場合 |
| 再重み付け・費用感応損失（Reweighting / Cost-sensitive Loss） | `may_mitigate` | Worst-group Performance | 費用と群別指標に応じた重み付け |
| 正則化（Regularization） | `may_mitigate` | Overfitting | 正則化と対象タスクの適合が必要 |
| ドメイン適応手法（Domain Adaptation Method） | `may_mitigate` | Domain Adaptation | 対象ドメイン情報が利用可能な場合 |
| 確率校正手法（Calibration Method） | `may_mitigate` | Miscalibration | 校正用データの代表性が必要 |
| 継続学習手法（Continual Learning Method） | `may_mitigate` | Catastrophic Forgetting | 知識保持と更新のトレードオフあり |
| 量子化（Quantization） | `may_mitigate` | Memory Footprint | ビット幅低減でメモリ削減が期待できる |
| 量子化（Quantization） | `may_exacerbate` | Quantization Degradation | 量子化誤差が精度に影響する場合 |
| 監視手法（Model Monitoring） | `helps_detect` | Data Drift | 適切な基準分布や特徴が必要 |
| 自己教師あり学習（Self-supervised Learning） | `may_mitigate` | Label Scarcity | 未ラベルデータを使って表現を学習 |
| アンサンブル（Ensemble Method） | `may_mitigate` | Epistemic Uncertainty | 構成モデルが十分に多様な場合 |
| 予測棄却・保留（Selective Prediction / Abstention） | `may_mitigate` | Selective Prediction | リスク推定が有効な場合 |
| 条件別評価（Group-conditional Evaluation） | `helps_detect` | Worst-group Performance | 評価対象群の情報が得られる場合 |

## 評価指標系列（12件）

| 指標系列 |
|---|
| 訓練・検証性能差（Train/Validation Gap） |
| クラス別再現率（Per-class Recall） |
| 最悪群精度（Worst-group Accuracy） |
| 校正・確率スコア（ECE / Brier / NLL） |
| OOD識別性能（OOD AUROC） |
| 分布・潜在表現距離（MMD / Representation Distance） |
| 忘却・後方転移（Forgetting / Backward Transfer） |
| 速度・メモリ・エネルギー（Latency / VRAM / Energy） |
| 推定区間・試行間ばらつき（Statistical CI / Seed Variance） |
| リスク・自動判定率曲線（Risk–Coverage Curve） |
| 条件ごとのデータ網羅率（Data Coverage by Context） |
| 時系列の分布変化量（Temporal Drift Statistic） |

## 概念と評価指標の関係（12件）

| 概念 | 関係 | 指標系列 | 条件・補足 |
|---|---|---|---|
| Overfitting | `evaluated_with` | 訓練・検証性能差（Train/Validation Gap） | 過学習の診断に使えるが十分条件ではない |
| Class Imbalance | `evaluated_with` | クラス別再現率（Per-class Recall） | クラス別性能と頻度を併記 |
| Worst-group Performance | `evaluated_with` | 最悪群精度（Worst-group Accuracy） | 平均値と同時に表示 |
| Miscalibration | `evaluated_with` | 校正・確率スコア（ECE / Brier / NLL） | ECE単独より複数指標を併用 |
| OOD Detection | `evaluated_with` | OOD識別性能（OOD AUROC） | 未知サンプルの定義と分割が必要 |
| Out-of-Distribution Generalization | `evaluated_with` | 分布・潜在表現距離（MMD / Representation Distance） | 分布差は精度低下の直接証明ではない |
| Catastrophic Forgetting | `evaluated_with` | 忘却・後方転移（Forgetting / Backward Transfer） | タスク別性能の時系列を併記 |
| Inference Latency | `evaluated_with` | 速度・メモリ・エネルギー（Latency / VRAM / Energy） | 実ハードウェアと負荷条件で測定 |
| Run-to-run Variability | `evaluated_with` | 推定区間・試行間ばらつき（Statistical CI / Seed Variance） | 複数シード・再学習回数を指定 |
| Selective Prediction | `evaluated_with` | リスク・自動判定率曲線（Risk–Coverage Curve） | 保留率と誤り率を対で見る |
| Coverage Gap | `evaluated_with` | 条件ごとのデータ網羅率（Data Coverage by Context） | 撮影条件・クラスの組合せを点検 |
| Data Drift | `evaluated_with` | 時系列の分布変化量（Temporal Drift Statistic） | 比較基準と期間を定義 |

## 運用上の注意

- YAMLのリレーションID・端点はUUID。分類番号や過去の表示コードでは参照しない。
- 手法による効果は一般的に条件付きであり、評価値から自動的に因果結論を確定しない。
- 指標系列と計算仕様（`METRIC_SPEC_VERSION`）を分け、ECEとBrier Scoreを同じ計算指標として比較しない。
