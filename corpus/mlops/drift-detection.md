---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/web/choosing-univariate-drift-detection-methods.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - drift detection
  - data drift
  - distribution shift
  - univariate drift detection
  - drift detection methods
  - covariate shift
  - model monitoring
  - distance metrics for drift
tags:
  - corpus/mlops
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Drift Detection

**TL;DR**: Drift detection is the monitoring discipline of comparing a production **analysis** sample against a fixed **reference** sample to spot distribution shift in model inputs (and outputs) [^src1]. For **univariate** drift, each feature is monitored with a distance metric or statistical test chosen for the variable's type (categorical vs. continuous) and distribution [^src1]. There is no one-size-fits-all method: each metric has characteristic blind spots, so method choice is a tradeoff. The practical defaults are **Jensen-Shannon** or **Wasserstein** for continuous features, and **Jensen-Shannon** or **L-Infinity** for categorical features [^src1].

The reference/analysis split is the core construct: all methods below "compare two samples of data — one of which we call a reference sample and the other an analysis sample" [^src1].

## Method selection cheat sheet

| Method | Categorical | Continuous | Recommended use | Key weakness |
|---|---|---|---|---|
| Jensen-Shannon | Yes | Yes | Versatile default | Does not differentiate very strong vs. extreme drifts (overlap-based, caps at 1) [^src1] |
| Hellinger | Yes | Yes | Medium-strength shifts | Breaks down in extreme shifts (also overlap-based) [^src1] |
| Wasserstein | No | Yes | When magnitude of shift matters | Sensitive to outliers [^src1] |
| L-Infinity | Yes | No | Many categories | Sensitive to big change in one category (by design) [^src1] |
| Kolmogorov-Smirnov (KS) | No | Yes | Statistical significance | False positives; insensitive to changes in tails [^src1] |
| Chi-2 | Yes | No | Statistical significance | False positives; value is a function of sample size [^src1] |

## Two families: overlap vs. transport

The continuous metrics split into two conceptual families, which explains most of their tradeoffs:

- **Overlap-based** (Jensen-Shannon, Hellinger): tied to the amount of overlap between the two probability distributions [^src1]. Bounded in `[0, 1]`. **Failure mode**: once distributions are completely disjoint, both "will be maxed out at 1" and stop increasing even as the distributions move further apart [^src1]. They also miss shifts where overlap stays constant but the distribution moves [^src1].
- **Transport-based** (Wasserstein): "can be thought of as the amount of work ... that it would take to transform one distribution into the other" [^src1]. Range `[0, ∞)`, so it keeps growing with the distance moved — it catches disjoint-and-separating drift that overlap metrics miss [^src1]. Cost: extreme sensitivity to outliers (moving one point to an extreme value inflates it while other metrics are unaffected) [^src1].

The disjoint-distribution edge case is the same one that motivates **Wasserstein-based GAN loss functions** [^src1] — a `uses` link from generative-model training back to this transport idea.

## Continuous-variable behavior

- **Mean shift**: Wasserstein changes proportionally to the mean shift; JS and KS are relatively more sensitive to small shifts than large ones; Hellinger is sigmoid-shaped (least sensitive to small and large changes, most to medium) [^src1].
- **Std-dev shift**: Wasserstein again scales proportionally; JS, KS, and Hellinger are all highly sensitive even to small changes, with JS the most stable of the three [^src1].
- **KS blind spot (ECDF-max)**: the KS D-statistic is "the maximum distance between the empirical cumulative density functions (ECDFs) of the two analyzed samples" [^src1]. Drift in one region of the distribution can hide drift in another, and a bimodal shift in only one mode can leave the max-ECDF gap unchanged — making KS insensitive there while Wasserstein (area between ECDFs) still catches it [^src1].

## Categorical-variable behavior

- **Sample-size stability**: JS, Hellinger, and L-Infinity return the same value for the same drift magnitude regardless of sample size; the **Chi-Squared statistic does not** — it grows with sample size, which matters with unequal-sized chunks (e.g. period-based chunking) [^src1].
- **Number of categories**: JS, Hellinger, and Chi-2 grow as the category count rises (summed sampling noise across many terms), while **L-Infinity does not** because it only looks at the single largest frequency change [^src1].
- **Many categories / few-category drift**: when drift hits only a few of many categories, summing metrics (JS, Hellinger, Chi-2) let sampling noise hide the real shift; **L-Infinity flags it** because it ignores the summed small differences [^src1]. So "when dealing with data sets with many categories, using the L-infinity distance may help to reduce false-positive alerts" [^src1].

## Recommended defaults (TLDR)

- **Continuous**: Jensen-Shannon or Wasserstein [^src1]. JS is bounded `[0,1]` and more sensitive to small drift (more false alarms but catches low-magnitude meaningful drift); Wasserstein is unbounded and more outlier-sensitive [^src1].
- **Categorical**: Jensen-Shannon generally; **L-Infinity when you have many categories** and care about changes to even one of them [^src1].

> [unsourced — please verify] This source covers univariate drift only; multivariate drift detection (e.g. reconstruction-error / domain-classifier methods) is a separate technique not addressed here.

## See also

- [[mlops/python|Python]] — these metrics are typically computed in Python monitoring libraries (the source is NannyML's docs)
- [[mlops/README|MLOps hub]] — model monitoring sits in the deploy/operate layer of the ML lifecycle
- [[data-engineering/README|Data Engineering]] — data-quality checks on pipelines are the upstream cousin of drift monitoring on model inputs

---

[^src1]: [Choosing Univariate Drift Detection Methods (NannyML)](../../raw/web/choosing-univariate-drift-detection-methods.md)
