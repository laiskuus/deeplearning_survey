# 参考文献と設計検証の範囲

## 1. 収録データ

初期カタログには、20領域、215の主概念、2つの補助概念、52の概念間関係、12の施策、12の評価指標系列、施策・評価指標への対応が含まれる。カタログは研究全体の完全網羅を保証せず、定義・概念間関係は個別の原典検証とレビューによって更新する。

## 2. 研究資料の例


これらは課題体系化の背景資料であり、52件の関係に対する**行単位の直接出典をすべて確立したものではない**。

1. Geirhos et al. (2020), *Shortcut learning in deep neural networks*, Nature Machine Intelligence. https://doi.org/10.1038/s42256-020-00257-z
2. Koh et al. (2021), *WILDS: A Benchmark of in-the-Wild Distribution Shifts*, ICML. https://proceedings.mlr.press/v139/koh21a.html
3. D’Amour et al. (2022), *Underspecification Presents Challenges for Credibility in Modern Machine Learning*, JMLR. https://www.jmlr.org/papers/v23/20-1335.html
4. NIST (2023), *AI Risk Management Framework 1.0*. https://www.nist.gov/itl/ai-risk-management-framework
5. Sculley et al. (2015), *Hidden Technical Debt in Machine Learning Systems*, NeurIPS. https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems

このうち一部は2020年以前の基礎資料であり、対象期間中の初出を意味しない。参考情報は初期カタログの参考情報として収録しており、外部サイト内容の最新確認や各エッジの原典検証はしていない。


## 3. 検証できること・できないこと

`../checks/validate_package.py` は、UUID一意性、215件の概念分類所属と分類版の参照、関係の端点型、52件の候補、ER図の共通フィールド型、Markdown相対リンク、PlantUMLブロック数、manifest内の全ファイルハッシュを検証する。`../checks/test_validation.py` は9件の正常系・異常系を検査する。

これは設計と初期データの**静的整合性検査**であり、研究内容の学術的妥当性、論文との対応、PlantUMLレンダリング結果、RDBへのロード、API動作を検証するものではない。

研究資料は出典を識別するメタデータとして保持し、個々の因果関係や効果の確定には当該主張に対応する実験・原文位置・適用条件のレビューが必要。
