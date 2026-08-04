---
type: concept
domain: software-engineering
status: draft
title: Combinatorics
aliases:
  - counting
  - permutations
  - combinations
  - multiplication principle
  - combinatorial analysis
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-06.md
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

# Combinatorics

TL;DR: The mathematics of counting discrete structures — how many ways can something be arranged, selected, or configured? Combinatorics underpins algorithm analysis, cryptographic security proofs, and probability calculations.

## Core counting principles

### Multiplication principle (rule of product)

If a choice has k parts where part i has nᵢ options, the total number of choices is n₁ × n₂ × ... × nₖ.[^1]

Example (license plates): 3 characters (36 options each) + 4 digits (10 options each) = 36³ × 10⁴ = 466,560,000.

### Addition principle (rule of sum)

If an event can happen in n₁ OR n₂ mutually exclusive ways, total = n₁ + n₂.

### Complement trick

"Count the hard thing" = "total - count its complement." Useful when the complement is easy to count.[^1]

Example: "passwords with at least one digit" = "all passwords" − "passwords with no digits."

## Exponential growth

Modifying an exponent dominates all lower-order terms. A 7-character alphanumeric plate count ≈ 7 + 6 + 5 + 4 + 3 + 2 + 1 character plates combined, approximately.[^1] For approximation: only count the largest term.

## Permutations and combinations

**Permutation** P(n,k): ordered selection of k from n distinct items = n! / (n-k)!

**Combination** C(n,k) or "n choose k": unordered selection of k from n = n! / (k! · (n-k)!)

**Binomial theorem**: (x+y)ⁿ = Σₖ C(n,k) xᵏ yⁿ⁻ᵏ

## CS applications

- Password/key space analysis (security strength)
- Hash collision probability (birthday paradox: ~√|space| probes)
- Algorithm complexity analysis (counting paths, comparisons)
- Random sampling and Monte Carlo methods
- Data compression (counting distinct inputs vs. codewords)

See also: [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Discrete Probability](/software-engineering/discrete-probability.md), [Complexity Theory and NP-Completeness](/software-engineering/complexity-theory.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-06.md — Davies, Ch. 6 "Counting."
