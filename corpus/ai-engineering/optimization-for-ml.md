---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-12.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-08.md
    channel: pdf
    ingested_at: 2026-07-08
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-26.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - gradient descent
  - convex optimization
  - Lagrange multipliers
  - KKT conditions
  - Newton's method
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-08
updated: 2026-07-10
---

# Optimization for Machine Learning

TL;DR: ML training = optimization: minimize a loss L(theta) over parameters theta. Gradient descent and variants (momentum, Adam) are workhorses. For constrained problems, Lagrange multipliers yield KKT conditions. Convex optimization guarantees global optimum and includes linear programming (LP) and quadratic programming (QP) as subclasses — SVMs and regularized regression are convex QPs. Backpropagation (chain rule applied to computation graphs) computes gradients of scalar losses w.r.t. all parameters efficiently.

## Gradients and the Jacobian

For f: R^n -> R, the **gradient** is the vector of partial derivatives:

```
nabla_x f = [df/dx_1, ..., df/dx_n]^T  in R^n
```

For f: R^n -> R^m (vector-valued), the **Jacobian** is:

```
J = df/dx  in R^{m x n},  J_{ij} = df_i/dx_j
```

For matrix-valued functions, gradients become higher-order tensors. A practical approach: flatten A in R^{m x n} to a vector in R^{mn}, compute Jacobian, reshape [^src2].

**Key gradient identities** (for scalar/vector/matrix derivatives common in ML):
- d/dx (x^T a) = a
- d/dx (x^T Ax) = (A + A^T)x = 2Ax if A symmetric
- d/dA (tr(AB)) = B^T
- d/dA (ln det A) = A^{-T}

**Backpropagation** applies the chain rule across a computation graph: for scalar loss L and intermediate variable z = f(x), dL/dx = dL/dz * dz/dx. Chained over network layers, this yields gradients for all parameters in a single backward pass [^src2].

## Gradient Descent

**Update rule**: given loss L(theta), iterate:

```
theta_{t+1} = theta_t - alpha * nabla_theta L(theta_t)
```

where alpha > 0 is the **learning rate** (step size) [^src1].

**Intuition**: the gradient points in the direction of steepest ascent. Subtracting it moves toward lower loss.

**Convergence**:
- Too large alpha: oscillates or diverges
- Too small alpha: converges but slowly
- For convex L with Lipschitz gradient, gradient descent converges at rate O(1/t)

**Variants in practice**:
- **Stochastic gradient descent (SGD)**: use mini-batch gradient estimate; O(1) cost per step
- **Momentum**: accumulate velocity; helps navigate ravines
- **Adam**: adaptive learning rates per parameter; de facto default for neural networks

**Gradient descent does NOT guarantee global optimum for non-convex L** (neural network losses are non-convex). In practice, local minima are often near-global in high dimensions, but saddle points can slow convergence [^src1].

## Constrained Optimization and Lagrange Multipliers

Standard form of constrained optimization [^src1]:

```
min_x f(x)
subject to:
  g_i(x) <= 0   (inequality constraints)
  h_j(x) = 0    (equality constraints)
```

**Lagrangian**: convert to unconstrained by introducing Lagrange multipliers lambda_i >= 0 (for inequalities) and nu_j (for equalities):

```
L(x, lambda, nu) = f(x) + sum_i lambda_i g_i(x) + sum_j nu_j h_j(x)
```

**KKT (Karush-Kuhn-Tucker) conditions**: necessary conditions for optimality [^src1]:
1. **Stationarity**: nabla_x L = 0 (gradient of Lagrangian w.r.t. x vanishes)
2. **Primal feasibility**: g_i(x*) <= 0, h_j(x*) = 0
3. **Dual feasibility**: lambda_i >= 0
4. **Complementary slackness**: lambda_i g_i(x*) = 0 (either constraint is active or multiplier is zero)

KKT conditions are sufficient for optimality when the problem is convex.

**Lagrange multipliers (equality-only case)**: minimize f(x) subject to h(x) = 0. At the optimum, nabla f and nabla h are parallel:

```
nabla f(x*) = nu nabla h(x*)
```

This says the level curves of f and the constraint surface are tangent at the optimum.

## Convex Optimization

A **convex set** C: for all x, y in C and theta in [0,1], theta*x + (1-theta)*y in C. A set is convex iff the line segment between any two points lies in the set.

A **convex function** f: R^D -> R satisfies [^src1]:

```
f(theta*x + (1-theta)*y) <= theta*f(x) + (1-theta)*f(y)
```

for all x, y in domain and theta in [0,1]. Geometrically: chord lies above function.

**Equivalent characterizations** (for differentiable f):
- First-order: f(y) >= f(x) + nabla f(x)^T (y - x)  (function lies above tangent)
- Second-order: nabla^2 f(x) is positive semidefinite everywhere

**Jensen's inequality**: for convex f and weights alpha_i summing to 1: f(sum_i alpha_i x_i) <= sum_i alpha_i f(x_i) [^src1].

**Key property**: every local minimum of a convex function over a convex set is a **global minimum**. This makes convex problems tractable.

**Convex optimization problem**: minimize f(x) subject to g_i(x) <= 0 and h_j(x) = 0 where f and g_i are convex, and h_j = 0 are convex sets [^src1].

## Linear Programming (LP)

Special case: linear objective and linear constraints [^src1]:

```
min_x c^T x
subject to Ax <= b
```

- d variables, m constraints
- The feasible set is a convex polytope; the optimum is always at a vertex
- Dual LP: max_{lambda>=0} -lambda^T b  subject to A^T lambda + c = 0
- Can solve primal or dual depending on which has fewer variables

LP is one of the most widely used optimization classes in industry (supply chain, scheduling, portfolio optimization).

## Quadratic Programming (QP)

Special case: quadratic objective, linear constraints [^src1]:

```
min_x 0.5 x^T Q x + c^T x
subject to Ax <= b
```

where Q is symmetric positive definite (so objective is convex).

**Key property**: the dual of a QP is also a QP. SVMs (support vector machines) are solved as QPs (see [/ai-engineering/support-vector-machines.md](/ai-engineering/support-vector-machines.md)).

**Regularized regression as QP**: Ridge regression minimizes ||y - Phi theta||^2 + lambda||theta||^2 — a QP with no constraints (unconstrained, convex).

## Newton's Method

Gradient descent uses first-order information; Newton's method uses second-order (Hessian) [^src1]:

```
theta_{t+1} = theta_t - (nabla^2 L(theta_t))^{-1} nabla L(theta_t)
```

- Converges quadratically (doubles digits of precision per step) vs linearly for gradient descent
- Computationally expensive: requires O(n^3) to invert n×n Hessian
- **Quasi-Newton methods** (L-BFGS): approximate Hessian without full computation; standard for medium-scale ML

## Duality

For any primal optimization problem, the **Lagrange dual** is:

```
max_{lambda>=0, nu} D(lambda, nu) = min_x L(x, lambda, nu)
```

**Weak duality**: D(lambda*, nu*) <= f(x*) always. The dual is a lower bound.

**Strong duality**: D(lambda*, nu*) = f(x*) holds for convex problems satisfying Slater's condition (there exists a strictly feasible point). Dual solution = primal solution.

**Dual SVM**: the SVM dual expresses the problem purely in terms of inner products between training points, enabling the kernel trick.

## ML Training as Optimization

| ML task | Optimization problem | Key property |
|---|---|---|
| Linear regression (MLE) | min ||y - X theta||^2 | Closed form: theta = (X^T X)^{-1} X^T y |
| Ridge regression (MAP) | min ||y - X theta||^2 + lambda||theta||^2 | Closed form: theta = (X^T X + lambda I)^{-1} X^T y |
| Logistic regression | min sum log(1 + exp(-y_n theta^T x_n)) | Convex, no closed form; use gradient descent |
| SVM (hard margin) | min ||w||^2 s.t. y_n(w^T x_n + b) >= 1 | Convex QP; dual has kernel trick |
| Deep learning | min L(theta) for non-convex L | No convergence guarantee; SGD with momentum in practice |
| EM algorithm (GMMs) | max E[log p(X, Z | theta)] | Monotone non-decreasing in each step; converges to local optimum |

## Adaptive Optimization Algorithms (D2L Chapter 12)

Beyond plain SGD, a family of adaptive algorithms adjust learning rates per parameter [^src3]:

**Adagrad** (Duchi et al. 2011): accumulates squared gradient magnitudes; divides learning rate by the square root. Coordinates with historically large gradients get smaller updates. "Particularly effective for sparse features where the learning rate needs to decrease more slowly for infrequently occurring terms." Problem: accumulated sum grows without bound → learning rate → 0 [^src3].

**RMSProp** (Tieleman and Hinton 2012): fixes Adagrad's unbounded accumulation with an exponential moving average: s_t = gamma * s_{t-1} + (1-gamma) * g_t^2. Decouples the learning rate schedule from coordinate-adaptive scaling. gamma ≈ 0.9 typical [^src3].

**Adadelta**: variant of Adagrad that uses a ratio of running averages to avoid needing to set a global learning rate. Less commonly used in practice.

**Adam** (Kingma and Ba 2014): combines momentum (first moment of gradient) with adaptive learning rates (second moment of gradient squared); adds bias correction for the first few steps [^src3]:

```
m_t = beta_1 * m_{t-1} + (1 - beta_1) * g_t          (first moment)
v_t = beta_2 * v_{t-1} + (1 - beta_2) * g_t^2         (second moment)
m_hat = m_t / (1 - beta_1^t)                           (bias correction)
v_hat = v_t / (1 - beta_2^t)
theta_{t+1} = theta_t - eta * m_hat / (sqrt(v_hat) + eps)
```

Default hyperparameters: beta_1=0.9, beta_2=0.999, eps=1e-8. Adam is the de facto default for deep learning. "Yogi" (Zaheer et al. 2018) is a variant that addresses Adam's convergence issues on non-stationary data.

**Learning rate scheduling**: decay the learning rate over training. Common schedules: step decay (halve every N epochs), cosine annealing, warmup + decay (ramp LR from 0 over first K steps before decaying). Warmup is critical for Transformer training [^src3].

## Related Corpus Pages

- [/ai-engineering/linear-algebra-for-ml.md](/ai-engineering/linear-algebra-for-ml.md) — vector calculus prerequisites
- [/ai-engineering/probability-and-statistics-for-ml.md](/ai-engineering/probability-and-statistics-for-ml.md) — MLE/MAP objectives to optimize
- [/ai-engineering/support-vector-machines.md](/ai-engineering/support-vector-machines.md) — SVM as a QP with dual formulation
- [/ai-engineering/gaussian-mixture-models.md](/ai-engineering/gaussian-mixture-models.md) — EM algorithm for GMM optimization
- [/ai-engineering/sources/mathematics-for-machine-learning.md](/ai-engineering/sources/mathematics-for-machine-learning.md) — full book summary

---

[^src1]: [Mathematics for Machine Learning, Part 12](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-12.md)
[^src2]: [Mathematics for Machine Learning, Part 8](../../raw/pdf/pdf-deisenroth-faisal-ong-mathematics-for-machine-learning-autho-part-08.md)
[^src3]: [D2L Part 26 — Adagrad, RMSProp, Adam (Ch 12 Optimization Algorithms)](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-26.md)
