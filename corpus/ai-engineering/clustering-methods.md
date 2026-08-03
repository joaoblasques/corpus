---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-20.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-21.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/pdf/pdf-foundations-of-data-science-part-01.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-09.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-10.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - clustering
  - K-means clustering
  - hierarchical clustering
  - dendrogram
  - unsupervised clustering
  - Suffix Tree Clustering
  - STC
  - Buckshot clustering
  - document clustering
  - cluster hypothesis
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-09
updated: 2026-08-03
---

# Clustering Methods

TL;DR: Clustering partitions observations into homogeneous subgroups without labeled responses. Two dominant approaches: **K-means** (requires pre-specifying K, finds local optimum via centroid reassignment) and **hierarchical clustering** (builds a tree/dendrogram bottom-up, does not require K upfront). Both are sensitive to dissimilarity measure, scaling, and choice of linkage (hierarchical). Results should be treated as exploratory starting points, not ground truth.

## The Unsupervised Learning Challenge

Clustering is part of **unsupervised learning** — no response variable Y is available. Goals are exploratory: discover subgroups, visualize structure, generate hypotheses. This contrasts with supervised learning where cross-validation objectively measures model quality [^src1].

**PCA vs clustering**: both simplify data, but differently. PCA finds a low-dimensional representation explaining variance; clustering finds homogeneous partitions of observations [^src1].

**Applications**: cancer subtype discovery (gene expression profiles), market segmentation, search engine personalization.

## K-Means Clustering

**Setup**: partition n observations into K non-overlapping clusters C_1, ..., C_K such that every observation belongs to exactly one cluster [^src1].

**Objective**: minimize total within-cluster variation:

```
minimize over C_1,...,C_K:  sum_k W(C_k)
```

where W(C_k) = (1/|C_k|) * sum_{i,j in C_k} ||x_i - x_j||^2  (squared Euclidean distance) [^src1].

**Algorithm (Algorithm 10.1)**:
1. Randomly assign each observation to one of K clusters.
2. Iterate until assignments stop changing:
   a. For each cluster, compute the centroid (mean vector of length p).
   b. Assign each observation to the cluster whose centroid is closest (Euclidean distance).

**Convergence**: guaranteed to decrease the objective at each step (by the identity that the within-cluster sum of squares equals twice the sum of squared distances from each point to its centroid). Converges to a local optimum, not necessarily global [^src1].

**Local optima**: different random initializations yield different solutions. **Recommendation: run with many random starts (nstart=20 or 50) and select the result with smallest total within-cluster sum of squares** [^src1].

**Selecting K**: not simple. Must be pre-specified; the problem of choosing K is non-trivial and has no universally accepted solution. Common heuristics: elbow in the within-cluster SS vs K plot; domain knowledge.

## Hierarchical Clustering

Hierarchical clustering avoids pre-specifying K by building a full tree structure (**dendrogram**) that can be cut at any height to obtain any number of clusters [^src1].

**Bottom-up (agglomerative) algorithm (Algorithm 10.2)**:
1. Start with n clusters (one per observation). Compute all n(n-1)/2 pairwise dissimilarities.
2. Fuse the two most similar clusters into one. Record fusion height in the dendrogram.
3. Recompute pairwise dissimilarities among the n-1 clusters. Repeat until one cluster remains.

**Reading a dendrogram**:
- **Vertical position of fusion = dissimilarity** between fused groups. Low fusion = similar; high fusion = dissimilar.
- **Horizontal position is meaningless**. Two leaves close horizontally may be very dissimilar if their fusion is high on the tree. "Proximity on x-axis does not imply similarity" is the most common misreading [^src1].
- **Cut the dendrogram at a given height** to obtain clusters. Height controls the number of clusters (same role as K in K-means) [^src2].

## Linkage

**Linkage** defines how inter-cluster dissimilarity is computed when one or both clusters contain multiple observations [^src1]:

| Linkage | Rule |
|---|---|
| Complete | Maximum pairwise dissimilarity between A and B. Tends to produce balanced dendrograms. Preferred. |
| Average | Mean pairwise dissimilarity between A and B. Generally preferred. |
| Single | Minimum pairwise dissimilarity. Can produce "trailing" chains where single observations fuse one-by-one. Usually avoided. |
| Centroid | Dissimilarity between cluster centroids. Can produce **inversions** (a cluster fused below its components) — avoid in practice. |

Complete and average linkage are generally preferred; they yield more compact, balanced clusters [^src2].

## Choice of Dissimilarity Measure

**Euclidean distance**: most common. Measures absolute magnitude differences. High-volume shoppers cluster together regardless of purchase preferences [^src1].

**Correlation-based distance**: 1 - cor(x_i, x_j). Two observations are similar if their feature profiles are highly correlated (same shape), regardless of magnitude. Useful when the pattern matters more than the level (e.g., shoppers with the same purchase preferences regardless of purchase volume) [^src1].

**Scaling**: if variables have different units or variances, scale to standard deviation 1 before computing dissimilarities. Otherwise, variables with large variance dominate. (Same issue as in PCA — see [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md)) [^src1].

## Practical Issues

**Small decisions, big consequences**: dissimilarity measure, linkage, scaling, and K (or cut height) each strongly affect results. No single right choice — try several and look for consistent patterns [^src1].

**Validating clusters**: difficult in practice. Clusters will always be found even in pure noise. No universally accepted method for assigning a p-value to a cluster. Technique: re-cluster subsets of data to assess robustness [^src1].

**Outlier sensitivity**: both K-means and hierarchical clustering force every observation into a cluster. Outliers can severely distort results. Mixture models (soft K-means) handle outliers more gracefully [^src1].

**Non-robustness**: removing a small random subset of observations can substantially change the clustering. Treat results as exploratory hypotheses requiring independent validation [^src1].

**Hierarchical structure assumption**: hierarchical clustering imposes nested clusters. If the true structure is non-nested (e.g., best two-cluster split is by gender; best three-cluster split is by nationality), hierarchical clustering may perform worse than K-means [^src1].

## R Lab (ISL)

**K-means** (ISL Lab 2):
```r
set.seed(2)
km.out <- kmeans(x, 2, nstart=20)   # nstart=20: multiple random starts
km.out$cluster                        # cluster assignments
km.out$tot.withinss                   # total within-cluster SS (minimize this)
```

**Hierarchical clustering** (ISL Lab 2):
```r
hc.complete <- hclust(dist(x), method="complete")
hc.average  <- hclust(dist(x), method="average")
hc.single   <- hclust(dist(x), method="single")
plot(hc.complete)                     # plot dendrogram
cutree(hc.complete, 2)               # cut to get 2 clusters
```

**Correlation-based distance**:
```r
dd <- as.dist(1 - cor(t(x)))         # requires at least 3 features
hclust(dd, method="complete")
```

**NCI60 cancer example**: hierarchical clustering with complete linkage + Euclidean distance on 6,830-gene profiles of 64 cancer cell lines. Cell lines of the same cancer type cluster together (though imperfectly). Cutting at 4 clusters: all leukemia lines fall in one cluster; breast cancer lines spread across three [^src2].

**PCA + clustering**: perform clustering on the first few PC score vectors instead of the raw data. Treats PCA as a denoising step; often yields cleaner clusters [^src2].

## Spectral Clustering (Blum/Hopcroft/Kannan)

Spectral clustering handles non-convex cluster shapes by leveraging the **graph Laplacian**. Unlike k-means (which assumes convex clusters), spectral methods can separate rings, crescents, or clusters connected by thin bridges [^src_bhk].

**Algorithm**:
1. Build a similarity graph on the data (k-nearest-neighbor or ε-ball).
2. Compute the normalized graph Laplacian L = I - D⁻¹/²AD⁻¹/² (A = adjacency, D = degree diagonal).
3. Take the top-k eigenvectors of L; this embeds each node as a k-dimensional vector.
4. Run k-means on the embedded vectors.

**Why eigenvectors?** The Fiedler vector (second eigenvector) minimizes the graph **conductance** — the ratio of edge weight crossing the cut to the total edge weight on the smaller side. Minimizing conductance finds the best balanced partition [^src_bhk].

**Approximation stability**: BHK show that if the true k-clustering has a large approximation-stability margin (any other k-clustering with similar cost differs in a bounded number of points), then spectral clustering recovers the true partition even under perturbation [^src_bhk].

**Limitation**: spectral clustering is O(n³) naively (eigendecomposition); for large n, power-method or sparse-Laplacian tricks are needed. K-means remains preferred when clusters are roughly spherical [^src_bhk].

## Document Clustering for Information Retrieval

Document clustering applies the same methods above to text collections, with the goal of supporting browsing, navigation, and retrieval. The **cluster hypothesis** (van Rijsbergen, 1979): documents that are similar tend to be relevant to the same queries — so retrieving one relevant document and expanding to its cluster should yield additional relevant documents [^irsrc9].

### Agglomerative Hierarchical Clustering (AHC) for documents

Same algorithm as above, applied to document-document cosine similarity matrices. IR-specific linkage behavior [^irsrc9]:

| Linkage | IR property |
|---|---|
| **Single-link** ("nearest neighbor") | Produces large, loose, "straggly" clusters; connected by chains of single high-similarity links; two documents in the same cluster are not guaranteed to be above the threshold |
| **Complete-link** | Produces small, tight, cohesive clusters; every pair in a cluster is above the similarity threshold; better suited to IR |
| **Group-average** | Intermediate: each member has greater average similarity to its own cluster than to any other |
| **Ward's method** | Minimizes total within-cluster Euclidean distance increase at each merge |

Complete-link clustering is O(N²) in time with O(N²) space; with O(N) space it requires O(N³) time [^irsrc9].

### Heuristic clustering for large collections

For collections of thousands of documents or more, O(N²) methods are impractical. Heuristic methods run in O(kN) (rectangular) time by sacrificing some theoretical guarantees [^irsrc9]:

- **Buckshot** (Cutting et al., SIGIR 1992): apply a complete O(N²) AHC method to a random sample of √(kN) documents to obtain k seed clusters; then assign all N documents to the nearest seed in O(kN) time. Non-deterministic (results vary with random sample).
- **Fractionation**: partition the corpus into N/m buckets of m documents each; cluster each bucket to mr centroids; treat centroids as new documents and repeat until k clusters remain. Applies AHC to the whole corpus but coarsely (in buckets); deterministic.
- Both support O(kN log N) hierarchical clustering by iterative application.

### Suffix Tree Clustering (STC) — incremental, linear-time

STC (Zamir & Etzioni, SIGIR 1998) achieves O(N) time and space while producing clusters competitive with O(N²) methods in evaluation experiments [^irsrc10]. It was designed for interactive clustering of Web search results.

Core insight: STC uses **shared phrase** as the similarity measure. If D1 and D2 share a phrase, and D2 and D3 share the same phrase, then D1 and D3 certainly share it too (transitivity). This allows complete clustering at the base-cluster level without O(N²) penalty.

**Algorithm**:
1. Build a **suffix tree** over all documents using Ukkonen's O(N) algorithm. Each internal node of the suffix tree represents a phrase shared by some subset of documents (the **base cluster** for that phrase).
2. Score each base cluster: `score = |B| × f(|P|)` where |B| is the number of documents sharing phrase P and f(|P|) is a length bonus (linear for 2–6 word phrases; penalizes single-word and very long phrases).
3. Cluster base clusters together (stage 2) if they share ≥ 50% of their documents, limiting revisits to the q best clusters per step to maintain O(1) amortized time.
4. Rank the final clusters; present the best p to the user.

STC labels clusters by the shared phrases that define them — human-readable cluster descriptions, unlike centroid-based methods [^irsrc10].

In a comparative experiment (10 Web queries, human relevance judgments), STC outperformed Buckshot, Fractionation, K-means, and even Group-Average Hierarchical Clustering (O(N²)) in average precision when selecting the best clusters for interactive browsing [^irsrc10].

### Cluster validation for IR

Meaningful clusters are those that satisfy the **cluster hypothesis**: relevant documents cluster together. Validation approaches [^irsrc10]:

1. **Inter-document similarity gap**: compare average similarity among relevant documents to average similarity between relevant-nonrelevant pairs. If the cluster hypothesis holds, the former should be substantially higher.
2. **Nearest-neighbor relevance** (Voorhees): for each relevant document, check how many of its 5 nearest neighbors are also relevant.
3. **Term density** (El-Hamdouchi & Willett): `postings / (documents × unique_terms)`. Higher density → more document pairs share terms → better clustering. This measure correlates best with retrieval effectiveness in comparative studies [^irsrc10].

## Related Corpus Pages

- [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md) — complement to clustering; both are unsupervised; PCA for variance explanation, clustering for partition discovery
- [/ai-engineering/statistical-learning.md](/ai-engineering/statistical-learning.md) — supervised vs unsupervised framing
- [/ai-engineering/gaussian-mixture-models.md](/ai-engineering/gaussian-mixture-models.md) — soft/probabilistic alternative to K-means; handles outliers
- [/ai-engineering/sources/introduction-to-statistical-learning.md](/ai-engineering/sources/introduction-to-statistical-learning.md) — ISL book summary
- [/data-engineering/data-mining.md](/data-engineering/data-mining.md) — data mining domain page (Han/Kamber/Pei textbook); covers DBSCAN and advanced hierarchical methods (BIRCH, CURE, CHAMELEON) beyond ISL's treatment; situates clustering within the KDD pipeline (cross-domain → data-engineering)

---

[^src1]: [Introduction to Statistical Learning, Part 20](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-20.md)
[^src2]: [Introduction to Statistical Learning, Part 21](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-21.md)
[^src_bhk]: [Foundations of Data Science (Blum, Hopcroft, Kannan 2018) — Chapter 7](../../raw/pdf/pdf-foundations-of-data-science-part-01.md)
[^irsrc9]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 9](../../raw/pdf/pdf-information-retrieval-a-survey-part-09.md)
[^irsrc10]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 10](../../raw/pdf/pdf-information-retrieval-a-survey-part-10.md)
