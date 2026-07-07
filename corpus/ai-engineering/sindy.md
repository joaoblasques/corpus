---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-15.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - SINDy
  - Sparse Identification of Nonlinear Dynamics
  - SINDYc
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# SINDy — Sparse Identification of Nonlinear Dynamics

TL;DR: SINDy (Brunton, Proctor, Kutz, 2016) discovers governing equations from time-series data by solving a sparse regression problem: the dynamics ẋ = f(x) is assumed to be a sparse combination of candidate library functions (polynomials, trig, etc.), and ℓ₁ optimization or sequential thresholding reveals which terms are active.

## Core idea

Many physical systems are governed by equations with only a few active terms (sparse in function space), even when the state space is high-dimensional. SINDy exploits this sparsity to go from data → equations [^src1].

Given state measurements **X** = [x₁, …, xₙ] and their time derivatives **Ẋ**:

1. Build a library **Θ(X)** of candidate functions: [1, x, x², x³, sin(x), cos(x), x·y, …]
2. Solve sparse regression: **Ẋ** = **Θ(X)Ξ** where **Ξ** is sparse
3. Each nonzero column of **Ξ** is an identified governing equation

**Algorithm**: Sequential Thresholded Least-Squares (STLS) — iteratively zero out small coefficients below threshold, refit on surviving terms [^src1].

## Canonical example

For the Lorenz system (ẋ = σ(y−x), ẏ = x(ρ−z)−y, ż = xy−βz), SINDy recovers the exact equations from noisy simulation data using only polynomial up to degree-2 terms in the library [^src1].

## Extensions

| Variant | Description |
|---|---|
| SINDYc | SINDy with control: identifies f(x, u) for controlled systems |
| Weak SINDy | Integral formulation; robust to noisy derivatives |
| SINDy-PI | Implicit formulation; handles algebraic constraints |
| PDE-FIND | Extension to partial differential equations (spatial derivatives in library) |

## Strengths and limitations

**Strengths**:
- Produces human-interpretable equations (not a black box)
- Works with very short time-series if signal is clean
- Library encodes domain knowledge (only physically plausible terms)

**Limitations**:
- Sensitive to measurement noise (derivatives must be estimated)
- Library must contain the true terms (expert knowledge required)
- Scales poorly with state dimension (library size grows combinatorially)

## Relationship to other methods

- Complements [DMD](/ai-engineering/dynamic-mode-decomposition.md): DMD finds linear dynamics; SINDy finds nonlinear sparse dynamics
- Enabled by [compressed sensing](/ai-engineering/compressed-sensing.md): the sparse regression machinery is the same as in compressed sensing
- Koopman connection: [Koopman operator theory](/ai-engineering/koopman-operator.md) provides a framework for when DMD and SINDy can be combined (Koopman-based SINDy for discovering observables)

[^src1]: [Data-Driven Science and Engineering](../../raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-15.md), Brunton & Kutz (2021), §7.3
