---
type: concept
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Structures and Big O Notation Explained.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-c-part-01.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-data-structures-and-algorithm-analysis-in-java-part-01.md
    channel: pdf
    ingested_at: 2026-07-12
  - path: raw/_inbox/pdf-purely-functional-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
aliases:
  - data structures
  - Big O notation
  - time complexity
  - arrays
  - linked lists
  - hashmaps
  - binary search tree
  - BST
  - abstract data type
  - ADT
  - hashing
  - hash table
  - B-tree
  - B+-tree
  - union find
  - union-find
  - UNION FIND
  - 2-3 tree
  - self-organizing list
  - move-to-front
  - Zipf distribution
  - deque
  - double-ended queue
  - implicit data structure
tags:
  - corpus/software-engineering
  - concept
created: 2026-05-21
updated: 2026-07-13
---

# Data Structures and Big O Notation

**TL;DR**: Foundational CS reference — Big O complexity classes and time-complexity trade-offs for the eight core data structures. Choose the structure based on which operation (access, insert, delete) dominates in your use case [^src1].

## Big O complexity classes

| Class | Notation | Behavior |
|---|---|---|
| Constant | O(1) | Independent of input size |
| Logarithmic | O(log n) | Halves search space each step |
| Linear | O(n) | Grows proportionally with input |
| Quadratic | O(n²) | Every item interacts with every other |

## Data structure quick reference

| Structure | Access | Insert | Delete | Primary use case |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | Index-based access; contiguous memory |
| Linked List | O(n) | O(1)* | O(1)* | Frequent insert/delete at known position |
| Stack (LIFO) | O(n) | O(1) | O(1) | DFS, undo operations, call stacks |
| Queue (FIFO) | O(n) | O(1) | O(1) | BFS, task scheduling |
| Heap | O(1)† | O(log n) | O(log n) | Priority queues; heap sort |
| Hashmap | O(1) | O(1) | O(1) | Key-value lookup; average case |
| BST | O(log n) | O(log n) | O(log n) | Sorted data; when balanced |
| Set | O(1) | O(1) | O(1) | Uniqueness checks; membership tests |

*If insertion/deletion position is already known. †Root access only.

## Selection heuristics

- **Frequent random access** → Array (O(1) index lookup)
- **Frequent insert/delete, unknown access** → Linked List or Hashmap
- **Need ordering + fast search** → BST (only effective when balanced)
- **Priority-based processing** → Heap
- **Deduplication or membership** → Set or Hashmap

## ADT vs. data structure (Shaffer framing)

An **Abstract Data Type (ADT)** defines the *logical* form: a type plus a set of operations with specified behavior, without specifying implementation. A **data structure** is the *physical* implementation of that ADT. The same ADT (e.g., list) maps to multiple data structures (array-based list, singly linked, doubly linked); choosing among them requires knowing which operations dominate in the application [^src2].

Three selection questions to ask [^src2]:
1. Are all items inserted at the start, or are insertions interleaved with other operations? (Static vs. dynamic.)
2. Can items be deleted? (Complicates implementation.)
3. Are items processed in a fixed order, or is random access required?

## Hashing

Hash tables achieve O(1) average for insert, delete, and exact-match search by mapping keys to array slots via a hash function. Two main collision strategies [^src2]:
- **Open hashing (separate chaining)**: each slot holds a linked list; degrades gracefully but uses extra memory.
- **Closed hashing (open addressing)**: linear probing, quadratic probing, or double hashing; faster when load factor is low, but degrades above ~70% fill. Deletion requires tombstone markers; periodic offline reorganization restores peak efficiency.

> Hashmaps are inappropriate for range queries — use B+-trees or sorted structures when you need "all records where field ∈ [a, b]" [^src2].

## B-trees and B+-trees (disk-optimized indexing)

Designed for secondary storage: each node = one disk block (thousands of keys). Minimize I/O operations by maximizing branching factor [^src2]:
- **B-tree**: keys and records in both internal and leaf nodes.
- **B+-tree**: records only in leaves (linked list for range scans); internal nodes are pure routing keys. Preferred for databases — supports both exact-match and range queries efficiently.

B+-trees vs. hashing: use hashing for exact-match-only workloads (faster); use B+-tree when range queries are needed.

## Union-Find (disjoint-set structure)

Maintains a partition of a set into disjoint groups. Operations: `FIND(x)` returns the group representative; `UNION(a, b)` merges two groups. Used in Kruskal's MST algorithm. With **union by weight** + **path compression**, amortized cost per operation approaches O(1) (inverse Ackermann function) [^src2].

## Self-organizing lists and Zipf distribution

Real-world access patterns are rarely uniform. The **Zipf distribution** (80/20 rule) describes natural access: 20% of records account for ~80% of accesses. Self-organizing lists exploit this by moving recently-accessed records toward the front [^src_shaffer_java]:

- **Move-to-front**: accessed record is moved to the head of the list. Excellent for highly skewed distributions; poor for random access.
- **Transposition**: accessed record swaps with the record immediately before it. Converges more slowly but avoids "promoting" a record that was accessed just once.

Both heuristics are applicable when the distribution is not known in advance and cannot be used to build a perfect hash or sorted index.

## 2-3 trees

A **2-3 tree** is a balanced search tree that always maintains exact balance by allowing internal nodes to hold either 1 or 2 keys (2-nodes or 3-nodes) [^src_shaffer_java]:

- **Search**: similar to BST — compare against node's key(s) to select correct child (left/middle/right).
- **Insert**: add to leaf; if the leaf becomes a 3-key node, split it and push the middle key up to the parent; repeat up the tree if necessary. Inserting never creates an unbalanced tree — height increases by promoting to a new root.
- **Guarantee**: all leaf nodes are at the same depth; height is always O(log n).

2-3 trees are a conceptual predecessor to B-trees (generalized to nodes with k keys and k+1 children for disk-based storage).

## 2-3 trees vs B+-trees

| Property | 2-3 tree | B+-tree |
|---|---|---|
| Node capacity | 1–2 keys | k–2k keys (disk-block-sized) |
| Leaf linkage | None | Leaves linked for range scans |
| Primary use | In-memory balanced search | Disk-based database indexing |

## Closed hashing methods

Three collision resolution strategies for closed (open-addressing) hash tables [^src_shaffer_java]:

- **Linear probing**: probe `h(k)+i` (mod m) for i=1,2,… Primary clustering — consecutive filled slots grow, increasing collision probability.
- **Quadratic probing**: probe `h(k)+i²` (mod m). Reduces primary clustering but may not visit all slots if m is not prime.
- **Double hashing**: probe `h(k) + i·h₂(k)` (mod m) with a second hash function. Best distribution; eliminates clustering patterns.

All three degrade above ~70% load factor. **Tombstone markers** are required for deletion: simply erasing a record breaks probe chains. A tombstone occupies the slot and allows insertion but not search termination.

**Perfect hashing**: a hash function tailored to a specific static set of records, guaranteeing zero collisions. Viable only when the full dataset is known before the hash function is selected (e.g., read-only CD-ROM databases) [^src_shaffer_java].

## Deque (double-ended queue)

A **deque** supports efficient insert and remove at both front and back. Key use case: **work-stealing** job scheduling (A-Steal algorithm) — each processor maintains a deque of threads; the processor takes from the front; when its deque is empty, it steals from the *back* of another processor's deque. The front/back asymmetry prevents conflicts between the owner (front) and thieves (back) [^src_wikipedia].

## Implicit data structures

An **implicit data structure** encodes relationships among elements via address formulas rather than explicit pointers. The array is the canonical example: element positions are determined by index arithmetic (row-major layout for 2D: address = base + row*cols + col). The heap is the exemplary implicit structure — parent of node i is at i/2, children are 2i and 2i+1. Without the accessing code, the array reveals no structure; with it, full heap ordering is maintained [^src_nievergelt].

Implicit structures save memory (no pointer fields) and improve cache locality. They require static or predictable shape — use explicit pointer structures (linked lists, trees) when shape is dynamic or irregular.

## Functional and persistent data structures

When old versions of a data structure must remain accessible after updates (persistence), imperative structures are insufficient — mutation destroys old versions. Functional data structures avoid mutation entirely; every update returns a new version sharing structure with the old one. Lazy evaluation with memoization enables amortized O(1)–O(log n) bounds to hold even with persistence (see [Functional and Persistent Data Structures](/software-engineering/functional-persistent-data-structures.md)) [^src_okasaki].

## See also

- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — recursion, binary search, and DP/memoization that operate over these structures
- [Functional and Persistent Data Structures](/software-engineering/functional-persistent-data-structures.md) — immutable, persistence-safe versions
- [Software Design Principles](/software-engineering/software-design-principles.md) — code-level design choices that interact with structure selection
- [Software Architecture hub](/software-engineering/README.md)
- [Data Structures and Algorithm Analysis in C++ (Shaffer)](/software-engineering/sources/algorithms-shaffer-c.md) — full textbook source; ADT philosophy, hashing, B-trees, union-find
- [Data Structures and Algorithm Analysis in Java (Shaffer)](/software-engineering/sources/algorithms-shaffer-java.md) — Java edition; also covers 2-3 trees, graphs, lower bounds
- [Purely Functional Data Structures (Okasaki)](/software-engineering/sources/purely-functional-data-structures-okasaki.md) — functional/persistent data structure source
- [Algorithms and Data Structures (Nievergelt)](/software-engineering/sources/algorithms-nievergelt.md) — open-access textbook; implicit data structures
- [Data Structures — Wikipedia Compilation](/software-engineering/sources/data-structures-wikipedia.md) — broad reference survey

---

[^src1]: [Data Structures and Big O Notation Explained](/03_Resources/Study Notes/Data Structures and Big O Notation Explained.md)
[^src2]: [Data Structures and Algorithm Analysis in C++ (Shaffer) — Part 1](../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-c-part-01.md)
[^src_shaffer_java]: [Data Structures and Algorithm Analysis in Java (Shaffer) — Parts 17-30](../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-java-part-17.md)
[^src_okasaki]: [Purely Functional Data Structures, Okasaki — Part 1](../../raw/pdf/pdf-purely-functional-data-structures-part-01.md)
[^src_wikipedia]: [Data Structures (Wikipedia) — Part 3](../../raw/pdf/pdf-data-structures-part-03.md)
[^src_nievergelt]: [Algorithms and Data Structures (Nievergelt) — Part 10](../../raw/pdf/pdf-algorithms-and-data-structures-part-10.md)
