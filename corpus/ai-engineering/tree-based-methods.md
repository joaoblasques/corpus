---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-16.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-17.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - decision trees
  - CART
  - random forests
  - bagging
  - boosting
  - gradient boosting
  - XGBoost
  - AdaBoost
  - recursive binary splitting
  - ensemble methods
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Tree-based methods partition the predictor space into regions using recursive binary splits and predict by averaging (regression) or majority vote (classification); single trees are interpretable but weak — bagging, random forests, and boosting dramatically improve accuracy by combining many trees.

## Decision Trees (CART)

Tree-based methods **stratify the predictor space** into J non-overlapping rectangular regions R₁, ..., Rⱼ. For a test observation falling in region Rⱼ:
- Regression: predict ŷ = mean of training Y in Rⱼ
- Classification: predict the majority class in Rⱼ

The resulting decision rules can be displayed as a tree structure (internal nodes = splitting conditions, leaves = predictions), which makes trees highly interpretable [^src1].

### Recursive Binary Splitting

Trees are built via a **top-down, greedy** algorithm called recursive binary splitting [^src1]:

1. Consider all predictors X₁, ..., Xₚ and all possible split cutpoints s
2. For each candidate (j, s), define the two half-planes {X | Xⱼ < s} and {X | Xⱼ ≥ s}
3. Choose the (j, s) pair that minimizes the total weighted RSS:
```
Σ(yᵢ - ŷ_{R1})² + Σ(yᵢ - ŷ_{R2})²
```
4. Repeat, splitting one of the existing regions, until a stopping criterion (e.g., minimum leaf size) is reached

"Top-down" because the first split is on the whole space; "greedy" because each split is locally optimal without looking ahead. This means trees do not find the globally optimal partition.

### Impurity Measures for Classification Trees

For classification, instead of RSS, splits are evaluated using node impurity measures [^src1]:

- **Gini index**: G = Σ_{k} p̂_{mk}(1 - p̂_{mk}) — measures total variance across classes; small when node is pure
- **Cross-entropy (deviance)**: D = -Σ_{k} p̂_{mk} log(p̂_{mk}) — numerically similar to Gini; both preferred for growing trees
- **Classification error rate**: 1 - max_k(p̂_{mk}) — used for evaluating pruned tree performance, not for building

### Pruning (Cost Complexity Pruning)

Fully grown trees overfit. Better strategy: grow a very large tree T₀, then **prune back** [^src1]:

1. Grow T₀ using recursive binary splitting until terminal nodes are small
2. Apply cost complexity pruning: for each α ≥ 0, find the subtree T ⊆ T₀ that minimizes:
```
Σ_{m=1}^{|T|} Σ_{xᵢ∈Rₘ} (yᵢ - ŷ_{Rₘ})² + α|T|
```
   where |T| = number of terminal nodes. α is the complexity penalty — analogous to λ in lasso.
3. As α increases, branches are pruned in a nested sequence of subtrees
4. Use k-fold cross-validation to choose α; return the subtree for that α

At α=0: full tree T₀. As α increases: tree shrinks. Cross-validation identifies the α with best test performance.

### Advantages and Disadvantages of Single Trees

Advantages: interpretable, mirror human decision-making, handle qualitative predictors without dummies, no feature scaling needed.

Disadvantages: high variance (small changes in training data can produce very different trees), generally non-competitive with the best supervised learning methods. Ensemble methods fix the variance problem.

## Bagging (Bootstrap Aggregation)

**Bagging** reduces variance by averaging over many trees trained on bootstrap samples [^src1]:

1. Draw B bootstrap datasets from the training data (sampling with replacement; see [Resampling Methods](/ai-engineering/resampling-methods.md))
2. Fit a deep, unpruned tree on each bootstrap dataset: f̂*b(x)
3. Aggregate: for regression, average the B predictions; for classification, majority vote

```
f̂_bag(x) = (1/B) Σ_b f̂*b(x)
```

Bagging works because averaging reduces variance: Var(mean of B iid estimates) = Var(single estimate) / B. Trees have high variance but low bias — averaging many of them retains the low bias while slashing variance.

**Out-of-bag (OOB) error**: each bootstrap sample omits ~36.8% of training observations. These OOB observations can be used as a free test set to estimate test error without cross-validation. OOB error is a reliable and computationally cheap estimator of test performance [^src1].

**Variable importance** (bagging): for each predictor, sum the total RSS reduction (regression) or Gini decrease (classification) across all B trees and all splits on that predictor. Large values = important predictors [^src2].

## Random Forests

Random forests improve on bagging by **decorrelating the trees** [^src2]:

At each split, instead of considering all p predictors, randomly sample m < p candidate predictors and choose the best split among only those m.

Typical default: m ≈ √p for classification, m ≈ p/3 for regression.

**Why this helps**: if one predictor is dominant, bagged trees will all use it in their top split — their predictions become highly correlated, and averaging correlated quantities doesn't reduce variance as much as averaging uncorrelated ones. By randomly excluding the dominant predictor from many splits, other predictors get a chance. The trees are decorrelated, and the ensemble is more reliable [^src2].

When m = p, random forest reduces to bagging.

OOB error, variable importance, and aggregation mechanics are identical to bagging.

## Boosting

Boosting builds trees **sequentially**, with each tree fitting the residuals of the ensemble so far — it learns slowly rather than fitting hard [^src2]:

**Boosting Algorithm for Regression Trees** (Algorithm 8.2):
1. Initialize f̂(x) = 0, residuals rᵢ = yᵢ for all i
2. For b = 1, ..., B:
   a. Fit a small tree f̂ᵇ with d splits to the training data (X, r)
   b. Update: f̂(x) ← f̂(x) + λ f̂ᵇ(x)
   c. Update residuals: rᵢ ← rᵢ - λ f̂ᵇ(xᵢ)
3. Output f̂(x) = Σ_b λ f̂ᵇ(x)

**Three tuning parameters** [^src2]:
- **B** (number of trees): unlike bagging, boosting can overfit if B is too large (though slowly); select via cross-validation
- **λ** (shrinkage/learning rate): typically 0.01 or 0.001; smaller λ requires larger B but can yield better generalization
- **d** (interaction depth / number of splits per tree): controls complexity; d=1 produces stumps (additive model, each term involves one variable); d=2 allows pairwise interactions

**AdaBoost** (for classification): the original boosting algorithm, which up-weights misclassified observations at each round so subsequent trees focus on hard cases.

**Gradient Boosting**: a generalization of boosting in the framework of optimizing a differentiable loss function via gradient descent in function space. Residual fitting is a special case (squared error loss).

**XGBoost**: a highly optimized, regularized gradient boosting implementation. Adds L1/L2 regularization on tree weights, handles sparse data, supports parallel tree construction. Dominant in structured/tabular ML competitions. See [Regularization](/ai-engineering/regularization.md) for the penalty concepts.

**Key difference from bagging**: in boosting, each tree explicitly depends on all previously grown trees (fits residuals). In bagging, trees are grown independently on bootstrap samples. Boosting benefits from small trees (stumps often suffice); bagging typically uses fully grown trees.

## Comparison: Single Tree vs Ensemble Methods

| Method | Bias | Variance | Interpretability | Overfitting risk |
|---|---|---|---|---|
| Single decision tree | Low | High | High | High |
| Bagging | Low | Low | Low | Low |
| Random forest | Low | Lower than bagging | Low | Low |
| Boosting | Low | Low | Medium | Moderate (controlled by λ, B) |

## See Also

- [Statistical Learning](/ai-engineering/statistical-learning.md) — bias-variance tradeoff driving ensemble design
- [Resampling Methods](/ai-engineering/resampling-methods.md) — bootstrap underpins bagging; cross-validation selects α and B
- [Regularization](/ai-engineering/regularization.md) — cost complexity pruning parallels lasso; XGBoost adds regularization
- [Support Vector Machines](/ai-engineering/support-vector-machines.md) — alternative non-linear classification approach
- [Classification Methods](/ai-engineering/classification-methods.md) — logistic/LDA comparison for classification problems

[^src1]: [Introduction to Statistical Learning, Part 16](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-16.md)
[^src2]: [Introduction to Statistical Learning, Part 17](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-17.md)
