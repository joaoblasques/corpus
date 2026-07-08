---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-18.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - GMM
  - Gaussian mixture model
  - mixture model
  - density estimation
  - EM algorithm
  - expectation maximization
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Gaussian Mixture Models

TL;DR: A GMM models a distribution as a weighted sum of K Gaussians. Parameters (mixing weights, means, covariances) are estimated via the EM algorithm — an E-step computing soft cluster assignments (responsibilities) and an M-step updating parameters by weighted MLE. EM monotonically increases the log-likelihood but converges only to a local optimum.

## Model Definition

A GMM defines a density over x ∈ R^D as [^src1]:

p(x) = Σ_{k=1}^K π_k N(x | μ_k, Σ_k)

Where:
- **π_k ∈ [0,1]**: mixing weights with Σ_k π_k = 1
- **μ_k ∈ R^D**: mean of the k-th Gaussian component
- **Σ_k ∈ R^{D×D}**: covariance matrix of the k-th component (symmetric positive definite)

The GMM is a **universal approximator** of smooth densities — any smooth density can be approximated to arbitrary precision with enough components.

## Latent Variable Interpretation

Introduce discrete latent variable z_n ∈ {1,...,K} indicating which component generated x_n:

p(z = k) = π_k    (prior on component assignment)
p(x | z = k) = N(x | μ_k, Σ_k)    (component-conditional density)

The marginal p(x) = Σ_k p(z=k) p(x|z=k) recovers the GMM density. The latent variable is unobserved — EM estimates parameters by treating z as a hidden variable [^src1].

## Parameter Learning via Maximum Likelihood

The log-likelihood of N i.i.d. observations is [^src1]:

ℓ(π, μ, Σ) = Σ_{n=1}^N log Σ_{k=1}^K π_k N(x_n | μ_k, Σ_k)

The sum inside the log makes direct MLE intractable — differentiating gives coupled nonlinear equations with no closed form. EM circumvents this by optimizing a lower bound.

## EM Algorithm

The EM algorithm alternates two steps until convergence [^src1]:

### E-step (Expectation): Compute Responsibilities

For each data point x_n and component k, compute the **responsibility** — the posterior probability that component k generated x_n:

r_{nk} = P(z=k | x_n) = π_k N(x_n | μ_k, Σ_k) / Σ_j π_j N(x_n | μ_j, Σ_j)

r_{nk} ≥ 0 and Σ_k r_{nk} = 1 for each n. The vector r_n = [r_{n1},...,r_{nK}] is a soft assignment distribution over components — as opposed to k-means' hard assignment.

### M-step (Maximization): Update Parameters

Given fixed responsibilities, update each parameter by weighted MLE:

**Means**:
μ_k^new = (1/N_k) Σ_n r_{nk} x_n

where N_k = Σ_n r_{nk} is the effective number of points assigned to component k. The new mean is a responsibility-weighted average of data points [^src1].

**Covariances**:
Σ_k^new = (1/N_k) Σ_n r_{nk} (x_n − μ_k^new)(x_n − μ_k^new)^T

**Mixing weights**:
π_k^new = N_k / N

### Convergence

EM monotonically increases the log-likelihood at each iteration: ℓ(θ^{t+1}) ≥ ℓ(θ^t). This follows from the EM lower bound (ELBO) argument: the E-step tightens the bound; the M-step maximizes it. The algorithm converges to a **stationary point** (local optimum) — not necessarily a global maximum.

## Relationship to K-Means

K-means is the hard-assignment limit of EM for GMMs [^src1]:
- Replace responsibilities r_{nk} ∈ [0,1] with hard assignments r_{nk} ∈ {0,1} (one-hot per data point)
- Assume spherical, equal covariances (Σ_k = σ^2 I) and equal mixing weights
- The M-step update for μ_k becomes the standard k-means centroid update

K-means is faster but less expressive — it cannot model elongated or differently sized clusters.

## Practical Considerations

**Initialization sensitivity**: EM converges to a local optimum; results depend on initialization. Common strategies:
- K-means++ initialization for initial means
- Multiple random restarts; keep the run with highest log-likelihood

**Degeneracy**: a component can "collapse" onto a single data point, driving its variance to zero and its log-likelihood to infinity. Regularize Σ_k by adding ε I (diagonal loading).

**Model selection**: the number of components K is a hyperparameter. Use BIC (Bayesian Information Criterion) or held-out likelihood to select K.

**Computational cost**: O(N K D^2) per EM iteration (dominated by covariance updates). For large D, use diagonal or tied covariances to reduce cost.

## Applications

- **Density estimation**: fit GMM to data, evaluate p(x) for new points
- **Soft clustering**: assign each point to the mixture component with highest responsibility
- **Generative models**: sample from the GMM by first sampling a component (π_k), then sampling from N(μ_k, Σ_k)
- **Anomaly detection**: flag points with low p(x) under the fitted GMM

[^src1]: [Mathematics for Machine Learning, Part 18](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-18.md)
