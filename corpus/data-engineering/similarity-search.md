---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-07.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-08.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-09.md
    channel: pdf
    ingested_at: 2026-07-18
aliases:
  - LSH
  - locality-sensitive hashing
  - MinHash
  - Jaccard similarity
  - near-duplicate detection
  - shingling
  - minhashing
  - approximate nearest neighbor
  - ANN
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-18
updated: 2026-07-18
---

## TL;DR

Similarity search at scale is the problem of finding all pairs (or nearest neighbors) among millions of items without comparing every pair — a naively O(n²) task. The standard pipeline converts items to shingle sets, compresses them via MinHash signatures, then uses Locality-Sensitive Hashing (LSH) with a band/row structure to reduce comparisons to near-linear time, at the cost of tunable false-positive/false-negative tradeoffs.

See also: [/data-engineering/data-mining.md](/data-engineering/data-mining.md) and the book-level summary at [/data-engineering/sources/mining-of-massive-datasets-leskovec.md](/data-engineering/sources/mining-of-massive-datasets-leskovec.md).

---

## The scale problem

With one million documents and signatures of length 250, the signature matrix fits comfortably in ~1 GB of RAM. But there are roughly half a trillion pairs of documents. At one microsecond per comparison, exhaustive pairwise comparison takes almost six days on a single machine.[^src1] The core insight of the similarity search pipeline is that we do not need to evaluate every pair — we need to focus attention on pairs that are *likely* to be similar, without inspecting all the rest.

---

## Jaccard similarity

The **Jaccard similarity** of two sets A and B is:

```
SIM(A, B) = |A ∩ B| / |A ∪ B|
```

It ranges from 0 (disjoint) to 1 (identical). The complement, **Jaccard distance** `d(A,B) = 1 − SIM(A,B)`, is a true distance measure: non-negative, zero iff A=B, symmetric, and satisfying the triangle inequality.[^src1]

Jaccard similarity is appropriate for set-based comparison of documents, user purchase histories, fingerprint minutiae sets, and any domain where items can be represented as subsets of a universal set.

---

## Shingling: documents as sets

A **k-shingle** (k-gram) is any contiguous subsequence of k characters in a document. Representing each document by its set of k-shingles lets Jaccard similarity serve as a proxy for textual similarity.[^src3]

Choice of k matters:
- Small k (e.g., k=2) yields very common shingles; most documents will share most of them, washing out signal.
- Large k (e.g., k=9 or k=10 for web pages) yields shingles sparse enough that genuine similarity dominates.

For web-page deduplication, a common approach is to hash shingles to 4-byte integers before building the signature — this keeps the universal set tractable.[^src3]

**Stop-word shingling** is a variant for news article matching: define a shingle as a stop word followed by the next two words. Ads and headlines (low stop-word density) generate no shingles and are effectively ignored, making the similarity measurement focus on prose content.[^src2]

---

## MinHash: compressing sets into signatures

Comparing shingle sets directly is expensive because sets can be large. **MinHash** compresses each set into a short integer vector (the **signature**) while preserving expected Jaccard similarity.

A minhash function `h` is built from a permutation of the universal set. Given a permutation, the minhash value of set S is the element of S that appears first in the permuted order. In practice, random hash functions simulate permutations: `minhash(S) = min_{x ∈ S} hash(x)`.[^src3]

**Key property**: for any two sets A and B and any minhash function h,

```
P[h(A) = h(B)] = SIM(A, B)
```

That is, the probability that A and B hash to the same value equals their Jaccard similarity.[^src1]

A **minhash signature** of length n is produced by applying n independent minhash functions. The expected fraction of positions where two signatures agree equals the Jaccard similarity of the underlying sets. The signature matrix has one column per document and one row per hash function — a compact representation suitable for pairwise comparison.[^src3]

**Efficient minhashing**: because true random permutations are impractical for large universal sets, the standard implementation picks a random hash function `h(x) = (ax + b) mod p mod N` and treats the minimum hash value over all set members as the minhash value.[^src3]

---

## Locality-Sensitive Hashing (LSH)

Even with short signatures, comparing all pairs is still O(n²) in the number of documents. **LSH** avoids this by identifying **candidate pairs** — pairs likely to be similar — using a band-and-row structure.[^src1]

### Band/row construction

Divide the signature matrix into **b bands** of **r rows** each (so `b × r = n`, the signature length). For each band, hash the r-element column slice for each document into buckets. Two documents become a **candidate pair** if they hash to the same bucket in *at least one* band.[^src1]

The probability that a pair with Jaccard similarity s becomes a candidate is:

```
P(candidate | s) = 1 − (1 − s^r)^b
```

This function has an **S-curve** shape: low probability for s well below the threshold, then a steep rise, then high probability above it.[^src1] The threshold (point where the curve is at 0.5) is approximately `(1/b)^(1/r)`.

**Example** (b=20, r=5): at s=0.8, roughly 99.96% of pairs become candidates; at s=0.3, only about 4.7% do.[^src1] This sharply focuses computation on genuinely similar pairs.

### False positives and false negatives

- **False positives**: dissimilar pairs that hash to the same bucket in some band and must be checked. Can be reduced by increasing r (narrowing the band).
- **False negatives**: similar pairs that never match in any band and are missed. Can be reduced by increasing b.

Choosing b and r trades off these two error types. The combined pipeline is: shingling → minhash signatures → LSH candidate generation → signature comparison → (optionally) full document comparison.[^src1]

### AND/OR amplification

The band/row construction is equivalent to applying an **AND-construction** (all r rows in a band agree) followed by an **OR-construction** (at least one of b bands agrees). This framework generalizes: any (d1, d2, p1, p2)-sensitive function family can be amplified by cascading AND and OR constructions to drive the low probability toward 0 and the high probability toward 1, at the cost of more hash evaluations.[^src1]

A family F is **(d1, d2, p1, p2)-sensitive** if: for items at distance ≤ d1, any f in F agrees with probability ≥ p1; for items at distance ≥ d2, it agrees with probability ≤ p2.[^src1]

---

## LSH for other similarity functions

### Cosine similarity and random hyperplanes

For vector data, the **cosine distance** is the angle θ between two vectors (0–180°). The LSH family uses random hyperplanes: pick a random normal vector v; hash function f(x) = sign(v · x). Two vectors x and y are candidates if they land on the same side of the hyperplane. The probability of agreement is `(180 − θ)/180`.[^src2]

A **sketch** of vector x is computed by applying n random ±1 vectors and recording signs. The fraction of sketch positions where two vectors agree, multiplied by 180, estimates the angle between them. Restricting random vectors to ±1 components is sufficient for good locality-sensitivity.[^src2]

### Euclidean distance and random projections

For Euclidean distance, each hash function projects points onto a random line and buckets them into intervals of width a. Two points at distance ≤ a/2 hash to the same bucket with probability ≥ 0.5; two points at distance ≥ 2a hash together with probability ≤ 1/3 — forming a (a/2, 2a, 1/2, 1/3)-sensitive family.[^src2] The approach extends to any number of dimensions, and amplification applies as before.

---

## High-similarity regime: beyond LSH

When the target Jaccard similarity threshold is close to 1 (e.g., ≥ 0.9), there are exact alternatives to LSH that are faster and have no false negatives.

**Length-based filtering**: sort sets (represented as sorted strings of their elements) by length. A pair with similarity ≥ J must satisfy `L_t ≤ L_s / J`, so each string need only be compared with a short window of following strings.[^src3]

**Prefix indexing**: index each string under its first `⌊(1−J)·L⌋ + 1` symbols. Any similar pair shares at least one symbol in their respective prefixes — so only strings sharing a prefix symbol need be compared.[^src3]

**Position and suffix indexing**: further reduce candidates by indexing on (symbol, position-in-prefix) pairs and on suffix length. This eliminates pairs that share a symbol but differ in enough preceding or following positions to guarantee similarity below J.[^src3]

---

## Applications

| Application | Representation | Similarity measure | Notes |
|---|---|---|---|
| Near-duplicate web page detection | k-shingles or stop-word shingles | Jaccard | Core use case in Broder (1997); MinHash + LSH standard pipeline[^src1] |
| News article grouping | Stop-word shingles | Jaccard | Focuses on prose, ignores ads/boilerplate[^src2] |
| Plagiarism detection | k-shingles | Jaccard | Same pipeline; k=9 typical for natural language[^src3] |
| Entity resolution / record linkage | Field-level edit distance scoring | Custom scoring + LSH bucket grouping | LSH used to generate candidate pairs; scoring resolves them[^src2] |
| Collaborative filtering | User-item purchase sets | Jaccard | Documents become users; shingles become purchased items[^src3] |
| Fingerprint matching | Minutiae grid-square sets | Jaccard / custom LSH family | Each function defined by 3 grid squares; OR-construction balances false positives/negatives[^src2] |
| Approximate nearest neighbor (ANN) | Feature vectors | Cosine or Euclidean | Random hyperplane or projection-based LSH families[^src2] |

---

## Complexity summary

| Step | Cost |
|---|---|
| Shingling | O(document size) per document |
| Minhash signature (n functions) | O(n × |shingles|) per document |
| LSH candidate generation | O(b × N) where N = number of documents |
| Candidate pair checking | O(candidates × n) |
| Full document comparison (optional) | O(candidates × document size) |

Without LSH, candidate generation alone would be O(N²). LSH reduces it to near-linear in practice for reasonable similarity thresholds.

---

[^src1]: Mining of Massive Datasets (Leskovec et al.), Part 7 — §3.4 "Locality-Sensitive Hashing for Documents", §3.4.2 "Analysis of the Banding Technique", §3.5.3 "Jaccard Distance", §3.6 "The Theory of Locality-Sensitive Functions". `raw/_inbox/pdf-mining-of-massive-datasets-part-07.md`.
[^src2]: Mining of Massive Datasets (Leskovec et al.), Part 8 — §3.7.2 "Random Hyperplanes and the Cosine Distance", §3.7.3 "Sketches", §3.7.4 "LSH Families for Euclidean Distance", §3.8 "Applications of Locality-Sensitive Hashing" (entity resolution, fingerprints, news articles). `raw/_inbox/pdf-mining-of-massive-datasets-part-08.md`.
[^src3]: Mining of Massive Datasets (Leskovec et al.), Part 9 — §3.9 "Methods for High Degrees of Similarity", §3.10 "Summary of Chapter 3" (shingling, minhash, signature properties, prefix/position/suffix indexing). `raw/_inbox/pdf-mining-of-massive-datasets-part-09.md`.

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Vector Database](/ai-engineering/vector-database.md) · _ai-engineering_

<!-- RELATED:END -->
