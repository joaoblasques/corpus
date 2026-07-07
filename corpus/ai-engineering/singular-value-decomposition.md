---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-01.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - SVD
  - Singular Value Decomposition
  - PCA
  - Principal Component Analysis
  - truncated SVD
  - rSVD
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Singular Value Decomposition (SVD)

TL;DR: The SVD decomposes any matrix **X** = **UΣV*** into orthonormal bases **U** (left singular vectors), **V** (right singular vectors), and diagonal **Σ** (singular values). It produces the optimal low-rank approximation (Eckart–Young theorem) and is the mathematical backbone of PCA, DMD, compressed sensing, and reduced-order models.

## Core decomposition

For a matrix **X** ∈ ℝ^(n×m):

**X** = **UΣV***

Where:
- **U** ∈ ℝ^(n×n): left singular vectors (columns are orthonormal spatial modes)
- **Σ** ∈ ℝ^(n×m): diagonal matrix of singular values σ₁ ≥ σ₂ ≥ ... ≥ 0 (in decreasing order)
- **V** ∈ ℝ^(m×m): right singular vectors (columns are orthonormal temporal modes)

The rank-r truncation **X** ≈ **Ũ** **Σ̃** **Ṽ*** using only the top r singular values/vectors is the best possible rank-r approximation in both the L2 and Frobenius norms (Eckart–Young theorem) [^src1].

## PCA connection

Principal Component Analysis (PCA) is a special case of SVD applied to centered data. PCA finds the directions of maximum variance (principal components = left singular vectors **U**). The proportion of variance explained by each component = σᵢ² / Σσⱼ² [^src1].

**Eigenfaces** (face recognition on image matrices) is the canonical PCA example: a 100×100-pixel face image lives in ℝ^10000 but the "face manifold" is ~50-dimensional. SVD reveals this intrinsic low-rank structure [^src1].

## Key variants

| Variant | Key idea |
|---|---|
| Truncated SVD | Keep only top-r modes; O(mnr) instead of O(min(mn², m²n)) |
| Randomized SVD (rSVD) | Random projections to estimate dominant subspace; further speedup |
| Robust PCA | Decomposes **X** = **L** + **S** (low-rank + sparse); handles outliers and corrupted data |
| Tensor decompositions | Extension to N-way arrays (CP decomposition, Tucker decomposition) |

## Pseudo-inverse and least squares

The Moore-Penrose pseudo-inverse **X**† = **VΣ**⁻¹**U*** solves the least-squares problem **Xξ** ≈ **y** optimally when **X** is rank-deficient. This connects SVD directly to regression [^src1].

## Applications

- **Image compression**: JPEG-like compression via rank-r SVD (trade quality for file size)
- **Noise filtering**: zero out small singular values corresponding to noise
- **DMD**: SVD is the first step of Dynamic Mode Decomposition (see [DMD](/ai-engineering/dynamic-mode-decomposition.md))
- **Reduced-order models**: SVD modes (**U**) form the projection basis
- **Compressed sensing**: SVD basis is optimal for sparse signal recovery (see [Compressed Sensing](/ai-engineering/compressed-sensing.md))

[^src1]: [Data-Driven Science and Engineering](../../raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-01.md), Brunton & Kutz (2021), Chapter 1
