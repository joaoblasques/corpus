---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-07.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - matrix factorization
  - eigendecomposition
  - Cholesky decomposition
  - LU decomposition
  - spectral decomposition
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Matrix decompositions factorize a matrix into structured components, revealing geometric and spectral properties essential for ML algorithms — eigendecomposition for symmetric matrices, Cholesky for positive definite ones, LU for general square ones.

## Determinant and Trace

**Determinant** det(A): measures how much a linear transformation scales volume. det(A) ≠ 0 iff A is invertible. det(AB) = det(A)det(B). For a 2×2 matrix: det([[a,b],[c,d]]) = ad − bc [^src1].

**Trace** tr(A) = sum_i A_{ii}: sum of diagonal entries, equal to sum of eigenvalues. Invariant under cyclic permutation: tr(ABC) = tr(CAB) = tr(BCA).

## Eigenvalues and Eigenvectors

For A ∈ R^{n×n}, a non-zero vector x is an **eigenvector** with **eigenvalue** λ if Ax = λx. Eigenvectors encode the "axes" that a matrix stretches; eigenvalues encode the scaling factors [^src1].

Eigenvalues are roots of the characteristic polynomial det(A − λI) = 0. For symmetric matrices (A = A^T), all eigenvalues are real. The **eigenspace** E_λ = {x : Ax = λx} is the null space of (A − λI).

**Spectral theorem**: Every real symmetric matrix A has n real eigenvalues and an orthonormal basis of eigenvectors — it is diagonalizable with A = PDP^T where D is diagonal (eigenvalues) and P is orthogonal (eigenvectors as columns).

## Eigendecomposition

A matrix A ∈ R^{n×n} is **diagonalizable** if it has n linearly independent eigenvectors, yielding A = PDP^{-1} where D = diag(λ_1,...,λ_n) [^src1].

For symmetric A: A = QDQ^T with Q orthogonal. This is the **eigendecomposition**. Key uses:
- Computing matrix powers: A^k = QD^k Q^T (cheap since D is diagonal)
- Understanding long-run behavior of linear dynamical systems
- Foundation of spectral methods (PCA, Fisher discriminant analysis, Laplacian eigenmaps)

**Defective matrices**: matrices with fewer than n linearly independent eigenvectors cannot be diagonalized. A matrix may be non-singular (invertible) but defective — these are distinct properties [^src1].

## Cholesky Decomposition

For a symmetric, positive definite (SPD) matrix A (x^T Ax > 0 for all x ≠ 0), a unique **Cholesky decomposition** A = LL^T exists, where L is lower triangular with positive diagonal entries [^src1].

- Positive definite iff all eigenvalues > 0 (and det > 0)
- Cholesky is roughly 2x faster than LU for SPD matrices
- Used to: solve linear systems (Ax = b → Ly = b, L^T x = y), sample from multivariate Gaussians (Σ = LL^T → sample x = Lz for z ~ N(0,I)), implement the **reparametrization trick** in variational autoencoders

## LU Decomposition

Any square matrix A (with appropriate pivoting) factors as A = PLU where P is a permutation matrix, L is lower triangular, U is upper triangular. Primarily used for numerical solution of linear systems Ax = b.

LU is the workhorse of Gaussian elimination. Determinants are then computed as det(A) = det(U) = product of diagonal entries of U (since det(P) = ±1 and det(L) = 1).

## Matrix Phylogeny

The book organizes matrices into a hierarchy [^src1]:
- All real matrices → SVD always exists (see [SVD](/ai-engineering/singular-value-decomposition.md))
- Square matrices → determinant exists; invertible (regular) if det ≠ 0
- Non-defective square matrices → eigendecomposition exists
- Normal matrices (A^T A = AA^T) → subset includes symmetric matrices
- Symmetric matrices → real eigenvalues; orthogonal eigenvectors
- Positive definite symmetric matrices → Cholesky decomposition exists; all eigenvalues > 0
- Orthogonal matrices (A^T A = I) → subset of regular matrices; A^{-1} = A^T

## Relationship to SVD

SVD generalizes eigendecomposition to non-square matrices and is more numerically stable. For a symmetric PSD matrix A = XX^T, the eigenvalues of A equal the squared singular values of X; see [SVD](/ai-engineering/singular-value-decomposition.md) for the full treatment including the Eckart-Young theorem.

[^src1]: [Mathematics for Machine Learning, Part 7](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-07.md)
