---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-20.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-21.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-22.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-23.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-24.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-25.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-26.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-27.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-28.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-29.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-30.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-31.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-32.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-33.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-34.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-35.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-36.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-37.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-38.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-39.md
    channel: pdf
    ingested_at: 2026-07-16
aliases:
  - Han Kamber Pei Ch 8-13
  - Data Mining Concepts and Techniques classification clustering outlier
tags:
  - corpus/data-engineering
  - source
created: 2026-07-16
updated: 2026-07-16
---

# Data Mining: Concepts and Techniques — Chapters 8–13 (Han, Kamber, Pei)

TL;DR: Continuation of the Han/Kamber/Pei textbook (3rd ed., 2011). Chapters 8–9 cover classification algorithms from decision trees through SVMs, neural networks, and ensemble methods. Chapters 10–11 cover cluster analysis from k-means through DBSCAN, hierarchical methods, and advanced probabilistic/spectral clustering. Chapter 12 covers outlier detection. Chapter 13 surveys research frontiers (social networks, privacy, recommender systems). Parts 36–39 are bibliography and index.

This source continues from [/data-engineering/sources/data-mining-han-kamber-pei.md](/data-engineering/sources/data-mining-han-kamber-pei.md) (which covers Ch. 1–5).

## Chapter 8: Classification — Basic Concepts

### Decision Tree Induction

The standard algorithm for decision tree classification partitions the training data recursively using an **attribute selection measure** to choose the best splitting attribute at each node [^src1].

Three major measures:

| Measure | Formula basis | Preferred by |
|---|---|---|
| **Information gain** | Shannon entropy reduction | ID3, C4.5 |
| **Gain ratio** | Info gain normalized by split info | C4.5 (bias correction for multivalued attrs) |
| **Gini index** | Impurity measure (1 − Σpᵢ²) | CART |

**Overfitting prevention** via **pruning**:
- *Pre-pruning*: stop growing when threshold criteria not met.
- *Post-pruning*: grow full tree, then prune using validation set or MDL criterion.

### Naïve Bayesian Classifier

Assumes class-conditional independence of attributes: P(**X**|Cᵢ) = Π P(xₖ|Cᵢ). Then classifies by maximum posterior probability P(Cᵢ|**X**) ∝ P(**X**|Cᵢ)·P(Cᵢ) [^src2].

**Laplacian correction**: add 1 to each count to avoid zero probabilities when a class-value combination is absent from training data. Small correction for large databases, eliminates zero-probability problem [^src2].

### Model Evaluation Metrics

Confusion matrix metrics [^src3]:

| Metric | Definition |
|---|---|
| Accuracy | (TP + TN) / (P + N) |
| Sensitivity / Recall | TP / P |
| Specificity | TN / N |
| Precision | TP / (TP + FP) |
| F (F1 score) | 2·Precision·Recall / (Precision+Recall) |

**ROC curves**: plot TPR (sensitivity) vs. FPR (1-specificity) as the decision threshold varies. Area under the ROC curve (AUC) measures overall classifier accuracy — model-agnostic and threshold-free [^src3].

**Cross-validation**: k-fold CV is the recommended evaluation method. Stratified 10-fold CV is the standard (Kohavi 1995). Bootstrapping works better for small datasets (63.2% of tuples appear in each bootstrap sample) [^src3].

**t-test for model comparison**: pairwise t-test on k cross-validation rounds to determine whether difference in mean error rates is statistically significant vs. attributable to chance [^src3].

## Chapter 9: Classification — Advanced Methods

### Support Vector Machines (SVM)

Finds the **maximum marginal hyperplane** — the hyperplane with maximum distance (margin) from the nearest training points of each class (the **support vectors**). Only support vectors determine the boundary; all other points are irrelevant [^src4].

For linearly inseparable data: use **kernel functions** to map into higher-dimensional space where linear separation is possible. Common kernels: polynomial, Gaussian (RBF), sigmoid. The kernel trick avoids computing the explicit high-dimensional mapping.

### Genetic Algorithms

Evolve rule populations using crossover and mutation operators. Fitness = classification accuracy on training tuples. Useful for classification and optimization; easily parallelizable [^src5].

### Rough Sets

Handles imprecise or noisy data via **equivalence classes**. For each class C, defines a **lower approximation** (tuples certainly in C) and **upper approximation** (tuples possibly in C). Applies only to discrete-valued attributes; continuous values must be discretized first [^src5].

### Ensemble Methods

- **Bagging**: train k classifiers on k bootstrap samples; majority vote.
- **Boosting**: iteratively reweight misclassified examples; AdaBoost is the standard.
- **Random forests**: bag + random feature subsets at each split. The dominant ensemble method in practice.

## Chapter 10: Cluster Analysis — Basic Concepts

**Clustering** = unsupervised partitioning of objects into groups with high intra-cluster similarity and low inter-cluster similarity [^src6].

### k-Means (Partition-Based)

1. Randomly initialize k cluster centroids.
2. Assign each object to nearest centroid.
3. Recompute centroids as mean of assigned objects.
4. Repeat until convergence.

Weakness: sensitive to initialization; requires k to be specified; converges to local minimum; works poorly for non-convex clusters and clusters of different sizes/densities.

**k-Means++**: smart initialization — select centroids with probability proportional to distance from already-chosen centroids. Reduces iterations and improves final quality.

### Hierarchical Methods

Build a tree (dendrogram) of nested clusters [^src7]:

**Agglomerative (bottom-up)**: start with each object as its own cluster; repeatedly merge the two closest clusters until one cluster remains. Four linkage measures:
- Single-link (min distance) — elongated chains
- Complete-link (max distance) — more compact, rounded clusters  
- Average-link — compromise
- Centroid — distance between cluster means

**Divisive (top-down)**: start with all objects in one cluster, split recursively. Computationally expensive (2^(n-1)−1 possible binary splits for n objects).

### DBSCAN (Density-Based)

Clusters are regions of high density separated by low-density regions. Discovers arbitrary-shaped clusters; noise-robust; parameter-free (given ε and MinPts):
- **Core point**: has ≥ MinPts neighbors within radius ε.
- **Border point**: reachable from a core point but not itself a core point.
- **Noise point**: neither core nor border.

## Chapter 11: Advanced Cluster Analysis

### Probabilistic/Model-Based

**Gaussian Mixture Models**: assume data generated from a mixture of K Gaussians. Estimate parameters via **EM (Expectation-Maximization)**: E-step assigns each point a soft probability of belonging to each Gaussian; M-step re-estimates Gaussian parameters from soft assignments. Generalizes k-means (which is hard-assignment EM).

### High-Dimensional Clustering

Standard distance measures lose meaning in high dimensions (the **curse of dimensionality**) [^src8]:

**Subspace clustering**: search for clusters existing in subspaces of the original high-dimensional space. Methods: CLIQUE (grid-based), PROCLUS (projected clustering).

**Biclustering**: simultaneously cluster objects and attributes. Useful for gene expression analysis where different genes are co-regulated only under certain conditions. Four types: constant-value, constant-row/column, coherent-values, coherent-evolution biclusters.

**Spectral clustering**: use eigendecomposition of an affinity/Laplacian matrix to project data into a new space where clusters separate cleanly. Handles non-convex clusters that k-means cannot. Equivalent to clustering in a derived low-dimensional space [^src8].

## Chapter 12: Outlier Detection

**Outliers** are data objects that deviate substantially from the majority. Three families [^src9]:

### Statistical Methods

Model data distribution (Gaussian, mixture) and flag low-probability regions as outliers. **Kernel density estimation** (KDE): non-parametric probability density estimate using a kernel function (e.g., Gaussian). An object is an outlier if its density estimate f̂(o) is below a threshold. Bandwidth h controls smoothing — too small → high FP rate; too large → high FN rate [^src9].

### Proximity-Based Methods

**Distance-based outliers**: object o is a top-k outlier if distance to its k-nearest neighbor is large.

**LOF (Local Outlier Factor)**: density-based; compares local density of o to densities of its neighbors. LOF > 1 means o is in a sparser region than its neighbors — likely an outlier. Handles variable-density data that distance-based methods cannot [^src9].

### Clustering-Based Methods

Objects in small, sparse clusters or unassigned to any cluster are outliers.

### High-Dimensional Outlier Detection

Standard proximity measures degrade in high dimensions (all distances converge). **HilOut** uses ranks of distances rather than absolute distances. **Subspace outlier detection**: find outliers that are anomalous in certain subspaces but not in the full space [^src10].

## Chapter 13: Trends and Research Frontiers

- **Web and social network mining**: link prediction, community detection, SimRank similarity, HITS/PageRank authority measures.
- **Recommender systems**: memory-based (k-NN with Pearson/cosine similarity) and model-based (matrix factorization, Bayesian networks). Cold-start problem, scalability.
- **Data mining and privacy**: privacy-preserving data mining, k-anonymity, ℓ-diversity. Data mining is "ubiquitous and invisible" in daily life (store inventory, ad targeting, fraud detection) [^src11].
- **Biological and scientific data**: mining microarray gene expression, protein structures, DNA sequences, scientific computing logs.

## Relationship to Corpus Pages

- Primary synthesis: [/data-engineering/data-mining.md](/data-engineering/data-mining.md)
- Classification algorithms: [/ai-engineering/classification-methods.md](/ai-engineering/classification-methods.md)
- Clustering algorithms: [/ai-engineering/clustering-methods.md](/ai-engineering/clustering-methods.md)
- OLAP and data warehousing: [/data-engineering/olap.md](/data-engineering/olap.md)
- Frequent pattern mining: [/data-engineering/frequent-pattern-mining.md](/data-engineering/frequent-pattern-mining.md)
- Full book bibliographic source (Ch. 1–5): [/data-engineering/sources/data-mining-han-kamber-pei.md](/data-engineering/sources/data-mining-han-kamber-pei.md)

---

[^src1]: [Data Mining: C&T Part 20 — Ch. 8 decision tree, attribute selection measures (info gain, Gini)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-20.md)
[^src2]: [Data Mining: C&T Part 21 — Ch. 8 Naïve Bayes classifier, Laplacian correction](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-21.md)
[^src3]: [Data Mining: C&T Part 22 — Ch. 8 model evaluation (bootstrap, t-test, ROC curves)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-22.md)
[^src4]: [Data Mining: C&T Part 25 — Ch. 9 advanced classification (genetic algorithms, rough sets)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-25.md)
[^src5]: [Data Mining: C&T Part 25 — Ch. 9 advanced classification methods](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-25.md)
[^src6]: [Data Mining: C&T Part 26 — Ch. 10 cluster analysis overview, requirements, k-means](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-26.md)
[^src7]: [Data Mining: C&T Part 27 — Ch. 10 hierarchical clustering, dendrogram, linkage measures](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-27.md)
[^src8]: [Data Mining: C&T Part 30–31 — Ch. 11 advanced cluster analysis (spectral, subspace, biclustering)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-30.md)
[^src9]: [Data Mining: C&T Part 32 — Ch. 12 outlier detection (statistical methods, KDE, LOF)](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-32.md)
[^src10]: [Data Mining: C&T Part 33 — Ch. 12 high-dimensional outlier detection](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-33.md)
[^src11]: [Data Mining: C&T Part 35 — Ch. 13 recommender systems, data mining and society](../../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-35.md)
