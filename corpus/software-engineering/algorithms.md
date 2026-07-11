---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-fkcfaapypuq.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-08-youre-learning-algorithms-the-wrong-way.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/_inbox/pdf-algorithms-and-complexity-part-01.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-algorithms-part-01.md
    channel: pdf
    ingested_at: 2026-07-11
aliases:
  - algorithms
  - recursion
  - binary search
  - dynamic programming
  - memoization
  - divide and conquer
  - tree traversal
  - linear search
  - sorting algorithms
  - merge sort
  - quick sort
  - bubble sort
  - quicksort
  - pathfinding
  - Dijkstra's algorithm
  - minimum spanning tree
  - Prim's algorithm
  - Borůvka's algorithm
  - Kruskal's algorithm
  - greedy algorithm
  - Huffman codes
  - network flow
  - Ford-Fulkerson
  - FFT
  - discrete Fourier transform
  - Strassen matrix multiplication
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-15
updated: 2026-07-11
---

# Algorithms (Strategies, Not Tricks)

**TL;DR** — Algorithms are best learned as **strategies to reach for**, not solutions to memorize. "The goal is not to memorize every algorithm as a separate trick… [it's] to understand the strategy behind each one, so when a similar problem shows up, you know what to reach for" [^src2]. The recurring strategies: **recursion** (break a problem into smaller copies of itself), **divide and conquer** (e.g. binary search halves the search space), and **dynamic programming / memoization** (cache results so you never recompute the same subproblem) [^src1][^src2]. This is the algorithmic companion to [Data Structures and Big O Notation](/software-engineering/data-structures.md).

## The six interview-relevant categories

The source frames the curriculum as **six key types of algorithms** worth knowing for any CS course or technical interview: recursion, linear/binary search, sorting algorithms, pathfinding, minimum spanning tree, and dynamic programming [^src1]. The presenter is explicit that the point is strategy acquisition, not memorization: the goal is "to teach you how recursion works and how you can apply this to any arbitrary problem" so the strategies live "in your tool belt" for harder problems later [^src1]. The categories below build on the recursion / binary-search / DP core already detailed; the remaining three — sorting, pathfinding (Dijkstra), and MST (Prim's) — operate over the [data structures](/software-engineering/data-structures.md) (arrays, heaps, graphs) catalogued separately.

## Recursion

A function that calls itself; every recursive algorithm needs two parts [^src1][^src2]:

- **Base case** — a situation where the answer is already known and no further recursion happens.
- **Recursive case** — call the same function on a smaller version of the problem.

This is **divide and conquer**: solve a hard problem by solving its subproblems, then combining [^src1]. Canonical example — Fibonacci: base cases `f(1)=1`, `f(2)=1`; recursive case `f(n)=f(n-1)+f(n-2)` [^src1][^src2]. Recursion also expresses non-numeric problems cleanly: in-order / pre-order / post-order **binary-tree traversal** (base case `node == null`), and reversing a string as `reverse(s) = reverse(s[1:]) + s[0]` [^src1].

> Gotcha: naive recursive Fibonacci is **O(2ⁿ)** — it recomputes the same subproblems exponentially often, becoming "infeasible" by n≈70 [^src1].

## Binary search (divide and conquer)

Works **only on a sorted array** [^src2]. Check the middle element; if it equals the target you're done, otherwise the sorted property tells you which half to discard — every step halves the remaining problem, giving **O(log n)** vs. O(n) for a linear scan [^src1][^src2]. Implemented recursively by passing `start`/`end` indices (base case `start > end` → not found) rather than slicing, to avoid the O(k) cost of rebuilding subarrays [^src1].

Trade-off worth knowing: sorting first is O(n log n), so binary search pays off when you do **repeated** searches over the same data; a single lookup may be cheaper with a linear scan [^src1].

## Dynamic programming & memoization

DP "simply means reusing results you already calculated instead of solving the same smaller problem again" [^src2]. **Memoization** is the cache: store each computed value (e.g. in an object/dict) and return it on re-request [^src1]. Applied to Fibonacci, this collapses O(2ⁿ) → **O(n) time** at the cost of **O(n) space**; an iterative version (track only the last two terms) keeps O(n) time at **O(1) space** [^src1].

| Fibonacci approach | Time | Space |
|---|---|---|
| Naive recursion | O(2ⁿ) | O(n) call stack |
| Memoized recursion | O(n) | O(n) |
| Iterative | O(n) | O(1) |

## Sorting algorithms

Two properties classify a sort [^src1]:

- **Stable** — elements with the same key "maintain the same relative order as in the original array" [^src1].
- **In-place** — mutates the original array rather than building a new sorted one; "most of these work" this way [^src1].

The source splits the algorithms by efficiency [^src1]:

| Sort | Time | Stable? |
|---|---|---|
| Selection sort | O(n²) | No |
| Insertion sort | O(n²) | Yes |
| Bubble sort | O(n²) | Yes |
| Merge sort | O(n log n) | Yes |
| Heap sort | O(n log n) | No (uses a heap) |
| Quick sort | O(n log n) | No |

Practical takeaway: selection / insertion / bubble are the simple-but-slow O(n²) family; merge / heap / quick are the efficient O(n log n) family. Because languages typically implement quick sort or merge sort under the hood (e.g. JavaScript's built-in `sort`), "we assume that when we need to sort something that it will run in… O(n log n)" — which is exactly the precondition the [binary search](/software-engineering/algorithms.md) above trades against [^src1].

## Pathfinding — Dijkstra's algorithm

Dijkstra's is a pathfinding algorithm over a **weighted graph** that finds "the smallest distance and path from any starting vertex to every other vertex in the graph" [^src1]. Run from a start vertex A, it yields both the shortest distance and the shortest path to every other vertex [^src1]. The motivation is scale: a human can trace shortest paths on a tiny graph, but past ~20–50 nodes it becomes infeasible by hand, so "having computer systems that can… determine the shortest possible path in a graph is actually very powerful" — used in "millions of different programs," GPS routing being the canonical example [^src1]. Operates over the graph structures in [Data Structures and Big O Notation](/software-engineering/data-structures.md).

## Minimum spanning tree — Prim's algorithm

A **spanning tree** of a graph is "a set of edges such that they connect all of the different vertices but there is no cycle" [^src1]. The **minimum spanning tree (MST)** is the spanning tree whose total edge weight is the smallest possible [^src1]. Finding the MST is non-trivial: the naive approach — enumerate every spanning tree and compare total weights — is intractable, so a greedy algorithm is used instead. The source demonstrates **Prim's algorithm**, which grows the tree by repeatedly adding the cheapest edge that extends the current tree (defined on an undirected weighted graph) until `V − 1` edges are included; Kruskal's is named as the alternative greedy MST algorithm [^src1].

> A graph can have more than one MST of equal minimum total weight [^src1].

## Why this still matters under AI tooling

"You may use built-in tools most of the time, but understanding algorithms still matters because the same ideas show up everywhere: slow code, repeated work, structured data, and simple solutions that do more work than they should" [^src2]. The strategies-not-tricks framing is also interview advice — these are "the parts of the algorithms you actually need to know… [for] technical interviews" [^src1]. This connects to the fundamentals-under-AI argument in [AI-Assisted Development](/software-engineering/ai-assisted-development.md) and the interview-fluency point in [Navigating a Technical Career](/ai-business/technical-career.md) (practice DSA without autocomplete).

## Greedy algorithms

Greedy algorithms make the locally optimal choice at each step and never reconsider. Correctness proofs use the **exchange argument**: assume an optimal solution differs from greedy at the "first" point; show swapping the optimal choice for the greedy choice doesn't worsen the solution; conclude greedy is optimal by induction [^src4].

**Huffman codes**: given symbol frequencies, build an optimal prefix-free binary code by repeatedly merging the two least-frequent nodes. Each symbol's code length equals its depth in the code tree; minimizing weighted depth minimizes the total encoded message length. The proof is a greedy exchange argument — the two least-frequent symbols must be at the same (maximum) depth in any optimal code [^src4].

**Scheduling**: greedy task scheduling by increasing deadline order minimizes maximum lateness. Tape sorting (minimize average seek time) solved by scheduling in order of increasing processing time [^src4].

## Advanced graph algorithms

**Network flow (Ford-Fulkerson)**: finds the maximum flow from a source *s* to a sink *t* in a directed capacitated network by repeatedly finding augmenting paths in the residual graph. The **max-flow min-cut theorem** guarantees maximum flow = minimum cut capacity — the most important duality in combinatorial optimization [^src3].

**Minimum spanning tree algorithms**:
- **Borůvka's (1926)**: in each phase, every component adds its cheapest outgoing edge; halves component count per phase → O(E log V). Unique advantages: parallelism-friendly (each component is independent), often faster than worst-case, and generalizes to all known sub-O(E log V) MST algorithms. Erickson argues this is "the MST algorithm you want" in practice [^src5].
- **Kruskal's**: sort all edges by weight; add the next edge if it doesn't create a cycle (use Union-Find). O(E log E).
- **Prim's / Jarník's**: grow a single tree by repeatedly adding the cheapest edge to a non-tree vertex. O(E log V) with a binary heap. Originally by Vojtěch Jarník (1930), not Prim.

**FFT (Fast Fourier Transform)**: reduces polynomial multiplication from O(n²) to O(n log n) by converting between coefficient and value representations at *n* roots of unity. Critical for signal processing, high-precision arithmetic, and polynomial operations [^src3_wilf].

**Strassen matrix multiplication**: multiplies n×n matrices in O(n^{log_2 7}) ≈ O(n^{2.81}) by reducing 8 recursive multiplications to 7. A divide-and-conquer algorithm — the structure generalizes: any method doing *k* multiplications of M×M blocks yields O(n^{log_M k}) [^src3_wilf].

## NP-completeness

Some problems have no known polynomial algorithm and are suspected to require exponential time. See [Complexity Theory](/software-engineering/complexity-theory.md) for full coverage.

## See also

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — the complexity classes (O(1)/O(log n)/O(n)/O(n²)) these strategies trade in, and the structures (stacks, trees, hashmaps) the algorithms operate on.
- [Complexity Theory](/software-engineering/complexity-theory.md) — P vs NP, NP-complete problems, reductions.
- [Software Design Principles](/software-engineering/software-design-principles.md) — simplicity as a design value mirrors "don't do more work than needed."

[^src1]: [Famous Computer Science Algorithms (recursion, search, DP)](../../raw/youtube/youtube-fkcfaapypuq.md) (Tech With Tim; fetched via the source email)
[^src2]: [you're learning algorithms the wrong way](../../raw/email/email-2026-06-08-youre-learning-algorithms-the-wrong-way.md) (Tech With Tim newsletter)
[^src3_wilf]: [Algorithms and Complexity, Wilf — Part 5 (FFT, Strassen)](../../raw/pdf/pdf-algorithms-and-complexity-part-05.md)
[^src4]: [Algorithms, Erickson — Part 10 (Greedy: exchange argument, Huffman)](../../raw/pdf/pdf-algorithms-part-10.md)
[^src5]: [Algorithms, Erickson — Part 15 (MST: Borůvka, Jarník)](../../raw/pdf/pdf-algorithms-part-15.md)
[^src3]: [Algorithms, Erickson — Part 21 (Network Flow applications)](../../raw/pdf/pdf-algorithms-part-21.md)
