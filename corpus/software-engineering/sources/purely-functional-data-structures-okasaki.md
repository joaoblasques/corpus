---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-02.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-03.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-04.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-05.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-06.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-07.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-08.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-09.md
    channel: pdf
    ingested_at: 2026-07-13
aliases:
  - Okasaki functional data structures
  - purely functional data structures
  - Okasaki 1996
  - persistent data structures Okasaki
tags:
  - corpus/software-engineering
  - source
created: 2026-07-13
updated: 2026-07-13
---

# Purely Functional Data Structures (Okasaki, CMU 1996)

**TL;DR**: Okasaki's CMU PhD thesis establishes foundational techniques for designing efficient *purely functional* data structures — structures that work correctly even when old versions are retained (persistence). The central contribution is showing that **lazy evaluation with memoization** makes amortized analysis compatible with persistence [^src1].

## The core problem

In imperative languages, efficient data structures rely on in-place mutation. In functional languages (Standard ML, Haskell), assignments are disallowed. Most imperative structures can't be directly ported because they depend on mutation. Additionally, functional languages provide *persistence* by default — old versions of a structure remain accessible after updates. Traditional amortization arguments break down in persistent settings.

## Why traditional amortization fails with persistence

The banker's method (credit invariant) and physicist's method (potential function) both assume each operation has a **unique future** — that accumulated savings are spent at most once. With persistence, a data structure can have **multiple logical futures**: the same old version can be used as input to many operations, each computing independently.

If version q accumulated savings to pay for one expensive operation, and q is used in n independent futures each triggering that operation, the savings are exhausted after the first use and the remaining n-1 futures have nothing to draw on. Both amortization methods break [^src2].

> "Although savings can only be spent once, it does no harm to pay off debt more than once." [^src2]

## Lazy evaluation as the solution

**Call-by-need** (lazy evaluation with memoization): a computation is suspended until needed; on first evaluation it runs and memoizes the result; all subsequent accesses return the cached result in O(1).

Applied to amortization: replace accumulated *savings* with accumulated *debt* (cost of unevaluated suspensions). An expensive operation is suspended; the first caller forces it and pays the full cost; subsequent callers get the memoized result for free. The expensive computation is paid for once regardless of how many futures exist. This is exactly the behavior needed for persistent amortization [^src2].

Without side-effects, this is impossible under strict (call-by-value) or call-by-name (lazy without memoization) evaluation — every invocation takes the same time. Only call-by-need enables it.

## Example: functional queues (two-list representation)

A common functional queue [Gri81, HM81, Bur82] uses two lists `F` (front, in order) and `R` (rear, reversed). Invariant: F is empty only if R is also empty. When F would become empty, `rev R` is installed as the new F and R is reset to `[]`.

- `snoc`: append to R; O(1) worst-case
- `head`: read first element of F; O(1) worst-case
- `tail`: remove first element of F; O(n) worst-case (when reversal triggered), O(1) amortized

Amortized proof (physicist's method): potential = length of R. Every `snoc` raises potential by 1 (amortized cost 2); every `tail` with reversal spends m steps and reduces potential by m (amortized cost 1). Total amortized cost is O(1) per operation [^src2].

Problem with persistence: if the same queue q is used to call `tail` n times, each call triggers the same O(n) reversal — no memoization means no savings. Solution: make the reversal a suspension; the first `tail` forces and memoizes it; subsequent `tail q` calls retrieve the cached result [^src2].

## Key data structures in the thesis

| Structure | Key property | Complexity |
|---|---|---|
| Binomial heaps | Functional implementation via binomial trees | O(log n) merge/insert/delete-min |
| Leftist heaps | Rank-based merge; right spine bounded by log n | O(log n) merge |
| Binary random-access lists | Encode size in binary; each 1-bit → complete binary tree | O(log n) random access, O(log n) cons/tail |
| Binomial queues (lazy) | Lazy merging of binomial trees | O(1) amortized insert |
| Finger trees | Deque generalization with monoidal annotation | O(1) amortized front/back, O(log n) split/concat |
| Bootstrapped heaps | Use simpler heap to implement more complex | O(1) insert, O(log n) delete-min |

## Numerical representations

A systematic framework for designing functional data structures: encode a collection of size n using a positional number system (binary, skew binary, etc.). Each digit corresponds to a tree of that size/rank. The "carry" operation in arithmetic corresponds to *linking* two trees of equal rank into one of the next rank. This gives a uniform way to design random-access lists, priority queues, and other structures [^src3].

Three tree types used: complete binary leaf trees, binomial trees, pennants. Each supports O(1) link/unlink.

## See also

- [Functional and Persistent Data Structures](/software-engineering/functional-persistent-data-structures.md) — concept page derived from this source
- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — imperative counterpart
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — amortization analysis context
- [Data Structures and Algorithm Analysis in Java (Shaffer)](/software-engineering/sources/algorithms-shaffer-java.md) — imperative DSA textbook

---

[^src1]: [Purely Functional Data Structures, Okasaki — Part 1 (Abstract, Introduction)](../../../raw/pdf/pdf-purely-functional-data-structures-part-01.md)
[^src2]: [Purely Functional Data Structures, Okasaki — Part 2 (Amortization and Persistence via Lazy Evaluation)](../../../raw/pdf/pdf-purely-functional-data-structures-part-02.md)
[^src3]: [Purely Functional Data Structures, Okasaki — Part 5 (Numerical Representations)](../../../raw/pdf/pdf-purely-functional-data-structures-part-05.md)
