---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-15.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-16.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-17.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-18.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-19.md
    channel: pdf
    ingested_at: 2026-07-16
aliases:
  - association rule mining
  - frequent itemset mining
  - Apriori algorithm
  - FP-growth
  - market basket analysis
  - frequent patterns
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-16
updated: 2026-07-16
---

# Frequent Pattern Mining

TL;DR: Frequent pattern mining discovers sets of items, sequences, or structures that appear together in a dataset above a minimum support threshold. The canonical form is market basket analysis: find all itemsets appearing in ≥ support% of transactions. Apriori (generate-and-test with antimonotonicity pruning) and FP-growth (prefix-tree, no candidate generation) are the two foundational algorithms. Advanced extensions cover multilevel, multidimensional, and constraint-based patterns.

## Core Concepts

### Itemsets and Association Rules

Given a transaction database D where each transaction is a set of items [^src1]:

- **Frequent itemset**: an itemset X appearing in ≥ min_sup% of transactions (the **support** threshold).
- **Association rule**: X → Y, where X ∩ Y = ∅. Its **support** = P(X ∪ Y); its **confidence** = P(Y|X) = support(X ∪ Y) / support(X).
- A rule is **strong** if it clears both min_sup and min_conf thresholds.

Market basket example: {diapers} → {beer}, support = 3%, confidence = 75% means 3% of all transactions contain both diapers and beer, and 75% of transactions containing diapers also contain beer.

### Antimonotonicity (Apriori Property)

**All nonempty subsets of a frequent itemset must also be frequent** [^src1]. Equivalently: if an itemset X is infrequent, no superset of X can be frequent. This allows massive search space pruning.

### Closed and Maximal Frequent Itemsets

Given 2^n possible subsets, enumerating all frequent itemsets is often impractical [^src1]:

- **Closed frequent itemset**: X is frequent AND no proper superset of X has the same support count. The set of closed frequent itemsets preserves complete support information.
- **Maximal frequent itemset**: X is frequent AND no proper superset of X is frequent. Smaller compressed representation but loses exact support counts.

Example: If only two transactions {a₁,…,a₁₀₀} and {a₁,…,a₅₀} exist (min_sup=1), the 2¹⁰⁰−1 frequent itemsets compress to 2 closed itemsets and 1 maximal itemset.

## Apriori Algorithm

Proposed by Agrawal and Srikant (1994) [^src1]. Level-wise iterative approach:

1. Scan database to find frequent 1-itemsets L₁.
2. Join L_{k-1} with itself to generate candidate k-itemsets C_k.
3. **Prune** C_k: remove any candidate whose (k−1)-subset is not in L_{k-1} (Apriori property).
4. Scan database to count support of remaining C_k → keep those meeting min_sup → L_k.
5. Repeat until no new frequent itemsets found.
6. Generate association rules from each frequent itemset (enumerate high-confidence rules).

**Bottleneck**: multiple full database scans; C_k can be huge. For a 100-itemset at min_sup=1, the naive approach generates 2¹⁰⁰ candidates — but the Apriori property prunes this aggressively.

**Optimizations**: hash-based candidate filtering, transaction reduction (remove transactions containing no frequent k-itemsets), partitioning (mine each partition in memory then aggregate), sampling (mine a random sample first) [^src1].

## FP-Growth Algorithm

Pattern-growth method that avoids candidate generation entirely [^src1]. Encodes the database in a compact prefix-tree structure (FP-tree), then mines directly:

1. Scan database once to find frequent 1-itemsets; sort by descending frequency.
2. Scan database again to insert each transaction into the FP-tree (ordered by frequency, with shared prefixes compressed).
3. For each frequent item (in ascending frequency order): extract its **conditional pattern base** (all prefix paths co-occurring with that item), build a **conditional FP-tree**, then mine it recursively.

**Why faster than Apriori**: no exponential candidate generation; the FP-tree is highly compressed for dense data; uses divide-and-conquer recursion to confine each subproblem to a small conditional database. Only two database scans are needed.

## Interestingness Beyond Support/Confidence

Support and confidence alone produce many misleading or trivial rules [^src2]. Example: if 75% of customers buy beer, then "buys diapers → buys beer, conf=75%" is uninteresting because beer is purchased 75% of the time regardless.

**Null-invariant measures** (unaffected by transactions containing neither X nor Y, which dominate large databases):

| Measure | Formula | Range |
|---|---|---|
| Lift | P(X∪Y) / (P(X)·P(Y)) | 0 to ∞; >1 = positive correlation |
| Cosine | support(X∪Y) / √(support(X)·support(Y)) | 0 to 1 |
| Kulczynski | ½ [P(X|Y) + P(Y|X)] | 0 to 1 |
| All-confidence | support(X∪Y) / max(support(X), support(Y)) | 0 to 1 |

Lift > 1: positive correlation; < 1: negative correlation; = 1: statistical independence [^src2].

## Advanced Pattern Mining (Ch. 7)

### Multilevel Associations

Mine patterns at multiple levels of the concept hierarchy. Example: at the top level, "{milk} → {bread}" holds; drilling down, "{2% milk} → {sourdough bread}" may hold at a refined level but with lower support [^src3]. Requires adjusted support thresholds per level.

### Multidimensional Association Rules

Rules involving multiple attributes/dimensions: `age(X,"20-29") ∧ occupation(X,"student") → buys(X,"laptop")`. Mixed single-dimension and multi-dimension rules.

### Constraint-Based Pattern Mining

Most discovered patterns are uninteresting in practice — constraint-guided mining restricts the search space [^src4]:

- **Antimonotonic constraints**: if an itemset fails, all supersets fail (e.g., `sum(price) ≤ $100`). Safe to prune early.
- **Monotonic constraints**: if an itemset satisfies, all supersets also satisfy (e.g., `avg(price) ≥ $50` when items sorted by price descending). Can push constraint into mining.
- **Succinct constraints**: can be directly encoded at the start to prune the dataset.
- **Convertible constraints**: not inherently antimonotonic/monotonic, but becomes so with a suitable item ordering. Example: `avg(price) ≤ $10` is antimonotonic if items sorted by price ascending.

### High-Dimensional Pattern Mining

Standard Apriori/FP-growth break down on thousands of dimensions (gene expression data, web log features). Special methods: **colossal pattern mining** (CARPENTER algorithm — rows-enumeration approach); pattern reduction by selecting representative patterns [^src4].

### Applications of Frequent Pattern Mining

- **Preprocessing**: noise filtering (infrequent co-occurrences are likely noise; very frequent ones may be uninformative stopwords) [^src5].
- **Pattern-based classification**: use frequent discriminative patterns as features — more reliable than individual attributes.
- **Subspace clustering**: cluster high-dimensional data in frequent-pattern-defined subspaces.
- **Recommender systems**: "customers who buy X also buy Y" is a direct association rule application.
- **Spatiotemporal/multimedia analysis**: colocation patterns in geographic data; frequent visual fragments in image recognition.

## Relationship to Corpus Pages

- Full mining context: [/data-engineering/data-mining.md](/data-engineering/data-mining.md)
- Clustering applications of pattern mining: [/ai-engineering/clustering-methods.md](/ai-engineering/clustering-methods.md)
- Classification extensions: [/ai-engineering/classification-methods.md](/ai-engineering/classification-methods.md)

---

[^src1]: [Data Mining: C&T Part 15 — Ch. 6 frequent itemset mining, Apriori, FP-growth, closed/maximal itemsets](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-15.md)
[^src2]: [Data Mining: C&T Part 16 — Ch. 6 pattern evaluation measures, null-invariance, Kulczynski](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-16.md)
[^src3]: [Data Mining: C&T Part 17 — Ch. 7 multilevel and multidimensional patterns](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-17.md)
[^src4]: [Data Mining: C&T Part 18 — Ch. 7 constraint-based mining, antimonotonicity, data antimonotonicity](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-18.md)
[^src5]: [Data Mining: C&T Part 19 — Ch. 7 pattern mining applications (noise filtering, classification, clustering, recommenders, spatiotemporal)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-19.md)
