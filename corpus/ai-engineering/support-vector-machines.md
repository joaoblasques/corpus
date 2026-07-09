---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-19.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-19.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - SVM
  - support vector machine
  - maximum margin classifier
  - kernel methods
  - soft margin SVM
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Support Vector Machines

TL;DR: SVMs find the maximum-margin separating hyperplane between two classes. The margin — distance from hyperplane to nearest training points — measures classifier robustness; maximizing it leads to a convex QP. The dual SVM reformulation involves only inner products between training points, enabling the kernel trick to extend SVMs to nonlinear boundaries without explicitly mapping to high-dimensional feature space. Soft-margin SVMs allow misclassification with a penalty C that trades off margin size against training error.

## Binary Classification Setup

Given training set {(x_1, y_1), ..., (x_N, y_N)} where x_n in R^D and y_n in {-1, +1} [^src1].

Goal: find a function f: R^D → {-1, +1} that correctly classifies unseen data.

**Separating hyperplane**: defined by weights w in R^D and bias b in R:

```
<w, x> + b = 0
```

A point x is classified as:
- positive: <w, x> + b > 0
- negative: <w, x> + b < 0

**Linear classifier**: f(x) = sign(<w, x> + b).

When data is **linearly separable**, infinitely many hyperplanes separate the classes (Figure 12.3 in MML). SVMs choose the unique one that maximizes the margin [^src1].

## Concept of Margin

The **margin** is the distance from the separating hyperplane to the closest training examples (support vectors) [^src1].

For a point x_a on the positive side, its distance to the hyperplane is [^src1]:

```
r = <w/||w||, x_a> + b/||w||
```

The convention: parameterize so ||w|| = 1 (unit-norm weight vector). Then r is directly the geometric distance.

**Margin = 2r**: there is a margin r on each side of the hyperplane, so total margin width is 2r.

**Intuition for maximizing margin**: classifiers with larger margins tend to generalize better. A point that must be misclassified needs to cross the entire margin, so larger margins are more robust to perturbations.

## Hard-Margin SVM (Primal)

**Primal formulation**: find w, b to maximize margin subject to correct classification [^src1]:

```
max_{w, b}  r
subject to: y_n (<w, x_n> + b) >= r    for all n = 1, ..., N
            ||w|| = 1
```

**Equivalent reformulation** (standard form): rescale so margin endpoints satisfy y_n (<w, x_n> + b) = 1. Then the margin is 2/||w||. Maximizing margin = minimizing ||w||:

```
min_{w, b}  (1/2) ||w||^2
subject to: y_n (<w, x_n> + b) >= 1    for all n = 1, ..., N
```

This is a **convex QP** (quadratic objective, linear constraints). Unique global solution [^src1].

**Support vectors**: training points that achieve y_n (<w, x_n> + b) = 1, i.e., lie exactly on the margin boundary. They are the critical points — removing non-support vectors doesn't change the solution.

## Dual SVM

The dual of the hard-margin primal involves Lagrange multipliers alpha_n >= 0 (one per training point) [^src1]:

```
max_{alpha}  sum_n alpha_n - (1/2) sum_{n,m} alpha_n alpha_m y_n y_m <x_n, x_m>
subject to:  sum_n alpha_n y_n = 0
             alpha_n >= 0
```

**KKT conditions** (complementary slackness):
- alpha_n (y_n (<w, x_n> + b) - 1) = 0  for all n
- alpha_n >= 0
- Either alpha_n = 0 (non-support vector) or y_n (<w, x_n> + b) = 1 (support vector)

**Recovering the primal from dual**:

```
w* = sum_n alpha_n y_n x_n    (w is a linear combination of support vectors)
b* = y_n - <w*, x_n>          (for any support vector x_n)
```

**Prediction**: f(x) = sign(<w*, x> + b*) = sign(sum_n alpha_n y_n <x_n, x> + b*).

**Critical observation**: both the dual objective and prediction involve only **inner products** <x_n, x_m> between training points. This enables the kernel trick [^src1].

## Soft-Margin SVM

**Problem**: if data is not linearly separable, the hard-margin SVM has no feasible solution.

**Soft-margin SVM** introduces slack variables xi_n >= 0 to allow constraint violations [^src1]:

```
min_{w, b, xi}  (1/2) ||w||^2 + C sum_n xi_n
subject to:  y_n (<w, x_n> + b) >= 1 - xi_n    for all n
             xi_n >= 0
```

**Interpretation**:
- xi_n = 0: point correctly classified outside margin
- 0 < xi_n <= 1: point correctly classified inside margin
- xi_n > 1: point misclassified

**Hyperparameter C** controls the tradeoff:
- Large C: small xi_n → hard margin (few violations, may overfit)
- Small C: large xi_n → soft margin (many violations allowed, more regularization)

The soft-margin SVM is also a convex QP. Its dual has the same form as the hard-margin dual but with additional box constraints: 0 <= alpha_n <= C [^src1].

## Kernel Trick

**Motivation**: linear SVMs cannot classify non-linearly separable data. Solution: map x → phi(x) to a high-dimensional feature space where data becomes separable, then train a linear SVM there [^src1].

**Kernel function**: k(x_i, x_j) = <phi(x_i), phi(x_j)>. The kernel computes the inner product in feature space without explicitly computing phi.

**Dual SVM with kernels** — replace all inner products:

```
max_{alpha}  sum_n alpha_n - (1/2) sum_{n,m} alpha_n alpha_m y_n y_m k(x_n, x_m)
```

**Common kernels**:
- **Linear**: k(x, x') = <x, x'>  (recovers standard SVM)
- **Polynomial**: k(x, x') = (<x, x'> + c)^d
- **RBF (Gaussian)**: k(x, x') = exp(-gamma ||x - x'||^2). Maps to infinite-dimensional feature space; very flexible.
- **Sigmoid**: k(x, x') = tanh(kappa <x, x'> + c)

**Mercer's condition**: a function k is a valid kernel iff the corresponding Gram matrix K (with K_{ij} = k(x_i, x_j)) is symmetric positive semidefinite for any set of inputs [^src1].

## Numerical Solution

SVMs are solved as QPs using specialized solvers [^src1]:
- **Sequential minimal optimization (SMO)**: breaks the QP into 2-variable subproblems, each with closed-form solution. Standard algorithm in `libsvm` and `sklearn.svm`.
- **Pegasos**: stochastic sub-gradient method for large-scale SVMs.
- **Cutting plane**: efficient for structured SVMs.

**Computational complexity**:
- Training: O(N^2) to O(N^3) depending on kernel and solver
- Prediction: O(N_sv * D) where N_sv = number of support vectors (often small fraction of N)

## SVM vs. Logistic Regression

| | SVM | Logistic Regression |
|---|---|---|
| Loss | Hinge loss: max(0, 1 - y f(x)) | Log-loss: log(1 + exp(-y f(x))) |
| Sparsity | Sparse: only support vectors matter | Dense: all training points influence w |
| Probability output | Not directly (calibration needed) | Natural probability output |
| Non-linearity | Kernel trick | Feature engineering or deep features |
| Scalability | Slow for large N | Efficient (SGD) |
| Margin concept | Explicit maximum margin | Implicit via loss function |

## Mathematical Connections

- SVMs as regularized risk minimization: minimize (1/N) sum_n hinge_loss(x_n, y_n) + lambda ||w||^2
- Relationship to Ridge regression: same form, different loss function
- Connection to deep learning: neural nets can be seen as learning the feature map phi that SVMs then classify over

## SVM in Practice (R Lab, ISL Ch. 9)

**Radial kernel.** For non-linearly separable data, a radial (RBF) kernel `exp(-gamma * ||x-x'||^2)` with cross-validated cost and gamma produces a non-linear decision boundary. ISL example: gamma=2, cost=1 achieves 10% test error on a 100-obs simulated set [^src2].

**Hyperparameter selection.** Use `tune()` (R e1071 package) with cross-validation over a grid of cost and gamma values. ISL tip: large cost with radial kernel risks overfitting; optimal parameters often have moderate cost [^src2].

**ROC curves.** Obtain fitted values via `decision.values=TRUE` in the `svm()` call, then pass to ROCR's `prediction()`/`performance()`. Comparing train vs. test ROC curves detects overfitting; a more flexible model (higher gamma) may improve train-ROC but worsen test-ROC [^src2].

**Multi-class SVMs.** When the response has >2 levels, `svm()` uses **one-versus-one** classification: it fits C(K,2) binary SVMs and assigns the class that wins the most pairwise contests [^src2].

**High-p, low-n setting.** When p >> n (e.g., gene expression data with 2308 genes, 63 training samples), a **linear kernel** is preferred — additional flexibility from non-linear kernels is unnecessary and risks overfitting. ISL Khan dataset: linear SVM achieves zero training error and 2 test errors out of 20 observations [^src2].

## Related Corpus Pages

- [/ai-engineering/optimization-for-ml.md](/ai-engineering/optimization-for-ml.md) — convex QP; KKT conditions; Lagrange multipliers; duality
- [/ai-engineering/linear-algebra-for-ml.md](/ai-engineering/linear-algebra-for-ml.md) — inner products; orthogonal projections; hyperplanes
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — probability perspective on classification
- [/ai-engineering/classification-methods.md](/ai-engineering/classification-methods.md) — logistic regression; LDA; KNN; ROC/AUC
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — full book summary
- [/ai-engineering/sources/introduction-to-statistical-learning.md](/ai-engineering/sources/introduction-to-statistical-learning.md) — ISL book summary

---

[^src1]: [Mathematics for Machine Learning, Part 19](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-19.md)
[^src2]: [Introduction to Statistical Learning, Part 19](../../raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-19.md)
