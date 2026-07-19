---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-mining-of-massive-datasets-part-25.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-mining-of-massive-datasets-part-26.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-mining-of-massive-datasets-part-27.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-mining-of-massive-datasets-part-28.md
    channel: pdf
    ingested_at: 2026-07-19
aliases:
  - MMDS
  - Mining of Massive Datasets
  - Leskovec Rajaraman Ullman
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-19
updated: 2026-07-19
---

# Mining of Massive Datasets (Leskovec, Rajaraman, Ullman)

TL;DR: Graduate textbook on algorithms for large-scale data — covering MapReduce, locality-sensitive hashing, stream processing, clustering, recommender systems, link analysis (PageRank), and machine learning at scale (SVD, CUR decomposition, perceptrons, SVMs, nearest-neighbor).

## Coverage (parts 25-28)

The ingested portions cover Chapters 11–12 of the book:

**Chapter 11 — Dimensionality Reduction**
- Singular Value Decomposition (SVD): eigenvalues from M^T M and MM^T; U, Σ, V^T decomposition; using SVD for concept-space queries and collaborative filtering. [^mmds-p25]
- Energy retention: minimizing reconstruction error by preserving the k largest singular values. [^mmds-p25]
- **CUR Decomposition**: an alternative to SVD for sparse matrices. Randomly selects r columns (matrix C) and r rows (matrix R) with probability proportional to squared Frobenius norm; constructs middle matrix U via pseudoinverse of the intersection matrix W. Advantage: C and R inherit sparsity from M, unlike dense U and V in SVD. [^mmds-p25]
- Eliminating duplicate rows/columns in CUR via √k scaling.

**Chapter 12 — Large-Scale Machine Learning**
- Training set, feature vectors, labels; regression vs binary classification vs multiclass classification.
- Architectures: batch vs on-line learning; active learning; feature selection; cross-validation.
- **Perceptron**: linear binary classifier with weight vector w and threshold θ; training via gradient ascent update w ← w + ηyx on misclassified point. Converges to a separating hyperplane when data is linearly separable. [^mmds-p26]
- **Support Vector Machines**: maximize margin between support vectors and hyperplane; hinge loss; gradient descent via quadratic programming or GD with on-disk data. [^mmds-p27]
- **k-Nearest Neighbor (kNN)**: instance-based learning; classify by majority vote of k nearest neighbors; multi-dimensional index structures for approximate search. [^mmds-p27]
- Large-scale techniques: stochastic gradient descent; locality-sensitive hashing for nearest-neighbor search.

## Key ideas

- CUR decomposition is preferable to SVD when the original matrix is sparse, because C and R remain sparse while U and V in SVD are typically dense. [^mmds-p25]
- "Mining of Massive Datasets" views machine learning through the lens of scalability: how to run these algorithms when data cannot fit in memory. [^mmds-p28]
- Perceptrons only converge when data is linearly separable; SVMs extend this by finding the *best* hyperplane even when no perfect separator exists. [^mmds-p26]

## Related corpus pages

- [Singular Value Decomposition](/ai-engineering/singular-value-decomposition.md)
- [CUR Decomposition](/ai-engineering/cur-decomposition.md)
- [Support Vector Machines](/ai-engineering/support-vector-machines.md)
- [Machine Learning](/ai-engineering/machine-learning.md)
- [PCA and Dimensionality Reduction](/ai-engineering/pca-and-dimensionality-reduction.md)
- [Recommender Systems](/ai-engineering/recommender-systems.md)

[^mmds-p25]: raw/pdf/pdf-mining-of-massive-datasets-part-25.md — Chapter 11: Dimensionality Reduction (SVD, CUR)
[^mmds-p26]: raw/pdf/pdf-mining-of-massive-datasets-part-26.md — Chapter 12: Perceptrons
[^mmds-p27]: raw/pdf/pdf-mining-of-massive-datasets-part-27.md — Chapter 12: SVMs via gradient descent
[^mmds-p28]: raw/pdf/pdf-mining-of-massive-datasets-part-28.md — Chapter 12 index and references
