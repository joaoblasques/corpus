---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-08.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-10.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - probability theory
  - probabilistic ML
  - Bayesian inference
  - probability distributions
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Probability theory formalizes uncertainty in data and models; key tools are Bayes' theorem (updating beliefs), the Gaussian distribution (with closed-form marginals/conditionals), and the exponential family (conjugate priors enabling tractable inference).

## Probability Space

A probability space is a triple (Ω, A, P): **sample space** Ω (all outcomes), **event space** A (subsets of Ω we can assign probability to), and **probability measure** P (P: A → [0,1] with P(Ω) = 1) [^src1].

A **random variable** X: Ω → T is a function from outcomes to a target space T (often R^n). The distribution P_X is the induced probability on T. "Random variable" is a function, not a variable [^src1].

## Sum Rule, Product Rule, Bayes' Theorem

- **Sum rule** (marginalization): p(x) = ∫ p(x,y) dy — integrate out unwanted variables
- **Product rule**: p(x,y) = p(x|y)p(y) = p(y|x)p(x)
- **Bayes' theorem**: p(θ|data) = p(data|θ)p(θ) / p(data)

Bayes' theorem is the engine of probabilistic ML: posterior = likelihood × prior / evidence. The denominator p(data) is a normalizing constant, often intractable, which motivates variational inference and MCMC [^src1].

## Summary Statistics

**Mean/Expectation**: E[x] = ∫ x p(x) dx (continuous); the "center of mass" of the distribution.

**Variance**: Var[x] = E[(x − E[x])^2] = E[x^2] − (E[x])^2; measures spread.

**Covariance matrix** (multivariate): Σ = E[(x − μ)(x − μ)^T]; always symmetric, positive semi-definite. Off-diagonal entries Σ_{ij} = Cov[x_i, x_j] measure linear co-variation.

**Correlation**: ρ(X,Y) = Cov[X,Y] / (std(X) std(Y)) ∈ [−1, 1]. Geometrically, correlation is the cosine of the angle between two random variables viewed as vectors in an inner-product space [^src2].

## Common Distributions

**Gaussian (Normal)**: N(μ, Σ) with density p(x) ∝ exp(−½(x−μ)^T Σ^{-1} (x−μ)). Arises as the limit of sums of i.i.d. random variables (central limit theorem). Key properties:
- Marginals of a joint Gaussian are Gaussian: p(x) = N(μ_x, Σ_{xx})
- Conditionals of a joint Gaussian are Gaussian: p(x|y) = N(μ_{x|y}, Σ_{x|y}) with closed-form parameters
- Product of two Gaussians is a scaled Gaussian: N(x|a,A) N(x|b,B) = c N(x|c,C) [^src2]

**Bernoulli**: Ber(μ) for binary outcomes; p(x=1) = μ.

**Beta**: Beta(α,β) for μ ∈ [0,1]; conjugate prior for Bernoulli likelihood. Shape controlled by α,β.

**Dirichlet**: Dir(α) generalizes Beta to K-dimensional probability vectors; conjugate prior for categorical/multinomial.

**Binomial**: Bin(N,μ); counts of successes in N Bernoulli trials.

## Exponential Family and Conjugate Priors

The **exponential family** of distributions has density p(x|η) = h(x) exp(η^T φ(x) − A(η)) where η are natural parameters, φ(x) are sufficient statistics, and A(η) is the log-partition function. Gaussians, Bernoulli, Beta, Gamma, Dirichlet all belong to this family [^src1].

**Conjugate prior**: a prior p(θ) is conjugate to a likelihood p(data|θ) if the posterior p(θ|data) is in the same distribution family as the prior. Conjugacy makes Bayesian updates analytic — no integration required. Examples: Beta-Bernoulli, Gaussian-Gaussian (linear regression), Dirichlet-Categorical (topic models).

## Change of Variables

If Y = U(X) and U is invertible and differentiable, then [^src3]:

p_Y(y) = p_X(U^{-1}(y)) |det(∂U^{-1}/∂y)|

The term |det J| (absolute value of the Jacobian determinant) accounts for how the transformation stretches/shrinks volume. This is used in normalizing flows, variational inference (reparametrization trick), and density estimation. For linear transformations Y = AX: p_Y(y) = p_X(A^{-1}y) / |det(A)|.

## Independence

X and Y are **independent** if p(x,y) = p(x)p(y). Independence implies zero covariance, but zero covariance does not imply independence (only for Gaussians does it).

**Conditional independence**: X ⊥⊥ Y | Z if p(x,y|z) = p(x|z)p(y|z). Conditional independence structures are encoded in graphical models.

[^src1]: [Mathematics for Machine Learning, Part 8](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-08.md)
[^src2]: [Mathematics for Machine Learning, Part 10](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-10.md)
[^src3]: [Mathematics for Machine Learning, Part 11](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md)
