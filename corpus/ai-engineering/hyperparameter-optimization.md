---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-38.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-39.md
    channel: pdf
    ingested_at: 2026-07-11
aliases:
  - hyperparameter optimization
  - HPO
  - hyperparameter tuning
  - neural architecture search
  - NAS
  - Bayesian optimization
  - successive halving
  - random search
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-11
updated: 2026-07-11
---

# Hyperparameter Optimization (HPO)

**TL;DR**: Hyperparameters (learning rate, batch size, layer counts, dropout rate, regularization strength) cannot be learned by gradient descent — they must be set externally. HPO automates the search for good hyperparameter configurations [^src1].

## Why HPO is hard

Hyperparameter optimization cannot simply minimize training loss: setting dropout or weight decay to zero minimizes training loss but hurts generalization. Validation loss is the correct signal, but evaluating it requires training the model — each trial is expensive [^src1].

The standard loop: **Set Hyperparameters → Train → Evaluate on validation set → repeat until validation performance is maximized → Deploy** [^src1].

## Search strategies

| Strategy | Mechanism | When to use |
|---|---|---|
| **Grid search** | Exhaustively evaluate all combinations in a grid | Only viable with ≤2 hyperparameters; exponential in dimension |
| **Random search** | Sample configurations randomly | Strongly outperforms grid search in high dimensions (Bergstra & Bengio 2012) — most parameters have low influence; random search avoids wasting trials on redundant grid points |
| **Bayesian optimization** | Fit a surrogate model of val. loss over config space; use acquisition function to select next config | Fewer trials needed; useful for expensive evaluations |

## Multi-fidelity methods

Training a neural network to convergence for every candidate configuration is wasteful — most bad configurations fail early. Multi-fidelity methods use cheap approximations to screen out bad configs:

**Successive Halving (SHA)**: given a budget of *n* configurations and *r_max* max epochs [^src2]:
1. Evaluate all *n* configs for *r_min* epochs (cheapest rung).
2. Keep the top 1/η fraction; train them for *r_min × η* epochs.
3. Repeat, halving the set and multiplying epochs by η, until one configuration trains fully.

The D2L implementation uses `SuccessiveHalvingScheduler` with rung levels `{r_min, r_min×η, ..., r_max}`. Configurations are promoted to the next rung only if they are in the top 1/η on the current rung [^src2].

**ASHA** (Asynchronous SHA): runs SHA asynchronously across parallel workers — no idle waiting at rung boundaries.

**Hyperband**: wraps SHA with multiple brackets varying *n* and *r_min* to hedge between few-full-training vs. many-short-training strategies.

## Neural Architecture Search (NAS)

NAS automates the search over neural network architectures (number of layers, layer types, skip connections). Methods range from reinforcement learning (train a controller that generates architecture descriptions) to differentiable NAS (DARTS — relax discrete architecture choices into continuous weights and optimize jointly) [^src1].

## Practical guidance

- Start with random search over the most sensitive hyperparameters (learning rate is almost always #1).
- Use successive halving as soon as you can tell relative ordering of configs early in training.
- Learning rate and batch size interact: larger batch often requires proportionally larger learning rate (linear scaling rule).

## Connections to other corpus pages

- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — SGD learning rate, momentum, and batch size are the most impactful HPO targets.
- [Regularization](/ai-engineering/regularization.md) — dropout rate and weight decay λ are key hyperparameters.
- [Resampling Methods](/ai-engineering/resampling-methods.md) — k-fold cross-validation for HPO; trade-off between expensive k-fold and cheap single-split validation.

---

[^src1]: [D2L Part 38 — Hyperparameter Optimization (overview, random search)](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-38.md)
[^src2]: [D2L Part 39 — Successive Halving Scheduler](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-39.md)
