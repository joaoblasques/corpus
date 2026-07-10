---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-08.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-09.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - logistic regression
  - LDA
  - QDA
  - linear discriminant analysis
  - quadratic discriminant analysis
  - k-nearest neighbors
  - classification
  - confusion matrix
  - ROC curve
  - AUC
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Classification assigns observations to discrete categories; the main methods are logistic regression (log-odds linear in X), LDA/QDA (Gaussian class-conditional distributions), and KNN (non-parametric majority vote); method choice depends on the linearity of the decision boundary and sample size.

## Overview

When the response Y is categorical (binary or multi-class), regression methods are inappropriate — they don't produce class probabilities and can predict outside [0,1]. Classification methods model Pr(Y=k|X) or directly model the decision boundary. ISL covers four classical methods in depth [^src1]:

1. Logistic regression
2. Linear discriminant analysis (LDA)
3. Quadratic discriminant analysis (QDA)
4. K-nearest neighbors (KNN)

## Logistic Regression

Models the **log-odds** (logit) of the outcome as a linear function of X:

```
log(p(X) / (1 - p(X))) = β₀ + β₁X₁ + ... + βₚXₚ
```

Equivalently, the probability of class 1:

```
p(X) = exp(β₀ + β₁X) / (1 + exp(β₀ + β₁X))   [sigmoid function]
```

The sigmoid ensures p(X) ∈ (0,1) for any linear combination of X [^src1].

**Fitting**: parameters are estimated via **maximum likelihood estimation (MLE)** — find β that maximizes the likelihood of the observed class labels. MLE is a more general approach than least squares; for linear regression, least squares is a special case of MLE [^src1].

**Interpretation**: A one-unit increase in Xⱼ changes the log-odds by βⱼ, or equivalently multiplies the odds by exp(βⱼ). Unlike linear regression coefficients, this effect is not additive on the probability scale.

**Multiple logistic regression**: straightforward extension to p predictors. Confounding is a real concern — a predictor that appears positively associated with Y in simple logistic regression can flip sign in multiple logistic regression (e.g., the student/default example: students appear riskier overall but are less risky *given the same credit card balance*) [^src1].

**Multi-class logistic regression**: extensions exist but LDA is often preferred for K > 2 classes.

## Linear Discriminant Analysis (LDA)

LDA takes a generative approach: model the class-conditional distribution of X|Y=k, then use Bayes' theorem to compute Pr(Y=k|X).

Assumptions:
- X|Y=k ~ N(μₖ, Σ) — each class has a Gaussian distribution with class-specific mean μₖ but **shared covariance matrix** Σ across all classes
- Class priors πₖ = Pr(Y=k) estimated from training data frequencies

Bayes' theorem gives the posterior:

```
Pr(Y=k|X=x) ∝ πₖ · f_k(x)
```

Under the shared-Σ assumption, this leads to **linear discriminant functions** — the decision boundary between classes k and l is a linear function of X. Classify to the class with highest discriminant score [^src1].

**Why LDA vs logistic regression?**
- LDA is more stable when classes are well separated (logistic MLE can diverge in that case)
- LDA uses all training data to estimate Σ (more efficient when normal assumption holds)
- LDA is natural for K > 2 classes (produces K-1 linear boundaries simultaneously)
- Logistic regression outperforms LDA when the normality assumption is violated

## Quadratic Discriminant Analysis (QDA)

Like LDA but allows **class-specific covariance matrices** Σₖ. This relaxes the shared-covariance assumption and produces **quadratic decision boundaries** [^src2].

- More flexible than LDA (lower bias, higher variance)
- Better when training n is large (enough to estimate Σₖ per class reliably) or when the true boundary is genuinely quadratic
- QDA requires estimating p(p+1)/2 parameters per class vs. LDA's single Σ; with p large and n small, QDA suffers

## K-Nearest Neighbors (KNN)

Fully non-parametric. For a test point x₀:
1. Find the K training points closest to x₀ (by Euclidean distance)
2. Predict the most common class among those K neighbors

```
Pr(Y=j|X=x₀) = (1/K) Σᵢ∈N₀ I(yᵢ = j)
```

- **K=1**: extremely flexible, zero training error, high variance — memorizes training data; the worst out-of-sample results in ISL's six scenarios
- **Large K**: smoother boundary, higher bias, lower variance
- K is chosen via cross-validation (see [Resampling Methods](/ai-engineering/resampling-methods.md))
- KNN is best when the true decision boundary is highly non-linear and n is large relative to p; degrades in high dimensions (curse of dimensionality) [^src2]

## Comparison of Methods

From ISL's six simulation scenarios [^src2]:

| Scenario | True boundary | Best method(s) |
|---|---|---|
| Gaussian, uncorrelated | Linear | LDA, logistic regression |
| Gaussian, correlated within class | Linear | LDA, logistic regression |
| t-distributed (heavier tails) | Linear | Logistic regression > LDA |
| Gaussian, different class covariances | Quadratic | QDA |
| Quadratic signal | Quadratic | QDA, KNN-CV |
| Complex non-linear | Complex | KNN-CV |

No method dominates all scenarios. Linear boundaries → LDA/logistic. Moderate non-linearity → QDA. Complex non-linearity + large n → KNN with CV-tuned K.

## Evaluating Classifiers

**Confusion matrix**: tabulates true positives (TP), true negatives (TN), false positives (FP), false negatives (FN). Derived metrics:

```
Sensitivity (recall) = TP / (TP + FN)   [true positive rate]
Specificity = TN / (TN + FP)            [true negative rate]
Precision = TP / (TP + FP)
Overall error rate = (FP + FN) / n
```

**ROC curve**: plots sensitivity (TPR) vs. 1-specificity (FPR) as the classification threshold varies from 0 to 1. A diagonal line = random classifier; the top-left corner = perfect.

**AUC** (area under the ROC curve): summarizes classifier performance across all thresholds. AUC = 1.0 is perfect; AUC = 0.5 is random. Allows comparison across classifiers without committing to a single threshold.

## See Also

- [Statistical Learning](/ai-engineering/statistical-learning.md) — supervised vs unsupervised, Bayes classifier, irreducible error
- [Resampling Methods](/ai-engineering/resampling-methods.md) — cross-validation for threshold and K selection
- [Support Vector Machines](/ai-engineering/support-vector-machines.md) — alternative approach to linear and non-linear classification
- [Tree-Based Methods](/ai-engineering/tree-based-methods.md) — non-parametric tree classifiers

[^src1]: [Introduction to Statistical Learning, Part 8](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-08.md)
[^src2]: [Introduction to Statistical Learning, Part 9](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-09.md)
