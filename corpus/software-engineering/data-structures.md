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
tags:
  - corpus/software-engineering
  - concept
created: 2026-05-21
updated: 2026-07-12
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

## See also

- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — recursion, binary search, and DP/memoization that operate over these structures and trade in these complexity classes
- [Software Design Principles](/software-engineering/software-design-principles.md) — code-level design choices that interact with structure selection (e.g., encapsulation of data structure internals)
- [Software Architecture hub](/software-engineering/README.md)
- [Data Structures and Algorithm Analysis in C++ (Shaffer)](/software-engineering/sources/algorithms-shaffer-c.md) — full textbook source; ADT philosophy, hashing, B-trees, union-find
- [Data Structures and Algorithm Analysis in Java (Shaffer)](/software-engineering/sources/algorithms-shaffer-java.md) — Java edition of the same text

---

[^src1]: [Data Structures and Big O Notation Explained](/03_Resources/Study Notes/Data Structures and Big O Notation Explained.md)
[^src2]: [Data Structures and Algorithm Analysis in C++ (Shaffer) — Part 1](../../raw/pdf/pdf-data-structures-and-algorithm-analysis-in-c-part-01.md)
