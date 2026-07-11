---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-11.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-19.md
    channel: pdf
    ingested_at: 2026-07-11
aliases:
  - complexity theory
  - NP-completeness
  - P vs NP
  - NP-hard
  - polynomial reduction
  - computational complexity
  - NP
  - P
  - co-NP
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-11
updated: 2026-07-11
---

# Complexity Theory and NP-Completeness

**TL;DR**: Complexity theory classifies problems by the resources (time, space) required to solve them. The central open question — **P vs NP** — asks whether problems whose solutions are easy to verify (NP) are also easy to find (P). NP-complete problems are the hardest in NP; a polynomial-time algorithm for any one would solve all [^src1].

## Complexity classes

| Class | Definition | Canonical members |
|---|---|---|
| **P** | Solvable in polynomial time O(n^k) by a deterministic algorithm | Sorting, shortest paths, max-flow |
| **NP** | Solutions *verifiable* in polynomial time | SAT, TSP decision, graph coloring, independent set |
| **co-NP** | Complements of NP problems — *negative* answers verifiable | UNSAT, complement of clique |
| **NP-complete** | In NP AND every NP problem reduces to it in polynomial time | SAT (Cook-Levin), 3-SAT, 3-colorability, Hamiltonian cycle |
| **NP-hard** | Every NP problem reduces to it; may not be in NP | Optimization versions of NP-complete problems |

The famous question: **P = NP?** — most researchers believe P ≠ NP, but no proof exists [^src1].

## Polynomial-time reductions

A problem A **reduces** to problem B (A ≤_P B) if: given an efficient algorithm for B, we can construct an efficient algorithm for A by transforming A-instances to B-instances in polynomial time. Reductions compose: if A ≤_P B and B ≤_P C, then A ≤_P C [^src2].

**Cook-Levin theorem (1971)**: Boolean Satisfiability (SAT) is NP-complete — the first proved NP-complete problem. All NP problems reduce to SAT. Once one NP-complete problem is known, others are proved NP-complete by reducing from a known NP-complete problem (transitivity of reductions) [^src2].

## The standard NP-completeness toolkit

Commonly reduced-from problems (each useful for different new reductions):

- **3-SAT**: each clause has exactly 3 literals; NP-complete even with this restriction
- **3-colorability**: is a graph 3-vertex-colorable? NP-complete; average backtrack search uses ~197 steps on random graphs despite worst-case hardness [^src1]
- **Independent Set**: largest set of pairwise non-adjacent vertices
- **Clique**, **Vertex Cover**, **Hamiltonian Cycle**, **TSP** (decision version)

## Average case vs. worst case

NP-completeness is a worst-case notion. Many NP-complete problems are easy on random instances:

> "The average number of nodes in the backtrack search tree for [3-colorability] is about 197, averaged over all graphs of all sizes. This means that if we input a random graph of 1,000,000 vertices, and ask if it is 3-colorable, we can expect an answer (probably 'No') after only about 197 steps of computation." [^src1]

This is why NP-completeness does not mean "hard in practice" for most real inputs — heuristics, approximation algorithms, and average-case easy instances make NP-hard problems tractable in many applications.

## Approximation algorithms

When exact polynomial-time solution is impossible (assuming P ≠ NP), approximation algorithms guarantee a solution within a constant factor of optimal:

- **Vertex Cover**: a 2-approximation exists (take both endpoints of any maximal matching).
- **TSP with triangle inequality**: 1.5-approximation via Christofides algorithm.
- **General TSP**: no constant-factor approximation exists unless P = NP.

## Dealing with NP-hardness in practice

1. **Small input size**: exact exponential algorithms (branch-and-bound, ILP solvers) work for n ≤ 30–50.
2. **Approximation**: accept near-optimal solutions with guaranteed bounds.
3. **Parameterized complexity**: exponential in a small parameter *k* (e.g., treewidth, pathwidth) but polynomial in *n* — FPT algorithms.
4. **Randomization**: sometimes expected polynomial time (e.g., randomized 3-SAT solvers on random instances).
5. **Heuristics**: no worst-case guarantees but empirically fast (genetic algorithms, simulated annealing, SAT solvers like CDCL).

## Connections to other corpus pages

- [Algorithms](/software-engineering/algorithms.md) — all polynomial-time algorithms implicitly operate within the P class.
- [Data Structures](/software-engineering/data-structures.md) — NP-completeness proofs often encode data structures (graphs, sequences) as inputs.
- [Algorithms and Complexity (Wilf)](/software-engineering/sources/algorithms-and-complexity-wilf.md) — Chapter 5 source.
- [Algorithms (Erickson)](/software-engineering/sources/algorithms-erickson.md) — Chapter 12 source.

---

[^src1]: [Algorithms and Complexity, Wilf — Part 11 (Ch 5: NP, backtracking, graph coloring)](../../raw/pdf/pdf-algorithms-and-complexity-part-11.md)
[^src2]: [Algorithms, Erickson — Part 19 (NP-hardness, reductions)](../../raw/pdf/pdf-algorithms-part-19.md)
