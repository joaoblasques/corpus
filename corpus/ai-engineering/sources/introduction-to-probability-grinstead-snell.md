---
type: source
domain: ai-engineering
status: draft
sources:
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
  - Grinstead Snell
  - Introduction to Probability
  - CHANCE project probability textbook
  - Grinstead and Snell probability
  - probability textbook AMS
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-06
updated: 2026-08-06
---

# Introduction to Probability (Grinstead & Snell, 2006)

TL;DR: Classic undergraduate probability textbook (518pp, GNU FDL open access). Simulation-first pedagogy: every concept introduced alongside a simulation experiment before the formal definition. Twelve chapters from discrete distributions through Markov chains. 19 of 25 parts ingested covering chapters 1–9; all foundational probability needed for ML (Bayes' theorem, CLT, LLN, MGFs, joint densities) is present.

## Authors

**Charles M. Grinstead** — mathematician at Swarthmore College; co-author with J. Laurie Snell [^p01].

**J. Laurie Snell** — probabilist at Dartmouth College; originator of the CHANCE project (applying probability and statistics to current events in the news); co-author with Grinstead [^p01].

Published by the American Mathematical Society (AMS), 2003. The version dated 4 July 2006 was published by Peter Doyle and released under the GNU Free Documentation License, making it freely redistributable [^p01].

## Scope (parts 01–19 ingested)

| Chapter | Title | Content |
|---|---|---|
| Ch1 | Discrete Probability Distributions | Sample space, events, probability distribution, simulation, expected value, variance |
| Ch2 | Continuous Probability Densities | Density functions, CDFs, simulation via inverse CDF, exponential and normal distributions, Poisson process |
| Ch3 | Combinatorics | Permutations, combinations, multinomial coefficients, card shuffling as Markov chain |
| Ch4 | Conditional Probability | Bayes' theorem, independence, continuous conditional probability, Monty Hall, Bertrand paradoxes, Polya urn |
| Ch5 | Distributions and Expected Value | Geometric, negative binomial, Poisson (as binomial limit), exponential, normal; linearity of expectation |
| Ch6 | Expected Value and Variance | Var formula, covariance, Chebyshev's inequality, Weak and Strong Law of Large Numbers |
| Ch7 | Generating Functions and CLT | PGF, MGF, moments from derivatives, CLT proof via MGFs |
| Ch8 | Markov Chains (beginning) | Transition matrices, stationary distributions |
| Ch9 | Random Variables | Joint density, marginal density, sums of independent RVs, MGF of continuous distributions |

## Chapter 1: Discrete Probability Distributions

The **sample space** Ω is the set of all possible outcomes of an experiment. An **event** is a subset of Ω. A **probability distribution** assigns a non-negative mass m(ω) to each outcome ω ∈ Ω such that Σ m(ω) = 1 [^p01].

The **distribution function** (pmf) p(x) = P(X = x) gives the probability that random variable X takes value x [^p02].

**Discrete distribution examples** [^p02]:
- **Bernoulli(p)**: X ∈ {0, 1}; P(X=1) = p, P(X=0) = 1-p
- **Binomial(n, p)**: number of successes in n independent Bernoulli trials; P(X=k) = C(n,k) p^k (1-p)^{n-k}
- **Geometric(p)**: number of trials until first success; P(X=k) = (1-p)^{k-1} p for k = 1, 2, ...
- **Uniform on {1,...,n}**: m(ω) = 1/n for each outcome

**Expected value**: E[X] = Σ_x x · p(x) — the probability-weighted average of all values [^p02].

**Variance**: Var[X] = E[(X - E[X])^2] = E[X^2] - (E[X])^2 [^p03].

The simulation approach: the textbook introduces every distribution with a computer simulation before formal definition, building intuition that the empirical frequency histogram converges to the theoretical pmf [^p01].

## Chapter 2: Continuous Probability Densities

A **density function** f(x) ≥ 0 satisfies ∫_{-∞}^{∞} f(x) dx = 1. For a continuous random variable X, P(a ≤ X ≤ b) = ∫_a^b f(x) dx [^p04].

The **cumulative distribution function (CDF)**: F(x) = P(X ≤ x) = ∫_{-∞}^x f(t) dt. The density is the derivative: f(x) = F'(x) [^p04].

**Simulation via inverse CDF**: to sample X with CDF F, draw U ~ Uniform[0,1] and return X = F^{-1}(U). This works because F(X) is uniformly distributed when X has CDF F [^p04].

**Key continuous distributions** [^p04]:
- **Exponential(λ)**: f(x) = λ exp(-λx) for x ≥ 0; CDF F(x) = 1 - exp(-λx); mean 1/λ; memoryless property P(X > s+t | X > s) = P(X > t)
- **Normal N(μ, σ²)**: f(x) = (1/(σ√(2π))) exp(-(x-μ)²/(2σ²)); standardized Z = (X-μ)/σ ~ N(0,1)

**Poisson process**: arrivals at rate λ; the number of arrivals in time t is Poisson(λt); inter-arrival times are Exponential(λ) [^p04].

## Chapter 3: Combinatorics

**Permutations**: the number of ordered selections of k objects from n is P(n,k) = n!/(n-k)! [^p05].

**Combinations**: C(n,k) = n!/(k!(n-k)!) — the number of unordered subsets of size k from n objects [^p05].

**Multinomial coefficients**: C(n; k_1, k_2, ..., k_r) = n!/(k_1! k_2! ... k_r!) counts arrangements of n objects of r types with k_i of type i [^p05].

**Card shuffling as a Markov chain**: a riffle shuffle permutes the deck; repeated shuffles constitute a Markov chain on the symmetric group S_{52}. The mixing time (number of shuffles to reach near-uniform distribution) is approximately 7 for a standard 52-card deck [^p06]. This connects combinatorics to the later Markov chain theory.

## Chapter 4: Conditional Probability

**Conditional probability**: P(A|B) = P(A ∩ B) / P(B), defined when P(B) > 0 [^p07].

**Bayes' theorem**: P(H|E) = P(E|H) · P(H) / P(E) where P(E) = Σ_i P(E|H_i) P(H_i) over a partition {H_i} of the sample space [^p07]. Updates prior belief P(H) to posterior P(H|E) upon observing evidence E.

**Independence**: A and B are independent iff P(A ∩ B) = P(A)P(B), equivalently P(A|B) = P(A) [^p07].

**Continuous conditional probability**: for continuous random variables, the conditional density f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y) [^p08].

**Classic paradoxes** [^p08]:
- **Monty Hall problem**: switching doors after the host reveals a goat doubles the probability of winning (from 1/3 to 2/3); the paradox arises because the host's action is not uniformly random
- **Bertrand's box paradox**: three boxes (gold/gold, gold/silver, silver/silver); given you drew a gold coin, probability the other coin is gold = 2/3 (not 1/2); illustrates base-rate neglect

**Polya urn model**: start with r red and b blue balls; draw one ball, return it with one additional ball of the same color. The fraction of red balls at step n is a martingale converging to a Beta(r, b) distribution; this is the canonical Bayesian-updating illustration [^p08].

**Bayesian updating and Beta distribution**: after observing h heads in n coin flips with unknown bias θ, the posterior P(θ | data) is Beta(h+1, n-h+1) when the prior is uniform (Beta(1,1)). Each new flip updates the Beta hyperparameters by incrementing α or β [^p09].

## Chapter 5: Distributions and Expected Value

**Geometric distribution**: P(X = k) = (1-p)^{k-1} p for k = 1, 2, ...; X is the number of trials until first success; E[X] = 1/p; Var[X] = (1-p)/p^2 [^p10].

**Negative binomial**: number of trials until r successes; P(X=k) = C(k-1, r-1) p^r (1-p)^{k-r} [^p10].

**Poisson distribution as limit of Binomial**: for large n and small p with λ = np fixed, Binomial(n,p) → Poisson(λ). P(X=k) = e^{-λ} λ^k / k! ; E[X] = Var[X] = λ [^p10].

**Exponential distribution**: memoryless continuous distribution; if X ~ Exp(λ) then P(X > s+t | X > s) = P(X > t) for all s, t > 0 [^p11].

**Normal distribution**: P(a < X < b) computed via standard normal table; the standardization Z = (X - μ)/σ converts any normal to N(0,1) [^p11].

**Linearity of expectation**: E[X + Y] = E[X] + E[Y] for any random variables X, Y (even dependent); E[cX] = c E[X] [^p11].

## Chapter 6: Variance and the Law of Large Numbers

**Variance formula**: Var[X] = E[(X - μ)^2] = E[X^2] - μ^2 where μ = E[X] [^p12].

**Covariance**: Cov[X, Y] = E[(X - E[X])(Y - E[Y])] = E[XY] - E[X]E[Y]. If X, Y are independent then Cov[X,Y] = 0 (converse not generally true) [^p12].

**Variance of sum**: Var[X + Y] = Var[X] + Var[Y] + 2 Cov[X, Y]; for independent X, Y: Var[X + Y] = Var[X] + Var[Y] [^p12].

**Chebyshev's inequality**: for any random variable X with finite mean μ and variance σ²: P(|X - μ| ≥ kσ) ≤ 1/k² for any k > 0 [^p13]. Does not assume any distributional form; gives a universal bound.

**Weak Law of Large Numbers (WLLN)**: let X_1, X_2, ... be i.i.d. with E[X_i] = μ and Var[X_i] = σ² < ∞. For S_n = X_1 + ... + X_n, the sample mean S_n/n converges in probability to μ: for every ε > 0, P(|S_n/n - μ| > ε) → 0 as n → ∞ [^p13]. Proof: apply Chebyshev to S_n/n noting Var[S_n/n] = σ²/n → 0.

**Strong Law of Large Numbers (SLLN)**: under the same conditions, S_n/n → μ almost surely (with probability 1) [^p14]. The SLLN is stronger: not merely convergence in probability but convergence on a set of probability 1.

## Chapter 7: Generating Functions and Central Limit Theorem

**Probability generating function (PGF)**: for a non-negative integer-valued random variable X, g(z) = E[z^X] = Σ_{k=0}^{∞} P(X=k) z^k. The k-th derivative at z=0 gives k! P(X=k) [^p15].

**Moment generating function (MGF)**: M(t) = E[e^{tX}] = Σ_{k=0}^{∞} E[X^k] t^k / k! [^p15]. The k-th moment E[X^k] = M^{(k)}(0) (k-th derivative of M evaluated at 0).

**MGF of sum of independent RVs**: if X and Y are independent, M_{X+Y}(t) = M_X(t) · M_Y(t) [^p15]. This multiplicative property makes MGFs powerful for proving limit theorems.

**Central Limit Theorem (CLT)**: let X_1, X_2, ... be i.i.d. with mean μ and variance σ² > 0. The standardized sum Z_n = (S_n - nμ) / (σ √n) converges in distribution to N(0,1) as n → ∞ [^p16]. For any -∞ < a < b < ∞: P(a ≤ Z_n ≤ b) → Φ(b) - Φ(a) where Φ is the standard normal CDF.

**CLT proof via MGFs**: the MGF of Z_n is [M_X((t/(σ√n))) exp(-μt/(σ√n))]^n. Taylor-expanding M_X around 0 and taking the limit n → ∞ yields exp(t²/2), the MGF of N(0,1) [^p16].

**Normal approximation**: for large n, Binomial(n,p) ≈ N(np, np(1-p)). The normal approximation to the Poisson(λ) for large λ: N(λ, λ) [^p17].

## Chapters 8–9: Markov Chains Beginning and Random Variables

**Joint density**: for continuous random variables X, Y, the joint density f_{X,Y}(x,y) ≥ 0 satisfies ∫∫ f_{X,Y}(x,y) dx dy = 1 [^p18].

**Marginal density**: f_X(x) = ∫ f_{X,Y}(x,y) dy; f_Y(y) = ∫ f_{X,Y}(x,y) dx [^p18].

**Independence for continuous RVs**: X and Y are independent iff f_{X,Y}(x,y) = f_X(x) f_Y(y) for all x, y [^p18].

**Density of sum of independent RVs**: if X and Y are independent, the density of Z = X + Y is the convolution f_Z(z) = ∫ f_X(x) f_Y(z-x) dx [^p19].

**MGF of continuous distributions**: for Exponential(λ), M(t) = λ/(λ-t) for t < λ; for Normal N(μ, σ²), M(t) = exp(μt + σ²t²/2) [^p19].

## Connection to ML

The probability foundations in this textbook underpin core ML methods [^p01][^p07][^p16]:

- **Bayesian inference**: Bayes' theorem (Ch4) is the backbone of Bayesian ML (priors, posteriors, MAP estimation)
- **MLE/MAP estimation**: expected value, variance, and the Gaussian distribution (Ch1–2, Ch5–6)
- **Distributional assumptions**: the normal distribution assumption in linear regression; Poisson assumption in count models
- **Naive Bayes classifiers**: direct application of Bayes' theorem with conditional independence assumptions
- **CLT and Gaussian justification**: the CLT (Ch7) explains why Gaussian approximations are appropriate for sums of many independent factors
- **LLN and consistency of estimators**: the WLLN/SLLN (Ch6) justify that sample statistics converge to population parameters as dataset size grows

See also:
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — ML-oriented coverage (Deisenroth MML, Thomas 2018)
- [/ai-engineering/statistical-learning.md](/ai-engineering/statistical-learning.md) — statistical learning framework
- [/ai-engineering/gaussian-mixture-models.md](/ai-engineering/gaussian-mixture-models.md) — Gaussian distributions in density estimation

---

[^p01]: [Introduction to Probability — Part 01](../../../raw/pdf/pdf-introduction-to-probability-part-01.md)
[^p02]: [Introduction to Probability — Part 02](../../../raw/pdf/pdf-introduction-to-probability-part-02.md)
[^p03]: [Introduction to Probability — Part 03](../../../raw/pdf/pdf-introduction-to-probability-part-03.md)
[^p04]: [Introduction to Probability — Part 04](../../../raw/pdf/pdf-introduction-to-probability-part-04.md)
[^p05]: [Introduction to Probability — Part 05](../../../raw/pdf/pdf-introduction-to-probability-part-05.md)
[^p06]: [Introduction to Probability — Part 06](../../../raw/pdf/pdf-introduction-to-probability-part-06.md)
[^p07]: [Introduction to Probability — Part 07](../../../raw/pdf/pdf-introduction-to-probability-part-07.md)
[^p08]: [Introduction to Probability — Part 08](../../../raw/pdf/pdf-introduction-to-probability-part-08.md)
[^p09]: [Introduction to Probability — Part 09](../../../raw/pdf/pdf-introduction-to-probability-part-09.md)
[^p10]: [Introduction to Probability — Part 10](../../../raw/pdf/pdf-introduction-to-probability-part-10.md)
[^p11]: [Introduction to Probability — Part 11](../../../raw/pdf/pdf-introduction-to-probability-part-11.md)
[^p12]: [Introduction to Probability — Part 12](../../../raw/pdf/pdf-introduction-to-probability-part-12.md)
[^p13]: [Introduction to Probability — Part 13](../../../raw/pdf/pdf-introduction-to-probability-part-13.md)
[^p14]: [Introduction to Probability — Part 14](../../../raw/pdf/pdf-introduction-to-probability-part-14.md)
[^p15]: [Introduction to Probability — Part 15](../../../raw/pdf/pdf-introduction-to-probability-part-15.md)
[^p16]: [Introduction to Probability — Part 16](../../../raw/pdf/pdf-introduction-to-probability-part-16.md)
[^p17]: [Introduction to Probability — Part 17](../../../raw/pdf/pdf-introduction-to-probability-part-17.md)
[^p18]: [Introduction to Probability — Part 18](../../../raw/pdf/pdf-introduction-to-probability-part-18.md)
[^p19]: [Introduction to Probability — Part 19](../../../raw/pdf/pdf-introduction-to-probability-part-19.md)
