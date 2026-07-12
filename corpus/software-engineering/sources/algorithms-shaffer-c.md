---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-01.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-02.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-03.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-04.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-05.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-06.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-07.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-08.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-09.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-10.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-11.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-12.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-13.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-14.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-15.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-16.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-17.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-18.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-19.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-20.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-21.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-22.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-23.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-24.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-25.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-26.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-27.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-28.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-29.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-30.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-31.md
    channel: pdf
    ingested_at: 2026-07-12
aliases:
  - Shaffer data structures C++
  - Data Structures and Algorithm Analysis in C++
  - Clifford Shaffer
  - Shaffer DSA
tags:
  - corpus/software-engineering
  - source
created: 2026-07-12
updated: 2026-07-12
---

# Data Structures and Algorithm Analysis in C++ (Shaffer, Ed. 3.2)

**TL;DR**: Comprehensive 615-page teaching textbook by Clifford A. Shaffer (Virginia Tech). Free PDF under educational license. Covers all standard data structures and algorithm analysis in C++, with explicit emphasis on costs/benefits tradeoffs and ADT design. Companion Java version also available [^src1].

## Philosophy and approach

Four organizing principles [^src1]:
1. **Every data structure has costs and benefits** — no structure is universally superior; selection requires understanding the trade-offs.
2. **Tradeoffs are pervasive** — time vs. space, simplicity vs. generality.
3. **Know common practice** — master the toolkit before inventing new structures.
4. **Data structures follow needs** — analyze the application first, then select.

The book is a **teaching text**, not an encyclopedia — it covers the most important structures deeply rather than all structures shallowly.

## Chapter structure

| Part | Chapters | Topics |
|---|---|---|
| I Preliminaries | 1–3 | ADTs, design patterns (Flyweight, Visitor, Composite, Strategy), algorithm analysis, asymptotic notation |
| II Fundamental Data Structures | 4–6 | Lists (array-based, linked), stacks, queues, dictionaries; binary trees, heaps, Huffman coding trees; non-binary trees, union-find |
| III Sorting and Searching | 7–9 | Θ(n²) sorts (insertion, bubble, selection), shell sort, merge sort, quicksort, heapsort, radix sort; file/external sorting; hashing (open/closed) |
| IV Advanced Data Structures | 10–13 | Indexing (ISAM, B-trees, B+-trees), graphs (DFS/BFS, Dijkstra, Prim, Kruskal), memory management, advanced trees (tries, AVL, splay, K-D, quadtrees) |
| V Theory of Algorithms | 14–17 | Summation/recurrence techniques, amortized analysis, lower bounds, DP, randomized algorithms, NP-completeness |

## Key concepts

**ADT vs. data structure**: An ADT defines the *logical* form (interface + operations); a data structure is the *physical* implementation. The same ADT (e.g., list) can be implemented many ways (array-based or linked list) — the choice depends on which operations dominate [^src1].

**Design patterns covered**: Flyweight (shared identical objects — used in PR quadtree empty-leaf nodes), Visitor (generic traversal with pluggable action — used in tree and graph traversal), Composite (recursive tree structure), Strategy (pluggable algorithm) [^src1].

**Asymptotic analysis (Ch 3)**: Big-Θ (tight bound), Big-O (upper bound), Big-Ω (lower bound); best/worst/average cases; simplifying rules for polynomial growth rates. The key insight: a faster computer doesn't make an O(n²) algorithm acceptable on large inputs — the algorithm class matters more than constant factors [^src1].

**Sorting summary (Ch 7)**:

| Sort | Time | In-place | Stable |
|---|---|---|---|
| Insertion sort | Θ(n²) | Yes | Yes |
| Bubble sort | Θ(n²) | Yes | Yes |
| Selection sort | Θ(n²) | Yes | No |
| Shell sort | Between Θ(n) and Θ(n²) | Yes | No |
| Merge sort | Θ(n log n) | No | Yes |
| Quicksort | Θ(n log n) avg | Yes | No |
| Heapsort | Θ(n log n) | Yes | No |
| Binsort/Radix sort | Θ(n + k) | Varies | Yes |

Lower bound for comparison-based sorting: Ω(n log n) — proven via decision tree argument.

**Hashing (Ch 9)**: Hash functions, open hashing (separate chaining), closed hashing (linear probing, quadratic probing, double hashing). Trade-off: closed hashing degrades under high load factor; reorganization offline can restore performance. Deletion in closed hashing requires a tombstone mechanism.

**B-trees and B+-trees (Ch 10)**: Designed for disk access — minimize I/O by keeping nodes large (one disk block per node). B+-tree keeps all records in leaves (linked list), internal nodes are pure routing keys. Preferred when range queries are required; hashing preferred for exact-match only.

**Union-Find (UNION/FIND, Ch 6.2)**: Parent pointer trees for disjoint sets; used in Kruskal's MST algorithm. Path compression + union by weight achieves near-O(1) amortized per operation.

**Minimum spanning tree (Ch 11)**: Prim's algorithm (grow from single vertex, use priority queue) and Kruskal's (sort edges, add if no cycle via Union-Find). Both O(E log V).

**NP-completeness (Ch 17)**: Reductions, Cook-Levin theorem, NP-completeness proofs; coping strategies — approximation, heuristics, special structure. Impossible problems: uncountability, Halting Problem unsolvability.

## Corpus pages produced from this source

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — updated with Shaffer's ADT framing and hashing/B-tree detail
- [Algorithms](/software-engineering/algorithms.md) — updated with sorting lower bound, external sorting
- [Complexity Theory](/software-engineering/complexity-theory.md) — NP-completeness coping strategies

## See also

- [Data Structures and Algorithm Analysis in Java (Shaffer)](/software-engineering/sources/algorithms-shaffer-java.md) — same textbook in Java; nearly identical content
- [Algorithms (Erickson)](/software-engineering/sources/algorithms-erickson.md) — higher-theory companion

---

[^src1]: [Data Structures and Algorithm Analysis in C++ (Shaffer) — Part 1 (Preface, Ch 1: ADTs, design patterns)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-c-part-01.md)
