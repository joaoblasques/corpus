---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-01.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-02.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-03.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-04.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-05.md
    channel: pdf
    ingested_at: 2026-07-15
aliases:
  - KDD
  - knowledge discovery from data
  - knowledge discovery in databases
  - data mining pipeline
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-15
updated: 2026-07-15
---

# Data Mining

TL;DR: Data mining is the process of discovering interesting, non-trivial, and potentially useful patterns from large data repositories. It sits at the center of the KDD (Knowledge Discovery from Data) pipeline, which runs from raw data through preprocessing, transformation, mining, and interpretation. Core tasks include classification, regression, clustering, association rule mining, and outlier detection — each either descriptive or predictive.

## The KDD Pipeline

Data mining is one step in the broader **Knowledge Discovery from Data (KDD)** process [^src2]:

1. **Data cleaning** — remove noise, handle missing values, resolve inconsistencies.
2. **Data integration** — merge data from multiple sources (databases, flat files, data cubes).
3. **Data selection** — retrieve data relevant to the analysis task.
4. **Data transformation** — normalize, aggregate, or construct features for mining.
5. **Data mining** — apply algorithms to extract patterns.
6. **Pattern evaluation** — assess interestingness of discovered patterns (objective and subjective measures).
7. **Knowledge presentation** — visualize and communicate results.

The KDD view distinguishes data mining from the broader discovery process. In practice, the terms are used interchangeably [^src2].

## What Gets Mined: Data Types

Data mining applies to a wide range of repositories [^src2]:

- **Relational databases** — most common; SQL tables with records and attributes.
- **Data warehouses** — integrated, subject-oriented stores supporting OLAP; mined via multidimensional data cubes (see [/data-engineering/data-lake.md](/data-engineering/data-lake.md)).
- **Transactional data** — itemsets (market basket data); key input to association rule mining.
- **Complex types** — time series, sequences, graphs, spatial data, text, web data, streams.

## Core Mining Tasks

### Classification and Regression

**Classification** assigns records to predefined classes based on a model learned from labeled training data. **Regression** predicts a continuous value [^src2].

Learning methods covered in the textbook: decision trees (divide-and-conquer), Bayesian classifiers (probabilistic), support vector machines (margin maximization), neural networks, rule-based methods, ensemble methods (bagging, boosting, random forests) [^src1].

Classification is a **predictive** task — the goal is to predict the label of new, unseen records.

### Clustering

**Cluster analysis** groups similar objects into clusters without predefined labels (unsupervised). Clusters are formed so that intra-cluster similarity is high and inter-cluster similarity is low [^src2].

Methods: k-means (partition-based), DBSCAN (density-based), hierarchical agglomerative clustering, probabilistic/model-based clustering [^src1].

For detailed treatment of k-means and hierarchical clustering algorithms see [/ai-engineering/clustering-methods.md](/ai-engineering/clustering-methods.md). The data mining textbook additionally covers **DBSCAN** (density-reachability, noise handling) and hierarchical methods (BIRCH, CURE, CHAMELEON) beyond the statistical learning coverage [^src1].

### Association Rules and Frequent Pattern Mining

**Frequent pattern mining** discovers sets of items, sequences, or structures that appear frequently in a dataset [^src1]. The canonical form is the market basket problem: find all item sets appearing in ≥ support% of transactions.

**Apriori algorithm**: generate-and-test approach using the Apriori property — all subsets of a frequent itemset must themselves be frequent (antimonotonicity). Avoids exponential search space [^src1].

**FP-growth algorithm**: mines frequent itemsets without candidate generation by encoding the database in a compact prefix-tree (FP-tree) and using a divide-and-conquer strategy. Generally faster than Apriori on dense data [^src1].

**Association rules** derive from frequent itemsets: if X appears, then Y also appears, with confidence c and support s [^src2].

### Outlier Detection

**Outlier analysis** (anomaly detection) finds data objects that deviate substantially from the majority [^src2]. Three families of methods [^src1]:

- **Statistical** — model data distribution; outliers fall in low-probability regions.
- **Proximity-based** — outliers are far from their neighbors (distance-based and density-based variants; LOF = Local Outlier Factor uses local density ratios).
- **Clustering-based** — outliers belong to small or sparse clusters, or to no cluster at all.

Outlier detection is **descriptive** when used for exploration, and can be predictive when deployed to flag anomalies in new data.

### Characterization and Discrimination

- **Data characterization** — summarize general properties of a target class (e.g., statistical profiles, attribute-value frequency).
- **Data discrimination** — compare a target class against one or more contrasting classes to surface distinguishing features [^src2].

## Pattern Interestingness

Not every pattern discovered is useful. Interestingness has two dimensions [^src3]:

**Objective measures**: statistical thresholds computed from the data itself.
- **Support** — fraction of transactions containing the pattern.
- **Confidence** — conditional probability of the consequent given the antecedent (for rules).

**Subjective measures**: depend on user background and goals.
- **Unexpectedness** — pattern contradicts the user's prior beliefs.
- **Actionability** — user can act on the pattern for benefit.

A pattern is interesting only when it clears both thresholds and is novel to the user [^src3].

## Data Preprocessing

Chapter 3 of the textbook details the preprocessing steps that dramatically affect mining quality [^src4]:

**Attribute types** (Ch. 2): nominal (unordered categories), binary (two states), ordinal (ordered categories), numeric (interval/ratio). Each requires different handling for distance computation and algorithm choice [^src4].

**Descriptive statistics**: central tendency (mean, median, mode), dispersion (range, IQR, variance, standard deviation), graphic displays (boxplots, histograms, quantile-quantile plots, scatter plots) [^src4].

**Proximity and similarity measures**: data matrix (n×p feature representation) vs. dissimilarity matrix (n×n pairwise distances). Key metrics [^src5]:

| Attribute type | Distance / similarity |
|---|---|
| Numeric | Minkowski distance (p=1: Manhattan; p=2: Euclidean; p→∞: supremum) |
| Binary (symmetric) | Simple matching coefficient |
| Binary (asymmetric) | Jaccard coefficient (ignores 0-0 co-absence) |
| Ordinal | Rank-transform → Minkowski |
| Mixed | Weighted combination of type-specific dissimilarities |
| Sparse term vectors | Cosine similarity (inner product / product of norms) |

## OLAP vs Data Mining

Data warehousing and OLAP (Online Analytical Processing) are closely related but distinct from data mining [^src2]:

| | OLAP | Data Mining |
|---|---|---|
| Query | User-specified; known hypotheses | Algorithm-driven; unknown patterns |
| Output | Aggregated summaries (drill-down, roll-up) | Rules, models, clusters, anomalies |
| Interaction | Interactive, human-guided | Batch or semi-automatic |
| Data model | Multidimensional cube (star/snowflake schema) | Same cubes + raw data |

**Multidimensional data mining** combines both: mine patterns across combinations of dimensions at varying abstraction levels using data cube space — for example, finding association rules that hold in certain market segments or time windows [^src3].

Data warehousing integration with data mining is covered in the [/data-engineering/data-lake.md](/data-engineering/data-lake.md) and [/data-engineering/dimensional-modeling.md](/data-engineering/dimensional-modeling.md) corpus pages.

## Technologies Underlying Data Mining

Data mining is multidisciplinary, drawing from [^src3]:

- **Statistics** — sampling theory, significance testing, regression, Bayesian reasoning.
- **Machine learning** — supervised, unsupervised, semi-supervised, and active learning paradigms; deep learning.
- **Database systems** — efficient query processing, indexing, data cube computation.
- **Information retrieval** — text mining, web mining, inverted indexes.

## Major Open Challenges (per 2011 textbook)

**Efficiency and scalability**: algorithms must run on terabyte-to-petabyte datasets. Solutions: parallel/distributed mining, incremental algorithms, approximate methods, cloud computing [^src3].

**Diversity of data types**: a single algorithm rarely generalizes across relational, spatial, temporal, text, graph, and stream data. Specialized algorithms per type are common.

**Data mining and society**: privacy-preserving data mining is a non-trivial research area. Mining behavioral data raises ethical questions about surveillance, profiling, and consent [^src3].

## Source Summary

Full book-level treatment: [/data-engineering/sources/data-mining-han-kamber-pei.md](/data-engineering/sources/data-mining-han-kamber-pei.md)

---

[^src1]: [Data Mining: Concepts and Techniques, Part 1 (TOC and structure)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-01.md)
[^src2]: [Data Mining: Concepts and Techniques, Part 2 (Ch. 1 Introduction)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-02.md)
[^src3]: [Data Mining: Concepts and Techniques, Part 3 (Ch. 1 continued — interestingness, technologies, challenges)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-03.md)
[^src4]: [Data Mining: Concepts and Techniques, Part 4 (Ch. 2 — attribute types and statistics)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-04.md)
[^src5]: [Data Mining: Concepts and Techniques, Part 5 (Ch. 2 — proximity measures)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-05.md)
