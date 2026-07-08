---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-01.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-02.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-03.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-04.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-05.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-06.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-07.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-08.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-09.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-10.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-12.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-13.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-14.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-15.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-16.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-17.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-18.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-19.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-20.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - MML
  - Mathematics for Machine Learning Deisenroth
  - Deisenroth Faisal Ong
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-08
updated: 2026-07-08
---

# Mathematics for Machine Learning (Deisenroth, Faisal, Ong)

TL;DR: A 417-page textbook (Cambridge University Press, 2020) bridging the gap between high-school mathematics and machine learning. Part I covers six mathematical pillars; Part II applies them to four canonical ML problems. Freely available at mml-book.com. Targets practitioners who want principled understanding, not just algorithmic recipes.

## Bibliographic Details

- **Authors:** Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong
- **Publisher:** Cambridge University Press, 2020
- **Free edition:** https://mml-book.com (author-released PDF)
- **Pages:** 417

## Book Structure

The book is divided into two parts organized around six mathematical foundations and four ML application pillars [^src1].

**Part I — Mathematical Foundations**

| Ch | Topic | Key sections |
|----|-------|-------------|
| 2 | Linear Algebra | Systems of equations, matrices, vector spaces, linear independence, basis, rank, linear mappings, affine spaces |
| 3 | Analytic Geometry | Norms, inner products, lengths, angles, orthogonality, Gram-Schmidt, orthogonal projections, rotations |
| 4 | Matrix Decompositions | Determinants, eigenvalues/eigenvectors, Cholesky, eigendecomposition, SVD, matrix approximation |
| 5 | Vector Calculus | Differentiation, partial derivatives, gradients, Jacobians, backpropagation, Taylor series |
| 6 | Probability and Distributions | Probability spaces, Bayes, Gaussian, conjugacy, exponential family, change of variables |
| 7 | Continuous Optimization | Gradient descent, Lagrange multipliers, KKT, convex optimization, LP, QP |

**Part II — Central Machine Learning Problems**

| Ch | Topic |
|----|-------|
| 8 | When Models Meet Data (empirical risk minimization, MLE, graphical models, model selection) |
| 9 | Linear Regression (MLE, MAP, Bayesian linear regression, orthogonal projection) |
| 10 | Dimensionality Reduction with PCA |
| 11 | Density Estimation with Gaussian Mixture Models (EM algorithm) |
| 12 | Classification with Support Vector Machines (primal/dual SVM, kernels) |

## Core Thesis

"Machine learning is about designing algorithms that automatically extract valuable information from data." The three components are **data** (represented as vectors), **models** (functions describing the data-generating process), and **learning** (optimizing model parameters via numerical methods) [^src1].

The book's motivation: the gap between high-school mathematics and standard ML textbooks is too large. MML closes that gap with principled mathematical treatment applied directly to ML [^src1].

## Key Claims by Chapter

### Linear Algebra (Ch. 2–3)

- Linear algebra is the study of vectors and rules to manipulate them. Any object satisfying closure under addition and scalar multiplication is a vector [^src1].
- A system of linear equations **Ax = b** has no solution, exactly one solution, or infinitely many solutions [^src2].
- Vector spaces are the fundamental structure: closed under addition and scaling. A basis is a minimal spanning set; rank of a matrix equals the dimension of its column space [^src3].
- Linear mappings (linear maps) can be represented as matrices once bases are fixed; change of basis is a key operation [^src3].
- Inner products generalize the dot product: they induce norms, angles, and orthogonality. Orthogonal projections minimize distance to a subspace [^src4].
- Gram-Schmidt orthogonalization constructs an orthonormal basis from any basis iteratively [^src5].

### Matrix Decompositions (Ch. 4)

- **Determinant**: product of eigenvalues; measures volume scaling by the linear map [^src6].
- **Eigenvalues/eigenvectors**: **Ax = λx**. The spectral theorem: symmetric matrices have real eigenvalues and an orthonormal eigenbasis [^src6].
- **Cholesky decomposition**: every symmetric positive-definite matrix **A = LL^T** where **L** is lower-triangular with positive diagonal. Used to sample from multivariate Gaussians and compute determinants efficiently [^src6].
- **Eigendecomposition**: **A = PDP^{-1}** requires n linearly independent eigenvectors. For symmetric **S**: **S = PDP^T** with orthogonal **P** [^src6].
- **SVD**: **A = UΣV^T** exists for any matrix; referred to as "the fundamental theorem of linear algebra." Singular values are square roots of eigenvalues of **A^T A** [^src7].
- **Eckart-Young theorem**: rank-k truncated SVD gives the best rank-k approximation in spectral and Frobenius norms [^src7].

### Vector Calculus (Ch. 5)

- Partial derivatives generalize to the Jacobian matrix **J ∈ R^{m×n}** for vector-valued functions **f: R^n → R^m** [^src8].
- Gradients of matrices with respect to vectors yield higher-order tensors; flatten-then-reshape is a practical computation strategy [^src8].
- Backpropagation is an application of the chain rule across a computation graph; yields gradients of a scalar loss w.r.t. all parameters [^src9].

### Probability and Distributions (Ch. 6)

- Bayes' theorem: **p(θ|x) ∝ p(x|θ) p(θ)**. Posterior is proportional to likelihood × prior [^src10].
- Multivariate Gaussian **N(μ, Σ)**: fully specified by mean vector **μ** and covariance matrix **Σ**. Marginals and conditionals of Gaussians are Gaussian [^src10].
- Sampling from **N(μ, Σ)**: use Cholesky **Σ = LL^T**, draw **z ~ N(0, I)**, then **x = Lz + μ** [^src10].
- Exponential family: **p(x|θ) = h(x) exp(θ^T φ(x) − A(θ))**. Includes Gaussian, Bernoulli, Binomial, Beta. Finite-dimensional sufficient statistics; conjugate priors always exist within the family [^src11].
- Change of variables: if **y = U(x)**, then **f_Y(y) = f_X(U^{-1}(y)) · |dU^{-1}/dy|** [^src11].

### Continuous Optimization (Ch. 7)

- Gradient descent: **θ_{t+1} = θ_t − α ∇L(θ_t)**. Step size (learning rate) α controls convergence; too large diverges, too small is slow [^src12].
- Constrained optimization via Lagrange multipliers: stationarity, primal feasibility, dual feasibility, complementary slackness (KKT conditions) [^src12].
- Convex optimization: objective and inequality constraints are convex functions; every local minimum is global. Includes LP and QP as special cases [^src12].
- Jensen's inequality: for convex f and weights summing to 1: **f(Σα_i x_i) ≤ Σα_i f(x_i)** [^src12].

### When Models Meet Data (Ch. 8)

- Empirical risk minimization: minimize average loss over training set. Squared loss for regression; cross-entropy for classification [^src13].
- MLE finds parameters that maximize the likelihood of observed data; MAP adds a prior term (equivalent to regularization) [^src13].

### Linear Regression (Ch. 9)

- MLE solution: **θ_ML = (Φ^T Φ)^{-1} Φ^T y** (normal equations / pseudo-inverse) [^src15].
- MAP with Gaussian prior adds regularization: **θ_MAP = (Φ^T Φ + σ²/b² I)^{-1} Φ^T y** [^src15].
- Overfitting: polynomial degree too high → training error → 0 but test error rises. Cross-validation selects degree [^src15].
- Bayesian linear regression: maintains a posterior distribution over parameters rather than a point estimate; provides uncertainty quantification [^src14].

### PCA (Ch. 10)

- PCA finds the directions of maximum variance in data. Principal components are eigenvectors of the data covariance matrix **S = (1/N) X X^T** [^src16].
- Equivalently: minimizes average squared reconstruction error. Both perspectives give the same eigenvectors [^src16].
- In high dimensions (D >> N): compute eigenvectors of the N×N matrix **(1/N) X^T X** instead of D×D **S**; same nonzero eigenvalues [^src17].
- Practical steps: center data, standardize, compute eigendecomposition of covariance matrix, project [^src17].

### GMM (Ch. 11)

- GMM: **p(x) = Σ_k π_k N(x | μ_k, Σ_k)** where π_k are mixing weights summing to 1 [^src18].
- EM algorithm alternates E-step (compute responsibilities **r_{nk} = π_k N(x_n | μ_k, Σ_k) / p(x_n)**) and M-step (update μ_k, Σ_k, π_k using responsibilities) [^src18].

### SVM (Ch. 12)

- Hard-margin SVM: find maximum-margin separating hyperplane. Primal: minimize **||w||²** subject to **y_n(w^T x_n + b) ≥ 1** [^src19].
- Soft-margin SVM: introduces slack variables ξ_n to allow misclassification with penalty C [^src19].
- Dual SVM: expressed in terms of inner products only → kernel trick: replace **<x_i, x_j>** with **k(x_i, x_j)** [^src19].

## Conceptual Framework: Four Pillars of ML

The book organizes ML around four algorithmic pillars, each requiring different subsets of the mathematical foundations [^src1]:

```
Machine Learning
├── Regression (Ch. 9)               ← Linear algebra, optimization, probability
├── Dimensionality Reduction (Ch. 10) ← Linear algebra, matrix decompositions
├── Density Estimation (Ch. 11)       ← Probability, optimization
└── Classification (Ch. 12)           ← Linear algebra, convex optimization
```

## Related Corpus Pages

- [/ai-engineering/linear-algebra-for-ml.md](/ai-engineering/linear-algebra-for-ml.md) — Ch. 2–3 content
- [/ai-engineering/matrix-decompositions.md](/ai-engineering/matrix-decompositions.md) — Ch. 4 content
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — Ch. 6 content
- [/ai-engineering/optimization-for-ml.md](/ai-engineering/optimization-for-ml.md) — Ch. 7 content
- [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md) — Ch. 10 content
- [/ai-engineering/gaussian-mixture-models.md](/ai-engineering/gaussian-mixture-models.md) — Ch. 11 content
- [/ai-engineering/support-vector-machines.md](/ai-engineering/support-vector-machines.md) — Ch. 12 content
- [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md) — SVD/Eckart-Young (Brunton & Kutz perspective)

---

[^src1]: [Mathematics for Machine Learning, Part 1](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-01.md)
[^src2]: [Mathematics for Machine Learning, Part 2](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-02.md)
[^src3]: [Mathematics for Machine Learning, Part 3](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-03.md)
[^src4]: [Mathematics for Machine Learning, Part 4](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-04.md)
[^src5]: [Mathematics for Machine Learning, Part 5](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-05.md)
[^src6]: [Mathematics for Machine Learning, Part 6](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-06.md)
[^src7]: [Mathematics for Machine Learning, Part 7](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-07.md)
[^src8]: [Mathematics for Machine Learning, Part 8](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-08.md)
[^src9]: [Mathematics for Machine Learning, Part 9](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-09.md)
[^src10]: [Mathematics for Machine Learning, Part 10](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-10.md)
[^src11]: [Mathematics for Machine Learning, Part 11](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md)
[^src12]: [Mathematics for Machine Learning, Part 12](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-12.md)
[^src13]: [Mathematics for Machine Learning, Part 13](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-13.md)
[^src14]: [Mathematics for Machine Learning, Part 14](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-14.md)
[^src15]: [Mathematics for Machine Learning, Part 15](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-15.md)
[^src16]: [Mathematics for Machine Learning, Part 16](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-16.md)
[^src17]: [Mathematics for Machine Learning, Part 17](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-17.md)
[^src18]: [Mathematics for Machine Learning, Part 18](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-18.md)
[^src19]: [Mathematics for Machine Learning, Part 19](../../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-19.md)
