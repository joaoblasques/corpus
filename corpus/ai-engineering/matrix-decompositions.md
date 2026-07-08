---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-06.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-07.md
    channel: pdf
    ingested_at: 2026-07-08
aliases:
  - Cholesky decomposition
  - eigendecomposition
  - diagonalization
  - matrix factorization
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Matrix Decompositions

TL;DR: Decomposing a matrix into simpler factors reveals its geometric action, enables efficient computation, and unlocks ML algorithms. Key decompositions: Cholesky (for SPD matrices — sampling Gaussians, solving linear systems efficiently), eigendecomposition (for square matrices — diagonalization, spectral analysis), and SVD (for any matrix — best low-rank approximation, covered in depth at [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md)).

## Determinant and Trace

The **determinant** det(**A**) of a square matrix measures the signed volume scaling factor of the linear map represented by **A** [^src1]:
- det(**AB**) = det(**A**) det(**B**)
- det(**A^T**) = det(**A**)
- det(**A^{-1}**) = 1/det(**A**)
- det(**A**) = 0 iff **A** is singular (not invertible)
- det(**A**) = product of all eigenvalues of **A**

The **trace** tr(**A**) = sum of diagonal entries = sum of all eigenvalues [^src1].

Geometric interpretation: |det(**A**)| is the ratio of volumes (area of image of unit cube / area of unit cube). If det > 0, orientation is preserved; if det < 0, orientation is flipped.

## Eigenvalues and Eigenvectors

**Definition**: **x** ≠ 0 is an eigenvector of **A** with eigenvalue λ if **Ax = λx** [^src1].

Equivalently: (**A** − λ**I**)**x** = 0 has nontrivial solutions, i.e., det(**A** − λ**I**) = 0.

**Characteristic polynomial**: p_A(λ) = det(**A** − λ**I**). The eigenvalues are its roots. For n×n matrix, this is a degree-n polynomial.

**Eigenspace**: E_λ = {x : **Ax** = λ**x**} = ker(**A** − λ**I**). All eigenvectors for eigenvalue λ form a subspace.

**Key theorems**:
- Eigenvectors for distinct eigenvalues are linearly independent [^src1]
- **Spectral theorem**: if **A** is symmetric (**A = A^T**), then all eigenvalues are real and there exists an ONB of eigenvectors [^src1]
- det(**A**) = Π_i λ_i (product of eigenvalues)
- tr(**A**) = Σ_i λ_i (sum of eigenvalues)

**Defective matrices**: a square matrix with fewer than n linearly independent eigenvectors. Cannot be diagonalized.

**Google PageRank** uses the eigenvector corresponding to eigenvalue 1 of a transition matrix. Power iteration converges to the dominant eigenvector [^src1].

**Practical computation**: eigenvalues are found iteratively (the Abel-Ruffini theorem proves no algebraic formula exists for polynomials of degree ≥ 5). Use `np.linalg.eigh` (symmetric) or `np.linalg.eig` (general).

## Cholesky Decomposition

**Definition (Theorem 4.18)**: Every symmetric positive-definite (SPD) matrix **A** can be factorized as [^src1]:

```
A = LL^T
```

where **L** is lower-triangular with positive diagonal elements (the Cholesky factor). **L** is unique.

**Computing L**: Elements lij are recovered column by column:
- Diagonal: l_{ii} = sqrt(a_{ii} − Σ_{k<i} l_{ik}²)
- Off-diagonal: l_{ji} = (a_{ji} − Σ_{k<i} l_{jk} l_{ik}) / l_{ii}

**Why SPD requirement**: the square-root analogy requires positive quantities; SPD is the matrix generalization.

**Applications in ML**:

1. **Sampling from N(μ, Σ)**: Compute Cholesky of Σ = **LL^T**. Draw **z ~ N(0, I)**. Then **x = Lz + μ** [^src1].

2. **Efficient determinant**: det(**A**) = det(**L**)² = (Π_i l_{ii})². Only requires O(n²) work after factorization vs O(n³) for a general determinant.

3. **Solving linear systems**: **Ax = b** → **LL^T x = b**. Solve **Ly = b** (forward substitution), then **L^T x = y** (backward substitution). Both O(n²).

4. **Variational autoencoders**: the reparametrization trick requires a differentiable sample from a Gaussian; Cholesky enables this [^src1].

**Gotcha**: Cholesky factorization requires the matrix to be SPD. Covariance matrices always are (if full-rank). Near-singular covariance matrices may need regularization (add ε**I**) before Cholesky.

## Eigendecomposition and Diagonalization

**Definition (Theorem 4.20)**: A square matrix **A** ∈ R^{n×n} can be diagonalized as [^src1]:

```
A = PDP^{-1}
```

where **P** contains eigenvectors as columns, and **D** is diagonal with eigenvalues, if and only if **A** has n linearly independent eigenvectors.

**Existence conditions**:
- Non-defective matrices can be diagonalized
- Symmetric matrices can always be diagonalized (spectral theorem)
- For symmetric **A**: **P** is orthogonal (P^T = P^{-1}), so **A = PDP^T**

**Geometric interpretation**: [^src1]
1. **P^{-1}**: change of basis from standard basis to eigenbasis
2. **D**: scale each axis by the corresponding eigenvalue
3. **P**: change back to standard coordinates

**Matrix powers**: if **A = PDP^{-1}**, then **A^k = PD^k P^{-1}**. D^k is cheap (raise each diagonal entry to power k). This makes matrix exponentiation efficient.

**Efficient determinant via eigendecomposition**: det(**A**) = det(**P**) det(**D**) det(**P^{-1}**) = det(**D**) = Π_i λ_i.

**Practical note**: For symmetric matrices, eigendecomposition and SVD coincide: **A = PDP^T = UΣV^T** with **U = V = P** and **Σ = D** (assuming non-negative eigenvalues). [^src1]

## SVD (Overview — defer to dedicated page)

The SVD **A = UΣV^T** generalizes eigendecomposition to non-square matrices. It always exists for any **A** ∈ R^{m×n}. The singular values σ_i are square roots of eigenvalues of **A^T A** [^src1].

Key differences from eigendecomposition:
- SVD works for non-square matrices; eigendecomposition requires square
- **U** and **V** in SVD are orthogonal but generally differ; in eigendecomposition **P** and **P^{-1}** are inverses
- Singular values in **Σ** are always real and non-negative; eigenvalues can be complex

See [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md) for the Eckart-Young theorem, low-rank approximation, and ML applications.

## Matrix Approximation via SVD

**Rank-1 decomposition**: a rank-r matrix **A** = Σ_{i=1}^r σ_i **u_i v_i^T** (sum of rank-1 outer products, weighted by singular values) [^src1].

**Truncated SVD (rank-k approximation)**: 

```
A_k = Σ_{i=1}^k σ_i u_i v_i^T
```

The Eckart-Young theorem: A_k is the best rank-k approximation to **A** in both Frobenius and spectral norm.

Application: image compression — a 1432×1910 grayscale image stored as matrix can be approximated with k singular values, storing only k(1432+1910+1) values instead of 1432×1910 [^src1].

## Matrix Phylogeny

Relationship between matrix types [^src1]:

```
All matrices (A ∈ R^{m×n})
└── Square (m = n)
    ├── Invertible (full rank)
    │   ├── Symmetric (A = A^T)
    │   │   ├── Positive semidefinite (x^T Ax ≥ 0)
    │   │   │   └── Positive definite (x^T Ax > 0) ← Cholesky applies
    │   │   └── Diagonalizable ← spectral theorem applies
    │   └── Orthogonal (A^T = A^{-1})
    └── Defective (cannot diagonalize)
```

## Related Corpus Pages

- [/ai-engineering/linear-algebra-for-ml.md](/ai-engineering/linear-algebra-for-ml.md) — vector spaces, basis, rank, inner products
- [/ai-engineering/singular-value-decomposition.md](/ai-engineering/singular-value-decomposition.md) — SVD and Eckart-Young theorem
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — Gaussian sampling uses Cholesky
- [/ai-engineering/pca-and-dimensionality-reduction.md](/ai-engineering/pca-and-dimensionality-reduction.md) — PCA uses eigendecomposition of covariance matrix
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — full book summary

---

[^src1]: [Mathematics for Machine Learning, Part 6](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-06.md)
[^src2]: [Mathematics for Machine Learning, Part 7](../../raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-07.md)
