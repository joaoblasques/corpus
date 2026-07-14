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
aliases:
  - clustering
  - K-means clustering
  - hierarchical clustering
  - dendrogram
  - unsupervised clustering
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-09
updated: 2026-07-14
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

## Related Corpus Pages

- [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md) — complement to clustering; both are unsupervised; PCA for variance explanation, clustering for partition discovery
- [/ai-engineering/statistical-learning.md](/ai-engineering/statistical-learning.md) — supervised vs unsupervised framing
- [/ai-engineering/gaussian-mixture-models.md](/ai-engineering/gaussian-mixture-models.md) — soft/probabilistic alternative to K-means; handles outliers
- [/ai-engineering/sources/introduction-to-statistical-learning.md](/ai-engineering/sources/introduction-to-statistical-learning.md) — ISL book summary

---

[^src1]: [Introduction to Statistical Learning, Part 20](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-20.md)
[^src2]: [Introduction to Statistical Learning, Part 21](../../raw/pdf/pdf-james-witten-hastie-tibshirani-intro-to-statistical-learning-part-21.md)
[^src_bhk]: [Foundations of Data Science (Blum, Hopcroft, Kannan 2018) — Chapter 7](../../raw/pdf/pdf-foundations-of-data-science-part-01.md)
