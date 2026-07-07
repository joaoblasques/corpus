---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-14.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-15.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - DMD
  - Dynamic Mode Decomposition
  - mrDMD
  - multi-resolution DMD
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Dynamic Mode Decomposition (DMD)

TL;DR: DMD computes a best-fit linear operator **A** from sequential data snapshots (**X** → **X**') such that **X**' ≈ **A** **X**. The eigendecomposition of **A** yields spatial-temporal modes (DMD modes) — each with a frequency and growth/decay rate — without requiring knowledge of the governing equations.

## Core algorithm

Given data matrix **X** = [x₁, x₂, …, xₙ] and shifted matrix **X**' = [x₂, x₃, …, x_{n+1}]:

1. Compute SVD: **X** = **UΣV***
2. Project: **Ã** = **U*****X**'**VΣ**⁻¹ (low-dimensional surrogate for **A**)
3. Eigendecompose **Ã**: **ÃW** = **WΛ**
4. DMD modes: **Φ** = **X**'**VΣ**⁻¹**W**

Each DMD mode φⱼ oscillates at frequency ω_j = Im(log(λⱼ))/Δt and grows/decays at rate Re(log(λⱼ))/Δt [^src1].

## Key properties

- **Equation-free**: only needs time-series measurements, no model knowledge
- **Connects to Koopman theory**: exact DMD modes are eigenfunctions of the Koopman operator (see [Koopman Operator](/ai-engineering/koopman-operator.md)) when the system is linear, and approximate them for weakly nonlinear systems
- **Spatio-temporal coherence**: unlike FFT (frequency only) or SVD (spatial structure only), DMD extracts coupled spatial-frequency patterns
- **Limitation**: fundamentally linear; struggles with strong nonlinearity, traveling waves, broadband spectra, and transients [^src1]

## Applications

| Domain | Use |
|---|---|
| Fluid dynamics | Background subtraction in turbulence; coherent structure identification |
| Video processing | Background/foreground separation in surveillance video |
| Neuroscience | Spatiotemporal neural activity modes |
| Finance | Extracting oscillatory market modes |
| Plasma physics | Mode analysis |

## Variants

- **Exact DMD**: uses both **X** and **X**' in mode computation (recommended over "standard" DMD)
- **Optimized DMD (opt-DMD)**: minimizes reconstruction error without assuming uniform sampling
- **Multi-resolution DMD (mrDMD)**: multi-scale analysis; separates slow/fast dynamics
- **Compressed DMD**: DMD from random projections; handles high-dimensional data
- **Hankel-DMD (HAVOK)**: embeds delay coordinates before DMD; handles chaotic systems (e.g., Lorenz) via a "forcing" interpretation

## Relationship to SINDy

DMD produces the best-fit **linear** operator; [SINDy](/ai-engineering/sindy.md) discovers the best-fit **nonlinear** sparse governing equation. For many systems, DMD is the first diagnostic; SINDy is the next step when the system is clearly nonlinear [^src1].

[^src1]: [Data-Driven Science and Engineering](../../raw/pdf/pdf-brunton-kutz-data-driven-science-and-engineering-v2-author-f-part-14.md), Brunton & Kutz (2021), Chapter 7
