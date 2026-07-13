---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-01.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-02.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-03.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-04.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-05.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-06.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-07.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-08.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-09.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-10.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-11.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-12.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-13.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-14.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-15.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-16.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-17.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-18.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-19.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-20.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-21.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-22.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-23.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-24.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-25.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-26.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-27.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-28.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-29.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-30.md
    channel: pdf
    ingested_at: 2026-07-13
aliases:
  - Shaffer data structures Java
  - Data Structures and Algorithm Analysis in Java
  - Shaffer DSA Java
tags:
  - corpus/software-engineering
  - source
created: 2026-07-12
updated: 2026-07-13
---

# Data Structures and Algorithm Analysis in Java (Shaffer, Ed. 3.2)

**TL;DR**: Java edition of Shaffer's comprehensive DSA textbook (601 pages). Identical structure and content to the C++ edition; language-specific differences are minor. Uses Java generics instead of C++ templates; notes Java's weakness for file processing and fine memory control. Free PDF under educational license [^src1].

## Relation to C++ edition

Same author, same edition (3.2), same 17 chapters, same philosophy and examples. Key language differences noted in the Java edition:
- Uses **generics** (not C++ templates); assumes reader familiarity.
- Uses `Assert.notFalse()` / `Assert.notNull()` for parameter checking (vs. `Assert` macro in C++).
- Java is "poor for file processing and fine memory control" — Section 12.3 on memory management is more awkward to express in Java [^src1].
- Inheritance used sparingly in examples (same reasoning as C++ edition — it obscures the pedagogical point).

For full content, see [Data Structures and Algorithm Analysis in C++ (Shaffer)](/software-engineering/sources/algorithms-shaffer-c.md) — all concepts, chapter structure, and key algorithms are shared.

## Chapters 8–17 (later half, parts 17–30)

Content from the second half of the Java edition (same as C++ Ch 8–17):

**Ch 8 (File Processing)**: disk I/O model — platters, tracks, sectors; seek time (~3.6ms average for 15,000 rpm drives), rotational latency, transfer time; buffer pools with FIFO, LFU, and LRU replacement strategies; batch vs. interactive query tradeoff (batch sorts queries by position, amortizing seek cost; interactive processes queries in arrival order). Exercises include calculating average time to read files of various sizes from specific drive specs.

**Ch 9 (Searching)**: self-organizing lists — move-to-front heuristic (accessed record moved to head) and transposition heuristic (swap with predecessor); Zipf distribution (80/20 rule: a few records account for most accesses). Hashing: mid-square method, folding, Horner's method for string hashing; collision resolution: closed hashing — linear probing (clusters near collision point), quadratic probing (reduces primary clustering), double hashing (best distribution, ~two hash functions); open hashing (separate chaining, degrades gracefully, allows load factor >1); perfect hashing (no collisions, viable only for static read-only databases like CD-ROMs); deletion via tombstone markers; performance degrades above ~70% load factor for closed hashing.

**Ch 10 (Indexing)**: linear index, 2-3 trees (always balanced; internal nodes hold 1–2 keys and 2–3 children; search descends via key comparison; insert adds to leaf and splits upward if needed — guarantees O(log n) height at all times), ISAM, B+-trees with leaf-linked list for range scans.

**Ch 11 (Graphs)**: adjacency matrix (O(V²) space, fast edge lookup) vs. adjacency list (O(V+E) space, fast neighbor iteration); topological sort via DFS for DAGs; shortest paths: Dijkstra's algorithm (greedy, relaxes edges, O((V+E) log V) with binary heap) and BFS (unweighted graphs, O(V+E)); MST: Prim's (grow from one vertex, add cheapest edge to non-tree vertex; correctness by exchange argument) and Kruskal's (sort all edges O(E log E), use Union-Find to detect cycles; O(E log E) dominated by sort).

**Ch 14 (Analysis Techniques)**: amortization; space/time tradeoffs — preprocessing input to speed up queries (input enhancement); precomputing indexes vs. on-the-fly computation.

**Ch 15 (Lower Bounds)**: Ω(n log n) comparison sort lower bound via decision tree (n! permutations → n! leaves → height ≥ log₂(n!) = Θ(n log n)); finding the ith element: naive O(n log n) sort is unnecessarily powerful; median-of-medians algorithm achieves O(n) worst-case by choosing a pivot guaranteed to discard a constant fraction of elements (median of groups of 5 medians → T(n) ≤ T(⌈n/5⌉) + T(⌈7n/10⌉) + O(n) → O(n); constant factor too high for practical use, but theoretically significant).

**Ch 17 (Limits of Computation)**: programs are countable (assignable to bins by length), functions from integers to integers are uncountable (diagonalization: given any enumeration of functions, construct a new function that differs from each at its own index) → unsolvable problems exist; Halting Problem as the canonical unsolvable problem; connection to NP-completeness (efficiently unsolvable vs. provably unsolvable).

## Corpus pages updated

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — ADT/complexity, hashing, B-trees, 2-3 trees, self-organizing lists
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — sorting, MST (Prim's/Kruskal's), Dijkstra's, lower bounds, median-of-medians
- [Complexity Theory and NP-Completeness](/software-engineering/complexity-theory.md) — limits of computation, unsolvable problems

---

[^src1]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 1 (Preface, Ch 1)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-01.md)
[^src2]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 17 (Ch 8 exercises: disk I/O)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-17.md)
[^src3]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 18 (Ch 9: hashing, hash functions, collision resolution)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-18.md)
[^src4]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 20 (Ch 10: 2-3 trees, indexing)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-20.md)
[^src5]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 22 (Ch 11: graphs, MST, Kruskal's)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-22.md)
[^src6]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 27 (Ch 15: lower bounds, median-of-medians)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-27.md)
[^src7]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Part 30 (Ch 17: limits of computation, diagonalization)](../../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-30.md)
