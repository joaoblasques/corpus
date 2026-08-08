---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-open-logic-text-part-01.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-02.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-03.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-04.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-05.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-06.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-07.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-08.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-09.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-10.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-11.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-12.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-13.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-14.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-15.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-the-open-logic-text-part-16.md
    channel: pdf
    ingested_at: 2026-08-08
aliases:
  - The Open Logic Text
  - Open Logic Project
  - OLT
  - Open Logic Text formal metalogic
tags:
  - corpus/software-engineering
  - source
  - formal-logic
  - computability
  - mathematics
created: 2026-08-08
updated: 2026-08-08
---

# The Open Logic Text (Open Logic Project, 2026)

TL;DR: Open-source collaborative textbook of formal metalogic and formal methods (1016pp, CC BY 4.0, revision 9620cc7 dated 2026-07-12). Aimed at philosophy and computer science students at an intermediate level (after introductory formal logic). Covers: sets, relations, functions, cardinality, propositional logic, first-order logic, model theory, computability, incompleteness, and modal/temporal/intuitionistic logics. 16 of 47 parts ingested (covering the foundations through first-order logic: chapters 1–20). Remaining 31 parts (chapters 21–57) cover model theory, second-order logic, computability, Gödel's theorems, modal logics, and more.

## About the Project

**Open Logic Project** — a collaborative, open-source textbook project. The full source (LaTeX) is freely available and licensed CC BY 4.0, allowing modification and redistribution. The text is "modular": instructors can select which chapters to include. Revision controlled on GitHub [^p01].

---

## Part I: Sets and Functions (Chapters 1–5)

### Chapter 1: Sets

**Extensionality**: two sets are equal iff they have the same members. This is the foundational axiom of set theory: a set is determined entirely by its elements, not by how it was defined or by its order of listing [^p04].

**Russell's Paradox**: the set R = {x : x ∉ x} leads to contradiction (R ∈ R iff R ∉ R). Shows that unrestricted comprehension ("any property defines a set") is inconsistent. The resolution: Zermelo-Fraenkel (ZF) set theory restricts comprehension to subsets of existing sets [^p04].

**Set operations**: union (∪), intersection (∩), difference (−), power set ℘(A) (set of all subsets), Cartesian product A × B (set of ordered pairs). The power set of A has 2^|A| elements for finite A [^p04].

### Chapter 3: Relations

**Relation**: a subset R ⊆ A × B. A binary relation on A is a subset of A × A. Key properties: reflexive (∀x. xRx), symmetric (xRy → yRx), transitive (xRy ∧ yRz → xRz), antisymmetric (xRy ∧ yRx → x = y) [^p04].

**Equivalence relation**: reflexive + symmetric + transitive. Partitions A into equivalence classes. Canonical example: congruence modulo n [^p05].

**Partial order**: reflexive + antisymmetric + transitive. Examples: ⊆ on sets, ≤ on ℝ. **Linear (total) order**: additionally, every two elements are comparable [^p05].

### Chapter 3–4: Functions and Cardinality

**Injection (one-to-one)**: f: A → B is injective iff f(x) = f(y) → x = y. If f is injective, it has a left inverse g: B → A such that g(f(x)) = x for all x (requires Axiom of Choice for the general case when f is surjective) [^p05].

**Surjection (onto)**: f: A → B is surjective iff every b ∈ B has some a with f(a) = b. A surjective f has a right inverse h: B → A [^p05].

**Bijection**: injective + surjective. A bijection between A and B exists iff |A| = |B| (cardinality equal). Every bijection has a two-sided inverse [^p05].

**Cantor's Theorem**: for any set A, the power set ℘(A) is strictly larger than A — that is, there is no surjection from A onto ℘(A). Proof: for any function g: A → ℘(A), the set D = {x ∈ A : x ∉ g(x)} cannot be in the range of g (the diagonal argument). Therefore |A| < |℘(A)| for all A [^p06].

**Countable vs. uncountable**: a set A is countable (enumerable) iff |A| ≤ |ℕ|. ℕ, ℤ, ℚ are countable; ℝ and ℘(ℕ) are uncountable. A is non-enumerable iff |ℕ| < |A| [^p06].

---

## Part II: Propositional Logic (Chapters 6–13)

### Chapter 7: Syntax and Semantics of Propositional Logic

**Language L₀**: atomic propositions p₀, p₁, …; connectives ¬, ∧, ∨, →, ⊥. Formulas defined inductively via a formation sequence [^p08].

**Valuation**: a function v: At₀ → {T, F}. Extended inductively to all formulas:
- v(¬φ) = T iff v(φ) = F
- v(φ ∧ ψ) = T iff v(φ) = T and v(ψ) = T
- v(φ → ψ) = T iff v(φ) = F or v(ψ) = T [^p08].

**Satisfaction, validity, entailment**: a formula φ is *valid* (tautology) if v ⊨ φ for every valuation v. Γ *entails* φ (Γ ⊨ φ) if every valuation satisfying all of Γ also satisfies φ [^p08].

### Chapter 9: The Sequent Calculus

**Sequent**: Γ ⇒ Δ where Γ (left side) and Δ (right side) are finite sets of formulas. Semantics: Γ ⇒ Δ is valid iff every valuation satisfying all Γ satisfies some formula in Δ [^p09].

**Structural rules**: weakening (add formulas to either side), contraction (deduplicate), exchange (reorder). **Logical rules**: for each connective, one left rule (eliminating it on the left) and one right rule (introducing it on the right).

**Soundness of the sequent calculus**: every derivable sequent is valid. Proved by induction on the derivation, case-splitting on the last inference rule applied [^p09].

**Completeness**: every valid sequent is derivable. For propositional logic, completeness follows from the existence of saturated sets and the canonical model construction (Lindenbaum–Tarski method) [^p14].

### Chapter 10–11: Axiomatic Derivations and Natural Deduction

**Axiomatic derivation system**: a fixed set of axiom schemas plus modus ponens as the only inference rule. Derivations are sequences of formulas where each is an axiom or follows by modus ponens from prior formulas [^p14].

**Natural deduction**: inference rules that directly correspond to introduction and elimination of connectives. Hypotheses can be introduced and discharged during the proof. More readable than axiomatic systems for informal derivations [^p14].

---

## Part III: First-Order Logic (Chapters 14–20)

### Chapter 15: Syntax of First-Order Logic

**First-order language L**: constant symbols, function symbols (each with a fixed arity), predicate symbols (each with a fixed arity), equality predicate =, logical symbols ¬, ∧, ∨, →, ∃, ∀ [^p12].

**Terms**: built inductively from variables and constants using function symbols. **Formulas**: built from atomic formulas (predicate applications, identity) using connectives and quantifiers [^p12].

**Syntactic identity (≡)**: used to talk about strings of symbols being literally identical. φ ≡ ψ means φ and ψ are the same formula string character-by-character [^p12].

**Substitution**: t[s/x] denotes the term t with every occurrence of variable x replaced by term s. A variable y is *free* in φ if it is not bound by a quantifier ∀y or ∃y [^p12].

### Chapter 16–20: Semantics and Proof Theory of FOL

**Structure M**: an interpretation of L consisting of a non-empty domain |M|, interpreting each constant as an element, each function symbol as a function, each predicate symbol as a relation. **Variable assignment s**: a function assigning each variable to an element of |M| [^p16].

**Satisfaction (M ⊨ φ[s])**: defined inductively. For ∃x φ: M ⊨ (∃x φ)[s] iff there exists d ∈ |M| such that M ⊨ φ[s[x/d]] [^p16].

**Soundness of FOL proof systems**: if Γ ⊢ φ (φ is derivable from Γ), then Γ ⊨ φ (φ is entailed by Γ). Proved by induction on derivations, including the natural deduction rules for quantifiers [^p16].

**Completeness of FOL (Gödel, 1929)**: if Γ ⊨ φ then Γ ⊢ φ. This is harder — requires constructing a canonical model from a maximally consistent set of formulas. Proved via the Lindenbaum–Tarski method [^p14].

**Soundness vs. Completeness distinction**: soundness says the proof system does not prove falsehoods; completeness says it proves everything true. Both are required for a useful proof system. Gödel's completeness theorem (1929) confirmed FOL has both; his incompleteness theorems (1931) showed that sufficiently strong arithmetic systems cannot have both for arithmetic truth [^p14].

---

## Scope of Remaining Parts (not yet ingested: parts 17–47)

The content of the table of contents (parts 2-3) reveals the remaining scope:
- **Model Theory**: Löwenheim-Skolem theorems, compactness, models of arithmetic.
- **Craig's Interpolation and Definability theorems**.
- **Lindström's Theorem** (characterization of FOL among abstract logics).
- **Computability**: recursive functions, primitive recursion, Church-Turing thesis, Turing machines.
- **Incompleteness**: Gödel's first and second incompleteness theorems, Peano Arithmetic.
- **Second-Order Logic, Modal Logic, Temporal Logic, Epistemic Logic, Intuitionistic Logic**.

---

## Relevance to Software Engineering

- **Formal verification**: FOL and proof systems are the mathematical basis for formal specification languages (TLA+, Alloy, Z notation) and theorem provers (Coq, Isabelle, Lean).
- **Type theory**: the Curry-Howard correspondence maps logical proofs to programs; propositional logic corresponds to simply-typed lambda calculus.
- **Database theory**: relational databases are implementations of first-order theories; SQL queries correspond to FOL formulas.
- **Model checking**: temporal logic (CTL, LTL) is used in software model checking tools to specify and verify concurrent system properties.
- **Computability and limits**: understanding Gödel's incompleteness and the halting problem sets principled bounds on what can be automated or formally verified.

Cross-links: [/software-engineering/propositional-logic.md](/software-engineering/propositional-logic.md), [/software-engineering/formal-verification.md](/software-engineering/formal-verification.md), [/software-engineering/mathematical-proof.md](/software-engineering/mathematical-proof.md), [/software-engineering/set-theory.md](/software-engineering/set-theory.md).

---

[^p01]: [The Open Logic Text — Part 01](../../../raw/pdf/pdf-the-open-logic-text-part-01.md)
[^p04]: [The Open Logic Text — Part 04](../../../raw/pdf/pdf-the-open-logic-text-part-04.md)
[^p05]: [The Open Logic Text — Part 05](../../../raw/pdf/pdf-the-open-logic-text-part-05.md)
[^p06]: [The Open Logic Text — Part 06](../../../raw/pdf/pdf-the-open-logic-text-part-06.md)
[^p08]: [The Open Logic Text — Part 08](../../../raw/pdf/pdf-the-open-logic-text-part-08.md)
[^p09]: [The Open Logic Text — Part 09](../../../raw/pdf/pdf-the-open-logic-text-part-09.md)
[^p12]: [The Open Logic Text — Part 12](../../../raw/pdf/pdf-the-open-logic-text-part-12.md)
[^p14]: [The Open Logic Text — Part 14](../../../raw/pdf/pdf-the-open-logic-text-part-14.md)
[^p16]: [The Open Logic Text — Part 16](../../../raw/pdf/pdf-the-open-logic-text-part-16.md)
