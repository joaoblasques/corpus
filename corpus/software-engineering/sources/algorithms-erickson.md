---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-algorithms-part-01.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-02.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-03.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-04.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-05.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-06.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-07.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-08.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-09.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-10.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-11.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-12.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-13.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-14.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-15.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-16.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-17.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-18.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-19.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-20.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-21.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-22.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-algorithms-part-23.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-algorithms-part-24.md
    channel: pdf
    ingested_at: 2026-07-12
aliases:
  - Algorithms Erickson
  - Jeff Erickson algorithms
  - algorithms.wtf
  - jeffe algorithms
tags:
  - corpus/software-engineering
  - source
created: 2026-07-11
updated: 2026-07-12
---

# Algorithms (Erickson, 2019)

**TL;DR**: Comprehensive 472-page algorithms textbook by Jeff Erickson (University of Illinois at Urbana-Champaign). Free under CC BY 4.0. Covers recursion → divide-and-conquer → dynamic programming → greedy → graph algorithms → minimum spanning trees → shortest paths → network flow → NP-hardness. Grew from 20+ years of algorithms course notes. Available at algorithms.wtf [^src1].

## Prerequisites assumed

Discrete mathematics, proof techniques (induction, contradiction, exchange arguments), iterative programming, and fundamental data structures (stacks, queues, priority queues, ordered maps). Not a first algorithms course [^src1].

## Chapter structure

| Chapter | Topic | Key content |
|---|---|---|
| 0 | Introduction | History of multiplication algorithms (Fibonacci/Egyptian); O(mn) lattice multiplication; peasant multiplication (duplation/mediation) |
| 1 | Recursion | Tower of Hanoi (canonical recursion); "Recursion Fairy" mental model; structural induction |
| 2 | Backtracking | — |
| 3 | Dynamic Programming | Sequence DP, subset DP, optimal BSTs |
| 4 | Greedy Algorithms | Exchange argument proofs; tape sorting; Huffman codes (prefix-free binary codes, optimal encoding) |
| 5 | Basic Graph Algorithms | DFS/BFS, topological sort, DAGs |
| 6 | Depth-First Search | SCCs, bridge finding |
| 7 | Minimum Spanning Trees | Borůvka (MST algorithm you want), Jarník/Prim, Kruskal; exchange argument correctness |
| 8 | Shortest Paths | Dijkstra, Bellman-Ford, Johnson's algorithm |
| 9 | All-Pairs Shortest Paths | Floyd-Warshall |
| 10 | Maximum Flows & Min Cuts | Ford-Fulkerson |
| 11 | Applications of Flows | Bipartite matching, demographic ad assignment |
| 12 | NP-Hardness | Polynomial-time reductions, Cook-Levin; MaxIndSet, MaxClique, VertexCover, 3-colorability, HamCycle (two proofs), SubsetSum; NP-hard problems list; draughts reduction from HamCycle |

## Key pedagogical concepts

**"Recursion Fairy" model**: when writing a recursive algorithm, assume the recursive call works correctly and focus only on the top-level reduction. Avoids the temptation to trace recursion manually [^src3].

**Exchange argument for greedy correctness**: assume an optimal solution differs from the greedy solution at the "first" difference; show that swapping the optimal choice for the greedy choice does not make the solution worse; conclude by induction that the greedy solution is optimal [^src10].

**Huffman codes**: given character frequencies, build the optimal prefix-free binary code by repeatedly merging the two least-frequent symbols into a parent node. Correct because the greedy exchange argument shows the two least-frequent symbols belong at the same depth [^src10].

**Borůvka's MST**: the oldest MST algorithm (1926), but Erickson argues it is the best in practice. Parallelism-friendly; achieves O(E) for planar graphs; generalizes to all modern fast MST algorithms [^src15].

**Jarník's ("Prim's") algorithm**: actually independently discovered by Vojtěch Jarník (1930), then Kruskal (1956), Prim (1957), Loberman & Weinberger (1957), and Dijkstra (1958). Named after Prim in most textbooks despite Jarník's priority [^src15].

**NP-hardness proof patterns (Ch 12)**: reductions follow a three-part template — (1) polynomial-time transform of arbitrary instance of X to special instance of Y; (2) "if X is good then Y is good"; (3) "if Y is good then X is good" (the hardest direction). The certificate transformation must be reversible; the instance transformation need not be. Decomposing into **gadgets** (subgraphs encoding semantics) is the key design strategy [^src22].

**Key reductions from Ch 12**:
- MaxIndSet ← 3-SAT (clause triangles + variable edges); MaxClique = MaxIndSet on complement graph; MinVertexCover = n − MaxIndSet.
- 3-colorability ← 3-SAT (truth gadget + variable gadgets + clause gadgets with "majority gate" triangles).
- DirectedHamCycle ← VertexCover (edge gadgets + vertex chains + cover vertices); also ← 3-SAT (variable gadgets as doubly-linked lists + clause vertices).
- SubsetSum ← VertexCover (base-4 integer encoding; each edge contributes one digit, each vertex contributes its incident edges + a 1 in the top digit).
- **Pseudo-polynomial vs. strongly NP-hard**: SubsetSum is solvable in O(nT) pseudo-polynomial DP (T can be exponential in input bits — weakly NP-hard). TravelingSalesman on unit-weight graphs is strongly NP-hard [^src22].
- **International draughts example**: finding a legal move in the n×n generalization is NP-hard by reduction from HamCycle; this is unique in being a real-world game where merely following the rules is NP-hard [^src23] [^src22].

## Corpus pages produced from this source

- [Algorithms](/software-engineering/algorithms.md) — updated with divide-and-conquer, greedy, MST, shortest paths, sorting lower bound content
- [Complexity Theory](/software-engineering/complexity-theory.md) — NP-hardness, reductions, gadget-based proofs content
- [Data Structures](/software-engineering/data-structures.md) — graph representations referenced

---

[^src1]: [Algorithms, Erickson — Part 1 (Preface, prerequisites)](../../../raw/pdf/pdf-algorithms-part-01.md)
[^src3]: [Algorithms, Erickson — Part 3 (Recursion: Tower of Hanoi, Recursion Fairy)](../../../raw/pdf/pdf-algorithms-part-03.md)
[^src10]: [Algorithms, Erickson — Part 10 (Greedy: exchange arguments, Huffman codes)](../../../raw/pdf/pdf-algorithms-part-10.md)
[^src15]: [Algorithms, Erickson — Part 15 (MST: Borůvka, Jarník/Prim)](../../../raw/pdf/pdf-algorithms-part-15.md)
[^src22]: [Algorithms, Erickson — Part 22 (NP-hardness: MaxIndSet→MaxClique/VertexCover, 3-colorability, HamCycle, SubsetSum, NP-hard list)](../../../raw/pdf/pdf-algorithms-part-22.md)
[^src23]: [Algorithms, Erickson — Part 23 (NP-hardness: draughts reduction from HamCycle)](../../../raw/pdf/pdf-algorithms-part-23.md)
