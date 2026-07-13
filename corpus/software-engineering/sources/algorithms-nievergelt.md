---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-01.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-02.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-03.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-04.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-05.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-06.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-07.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-08.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-09.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-10.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-11.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-12.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-13.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-14.md
    channel: pdf
    ingested_at: 2026-07-13
  - path: raw/_inbox/pdf-algorithms-and-data-structures-part-15.md
    channel: pdf
    ingested_at: 2026-07-13
aliases:
  - Nievergelt algorithms
  - Algorithms and Data Structures Global Text
  - Nievergelt DSA
  - Algorithms and Data Structures Nievergelt Hinrichs
tags:
  - corpus/software-engineering
  - source
created: 2026-07-13
updated: 2026-07-13
---

# Algorithms and Data Structures (Nievergelt & Hinrichs, Global Text Project)

**TL;DR**: An open-access (Creative Commons Attribution 3.0) algorithms and data structures textbook by Jürg Nievergelt and Klaus Hinrichs (371 pages). Covers foundational CS from algorithm analysis through data structures, with emphasis on *representation*, *implicit data structures*, and *algorithm animation/visualization*. Note: Part 1 has corrupted PDF character encoding; parts 2-15 are readable.

## Scope

Topics covered: algorithm analysis and recurrence relations, programming language syntax (grammars, EBNF, BNF, syntax diagrams), abstract data types vs concrete representations, sorting and searching, list structures, trees, graphs, and implicit data structures (arrays and heaps). Available free at textbookequity.org.

## Distinctive emphasis

Unlike Shaffer (pedagogy-focused) or Okasaki (theoretical), Nievergelt emphasizes *algorithm animation* — exercises ask students to implement animated visualizations of algorithms, exposing the step-by-step behavior. This makes it more interactively-oriented.

## Key content

**Recurrence relations and floating-point precision**: recurrence `z_k = sum(c_i * z_{k-i})` for i=1..d generates curves (circles, fractals) when plotted in the complex plane. A single bit of precision difference in floating-point can change the resulting image entirely — illustrating how computational behavior is sensitive to implementation precision [^src1].

**Syntax and grammars (Ch 6)**: Programming language syntax formally defined by context-free grammars. Backus-Naur Form (BNF), introduced 1960 for Algol, and Extended BNF (EBNF) are standard notations. Syntax diagrams are the graphical equivalent. Key components: terminal symbols (alphabet), nonterminal symbols (syntactic entities), and production rules. Recursion is central to all these notations — large programs are parsed by reducing to smaller components [^src2].

**Implicit data structures (Ch 20)**: When data structure is *static* and *regular*, relationships among elements can be expressed by formulas rather than explicit pointers. This saves memory and often gives faster programs. The array is the canonical implicit structure: its layout (row-major or column-major for 2D arrays) encodes the element relationships in the program's addressing logic, not in stored pointers [^src3].

> "Separated from its code, an implicit data structure represents at best an unordered set of data. With the right code, it exhibits a rich structure, as is beautifully illustrated by the heap." [^src3]

The heap data structure is presented as the exemplary implicit structure: stored as a plain array, but its heap-order and shape properties are maintained by index arithmetic (parent = i/2, children = 2i and 2i+1) rather than pointer fields.

**Data structure design principle**: Data is usually modeled as a graph; relationships serve two purposes — semantic interpretation and access paths. When structure is irregular or highly dynamic, explicit links (list structures) are necessary. When structure is static and regular, implicit representation (formulas) is preferred [^src3].

**Array storage**: Two-dimensional array stored row-by-row in C (row-major) or column-by-column in Fortran (column-major); element address = base + linear formula of indices [^src3].

## Relation to corpus pages

- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — array and heap content corroborated; implicit data structure concept is additive
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — algorithm analysis and recurrence relations corroborated
- [Data Structures and Algorithm Analysis in Java (Shaffer)](/software-engineering/sources/algorithms-shaffer-java.md) — companion reference; Shaffer more comprehensive on specific data structure implementations

---

[^src1]: [Algorithms and Data Structures (Nievergelt) — Part 2 (recurrence relations, floating-point precision)](../../../raw/pdf/pdf-algorithms-and-data-structures-part-02.md)
[^src2]: [Algorithms and Data Structures (Nievergelt) — Part 3 (Ch 6: Syntax, EBNF, grammars)](../../../raw/pdf/pdf-algorithms-and-data-structures-part-03.md)
[^src3]: [Algorithms and Data Structures (Nievergelt) — Part 10 (Ch 20: Implicit data structures, array storage)](../../../raw/pdf/pdf-algorithms-and-data-structures-part-10.md)
