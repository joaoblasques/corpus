---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-16.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-17.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-19.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-20.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - PCA
  - principal component analysis
  - dimensionality reduction
  - eigenfaces
  - probabilistic PCA
  - PPCA
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# PCA and Dimensionality Reduction

TL;DR: PCA finds a low-dimensional linear subspace that captures maximum variance in data. Principal components are eigenvectors of the data covariance matrix S = (1/N) X X^T, ordered by eigenvalue magnitude. Equivalently, PCA minimizes average squared reconstruction error. The Eckart-Young theorem (covered at [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md)) connects PCA to the best low-rank SVD approximation. Practical steps: center, standardize, eigendecompose, project. In high dimensions (D >> N), compute with N×N matrix instead of D×D for efficiency.

## Problem Setting

Given N data points x_n in R^D. Goal: find an M-dimensional (M < D) representation that preserves structure [^src1].

Two equivalent perspectives:
1. **Maximum variance**: find projection that maximizes variance of projected data
2. **Minimum reconstruction error**: find projection that minimizes average squared distance between original and reconstructed data

Both yield the same solution: eigenvectors of the data covariance matrix.

**Why reduce dimensions?**
- Visualization (M = 2 or 3)
- Remove noise (low-variance directions often capture noise)
- Compression (store M < D numbers per data point)
- Speed up downstream algorithms (curse of dimensionality)

## Data Covariance Matrix

Center the data: mu = (1/N) sum_n x_n. Compute centered data matrix X_c.

**Data covariance matrix** [^src1]:

```
S = (1/N) sum_n (x_n - mu)(x_n - mu)^T = (1/N) X_c X_c^T  in R^{D x D}
```

S is symmetric positive semidefinite. Its eigenvectors are the principal directions.

## Maximum Variance Derivation

Seek unit vector b_1 (the first principal component) to maximize variance of projected data {b_1^T x_n} [^src1]:

```
Var[b_1^T x] = b_1^T S b_1    subject to ||b_1|| = 1
```

Using Lagrange multiplier: maximize b_1^T S b_1 - lambda(b_1^T b_1 - 1). Setting gradient to zero: **S b_1 = lambda b_1**. So b_1 is an eigenvector of S, and the variance equals eigenvalue lambda.

To maximize variance, choose the eigenvector corresponding to the **largest eigenvalue** lambda_1.

For M components: choose the M eigenvectors corresponding to the M largest eigenvalues. These span the **principal subspace** U_M [^src1].

## Projection Perspective (Reconstruction Error)

Alternative derivation via minimizing reconstruction error [^src1]:

Given projection matrix B = [b_1, ..., b_M] in R^{D x M}, the reconstruction of x is:

```
x_tilde = BB^T x + mu_x - BB^T mu_x
```

Average squared reconstruction error:

```
J = (1/N) sum_n ||x_n - x_tilde_n||^2
```

Minimizing J over B (subject to B^T B = I_M) yields the same eigenvectors of S. The minimum reconstruction error for the M-dimensional subspace is sum_{d=M+1}^D lambda_d (sum of discarded eigenvalues) [^src1].

**Key insight**: both perspectives — maximize retained variance and minimize discarded variance — yield identical solutions.

## Eckart-Young Connection

The Eckart-Young theorem (see [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md)) states that the best rank-M approximation to X (in spectral and Frobenius norm) is given by truncating the SVD at M singular values [^src1]:

```
X_tilde_M = U_M Sigma_M V_M^T
```

This directly connects PCA to SVD: the left singular vectors U_M of the (centered) data matrix X_c are the principal components.

**Relationship between SVD and covariance eigenvectors**:
- S = (1/N) X_c X_c^T  →  eigenvectors of S = left singular vectors of X_c / sqrt(N)
- Singular values of X_c = sqrt(N) * sqrt(eigenvalues of S)

## PCA in High Dimensions

If D >> N (e.g., image data with millions of pixels but thousands of images), computing the D×D covariance matrix S is infeasible [^src1].

**Trick**: the nonzero eigenvalues of S = (1/N) X X^T and of (1/N) X^T X are identical. The N×N matrix (1/N) X^T X has the same spectrum as S but is far smaller [^src1].

**Algorithm for D >> N**:
1. Compute (1/N) X^T X in R^{N x N}
2. Find its eigenvectors c_m (each in R^N)
3. Recover original eigenvectors: b_m = X c_m (unnormalized), then normalize

This reduces eigendecomposition from O(D^3) to O(N^3) time.

**Power iteration**: for computing only the top eigenvector, iteratively multiply by S and renormalize. Converges to the dominant eigenvector. The original Google PageRank algorithm uses this approach [^src1].

## Practical PCA Steps

Algorithm for performing PCA on a dataset [^src1]:

1. **Mean subtraction**: compute sample mean mu, subtract from each x_n. Ensures data is zero-centered.

2. **Standardization**: divide by standard deviation sigma_d along each dimension d. Makes data unit-free; prevents dimensions with large numerical values from dominating.

3. **Eigendecomposition of covariance matrix**: compute S = (1/N) X_c X_c^T; find eigenvalues lambda_1 >= ... >= lambda_D and eigenvectors b_1, ..., b_D (columns of projection matrix B).

4. **Select M**: choose number of components. Common criteria: retain 95% of total variance (sum_{m=1}^M lambda_m / sum_d lambda_d >= 0.95), or use elbow in scree plot.

5. **Projection**: for new test point x*, standardize using training data statistics, then: z = B_M^T ((x* - mu) / sigma) in R^M.

6. **Reconstruction (if needed)**: x_tilde = B_M z * sigma + mu in R^D. Note: standardization must be undone.

## Latent Variable Perspective (Probabilistic PCA)

**Probabilistic PCA (PPCA)** (Tipping and Bishop, 1999) models the generative process [^src1]:

```
z ~ N(0, I_M)          (latent variable)
x | z ~ N(Bz + mu, sigma^2 I_D)  (observation)
```

where B in R^{D x M} maps latent to observation space. The MLE of B recovers the principal components (up to rotation). sigma^2 -> 0 reduces to standard PCA.

**Benefits of PPCA**:
- Principled handling of missing data (treat missing as marginalized)
- Probabilistic interpretation of reconstruction
- Extension to mixtures of PPCA (MPPCA) for multi-modal data

## Eigenfaces (Application)

A classic PCA application: face recognition via the eigenfaces method [^src1].

**Setup**: N face images in R^D (D = width × height pixels). Compute covariance matrix S and its top M eigenvectors (eigenfaces u_1, ..., u_M).

**Encoding**: each face x is represented by M coordinates: alpha_m = u_m^T (x - mu).

**Reconstruction**: x_tilde = mu + sum_m alpha_m u_m.

**Recognition**: compare query to database using Euclidean distance in the M-dimensional eigenface space. Much cheaper than pixel-space comparison.

The eigenfaces are interpretable: early ones capture broad illumination and face shape; later ones capture finer features. This reveals that face space is low-dimensional (~50-100 components often sufficient for recognition).

## Loading Vectors, Score Vectors, and the Biplot (ISL)

ISL introduces PCA via the **loading vector** φ_m (each element a loading) and **score vector** z_m (the projections of observations onto φ_m) [^src3].

**Loading vector** φ_1 = (φ_11, φ_21, ..., φ_p1): defines the direction of maximum variance. Elements constrained to sum-of-squares = 1. The first PC score for observation i: z_i1 = φ_11*x_i1 + ... + φ_p1*x_ip [^src3].

**Biplot**: a plot that simultaneously displays the score vectors (observations in PC space) and the loading vectors (variable directions) on the same axes. Standard tool for interpreting PCA results [^src3].

**Uniqueness**: each loading vector is unique up to a sign flip; flipping the sign of a loading vector simultaneously requires flipping the corresponding scores, leaving the product z_im * φ_jm unchanged [^src3].

## Proportion of Variance Explained (PVE) and Scree Plot

**PVE of the m-th PC** = (sum_i z_im^2) / (sum_j sum_i x_ij^2). The total variance in a mean-centered dataset is sum_j sum_i x_ij^2 [^src4].

**Scree plot**: bar/line chart of PVE per component. Look for an "elbow" — the point where PVE drops sharply — to decide how many components to retain. ISL USArrests example: PC1=62.0%, PC2=24.7%, together 86.7%; elbow after PC2 [^src4].

**Selecting M**: no universal rule for unsupervised PCA. Contrast with supervised PCR (principal components regression), where the number of PCs is selected by cross-validation as a tuning parameter [^src4].

**PCA as denoising**: running clustering on the first few PC score vectors rather than the full data can yield better results, treating the PC step as denoising (signal concentrates in leading PCs) [^src4].

## Limitations of PCA

- **Linear only**: cannot capture nonlinear structure (manifolds). Kernel PCA or autoencoders address this.
- **Unsupervised**: does not use labels; the directions of maximum variance may not be discriminative directions.
- **Sensitive to scale**: standardization required when features have different units — ISL confirms this with the USArrests example (unscaled PCA dominated by Assault's large variance) [^src3].
- **Global structure only**: does not preserve local neighborhoods (t-SNE and UMAP do).
- **Subjective M selection**: for unsupervised PCA, how many components to keep is an inherently ad hoc, exploratory decision [^src4].

## Related Corpus Pages

- [/ai-engineering/linear-algebra-for-ml.md](/ai-engineering/linear-algebra-for-ml.md) — orthogonal projections, eigenvectors
- [/ai-engineering/matrix-decompositions.md](/ai-engineering/matrix-decompositions.md) — eigendecomposition; SVD overview
- [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md) — Eckart-Young theorem, low-rank approximation
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — probabilistic PCA; Gaussian marginals
- [/ai-engineering/clustering-methods.md](/ai-engineering/clustering-methods.md) — K-means and hierarchical clustering; complement to PCA for unsupervised learning
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — full book summary
- [/ai-engineering/sources/introduction-to-statistical-learning.md](/ai-engineering/sources/introduction-to-statistical-learning.md) — ISL book summary

---

[^src1]: [Mathematics for Machine Learning, Part 16](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-16.md)
[^src2]: [Mathematics for Machine Learning, Part 17](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-17.md)
[^src3]: [Introduction to Statistical Learning, Part 19](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-19.md)
[^src4]: [Introduction to Statistical Learning, Part 20](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-20.md)
