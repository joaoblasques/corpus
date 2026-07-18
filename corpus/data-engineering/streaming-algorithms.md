---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-10.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-11.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-12.md
    channel: pdf
    ingested_at: 2026-07-18
aliases:
  - data stream algorithms
  - Bloom filter
  - count-min sketch
  - DGIM algorithm
  - Flajolet-Martin
  - hyperloglog
  - synopsis
  - sketch
  - sliding window
  - reservoir sampling
  - streaming data structures
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-18
updated: 2026-07-18
---

# Streaming Algorithms

**TL;DR.** Streaming algorithms process each element once in arrival order, maintain only a bounded (sub-linear) working set, and produce approximate answers with quantifiable error guarantees. They are the only practical option when data arrives faster than it can be stored or when running many parallel streams simultaneously. The canonical structures are Bloom filters (membership), DGIM (sliding-window counts), Flajolet-Martin (cardinality), Count-Min Sketch (frequency), and reservoir sampling (uniform samples).

See [/data-engineering/data-flow-patterns.md](/data-engineering/data-flow-patterns.md) for the broader streaming-pipeline context and [/data-engineering/sources/mining-of-massive-datasets-leskovec.md](/data-engineering/sources/mining-of-massive-datasets-leskovec.md) for the primary textbook source.

---

## 1. The Streaming Model

Data arrives at the processing engine at a rate that makes full storage infeasible. Two strategies handle this:

1. **Summaries / synopses** — maintain a compact structure sufficient to answer expected queries; answer is approximate but uses far less memory than the number of distinct elements.[^src1]
2. **Sliding window** — keep only the most recently arrived N elements; answer queries about that tail.[^src1]

Key properties of the model:
- Each stream element is seen **at most once** (or must be processed in bounded time before the next arrives).
- Working memory is **O(polylog N)** or O(√N), never O(N).
- Answers carry an **error guarantee** expressed as a fractional bound (e.g., ≤50% error) or a probabilistic bound (false-positive rate ≤ε).

The stream-data model was introduced in the chronicle data model literature and formalized in the stream-management systems survey.[^src1]

---

## 2. Bloom Filters — Membership Testing

**Purpose:** decide whether an arriving stream element belongs to a fixed set S, allowing a tunable false-positive rate but zero false negatives.

### Structure

A Bloom filter is a bit array of n bits plus k independent hash functions h₁ … hₖ, each mapping universe elements to positions in [0, n−1].[^src1]

**Initialization:** for every key K ∈ S, set bits h₁(K), h₂(K), …, hₖ(K) to 1.

**Membership test:** for a stream element K, accept it if and only if all of h₁(K) … hₖ(K) are 1 in the array.[^src1]

### False Positive Analysis

The analysis uses a dart-throwing model: n bit positions are targets; km darts are thrown (m = |S|, k hash functions per key). The probability that a given bit remains 0 is:

```
P(bit = 0) = e^(−km/n)
```

The false-positive rate — the probability that a non-member passes — is:[^src1]

```
FP = (1 − e^(−km/n))^k
```

**Example (from source):** with n = 8 billion bits, m = 1 billion members, k = 1:
- Fraction of 1-bits ≈ 1 − e^(−1/8) ≈ 0.1175
- FP rate ≈ 0.1175

With k = 2 (two hash functions into the same array):
- Fraction of 1-bits ≈ 1 − e^(−1/4)
- FP rate ≈ (1 − e^(−1/4))² ≈ 0.0493

Adding a second hash function cuts the false-positive rate from 11.75% to 4.93%.[^src1]

### Space / Accuracy Tradeoff

Choosing k ≤ n/m keeps the 0-bit fraction at ≥ e⁻¹ ≈ 37%. The optimal k (minimizing FP rate as a function of n and m) can be derived analytically.[^src1]

**Gotcha:** Bloom filters have no false negatives. If a member is absent from the filter result, it is definitely not in S. They are unsuitable when false positives are intolerable (e.g., blocklist enforcement where false blocks have high cost).

---

## 3. DGIM Algorithm — Counting 1s in a Sliding Window

**Purpose:** estimate the number of 1-bits in the most recent k positions of a binary stream, for any k ≤ N, using O(log² N) bits of storage.

### Why Exact Counts Require O(N) Space

Any representation using fewer than N bits must map two distinct N-bit strings to the same representation; for those two strings, at least one query "how many 1s in the last k bits?" will produce the wrong answer. Exact sliding-window counts are therefore fundamentally O(N).[^src1]

### Bucket Representation

DGIM partitions the stream's 1-positions into **buckets**. Each bucket stores:
- The timestamp of its right (most recent) end — O(log N) bits.
- Its size (number of 1s) — a power of 2, stored as the exponent, O(log log N) bits.

Total per bucket: O(log N) bits.[^src1]

**Six invariants:**
1. The right end of every bucket is a 1-position.
2. Every 1-position belongs to exactly one bucket.
3. Bucket sizes are powers of 2.
4. There are one or two buckets of each size up to the maximum.
5. Sizes never decrease moving left (older → smaller timestamps).
6. Leftmost bucket is dropped when its timestamp falls outside the window.[^src1]

Because there are at most O(log N) distinct sizes and each needs O(log N) bits, total storage is **O(log² N)**.[^src1]

### Query Answering

To answer "how many 1s in the last k positions?":
1. Find the oldest bucket b that is at least partially within the k-position range.
2. Estimate = (sum of sizes of all fully-included buckets) + ½ × (size of b).[^src1]

**Error bound:** the estimate is always within 50% of the true count. In the worst overestimate case, the estimate is at most 50% above the true count; in the worst underestimate case, it is at least 50% of the true count.[^src1]

### Maintaining the Invariants

When a new bit arrives:
- Drop leftmost bucket if its timestamp is outside [current − N, current].
- If new bit is 0: nothing more to do.
- If new bit is 1: create a new size-1 bucket; if there are now three size-1 buckets, merge the two oldest into a size-2 bucket; cascade merges upward if needed (at most O(log N) merges).[^src1]

### Reducing Error Below 50%

Allow r−1 or r buckets of each size (instead of 1 or 2). The fractional error is bounded by 1/(r−1). Choosing r ≥ 1/ε + 1 achieves ε-relative error, still using O(log² N) space (with a constant factor growing as ε shrinks).[^src2]

### Extension to Integer Sums

For streams of non-negative integers in [1, 2^m], treat each bit-position as a separate binary stream, apply DGIM to each, then sum bit-weighted counts. This gives ε-error on the sum. Works only for non-negative integers; positive/negative mixed streams can have unbounded fractional error because a partially-counted bucket may contain large canceling values.[^src2]

---

## 4. Flajolet-Martin Algorithm — Estimating Cardinality

**Purpose:** estimate the number of distinct elements in a stream (count-distinct / 0th moment) using one integer per hash function.

### Core Idea

Hash each element to a bit-string long enough to cover the universe (64 bits for URLs). The **tail length** of element a under hash h is the number of trailing 0-bits in h(a). Let R be the maximum tail length seen so far. The estimate is **2^R**.[^src1]

**Intuition:** if there are m distinct elements, the probability that none has tail length ≥ r is (1 − 2^(−r))^m ≈ e^(−m·2^(−r)). This approaches 0 when 2^r ≪ m and approaches 1 when 2^r ≫ m, so R concentrates around log₂ m.[^src1]

**Space:** one integer per hash function recording the maximum tail length seen — O(log log m) bits per hash function.[^src1]

### Combining Estimates

Naive averaging fails: the occasional large 2^R (when a lucky hash produces many trailing zeros) dominates the mean and inflates the estimate without bound.[^src1]

Taking the **median** alone also fails: the median is always a power of 2, so values between two consecutive powers of 2 cannot be represented accurately.[^src1]

**Correct combination:** group hash functions into small groups; take the average within each group; then take the median of the group averages. Group size should be at least a small multiple of log₂ m to make averages non-integer.[^src1]

### Relationship to Moments

The 0th moment of a stream is the count of distinct elements. The 1st moment is the stream length. The 2nd moment (surprise number) = Σ mᵢ², measuring distribution unevenness. Flajolet-Martin estimates the 0th moment; the AMS algorithm (below) estimates higher moments.[^src1]

---

## 5. Alon-Matias-Szegedy (AMS) — Estimating Frequency Moments

**Purpose:** estimate the k-th moment Σ mᵢ^k where mᵢ is the count of the i-th distinct element. Most practically useful: k=2 (surprise number / second moment).

### Variables

Maintain s variables X₁ … Xₛ. Each variable stores:
- `X.element` — a stream element chosen by picking a uniform random position.
- `X.value` — initialized to 1 at the chosen position; incremented each time the same element appears subsequently.[^src1]

### Estimating the Second Moment

From variable X with value v at end of stream of length n, estimate = **n(2v − 1)**.[^src1]

**Why it works:** E[n(2v−1)] = Σₐ mₐ² = second moment. The formula n(2v−1) follows from the identity 1 + 3 + 5 + … + (2m−1) = m².[^src1]

**Example (from source):** stream a,b,c,b,d,a,c,d,a,b,d,c,a,a,b (n=15, true second moment = 5²+4²+3²+3² = 59). Three variables starting at positions 3, 8, 13 give estimates 75, 45, 45; average = 55, close to 59.[^src1]

### Higher Moments

For k-th moment, replace n(2v−1) with **n(v^k − (v−1)^k)**. The identity Σᵥ₌₁ᵐ [v^k − (v−1)^k] = m^k ensures correctness.[^src1]

### Maintaining Uniformity in Infinite Streams

The stream length n grows. To keep all positions equally likely for variable assignment: when the (n+1)-th element arrives, select it as a variable position with probability s/(n+1). If selected, randomly evict one of the current s variables and replace it. By induction, all positions maintain equal selection probability s/n.[^src1] This technique is **reservoir sampling** (Section 6 below).

---

## 6. Reservoir Sampling — Uniform Sample from Unknown-Length Stream

**Purpose:** maintain a uniform random sample of exactly k elements from a stream whose total length is unknown.

### Algorithm

1. Store the first k elements unconditionally.
2. When the (n+1)-th element arrives (n ≥ k): include it in the sample with probability k/(n+1). If included, evict one of the current k sample elements uniformly at random.

**Invariant:** at all times, each element seen so far has equal probability k/n of being in the sample.[^src1]

**Proof sketch (by induction):** before arrival of element n+1, each of the n elements has probability k/n. After arrival: element n+1 is included with probability k/(n+1). Each existing sample element is evicted with probability (k/(n+1)) × (1/k) = 1/(n+1). So each existing element stays with probability k/n × (1 − 1/(n+1)) = k/n × n/(n+1) = k/(n+1). Both old and new elements end up with probability k/(n+1).[^src1]

**Application:** limits the number of tuples for any key K in a stream sample to a constant s — when a new tuple for K arrives, apply reservoir sampling over all tuples seen for that key.[^src1]

Original algorithm by Vitter (1985).[^src2]

---

## 7. Decaying Windows — Exponentially Weighted Recency

**Purpose:** weight recent stream elements more heavily than old ones without maintaining a fixed window boundary.

### Definition

Given stream a₁, a₂, …, aₜ and a small constant c (e.g., 10⁻⁶ or 10⁻⁹), the **exponentially decaying window** is the sum:

```
W = Σᵢ (1−c)^(t−i) · aᵢ
```

Elements t time units in the past are weighted by (1−c)^t ≈ e^(−ct). The effective window width (total weight) is ≈ 1/c.[^src2]

### Update Rule

When a new element aₜ₊₁ arrives:
1. Multiply the current sum W by (1 − c).
2. Add aₜ₊₁.

This is O(1) per element — far simpler than a sliding window which must track element expiry.[^src2]

### Contrast with Fixed Sliding Window

| Property | Fixed sliding window | Decaying window |
|---|---|---|
| Recency weighting | Step function (0 before N, 1 after) | Smooth exponential decay |
| Update complexity | Requires element expiry tracking (→ DGIM) | O(1) multiply-add |
| Error model | Approximate count (DGIM ≤50%) | Exact weighted sum |
| Boundary | Sharp at N | No hard boundary |

### Finding Most Frequent Elements

To track popular items (e.g., trending movies) in a decaying window:[^src2]
1. Maintain a score per item; decay all scores by (1−c) each step.
2. Increment the score of the newly arrived item by 1 (create if absent).
3. Drop any item whose score falls below threshold 1/2.

**Space bound:** total weight ≈ 1/c; no more than 2/c items can simultaneously have score ≥ 1/2, since otherwise the sum would exceed 1/c. In practice, popular items are far fewer.[^src2]

---

## 8. Practical Comparison

| Algorithm | Problem | Error guarantee | Space |
|---|---|---|---|
| Bloom filter | Membership (no false negatives) | FP rate (1 − e^(−km/n))^k | n bits + k hash functions |
| DGIM | Count 1s in sliding window of N | ≤50% (tunable to ε) | O(log² N) bits |
| Flajolet-Martin | Count distinct elements | Probabilistic; improves with more hash groups | O(log log m) per hash function |
| AMS | k-th frequency moment | Unbiased; variance shrinks with more variables | O(s · log n) |
| Reservoir sampling | Uniform sample of size k | Exact uniform; no approximation | O(k) elements |
| Decaying window | Weighted recent sum / frequent items | Exact for sum; bounded item count | O(1/c) active items |

**Count-Min Sketch** (not in this source) is the standard industrial complement to AMS for point frequency queries: a width×depth array of hash-indexed counters, supporting ε-additive error on frequency estimates with O(1/ε · log(1/δ)) space.

---

## Footnotes

[^src1]: Leskovec, Rajaraman, Ullman, *Mining of Massive Datasets*, Chapter 4 "Mining Data Streams," extracted from `raw/_inbox/pdf-mining-of-massive-datasets-part-10.md` (§§4.3–4.5) and `raw/_inbox/pdf-mining-of-massive-datasets-part-11.md` (§§4.6–4.8).

[^src2]: Leskovec, Rajaraman, Ullman, *Mining of Massive Datasets*, Chapter 4 §§4.6.6–4.7, extracted from `raw/_inbox/pdf-mining-of-massive-datasets-part-11.md`. References: Bloom (1970) for Bloom filters; Datar, Gionis, Indyk, Motwani (2002) for DGIM; Flajolet & Martin (1983) for cardinality; Alon, Matias, Szegedy (1996) for moments; Vitter (1985) for reservoir sampling.

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) · _software-engineering_

<!-- RELATED:END -->
