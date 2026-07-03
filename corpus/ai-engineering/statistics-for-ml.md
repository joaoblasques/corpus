---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-_Pyi12dn4Kw-all-of-statistics-in-1-hour-ultimate-study-guide.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - statistics
  - probability
  - statistics for ML
  - probability for ML
  - hypothesis testing
  - confidence interval
  - normal distribution
  - regression
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Statistics & Probability for ML

**TL;DR**: The mathematical substrate under [machine learning](/ai-engineering/machine-learning.md) and the "uncertainty" branch of [AI](/ai-engineering/ai-fundamentals.md) — describing data, quantifying uncertainty, and inferring from samples [^src1]. A practitioner needs working fluency in the ten areas below, not proofs; they recur in loss functions, evaluation metrics, A/B tests, and probabilistic reasoning.

## Describing data

- **Data types** — qualitative (nominal vs ordinal) vs quantitative (discrete vs continuous) determines which methods and graphs apply [^src1].
- **Central tendency** — mean (average), median (middle value, robust to outliers), mode (most frequent) [^src1].
- **Spread** — range (max − min), interquartile range (Q3 − Q1, the middle 50%), and **standard deviation** (typical distance of values from the mean; sample form divides squared deviations by `n − 1` to correct for a lost degree of freedom) [^src1].
- **Graphing** — bar/pie charts for qualitative data; histograms and box plots (five-number summary: min, Q1, median, Q3, max) for quantitative [^src1].

## Probability

- **Basics** — a probability is a number in [0, 1]; theoretical (favorable ÷ total outcomes) vs experimental (observed ÷ trials), which converges to theoretical as trials grow (law of large numbers) [^src1].
- **Independent events** multiply: P(three then three) = ⅙ × ⅙ = 1/36 [^src1].
- **Discrete distributions** — a probability mass function over discrete outcomes; the **binomial** (k successes in n independent trials at constant p) via `P(X=k) = C(n,k) · pᵏ · (1−p)ⁿ⁻ᵏ` [^src1].
- **Continuous distributions** — a probability density function where *area under the curve* over an interval gives the probability; the **normal distribution** with its 68/95/99.7 rule, and the **standard normal** (mean 0, sd 1) whose x-values are **z-scores** used with a z-table to find areas [^src1].

## Inference

- **Confidence intervals** — `estimate ± margin of error`, where margin = critical value × standard error. For a population mean (z-interval), standard error = σ/√n; a 95% interval uses z\* = 1.96. Interpretation: 95% of such intervals from repeated samples would contain the true mean [^src1].
- **Hypothesis testing** — illustrated with the **χ² goodness-of-fit test**: state a null hypothesis (observed matches expected; differences are chance), compute the χ² statistic `Σ(O−E)²/E`, compare to a critical value set by significance level α and degrees of freedom (categories − 1). If observed χ² > critical (equivalently p < α), reject the null [^src1]. The fair-die example: χ² = 3.4 < critical 11.07 (α = 0.05, df = 5), p ≈ 0.64 → fail to reject; the die is likely fair [^src1].
- **Regression & correlation** — linear regression fits a line minimizing squared **residuals**; the correlation coefficient **r** measures strength/direction of linear relationship, and **r²** (coefficient of determination) gives the fraction of variation in the dependent variable explained by the independent one [^src1].

## Why it matters for AI engineering

These primitives are not academic decoration: standard deviation and the normal distribution underpin model evaluation and anomaly detection; regression is the simplest [ML](/ai-engineering/machine-learning.md) model; Bayesian/probabilistic reasoning is the "uncertainty" pillar of [classical AI](/ai-engineering/ai-fundamentals.md); and confidence intervals / hypothesis tests are the math behind A/B experiments and [eval](/ai-engineering/agent-evaluation.md) funnels. The "learn the math you actually need" advice for ML emphasizes exactly this practical subset (distributions, mean/variance, Bayes, gradients) over proofs.

## See also

- [Machine Learning](/ai-engineering/machine-learning.md) — regression, loss, and evaluation rest on this
- [AI Fundamentals](/ai-engineering/ai-fundamentals.md) — the "uncertainty" pillar (Bayesian/Markov)
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — eval funnels and statistical experiment design
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [All of Statistics in 1 Hour (ultimate study guide)](../../raw/youtube/youtube-_Pyi12dn4Kw-all-of-statistics-in-1-hour-ultimate-study-guide.md) — JensenMath
