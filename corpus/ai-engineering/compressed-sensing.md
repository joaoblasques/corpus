---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-06.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-07.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - compressed sensing
  - compressive sensing
  - CS
  - sparse recovery
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Compressed Sensing

TL;DR: Compressed sensing (Candès, Romberg, Tao; Donoho; 2006) guarantees exact recovery of a sparse signal **s** from far fewer linear measurements **y** = **Cs** than the signal's ambient dimension — provided the signal is sparse in some basis **Ψ** and the measurement matrix **C** is incoherent with that basis.

## Core result

If a signal has only k nonzero entries in basis **Ψ** (k-sparse), it can be exactly recovered from O(k log(n/k)) measurements instead of the n measurements Shannon-Nyquist requires. Recovery is done via convex optimization (ℓ₁ minimization) [^src1]:

**ŝ** = argmin ||s||₁ subject to **y** = **Θs**

where **Θ** = **CΨ** is the sensing matrix and **y** are the compressive measurements.

## Key conditions

1. **Sparsity**: the signal has only k ≪ n significant coefficients in some basis **Ψ**
2. **Incoherence**: the measurement basis **C** must be "spread out" relative to the sparsity basis **Ψ** — random Gaussian or Bernoulli measurements satisfy this with high probability
3. **Restricted Isometry Property (RIP)**: the sensing matrix **Θ** approximately preserves the norm of all k-sparse vectors

## Sparsity basis choices

| Basis | When to use |
|---|---|
| Fourier (DCT) | Signals bandlimited or with few dominant frequencies |
| Wavelets | Natural images (piecewise smooth) |
| [SVD](/ai-engineering/singular-value-decomposition.md) modes | Data-adapted; optimal when the system's dominant subspace is known |
| Random | Theory-optimal; works when signal structure is unknown |

**Bad measurements**: measuring in the same basis as the sparsity basis (e.g., sampling the Fourier coefficients to recover a Fourier-sparse signal) loses information — the sensing matrix collapses [^src1].

## Sparse regression (ℓ₁ norm)

The ℓ₁ norm (rather than ℓ₂) promotes sparsity because the ℓ₁ unit ball has corners along the coordinate axes — optimizing under ℓ₁ constraints tends to produce solutions with many zeros. This makes ℓ₁ regression (LASSO) robust to outliers compared to ℓ₂ (least squares), which up-weights large deviations [^src1].

## Applications

- MRI acceleration: recover full-resolution MRI from ~8× fewer k-space samples (clinical translation)
- Single-pixel camera: 1 detector + random binary masks reconstructs full image
- Neuroscience: recover full neural population activity from few electrode recordings
- SINDy foundation: the sparse regression engine in [SINDy](/ai-engineering/sindy.md) is a compressed-sensing-style ℓ₁ recovery problem

[^src1]: [Data-Driven Science and Engineering](../../raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-06.md), Brunton & Kutz (2021), Chapter 3
