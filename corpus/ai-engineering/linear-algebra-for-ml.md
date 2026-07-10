---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-01.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-02.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-03.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-04.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-05.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - linear algebra ML
  - vector spaces
  - linear mappings
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Linear Algebra for Machine Learning

TL;DR: Linear algebra is the language of ML. Data is represented as vectors in R^n; models as linear mappings (matrices); solutions to Ax=b as intersections of hyperplanes. The key structures are vector spaces, bases, rank, inner products, and orthogonal projections. These underpin every major ML algorithm — regression solves a linear system, PCA projects onto eigenvectors, neural network layers are matrix multiplications.

## Vectors and Vector Spaces

A **vector** is any object closed under addition and scalar multiplication. This includes geometric arrows, polynomials, audio signals, and tuples in R^n. In ML, data points **x** ∈ R^D are vectors [^src1].

A **vector space** V over R satisfies: closed under addition (x + y ∈ V) and scalar multiplication (λx ∈ V) [^src1].

Key concept: **closure** — what is the set of all objects reachable by adding and scaling a given set? This generates a subspace.

## Systems of Linear Equations

The fundamental ML problem: given **A** ∈ R^{m×n} and **b** ∈ R^m, find **x** such that **Ax = b** [^src2].

Three possible outcomes:
- **No solution** — the system is inconsistent (b is not in the column space of A)
- **Unique solution** — A has full column rank
- **Infinitely many solutions** — underdetermined system; the solution set is an affine subspace

Geometric interpretation: each row of **Ax = b** defines a hyperplane; the solution is the intersection of all hyperplanes [^src2].

**Gaussian elimination** (row echelon form → reduced row echelon form) is the standard algorithm for solving linear systems. The augmented matrix [A|b] is reduced to reveal pivots, free variables, and the solution [^src2].

## Matrices

An m×n matrix **A** ∈ R^{m×n} collects m×n scalars. Key operations [^src2]:

- **Addition**: element-wise, requires same shape
- **Multiplication**: **C = AB** where c_{ij} = Σ_k a_{ik} b_{kj}. Not commutative (AB ≠ BA in general). Requires inner dimensions to match.
- **Hadamard product**: element-wise multiplication (not standard matrix product)
- **Transpose**: **(AB)^T = B^T A^T**
- **Inverse**: **A^{-1}** exists iff A is square and full-rank; **AA^{-1} = I**

**Similarity**: A and D are similar if **D = P^{-1}AP** for some invertible P. Similar matrices represent the same linear map in different bases [^src3].

## Vector Spaces, Subspaces, Span

A **subspace** U ⊆ V is a vector space contained in V: closed under addition and scaling, contains **0** [^src3].

**Span**: the set of all linear combinations of a given set S = {b_1, ..., b_k}:
span[S] = {Σ λ_i b_i : λ_i ∈ R}

This is the smallest subspace containing S.

## Linear Independence, Basis, Rank

A set {b_1, ..., b_k} is **linearly independent** if Σ λ_i b_i = 0 implies all λ_i = 0. No vector in the set can be expressed as a linear combination of the others [^src3].

A **basis** of V is a linearly independent spanning set. All bases of V have the same cardinality = **dim(V)** [^src3].

**Rank** of matrix **A**: rk(**A**) = dimension of the column space = dimension of the row space. Key facts:
- rk(**A**) = rk(**A^T**)
- rk(**A**) ≤ min(m, n) for **A** ∈ R^{m×n}
- Full rank: rk(**A**) = min(m, n) — system has unique solution (when m=n)
- **A** is invertible iff rk(**A**) = n (for square n×n)

## Linear Mappings

A **linear mapping** Φ: V → W satisfies [^src3]:
- Φ(x + y) = Φ(x) + Φ(y)
- Φ(λx) = λΦ(x)

Every linear mapping has a matrix representation once bases are chosen. If B = {b_1, ..., b_n} is a basis of V and C = {c_1, ..., c_m} is a basis of W, the **transformation matrix** **A_Φ** ∈ R^{m×n} has columns = coordinates of Φ(b_j) in basis C.

**Change of basis**: if **B** and **B~** are two bases of the same space, the basis change matrix **S** transforms coordinates: x~ = S^{-1} x.

**Image and kernel**:
- Im(Φ) = {Φ(x) : x ∈ V} — the column space of A
- ker(Φ) = {x ∈ V : Φ(x) = 0} — the null space of A
- **Rank-nullity theorem**: dim(ker(Φ)) + dim(Im(Φ)) = dim(V) = n

## Analytic Geometry: Norms, Inner Products

A **norm** ‖·‖ on V satisfies: non-negativity, absolute homogeneity, triangle inequality. The L2 (Euclidean) norm: ‖x‖_2 = √(x^T x) [^src4].

An **inner product** ⟨·,·⟩: V × V → R satisfies: bilinearity, symmetry, positive-definiteness. The standard dot product ⟨x, y⟩ = x^T y [^src4].

Inner products induce:
- **Length**: ‖x‖ = √⟨x, x⟩
- **Distance**: d(x, y) = ‖x − y‖
- **Angle**: cos θ = ⟨x, y⟩ / (‖x‖ ‖y‖)
- **Orthogonality**: x ⊥ y iff ⟨x, y⟩ = 0

**Symmetric positive definite (SPD)** matrices: A matrix **A** is SPD if **x^T Ax > 0** for all x ≠ 0. SPD matrices define valid inner products ⟨x, y⟩_A = x^T Ay [^src4].

## Orthogonality and Projections

**Orthonormal basis (ONB)**: a basis where all vectors have unit length and are mutually orthogonal. In ONB, the transformation matrix is orthogonal: **P^T P = I**, so **P^T = P^{-1}** [^src4].

**Orthogonal complement** V⊥: the set of all vectors orthogonal to every element of V.

**Orthogonal projection** onto a subspace U with ONB {b_1, ..., b_k}: [^src4]

```
π_U(x) = Σ_i ⟨x, b_i⟩ b_i = BB^T x
```

where B = [b_1, ..., b_k]. The projection matrix **P_π = BB^T** (for ONB). Properties:
- P_π² = P_π (idempotent)
- P_π^T = P_π (symmetric)
- x − P_π x ⊥ U

For a general (non-ONB) basis: **π_U(x) = B(B^T B)^{-1} B^T x** (pseudo-inverse form).

**Gram-Schmidt orthogonalization**: iteratively constructs ONB from any basis [^src5]:
1. Start with b_1: u_1 = b_1 / ‖b_1‖
2. For each b_k: subtract projections onto previous u_i, normalize
3. Result: orthonormal set spanning the same subspace

## Affine Spaces

An **affine subspace** is a translated linear subspace: x_0 + U, where x_0 is a fixed point and U is a linear subspace. Solutions to **Ax = b** (when non-empty) form an affine subspace: x_particular + ker(A) [^src3].

## ML Connections

| Linear algebra concept | ML use |
|---|---|
| Vector space | Feature space, latent space |
| Linear mapping / matrix | Weight matrix in neural networks; any linear layer |
| Rank | Number of independent features; condition for MLE to have unique solution |
| Projection | Least-squares regression; PCA |
| Inner product | Similarity between vectors; kernel methods |
| Gram-Schmidt | QR decomposition; orthogonal regression |
| Change of basis | Eigendecomposition; diagonalization; SVD (two separate basis changes) |
| Null space (kernel) | Redundant features; solutions to underdetermined systems |

## Related Corpus Pages

- [/ai-engineering/matrix-decompositions.md](/ai-engineering/matrix-decompositions.md) — eigenvalues, Cholesky, eigendecomposition, SVD
- [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md) — SVD in depth (Brunton & Kutz perspective)
- [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md) — PCA as projection onto eigenvectors
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — full book summary

---

[^src1]: [Mathematics for Machine Learning, Part 1](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-01.md)
[^src2]: [Mathematics for Machine Learning, Part 2](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-02.md)
[^src3]: [Mathematics for Machine Learning, Part 3](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-03.md)
[^src4]: [Mathematics for Machine Learning, Part 4](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-04.md)
[^src5]: [Mathematics for Machine Learning, Part 5](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-05.md)
