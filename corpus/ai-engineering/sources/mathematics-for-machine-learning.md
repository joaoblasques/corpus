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
  - Deisenroth Faisal Ong
  - Mathematics for Machine Learning book
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Comprehensive textbook (417 pages, Cambridge University Press 2020) covering mathematical foundations for ML — linear algebra, analytic geometry, matrix decompositions, vector calculus, probability, optimization — applied to four central problems: linear regression, PCA, GMMs, and SVMs.

## Authors and Publication

Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong. Published by Cambridge University Press (2020). Author-free edition available at https://mml-book.com. 417 pages, split into 20 PDF parts for corpus ingestion.

## Book Structure

**Part I: Mathematical Foundations**

- **Ch 1 — Introduction and Motivation**: Three core ML concepts (data, models, learning); book designed for bottom-up or top-down reading; targets undergraduate/graduate level.
- **Ch 2 — Linear Algebra**: Systems of linear equations; matrices (addition, multiplication, inverse, transpose); vector spaces; linear independence; basis and rank; linear mappings; affine spaces.
- **Ch 3 — Analytic Geometry**: Norms; inner products; lengths and distances; angles and orthogonality; orthonormal basis; orthogonal projections; Gram-Schmidt process; rotations.
- **Ch 4 — Matrix Decompositions**: Determinant and trace; eigenvalues and eigenvectors; Cholesky decomposition; eigendecomposition/diagonalization; SVD; matrix approximation (Eckart-Young theorem); matrix phylogeny.
- **Ch 5 — Vector Calculus**: Differentiation of univariate functions; partial derivatives and gradients; Jacobians; gradients of matrices; backpropagation and automatic differentiation; Hessian; multivariate Taylor series.
- **Ch 6 — Probability and Distributions**: Probability space (sample space, event space, probability measure); discrete vs continuous; sum/product rules; Bayes' theorem; summary statistics; Gaussian distribution (marginals, conditionals, products); conjugacy and exponential family; change of variables/Jacobian.
- **Ch 7 — Continuous Optimization**: Gradient descent (batch, momentum, SGD); constrained optimization and Lagrange multipliers; convex optimization (linear programming, quadratic programming); KKT conditions.

**Part II: Central Machine Learning Problems**

- **Ch 8 — When Models Meet Data**: Data/models/learning formalized; empirical risk minimization; parameter estimation; probabilistic modeling; graphical models; model selection.
- **Ch 9 — Linear Regression**: Problem formulation; MLE parameter estimation (closed-form via pseudo-inverse); overfitting; MAP estimation with Gaussian prior (regularization); Bayesian linear regression; maximum likelihood as orthogonal projection.
- **Ch 10 — Dimensionality Reduction with PCA**: Maximum variance perspective; projection perspective; eigenvector computation; low-rank approximations (Eckart-Young); PCA in high dimensions (N x N covariance trick); key steps in practice; latent variable perspective (PPCA).
- **Ch 11 — Density Estimation with GMMs**: Gaussian mixture model definition; parameter learning via MLE; E-step (responsibilities) and M-step (mean/covariance/weight updates); EM algorithm; latent variable perspective.
- **Ch 12 — Classification with SVMs**: Separating hyperplanes; primal SVM (max-margin); margin derivation; dual SVM; soft-margin SVM (slack variables); kernels (polynomial, RBF); numerical solution.

## Key Pedagogical Choices

The book organizes ML through the lens of four pillars — regression, dimensionality reduction, density estimation, classification — each grounded in the Part I mathematics. Data is represented as vectors; models are learned by numerical optimization of an objective; the bridge is always explicit [^src1].

The book deliberately excludes deep learning, neural architectures, and probabilistic graphical models beyond basics, focusing instead on deriving the math of four canonical ML algorithms from first principles.

## Corpus Pages Produced

- [Linear Algebra for ML](/ai-engineering/linear-algebra-for-ml.md)
- [Matrix Decompositions](/ai-engineering/matrix-decompositions.md)
- [Probability and Statistics for ML](/ai-engineering/probability-and-statistics-for-ml.md)
- [Optimization for ML](/ai-engineering/optimization-for-ml.md)
- [PCA and Dimensionality Reduction](/ai-engineering/pca-and-dimensionality-reduction.md)
- [Gaussian Mixture Models](/ai-engineering/gaussian-mixture-models.md)
- [Support Vector Machines](/ai-engineering/support-vector-machines.md)
- [SVD](/ai-engineering/singular-value-decomposition.md) (pre-existing; cross-linked)

[^src1]: [Mathematics for Machine Learning, Part 1](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-01.md)
