---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-10.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-11.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - cross-validation
  - bootstrap
  - k-fold cross-validation
  - LOOCV
  - leave-one-out cross-validation
  - validation set
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Resampling methods estimate test error by repeatedly fitting models on subsets of training data; cross-validation finds the best model/flexibility level, bootstrap estimates parameter uncertainty — both without requiring a separate test set.

## Purpose

Resampling methods involve repeatedly drawing samples from a training set, refitting a model on each sample, and examining the variation across fits to gain information unavailable from a single fit. The two main uses [^src1]:

- **Model assessment** (cross-validation): estimate how well a model will generalize to new data
- **Parameter uncertainty** (bootstrap): estimate standard errors and confidence intervals for parameter estimates

## Validation Set Approach

The simplest strategy: randomly split n observations into a **training set** and a **validation set** (hold-out set). Fit on training, evaluate MSE on validation.

Drawbacks [^src1]:
1. High variability — different random splits produce substantially different test MSE estimates; no consensus on optimal model complexity
2. Overestimates test error — training set is typically ~half the data, so the model is fit with fewer observations than it would be in practice, inflating apparent error

## Leave-One-Out Cross-Validation (LOOCV)

Train on n−1 observations, evaluate on the 1 held-out observation; repeat n times, each time holding out a different observation. Final estimate [^src1]:

```
CV(n) = (1/n) Σᵢ MSEᵢ
```

Advantages over validation set:
- Far less bias: training sets are nearly the full data (n−1 vs ~n/2)
- No randomness: LOOCV always produces the same result

Disadvantage: high variance because the n model fits are trained on nearly identical datasets — their outputs are highly correlated. For linear/polynomial models, LOOCV has a shortcut formula:

```
CV(n) = (1/n) Σᵢ [(yᵢ - ŷᵢ) / (1 - hᵢ)]²
```

where hᵢ is the leverage of the i-th observation. This makes LOOCV computationally cheap for OLS [^src1].

## k-Fold Cross-Validation

Randomly divide observations into k equal-sized folds. Hold out fold j as validation, train on remaining k−1 folds. Repeat for j = 1, ..., k. Average the k MSEs [^src1]:

```
CV(k) = (1/k) Σⱼ MSEⱼ
```

Typical choices: k = 5 or k = 10.

**Bias-variance tradeoff for k-fold CV** [^src1]:
- LOOCV (k=n): low bias, high variance (all n models trained on nearly identical data → highly correlated outputs → mean of correlated quantities has high variance)
- Validation set (k=2): high bias, low variance
- k=5 or k=10: intermediate bias, lower variance than LOOCV — empirically the best balance

The shape of the CV curve (test MSE vs flexibility) is more important than the absolute value: the minimum of the curve identifies the best model complexity even when the CV error underestimates the true test error.

**Classification setting**: replace MSE with misclassification rate in each fold [^src1].

## One-Standard-Error Rule

When selecting among models (e.g., choosing λ in lasso, or polynomial degree), the one-standard-error rule says: among all models within one SE of the minimum CV error, choose the simplest (largest λ / lowest flexibility). This guards against overfitting to the idiosyncrasies of the CV splits [^src1].

## Bootstrap

The bootstrap estimates the variability of a statistic or model parameter by **sampling with replacement** from the training data. For B bootstrap samples [^src2]:

1. Draw a bootstrap dataset Z* of size n from Z by sampling with replacement
2. Compute the statistic of interest (e.g., β̂, prediction) on Z*
3. Repeat B times to get B estimates {α̂₁*, ..., α̂_B*}
4. Estimate SE: `SE_B(α̂) = sqrt[ (1/(B-1)) Σ_b (α̂_b* - ᾱ*)² ]`

Because we sample with replacement, each bootstrap dataset omits ~36.8% of original observations on average (probability an observation is not drawn in one trial = (1-1/n)^n → 1/e ≈ 0.368 as n→∞) [^src2].

**Key advantage over analytic standard errors**: bootstrap doesn't rely on model assumptions (such as the linear model being correct or errors being homoscedastic). When the model is misspecified, bootstrap SEs can be more accurate than formula-derived SEs [^src2].

**Bootstrap CI**: percentile method — take the 2.5th and 97.5th percentiles of the B bootstrap estimates. More robust alternatives: BCa (bias-corrected and accelerated).

**Limitation**: bootstrap cannot fix high-bias estimators and can underestimate uncertainty when the original sample itself is non-representative.

## Comparing Methods

| Method | Bias | Variance | Cost | Notes |
|---|---|---|---|---|
| Validation set | High | Low | 1 fit | High variability across splits |
| LOOCV | Low | High | n fits | Shortcut for OLS |
| k-fold CV (k=5/10) | Medium | Medium | k fits | Standard choice |
| Bootstrap | — | — | B fits | Standard errors, CIs |

## See Also

- [Statistical Learning](/ai-engineering/statistical-learning.md) — training vs test error, why estimation matters
- [Regularization](/ai-engineering/regularization.md) — cross-validation is the standard way to choose λ
- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — model fitting procedure repeated per fold/sample

[^src1]: [Introduction to Statistical Learning, Part 10](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-10.md)
[^src2]: [Introduction to Statistical Learning, Part 11](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-11.md)
