---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-17.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-18.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-19.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-20.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-21.md
    channel: pdf
    ingested_at: 2026-07-17
aliases:
  - proximal gradient
  - ISTA
  - FISTA
  - iterative soft-thresholding
  - proximal operator
  - ADMM
  - alternating direction method of multipliers
  - augmented Lagrangian
  - ALM
  - Nesterov acceleration
  - accelerated proximal gradient
  - proximal point algorithm
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-17
updated: 2026-07-17
---

# Proximal Gradient Methods

TL;DR: Proximal gradient methods efficiently minimize composite objectives F(x) = f(x) + g(x) where f is smooth and g is convex but nonsmooth (e.g. ℓ₁ norm, nuclear norm). They replace the gradient step on g with a **proximal operator** — yielding convergence rates matching gradient descent on smooth functions. ISTA and FISTA are the canonical instances; ADMM extends this to separable structures.

## Motivation

Structured signal recovery problems (Lasso, nuclear norm minimization, PCP) have objective functions of the form F(x) = f(x) + g(x) where:
- f is smooth and convex (e.g. ½‖y − Ax‖₂²)
- g is convex but nonsmooth (e.g. λ‖x‖₁ or ‖X‖*)

Generic subgradient methods converge at O(1/√k) — too slow. Proximal gradient exploits that g, while nonsmooth, has a tractable proximal operator [^src1].

## The Proximal Operator

**Definition**: for a convex function g and scalar L > 0:

```
prox_{g/L}[w] = argmin_x { g(x) + (L/2)‖x − w‖₂² }
```

Minimizing g while staying close to w. Key instances [^src1]:

| g(x) | prox_{g/L}[w] |
|---|---|
| Indicator of convex set D | Projection onto D |
| λ‖x‖₁ | Soft-thresholding: sign(wᵢ)·max(|wᵢ| − λ/L, 0) element-wise |
| λ‖X‖* (nuclear norm) | Singular-value soft-thresholding: U·soft(Σ, λ/L)·V* |
| g₁(x₁) + g₂(x₂) (separable) | prox decomposes: [prox_{g₁}[w₁]; prox_{g₂}[w₂]] |

## Proximal Gradient (PG) / ISTA

Basic iteration for min F(x) = f(x) + g(x) with ∇f having Lipschitz constant L [^src1]:

```
w_k = x_k − (1/L) ∇f(x_k)       # gradient step on smooth part
x_{k+1} = prox_{g/L}[w_k]        # proximal step on nonsmooth part
```

**Convergence**: F(xₖ) − F(x*) ≤ (L/2)‖x₀ − x*‖²/k — rate O(1/k), same as gradient descent on smooth functions.

**ISTA** (Iterative Soft-Thresholding Algorithm) is PG applied to Lasso:
- ∇f(x) = A*(Ax − y), Lipschitz constant L = λ_max(A*A)
- prox step = element-wise soft-thresholding by λ/L

## Nesterov Acceleration (FISTA)

An optimal first-order method for this problem class achieves O(1/k²) [^src1]:

```
y_{k+1} = x_k + (t_k − 1)/t_{k+1} · (x_k − x_{k-1})   # momentum extrapolation
x_{k+1} = prox_{g/L}[y_{k+1} − (1/L)∇f(y_{k+1})]
t_{k+1} = (1 + √(1 + 4t_k²)) / 2                         # update momentum coefficient
```

**FISTA** = ISTA + Nesterov momentum. This is information-theoretically optimal for first-order methods on this function class. The momentum coefficient tₖ ≈ k/2 asymptotically.

## ADMM (Alternating Direction Method of Multipliers)

For problems with **separable structure**: min f(x) + g(z) s.t. Ax + Bz = c [^src2].

Augmented Lagrangian: L_ρ(x, z, y) = f(x) + g(z) + y*(Ax+Bz−c) + (ρ/2)‖Ax+Bz−c‖²

ADMM alternates [^src2]:
```
x_{k+1} = argmin_x L_ρ(x, z_k, y_k)    # x-update (often a prox step)
z_{k+1} = argmin_z L_ρ(x_{k+1}, z, y_k) # z-update (often a prox step)
y_{k+1} = y_k + ρ(Ax_{k+1} + Bz_{k+1} − c)  # dual update
```

**PCP via ADMM**: for Principal Component Pursuit min ‖L‖* + λ‖S‖₁ s.t. L + S = M,
- L-update: singular-value soft-thresholding
- S-update: element-wise soft-thresholding
- These decouple because the g terms are separable [^src2].

Convergence: O(1/k) for convex problems under mild conditions.

## Augmented Lagrangian Method (ALM)

For equality-constrained problems min f(x) s.t. Ax = b, the naive penalty method solves a sequence of min f(x) + (μ/2)‖Ax−b‖² with increasing μ — but conditioning degrades as μ → ∞. ALM incorporates a dual variable y to avoid this [^src2]:

```
x_{k+1} = argmin_x { f(x) + y_k*(Ax−b) + (ρ/2)‖Ax−b‖² }
y_{k+1} = y_k + ρ(Ax_{k+1} − b)
```

With fixed ρ, ALM converges to the optimal primal-dual pair without driving ρ → ∞.

## Connections

- Lasso and compressed sensing: [/ai-engineering/compressed-sensing.md](/ai-engineering/compressed-sensing.md) — ISTA is the canonical solver
- Low-rank recovery and PCP: [/ai-engineering/low-rank-matrix-recovery.md](/ai-engineering/low-rank-matrix-recovery.md) — nuclear-norm proximal = SVT
- General ML optimization: [/ai-engineering/optimization-for-ml.md](/ai-engineering/optimization-for-ml.md) — broader family of gradient/Newton methods
- Wright & Ma textbook: [/ai-engineering/sources/wright-ma-high-dimensional-data-analysis.md](/ai-engineering/sources/wright-ma-high-dimensional-data-analysis.md)

---

[^src1]: [HDLM Part 17–18 — Ch. 8 proximal gradient, ISTA, Nesterov acceleration, convergence proofs](../../raw/pdf/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-17.md)
[^src2]: [HDLM Part 19–21 — Ch. 8 ADMM, ALM, PCP via ADMM, OMP exercises](../../raw/pdf/pdf-high-dimensional-data-analysis-with-low-dimensiona-part-19.md)
