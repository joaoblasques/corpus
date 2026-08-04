---
type: concept
domain: software-engineering
status: draft
title: Discrete Mathematics
aliases:
  - discrete math
  - discrete maths
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

# Discrete Mathematics

TL;DR: The branch of mathematics dealing with objects that take distinct, separated values — as opposed to continuous mathematics (calculus, real analysis). Fundamental to computer science because computers operate algorithmically, in discrete steps, on discrete data.

## Discrete vs. Continuous

| Discrete | Continuous |
|---|---|
| Integers (Z) | Real numbers (R) |
| `int` | `double` |
| Digital | Analog |
| Quantum | Continuum |
| Counting | Measuring |
| Number theory | Analysis |
| Σ (summation) | ∫ (integration) |
| Subtraction | Differentiation |

"Σ is just the discrete 'version' of ∫." Discrete things jump suddenly from position to position with rigid precision.[^1]

## Why CS uses discrete math

1. **Computers are discrete**: everything stored is ultimately bits, each 0 or 1.
2. **Algorithms are discrete**: step-by-step execution — the computer *has* completed step 7 but *not* step 8; it has accumulated exactly 38 values, not 39.
3. Reasoning about programs requires counting, logic, sets, and graphs — all discrete structures.[^1]

## Core topics

- **[Set Theory](/software-engineering/set-theory.md)** — sets, cardinality, operations, power sets
- **[Relations and Functions](/software-engineering/relations-and-functions.md)** — endorelations, injection/surjection/bijection
- **[Discrete Probability](/software-engineering/discrete-probability.md)** — sample spaces, conditional probability, independence
- **[Graph Theory](/software-engineering/graph-theory.md)** — graphs, trees, spanning trees, MST
- **[Combinatorics](/software-engineering/combinatorics.md)** — counting principles, permutations, combinations
- **[Number Systems](/software-engineering/number-systems.md)** — binary, octal, hexadecimal
- **[Propositional Logic](/software-engineering/propositional-logic.md)** — operators, truth tables, equivalences
- **[Mathematical Proof](/software-engineering/mathematical-proof.md)** — direct, contradiction, induction

## Primary source

- [A Cool Brisk Walk Through Discrete Mathematics](/software-engineering/sources/a-cool-brisk-walk-through-discrete-mathematics.md) — [Stephen Davies](/software-engineering/stephen-davies.md), UMW, v2.2.2 (CC BY-SA 4.0, 254pp)

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-01.md — Davies, Ch. 1 "Meetup at the trailhead."
