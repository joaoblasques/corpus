---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-01.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-02.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-03.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-04.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-05.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-06.md
    channel: pdf
    ingested_at: 2026-07-22
aliases:
  - Algorithms for Reinforcement Learning
  - Szepesvári RL
  - RL algorithms survey Szepesvari
  - TD learning algorithms
  - Q-learning analysis
  - actor-critic algorithms
  - temporal difference survey
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-22
updated: 2026-07-22
---

# Algorithms for Reinforcement Learning (Szepesvári, 2009)

**TL;DR**: A compact, mathematically rigorous survey monograph by Csaba Szepesvári (Morgan & Claypool, 2009; 98pp; last updated March 2019). Covers the algorithms and theory of RL building on dynamic programming. Focus: total expected discounted reward criterion. Organized into two main parts — value prediction problems and control problems — with complete pseudocode for ~20 algorithms. Target audience: advanced undergraduates, graduate students, and practitioners. All 6 parts ingested (complete). [^rl-p01]

## Core framework — Markov Decision Processes

A countable MDP is a triplet M = (X, A, P₀) where X is the state space, A the action space, and P₀(·|x,a) the transition probability kernel over X×R (state × reward). The discount factor γ ∈ [0,1]. A **deterministic stationary policy** π: X→A yields a Markov reward process; value functions V^π(x) = E[Σ_{t≥0} γ^t R_{t+1} | X_0 = x, following π]. [^rl-p01]

**Bellman equations** (Fact 1): V^π satisfies T^π V^π = V^π, where T^π V(x) = r(x, π(x)) + γ Σ_y P(x, π(x), y) V(y). T^π is a maximum-norm contraction when 0 < γ < 1 — unique fixed point. **Bellman optimality** (Fact 2): V* satisfies T*V* = V*, where T*V(x) = max_a [r(x,a) + γ Σ_y P(x,a,y) V(y)]. T* is also a max-norm contraction. [^rl-p01]

**Dynamic programming algorithms**: value iteration V_{k+1} = T* V_k converges geometrically to V*. Policy iteration alternates policy evaluation (solve T^{π_k} V = V) and policy improvement (π_{k+1} greedy w.r.t. Q^{π_k}). Policy iteration is computationally more expensive per step but needs fewer iterations. [^rl-p01]

## Value prediction algorithms (Section 3)

### TD(λ) — temporal difference learning
The fundamental insight of TD learning (Sutton 1988): update value estimates from bootstrapped targets rather than waiting for episode completion (Monte Carlo). **Tabular TD(0)** update: V(X_t) ← V(X_t) + α_t [R_{t+1} + γ V(X_{t+1}) − V(X_t)]. The term in brackets is the **TD error** δ_t. Convergence: TD(0) converges to V^π almost surely under standard step-size conditions. [^rl-p02]

**Every-visit Monte Carlo**: V(x) ← average of returns starting from x across all visits. Unbiased but high variance. TD methods reduce variance at cost of bias (from bootstrapping). **TD(λ)** unifies: eligibility traces e_t decay past states, propagating credit backward. λ=0 is TD(0); λ=1 is Monte Carlo. [^rl-p02]

### Function approximation
When |X| is too large to store one value per state: parameterize V_θ(x) ≈ V^π(x). **TD(λ) with linear function approximation**: V_θ(x) = θ · φ(x) where φ(x) ∈ R^d is a feature vector. Update: θ ← θ + α δ_t e_t, where e_t = γ λ e_{t-1} + φ(X_t). May diverge in off-policy settings (the "deadly triad"). [^rl-p02]

**Gradient TD methods** (GTD2, TDC): fix the divergence problem by using the projected Bellman equation and stochastic gradient descent on a true objective function. Converge under off-policy sampling. Two-timescale stochastic approximation: primary parameter θ uses slower step-size; auxiliary parameter w uses faster step-size. [^rl-p03]

**LSTD(λ)** (least-squares TD): batch method that solves for θ minimizing the projected Bellman error exactly. Requires O(d²) memory; O(d²) computation per update. Converges in O(d) samples rather than the O(d/ε) of incremental methods. More data-efficient but computationally costlier. [^rl-p03]

## Control algorithms (Section 4)

### Exploration — optimism in the face of uncertainty
**Bandits (UCB)**: maintain upper confidence bounds on estimated arm values; pull arm with highest UCB. Optimal regret O(√(K T log T)) for K arms, T steps. UCB1 algorithm: pull arm j maximizing Q̂_j + √(2 log t / N_j). [^rl-p04]

**E³ algorithm** (Kearns & Singh) for MDPs: partition states into "known" (visited ≥ m times) and "unknown"; maintain an optimistic MDP model; act optimally in optimistic model. PAC-MDP guarantee: with high probability, total steps with suboptimal behavior is polynomial in |X|, |A|, 1/ε, 1/δ, γ. [^rl-p04]

### Direct methods — Q-learning
**Tabular Q-learning** (Watkins 1989): model-free algorithm for learning Q*(x,a). Update: Q(X_t, A_t) ← Q(X_t, A_t) + α_t [R_{t+1} + γ max_{a'} Q(X_{t+1}, a') − Q(X_t, A_t)]. Converges to Q* under sufficient exploration and decaying step sizes. The "greedy in the limit with infinite exploration" (GLIE) condition is needed. [^rl-p04]

**Q-learning with function approximation**: Q_θ(x,a) = θ · φ(x,a). Suffers from divergence in the deadly triad (off-policy + function approximation + bootstrapping). Deep Q-networks (DQN, not in this book) address this via experience replay and target networks. [^rl-p05]

### Actor-critic methods
Separate the policy (actor, π_θ) from the value function estimator (critic, V or Q). **Policy gradient theorem**: ∇_θ E[return] = E[∇_θ log π_θ(a|x) · Q^{π_θ}(x,a)]. The critic reduces variance by replacing returns with Q̂. [^rl-p05]

**Natural policy gradient**: pre-multiplies the gradient by the inverse Fisher information matrix F^{-1}(θ). Equivalent to gradient descent in the space of distributions (invariant to parameterization). Connection to natural gradient in information geometry. [^rl-p05]

**Compatible function approximation** (Sutton et al.): if the critic approximates Q using features ψ(x,a) = ∇_θ log π_θ(a|x), then the gradient estimate is unbiased. This links actor and critic parameterizations. [^rl-p05]

## Connections to other corpus pages

- [Reinforcement Learning](/ai-engineering/reinforcement-learning.md) — conceptual overview; this source adds mathematical depth (Bellman operators, convergence proofs, TD(λ) analysis)
- [Probabilistic Machine Learning (Murphy)](/ai-engineering/sources/probabilistic-machine-learning-intro.md) — covers MDPs and RL from the probabilistic ML perspective
- [Deep Reinforcement Learning](/ai-engineering/sources/deep-reinforcement-learning-0-to-100-towards-data-science-100.md) — practical applications; Szepesvári provides the theoretical foundations

---

[^rl-p01]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-01.md — Overview, Section 2: MDP definition, value functions, Bellman equations, dynamic programming (value iteration, policy iteration)
[^rl-p02]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-02.md — Section 3.1: TD(0), every-visit Monte Carlo, TD(λ), eligibility traces, tabular case
[^rl-p03]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-03.md — Section 3.2: TD(λ) with function approximation, gradient TD (GTD2, TDC), LSTD(λ), LSPE
[^rl-p04]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-04.md — Section 4.1-4.2: catalog of learning problems, UCB bandits, E³ algorithm for MDPs, online learning in MDPs
[^rl-p05]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-05.md — Section 4.3-4.4: Q-learning (tabular and with function approximation), actor-critic, policy gradient, natural policy gradient, compatible function approximation
[^rl-p06]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-06.md — Section 5: further reading, applications, software; Appendix A: theory of discounted MDPs, contractions, Banach fixed-point theorem
