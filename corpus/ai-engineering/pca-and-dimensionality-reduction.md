---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-15.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-17.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - PCA
  - principal component analysis
  - dimensionality reduction
  - principal subspace
  - eigenfaces
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: PCA finds the low-dimensional linear subspace that captures maximum variance in data; derived as an eigendecomposition of the data covariance matrix, it is equivalent to optimal (in spectral norm sense) low-rank approximation via SVD.

## Problem Setting

Given N data points x_n ∈ R^D, find an M-dimensional subspace (M ≪ D) that best represents the data. PCA is an unsupervised method — no labels. Two equivalent perspectives [^src1]:

1. **Maximum variance**: find the projection direction that maximizes variance of projected data
2. **Minimum reconstruction error**: find the subspace minimizing average squared distance between original data and its projection

Both lead to the same eigenvector solution.

## Maximum Variance Perspective

After mean-centering (x_n ← x_n − μ), the data covariance matrix is S = (1/N) X X^T ∈ R^{D×D}. The first principal component b_1 maximizes [^src1]:

Var[b_1^T x] = b_1^T S b_1 subject to ||b_1|| = 1

By Lagrangian optimization (Lagrange multiplier λ): S b_1 = λ b_1. So b_1 must be an **eigenvector of S**; to maximize variance, choose the one with the **largest eigenvalue** λ_1. The projected variance equals λ_1.

More generally: the M principal components are the eigenvectors corresponding to the M largest eigenvalues of S, forming an orthonormal basis for the **principal subspace**.

## Projection Perspective

The projection of data point x_n onto the principal subspace is z_n = B^T x_n ∈ R^M (coordinates in the new basis) where B = [b_1,...,b_M]. The reconstruction is B z_n ∈ R^D.

The average squared reconstruction error is minimized by the same eigenvectors — minimizing reconstruction error is equivalent to maximizing variance [^src1].

## Relationship to SVD and Eckart-Young

The data matrix X ∈ R^{D×N} has SVD X = U Σ V^T. The best rank-M approximation (Eckart-Young theorem) is X_M = U_M Σ_M V_M^T, obtained by keeping only the top M singular values and vectors [^src1].

The principal components B = U_M are exactly the left singular vectors of X corresponding to the M largest singular values. The eigenvalues of S = (1/N)XX^T equal σ_i^2 / N. So PCA and truncated SVD are computationally equivalent.

For the Eckart-Young theorem and the spectral norm optimality proof, see [SVD](/ai-engineering/singular-value-decomposition.md).

## Practical Steps

1. **Mean subtraction**: compute μ = (1/N) Σ x_n; subtract from all data points
2. **Standardization**: divide each dimension by its standard deviation (makes data unit-free, variance 1 per axis)
3. **Eigendecomposition** of covariance matrix S: compute eigenvalues and eigenvectors (use `np.linalg.eigh` or `np.linalg.svd`)
4. **Select M components**: choose M largest eigenvalues (retain fraction of total variance = Σ_{i=1}^M λ_i / Σ_i λ_i)
5. **Project**: z_n = B^T x_n_standardized; reconstruct with B z_n + μ (after undoing standardization) [^src1]

## PCA in High Dimensions

When D ≫ N (e.g., images with 10,000 pixels but only 500 samples), the D×D covariance matrix is infeasible. Key insight: S = (1/N) XX^T and (1/N) X^T X share the same nonzero eigenvalues [^src1].

Solve the N×N eigenproblem for (1/N) X^T X → get eigenvectors c_m ∈ R^N → recover principal components b_m = X c_m (normalize to unit length). Cost is O(N^2 D) instead of O(D^3).

**Power iteration**: for the single top eigenvector, iteratively apply S and normalize: x_{k+1} = S x_k / ||S x_k||. Converges to the leading eigenvector. Used in Google PageRank.

## Data Compression and Eigenfaces

**MNIST example**: 60,000 images of 784 pixels each. PCA with M=10 principal components captures dominant stroke patterns; increasing M improves reconstruction. The principal components are "eigendigits" — basis images that combine to represent any digit [^src1].

**Eigenfaces**: same approach applied to face images. Each face is a linear combination of eigenfaces (principal components of a face dataset). Used for face recognition in low-dimensional eigenface space.

## Latent Variable Perspective (PPCA)

Probabilistic PCA (PPCA) interprets PCA through a generative model: x = Wz + μ + ε where z ~ N(0,I), ε ~ N(0,σ^2 I). The MLE of W recovers the principal subspace; the posterior p(z|x) is the PCA projection. PPCA enables missing data handling and Bayesian model comparison.

[^src1]: [Mathematics for Machine Learning, Part 17](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-17.md)
