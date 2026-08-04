---
type: concept
domain: software-engineering
status: draft
title: Relations and Functions
aliases:
  - relation
  - function
  - injection
  - surjection
  - bijection
  - endorelation
  - injective
  - surjective
  - bijective
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-03.md
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

# Relations and Functions

TL;DR: A **relation** is a subset of a Cartesian product; a **function** is a relation where each domain element maps to exactly one codomain element. Function properties (injection/surjection/bijection) govern whether functions are invertible.

## Relations

A **relation** R between sets A and B is any subset of A × B — a set of ordered pairs (a, b) where a ∈ A and b ∈ B.[^1]

An **endorelation** is a relation on a set with itself (A × A). Examples: "less than" on integers, "is friends with" on people.

The empty set ∅ is a valid relation (vacuously satisfies all constraints).

## Functions

A **function** f: A → B is a relation where every element of A maps to *exactly one* element of B. A is the **domain**, B the **codomain**.

Key constraint: each input has exactly one output. A relation fails to be a function if any domain element has 0 or 2+ mapped outputs.

## Function properties

| Property | Definition | Colloquial |
|---|---|---|
| **Injection** (one-to-one) | ∀ a₁≠a₂ ∈ A: f(a₁) ≠ f(a₂) | No two inputs share an output |
| **Surjection** (onto) | ∀ b ∈ B: ∃ a ∈ A such that f(a)=b | Every codomain element is hit |
| **Bijection** (one-to-one correspondence) | Injective AND surjective | Perfect pairing between domain and codomain |

**Bijection requires equal cardinality**: |A| = |B| is necessary but not sufficient for bijection — equal sizes guarantee it's *possible*, but not that a given function achieves it.[^1]

If |A| = |B|, injectivity and surjectivity are logically linked: violate one and you violate the other; uphold one and you uphold the other.[^1]

## CS relevance

- Hash functions aim for injection (no collisions) but often fail on inputs with large domains
- Database foreign keys enforce functions from child to parent
- Encryption requires bijection (invertible) over the key space
- Type coercions are surjections if information is lost

See also: [Set Theory](/software-engineering/set-theory.md), [Discrete Mathematics](/software-engineering/discrete-mathematics.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-03.md — Davies, Ch. 3 "Relations."
