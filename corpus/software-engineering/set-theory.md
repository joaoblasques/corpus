---
type: concept
domain: software-engineering
status: draft
title: Set Theory
aliases:
  - sets
  - set operations
  - Georg Cantor set theory
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-01.md
    channel: pdf
tags:
  - corpus/software-engineering
  - cs-fundamentals
  - mathematics
created: 2026-08-04
updated: 2026-08-04
confidence: 0.9
last_confirmed: 2026-08-04
---

# Set Theory

TL;DR: A set is a collection of distinct, unordered objects (elements). Set theory is the foundation of nearly all modern mathematics, invented by Georg Cantor in the 1870s. In CS it underpins data structure reasoning, type theory, and database theory.

## Core concepts

**Set**: a selection of objects from a group — each element is either *in* or *not in* the set, no shades of gray.[^1]

**Notation**: `A = { Dad, Lizzy }`. Elements listed in curly braces; order irrelevant.[^1]

**Empty set** (∅): `E = {}` or `E = ∅`. Zero members.[^1]

**Domain of discourse** (Ω or U): the set of everything under consideration.[^1]

## Defining sets

- **Extensionally**: list all members — `P = { Dad, Mom }`.
- **Intensionally**: define by a rule — "the set of all parents." Two sets with different intensions may have the same extension and are therefore equal.[^1]
- **Set-builder notation**: `M = { k : k is between 1 and 20, and a multiple of 3 }` — read "k such that."[^1]

## Cardinality

The number of elements in a set. Written `|A|`. Cardinality of ∅ is 0; of infinite sets is ∞. Importantly, |Q| = |N| < |R| — Cantor showed there are different *sizes* of infinity.[^1]

## Sets vs. arrays

| Property | Set | Array |
|---|---|---|
| Order | No order | Ordered |
| Duplicates | None | Allowed |
| Size | Can be infinite | Finite |
| Typing | Heterogeneous | Usually typed |

## Operations

| Operation | Symbol | Result |
|---|---|---|
| Union | A ∪ B | elements in A *or* B |
| Intersection | A ∩ B | elements in A *and* B |
| Partial complement | A − B | elements in A *not in* B |
| Total complement | Ā | elements in Ω *not in* A |
| Cartesian product | A × B | all ordered pairs (a, b) |

`|A × B| = |A| × |B|` (cardinality of product equals product of cardinalities).[^1]

## Laws

- **Commutative**: A ∪ B = B ∪ A; A ∩ B = B ∩ A
- **Associative**: (A ∪ B) ∪ C = A ∪ (B ∪ C)
- **Distributive**: X ∩ (Y ∪ Z) = (X ∩ Y) ∪ (X ∩ Z); also X ∪ (Y ∩ Z) = (X ∪ Y) ∩ (X ∪ Z)
- **Identity**: X ∪ ∅ = X; X ∩ Ω = X
- **Domination**: X ∪ Ω = Ω; X ∩ ∅ = ∅
- **Complement**: X ∪ X̄ = Ω; X ∩ X̄ = ∅
- **De Morgan's**: Ā ∪ B̄ = A̅∩̅B̅; Ā ∩ B̄ = A̅∪̅B̅ (complement of union = intersection of complements)[^1]

## Subsets

`X ⊆ Y` means every member of X is also in Y. ⊆ is like ≤ for sets; ⊂ (proper subset) is like <.

Distinguish: `a ∈ X` (element membership) vs. `A ⊆ X` (set containment). Every set is a subset of itself; ∅ is a subset of every set.[^1]

## Special sets

- Z — integers
- N — natural numbers (0, 1, 2, ...)
- Q — rational numbers
- R — real numbers

## Georg Cantor

Set theory was singlehandedly invented by **Georg Cantor** in the 1870s. After invention, nearly all mathematics was redefined in terms of sets. Cantor discovered that |N| < |R| (there are more reals than naturals), but that |Q| = |N| (rationals are countable). He went insane pursuing the full theory of infinity.[^1]

See also: [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Relations and Functions](/software-engineering/relations-and-functions.md), [Combinatorics](/software-engineering/combinatorics.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-01.md — Davies, Ch. 2 "Sets."
