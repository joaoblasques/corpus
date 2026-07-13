---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-02.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-03.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-04.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-05.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-06.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-07.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-08.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-09.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-10.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-11.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-data-structures-part-12.md
    channel: pdf
    ingested_at: 2026-07-13
aliases:
  - Wikipedia data structures
  - data structures reference PDF
  - data structures Wikipedia compilation
tags:
  - corpus/software-engineering
  - source
created: 2026-07-13
updated: 2026-07-13
---

# Data Structures — Wikipedia Reference Compilation (2010)

**TL;DR**: A comprehensive Wikipedia-sourced PDF compilation of data structure articles (503 pages, generated May 2010 via mwlib). Covers data structure theory from introduction through advanced trees, graphs, heaps, and specialized structures. A broad reference survey; note 2010 vintage means some content predates modern developments (e.g., concurrent data structures coverage is pre-Java-8).

## Coverage

Table of contents spans: introduction (data structure types: linked, succinct, implicit, compressed, search, static/dynamic, persistent, concurrent), abstract data types (list, stack, queue, deque, priority queue, map, multimap, set, tree), arrays (including row-major order), heaps, trees, hash-based structures, graphs, and more.

## Notable content

**Deque and work-stealing**: The A-Steal job scheduling algorithm uses a deque per processor. A worker gets its next thread from the *front* of its own deque. If the current thread forks, it is put at the *front* and the new thread executes. When a processor's deque empties, it *steals* from the *back* of another processor's deque. This front/back asymmetry is why a deque is required rather than a simple stack or queue [^src1].

**Bit fields and type safety**: Combining bit-flag enum values with bitwise OR produces values outside the enumeration — this violates type safety. The underlying issue is that bit flag combinations are elements of an elementary abelian group (Z/2Z)^n, which defines only a partial order (1011 and 1101 are incomparable), not the total order integer comparison assumes. Safe implementation: use a bit array where indices are values of an enumerated type (e.g., Java's EnumSet) [^src2].

**Thread safety with bit fields**: Flag and counter stored in the same word cannot be atomically loaded/stored on most machines — a single mutex must protect both, not two separate mutexes [^src2].

**Concurrent data structures** (pre-Java-8): thread-safety patterns for basic structures; lock-based vs lock-free approaches. Coverage reflects the state of practice circa 2010.

## Relation to corpus pages

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — broad corroboration; deque, bit arrays, and concurrent structures add detail to existing coverage
- [Data Structures and Algorithm Analysis in Java (Shaffer)](/software-engineering/sources/algorithms-shaffer-java.md) — the Shaffer textbook is the primary structured reference; this Wikipedia compilation is a secondary broad survey

---

[^src1]: [Data Structures (Wikipedia) — Part 3 (Deque, A-Steal work-stealing algorithm)](../../../raw/pdf/pdf-data-structures-part-03.md)
[^src2]: [Data Structures (Wikipedia) — Part 5 (Bit fields, type safety, thread safety)](../../../raw/pdf/pdf-data-structures-part-05.md)
