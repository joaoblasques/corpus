---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-01.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-02.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-03.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-04.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-05.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-06.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-07.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-08.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-09.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-10.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-11.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-12.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-13.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-14.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-15.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-16.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-17.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-18.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-19.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-20.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-21.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-22.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-23.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-24.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-25.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-26.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-27.md
    channel: pdf
    ingested_at: 2026-07-18
aliases:
  - Mining of Massive Datasets
  - MMDS
  - Leskovec Rajaraman Ullman
  - CS246
tags:
  - corpus/data-engineering
  - source
created: 2026-07-18
updated: 2026-07-18
---

# Mining of Massive Datasets — Leskovec, Rajaraman, Ullman (2014)

**TL;DR.** A 513-page Stanford CS246 textbook treating data mining as an algorithmic discipline for data that does not fit in main memory. Scale is the organising constraint throughout; every topic is revisited under that constraint, producing techniques — MapReduce, minhashing, Bloom filters, A-Priori, streaming moments, PageRank by power iteration — that are distinct from the in-memory equivalents covered in traditional mining texts such as Han/Kamber. See [/data-engineering/data-mining.md](/data-engineering/data-mining.md) for comparison with the Han/Kamber approach.

---

## 1. What the Book Is About

"This book is about data mining of very large amounts of data, that is, data so large it does not fit in main memory." [^src1] The emphasis on scale distinguishes it from classical mining curricula. Three further characteristics follow:

- **Web-centric examples.** Most running examples derive from web data (crawls, click streams, social graphs, ad auctions), the domain where massive scale first became routine. [^src1]
- **Algorithmic viewpoint.** Data mining is treated as applying algorithms to data, not as training ML engines. The gap between these views narrows in Ch. 12, but the framing matters: the book asks "what is the cheapest algorithm that produces a correct answer?" before asking "what model generalises best?" [^src1]
- **Ten major topic areas.** The preface enumerates them explicitly: (1) MapReduce and distributed file systems; (2) similarity search and LSH; (3) data-stream processing; (4) search-engine technology (PageRank, spam detection, HITS); (5) frequent-itemset mining; (6) large-scale clustering; (7) web advertising; (8) recommender systems; (9) social-network graph mining; (10) dimensionality reduction; and (11) large-scale machine learning. [^src1]

---

## 2. Chapter-by-Chapter Summary

### Ch. 1 — Data Mining (Foundations)

Defines data mining, introduces Bonferroni's principle (beware spurious patterns when searching many combinations), covers hash functions, secondary storage costs, power laws, and TF-IDF weighting. These primitives reappear throughout the book.

### Ch. 2 — MapReduce and the New Software Stack

MapReduce is the book's primary computational model. A Map task reads key–value pairs and emits intermediate key–value pairs; a shuffle groups by key; a Reduce task aggregates all values for a single key. [^src1_toc] Combiners are local pre-reducers that cut shuffle volume. Execution handles node failures by re-running Map tasks (outputs are on local disk) but not Reduce tasks (outputs land in the distributed file system). [^src1_toc]

The chapter covers relational algebra over MapReduce (selection, projection, join, grouping/aggregation, set operations, natural join, matrix–vector multiply) and workflow systems (Pig, Hive) for multi-stage pipelines.

**Communication cost model** (§2.5–2.6): The dominant cost in MapReduce is data movement between Map and Reduce tasks, not arithmetic. The model counts bytes crossing the network. For a three-way join R(A,B) ⋈ S(B,C) ⋈ T(A,C) with k reducers, the total communication is minimised by hashing B-values to b = √(kr/t) buckets and C-values to c = √(kt/r) buckets; the optimal total Reduce-task communication equals s + 2√(krt). [^src5]

Two complexity parameters characterise algorithm families: **reducer size** q (maximum values per reduce key, controls main-memory footprint and parallelism) and **replication rate** r (average key–value pairs emitted per input element, controls communication). For most problems these trade off as r ≈ p/q where p is the input size, and this lower bound can be proved via a graph model of inputs and outputs. [^src5]

The star-join structure common in analytical workloads (one large fact table, many small dimension tables) is an important special case: the multiway join is almost always cheaper than a cascade of two-way joins. [^src5]

Extensions: Pregel for iterative graph computation, recursive MapReduce for transitive closure.

### Ch. 3 — Finding Similar Items

**Problem.** Given a large set of documents, find near-duplicate pairs without comparing all O(n²) pairs.

**Pipeline.**
1. *Shingling*: represent each document as the set of k-shingles (overlapping substrings of length k). k = 9 is typical for web pages. [^src1_toc]
2. *Minhashing*: compress the shingle set into a signature (length-n vector of minimum hash values under n independent hash functions). The probability that two minhash signatures agree on position i equals the Jaccard similarity of the underlying sets — the fundamental theorem of minhashing. [^src1_toc]
3. *Locality-Sensitive Hashing (LSH)*: band the signature matrix into b bands of r rows each. Two documents become candidates iff they agree in at least one band. The S-curve P(candidate | Jaccard = s) ≈ 1 − (1 − s^r)^b concentrates near the threshold t ≈ (1/b)^(1/r). [^src1_toc]

Distance measures covered: Euclidean, Jaccard, cosine, edit, Hamming. LSH families exist for each. The Flajolet-Martin sketch of §4.4 and the AMS second-moment sketch of §4.5 are related ideas — compact randomised summaries that answer a specific query approximately.

### Ch. 4 — Mining Data Streams

**Model.** Elements arrive faster than they can be stored. The algorithm gets at most one pass; main memory is the primary constraint.

Core techniques:

| Technique | Problem | Key idea |
|---|---|---|
| Hash-based sampling | Maintain representative sample | Hash key to a set and keep all tuples with matching hashes |
| Bloom filter | Stream filtering (set membership) | k hash functions, n-bit array; false positive rate ≈ (1 − e^(−km/n))^k [^src10] |
| Flajolet-Martin | Count distinct elements | Longest trailing-zero run in hash values estimates log₂(count) [^src10] |
| AMS sketch | Estimate kth-order moments | Random variable n(2X.value − 1) is unbiased estimator of second moment; generalises to k-th moment via n(v^k − (v−1)^k) [^src10] |
| DGIM | Count 1s in sliding window of N bits | O(log² N) space; at most 50% error; bucket sizes are powers of 2 [^src10] |
| Decaying window | Track recent frequency | Weight element i steps ago by (1−c)^i; score ≥ ½ kept |

Bloom filter analysis: with m set members, n bits, and k hash functions the false-positive probability is (1 − e^(−km/n))^k. Setting k = n/m makes the bit array 37% zeros; the rate drops substantially with each additional hash function. In a concrete example with 1 billion members and 8 billion bits, a single hash function gives false-positive rate 0.1175; adding a second function drops it to 0.0493. [^src10]

DGIM uses O(log N) buckets, each stored in O(log N) bits, for total O(log² N) space. Queries answered with ≤50% error by summing all complete buckets plus half the partially covered bucket. Reducing to r−1 or r buckets per size lowers the error bound to 1/(r−1). [^src10]

### Ch. 5 — Link Analysis

**PageRank.** Iterative power method on the web's link graph. The stationary distribution of a random walk with teleportation (probability β follow a link, 1−β teleport to a random page) avoids the dead-end and spider-trap problems that plague the naive definition. [^src1_toc]

PageRank iteration over MapReduce: represent the transition matrix in block-stripe form; use combiners to aggregate partial PageRank sums before the shuffle.

Topic-sensitive PageRank: bias the teleportation set to a topic-specific seed set; one vector per topic, combined at query time using an estimate of the user's interest.

Link spam (spam farms, TrustRank) and the HITS (Hubs and Authorities) model for query-dependent authority.

See [/data-engineering/pagerank.md](/data-engineering/pagerank.md) for a dedicated treatment.

### Ch. 6 — Frequent Itemsets

**Market-basket model.** Items and baskets; *support* of itemset I = number of baskets containing I; *frequent* iff support ≥ threshold s.

**A-Priori algorithm.** Two-pass algorithm exploiting the monotonicity property: every subset of a frequent itemset must also be frequent. Pass 1 counts singletons; Pass 2 counts only pairs of frequent items. Generalises to k-itemsets in k passes. "The part that often takes the most main memory is the counting of pairs of items." [^src15]

**PCY.** Improves A-Priori's first pass by hashing pairs into a bit-array (all available memory beyond item counts). Only pairs that (a) are both individually frequent and (b) hashed to a frequent bucket need counting in Pass 2. [^src15]

**Multistage / Multihash.** Insert additional hash tables between passes, or split memory into multiple independent hash tables on the first pass, to further shrink candidate pairs.

**SON algorithm.** Divide the file into segments that fit in memory; find frequent itemsets per segment; candidates = union of all per-segment frequent sets; one more pass counts candidates globally. Parallelises naturally over MapReduce: "This algorithm is especially appropriate in a MapReduce setting." [^src15]

**Toivonen's algorithm.** Sample the file; lower the threshold so the sample rarely misses a globally frequent set; add the *negative border* (infrequent sets all of whose immediate subsets are frequent in the sample); one pass over the full file; if any negative-border set is globally frequent, repeat. [^src15]

**Frequent itemsets in streams.** Use decaying-window scores (Section 4.7). Start scoring an itemset the first time it appears *and* all its immediate proper subsets are already being scored — an adaptation of the A-Priori trick to infinite streams. [^src15]

### Ch. 7 — Clustering

Two algorithm families: hierarchical (agglomerative) and point-assignment (k-means variants).

**Hierarchical.** O(n² log n) with a priority queue. Options for inter-cluster distance: centroid, minimum point, maximum point (diameter), average. Stopping rules: target k, diameter threshold, sudden jump in average diameter. In non-Euclidean spaces a *clustroid* (point minimising sum of distances to others in cluster) replaces the centroid. [^src15]

**BFR (Bradley-Fayyad-Reina).** Large-scale k-means for Euclidean spaces that do not fit in memory. Maintains three point sets per cluster: Discard Set (summarised by N, SUM, SUMSQ), Compressed Set (mini-clusters not yet assigned), Retained Set (outliers). Points absorbed when Mahalanobis distance is within threshold. [^src1_toc]

**CURE.** Uses a fixed number of representative points per cluster (shrunken toward the centroid) rather than a centroid. Handles non-convex cluster shapes; supports non-Euclidean spaces via clustroids. [^src1_toc]

**Curse of dimensionality.** In high-dimensional Euclidean space almost all pairs of random points are at approximately the same distance, and almost any two vectors are nearly orthogonal. This makes distance-based clustering ambiguous and justifies approximation. [^src15]

**Streaming clustering (DGIM-style).** Maintain exponentially sized buckets of sub-clusters; merge pairs when a third of the same size appears.

### Ch. 8 — Advertising on the Web

Models online ad allocation as a bipartite matching / online algorithm problem. Key concepts:

- **Competitive ratio.** Ratio of the online algorithm's value to the offline optimum, worst case over all inputs.
- **Balance algorithm.** Assign each query to the advertiser with the largest remaining budget fraction (fraction of budget not yet spent). Achieves competitive ratio 1 − 1/e ≈ 0.63 with equal budgets; generalised version handles unequal budgets. [^src1_toc]
- **Adwords.** Match search queries to keyword bids respecting per-advertiser daily budgets. Greedy gives competitive ratio ½; Balance improves this; MSVV generalisation achieves 1 − 1/e in the large-budget limit. [^src1_toc]

### Ch. 9 — Recommendation Systems

**Utility matrix.** Users × items, mostly blank. The long-tail property means most value comes from the non-obvious matches. [^src1_toc]

Two families:

| Approach | Mechanism | Strengths | Weaknesses |
|---|---|---|---|
| Content-based | Build item profiles (TF-IDF features, tags); match to user profiles | No cold-start for items; interpretable | Cold-start for users; limited serendipity |
| Collaborative filtering | Jaccard or cosine similarity over the utility matrix; find similar users or items | Cross-domain; captures latent preferences | Sparsity; cold-start for new users/items |

**Dimensionality reduction for recommendations.** UV-decomposition: factorise the utility matrix as U (users × d) × V (d × items) to minimise RMSE on non-blank entries. Updated via gradient descent — the Netflix Prize formulation. Related to the full SVD of Ch. 11 but trained only on observed ratings. [^src2_toc]

### Ch. 10 — Mining Social-Network Graphs

Social networks modelled as large directed or undirected graphs where standard O(n²) or O(n³) algorithms are infeasible.

Key problems:

- **Community detection.** Girvan-Newman: iteratively remove edges with highest betweenness centrality. Direct methods find cliques or complete bipartite subgraphs. Spectral methods partition via the Fiedler eigenvector of the normalised Laplacian. Affiliation-Graph Model (AGM) for overlapping communities. [^src2_toc]
- **SimRank / random walks with restart.** Similarity between nodes by probability of meeting in a random walk started from both nodes.
- **Triangle counting.** Detecting triadic closure; MapReduce algorithm counts triangles in O(m^(3/2) / k) communication with k reducers. [^src2_toc]
- **Neighbourhood / diameter estimation.** Approximate Neighbourhood Function (ANF) via Flajolet-Martin sketches; Flajolet-Martin + MapReduce BFS layers.

### Ch. 11 — Dimensionality Reduction

**SVD.** Factorise any m × n matrix M = UΣV^T where U is m × r column-orthonormal, Σ is r × r diagonal (singular values), V is n × r column-orthonormal. Best rank-k approximation (Eckart-Young theorem). Applications: latent semantic indexing (LSI), noise reduction, collaborative filtering. [^src1_toc]

**CUR decomposition.** Randomly sample C (columns of M) and R (rows of M); compute U as a pseudo-inverse of their intersection. Preserves sparsity — advantage over SVD for very large sparse matrices.

**PCA.** Find the eigenvectors of the covariance matrix; equivalent to SVD on a centred matrix. Used for feature compression before clustering or ML.

### Ch. 12 — Large-Scale Machine Learning

Covers algorithms whose training-time or memory requirements scale to data that does not fit on a single machine.

**Perceptrons.** Update the separator hyperplane w toward (away from) a misclassified positive (negative) example by a fraction η. Converges when the data is linearly separable. Parallelises by distributing training data across Map tasks and averaging weight vectors in the Reduce step. [^src1_toc]

**Support-vector machines.** Find the hyperplane that maximises the margin 2/||w||. With soft margins, the optimisation is: minimise ½||w||² + C Σ max(0, 1 − y_i(w·x_i + b)). The parameter C is a regularisation constant trading margin width for misclassification penalty. [^src27]

**Gradient descent for SVMs.** Compute partial derivatives of the hinge-loss objective; move w by −η × gradient each round. Allows training data to reside on disk. [^src27]

**Stochastic gradient descent.** Process one training example (or a small batch) per round; adjust w by a fraction of the gradient for that example only. Suited to very large training sets — the UV-decomposition update of §9.4 is an instance. [^src27]

**Nearest-neighbor learning.** Store the training set; classify each query by the majority label (or weighted average label) of its k nearest training points. Suffers severely from the curse of dimensionality in high dimensions; mitigation via VA-files (approximate index) or dimensionality reduction. [^src27]

---

## 3. The Communication Cost Model in Depth

The communication cost model is the book's primary analytical framework for comparing MapReduce algorithms. It is defined in §2.5–2.6:

**Total communication** = sum of bytes emitted by all Map tasks = sum received by all Reduce tasks. Wall-clock time is bounded by the maximum communication to any one reducer times the number of serial passes.

**Replication rate r** (average key–value pairs per input) and **reducer size q** (max values per key) trade off. For most problems a mapping schema must exist such that every output's required inputs are co-located at some reducer. The lower bound on r as a function of q is derived by:

1. Upper-bounding outputs coverable by a reducer of size q.
2. Noting the total output count must be covered.
3. Deriving a lower bound on Σ q_i (total communication) from the inequality.
4. Dividing by input count to get the per-input lower bound r. [^src5]

**Three-way join example.** For R(A,B) ⋈ S(B,C) ⋈ T(A,C) with sizes r, s, t and k reducers: optimal partition uses b = √(kr/t) B-buckets and c = √(kt/r) C-buckets; Reduce-side communication = s + 2√(krt). The 3-way join beats cascaded 2-way joins when k < (r_join_intermediate / 2)². For a social-network friends relation with r = 3 × 10¹¹ tuples, the 3-way join is preferable with up to ~961 reducers. [^src5]

**Matrix multiplication spectrum.** One-pass algorithm (each output element in one reducer): communication = 4n⁴/q. Two-pass algorithm (square partitions): first-pass communication = 2gn², second pass gn², total = 3√2 n³/√q ≈ 4.24 n³/√q. The two-pass method beats the one-pass method by O(√n) in communication, at the cost of managing two MapReduce jobs. [^src5]

---

## 4. Key Distinguishing Ideas vs. Traditional Data Mining

| Dimension | MMDS (Leskovec et al.) | Traditional mining (e.g., Han/Kamber) |
|---|---|---|
| **Primary constraint** | Scale: data does not fit in RAM | Correctness and generality; RAM is the working store |
| **Computational model** | MapReduce / streaming / one-pass | Relational/in-memory algorithms |
| **Approximation** | Accepted as first-class (LSH, Bloom, AMS, DGIM) | Typically exact algorithms, sampling as a variant |
| **Graph scale** | Algorithms for billion-node graphs | Graph mining at dataset scale, not web scale |
| **Communication cost** | Explicit analytical framework (replication rate × reducer size) | Not modelled |
| **ML coverage** | Perceptrons, SVMs, nearest-neighbor at scale | Not a focus; separate ML textbook territory |

---

## 5. Related Corpus Pages

- [/data-engineering/data-mining.md](/data-engineering/data-mining.md) — Han/Kamber approach; contrast with MMDS
- [/data-engineering/similarity-search.md](/data-engineering/similarity-search.md) — LSH, Jaccard similarity, minhashing (Ch. 3)
- [/data-engineering/streaming-algorithms.md](/data-engineering/streaming-algorithms.md) — Bloom filters, AMS sketches, DGIM (Ch. 4)
- [/data-engineering/pagerank.md](/data-engineering/pagerank.md) — PageRank, topic-sensitive PageRank, spam detection (Ch. 5)

---

[^src1]: [Mining of Massive Datasets part 1](../../../raw/pdf/pdf-mining-of-massive-datasets-part-01.md) — Preface: "this book is about data mining of very large amounts of data … data so large it does not fit in main memory."
[^src1_toc]: [Mining of Massive Datasets part 1](../../../raw/pdf/pdf-mining-of-massive-datasets-part-01.md) — Table of contents (pp. vii–xvi), chapter headings and section structure.
[^src2_toc]: [Mining of Massive Datasets part 2](../../../raw/pdf/pdf-mining-of-massive-datasets-part-02.md) — Table of contents continuation (Ch. 9–12), social-network and ML chapter outlines.
[^src5]: [Mining of Massive Datasets part 5](../../../raw/pdf/pdf-mining-of-massive-datasets-part-05.md) — §2.5 Communication Cost Model (3-way join, star joins); §2.6 Complexity Theory for MapReduce (reducer size, replication rate, lower bounds, matrix multiplication case study).
[^src10]: [Mining of Massive Datasets part 10](../../../raw/pdf/pdf-mining-of-massive-datasets-part-10.md) — §4.3 Bloom Filtering (false-positive analysis); §4.4 Flajolet-Martin algorithm; §4.5 AMS second-moment algorithm; §4.6 DGIM sliding-window algorithm.
[^src15]: [Mining of Massive Datasets part 15](../../../raw/pdf/pdf-mining-of-massive-datasets-part-15.md) — §6.5 Frequent itemsets in streams; §6.6 Ch. 6 summary (A-Priori, PCY, SON, Toivonen); §7.1–7.2 Clustering introduction, hierarchical clustering, curse of dimensionality.
[^src27]: [Mining of Massive Datasets part 27](../../../raw/pdf/pdf-mining-of-massive-datasets-part-27.md) — §12.3 SVM gradient descent (batch and stochastic); §12.4 nearest-neighbor learning; §12.5 comparison of learning methods; §12.6 Ch. 12 summary.
