---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-12.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - gradient descent
  - continuous optimization
  - convex optimization
  - stochastic gradient descent
  - SGD
  - Lagrange multipliers
  - KKT conditions
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: ML training reduces to minimizing a loss function; gradient descent is the workhorse (batch, mini-batch, stochastic variants); constrained problems use Lagrange multipliers / KKT; convexity guarantees global optima.

## Gradient Descent

To find a local minimum of f: R^n → R, start at x_0 and iterate [^src1]:

x_{i+1} = x_i − α ∇_x f(x_i)

The gradient ∇f points toward steepest ascent, so subtracting it moves toward a local minimum. The **step size** (learning rate) α controls convergence:
- Too small → slow convergence
- Too large → overshooting or divergence
- Adaptive schedules (e.g., learning rate decay) are commonly used in practice

Gradient descent converges to a stationary point (∇f = 0) but may be a saddle point or local minimum, not necessarily global. Convergence near minima can be slow ("zigzagging" in ill-conditioned landscapes) [^src1].

## Gradient Descent with Momentum

Standard gradient descent oscillates in narrow valleys. **Momentum** introduces memory of the previous update [^src1]:

∆x_i = α ∇_x f(x_{i-1}) + β ∆x_{i-1}

with β ∈ [0,1]. The momentum term β ∆x_{i-1} acts like a moving average of gradients, dampening oscillations and accelerating convergence in consistent descent directions.

## Stochastic and Mini-Batch Gradient Descent

**Batch gradient descent** uses the full training set to compute each gradient update — expensive for large datasets.

**Stochastic gradient descent (SGD)** uses a single randomly sampled data point per update: noisy but cheap. The noise can help escape local minima [^src1].

**Mini-batch SGD** uses a small random subset (batch size B) — the practical standard. Benefits:
- Vectorized computation (GPU efficiency)
- Lower variance than pure SGD
- Can escape sharp local minima

SGD with decreasing learning rate converges almost surely to a local minimum under mild assumptions (Bottou, 1998) [^src1].

## Newton's Method

Uses second-order (curvature) information via the Hessian H = ∇^2 f:

x_{i+1} = x_i − H^{-1} ∇f(x_i)

Converges much faster than gradient descent near the optimum (quadratic vs. linear convergence rate) but requires computing and inverting the Hessian (O(n^3) cost). Quasi-Newton methods (BFGS, L-BFGS) approximate H^{-1} without full computation.

## Constrained Optimization and Lagrange Multipliers

For the problem min_x f(x) subject to g(x) = 0, the **Lagrangian** is [^src2]:

L(x, λ) = f(x) + λ g(x)

At an optimum, ∂L/∂x = 0 and ∂L/∂λ = 0. The scalar λ is the **Lagrange multiplier** — it encodes how much the constraint is "costing" the objective.

For inequality constraints g(x) ≤ 0, the Lagrangian is L(x, λ) = f(x) + λ g(x) with λ ≥ 0 (KKT conditions below).

## KKT Conditions

For the general constrained problem min_x f(x) subject to g_i(x) ≤ 0, h_j(x) = 0, the **Karush-Kuhn-Tucker (KKT) conditions** are necessary (and sufficient for convex problems):

1. Stationarity: ∇_x L = 0
2. Primal feasibility: g_i(x*) ≤ 0, h_j(x*) = 0
3. Dual feasibility: λ_i ≥ 0
4. Complementary slackness: λ_i g_i(x*) = 0 for all i

Complementary slackness says each constraint is either active (g_i = 0) or its multiplier is zero. KKT conditions are central to SVM derivation — see [Support Vector Machines](/ai-engineering/support-vector-machines.md).

## Convex Optimization

A function f is **convex** if for all x,y and θ ∈ [0,1] [^src2]:

f(θx + (1−θ)y) ≤ θf(x) + (1−θ)f(y)

Equivalently (when twice differentiable): the Hessian ∇^2 f(x) is positive semi-definite everywhere. Convex functions have no local minima that are not global — a critical property for reliable optimization.

A **convex optimization problem** has a convex objective and convex inequality constraints (and linear equality constraints). For convex problems: every local minimum is a global minimum; KKT conditions are sufficient; duality gap is zero (strong duality).

**Linear programming**: convex objective and constraints both linear; solved in polynomial time via simplex or interior point methods.

**Quadratic programming**: quadratic convex objective with linear constraints. Arises in SVM training (dual formulation).

## Primal-Dual Duality

The **dual problem** of min_x f(x) s.t. g(x) ≤ 0 is max_λ D(λ) where D(λ) = min_x L(x, λ). The dual is always convex regardless of the primal. Under strong duality (Slater's condition for convex problems), the primal and dual optima coincide — enabling the dual formulation of SVMs which is often easier to solve [^src2].

[^src1]: [Mathematics for Machine Learning, Part 11](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md)
[^src2]: [Mathematics for Machine Learning, Part 12](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-12.md)
