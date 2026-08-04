---
type: concept
domain: software-engineering
status: draft
title: Propositional Logic
aliases:
  - boolean logic
  - logical operators
  - truth tables
  - propositional calculus
  - logical connectives
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-08.md
    channel: pdf
tags:
  - corpus/software-engineering
  - cs-fundamentals
  - mathematics
  - logic
created: 2026-08-04
updated: 2026-08-04
confidence: 0.9
last_confirmed: 2026-08-04
---

# Propositional Logic

TL;DR: The formal system for reasoning about true/false statements using logical operators. Propositions are the atomic building blocks; operators combine them into compound statements. Foundation of circuit design, program verification, and type theory.

## Propositions

A **proposition** is a statement to which a truth value (true/false) can be meaningfully assigned. Not all sentences are propositions — "This sentence is false" has no valid truth value (liar paradox).[^1]

## Logical operators

| Symbol | Name | Meaning |
|---|---|---|
| ∧ | AND (conjunction) | X∧Y is true iff both X and Y are true |
| ∨ | OR (disjunction) | X∨Y is true iff at least one is true |
| ⊕ | XOR (exclusive or) | X⊕Y is true iff exactly one is true (not both) |
| ¬ | NOT (negation) | ¬X flips the truth value; unary operator |
| ⇒ | IMPLIES | X⇒Y: "if X then Y"; false only when X=T and Y=F |

## The implication ⇒ explained

"X⇒Y" claims: *if* X is true, *then* Y must be true. It makes **no claim** when X is false — so the implication is vacuously true whenever X is false.[^1]

"X⇒Y is true whenever either X is false or Y is true or both."[^1]

Truth table for ⇒:
| X | Y | X⇒Y |
|---|---|---|
| T | T | T |
| T | F | **F** |
| F | T | T |
| F | F | T |

Key insight: to a logic system, propositions are atomic symbols with no inherent meaning. "The King of England is female ⇒ UMW is in Virginia" is a *true* proposition (vacuously, since the premise is false).[^1]

## Logical equivalences

Two propositions are **logically equivalent** if they have the same truth value for all assignments.

Key equivalences:
- **De Morgan's**: ¬(X∧Y) ≡ ¬X∨¬Y; ¬(X∨Y) ≡ ¬X∧¬Y
- **Double negation**: ¬¬X ≡ X
- **Contrapositive**: (X⇒Y) ≡ (¬Y⇒¬X)
- **Implication expansion**: (X⇒Y) ≡ (¬X∨Y)

## CS relevance

- **Boolean algebra** in circuit design (AND/OR/NOT gates)
- **Conditional logic** in programs (`if`, `while`, `assert`)
- **Type checking** (logical constraints over types)
- **SQL WHERE clauses** (compound predicates)
- **SAT solvers** (propositional satisfiability — NP-complete)

See also: [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Mathematical Proof](/software-engineering/mathematical-proof.md), [Complexity Theory and NP-Completeness](/software-engineering/complexity-theory.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-08.md — Davies, Ch. 8 "Logic."
