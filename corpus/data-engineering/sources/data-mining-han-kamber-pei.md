---
type: source
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
  - Han Kamber Pei data mining
  - Data Mining Concepts and Techniques 3rd edition
tags:
  - corpus/data-engineering
  - source
created: 2026-07-15
updated: 2026-07-15
---

# Data Mining: Concepts and Techniques (Han, Kamber, Pei — 3rd ed., 2011)

TL;DR: The canonical academic textbook on data mining. 740 pages across 13 chapters covering the full spectrum from data preprocessing and warehousing through pattern mining, classification, clustering, outlier detection, and research frontiers. Draws on statistics, machine learning, and database systems. Widely used in university courses.

## Bibliographic Details

- **Authors**: Jiawei Han, Micheline Kamber, Jian Pei
- **Publisher**: Morgan Kaufmann (Elsevier), 3rd edition
- **Year**: 2011 (copyright 2012)
- **Pages**: 740
- **Scope**: Introductory-to-advanced undergraduate/graduate textbook

## Structure

The book is organized into 13 chapters progressing from foundations to advanced methods [^src1]:

| Chapter | Topic |
|---|---|
| 1 | Introduction — KDD pipeline, mining tasks, technologies, open problems |
| 2 | Getting to Know Your Data — attribute types, statistics, visualization, proximity measures |
| 3 | Data Preprocessing — cleaning, integration, transformation, reduction |
| 4 | Data Warehousing and OLAP — star/snowflake schemas, OLAP operations |
| 5 | Data Cube Technology — cube computation, iceberg cubes, OLAP mining |
| 6 | Frequent Pattern Mining — Apriori, FP-growth, association rules |
| 7 | Advanced Pattern Mining — constraint-based, sequential, structured patterns |
| 8 | Classification: Basic Concepts — decision trees, Bayes classifiers, model evaluation |
| 9 | Classification: Advanced Methods — SVM, neural networks, ensemble methods |
| 10 | Cluster Analysis: Basic Concepts — k-means, DBSCAN, hierarchical clustering |
| 11 | Advanced Cluster Analysis — density/grid/probabilistic methods |
| 12 | Outlier Detection — statistical, proximity-based, clustering-based |
| 13 | Trends and Research Frontiers |

## Key Concepts by Chapter

### Chapter 1: Introduction and KDD Pipeline

Data mining = extraction of interesting (non-trivial, implicit, previously unknown, potentially useful) patterns from large data sets [^src2]. Positioned within the KDD (Knowledge Discovery from Data) process: data cleaning → integration → selection → transformation → mining → evaluation → presentation.

Mining tasks split into **descriptive** (characterize data, e.g., clustering, association) and **predictive** (use history to forecast, e.g., classification, regression) [^src2].

Pattern interestingness requires both objective thresholds (support, confidence) and subjective relevance (unexpectedness, actionability) [^src3].

Underlying technologies: statistics (sampling, Bayesian, regression), machine learning (supervised/unsupervised/semi-supervised/active), database systems (OLAP, query processing), information retrieval [^src3].

Open challenges: efficiency/scalability, data diversity, privacy-preserving mining, societal impact [^src3].

### Chapter 2: Getting to Know Your Data

**Attribute taxonomy** [^src4]:
- Nominal — unordered categories (e.g., eye color, zip code).
- Binary — two states; symmetric (both states equally important) vs. asymmetric (presence is rare/informative, e.g., disease).
- Ordinal — ordered but spacing undefined (e.g., education level, satisfaction rating).
- Numeric — interval (no true zero) or ratio (true zero, multiplicative interpretation).

**Central tendency**: mean, weighted mean, trimmed mean (robust to outliers), median (better for skewed distributions), mode (most frequent value, possibly multimodal).

**Dispersion**: range, IQR (Q3 − Q1), variance, standard deviation, coefficient of variation. Boxplot displays median + IQR + whiskers + outlier points [^src4].

**Visualization**: quantile plots, Q-Q plots, histograms, scatter plots for 2D; pixel-oriented techniques (one pixel per value ordered by some attribute), geometric projection (parallel coordinates for high-dimensional), icon-based (Chernoff faces, star glyphs), hierarchical (treemaps) [^src4].

**Proximity measures** [^src5]:
- Dissimilarity matrix (n×n) vs. data matrix (n×p).
- Minkowski distance: L^h = (sum |x_i − y_i|^h)^(1/h). h=1 → Manhattan; h=2 → Euclidean; h→∞ → supremum (max coordinate difference).
- Jaccard coefficient for asymmetric binary: |A∩B| / |A∪B| — ignores 0-0 pairs.
- Cosine similarity for term-frequency vectors: cos(θ) = X·Y / (||X|| · ||Y||). Range [0,1] for non-negative inputs.
- Mixed-type objects: normalize each attribute to [0,1], combine via weighted average with type-appropriate similarity.

## Relationship to Corpus Pages

The book's content maps directly to several corpus concept pages:

- **KDD pipeline, mining tasks, interestingness** → [/data-engineering/data-mining.md](/data-engineering/data-mining.md) (primary synthesis page)
- **Clustering (k-means, DBSCAN, hierarchical)** → [/ai-engineering/clustering-methods.md](/ai-engineering/clustering-methods.md) (cross-domain; statistical learning angle extends this book's treatment)
- **Data warehousing and OLAP** → [/data-engineering/data-lake.md](/data-engineering/data-lake.md), [/data-engineering/dimensional-modeling.md](/data-engineering/dimensional-modeling.md)
- **Data preprocessing and quality** → [/data-engineering/data-quality.md](/data-engineering/data-quality.md)

## Coverage Assessment

Parts 1–5 (this ingest) cover Ch. 1 introduction and Ch. 2 data familiarity topics through proximity measures. Chapters 3–13 (preprocessing, warehousing, cube technology, pattern mining, classification, advanced clustering, outlier detection, frontiers) are in parts 6–39 of the PDF but were not ingested in this batch. Remaining parts should be queued for follow-up ingest to fully populate classification, association rules, outlier detection, and OLAP corpus pages.

---

[^src1]: [Data Mining: Concepts and Techniques, Part 1 (TOC and structure)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-01.md)
[^src2]: [Data Mining: Concepts and Techniques, Part 2 (Ch. 1 — KDD pipeline and tasks)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-02.md)
[^src3]: [Data Mining: Concepts and Techniques, Part 3 (Ch. 1 — interestingness, technologies, challenges)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-03.md)
[^src4]: [Data Mining: Concepts and Techniques, Part 4 (Ch. 2 — attribute types and statistics)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-04.md)
[^src5]: [Data Mining: Concepts and Techniques, Part 5 (Ch. 2 — proximity measures)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-05.md)
