---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-16.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - Koopman operator
  - Koopman theory
  - Koopman eigenfunctions
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Koopman Operator Theory

TL;DR: The Koopman operator is an infinite-dimensional linear operator that acts on observable functions of the state space rather than the state itself. It lifts any nonlinear dynamical system to an equivalent (but infinite-dimensional) linear system, enabling linear analysis tools (eigendecomposition, spectral theory) to be applied to nonlinear dynamics.

## Core idea

For a nonlinear dynamical system **ẋ** = **f**(**x**), define observable functions g: ℝⁿ → ℝ. The Koopman operator **K** acts on observables:

(**Kg**)(**x**) = g(**f**(**x**))

The observable evolves linearly under **K**, even though **x** evolves nonlinearly under **f**. Koopman eigenfunctions φⱼ satisfy **Kφⱼ** = λⱼφⱼ — they capture the intrinsic oscillatory and decay modes of the nonlinear system [^src1].

## Connection to DMD

[Dynamic Mode Decomposition (DMD)](/ai-engineering/dynamic-mode-decomposition.md) computes a finite-dimensional approximation to the Koopman operator from data. When the DMD modes are computed using "exact DMD," they approximate Koopman eigenfunctions — which is why DMD can analyze nonlinear systems despite being a linear method [^src1].

## Practical challenge

Finding good Koopman eigenfunctions is the central challenge:
- For linear systems: the state coordinates **x** themselves are eigenfunctions — Koopman = standard linear analysis
- For nonlinear systems: must discover the right observable functions (features) in which the dynamics become linear
- Deep learning approach: train neural networks to find Koopman eigenfunctions (Lusch et al., 2018 — encoder/decoder + auxiliary network)

## Extended Dynamic Mode Decomposition (EDMD)

EDMD lifts the state **x** to a higher-dimensional feature space **ψ(x)** (e.g., polynomials, radial basis functions), then applies DMD in this lifted space. The choice of lifting functions determines approximation quality [^src1].

## Significance

Koopman theory provides the theoretical foundation explaining why linear methods (DMD, PCA — i.e. [SVD](/ai-engineering/singular-value-decomposition.md)) can successfully analyze nonlinear systems: they are implicitly discovering approximate Koopman eigenfunctions. This connects data-driven system identification to spectral operator theory [^src1].

[^src1]: [Data-Driven Science and Engineering](../../raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-16.md), Brunton & Kutz (2021), Chapter 7 (Koopman sections)
