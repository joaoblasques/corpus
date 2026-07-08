---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-12.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - ridge regression
  - lasso
  - L1 regularization
  - L2 regularization
  - shrinkage methods
  - elastic net
  - penalized regression
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Regularization adds a penalty on coefficient magnitude to the least-squares loss, deliberately introducing bias to reduce variance and prevent overfitting; ridge uses an L2 penalty (shrinks toward zero), lasso uses L1 (forces some to exactly zero, enabling feature selection).

## Why Regularization

Ordinary least squares (OLS) minimizes the residual sum of squares (RSS) with no constraint on coefficient magnitude. When p is large relative to n — or when predictors are highly correlated — OLS estimates have high variance: small changes in training data cause large swings in coefficients. Regularization trades a small increase in bias for a large decrease in variance, often lowering test MSE substantially [^src1].

OLS fails entirely when p > n (no unique solution). Ridge and lasso both yield unique solutions for any λ > 0.

See [Statistical Learning](/ai-engineering/statistical-learning.md) for the bias-variance decomposition that motivates regularization.

## Ridge Regression (L2)

Ridge minimizes:

```
RSS + λ Σⱼ βⱼ²   (j = 1 to p)
```

The penalty λ ‖β‖₂² shrinks all coefficients toward zero as λ increases. Key properties [^src1]:

- **λ = 0**: reduces to OLS
- **λ → ∞**: all coefficients shrink to zero (null model)
- Coefficients are never set *exactly* to zero — ridge always retains all p predictors
- Predictors must be **standardized** first (subtract mean, divide by std dev); otherwise the penalty is scale-dependent and coefficients of different scales are penalized unequally
- Particularly effective when p ≫ n or when many predictors have small but non-zero true coefficients

**Bias-variance behavior**: As λ increases, flexibility decreases — variance drops, bias rises. The optimal λ sits at the bottom of the test MSE U-curve, typically found via cross-validation [^src1].

**Coefficient path diagram**: Plotting standardized ridge coefficients against λ (or against ‖β̂_λ‖₂ / ‖β̂‖₂) shows all coefficients smoothly shrinking toward zero as the penalty increases. Individual paths can cross or temporarily increase as other predictors are shrunk away.

## Lasso (L1)

Lasso minimizes:

```
RSS + λ Σⱼ |βⱼ|   (j = 1 to p)
```

The L1 penalty |βⱼ| has a geometric property that causes some coefficients to be forced to **exactly zero** at sufficiently large λ, unlike the L2 penalty which only asymptotically approaches zero [^src1]. This makes lasso a **variable selection** method — the resulting model uses only a subset of predictors.

Key properties:
- **Sparse models**: lasso output is far easier to interpret than ridge when p is large
- At small λ: similar to OLS (low shrinkage)
- At large λ: most coefficients zero'd out, only the most important predictors survive
- Lasso paths are piecewise linear (unlike smooth ridge paths); as λ decreases from large to small, variables enter the model one at a time
- Also requires standardized predictors

**When lasso outperforms ridge**: when the true signal is sparse (most true βⱼ = 0 or very small), lasso's ability to zero out noise predictors reduces variance dramatically.

**When ridge outperforms lasso**: when many predictors have roughly equal non-zero effects, ridge's smoother shrinkage performs better.

## Elastic Net

Elastic net combines both penalties:

```
RSS + λ₁ Σⱼ |βⱼ| + λ₂ Σⱼ βⱼ²
```

This allows grouping of correlated predictors (ridge behavior) while still achieving sparsity (lasso behavior). Commonly parameterized as a mixing parameter α ∈ [0,1] between pure ridge (α=0) and pure lasso (α=1) [^src1].

## Choosing Lambda via Cross-Validation

Neither λ is known in advance; it must be selected empirically:

1. Fit the model on training data for a grid of λ values (e.g., λ ∈ {0.001, 0.01, ..., 10000})
2. For each λ, compute the k-fold cross-validation error (see [Resampling Methods](/ai-engineering/resampling-methods.md))
3. Choose the λ that minimizes CV error — or, applying the **one-standard-error rule**, choose the largest λ whose CV error is within one standard error of the minimum (favoring simpler models)
4. Refit on the full training set using the chosen λ [^src1]

## Comparison: Ridge vs Lasso vs OLS

| Property | OLS | Ridge | Lasso |
|---|---|---|---|
| Penalty | None | L2: Σβⱼ² | L1: Σ|βⱼ| |
| Coefficients = 0? | Can be | Never (unless λ=∞) | Yes — feature selection |
| Works when p > n? | No | Yes | Yes |
| Interpretability | Moderate | Low (all vars included) | High (sparse) |
| Best when | True signal dense, low n | Many small effects | Sparse signal |

## Connection to Optimization

The lasso objective is equivalent to minimizing RSS subject to Σ|βⱼ| ≤ s, and ridge to minimizing RSS subject to Σβⱼ² ≤ s. The L1 constraint region has corners at coordinate axes, which is why lasso solutions lie at corners where some coefficients are exactly zero. The L2 constraint is a sphere, so solutions rarely land on axes. See [Optimization for ML](/ai-engineering/optimization-for-ml.md) for related geometric intuitions.

## See Also

- [Statistical Learning](/ai-engineering/statistical-learning.md) — bias-variance tradeoff motivation
- [Resampling Methods](/ai-engineering/resampling-methods.md) — cross-validation for λ selection
- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — constrained optimization geometry

[^src1]: [Introduction to Statistical Learning, Part 12](../../raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-12.md)
