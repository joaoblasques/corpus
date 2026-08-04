---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-a-computational-logic-1979-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-04.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-05.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-06.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-07.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-08.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-09.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-10.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-11.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/pdf/pdf-a-computational-logic-1979-part-12.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - A Computational Logic
  - Boyer Moore 1979
  - ACM monograph Boyer Moore
tags:
  - corpus/software-engineering
  - source
created: 2026-08-03
updated: 2026-08-03
---

# A Computational Logic (Boyer & Moore, 1979)

**TL;DR** — Foundational ACM monograph presenting a formal theory for mechanically proving theorems about recursive programs. Introduces the Boyer-Moore theorem prover: a heuristic-driven system that proves theorems (including compiler correctness, string search correctness, and the Unique Prime Factorization Theorem) from axioms using induction guided by recursive function definitions. 440 pages, 12 PDF parts.

Authors: [Robert S. Boyer](/software-engineering/robert-s-boyer.md) and [J Strother Moore](/software-engineering/j-strother-moore.md), SRI International, Menlo Park. Published Academic Press, 1979 (ACM Monograph Series).

## Scope and motivation

The book addresses a gap in 1970s program verification: "Mechanical theorem-proving is crucial to the automation of reasoning about computer programs. Today, few computer programs can be mechanically certified to be free of 'bugs.' The principal reason is the lack of mechanical theorem-proving power." [^p01] Existing approaches either required user-directed proof-checking (too tedious) or freely introduced unproved "lemmas" as axioms — which the authors argue "so completely undermines the spirit of proof." [^p01]

The core claim: induction over inductively constructed objects (integers, sequences, trees) is the missing ingredient. Resolution theorem provers of the era (Chang, Lee, Loveland) did not handle axiom schemes like mathematical induction; Boyer and Moore built a system that does.

## The formal theory

The theory is typed around **shells** — colored n-tuples that model inductively constructed objects. Three built-in shells: natural numbers (via `ADD1`/`ZERO`/`SUB1`), literal atoms (`PACK`/`UNPACK`/`NIL`), and ordered pairs (`CONS`/`CAR`/`CDR`/`LISTP`). [^p01]

Key design choices:
- Prefix LISP-like notation: `(PLUS (H X) B)`.
- `IF` and `EQUAL` are the foundation of all conditionals and propositions at the term level.
- Logical connectives (`NOT`, `AND`, `OR`, `IMPLIES`) are defined as ordinary functions.
- No quantifiers — "recursive functions offer such a powerful form of expression when dealing with discrete mathematics that we do not use any additional form of quantification." [^p01]

**The Shell Principle:** Mechanism for adding new inductively constructed types consistently. Each shell declaration adds: a constructor, a recognizer, accessors, type restrictions, default values, and a well-founded relation. Consistency is guaranteed by exhibiting a set-theoretic model. [^p02]

**The Definition Principle:** Permits introduction of recursive functions only when a well-founded measure decreasing in each recursive call can be exhibited. This prevents inconsistency (e.g., the RUSSELL paradox definition is rejected). [^p02]

**The Induction Principle (Noetherian Induction):** To prove p, it suffices to prove: (1) base case when no induction condition holds, and (2) induction steps where instantiated copies of p at smaller measures are available as hypotheses. Soundness proved by well-founded minimality: assuming p fails yields a minimal counterexample, contradicting the induction steps. [^p02]

## Proof heuristics (Chapters 5–15)

The system applies heuristics in waterfall order. Each conjecture is first represented as a set of clauses, then the following heuristics are tried in sequence:

| Heuristic | Effect |
|---|---|
| Type information (Ch. 6) | Simplify by substituting type facts about terms |
| Rewrite rules (Ch. 7) | Apply previously proved lemmas as directed equalities |
| Definition expansion (Ch. 8) | Unfold non-recursive or carefully chosen recursive definitions |
| Destructor elimination (Ch. 10) | Replace `(CAR X)` / `(CDR X)` pairs with fresh variables via `CAR/CDR.ELIM` |
| Cross-fertilization (Ch. 11) | Use an equality hypothesis to substitute in the conclusion, then discard it for a more general conjecture |
| Generalization (Ch. 12) | Replace common subterms with variables to obtain a more induction-friendly conjecture |
| Irrelevance elimination (Ch. 13) | Delete hypotheses disconnected from the conclusion and likely falsifiable |
| Induction (Ch. 14–15) | Select induction scheme from recursive structure of terms; merge multiple candidate schemes |

The induction selection heuristic (Ch. 14–15) is the most important: the system analyzes recursive functions appearing in the conjecture to extract candidate induction schemes, then uses a flawed/unflawed analysis and merging procedure to choose a single scheme. A scheme is "flawed" if some variable that should be decreasing appears in a context where it is not being recursively decomposed. [^p01][^p02]

**Rewrite rules**: Previously proved theorems marked `(rewrite)` are used as left-to-right simplification rules. The system must avoid infinite loops from non-terminating rule sequences. Loops involving backchaining hypotheses are controlled by a check that hypothesis variables are "covered" by variables in the conclusion. [^p01]

**Generalization**: Replace common subterms (not variables, explicit values, destructors, or EQUAL-applications) with fresh variables. If the term's type set is a singleton, add the type as a hypothesis. Use known generalization lemmas to add relational constraints between the new variable and the original term. [^p07]

## Four major case studies

### 1. Tautology checker (Ch. 4)

A function `TAUTOLOGY.CHECKER` is defined in the theory that decides propositional tautologies. The machine proves three properties mechanically:
- `NORMALIZE` produces IF-normal form expressions.
- `NORMALIZE` preserves truth value.
- `TAUTOLOGYP` on IF-normal-form expressions is sound (non-F iff tautology under all assignments).

The proof illustrates the subsidiary-lemma / decomposition pattern: `ASSIGNMENT.APPEND`, `VALUE.CAN.IGNORE.REDUNDANT.ASSIGNMENTS`, and `VALUE.SHORT.CUT` are proved first, then combined. [^p04]

### 2. Optimizing expression compiler (Ch. 17)

A function `CODEGEN` compiles arithmetic expressions to stack-machine instruction sequences. The machine proves `CODEGEN.IS.CORRECT`: executing the compiled code starting from any stack leaves the evaluated expression on top. Proof uses induction on expression structure; key step involves cross-fertilizing the induction hypothesis for sub-expressions with the stack execution results. [^p10]

### 3. Boyer-Moore string search (Ch. 18)

Formal verification of the fast string searching algorithm (average-case optimal). The specification uses Floyd's inductive assertion style (verification conditions from loop invariants). The machine proves the verification conditions — including the algorithm's key invariant relating text and pattern positions. [^p01]

### 4. Unique Prime Factorization Theorem (Ch. 19)

Derived from Peano arithmetic axioms through ~345 definitions and theorems (Appendix A). Proves: (a) every positive integer equals the product of some finite list of primes; (b) any two such lists with equal products are permutations of each other. This demonstrates the system can handle "theorems that are generally considered difficult." [^p12]

## Appendix A: The full theorem sequence

Appendix A lists all ~345+ definitions and theorems the prover is expected to re-establish whenever a new technique is incorporated. Includes theorems about APPEND, REVERSE, FLATTEN, MC.FLATTEN, arithmetic operations (PLUS, TIMES, REMAINDER, QUOTIENT), GCD, prime factorization, sorting (DSORT, SORT2, ADDTOLIST2, ORDERED2), and the string search verification conditions. This sequence is the system's regression suite. [^p12]

## Historical significance

The Boyer-Moore prover (later NQTHM, then ACL2) is the direct ancestor of ACL2 — the industrial-strength theorem prover used to verify the AMD floating-point unit (AMD K5 bug fix), Intel microprocessors, and Java bytecode verifier. The induction-from-recursion insight and the rewrite-rule waterfall architecture remain the core of ACL2 as of 2026.

See [Formal Verification and Mechanical Theorem Proving](/software-engineering/formal-verification.md) for the broader concept context, and entity pages for [Robert S. Boyer](/software-engineering/robert-s-boyer.md) and [J Strother Moore](/software-engineering/j-strother-moore.md).

[^p01]: [A Computational Logic — Part 1/12 (Preface, Ch. 1–3)](../../../raw/pdf/pdf-a-computational-logic-1979-part-01.md)
[^p02]: [A Computational Logic — Part 2/12 (Ch. 2–3 continued)](../../../raw/pdf/pdf-a-computational-logic-1979-part-02.md)
[^p04]: [A Computational Logic — Part 4/12 (Ch. 4: Tautology checker proofs)](../../../raw/pdf/pdf-a-computational-logic-1979-part-04.md)
[^p07]: [A Computational Logic — Part 7/12 (Ch. 12: Generalization)](../../../raw/pdf/pdf-a-computational-logic-1979-part-07.md)
[^p10]: [A Computational Logic — Part 10/12 (Ch. 17: Compiler correctness proof)](../../../raw/pdf/pdf-a-computational-logic-1979-part-10.md)
[^p12]: [A Computational Logic — Part 12/12 (Appendix A: Full theorem sequence)](../../../raw/pdf/pdf-a-computational-logic-1979-part-12.md)
