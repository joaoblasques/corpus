---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-01.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-02.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-03.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-04.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-05.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-06.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-07.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-08.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-09.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-10.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-11.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-12.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-13.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-14.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-15.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-16.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-17.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-seven-sketches-in-compositionality-an-invitation-t-part-18.md
    channel: pdf
    ingested_at: 2026-08-08
aliases:
  - Seven Sketches in Compositionality
  - Applied Category Theory (Fong & Spivak)
  - Fong Spivak ACT
  - seven sketches
tags:
  - corpus/software-engineering
  - source
  - category-theory
  - mathematics
created: 2026-08-08
updated: 2026-08-08
---

# Seven Sketches in Compositionality: An Invitation to Applied Category Theory (Fong & Spivak, 2018)

TL;DR: Free applied category theory textbook (353pp, arXiv:1803.05316v3, CC-by) by Brendan Fong and David I. Spivak (MIT). Seven chapters each apply one categorical concept to a concrete domain: orders and databases and signal flow graphs and circuits and logic. Core thesis: category theory provides a rigorous, compositional language for reasoning across disparate domains. Prerequisite: minimal — designed for a broad audience including ML researchers, programmers, and philosophers.

## Authors

- **Brendan Fong** — MIT, applied category theory; co-developer of the optics framework for bidirectional programming.
- **David I. Spivak** — MIT, applied category theory; known for database schemas as categories, operadic composition.

Available free: arXiv:1803.05316. MIT OCW accompanying materials exist. All 18 parts (complete book) ingested [^p01].

---

## Chapter 1: Generative Effects — Orders and Adjunctions

**Preorder**: a set P with a reflexive and transitive relation ≤. Not necessarily antisymmetric — elements can satisfy both p ≤ q and q ≤ p without being equal (those are called isomorphic in the preorder) [^p01].

**Partial order**: a preorder that is also antisymmetric (p ≤ q and q ≤ p ⟹ p = q). Example: the power set P(X) ordered by inclusion [^p02].

**Hasse diagram**: visual representation of a partial order; edges drawn only for "cover" relations (immediate successors), omitting transitively implied edges [^p02].

**Join (∨) and meet (∧)**: in a preorder, the join A ∨ B is the least element ≥ A and ≥ B; the meet A ∧ B is the greatest element ≤ A and ≤ B. Need not exist in arbitrary preorders. In the power set lattice, join = union and meet = intersection [^p03].

**Galois connection**: a pair of monotone maps f: P → Q and g: Q → P satisfying f(p) ≤ q ⟺ p ≤ g(q). f is the left adjoint; g is the right adjoint. The partition lattice example: sending a partition c on T to its preimage 1!(c) on S is the right adjoint of the pushforward 1*(c) [^p01].

**Generative effects**: a map Φ: P → Q may satisfy Φ(A) ∨ Φ(B) < Φ(A ∨ B) — the combination of outputs is strictly less informative than the output of the combination. This inequality captures how "emergence" can arise when combining systems: the joined system has properties not present in either component alone [^p01].

---

## Chapter 2: Resources — Monoidal Preorders and Enrichment

**Monoidal preorder**: a preorder (X, ≤) equipped with a monoidal product ⊗: X × X → X and unit I, satisfying: if x₁ ≤ y₁ and x₂ ≤ y₂ then x₁ ⊗ x₂ ≤ y₁ ⊗ y₂. Example: (ℝ≥0, ≤, ×, 1) for resource accounting; (ℕ, ≤, +, 0) for cost budgets [^p04].

**Symmetric monoidal preorder**: monoidal preorder where ⊗ is symmetric (x ⊗ y ≅ y ⊗ x). Enables parallel composition in wiring diagrams: wires in parallel represent ⊗ of their labels [^p04].

**Wiring diagrams**: graphical language for monoidal preorders. Boxes represent relations (x ≤ y); wires represent elements; series composition = transitivity; parallel composition = ⊗. The formalism is "sound and complete" in the sense that valid wiring diagram manipulations correspond to valid inequalities [^p04].

**Enriched categories**: a category where hom-sets are replaced by objects in a monoidal category V. A V-enriched category has hom-objects hom(A,B) ∈ Ob(V) rather than mere sets. Preorder enrichment: hom(A,B) ∈ {true, false} (there is or isn't a morphism). ℝ≥0-enrichment gives metric spaces (hom(A,B) = distance) [^p04].

---

## Chapter 3: Databases — Categories, Functors, and (Co)limits

**Category**: objects + morphisms + identity morphisms + associative composition. Example: **Set** (sets and functions); **Grph** (graphs and graph homomorphisms); **Mat(R)** (matrices over a ring R) [^p06].

**Free category on a graph**: take a directed graph and form a category where morphisms are paths (finite sequences of composable edges). The identity morphism on each vertex is the empty path [^p06].

**Functor**: a map F: C → D between categories that preserves identities and composition. A database instance is a functor from the schema category (a finitely-presented category) to **Set** (data as sets and functions between them) [^p06].

**Natural transformation**: a family of morphisms αₓ: F(x) → G(x) for each x ∈ Ob(C) such that for every f: x → y in C, G(f) ∘ αₓ = αᵧ ∘ F(f) (naturality square commutes). Database migrations are natural transformations [^p06].

**Adjunction**: functors L: C ⇌ D: R with a natural bijection C(Lc, d) ≅ D(c, Rd) for all c, d. L is the left adjoint, R the right adjoint; written L ⊣ R. Key example: currying — (−×B) ⊣ (−)^B in Set, giving the one-to-one correspondence between functions A×B→C and functions A→C^B [^p07].

**Limits and colimits**: universal constructions generalizing products, equalizers, pullbacks (limits) and coproducts, pushouts (colimits). A limit of a diagram D: J → C is an object L with maps to every D(j) such that any other such cone factors uniquely through L [^p07].

**Data migration (∃, Π, Δ)**: given a functor f: C → D between schema categories, data migration gives three functors: Δ_f (restriction/reindexing), ∃_f (left Kan extension, "push forward"), Π_f (right Kan extension, "pull back"). These are adjoints: ∃_f ⊣ Δ_f ⊣ Π_f [^p07].

---

## Chapter 4: Collaborative Design — Co-design and Profunctors

**Feasibility relation**: given sets X and Y, a feasibility relation R: X ⇸ Y assigns to each pair (x, y) a truth value (or resource cost) indicating whether it is feasible to provide y given x [^p08].

**Profunctor**: a functor P: C^op × D → V (for V-enriched categories). Generalizes feasibility relations to the categorical setting; morphisms between profunctors are natural transformations [^p08].

**Co-design**: a framework for multi-stakeholder design where requirements from one subsystem become resources for another. Category theory structures the composition of these relationships, ensuring the whole is analyzed correctly from its parts [^p08].

---

## Chapter 5: Signal Flow Graphs — Props, Presentations, and Proofs

**PROP (Product and Permutation category)**: a symmetric strict monoidal category whose objects are natural numbers {0, 1, 2, …} and monoidal product is addition. Morphisms n → m are "boxes" with n inputs and m outputs [^p10].

**Signal flow graph (SFG)**: a graphical representation of a linear dynamical system; edges carry scalar gains. The free PROP on generators (copy, delete, add, scalar multiplication, zero) encodes signal flow graphs [^p10].

**Functor S: SFGR → Mat(R)**: maps a signal flow graph (as a PROP expression) to a matrix over a ring R. The (i,j) entry gives the amplification of the ith input at the jth output. Compositionality ensures S(α # β) = S(α) · S(β) (matrix multiplication) and S(α + β) = block diagonal [^p10].

---

## Chapter 6: Circuits — Hypergraph Categories and Operads

**Hypergraph category**: a symmetric monoidal category where every object is self-dual (has a Frobenius algebra structure). Enables wiring diagrams with sharing — wires can branch and merge freely, unlike in generic monoidal categories [^p12].

**Frobenius algebra**: an object X with multiplication μ: X⊗X → X, unit η: I → X, comultiplication δ: X → X⊗X, and counit ε: X → I satisfying the Frobenius condition. The compact closed case adds cups and caps [^p12].

**Operad**: generalizes PROPs to "one output" operations. An operad O assigns a set O(n) of n-ary operations for each n, with a composition rule and unit. Operadic composition glues outputs into inputs more flexibly than PROP composition [^p12].

---

## Chapter 7: Logic — Toposes as Generalized Set Theory

**Topos**: a category with finite limits, power objects (for any A, the object P(A) classifying subobjects of A), and a subobject classifier Ω. The category **Set** is a topos; so is the category of sheaves on a topological space [^p16].

**Subobject classifier (Ω)**: an object Ω in a topos with a "true" morphism 1 → Ω such that every monomorphism A → B corresponds uniquely to a characteristic morphism B → Ω. In **Set**, Ω = {true, false} and characteristic morphisms are indicator functions [^p16].

**Presheaf**: a functor C^op → Set. The category of presheaves on a category C forms a topos. Used to model databases that evolve over a category of "times" or "contexts" [^p16].

**Sheaf**: a presheaf satisfying a gluing condition. Sheaves on a topological space formalize the idea of local data that is compatible on overlaps and uniquely glues to global data [^p16].

**Internal logic of a topos**: every topos has an internal higher-order intuitionistic logic. Reasoning in the internal language corresponds to constructive mathematics inside the topos [^p16].

---

## Relevance to Software Engineering

- **Database schema as category**: functors and natural transformations give a rigorous compositional theory of data migration and schema mapping.
- **Adjoint functors as universal design**: many software constructions (free/forgetful, left/right Kan extensions) are adjoints — understanding adjunctions reveals the deep structure of APIs and compilers.
- **Signal flow graphs**: category-theoretic treatment of linear systems used in control engineering, DSP, and machine learning (backpropagation as a functor).
- **Wiring diagrams**: compositional graphical language applicable to hardware circuits, chemical reaction networks, and agent architectures.
- **Compositionality**: the central theme — understanding complex systems by composing simple subsystems with well-defined interfaces; directly applicable to microservices, type systems, and API design.

---

[^p01]: [Seven Sketches — Part 01](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-01.md)
[^p02]: [Seven Sketches — Part 02](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-02.md)
[^p03]: [Seven Sketches — Part 03](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-03.md)
[^p04]: [Seven Sketches — Part 04](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-04.md)
[^p06]: [Seven Sketches — Part 06](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-06.md)
[^p07]: [Seven Sketches — Part 07](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-07.md)
[^p08]: [Seven Sketches — Part 08](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-08.md)
[^p10]: [Seven Sketches — Part 10](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-10.md)
[^p12]: [Seven Sketches — Part 12](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-12.md)
[^p16]: [Seven Sketches — Part 16](../../../raw/pdf/pdf-seven-sketches-in-compositionality-an-invitation-t-part-16.md)
