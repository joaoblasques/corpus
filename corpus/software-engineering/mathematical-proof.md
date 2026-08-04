---
type: concept
domain: software-engineering
status: draft
title: Mathematical Proof
aliases:
  - proof techniques
  - proof by contradiction
  - mathematical induction
  - direct proof
  - proof strategies
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-09.md
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

# Mathematical Proof

TL;DR: A proof is a finite sequence of logical deductions from accepted axioms/hypotheses that establishes the truth of a proposition. Three core strategies for CS: direct proof, proof by contradiction, and mathematical induction.

## What is a proof

A proof starts from what is known or assumed true, applies agreed-upon logical steps, and arrives at the proposition to be established. Key property: **verifiability** — any reader from the intended audience should be able to follow every step.[^1]

Proof results are referred to by role:
- **Theorem**: key, important result
- **Lemma**: result used as a stepping stone in a larger proof
- **Corollary**: immediate consequence of a theorem[^1]

## Core proof strategies

### Direct proof

Assume the hypotheses, manipulate directly to reach the conclusion. Chain of logical steps from known → unknown.

### Proof by contradiction (reductio ad absurdum)

Assume the negation of what you want to prove. Derive a contradiction. Conclude the original proposition must be true.

**Classic example** — √2 is irrational:[^1]
1. Assume √2 = a/b in lowest terms (gcd(a,b)=1).
2. Then 2 = a²/b², so a² = 2b², meaning a² is even.
3. If a² is even, a is even → write a = 2k.
4. Then 4k² = 2b², so b² = 2k², meaning b is even.
5. Both a and b even contradicts gcd(a,b)=1. ∎

"Proving this directly seems pretty hard, since how do you prove that there *aren't* any two integers whose ratio is √2, no matter how hard you looked?"[^1]

### Mathematical induction

To prove a proposition P(n) for all natural numbers n ≥ n₀:
1. **Base case**: prove P(n₀).
2. **Inductive step**: assume P(k) (inductive hypothesis); prove P(k+1).
3. Conclude P(n) holds for all n ≥ n₀.

**Strong induction**: assume P(j) for all j ≤ k to prove P(k+1).

## CS relevance

- **Algorithm correctness**: loop invariants are inductive proofs
- **Complexity lower bounds**: adversarial arguments often use contradiction
- **Formal verification** and type safety proofs
- **Impossibility results**: many distributed systems impossibility proofs (FLP, CAP) use contradiction
- **Computability theory**: diagonalization (Cantor, Halting problem) is proof by contradiction

See also: [Propositional Logic](/software-engineering/propositional-logic.md), [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Formal Verification and Mechanical Theorem Proving](/software-engineering/formal-verification.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-09.md — Davies, Ch. 9 "Proof."
