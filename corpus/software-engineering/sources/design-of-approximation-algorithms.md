---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-01.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-02.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-03.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-04.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-05.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-06.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-07.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-the-design-of-approximation-algorithms-part-08.md
    channel: pdf
    ingested_at: 2026-07-21
aliases:
  - Design of Approximation Algorithms
  - Williamson Shmoys
  - approximation algorithms textbook
  - set cover approximation
  - LP rounding
  - primal-dual approximation
  - facility location approximation
  - MAX SAT approximation
  - MAX CUT approximation
  - bin packing approximation
  - TSP approximation
  - greedy approximation algorithms
  - performance guarantee algorithms
tags:
  - corpus/software-engineering
  - source
created: 2026-07-21
updated: 2026-07-21
---

# The Design of Approximation Algorithms (Williamson & Shmoys, 2011)

TL;DR: A graduate textbook by David P. Williamson and David B. Shmoys (Cambridge University Press, 2011; 500 pages; open-access electronic edition). Organized around **design techniques** rather than individual problems: each technique is applied to several NP-hard optimization problems. Parts 1-8 of 34 ingested, covering Chapters 1-5 (set cover through randomized rounding). Intended for graduate students and researchers; assumes undergraduate algorithms and NP-completeness background.

## Structure (parts 1-8 cover Chapters 1–5)

| Chapter | Topic | Parts |
|---|---|---|
| 1 | Introduction — set cover; greedy, LP relaxation, primal-dual illustrated on one problem | 1-2 |
| 2 | Greedy algorithms and local search — submodular functions, float maximization (1−1/e), minimum-degree spanning trees | 3-4 |
| 3 | Rounding data and dynamic programming — bin packing (APTAS), knapsack FPTAS | 5 |
| 4 | Deterministic rounding of linear programs — weighted vertex cover, LP duality | 6-7 |
| 5 | Random sampling and randomized rounding of LP — MAX SAT, MAX CUT | 8 |

## Design techniques (Chapters 1-5)

### Greedy + set cover (Chapter 1)
The canonical greedy set cover algorithm: repeatedly pick the set that covers the most uncovered elements. Achieves an **H_n ≈ ln n** approximation ratio, where H_n is the n-th harmonic number. The proof uses the exchange-argument/potential technique: at each step, some set in the optimum must cover ≥ OPT/k remaining elements (for k = OPT size), so the greedy picks something at least that good. [^daa-p01]

### Submodular function maximization (Chapter 2)
A set function v is **submodular** if marginal gains diminish: v(X ∪ {ℓ}) − v(X) ≥ v(Y ∪ {ℓ}) − v(Y) whenever X ⊆ Y. The greedy algorithm (add the element with the highest marginal value) gives a **(1 − 1/e)** approximation for maximizing a monotone submodular function subject to a cardinality constraint. Proof via the inequality 1 − x ≤ e^{−x} applied repeatedly to the gap between greedy value and OPT. [^daa-p04]

### Bin packing (Chapter 3)
Bin packing is strongly NP-hard (no FPTAS unless P = NP). An **APTAS** (asymptotic polynomial-time approximation scheme) exists: for any ε > 0, there is a polynomial algorithm using at most (1+ε)OPT + O(1/ε²) bins. The approach rounds item sizes up to a bounded number of groups (eliminating tiny items via First Fit Decreasing), then uses LP rounding on the rounded instance.

### LP rounding for weighted vertex cover (Chapter 4)
LP relaxation: replace integer constraints x_v ∈ {0,1} with x_v ∈ [0,1]; solve LP in polynomial time. Round up: set x_v = 1 whenever x_v ≥ 1/2. This gives a **2-approximation**: every edge is covered (both LP constraints were ≥ 1/2, at least one rounds to 1), and the rounded solution costs ≤ 2 × OPT_LP ≤ 2 × OPT_IP.

### Randomized rounding — MAX SAT and MAX CUT (Chapter 5)
**MAX SAT**: set each variable to TRUE with probability 1/2 independently. Expected weight of satisfied clauses ≥ OPT/2 (since any clause of length ≥ 1 is satisfied with probability ≥ 1/2). If all clauses have length ≥ k, the guarantee improves to (1 − (1/2)^k) × OPT. The PCP theorem (Theorem 5.2) implies no (7/8 + ε)-approximation for MAX E3SAT unless P = NP. [^daa-p08]

**MAX CUT**: place each vertex in U independently with probability 1/2. Expected cut weight ≥ OPT/2. An edge is in the cut iff its endpoints are in different parts, which happens with probability 1/2 per edge. [^daa-p08]

## Key theorems

- **Greedy set cover**: H_k ≤ ln k + 1 ≈ ln(OPT) approximation ratio; tight — no better factor unless NP ⊆ DTIME(n^{O(log log n)}).
- **Submodular maximization**: (1 − 1/e) ≈ 0.632 approximation; tight for greedy.
- **(7/8 + ε)-hardness of MAX E3SAT**: if such an algorithm exists, P = NP (from the PCP theorem). [^daa-p08]

## Relationship to other corpus pages

- [Complexity Theory](/software-engineering/complexity-theory.md) — approximation algorithms are the response to NP-hardness; NP-complete problems, P vs NP, and the PCP theorem are covered there.
- [Algorithms](/software-engineering/algorithms.md) — greedy algorithms, network flow, and MST appear there with correctness proofs; this source adds approximation ratios for NP-hard variants.
- [Text Algorithms](/software-engineering/sources/text-algorithms.md) — shortest common superstring approximation (Gallant, Chapter 15 of that book) is an instance of the greedy overlap framework discussed here.

[^daa-p01]: raw/pdf/pdf-the-design-of-approximation-algorithms-part-01.md — Preface; Chapter 1: set cover, performance guarantee definition, greedy algorithm
[^daa-p04]: raw/pdf/pdf-the-design-of-approximation-algorithms-part-04.md — Chapter 2: submodular function maximization, float maximization, (1−1/e) proof
[^daa-p08]: raw/pdf/pdf-the-design-of-approximation-algorithms-part-08.md — Chapter 5: MAX SAT 1/2-approximation, MAX CUT 1/2-approximation, (7/8+ε)-hardness via PCP theorem
