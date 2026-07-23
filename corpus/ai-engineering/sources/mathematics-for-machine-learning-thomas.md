---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-mathematics-for-machine-learning-part-01.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-mathematics-for-machine-learning-part-02.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-mathematics-for-machine-learning-part-03.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - Mathematics for Machine Learning Thomas
  - math4ml
  - Garrett Thomas Berkeley
  - CS 189 math background
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-23
updated: 2026-07-23
---

# Mathematics for Machine Learning (Thomas 2018)

TL;DR: 47-page math course notes for CS 189/289A at UC Berkeley, by Garrett Thomas (January 2018). Covers linear algebra, calculus/optimization, and probability in a compact, proof-oriented style. Assumes prior exposure at the level of UCB Math 53/54; intended as background reference, not a replacement for prerequisites. More concise and proof-heavy than Deisenroth et al. 2020; particularly strong on the geometric intuition for SVD, positive definite quadratic forms, and the connection between eigenvalues and convexity.

---

## Section 3: Linear Algebra

### 3.1 Vector Spaces and Subspaces

A **vector space** V is defined by six axioms covering additive identity, additive inverse, multiplicative identity, commutativity, associativity, and distributivity [^t-p01]. The quintessential example is Euclidean space R^n, with addition and scalar multiplication defined component-wise.

A **subspace** S ⊆ V must contain 0, and be closed under addition and scalar multiplication. Sums of subspaces U + W (and direct sums U ⊕ W when U ∩ W = {0}) are defined; dim(U + W) = dim(U) + dim(W) − dim(U ∩ W) [^t-p01].

A **basis** is a linearly independent spanning set. Every finite-dimensional vector space of the same dimension over the same field is isomorphic — all real n-dimensional spaces are isomorphic to R^n [^t-p01].

### 3.2 Linear Maps

A linear map T: V → W preserves addition and scalar multiplication. Every linear map has a matrix representation in chosen bases: the j-th column of the matrix consists of coordinates of T(v_j) in the basis of W [^t-p01].

**Nullspace and range**: null(T) = {x : Tx = 0}; range(T) = {Tx : x ∈ V}. Both are subspaces. The **rank** of a matrix equals the dimension of its columnspace, which equals the dimension of its rowspace [^t-p01].

### 3.3–3.5 Metric, Normed, and Inner Product Spaces

A **metric** d(x, y) ≥ 0 generalizes distance; a **norm** ‖·‖ generalizes length. Any norm induces a metric: d(x, y) = ‖x − y‖. The p-norms on R^n (1-norm, 2-norm, ∞-norm) are all equivalent on finite-dimensional spaces — convergence in one implies convergence in any other [^t-p01].

An **inner product** ⟨·, ·⟩ induces a norm. Orthogonality: ⟨x, y⟩ = 0. Key results [^t-p01]:
- **Pythagorean Theorem**: x ⊥ y implies ‖x + y‖² = ‖x‖² + ‖y‖²
- **Cauchy-Schwarz inequality**: |⟨x, y⟩| ≤ ‖x‖ ‖y‖, with equality iff x and y are linearly dependent

### 3.5.3 Orthogonal Projections

For a finite-dimensional subspace S with ONB u_1, ..., u_m, every v ∈ V decomposes uniquely as v = v_S + v_⊥ where v_S ∈ S and v_⊥ ∈ S⊥ [^t-p01]. The **orthogonal projection** P_S satisfies:
- P_S is linear and idempotent: P_S² = P_S
- range(P_S) = S; null(P_S) = S⊥
- P_S v is the closest point in S to v: arg min_{s ∈ S} ‖v − s‖ = P_S v
- Matrix form: P_S = UU^T where U has the ONB vectors as columns [^t-p01]

The proof that orthogonal projection minimizes distance is constructive and relies on the Pythagorean theorem.

### 3.6–3.11 Eigenvalues, Symmetric Matrices, Positive Definiteness

For a square matrix A, nonzero x is an **eigenvector** with **eigenvalue** λ if Ax = λx. Eigenvalues shift by γ when γI is added; invert to get eigenvalue λ^{-1}; A^k x = λ^k x [^t-p01].

**Trace** = sum of diagonal entries = sum of eigenvalues (with multiplicity). **Determinant** = product of eigenvalues. Trace is invariant under cyclic permutation: tr(ABCD) = tr(BCDA) [^t-p01].

**Spectral Theorem** (Theorem 2): if A is symmetric, there exists an ONB for R^n consisting of eigenvectors of A. This yields the **eigendecomposition** A = QΛQ^T where Q is orthogonal and Λ is diagonal [^t-p02].

**Rayleigh quotient** R_A(x) = x^T Ax / ‖x‖². Key results [^t-p02]:
- Scale invariant: R_A(αx) = R_A(x)
- **Min-max theorem**: λ_min(A) ≤ R_A(x) ≤ λ_max(A) for all x ≠ 0, with equality iff x is a corresponding eigenvector
- This gives a variational characterization: λ_max(A) = max_{‖x‖=1} x^T Ax

**Positive semi-definite (PSD)**: A is PSD if x^T Ax ≥ 0 for all x ↔ all eigenvalues ≥ 0. **Positive definite (PD)**: strict inequality ↔ all eigenvalues > 0. For any A, A^T A is always PSD; A^T A + εI is always PD for any ε > 0 [^t-p02].

**Geometry of PD quadratic forms**: the c-isocontours of f(x) = x^T Ax are ellipsoids. Axes point in directions of eigenvectors of A; axis radii proportional to inverse square roots of corresponding eigenvalues — larger eigenvalue → shorter axis [^t-p02].

### 3.12 Singular Value Decomposition

Every matrix A ∈ R^{m×n} has SVD: A = UΣV^T, where U ∈ R^{m×m} and V ∈ R^{n×n} are orthogonal, and Σ ∈ R^{m×n} is diagonal with non-increasing nonneg singular values σ_i [^t-p02].

Equivalently: A = Σ_{i=1}^r σ_i u_i v_i^T (sum of r rank-1 outer products, r = rank(A)).

The SVD reveals eigendecompositions of A^T A and AA^T:
- Columns of V (right-singular vectors) are eigenvectors of A^T A
- Columns of U (left-singular vectors) are eigenvectors of AA^T
- Singular values are square roots of eigenvalues of A^T A [^t-p02]

### 3.13 Fundamental Theorem of Linear Algebra

For A ∈ R^{m×n}: null(A) = range(A^T)⊥; null(A) ⊕ range(A^T) = R^n; rank(A) + dim(null(A)) = n (rank-nullity). The SVD factors provide ONBs for all four fundamental subspaces [^t-p02].

### 3.14–3.16 Norms and Low-rank Approximation

The **spectral norm** ‖A‖_2 = σ_1 (largest singular value). The **Frobenius norm** ‖A‖_F = √(tr(A^T A)) = √(Σ σ_i²). Both are **unitary invariant** [^t-p02].

**Eckart-Young-Mirsky theorem**: the best rank-k approximation to A (in any unitary invariant norm) is A_k = Σ_{i=1}^k σ_i u_i v_i^T, i.e., truncate to the top k singular values [^t-p02].

The **Moore-Penrose pseudoinverse**: A† ∈ R^{n×m} is uniquely defined by four properties (AA†A = A, A†AA† = A†, AA† symmetric, A†A symmetric). Computed from SVD: A† = VΣ†U^T where Σ† transposes Σ and inverts nonzero diagonal entries [^t-p02].

---

## Section 4: Calculus and Optimization

### 4.1–4.5 Gradients, Jacobians, Hessians

**Gradient** ∇f(x) ∈ R^d points in the direction of steepest ascent. **Jacobian** J_f ∈ R^{m×n} for f: R^n → R^m. **Hessian** ∇²f(x) is the matrix of second partials; symmetric when partials are continuous (Clairaut's theorem) [^t-p02].

Key matrix calculus identities [^t-p02]:
- ∇_x (a^T x) = a
- ∇_x (x^T Ax) = (A + A^T)x; simplifies to 2Ax if A is symmetric

**Chain rule** (multivariate): if f: R^m → R^k and g: R^n → R^m, then J_{f∘g}(x) = J_f(g(x)) J_g(x). For scalar f, ∇(f∘g)(x) = J_g(x)^T ∇f(g(x)) [^t-p02].

### 4.6–4.7 Taylor's Theorem and Local Minima Conditions

**Taylor's theorem** (multivariate): f(x + h) ≈ f(x) + ∇f(x)^T h + ½ h^T ∇²f(x) h, with a third-order remainder [^t-p02].

**Necessary conditions for local minimum x***:
1. ∇f(x*) = 0 (first-order / stationarity)
2. ∇²f(x*) is positive semi-definite (second-order)

**Sufficient conditions**: ∇f(x*) = 0 AND ∇²f is PSD in a neighborhood of x* → local min. If ∇²f(x*) is strictly PD → strict local min [^t-p02].

Caution: ∇f(x*) = 0 and ∇²f(x*) PSD at a single point is insufficient; x³ has a saddle at 0 despite zero gradient and zero Hessian there [^t-p02].

**Stationary points** where ∇f = 0 but no extremum exists are **saddle points**.

### 4.8 Convexity

Three levels of convexity (increasing strength) [^t-p02]:
- **Convex**: f(tx + (1−t)y) ≤ tf(x) + (1−t)f(y)
- **Strictly convex**: strict inequality for x ≠ y, t ∈ (0,1)
- **Strongly convex with parameter m**: f(x) − (m/2)‖x‖² is convex

**Implications for minima** [^t-p02]:
- Convex f over convex set: every local minimum is a global minimum
- Strictly convex f: at most one local minimum (hence the unique global minimum if it exists)

**Equivalent characterizations** (twice differentiable f):
- f convex ↔ ∇²f(x) ⪰ 0 everywhere
- ∇²f(x) ≻ 0 everywhere → strictly convex
- f is m-strongly convex ↔ ∇²f(x) ⪰ mI everywhere [^t-p02]

**Preservation rules**: norms are convex; nonneg linear combinations of convex functions are convex; f(Ax + b) is convex when f is convex; max of convex functions is convex [^t-p02].

**Examples** [^t-p03]:
- Convex but not strictly convex: affine functions w^T x + α; ‖x‖_1
- Strictly but not strongly convex: x⁴, exp(x), −log(x)
- Strongly convex: ‖x‖_2²

---

## Section 5: Probability

### 5.1 Probability Space Basics

A **probability space** (Ω, F, P) has sample space Ω, sigma-algebra of events F, and probability measure P: F → [0,1] with P(Ω) = 1 and countable additivity [^t-p03].

Derived rules: P(A^c) = 1 − P(A); P(A ∪ B) = P(A) + P(B) − P(A ∩ B); **Boole's inequality** (union bound): P(∪ A_i) ≤ Σ P(A_i) [^t-p03].

**Conditional probability**: P(A|B) = P(A ∩ B) / P(B). **Chain rule**: P(A ∩ B) = P(A|B) P(B). **Bayes' rule**: P(A|B) = P(B|A) P(A) / P(B). Under Bayes: P(A) is prior, P(B|A) is likelihood, P(A|B) is posterior [^t-p03].

### 5.2 Random Variables

A **random variable** X: Ω → R is a measurable function on the probability space. Discrete X is described by a **p.m.f.**; continuous X by a **p.d.f.** p(x) ≥ 0 with ∫ p(x) dx = 1. Density values can exceed 1; they are relative, not absolute probabilities [^t-p03].

### 5.3–5.6 Expectations, Variance, Covariance

**Expected value** E[X] = Σ x p(x) (discrete) or ∫ x p(x) dx (continuous). Linearity holds regardless of independence; product rule holds only if independent [^t-p03].

**Variance** Var(X) = E[(X − E[X])²] = E[X²] − (E[X])². Standard deviation = √Var(X). For uncorrelated X_1, ..., X_n: Var(Σ X_i) = Σ Var(X_i) [^t-p03].

**Covariance**: Cov(X, Y) = E[(X − E[X])(Y − E[Y])] = E[XY] − E[X]E[Y]. Bilinear; Var(X) = Cov(X, X). **Correlation** ρ(X, Y) = Cov(X, Y) / (√Var(X) √Var(Y)) ∈ [−1, 1] [^t-p03].

Independence implies uncorrelated; converse does not hold in general [^t-p03].

### 5.7 Random Vectors and Covariance Matrix

For a random vector X ∈ R^n, the **covariance matrix** Σ has entries Σ_{ij} = Cov(X_i, X_j). The covariance matrix is symmetric and always positive semi-definite. The inverse Σ^{-1} is called the **precision matrix** [^t-p03].

### 5.8 Estimation of Parameters

**MLE**: maximize the likelihood L(θ) = p(x_1, ..., x_n; θ). For i.i.d. observations, maximize the log-likelihood Σ log p(x_i; θ). Maximizing log L is equivalent to maximizing L since log is monotonically increasing [^t-p03].

**MAP**: treats θ as a random variable with prior p(θ); by Bayes' rule, θ_MAP = arg max p(x_1,...,x_n|θ) p(θ). Computing the normalizing constant is often intractable, but it is not needed for the argmax [^t-p03].

**Conjugate priors**: when the prior and posterior belong to the same family (e.g., Binomial likelihood + Beta prior → Beta posterior). Enables closed-form Bayesian updates [^t-p03].

### 5.9 Gaussian Distribution

The **multivariate Gaussian** N(µ, Σ) with mean µ ∈ R^d and positive-definite covariance Σ ∈ R^{d×d}:

p(x; µ, Σ) = (2π)^{−d/2} det(Σ)^{−1/2} exp(−½ (x − µ)^T Σ^{-1} (x − µ))

The density is a strictly monotonically decreasing function of the precision matrix quadratic form x̃^T Σ^{-1} x̃ (where x̃ = x − µ), so points closer to the mean have higher density [^t-p03].

**Geometry**: isocontours of the Gaussian density are ellipsoids centered at µ. Axes point in directions of eigenvectors of Σ^{-1} (equivalently Σ); axis lengths proportional to square roots of eigenvalues of Σ (i.e., inverse square roots of eigenvalues of Σ^{-1}). This follows directly from the geometry of positive definite quadratic forms [^t-p03].

---

## Key Differences from Deisenroth et al. 2020

- **Scope**: 47 pages vs. ~400 pages — Thomas covers essentials only; proofs are included for shorter arguments but omitted for complex ones.
- **Proof orientation**: Thomas explicitly includes proofs for projection, Rayleigh quotients, eigenvalue-definiteness relations, and convexity preservation — more proof-centric than Deisenroth et al. in the overlap zones.
- **No ML algorithms**: Thomas explicitly does not discuss ML models; pure math background only. Deisenroth et al. build toward PCA, SVM, Gaussian processes.
- **Stronger on geometric convexity**: the strict/strong convexity taxonomy with proofs (Propositions 16–25) is more developed than Deisenroth et al.
- **Less on change of basis**: Thomas treats it briefly through the lens of isomorphisms; Deisenroth et al. dedicate full sections to coordinate representations and change-of-basis matrices.

## Related Corpus Pages

- [/ai-engineering/linear-algebra-for-ml.md](/ai-engineering/linear-algebra-for-ml.md) — vector spaces, projections, SVD in ML context
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — Gaussian, MLE/MAP, Bayesian inference
- [/ai-engineering/optimization-for-ml.md](/ai-engineering/optimization-for-ml.md) — gradient descent, convexity, Hessian conditions
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — Deisenroth/Faisal/Ong 2020 source summary (different book)
- [/ai-engineering/matrix-decompositions.md](/ai-engineering/matrix-decompositions.md) — eigendecomposition, SVD in depth

---

[^t-p01]: [Mathematics for Machine Learning (Thomas 2018), Part 1/3](../../../raw/pdf/pdf-mathematics-for-machine-learning-part-01.md)
[^t-p02]: [Mathematics for Machine Learning (Thomas 2018), Part 2/3](../../../raw/pdf/pdf-mathematics-for-machine-learning-part-02.md)
[^t-p03]: [Mathematics for Machine Learning (Thomas 2018), Part 3/3](../../../raw/pdf/pdf-mathematics-for-machine-learning-part-03.md)
