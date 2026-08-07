---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-01.md
    channel: pdf
    ingested_at: 2026-08-07
  - path: raw/_inbox/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-02.md
    channel: pdf
    ingested_at: 2026-08-07
  - path: raw/_inbox/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-03.md
    channel: pdf
    ingested_at: 2026-08-07
  - path: raw/_inbox/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-04.md
    channel: pdf
    ingested_at: 2026-08-07
  - path: raw/_inbox/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-05.md
    channel: pdf
    ingested_at: 2026-08-07
  - path: raw/_inbox/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-06.md
    channel: pdf
    ingested_at: 2026-08-07
aliases:
  - Lies Damned Lies or Statistics
  - Poritz statistics textbook
  - How to Tell the Truth with Statistics
  - statistics undergraduate textbook Poritz
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-07
updated: 2026-08-07
---

# Lies, Damned Lies, or Statistics: How to Tell the Truth with Statistics (Poritz, 2017)

TL;DR: Free undergraduate statistics textbook (143pp, CC BY-SA 4.0) by Jonathan A. Poritz (CSU-Pueblo). Covers one-semester applied statistics: descriptive stats (distributions, center, spread), study design (sampling, experiments, ethics), and inferential statistics (CLT, confidence intervals, hypothesis testing). Critical-thinking framing — statistics as an alternative to lying, not a type of lie. All 6 parts ingested (complete).

## Author

**Jonathan A. Poritz** — mathematician at Colorado State University–Pueblo, Department of Mathematics and Physics; teaches Math 156 (introductory statistics). Email: jonathan@poritz.net [^p01].

Published 13 May 2017 as a first draft. Released under CC BY-SA 4.0, allowing free sharing, adaptation, and commercial reuse with attribution [^p01].

## Scope

The book is organized in three parts:

| Part | Title | Content |
|---|---|---|
| Part 1 | Descriptive Statistics | One-variable and bivariate statistics; visualizations; measures of center and spread; linear regression |
| Part 2 | Good Data | Probability theory; study design; data collection ethics |
| Part 3 | Inferential Statistics | CLT; confidence intervals; hypothesis testing |

## Part 1: Descriptive Statistics

### Terminology

**Individual**: the unit of observation (person, event, object). **Population**: all individuals of interest. **Variable**: the measurement question asked about each individual [^p01].

**Variable types** [^p01]:
- **Categorical variable**: finite set of possible values (e.g., coin face: heads/tails, election vote choice)
- **Quantitative variable**: numeric values (e.g., homework hours, letter grade as ordered numeric)

**Sample**: a subset of a population, size n; population size N; usually n << N [^p01].

### Visualizing Categorical Data

**Bar chart (frequency)**: bars over categorical values, height = count. The order of categories on the x-axis is arbitrary — never infer trends from bar chart order [^p01].

**Bar chart (relative frequency)**: height = fraction/percentage; heights must sum to 1 (100%). A common deception: showing only a portion of the y-axis to exaggerate differences [^p01].

**Pie charts**: fractions as wedge sizes. Poritz argues pie charts are almost never a good choice — 3,000 search results for "pie charts are bad"; they invite misinterpretation [^p01].

### Visualizing Quantitative Data

**Stem-and-leaf plot**: tens digit (stem) on left of vertical bar, ones digit (leaf) on right. Contains all data values; tedious for large datasets [^p01].

**Histogram**: bars over bins (class intervals); the most important visual for quantitative data. Bin width choice trades off noise vs. information loss [^p01].
- All bars same width; edge values assigned consistently (left or right inclusion)
- Shape descriptors: **symmetric**, **skewed left** (longer left tail), **skewed right** (longer right tail), **unimodal**, **multimodal**

**Relative frequency histogram**: divide bar heights by sample size n; shape identical, y-axis changes to fractions/percents [^p01].

### Measures of Center

**Mode**: value(s) occurring most often. Weakness: can be an accidental coincidence with no relation to the overall data structure; a single value change can shift the mode dramatically [^p01].

**Mean**: x̄ = (Σ x_i) / n. Very sensitive to outliers — one extreme value can shift the mean substantially [^p01].

**Median**: middle value after sorting; average of two middle values if n is even. Insensitive to outliers: even replacing a value with 1,000,000 changes the median by at most one rank position [^p01].

**Key insight** [^p01]: Mean > Median → right-skewed histogram; Mean < Median → left-skewed histogram. This allows detecting skew from summary statistics alone.

**Political example**: rising mean income can coexist with stagnant or falling median income if top earners capture all gains; using the mean hides what is happening to most of the population [^p01].

### Measures of Spread

**Range**: x_max − x_min. Supremely sensitive to outliers (which always set x_min or x_max) [^p01].

**Quartiles**: Q1 = median of lower half; Q3 = median of upper half. **IQR** = Q3 − Q1; resistant to outliers [^p01].

**1.5 IQR Rule** (outlier definition): a value is an outlier if it is < Q1 − 1.5·IQR or > Q3 + 1.5·IQR [^p02].

**Five-number summary**: (minimum, Q1, median, Q3, maximum). **Boxplot**: visual of the five-number summary; box spans Q1 to Q3, median line inside, whiskers to fences, outliers plotted individually [^p02].

**Variance**: s² = [Σ(x_i − x̄)²] / (n − 1); uses n−1 for sample variance (Bessel's correction). **Standard deviation**: s = √(s²). For a **population**: σ² = [Σ(x_i − µ)²] / N [^p02].

**Standard deviation interpretation**: for roughly bell-shaped data, approximately 68% of values fall within 1σ of the mean, 95% within 2σ, 99.7% within 3σ (the 68–95–99.7 rule) [^p02].

### Bivariate Statistics

**Scatterplot**: explanatory variable (independent) on x-axis, response variable (dependent) on y-axis [^p02].

**Correlation coefficient** r: measures linear association; always −1 ≤ r ≤ 1; r = 1 or −1 means perfect linear relationship; r = 0 means no linear relationship (not no relationship) [^p02].

**Least squares regression line (LSRL)**: ŷ = a + bx where b = r · (s_y / s_x), a = ȳ − b·x̄. Minimizes the sum of squared residuals Σ(y_i − ŷ_i)² [^p03].

**Coefficient of determination**: r² = fraction of variability in y explained by x [^p03].

**Cautions for regression** [^p03]:
- Sensitive to outliers (LSRL changes substantially with one extreme point)
- Correlation ≠ causation
- Extrapolation outside the observed range is unreliable
- **Simpson's Paradox**: a trend in aggregate data can reverse when data are broken into subgroups (e.g., a school whose average test scores rise even though every grade level's scores fell, because grade distribution shifted toward higher grades)

## Part 2: Good Data

### Probability Theory

**Sample space** Ω: set of all possible outcomes. **Event**: a subset of Ω. **Probability model**: assigns P(E) ≥ 0 to each event E with P(Ω) = 1 [^p04].

**Finite equiprobable models**: P(E) = |E| / |Ω| [^p04].

**Complement**: P(A^c) = 1 − P(A). **Union**: P(A ∪ B) = P(A) + P(B) − P(A ∩ B) [^p04].

**Conditional probability**: P(A|B) = P(A ∩ B) / P(B). **Independence**: A and B are independent iff P(A ∩ B) = P(A)P(B) [^p04].

**Random variables**: a function from Ω to the real numbers. **Discrete RVs** have a probability distribution table (values and probabilities summing to 1) [^p04].

**Expected value**: E[X] = Σ x · P(X=x) [^p04].

**Continuous RV**: defined via a density function f(x) ≥ 0 with ∫ f = 1; P(a ≤ X ≤ b) = ∫_a^b f(x) dx [^p04].

**Normal distribution** N(µ, σ²): the bell curve; 68–95–99.7 rule; standard normal Z ~ N(0,1) via Z = (X − µ)/σ [^p04].

### Study Design

**Simple Random Sample (SRS)**: each set of n individuals in the population has equal probability of being chosen [^p05].

**Sampling methods** [^p05]:
- **Voluntary response bias**: self-selected samples over-represent strong opinions
- **Convenience sample**: easy-to-reach individuals; typically not representative
- **Stratified random sample**: divide population into strata; SRS within each stratum
- **Cluster sample**: randomly select geographic clusters; sample all individuals in chosen clusters

**Population parameter vs sample statistic**: a parameter (µ, σ) describes the population; a statistic (x̄, s) describes the sample and estimates the parameter [^p05].

**Observational study vs experiment**: observational studies cannot establish causation due to confounding variables; experiments use random assignment to treatment/control groups to isolate causal effects [^p05].

**Experimental design elements** [^p05]:
- **Control group**: receives no treatment or a placebo
- **Placebo effect**: improvement due to belief in treatment, not the treatment itself
- **Blinding**: subjects unaware of group assignment (single-blind); evaluators also unaware (double-blind)
- **Randomized Controlled Trial (RCT)**: double-blind + random assignment; gold standard for causation
- **Confounded lurking variable**: a variable correlated with both explanatory and response variables that is not controlled

**Research ethics** [^p05]:
- Do no harm (Hippocratic principle)
- Informed consent — participants must understand risks
- Confidentiality of data
- Institutional Review Board (IRB) oversight for human-subject research

## Part 3: Inferential Statistics

**Central Limit Theorem (CLT)**: for i.i.d. random variables X_1, ..., X_n with mean µ_X and standard deviation σ_X, the sample mean X̄ is approximately N(µ_X, σ_X/√n) for large n [^p06].

**Standard error**: σ_{X̄} = σ_X / √n; the standard deviation of the sampling distribution of the sample mean [^p06].

### Confidence Intervals

**Critical value z*_L**: the normal quantile such that P(µ − z*_L σ ≤ X ≤ µ + z*_L σ) = L for N(µ,σ) [^p06].

Useful table [^p06]:

| L | .80 | .90 | .95 | .99 | .999 |
|---|---|---|---|---|---|
| z*_L | 1.282 | 1.645 | 1.960 | 2.576 | 3.291 |

**Confidence interval** at level L: (x̄ − z*_L · σ_X/√n, x̄ + z*_L · σ_X/√n) [^p06].

**Correct interpretation**: confidence level L means that if the procedure is repeated many times with independent SRSs, a fraction L of the resulting intervals will contain µ_X. Any particular interval either does or does not contain µ_X — µ_X is fixed, the intervals move [^p06].

**Margin of error**: E = z*_L · σ_X/√n; the half-width of the confidence interval [^p06].

### Hypothesis Testing

**Formal steps** [^p06]:
1. State null hypothesis H_0 (the "nothing is happening" claim) and alternative H_a
2. Collect SRS data; compute a test statistic
3. Compute the **p-value**: P(observing data at least as extreme as ours | H_0 is true)
4. If p-value < significance level α, reject H_0; otherwise fail to reject H_0

**Test statistic for population mean**: z = (x̄ − µ_0) / (σ_X/√n) under H_0: µ = µ_0 [^p06].

**Significance levels**: α = 0.05 is the conventional threshold; α = 0.01 for stronger evidence [^p06].

**Type I error**: rejecting H_0 when it is true (false positive); probability = α. **Type II error**: failing to reject H_0 when it is false (false negative) [^p06].

**Cautions for hypothesis testing** [^p06]:
- Statistical significance ≠ practical significance (a tiny effect can be statistically significant with large n)
- Multiple testing: performing many tests at α = 0.05 leads to ~5% false discoveries even if all null hypotheses are true
- Publication bias: only significant results get published, inflating apparent effect sizes

## Connection to ML and Data Engineering

This textbook provides the applied statistics foundation for [/ai-engineering/statistics-for-ml.md](/ai-engineering/statistics-for-ml.md) and [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md):

- **Descriptive statistics**: the vocabulary for understanding data distributions before modeling
- **Regression**: direct precursor to ML regression; R² and residuals are universal concepts
- **CLT and sampling**: justifies why test/validation splits work and why large datasets enable reliable estimates
- **Confidence intervals**: used in A/B testing and evaluating ML model performance bounds
- **Hypothesis testing**: p-values, α levels, and Type I/II errors appear directly in ML evaluation frameworks and statistical significance testing for model comparisons

---

[^p01]: [Lies, Damned Lies, or Statistics — Part 01](../../../raw/pdf/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-01.md)
[^p02]: [Lies, Damned Lies, or Statistics — Part 02](../../../raw/pdf/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-02.md)
[^p03]: [Lies, Damned Lies, or Statistics — Part 03](../../../raw/pdf/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-03.md)
[^p04]: [Lies, Damned Lies, or Statistics — Part 04](../../../raw/pdf/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-04.md)
[^p05]: [Lies, Damned Lies, or Statistics — Part 05](../../../raw/pdf/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-05.md)
[^p06]: [Lies, Damned Lies, or Statistics — Part 06](../../../raw/pdf/pdf-lies-damned-lies-or-statistics-how-to-tell-the-tru-part-06.md)
