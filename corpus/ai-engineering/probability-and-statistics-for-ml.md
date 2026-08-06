---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-10.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-mathematics-for-machine-learning-part-03.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-introduction-to-probability-part-01.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-02.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-03.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-04.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-05.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-06.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-07.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-08.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-09.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-10.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-11.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-12.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-13.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-14.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-15.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-16.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-17.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-18.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-introduction-to-probability-part-19.md
    channel: pdf
    ingested_at: 2026-08-06
aliases:
  - probability ML
  - Bayesian inference
  - Gaussian distribution
  - exponential family
  - conjugate prior
  - Polya urn
  - Chebyshev's inequality
  - Weak Law of Large Numbers
  - Central Limit Theorem
  - moment generating function
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-08-06
---

# Probability and Statistics for Machine Learning

TL;DR: ML models uncertainty via probability distributions. The Gaussian is central (conjugate to itself, closed under linear transforms, marginals/conditionals stay Gaussian). Bayes' theorem converts likelihood × prior to posterior. Exponential families unify named distributions and guarantee finite-dimensional sufficient statistics and conjugate priors. Change of variables enables sampling and density estimation. These foundations underpin linear regression, GMMs, Bayesian inference, and neural network training.

## Probability Space Basics

A probability space (Omega, F, P) consists of a sample space, a sigma-algebra (event space), and a probability measure P mapping to [0, 1] with P(Omega) = 1 [^src1].

**Key rules**:
- **Sum rule** (marginalization): p(x) = sum_y p(x, y) or integral p(x, y) dy
- **Product rule** (chain rule): p(x, y) = p(y|x) p(x)
- **Bayes' theorem**: p(theta|x) = p(x|theta) p(theta) / p(x) proportional to p(x|theta) p(theta) [^src1]
- **Union bound (Boole's inequality)**: P(∪ A_i) ≤ Σ P(A_i) for any countable set of events, disjoint or not [^t-src-prob]

**Independence**: X and Y are independent iff p(x, y) = p(x)p(y) iff p(x|y) = p(x) [^src1].

## Summary Statistics

**Mean (expectation)**: E_X[x] = sum x p(x) or integral x p(x) dx.

**Variance**: V_X[x] = E[(x - E[x])^2] = E[x^2] - (E[x])^2. Standard deviation = sqrt(V).

**Covariance**: Cov[x, y] = E[(x - E[x])(y - E[y])] = E[xy] - E[x]E[y].

**Correlation**: rho(x, y) = Cov[x, y] / (sqrt(V[x]) sqrt(V[y])). This is the cosine of the angle between random variables viewed as vectors: uncorrelated variables are orthogonal in that space [^src1].

**Covariance matrix**: Sigma = Cov[x, x] in R^{D x D}. Always symmetric positive semidefinite. The inverse Σ^{-1} is called the **precision matrix** [^t-src-prob].

**Affine transformations**: if y = Ax + b, then E[y] = AE[x] + b and V[y] = A V[x] A^T [^src1].

## Gaussian Distribution

The **multivariate Gaussian** (normal distribution) N(mu, Sigma) has density [^src1]:

```
p(x) = (2pi)^{-D/2} |Sigma|^{-1/2} exp(-0.5 (x - mu)^T Sigma^{-1} (x - mu))
```

where mu in R^D is the mean vector and Sigma in R^{D x D} is the SPD covariance matrix.

**Geometry of multivariate Gaussians**: the density is a strictly monotonically decreasing function of the precision quadratic form (x − µ)^T Σ^{-1} (x − µ). Therefore isocontours of the density are ellipsoids centered at µ, with axes pointing in directions of eigenvectors of Σ (equivalently of Σ^{-1}), and axis lengths proportional to square roots of eigenvalues of Σ [^t-src-prob]. This connects directly to the geometry of positive definite quadratic forms.

**Why the Gaussian is ubiquitous in ML**:
- Closed-form marginals and conditionals (both Gaussian)
- Closed under linear transformations
- Central limit theorem: sums of i.i.d. variables converge to Gaussian
- Maximum entropy distribution given fixed mean and variance
- Computationally convenient for Bayesian inference (conjugate prior to itself for the mean)

**Marginal distribution**: if [x, y] ~ N([mu_x, mu_y], Sigma), then p(x) = N(x | mu_x, Sigma_xx) [^src1].

**Conditional distribution**: p(x|y) = N(x | mu_{x|y}, Sigma_{x|y}) where [^src1]:
```
mu_{x|y} = mu_x + Sigma_xy Sigma_yy^{-1} (y - mu_y)
Sigma_{x|y} = Sigma_xx - Sigma_xy Sigma_yy^{-1} Sigma_yx
```
This formula underlies the Kalman filter and Gaussian processes.

**Product of two Gaussians**: N(x|a, A) N(x|b, B) = c N(x|c_mean, C) where [^src1]:
```
C = (A^{-1} + B^{-1})^{-1}
c_mean = C(A^{-1}a + B^{-1}b)
c = N(a | b, A + B)   (scaling constant)
```

**Sums of independent Gaussians**: if X ~ N(mu_x, Sigma_x) and Y ~ N(mu_y, Sigma_y) independent, then X+Y ~ N(mu_x + mu_y, Sigma_x + Sigma_y) [^src1].

**Linear transform**: if X ~ N(mu, Sigma) and y = Ax, then Y ~ N(Amu, A Sigma A^T) [^src1].

**Sampling algorithm**: To sample x ~ N(mu, Sigma) [^src1]:
1. Compute Cholesky: Sigma = LL^T
2. Draw z ~ N(0, I) (standard normal, i.i.d. components)
3. Return x = Lz + mu

## Named Distributions

**Bernoulli** Ber(mu): binary X in {0,1}. p(X=1) = mu. Mean = mu, Var = mu(1-mu) [^src1].

**Binomial** Bin(N, mu): number of successes in N Bernoulli trials. Mean = Nmu, Var = Nmu(1-mu) [^src1].

**Beta** Beta(alpha, beta): continuous X in [0,1]. p(x|alpha,beta) proportional to x^{alpha-1}(1-x)^{beta-1}. Used as prior on probabilities.
- alpha = beta = 1: uniform distribution
- alpha, beta > 1: unimodal
- alpha, beta < 1: bimodal (U-shaped)
- alpha moves probability mass toward 1; beta moves it toward 0 [^src1]

## Conjugate Priors

**Definition**: a prior is conjugate to a likelihood if the posterior has the same parametric form as the prior [^src1].

**Why conjugacy matters**: Bayesian inference requires computing posterior p(theta|x) proportional to p(x|theta)p(theta). With conjugate priors, the posterior is computed in closed form by updating the prior parameters — no numerical integration needed.

**Key conjugate pairs** [^src1]:

| Likelihood | Conjugate prior | Posterior |
|---|---|---|
| Bernoulli(mu) | Beta(alpha, beta) | Beta(alpha+x, beta+1-x) |
| Binomial(N, mu) | Beta(alpha, beta) | Beta(alpha+h, beta+N-h) |
| Gaussian (mean unknown, univariate) | Gaussian/inverse-Gamma | Gaussian/inverse-Gamma |
| Gaussian (mean unknown, multivariate) | Gaussian/inverse-Wishart | Gaussian/inverse-Wishart |
| Multinomial | Dirichlet | Dirichlet |

**Beta-Bernoulli example**: prior p(theta) = Beta(alpha, beta); posterior after observing x in {0,1} is Beta(alpha+x, beta+1-x). Each observation just increments the appropriate hyperparameter [^src1].

## Exponential Family

The **exponential family** unifies all major named distributions into one parametric form [^src1]:

```
p(x | theta) = h(x) exp(theta^T phi(x) - A(theta))
```

where:
- **theta** = natural parameters
- **phi(x)** = sufficient statistics vector
- **A(theta)** = log-partition function (normalizer)
- **h(x)** = base measure

**Members**: Gaussian, Bernoulli, Binomial, Beta, Poisson, Gamma, Dirichlet.

**Key properties** [^src1]:
1. **Finite sufficient statistics**: phi(x) captures all information about theta from data. As N grows, no more parameters needed (Pitman-Koopman-Darmois theorem, 1935-36).
2. **Conjugate prior always exists**: every exponential family has an exponential-family conjugate prior
3. **MLE behaves well**: log-likelihood is concave — convex optimization problem, gradient methods guaranteed to find global optimum
4. **Moment matching**: MLE sets expected sufficient statistics equal to empirical sufficient statistics

**Gaussian as exponential family**: N(mu, sigma^2) with phi(x) = [x, x^2]^T [^src1].

**Bernoulli as exponential family**: natural parameter theta = log(mu/(1-mu)) (logit function). Inverse is sigmoid: mu = 1/(1+exp(-theta)) — used in logistic regression and neural network activations [^src1].

**Sufficient statistics** (Fisher-Neyman theorem): phi(x) is sufficient for theta iff p(x|theta) = h(x) g_theta(phi(x)). All information about theta needed from the data is captured in phi(x) [^src1].

## Change of Variables / Inverse Transform

If Y = U(X) and U is invertible, the pdf of Y is [^src1]:

```
f_Y(y) = f_X(U^{-1}(y)) |d/dy U^{-1}(y)|         (univariate)
f_Y(y) = f_X(U^{-1}(y)) |det(J_{U^{-1}}(y))|       (multivariate)
```

where the Jacobian |det J| accounts for volume distortion of the transformation.

**Inverse transform method** (Theorem 6.15): if F_X(x) is the CDF of X, then Y = F_X(X) is uniformly distributed. Corollary: to sample from any distribution with known CDF, draw U ~ Uniform[0,1] and return X = F_X^{-1}(U) [^src1].

**Applications in ML**:
- Normalizing flows: chain of invertible transformations converts simple base distribution to complex target
- Reparametrization trick in VAEs: sample z = mu + sigma*epsilon where epsilon ~ N(0,1) — keeps gradient flowing through sampling operation

## Geometry of Random Variables

Random variables can be viewed as vectors with inner product ⟨X, Y⟩ = Cov[x, y] (for zero-mean variables) [^src1]:
- Length = standard deviation sqrt(Var[X])
- Angle between X and Y gives correlation rho(X, Y) = cos(theta)
- Orthogonality = zero correlation (uncorrelated)

Uncorrelated variables satisfy Pythagoras: Var[X + Y] = Var[X] + Var[Y].

## Discrete Distributions

The following named discrete distributions are foundations for ML classifiers, language models, and count-based inference [^gns01][^gns02]:

| Distribution | PMF | Mean | Variance |
|---|---|---|---|
| Bernoulli(p) | P(X=1)=p, P(X=0)=1-p | p | p(1-p) |
| Binomial(n,p) | C(n,k)p^k(1-p)^{n-k} | np | np(1-p) |
| Geometric(p) | (1-p)^{k-1}p, k=1,2,... | 1/p | (1-p)/p^2 |
| Negative Binomial(r,p) | C(k-1,r-1)p^r(1-p)^{k-r} | r/p | r(1-p)/p^2 |
| Poisson(λ) | e^{-λ}λ^k/k! | λ | λ |
| Hypergeometric(N,K,n) | C(K,k)C(N-K,n-k)/C(N,n) | nK/N | — |

**Poisson as limit of Binomial**: for large n and small p with λ = np fixed, Binomial(n,p) → Poisson(λ). This motivates the Poisson distribution as the natural model for rare events in large populations [^gns10].

**Expected value**: E[X] = Σ_x x · p(x) — the probability-weighted average [^gns01].

**Variance**: Var[X] = E[X^2] - (E[X])^2 — computing via E[X^2] is usually simpler than direct computation of E[(X-μ)^2] [^gns01].

## Key Inequalities and Limit Theorems

**Markov's inequality**: for any non-negative random variable X and a > 0: P(X ≥ a) ≤ E[X] / a [^gns06]. Proof: E[X] = ∫ x f(x) dx ≥ ∫_{x≥a} x f(x) dx ≥ a P(X ≥ a).

**Chebyshev's inequality**: for any random variable X with mean μ and finite variance σ²: P(|X - μ| ≥ kσ) ≤ 1/k² for any k > 0 [^gns06]. Follows directly from Markov applied to (X-μ)^2. Distribution-free; bounds are loose in practice but hold universally.

**Weak Law of Large Numbers (WLLN)**: let X_1, ..., X_n be i.i.d. with mean μ and variance σ² < ∞. The sample mean S_n/n = (X_1 + ... + X_n)/n satisfies: for every ε > 0, P(|S_n/n - μ| > ε) → 0 as n → ∞ [^gns06]. Proof: Var[S_n/n] = σ²/n → 0; apply Chebyshev.

**Strong Law of Large Numbers (SLLN)**: under the same conditions, S_n/n → μ with probability 1 (almost surely) [^gns06]. Stronger than WLLN: convergence holds on an event of probability 1, not merely that individual probabilities go to zero.

**Central Limit Theorem (CLT)**: let X_1, ..., X_n be i.i.d. with mean μ and variance σ² > 0. The standardized sum Z_n = (S_n - nμ)/(σ√n) converges in distribution to N(0,1) [^gns07]. Formally: P(a ≤ Z_n ≤ b) → Φ(b) - Φ(a) where Φ is the standard normal CDF. Justifies Gaussian approximations whenever outcomes are sums of many independent contributions — pervasive in ML (e.g., weight initialization, noise models, sampling distributions of estimators).

## Generating Functions

**Probability generating function (PGF)**: for a non-negative integer-valued random variable X, g(z) = E[z^X] = Σ_{k=0}^{∞} P(X=k) z^k [^gns07]. The k-th derivative at z=0 equals k! P(X=k). PGFs transform convolution (sums of independent RVs) into multiplication.

**Moment generating function (MGF)**: M(t) = E[e^{tX}] [^gns07]. Expanding the exponential: M(t) = Σ_{k=0}^{∞} E[X^k] t^k / k!, so the k-th moment E[X^k] = M^{(k)}(0) (k-th derivative evaluated at 0).

**MGF of sum of independent RVs**: if X and Y are independent, M_{X+Y}(t) = M_X(t) · M_Y(t) [^gns07]. This multiplicative property makes MGFs the natural tool for proving limit theorems about sums.

**Key MGFs** [^gns07]:
- Bernoulli(p): M(t) = 1 - p + p e^t
- Poisson(λ): M(t) = exp(λ(e^t - 1))
- Normal N(μ, σ²): M(t) = exp(μt + σ²t²/2)
- Exponential(λ): M(t) = λ/(λ - t) for t < λ

**CLT proof via MGFs**: the MGF of Z_n = (S_n - nμ)/(σ√n) is [M_X(t/(σ√n)) exp(-μt/(σ√n))]^n. Taylor-expanding M_X(s) = 1 + μs + (μ² + σ²)s²/2 + ... and taking n → ∞ gives exp(t²/2), the MGF of N(0,1) [^gns07].

## Related Corpus Pages

- [/ai-engineering/matrix-decompositions.md](/ai-engineering/matrix-decompositions.md) — Cholesky for Gaussian sampling
- [/ai-engineering/optimization-for-ml.md](/ai-engineering/optimization-for-ml.md) — MLE/MAP as optimization problems
- [/ai-engineering/gaussian-mixture-models.md](/ai-engineering/gaussian-mixture-models.md) — GMM density estimation using Gaussians
- [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md) — probabilistic PCA
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — Deisenroth/Faisal/Ong 2020 full book summary
- [/ai-engineering/sources/mathematics-for-machine-learning-thomas.md](/ai-engineering/sources/mathematics-for-machine-learning-thomas.md) — Thomas 2018 (CS 189 Berkeley), proof-oriented course notes

---

[^src1]: [Mathematics for Machine Learning, Part 10](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-10.md)
[^src2]: [Mathematics for Machine Learning, Part 11](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-11.md)
[^t-src-prob]: [Mathematics for Machine Learning (Thomas 2018), Part 3/3](../../raw/pdf/pdf-mathematics-for-machine-learning-part-03.md)
[^gns01]: [Introduction to Probability (Grinstead & Snell) — Part 01](../../raw/pdf/pdf-introduction-to-probability-part-01.md)
[^gns02]: [Introduction to Probability (Grinstead & Snell) — Part 02](../../raw/pdf/pdf-introduction-to-probability-part-02.md)
[^gns03]: [Introduction to Probability (Grinstead & Snell) — Part 03](../../raw/pdf/pdf-introduction-to-probability-part-03.md)
[^gns04]: [Introduction to Probability (Grinstead & Snell) — Part 04](../../raw/pdf/pdf-introduction-to-probability-part-04.md)
[^gns05]: [Introduction to Probability (Grinstead & Snell) — Part 05](../../raw/pdf/pdf-introduction-to-probability-part-05.md)
[^gns06]: [Introduction to Probability (Grinstead & Snell) — Part 06](../../raw/pdf/pdf-introduction-to-probability-part-06.md)
[^gns07]: [Introduction to Probability (Grinstead & Snell) — Part 07](../../raw/pdf/pdf-introduction-to-probability-part-07.md)
[^gns08]: [Introduction to Probability (Grinstead & Snell) — Part 08](../../raw/pdf/pdf-introduction-to-probability-part-08.md)
[^gns09]: [Introduction to Probability (Grinstead & Snell) — Part 09](../../raw/pdf/pdf-introduction-to-probability-part-09.md)
[^gns10]: [Introduction to Probability (Grinstead & Snell) — Part 10](../../raw/pdf/pdf-introduction-to-probability-part-10.md)
[^gns11]: [Introduction to Probability (Grinstead & Snell) — Part 11](../../raw/pdf/pdf-introduction-to-probability-part-11.md)
[^gns12]: [Introduction to Probability (Grinstead & Snell) — Part 12](../../raw/pdf/pdf-introduction-to-probability-part-12.md)
[^gns13]: [Introduction to Probability (Grinstead & Snell) — Part 13](../../raw/pdf/pdf-introduction-to-probability-part-13.md)
[^gns14]: [Introduction to Probability (Grinstead & Snell) — Part 14](../../raw/pdf/pdf-introduction-to-probability-part-14.md)
[^gns15]: [Introduction to Probability (Grinstead & Snell) — Part 15](../../raw/pdf/pdf-introduction-to-probability-part-15.md)
[^gns16]: [Introduction to Probability (Grinstead & Snell) — Part 16](../../raw/pdf/pdf-introduction-to-probability-part-16.md)
[^gns17]: [Introduction to Probability (Grinstead & Snell) — Part 17](../../raw/pdf/pdf-introduction-to-probability-part-17.md)
[^gns18]: [Introduction to Probability (Grinstead & Snell) — Part 18](../../raw/pdf/pdf-introduction-to-probability-part-18.md)
[^gns19]: [Introduction to Probability (Grinstead & Snell) — Part 19](../../raw/pdf/pdf-introduction-to-probability-part-19.md)
