---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-22.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-23.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-24.md
    channel: pdf
    ingested_at: 2026-07-18
aliases:
  - collaborative filtering
  - content-based filtering
  - matrix factorization
  - UV decomposition
  - SVD
  - latent factor model
  - Netflix challenge
  - recommender system
  - item-based CF
  - user-based CF
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-18
updated: 2026-07-18
---

# Recommender Systems

**TL;DR.** Recommender systems predict unknown user-item preferences from a sparse utility matrix. Two main paradigms: *content-based filtering* (represent items by features, recommend items similar to what the user liked) and *collaborative filtering* (infer preferences from rating patterns of similar users or items). Matrix factorization via UV decomposition is the dominant algorithmic approach for large-scale CF; SVD gives the theoretically optimal low-rank approximation. The 2009 Netflix Challenge ($1M prize, won by "Bellkor's Pragmatic Chaos") was the field's central benchmark: baseline RMSE 0.9525, winner RMSE 0.8563.[^src1]

See also: [/data-engineering/data-mining.md](/data-engineering/data-mining.md) · [/data-engineering/sources/mining-of-massive-datasets-leskovec.md](/data-engineering/sources/mining-of-massive-datasets-leskovec.md)

---

## 1. The Utility Matrix

The central data structure is the **utility matrix** M: rows are users, columns are items, entries are ratings (e.g. 1–5 stars) or purchase indicators.[^src1] The matrix is typically very sparse — most user-item pairs have no entry — meaning the essential problem is *predicting the blank entries*.

Key properties:
- **Sparsity**: in a real system a user rates only a tiny fraction of all items; most entries are unknown, not zero.[^src1]
- **Two kinds of entries**: explicit ratings (user-assigned stars) or implicit feedback (purchase/view = 1, absence = blank, not 0).[^src1]
- **Cold-start problem**: a new user or a new item has no history; neither content-based nor collaborative methods can bootstrap without some signal.

*Example (from MMDS §9.1)*: rows A–D, columns HP1/HP2/HP3/TW/SW1/SW2/SW3, ratings 1–5 with most cells blank. Goal: predict, e.g., whether user A would rate SW2 highly.[^src1]

---

## 2. Content-Based Filtering

**Approach**: represent each item as a feature vector; build a user profile by aggregating the profiles of items the user liked; recommend items whose feature vectors are closest to the user profile (cosine distance).[^src1]

### 2.1 Item Profiles

Features depend on item type:
- *Documents/news*: TF-IDF top-n words, treated as a Boolean or weighted vector.[^src1]
- *Movies*: actors (one component per actor, Boolean), director, genre.[^src1]
- *Products*: numerical attributes (screen size, disk capacity); scale numerical components with factor α to avoid domination by large-range dimensions.[^src1]
- *Images*: user-supplied tags (del.icio.us pattern).[^src1]

### 2.2 User Profiles

Aggregate the profiles of items the user has rated:
- Binary utility matrix: user profile = average of item profile vectors for liked items.[^src1]
- 1–5 rating matrix: normalize each rating by subtracting that user's average, weight item profiles by normalized rating. Result: positive weights for liked actors/genres, negative for disliked.[^src1]

*"If 20% of the movies that user U likes have Julia Roberts as one of the actors, then the user profile for U will have 0.2 in the component for Julia Roberts."*[^src1]

### 2.3 Making Recommendations

Compute cosine similarity between the user profile vector and each item profile vector. Recommend items with the smallest cosine distance (angle closest to 0°). Use random hyperplanes + LSH to avoid exhaustive search over millions of items.[^src1]

**Limitations**: requires good item features; suffers from over-specialization (recommends only what looks like items already rated); cannot surface serendipitous discoveries across genres.

---

## 3. Collaborative Filtering

**Approach**: use the utility matrix columns/rows directly as item/user vectors; measure similarity between users (or items) from rating patterns; predict missing ratings from the behaviour of similar users/items.[^src1]

### 3.1 Similarity Measures

Three options applied to rows (users) or columns (items) of the utility matrix:

| Measure | Formula | Best for |
|---|---|---|
| Jaccard | \|intersection\| / \|union\| (treat blanks as unrated) | Binary (purchase) data |
| Cosine | dot product / product of norms (treat blanks as 0) | General ratings, but biases near-zero |
| Normalized cosine | subtract per-user average rating, then cosine | Best for 1–5 ratings; penalizes opposite tastes |

*"A and C are much further apart than A and B [under normalized cosine], and neither pair is very close … A and C disagree on the two movies they rated in common."*[^src1]

Normalizing by subtracting the user's average (then optionally also subtracting each item's mean) removes systematic biases (users who always rate high, items that are generally popular).

### 3.2 User-Based CF

1. For target user U, find the n most similar users (nearest-neighbour search by cosine distance).[^src1]
2. For each blank entry (U, item I), average the ratings of the n similar users for I (excluding those who have not rated I).[^src1]
3. Undo normalization to return a predicted rating on the original scale.[^src1]

**Scalability problem**: the user space can be very large; computing all pairwise similarities is O(|users|²); must be precomputed offline and refreshed periodically.

### 3.3 Item-Based CF

Use the *column* similarity of the utility matrix instead of row similarity:
1. Precompute item-item similarity for the m most similar items to each item I.[^src1]
2. For target pair (U, I), find the m items most similar to I that U has already rated; average those ratings (normalizing as above).[^src1]

**Why item-based is often preferred**: items tend to belong to a single genre (a music piece cannot be simultaneously 60s rock and 1700s baroque), making item clusters tighter and more reliable than user clusters, since a user can like multiple unrelated genres.[^src1] Amazon's product recommendation engine is item-based CF.[^src1]

**Precomputation strategy**: recompute item similarities infrequently (the item catalogue changes slowly); cache preferred items per user rather than recomputing at request time.[^src1]

### 3.4 Clustering Users and Items

When the utility matrix is very sparse, even similar users may share no rated items in common (Jaccard / cosine have too little data). A fix: iteratively cluster items (merge columns of utility matrix), then cluster users (merge rows), reducing the matrix to a smaller cluster-cluster matrix. Entries for sparse clusters are filled by averaging ratings of their members.[^src1]

---

## 4. Matrix Factorization: UV Decomposition

**Core idea**: assume M ≈ U × V where U is (n × d) and V is (d × m), for small d.[^src1] The d "hidden" dimensions represent latent factors (genres, concepts) that explain user-item affinity. The product UV gives predicted ratings for *all* user-item pairs, including blanks.

### 4.1 Objective: Minimizing RMSE

Fit U and V by minimizing **RMSE** over known entries:[^src1]

```
RMSE = sqrt( (1/|known|) * sum_{(i,j) known} (M_ij - (UV)_ij)^2 )
```

Only non-blank entries of M contribute to the loss. Blank entries are left out (unlike standard matrix reconstruction problems).

### 4.2 Gradient Descent Optimization

**Algorithm** (per-element coordinate descent):[^src1]
1. Initialize U and V (e.g. all entries = sqrt(avg_M / d), or random perturbations).
2. For each element u_rs in U (or v_rs in V), compute the value that minimises RMSE holding all other entries fixed:

```
optimal u_rs = sum_j [ (m_rj - sum_{k≠s} u_rk * v_kj) * v_sj ]
               / sum_j [ v_sj^2 ]
```
   (analogous formula for v_rs, summing over rows i).[^src1]

3. Cycle through all elements of U then V repeatedly until improvement falls below a threshold.

**Multiple starting points**: gradient descent converges to local minima. To improve the chance of finding the global minimum, run from many random initializations and keep the best.[^src1]

**Overfitting remedies**:[^src1]
- Move only a fraction (e.g. half) of the way toward the optimised value at each step.
- Stop before full convergence.
- Ensemble multiple independent decompositions.

### 4.3 Stochastic Gradient Descent (SGD)

For large matrices, computing gradients over all known entries each round is expensive. **SGD** processes one randomly sampled entry at a time — cheaper per step, same asymptotic direction.[^src1] The approach converges to the same local minimum in expectation with much lower per-iteration cost.

### 4.4 Normalisation Before Decomposition

Subtract the user average and/or the item average from all non-blank entries before factorization. This removes scale biases, leaving residuals that reflect idiosyncratic taste. Undo the subtraction when producing final predictions.[^src1]

---

## 5. SVD: Singular Value Decomposition

**Definition**: any m × n matrix M of rank r decomposes as M = U Σ V^T where:[^src2]
- U is m × r, column-orthonormal (each column is a unit vector, columns are orthogonal).
- V is n × r, column-orthonormal (so V^T is row-orthonormal).
- Σ is r × r diagonal; the diagonal entries σ_1 ≥ σ_2 ≥ … ≥ σ_r > 0 are the **singular values**.

Columns of U and rows of V^T represent latent "concepts"; Σ weights their importance. In the MMDS movie-ratings example, the first concept corresponds to "science fiction" (σ_1 = 12.4), the second to "romance" (σ_2 = 9.5).[^src2]

### 5.1 Relationship to UV Decomposition

UV decomposition is an approximate, numerically fitted variant of SVD. Strict SVD gives the exact (and Frobenius-norm-optimal) decomposition for the full matrix. The UV decomposition of §4 minimises RMSE *only over known entries*, which is what matters for recommendation.[^src1]

### 5.2 Dimensionality Reduction via SVD

Set the s smallest singular values to zero and drop the corresponding columns of U and rows of V^T. This gives the best rank-(r−s) approximation in Frobenius norm.[^src2]

**Rule of thumb**: retain enough singular values so their squared sum ≥ 90% of the total energy (sum of all squared singular values).[^src2]

### 5.3 CUR Decomposition

A sparse-friendly variant: select C (a subset of columns of M), R (a subset of rows), and compute a small matrix U such that M ≈ CUR. C and R stay sparse if M is sparse, avoiding the dense U and V of SVD. Useful when M is too large to store as a dense matrix.[^src2]

---

## 6. The Netflix Challenge (2009)

**Setup**: Netflix released ~500K users × ~17K movies, each (user, movie) pair annotated with a 1–5 star rating and a date.[^src1] Contestants received a training set; performance was measured on a held-out test set.

**Baseline**: Netflix's own algorithm, CineMatch, achieved RMSE ≈ 0.9525. Strikingly, simply predicting the average of the user's mean rating and the item's mean rating came within 3% of CineMatch.[^src1]

**Target**: RMSE ≤ 90% of 0.9525, i.e. ≤ 0.8563.

**Key findings from the challenge**:[^src1]
- UV decomposition alone (with normalisation) yielded ~7% improvement over CineMatch.
- **Temporal dynamics**: rating date mattered. Some movies ("Patch Adams") got lower ratings from late raters; others ("Memento") improved over time. Slope-over-time is a useful feature.
- **Ensemble methods won**: the prize-winning entry "Bellkor's Pragmatic Chaos" was a blend of dozens of independently developed algorithms. The runner-up (submitted minutes later) was also an ensemble.
- External data (IMDB genres, actor info) turned out *not* to be useful — either the matrix factorization already captured those signals, or entity-resolution errors introduced noise.

**Winner**: RMSE 0.8563, awarded September 2009 after 3+ years of competition.

---

## 7. Evaluation Metrics

| Metric | Formula | Notes |
|---|---|---|
| RMSE | sqrt(mean((predicted - actual)^2)) | Standard for explicit ratings; penalises large errors |
| MAE | mean(\|predicted - actual\|) | Less sensitive to outliers than RMSE |
| Precision@k | \|relevant in top-k\| / k | For ranking / top-k recommendation |
| Recall@k | \|relevant in top-k\| / \|total relevant\| | Coverage of known liked items |
| Coverage | fraction of user-item pairs the system can predict | Sparse systems may leave many items unrecoverable |

RMSE was the Netflix Challenge metric and remains the de-facto standard for offline evaluation of rating prediction.[^src1]

---

## Footnotes

[^src1]: Leskovec, Rajaraman, Ullman. *Mining of Massive Datasets*, Chapter 9: "Recommendation Systems" (parts 18–20/28 of the PDF split). Collected 2026-07-12. Paths: `raw/_inbox/pdf-mining-of-massive-datasets-part-18.md`, `raw/_inbox/pdf-mining-of-massive-datasets-part-19.md`, `raw/_inbox/pdf-mining-of-massive-datasets-part-20.md`.

[^src2]: Leskovec, Rajaraman, Ullman. *Mining of Massive Datasets*, Chapter 11: "Dimensionality Reduction" (parts 24/28). Collected 2026-07-12. Path: `raw/_inbox/pdf-mining-of-massive-datasets-part-24.md`.

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Recommender Systems](/ai-engineering/recommender-systems.md) · _ai-engineering_
- [Matrix Decompositions](/ai-engineering/matrix-decompositions.md) · _ai-engineering_
- [Singular Value Decomposition (SVD)](/ai-engineering/singular-value-decomposition.md) · _ai-engineering_

<!-- RELATED:END -->
