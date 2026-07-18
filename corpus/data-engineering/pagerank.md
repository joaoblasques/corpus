---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-13.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-mining-of-massive-datasets-part-14.md
    channel: pdf
    ingested_at: 2026-07-18
aliases:
  - PageRank
  - link analysis
  - HITS
  - hubs and authorities
  - random walk
  - topic-sensitive PageRank
  - spam detection
  - TrustRank
  - web graph
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-18
updated: 2026-07-18
---

# PageRank and Link Analysis

**TL;DR.** PageRank assigns a real-valued importance score to every node in a directed graph by solving the recursive principle "a page is important if important pages link to it."[^src1] The score is the stationary distribution of a random walk over the graph — the long-run probability that a random surfer lands on a given page. Practical computation uses power iteration on a modified (teleporting) transition matrix, converges in ~50 iterations, and scales to Web-sized graphs via sparse-matrix MapReduce. Extensions include topic-sensitive ranking, anti-spam variants (TrustRank), and the HITS dual-score hub/authority model.

See also [/data-engineering/sources/mining-of-massive-datasets-leskovec.md](/data-engineering/sources/mining-of-massive-datasets-leskovec.md) for the broader textbook context.

---

## 1. Core equation

For a page `p`, PageRank `r(p)` is the sum of rank contributions from every page `q` that links to `p`:

```
r(p) = Σ  r(q) / |out(q)|
      q→p
```

where `|out(q)|` is the out-degree of `q`. A page splits its rank equally among all pages it links to.[^src1] The equation is recursive — solving it requires iterative computation (power iteration).

---

## 2. Transition matrix and power iteration

The web graph is represented as a **transition matrix M** of size n×n, where entry `M[i][j] = 1/k` if page `j` links to page `i` (k = out-degree of j), and 0 otherwise.[^src1]

**Power iteration:** start with any non-zero rank vector `r₀`, then repeatedly compute `r ← M · r`. For strongly connected graphs, this converges to the principal eigenvector of M, which is the true PageRank.[^src1] Convergence is reached in approximately 50 iterations for real-world Web graphs.

The limiting value of `r(p)` equals the probability that a random surfer is at page `p` at any given step — the **random-surfer model**.[^src1]

---

## 3. Dead ends and spider traps

Two structural problems break naive power iteration:

| Problem | Description | Symptom |
|---|---|---|
| **Dead end** | Page with no outgoing links | All PageRank drains to 0 (including non-dead pages) |
| **Spider trap** | Set of pages with no links out to the rest of the graph | All rank gets absorbed inside the trap |

**Handling dead ends:** recursively drop nodes with no outgoing arcs before running PageRank. Dropping one node can expose another as a dead end, so the process must be recursive.[^src1]

**Handling spider traps — teleportation:** introduce a damping factor `β ≈ 0.85`. At each step, the random surfer follows a link with probability `β` and "teleports" to a uniformly random page with probability `1 − β`.[^src1]

The modified iteration becomes:

```
r_new(p) = β · (M · r_old)(p)  +  (1 − β) / n
```

Equivalently: every surfer has probability `1 − β` of leaving the Web; an equal number of new surfers are injected uniformly across all pages.[^src1]

---

## 4. Efficient computation at scale

The transition matrix for a Web-scale graph is extremely sparse (almost all entries are 0). The efficient representation stores only non-zero entries **column-by-column**: for each column (source page), record the count of non-zero entries followed by the list of destination row indices. All non-zero values in a column share the same value `1/k`, so the value need not be stored per entry.[^src1]

**Block-stripe / MapReduce approach** for graphs too large to fit in RAM:[^src1]
1. Partition the rank vector `r` into `k` segments.
2. Partition the transition matrix into `k²` square blocks.
3. Each machine handles one block and its corresponding rank-vector segment.
4. Rank-vector segments are replicated to `k` machines each (small overhead).
5. Combine partial results to form the new rank vector.

This block-stripe decomposition allows PageRank iteration on Web-scale graphs using standard MapReduce infrastructure.

---

## 5. Topic-sensitive PageRank

Standard PageRank is query-agnostic. If the user is known to be interested in a specific topic, the teleportation step can be biased toward a **teleport set** — a curated collection of pages known to be about that topic.[^src1]

Modified iteration: instead of distributing the `(1 − β)` tax uniformly across all pages, distribute it only among pages in the teleport set S:

```
r_new(p) = β · (M · r_old)(p)  +  (1 − β) · [1/|S| if p ∈ S, else 0]
```

**Building teleport sets:** use the DMOZ open directory taxonomy (pages already categorized by topic), or select pages with unusually high term frequency for topic-specific keywords.[^src1]

---

## 6. HITS — Hubs and Authorities

Proposed by Kleinberg (1999)[^src2], HITS gives each page *two* scores rather than one:

- **Authority score** `a(p)`: how valuable is the content on page `p`? High if many high-quality hubs link to it.
- **Hub score** `h(p)`: how good is page `p` as a directory/pointer? High if it links to many high-quality authorities.

**Mutual reinforcement equations:**
```
a(p) = Σ  h(q)      (sum over all q that link to p)
      q→p

h(p) = Σ  a(q)      (sum over all q that p links to)
      p→q
```

These are also solved by iterative matrix–vector multiplication (analogous to PageRank power iteration).[^src1] Unlike PageRank, dead ends and spider traps do not distort HITS — no taxation scheme is required.[^src1]

HITS produces a **two-dimensional ranking**, useful for queries where one wants both definitive reference pages (high authority) and curated link lists (high hub) — e.g., academic citation networks, curated resource directories.

---

## 7. Web spam and TrustRank

### 7.1 Spam farms

Spammers construct **spam farms**: a target page `t` supported by many satellite pages `s₁…sₙ`.[^src1]

- `t` links to all `s_i`.
- Each `s_i` links back only to `t`.
- External links from outside the farm are seeded (e.g., blog comment spam) to inject initial rank.

This concentrates rank on `t` by recycling it internally. The spam farm's boost to `t` is roughly `βx/(1−β²)` where `x` is the external rank flowing in — mathematically small but non-negligible at scale.[^src1] [unsourced — exact formula not verbatim in source]

### 7.2 TrustRank

TrustRank is topic-sensitive PageRank where the teleport set is a **trusted seed set** — e.g., university homepages or government domains.[^src1] The intuition: spam farms are unlikely to be trusted pages or to receive many links from trusted pages, so the flow of "trust" through the Web degrades sharply before reaching them.

### 7.3 Spam mass

**Spam mass** of a page `p` is defined as:[^src1]

```
spam_mass(p) = (PageRank(p) − TrustRank(p)) / PageRank(p)
```

Pages with spam mass close to 1 (high conventional PageRank, very low TrustRank) are candidates for spam farm membership. This provides a computable signal for spam labeling.

---

## 8. Beyond the Web: applications

The same random-walk framework applies whenever there is a directed graph with meaningful link semantics:

| Domain | Nodes | Links | What PageRank measures |
|---|---|---|---|
| **Citation networks** | Academic papers | Citations | Paper influence/importance |
| **Social networks** | Users | Follows/retweets | Influence, reach |
| **Recommendation** | Items or users | Co-purchase, co-view | Item authority in preference graph |
| **Code dependency graphs** | Modules | Import/call edges | Central/critical modules |
| **Biological networks** | Genes/proteins | Interaction edges | Pathway centrality |

In each case the graph must be treated for dead ends and traps before iteration, and the damping factor `β` can be tuned to the domain's teleportation semantics.

---

## 9. Practical gotchas

- **Dangling nodes at scale:** Web crawls always produce dead ends; recursive pruning is essential before iteration begins.
- **Convergence check:** use L1 distance `‖r_new − r_old‖₁ < ε`; ~50 iterations suffice for ε ≈ 10⁻⁶ on real Web graphs.[^src1]
- **Numerical stability:** store rank values in double precision; single precision can diverge at n > 10⁷.
- **β sensitivity:** β = 0.85 is the standard; raising it (e.g., 0.99) slows convergence and increases spider-trap risk; lowering it (e.g., 0.70) makes rankings more uniform and less discriminative.
- **Topic-sensitive at serving time:** precompute one rank vector per topic offline; at query time, blend the topic-specific vector with the user's inferred topic distribution.

---

## Footnotes

[^src1]: Leskovec, J., Rajaraman, A., Ullman, J.D. *Mining of Massive Datasets*, Chapter 5: Link Analysis. Summary §5.6, pp. 197–200; References §5.7, p. 200. (Parts 13/28 of the corpus PDF split.) Original source: Brin & Page, "Anatomy of a large-scale hypertextual web search engine," WWW 1998.

[^src2]: Kleinberg, J.M., "Authoritative sources in a hyperlinked environment," *J. ACM* 46:5, pp. 604–632, 1999. (Cited in §5.7 of the source.)
