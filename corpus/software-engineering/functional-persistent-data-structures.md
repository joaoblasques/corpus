---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-02.md
    channel: pdf
    ingested_at: 2026-07-13
aliases:
  - functional data structures
  - persistent data structures
  - immutable data structures
  - persistent queues
  - functional queues
  - lazy data structures
  - amortized functional data structures
  - purely functional data structures
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-13
updated: 2026-07-13
---

# Functional and Persistent Data Structures

**TL;DR**: Purely functional data structures achieve the same asymptotic complexity as imperative ones while supporting *persistence* — old versions remain accessible after updates. The key enabling technique is **lazy evaluation with memoization**, which makes amortized analysis hold even when a data structure has multiple logical futures [^src1].

## Functional vs. imperative data structures

Imperative data structures (arrays, hash tables, linked lists with in-place mutation) rely on *assignment*. In functional languages (ML, Haskell) assignments are disallowed. Two consequences:

1. Most imperative data structures can't be directly ported — they depend on mutation for efficiency.
2. Every "update" creates a new version; old versions persist by default.

Persistence is a feature: it enables backtracking, rollback, undo, copy-on-write sharing, and purely functional programming. But it makes standard amortization techniques inapplicable [^src1].

## The persistence-amortization conflict

Traditional amortization (banker's method: credit invariant; physicist's method: potential function) assumes each operation has a **unique future** — savings are spent at most once. With persistence, a data structure has **multiple logical futures**: many operations can use the same old version as input.

If version q accumulated savings for one expensive operation, and n independent futures each trigger that operation on q, the savings are exhausted after the first use. The second through nth futures have no savings to draw on — the amortized bounds fail [^src1].

> "Although savings can only be spent once, it does no harm to pay off debt more than once." — Okasaki [^src1]

The fix: replace accumulated *savings* with accumulated *debt* — the cost of unevaluated lazy computations (suspensions).

## Lazy evaluation as the solution

**Call-by-need** (lazy evaluation with memoization): a computation is suspended until needed; on first evaluation it executes and memoizes the result; subsequent accesses retrieve the cached result in O(1).

Applied to amortization: an expensive operation is encoded as a suspension. The first caller forces it and pays the full cost. All subsequent callers get the memoized result for free. The expensive computation is paid for exactly once, regardless of how many futures exist — satisfying the amortization invariant [^src1].

Key constraint: this only works with call-by-need, not call-by-value (strict) or call-by-name (lazy without memoization). Both strict and call-by-name re-evaluate every invocation at the same cost.

## Example: functional queues

Two-list representation: F (front elements, in order) + R (rear elements, reversed). Invariant: F is non-empty whenever R is non-empty. When F would become empty, `rev R` is installed as the new F and R is reset to empty.

Without laziness: `tail` on a queue with an about-to-be-emptied F triggers `rev R`, costing O(n). With persistence, this O(n) can be triggered from n different futures on the same queue — O(n²) total.

With laziness: the reversal `rev R` is a suspension. The first `tail` forces it (O(n) paid once) and memoizes the result. All subsequent `tail q` calls on the same q retrieve the memoized reversed list in O(1). Total cost: O(n) for any number of futures.

Amortized cost: O(1) per operation (verified by either banker's or physicist's method applied to lazy suspensions).

## Key functional data structures

| Structure | Key property | Complexity |
|---|---|---|
| Functional queue (two-list) | Invariant-based F/R split; lazy reversal | O(1) amortized snoc/tail/head |
| Leftist heap | Rank-based merge; right spine ≤ log n | O(log n) merge, insert, delete-min |
| Binomial heap | Binomial trees; lazy merging | O(log n) or O(1) amortized insert |
| Binary random-access list | Size encoded in binary; 1-bit → complete binary tree | O(log n) random access |
| Finger tree | Deque with monoidal annotation; generalizes many structures | O(1) amortized front/back; O(log n) split/concat |
| Bootstrapped heap | Use simpler heap to implement complex heap | O(1) insert; O(log n) delete-min |

## Numerical representations (systematic framework)

A collection of size n is represented using a positional number system (binary, skew binary). Each digit position corresponds to a tree type. A "carry" in arithmetic = *linking* two trees of the same rank into one of the next rank. This gives a systematic method to design new functional data structures with provable bounds [^src1].

Three common tree types: complete binary leaf trees (elements at leaves only), binomial trees (n nodes in rank-n tree), pennants (n elements in rank-n pennant). All support O(1) link/unlink.

## Selection heuristic

Use functional/persistent structures when:
- You need backtracking, version history, or rollback
- The codebase is functional (ML/Haskell/Clojure/Scala)
- You need copy-on-write semantics without defensive copying

Use imperative structures (see [Data Structures and Big O Notation](/software-engineering/data-structures.md)) when:
- Maximum raw throughput matters and you don't need old versions
- Memory locality is critical (arrays outperform trees on cache)

## See also

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — imperative counterpart; complexity classes shared
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — amortization is a core analysis technique
- [Purely Functional Data Structures (Okasaki)](/software-engineering/sources/purely-functional-data-structures-okasaki.md) — primary source (CMU PhD thesis, 1996)

---

[^src1]: [Purely Functional Data Structures, Okasaki — Parts 1-2 (Abstract, Amortization and Persistence)](../../raw/pdf/pdf-purely-functional-data-structures-part-01.md)
