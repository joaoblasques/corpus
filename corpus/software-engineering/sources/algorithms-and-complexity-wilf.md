---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-01.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-02.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-03.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-04.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-05.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-06.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-07.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-08.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-09.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-10.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-11.md
    channel: pdf
    ingested_at: 2026-07-11
aliases:
  - Algorithms and Complexity
  - Wilf algorithms
  - Herbert Wilf
tags:
  - corpus/software-engineering
  - source
created: 2026-07-11
updated: 2026-07-11
---

# Algorithms and Complexity (Wilf, 1994)

**TL;DR**: Classic 139-page textbook by Herbert S. Wilf (University of Pennsylvania). Free for educational use. Five chapters spanning recursion + FFT, network flow, number theory, and NP-completeness. Mathematically rigorous — proofs and asymptotic analysis are front and center. Internet edition summer 1994; second edition (with solutions) published 2003 [^src1].

## Chapter structure

| Chapter | Topic | Key algorithms |
|---|---|---|
| 0 | What this book is about: hard vs. easy problems, preview | — |
| 1 | Mathematical Preliminaries | Orders of magnitude (Big-O), positional number systems, series, recurrences, counting (binomial), graphs |
| 2 | Recursive Algorithms | Quicksort, recursive graph algorithms (DFS/BFS), fast matrix multiplication (Strassen O(n^{log_2 7})), discrete Fourier transform (FFT: O(n²) → O(n log n)) |
| 3 | Network Flow | Ford-Fulkerson max-flow, max-flow min-cut theorem, MPM algorithm, applications |
| 4 | Algorithms in the Theory of Numbers | Euclidean algorithm, primality, cryptographic applications |
| 5 | NP-completeness | P vs NP, polynomial-time reductions, backtracking (independent sets, graph coloring average-case O(1)) |

## Key contributions to the corpus

**FFT**: The Fourier transform converts polynomial representation from coefficient form to value form at n points. Naive evaluation: O(n²) multiplications. FFT exploits the structure of *n*-th roots of unity to reduce to O(n log n). Applications: polynomial multiplication, high-precision integer arithmetic, signal processing (CAT/NMR scanners) [^src5].

**Network flow**: The Ford-Fulkerson algorithm repeatedly finds augmenting paths in the residual graph. The **max-flow min-cut theorem** guarantees correctness: maximum flow = minimum cut capacity. The MPM layered-network algorithm achieves O(V³) on unit-capacity networks [^src1].

**NP-completeness**: Some problems appear to require exponential time; NP-complete problems are those to which any NP problem reduces in polynomial time. But average-case analysis reveals surprises: 3-coloring of random graphs requires on average only ~197 backtracking steps, regardless of graph size [^src11].

## Pedagogical style

Wilf's approach: brief, clear, mathematical. Exercises are integral — solutions in the 2003 second edition. The book is explicitly aimed at computer science students who already have mathematical maturity [^src1].

## Corpus pages produced from this source

- [Algorithms](/software-engineering/algorithms.md) — updated with FFT, network flow, NP-completeness content
- [Complexity Theory](/software-engineering/complexity-theory.md) — new concept page seeded from Chapter 5

---

[^src1]: [Algorithms and Complexity, Wilf — Part 1 (TOC, Ch0, Ch1 intro)](../../../raw/pdf/pdf-algorithms-and-complexity-part-01.md)
[^src5]: [Algorithms and Complexity, Wilf — Part 5 (DFT/FFT)](../../../raw/pdf/pdf-algorithms-and-complexity-part-05.md)
[^src11]: [Algorithms and Complexity, Wilf — Part 11 (Backtracking, graph coloring)](../../../raw/pdf/pdf-algorithms-and-complexity-part-11.md)
