---
type: concept
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Structures and Big O Notation Explained.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - data structures
  - Big O notation
  - time complexity
  - arrays
  - linked lists
  - hashmaps
  - binary search tree
  - BST
tags:
  - corpus/software-engineering
  - concept
created: 2026-05-21
updated: 2026-06-16
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

## See also

- [[software-engineering/algorithms|Algorithms (Strategies, Not Tricks)]] — recursion, binary search, and DP/memoization that operate over these structures and trade in these complexity classes
- [[software-engineering/software-design-principles|Software Design Principles]] — code-level design choices that interact with structure selection (e.g., encapsulation of data structure internals)
- [[software-engineering/README|Software Architecture hub]]

---

[^src1]: [[03_Resources/Study Notes/Data Structures and Big O Notation Explained|Data Structures and Big O Notation Explained]]
