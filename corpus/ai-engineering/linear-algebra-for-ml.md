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
aliases:
  - linear algebra
  - vectors and matrices
  - vector spaces
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

TL;DR: Linear algebra provides the language for representing data (vectors), transformations (matrices), and structure (vector spaces, bases) that underpin all ML algorithms.

## Vectors and Vector Spaces

A **vector** is an object that can be added to another vector and scaled by a scalar, producing another vector of the same kind. ML treats data as vectors in R^n, where n is the feature dimension [^src1].

A **vector space** V is a set closed under vector addition and scalar multiplication. The key question linear algebra asks: "What is the set of all things reachable from a small starting set?" — this is the **span** [^src1].

**Subspaces**: A subset that is itself a vector space. The null space (kernel) of a matrix A is ker(A) = {x : Ax = 0}; the image (column space) is Im(A) = {Ax : x ∈ R^n}.

## Linear Independence, Basis, Rank

A set of vectors {b_1, ..., b_k} is **linearly independent** if no vector can be written as a linear combination of the others. An independent spanning set for a vector space is a **basis** [^src1].

- All bases for a vector space have the same number of elements — the **dimension** of the space.
- The **rank** rk(A) of a matrix is the dimension of its column space, equal to the dimension of its row space.
- **Rank-nullity theorem**: rk(A) + dim(ker(A)) = n for A ∈ R^{m×n}.

## Matrix Operations

For A ∈ R^{m×n}, B ∈ R^{n×k}, the product C = AB ∈ R^{m×k} has entries c_{ij} = sum_l a_{il} b_{lj} — computed as dot products of rows of A with columns of B [^src2].

Key properties: matrix multiplication is **not commutative** (AB ≠ BA in general); it is associative; distributive over addition.

**Inverse**: A^{-1} exists iff A is square and det(A) ≠ 0 (non-singular). When it exists, A A^{-1} = I = A^{-1} A.

**Transpose**: (AB)^T = B^T A^T; (A^{-1})^T = (A^T)^{-1}.

## Inner Products and Norms

An **inner product** ⟨·,·⟩ on a vector space generalizes the dot product. It must be symmetric, positive definite, and bilinear. The dot product x^T y is the standard inner product on R^n [^src1].

From an inner product we derive:
- **Norm** (length): ||x|| = sqrt(⟨x,x⟩)
- **Distance**: d(x,y) = ||x − y||
- **Angle**: cos θ = ⟨x,y⟩ / (||x|| ||y||)
- **Orthogonality**: x ⊥ y iff ⟨x,y⟩ = 0

**Common norms**: L1 norm ||x||_1 = sum|x_i|; L2 (Euclidean) ||x||_2 = sqrt(sum x_i^2); Frobenius norm for matrices ||A||_F = sqrt(sum_{ij} A_{ij}^2).

## Orthogonal Projections

The orthogonal projection of x onto a subspace U spanned by basis vectors {b_1,...,b_k} minimizes ||x − projection||. For a column space of matrix B: proj_U(x) = B(B^T B)^{-1} B^T x [^src1].

When B is orthonormal (columns have unit norm and are mutually orthogonal), this simplifies to BB^T x. This is the foundation for least-squares regression and PCA.

## Gram-Schmidt Orthogonalization

Given a basis {b_1,...,b_k}, Gram-Schmidt constructs an orthonormal basis {u_1,...,u_k} by iteratively subtracting the projection of each vector onto the previously constructed orthonormal vectors [^src1].

## Linear Mappings

A function Φ: V → W is a **linear mapping** if Φ(αx + βy) = αΦ(x) + βΦ(y). Every linear mapping between finite-dimensional spaces has a matrix representation that depends on the choice of bases.

**Kernel** ker(Φ) = {v : Φ(v) = 0_W}: the set of vectors mapped to zero. **Image** Im(Φ) = {Φ(v) : v ∈ V}: the set of reachable outputs. These encode the mapping's structure and relate to solvability of linear systems.

## Systems of Linear Equations

Ax = b has: no solution if b ∉ Im(A); a unique solution if A is invertible; infinitely many solutions if ker(A) is non-trivial. Solved via Gaussian elimination (row echelon form). This underlies linear regression's normal equations [^src1].

## Relationship to Decompositions

The rank, null space, and image of a matrix are fully revealed by the SVD — see [SVD](/ai-engineering/singular-value-decomposition.md). Eigendecomposition and Cholesky are covered in [Matrix Decompositions](/ai-engineering/matrix-decompositions.md).

[^src1]: [Mathematics for Machine Learning, Part 1](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-01.md)
[^src2]: [Mathematics for Machine Learning, Part 2](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-02.md)
