---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-a-computational-logic-1979-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-a-computational-logic-1979-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-a-computational-logic-1979-part-04.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-a-computational-logic-1979-part-10.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - formal verification
  - mechanical theorem proving
  - program verification
  - Boyer-Moore theorem prover
  - NQTHM
  - ACL2
  - automated theorem proving
  - program correctness
  - formal proof
  - inductive proof
  - Noetherian induction
  - mathematical induction in computing
  - shell principle
  - well-founded relation
  - induction scheme
  - verification condition
  - Floyd inductive assertion
  - McCarthy functional semantics
  - tautology checker verification
  - compiler correctness
  - string search verification
tags:
  - corpus/software-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Formal Verification and Mechanical Theorem Proving

**TL;DR** — Formal verification proves programs correct with mathematical certainty by reducing "does this program have property X?" to "are these formulas theorems?" in a formal logic. Mechanical theorem proving automates this reasoning. The Boyer-Moore theorem prover (1979) established the practical blueprint: induction guided by recursive function structure, heuristic proof search, rewrite-rule libraries. Its descendants (NQTHM, ACL2) remain in production use for hardware and critical software verification.

## The core reduction

Any program-correctness question can be reduced to theorem-proving. Program semantics (Floyd/Hoare/McCarthy) converts "does program P satisfy specification S?" into a set of formulas. Because computer programs manipulate inductively constructed objects — integers, sequences, trees, stacks, queues — "regardless of which program semantics we use to obtain the formulas to be proved, our formal theory and mechanical theorem prover must permit definition and proof by induction." [^bm79_p1]

This is the fundamental insight missing from 1970s proof checkers: they could verify proofs but could not discover inductive arguments. Boyer and Moore showed that **induction schemes can be extracted mechanically from recursive function definitions**.

## Two styles of program specification

Both can be handled within the Boyer-Moore framework:

**McCarthy's functional semantics**: The program itself is written as a recursive function in the logic. Correctness is stated as an equation: `(EQUAL (f args) expected-result)`. Example: `(EQUAL (MC.FLATTEN X ANS) (APPEND (FLATTEN X) ANS))`. [^bm79_p1]

**Floyd's inductive assertion method**: Loop invariants are expressed as first-order assertions at program points ("cut points"). The prover generates "verification conditions" — formulas that imply the invariant holds inductively. Used in the Boyer-Moore string search proof. [^bm79_p1]

## Well-founded induction (Noetherian Induction)

The engine of all mechanical induction. A relation r is **well-founded** if no infinite strictly-decreasing sequence exists under r. LESSP on nonnegative integers is well-founded. The CDR of a CONS is smaller than the CONS (by COUNT under LESSP).

**The Induction Principle**: To prove p(x), it suffices to:
1. Prove p(x) when no induction condition holds (base case).
2. For each induction step: assuming p(d(x)) for each "decremented" instance d(x) where `r(m(d(x)), m(x))` is a theorem, prove p(x).

Soundness: if p fails, take a minimal counterexample under the well-founded measure. Contradicts one of the above cases. [^bm79_p2]

This generalizes structural induction (induct on CDR of list), arithmetic induction (induct on SUB1 of number), and complex two-argument inductions where the measure is a lexicographic combination.

## Induction from recursion: the key heuristic

The practical insight: **the induction scheme for a conjecture should mirror the recursive structure of the functions appearing in it**.

When a conjecture involves `(APPEND A ...)`, APPEND recurses by taking `(CDR A)`. So induct on A, with base case `(NOT (LISTP A))` and induction step providing the hypothesis for `(CDR A)`. When multiple recursive functions are present, their candidate schemes are merged: two schemes merge if one implies the other, or if their induction variables are disjoint. Conflicting schemes require the prover to pick the "most likely" one (unflawed schemes preferred). [^bm79_p1]

**Flaw analysis**: A scheme is "flawed" for a conjecture if the induction variable appears in a context where neither the base case nor the step can make progress (e.g., variable appears as a second argument to a function that only recurses on its first argument). Unflawed schemes are strongly preferred. [^bm79_p2]

## The waterfall proof strategy

Conjectures flow through heuristics in order; any heuristic that makes progress restarts the sequence:

1. **Simplification**: Apply type information, rewrite rules (previously proved theorems used left-to-right), and definition expansion. Reduces to normal form.
2. **Destructor elimination**: Replace `(CAR X)` / `(CDR X)` with fresh variables using `CAR/CDR.ELIM`: if `(LISTP X)` then `(CONS (CAR X) (CDR X)) = X`. This "eliminates bad terms" by introducing variables, enabling further simplification. [^bm79_p2]
3. **Cross-fertilization**: When an equality hypothesis `(EQUAL x y)` exists, substitute x for y (or vice versa) in the conclusion, then discard the hypothesis. This yields a more general conjecture. The FLATTEN/MC.FLATTEN proof uses cross-fertilization twice in sequence. [^bm79_p2]
4. **Generalization**: Replace common subterms with variables to obtain a stronger conjecture that yields to induction. Add type restrictions and generalization-lemma constraints on the new variable. Critical: without generalizing `(FLATTEN Z)` to a fresh variable `Y`, the FLATTEN/MC.FLATTEN proof would fail — induction would produce deeper FLATTEN nests rather than simplifying. [^bm79_p7]
5. **Irrelevance elimination**: Delete hypotheses that are disconnected from the rest of the formula and "probably falsifiable." Prevents bad induction choices caused by irrelevant recursive terms competing for attention. [^bm79_p7]
6. **Induction**: Apply the induction principle with the selected scheme. Produces new subgoals (base case + induction steps), which cycle back through the waterfall.

## The shell principle and type system

New inductively constructed types are added via the **Shell Principle**: declare a constructor, recognizer, accessors, type restrictions on components, default values for type violations, and a well-founded relation. The system automatically adds the required axioms and ensures consistency by exhibiting a set-theoretic model. [^bm79_p1]

Built-in shells:
- **Natural numbers**: `ADD1` (constructor), `ZERO` (bottom), `NUMBERP` (recognizer), `SUB1` (accessor), `SUB1P` (well-founded relation).
- **Literal atoms**: `PACK` (constructor), `NIL` (bottom), `LITATOM` (recognizer), `UNPACK` (accessor).
- **Ordered pairs / lists**: `CONS` (constructor), `LISTP` (recognizer), `CAR`/`CDR` (accessors), `CAR.CDRP` (well-founded relation).

Type sets — the set of shell types a term can return — are computed for each term and used in simplification (type prescriptions) and generalization (singleton type sets add a type hypothesis on the new variable). [^bm79_p1]

## Major verified results (Boyer-Moore 1979)

| Example | Method | Key challenge |
|---|---|---|
| Tautology checker correctness | Functional semantics | 3 main lemmas + 4 subsidiary; induction on expression structure with non-trivial A1 (partial assignment) instance |
| Optimizing expression compiler | Functional semantics (McCarthy) | Induction on expression structure; cross-fertilization of stack induction hypotheses |
| Fast string searching algorithm | Floyd inductive assertions | Verification conditions for algorithm loop invariants; Boyer-Moore pattern matching algorithm |
| Unique Prime Factorization Theorem | Pure number theory from Peano axioms | ~345 definitions and lemmas; requires GCD, divisibility, prime lists, permutation machinery |

The string search verification is historically notable: Boyer and Moore were simultaneously developing the Boyer-Moore string search algorithm (1977) and used their theorem prover to verify its correctness — a case of the tool verifying its authors' own concurrent work. [^bm79_p1]

## Relationship to modern formal verification

The Boyer-Moore prover became **NQTHM** (the "Boyer-Moore theorem prover"), then **ACL2** (A Computational Logic for Applicative Common Lisp), developed by Moore and Matt Kaufmann. ACL2 proved:
- AMD K5 floating-point division correctness (Russinoff, post-Pentium FDIV bug).
- Java bytecode verifier correctness.
- Various Intel microprocessor properties.

The core design decisions of the 1979 book — induction from recursion, rewrite rule libraries, heuristic waterfall, shell principle — are preserved in ACL2. The book remains the primary reference for understanding ACL2's proof strategy. [unsourced — general knowledge]

## Contrast with resolution theorem proving

Resolution provers (the dominant approach in 1970s AI) operate on clause sets via a single inference rule (resolution). They handle quantified first-order logic but cannot directly axiomatize induction schemes (which are axiom *schemes*, not fixed axioms). Boyer-Moore trades generality for the ability to reason about concrete mathematical structures with induction. "While drawing heavily upon important facts of mathematical logic, our research is really more artificial intelligence than logic. The principal question we ask (and sometimes answer) is 'how do we discover proofs?'" [^bm79_p1]

## See also

- [Robert S. Boyer](/software-engineering/robert-s-boyer.md) — co-author, SRI International
- [J Strother Moore](/software-engineering/j-strother-moore.md) — co-author, SRI International; later developed ACL2
- [A Computational Logic (source)](/software-engineering/sources/a-computational-logic-1979.md) — full source summary
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — algorithmic context; Boyer-Moore string search algorithm appears here under string matching
- [Complexity Theory and NP-Completeness](/software-engineering/complexity-theory.md) — undecidability and complexity context for theorem proving

[^bm79_p1]: [A Computational Logic — Part 1/12](../../raw/pdf/pdf-a-computational-logic-1979-part-01.md)
[^bm79_p2]: [A Computational Logic — Part 2/12](../../raw/pdf/pdf-a-computational-logic-1979-part-02.md)
[^bm79_p4]: [A Computational Logic — Part 4/12](../../raw/pdf/pdf-a-computational-logic-1979-part-04.md)
[^bm79_p7]: [A Computational Logic — Part 7/12](../../raw/pdf/pdf-a-computational-logic-1979-part-07.md)
[^bm79_p10]: [A Computational Logic — Part 10/12](../../raw/pdf/pdf-a-computational-logic-1979-part-10.md)
