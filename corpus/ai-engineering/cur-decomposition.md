---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-mining-of-massive-datasets-part-25.md
    channel: pdf
    ingested_at: 2026-07-19
aliases:
  - CUR decomposition
  - CUR
  - column-row-union decomposition
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-19
updated: 2026-07-19
---

# CUR Decomposition

TL;DR: CUR decomposes a sparse matrix M ≈ CUR into three matrices — C (randomly selected columns), U (a middle connector), and R (randomly selected rows) — such that C and R remain sparse like M. This preserves interpretability and memory efficiency that SVD's dense U/V factors lose.

## Motivation

SVD is optimal for low-rank approximation (Eckart–Young), but even when M is sparse, its factor matrices U and V are typically dense. For matrices with millions of rows/columns (web interaction matrices, document-term matrices), dense U and V are impractical. CUR trades approximation quality for sparsity. [^mmds-p25]

## Algorithm

Given M (m×n) and a target rank r:

1. **Select r columns** for C: column j is chosen with probability q_j = (sum of squares of column j) / (Frobenius norm² of M). Scale selected column j by 1/√(r·q_j). Columns may be selected more than once; duplicates are merged with √k scaling.

2. **Select r rows** for R: row i chosen with probability p_i = (sum of squares of row i) / (Frobenius norm² of M). Scale by 1/√(r·p_i).

3. **Build W** (r×r): the intersection of the chosen columns and rows from M.

4. **Compute U**: take the SVD of W = XΣY^T; form the pseudoinverse Σ^+ (invert nonzero diagonal elements, leave zeros); then U = Y(Σ^+)²X^T. [^mmds-p25]

The product C·U·R approximates M.

## Properties

- **C and R are sparse** when M is sparse — unlike dense U and V in SVD. [^mmds-p25]
- **Interpretable**: selected rows and columns are actual rows/columns of M, not abstract linear combinations.
- **Approximation quality**: convergence to M is guaranteed as r grows, but in practice r must be very large for tight approximation. CUR is better suited to applications that tolerate moderate approximation error.
- **High-importance sampling**: the Frobenius-norm-based probability biases selection toward rows and columns with large values, capturing the dominant structure of M.

## Relationship to SVD

CUR is a randomized approximation; SVD is the exact optimal decomposition. Both decompose M into three matrices. SVD minimizes reconstruction error for a given rank; CUR sacrifices that guarantee for sparsity and interpretability. The middle matrix U in CUR plays the role of Σ in SVD, but U is constructed via the pseudoinverse rather than being diagonal. [^mmds-p25]

## Related pages

- [Singular Value Decomposition](/ai-engineering/singular-value-decomposition.md) — the exact counterpart; CUR sacrifices optimality for sparsity
- [PCA and Dimensionality Reduction](/ai-engineering/pca-and-dimensionality-reduction.md)
- [Recommender Systems](/ai-engineering/recommender-systems.md) — typical application (user-item matrices are sparse)
- [Matrix Decompositions](/ai-engineering/matrix-decompositions.md)

[^mmds-p25]: raw/pdf/pdf-mining-of-massive-datasets-part-25.md — Chapter 11: CUR Decomposition (§11.4)
