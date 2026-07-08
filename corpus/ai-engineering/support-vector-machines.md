---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-18.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - SVM
  - support vector machine
  - max-margin classifier
  - kernel SVM
  - soft-margin SVM
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Support Vector Machines

TL;DR: An SVM finds the maximum-margin hyperplane separating two classes. The margin is determined solely by the **support vectors** (boundary training points). The dual formulation introduces the kernel trick for nonlinear boundaries, and soft-margin SVMs handle non-separable data via slack variables.

## Separating Hyperplanes

For binary classification with labels y_n ∈ {+1, −1}, a hyperplane in R^D is {x : w^T x + b = 0}. A **separating hyperplane** satisfies [^src1]:

y_n (w^T x_n + b) ≥ 0 for all n

Many hyperplanes may separate the data — SVM selects the one with **maximum margin** (the widest "street" between the two classes).

## Primal SVM: Max-Margin Formulation

The margin between the two class boundaries {w^T x + b = +1} and {w^T x + b = −1} has width 2/||w||. Maximizing margin is equivalent to minimizing ||w|| [^src1]:

min_{w,b} (1/2) ||w||^2
subject to: y_n (w^T x_n + b) ≥ 1 for all n

This is a **quadratic program** (convex objective, linear constraints) — always has a unique global solution.

**Support vectors**: training points where y_n (w^T x_n + b) = 1 (i.e., on the margin boundary). The decision boundary depends only on these points — all other training points could be removed without changing w and b.

## Dual SVM

Applying Lagrange multipliers α_n ≥ 0 (one per constraint) and solving via KKT conditions yields the dual problem [^src1]:

max_{α} Σ_n α_n − (1/2) Σ_n Σ_m α_n α_m y_n y_m x_n^T x_m
subject to: α_n ≥ 0, Σ_n α_n y_n = 0

The dual depends only on **dot products x_n^T x_m** between training points — enabling the kernel trick. At the optimum, complementary slackness requires α_n = 0 for non-support-vectors.

The decision function becomes:
f(x) = sign(Σ_n α_n y_n x_n^T x + b)

where the sum runs only over support vectors (α_n > 0).

## Kernel Trick

Replace the dot product x_n^T x_m with a **kernel function** K(x_n, x_m) = φ(x_n)^T φ(x_m), where φ maps inputs to a (possibly infinite-dimensional) feature space. The kernel trick computes inner products in feature space without explicitly computing φ [^src1].

Common kernels:
- **Linear**: K(x,x') = x^T x' (standard SVM; D-dimensional)
- **Polynomial**: K(x,x') = (x^T x' + c)^p
- **RBF (Gaussian)**: K(x,x') = exp(−||x−x'||^2 / (2σ^2)) — infinite-dimensional feature space; universal approximator
- **String/graph kernels**: for discrete-structured inputs

A valid kernel must correspond to a positive semi-definite Gram matrix K_{nm} = K(x_n, x_m) (Mercer's theorem).

## Soft-Margin SVM

When data is not linearly separable (even in feature space), introduce **slack variables** ξ_n ≥ 0 allowing some misclassification [^src1]:

min_{w,b,ξ} (1/2)||w||^2 + C Σ_n ξ_n
subject to: y_n (w^T x_n + b) ≥ 1 − ξ_n, ξ_n ≥ 0 for all n

- ξ_n = 0: correctly classified with margin ≥ 1
- 0 < ξ_n ≤ 1: correctly classified but within the margin
- ξ_n > 1: misclassified

**C > 0**: regularization parameter trading off margin width vs. training errors.
- Large C: penalizes violations heavily → narrow margin, fewer training errors, risk of overfitting
- Small C: tolerates violations → wide margin, more training errors, better generalization

## Comparison to Logistic Regression

Both SVM and logistic regression learn a linear decision boundary w^T x + b = 0. Key differences [^src1]:

| Property | SVM | Logistic Regression |
|---|---|---|
| Objective | Max margin (hinge loss) | Max likelihood (log loss) |
| Support | Only boundary points matter | All points influence boundary |
| Calibration | No probability outputs | Outputs calibrated probabilities |
| Kernel extension | Natural via kernel trick | Less natural |
| Sparsity | Sparse (only support vectors) | Dense solution |

## Numerical Solution

The dual QP is solved with SMO (Sequential Minimal Optimization) or interior-point methods. SMO decomposes the problem into 2-variable subproblems with analytic solutions, scaling to large datasets. Libraries: scikit-learn wraps LIBSVM; `sklearn.svm.SVC` for classification, `SVR` for regression.

For the KKT conditions and Lagrangian duality theory underlying SVMs, see [Optimization for ML](/ai-engineering/optimization-for-ml.md).

[^src1]: [Mathematics for Machine Learning, Part 18](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-18.md)
