---
type: concept
domain: software-engineering
status: draft
title: Discrete Probability
aliases:
  - probability theory discrete
  - conditional probability
  - independence statistics
  - Bayes theorem
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-04.md
    channel: pdf
tags:
  - corpus/software-engineering
  - cs-fundamentals
  - mathematics
  - probability
created: 2026-08-04
updated: 2026-08-04
confidence: 0.9
last_confirmed: 2026-08-04
---

# Discrete Probability

TL;DR: Probability over finite or countable sample spaces — the foundation for reasoning about uncertainty in algorithms, machine learning, and distributed systems. Key concepts: sample space, events, conditional probability, independence, Bayes' theorem.

## Core concepts

**Sample space** (Ω): the set of all possible outcomes of an experiment.

**Event**: a subset of the sample space.

**Probability** Pr(E): a number in [0,1] assigned to each event. For uniform distributions: Pr(E) = |E| / |Ω|.

## Conditional probability

Pr(A|B) — "probability of A given B occurred." Restricts attention to outcomes where B holds:

Pr(A|B) = Pr(A ∩ B) / Pr(B)

## Independence

Events A and B are **independent** if knowing one occurred tells you nothing about the other:

Pr(A|B) = Pr(A)

Equivalently: Pr(A ∩ B) = Pr(A) · Pr(B).

Caution: independence is an aggressive claim requiring strong evidence from data. Default assumption should be *dependence*, not independence.[^1]

## Common mistakes

- **Confusing independence with mutual exclusivity**: mutually exclusive events (A ∩ B = ∅) are *almost never* independent (if B occurs, A definitely doesn't — they're maximally correlated).
- **Sample vs. population**: experimental data will show approximate independence even for truly independent events due to random fluctuation. Statisticians use hypothesis tests to determine "close enough."[^1]

## Bayes' theorem

Pr(A|B) = Pr(B|A) · Pr(A) / Pr(B)

Allows reversing conditional: given Pr(B|A) (likelihood), compute Pr(A|B) (posterior). Foundation of Bayesian inference.

## CS relevance

- Spam filtering, anomaly detection (Naive Bayes)
- A/B test significance (p-values use conditional probability)
- Hash collision probability (birthday paradox)
- Load balancing and queuing theory

See also: [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Combinatorics](/software-engineering/combinatorics.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-04.md — Davies, Ch. 4 "Probability."
