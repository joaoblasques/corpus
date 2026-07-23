---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-36.md
    channel: pdf
    ingested_at: 2026-07-11
  - path: raw/_inbox/pdf-the-quest-for-artificial-intelligence-a-history-of-part-24.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-the-quest-for-artificial-intelligence-a-history-of-part-25.md
    channel: pdf
    ingested_at: 2026-07-15
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
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-01.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-02.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-03.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-04.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-05.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-06.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-07.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-08.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-09.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-10.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-11.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - reinforcement learning
  - RL
  - Markov decision process
  - MDP
  - value iteration
  - Q-learning
  - policy gradient
  - temporal difference learning
  - TD(lambda)
  - actor-critic RL
  - Bellman optimality
  - SARSA
  - Monte Carlo RL
  - eligibility traces
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-11
updated: 2026-07-23
---

# Reinforcement Learning

**TL;DR**: Reinforcement learning (RL) trains agents to take actions in an environment to maximize cumulative reward. Unlike supervised learning (labelled examples) or unsupervised learning (structure-finding), RL learns from interaction — the agent observes state, chooses action, receives reward, observes next state [^src1].

## Core formalism — Markov Decision Processes

All standard RL environments are modeled as **Markov Decision Processes (MDP)**. Sutton & Barto define the MDP dynamics via the four-argument function **p(s', r | s, a)** — the joint probability of next state s' and reward r given current state s and action a [^src4]. This subsumes earlier notation (P^a_{ss'}, R^a_{ss'}) and fully characterizes the environment [^src4].

| Element | Meaning |
|---|---|
| **S** | State space — all possible observations the agent can be in |
| **A(s)** | Action space — actions available in state s |
| **p(s',r\|s,a)** | Dynamics function — joint probability of next state and reward |
| **R_t** | Reward at time t — immediate scalar signal; agent seeks to maximize cumulative reward |

The **Markov property**: p(S_{t+1}, R_{t+1} | S_t, A_t) is fully determined by just the current state and action, not earlier history. This is a restriction on the *state* (which must encode all decision-relevant history), not on the process [^src4].

**Return (discounted)**: G_t = R_{t+1} + γ R_{t+2} + γ² R_{t+3} + ... where γ ∈ [0,1] is the discount rate. γ=0 → myopic; γ→1 → farsighted. Episodic and continuing tasks unified by treating terminal states as absorbing states generating zero reward [^src5].

**Policy**: π(a|s) = probability of taking action a in state s. Deterministic policies map s → a directly.

**Value functions** [^src5]:
- v_π(s) = E_π[G_t | S_t = s] — state-value function; expected return from s following π
- q_π(s,a) = E_π[G_t | S_t = s, A_t = a] — action-value function; expected return taking a in s then following π

**Bellman equation for v_π**: v_π(s) = Σ_a π(a|s) Σ_{s',r} p(s',r|s,a) [r + γ v_π(s')]. Expresses each state's value as a weighted average of immediate reward plus discounted successor values. v_π is the *unique* solution [^src5].

**Bellman optimality equations** [^src6]:
- v*(s) = max_a Σ_{s',r} p(s',r|s,a) [r + γ v*(s')] — a policy greedy w.r.t. v* is optimal
- q*(s,a) = Σ_{s',r} p(s',r|s,a) [r + γ max_{a'} q*(s',a')] — q* gives optimal action directly without model

## Key algorithms

**Value Iteration**: Turns the Bellman optimality equation into an iterative update — V_{k+1}(s) = max_a Σ_{s',r} p(s',r|s,a) [r + γ V_k(s')]. Converges to v* for discounted finite MDPs. Each sweep combines one policy evaluation step and one policy improvement step [^src7].

**Generalized Policy Iteration (GPI)**: The universal pattern underlying nearly all RL — alternating (or interleaving at any granularity) between policy evaluation and policy improvement; converges to optimal when both processes stabilize [^src7].

**SARSA** (on-policy TD control): Q(S,A) ← Q(S,A) + α[R + γ Q(S',A') − Q(S,A)]. Uses the actual next action A' taken by the current policy. The name comes from the quintuple (S, A, R, S', A'). Converges to q* under GLIE conditions [^src9].

**Q-Learning** (off-policy TD control, Watkins 1989): Q(S,A) ← Q(S,A) + α[R + γ max_{a'} Q(S',a') − Q(S,A)]. The max operation targets q* directly regardless of the behavior policy; model-free. "The temporal-difference and optimal control threads were fully brought together in 1989 with Chris Watkins's development of Q-learning" [^src3].

**Policy Gradient**: Parameterize policy π(a|s,θ) and optimize by gradient ascent on J(θ) = v_{π_θ}(s₀). **Policy Gradient Theorem**: ∇J(θ) ∝ Σ_s μ(s) Σ_a q_π(s,a) ∇π(a|s,θ) — allows gradient computation without knowing dynamics p. REINFORCE algorithm: update θ ← θ + α γ^t G_t ∇ ln π(A_t|S_t,θ); adding a value-function baseline reduces variance [^src4].

**Actor-Critic**: Combines policy gradient (actor, π_θ) with a value estimator (critic, v̂(s,w)); critic replaces full-return G_t with a TD target, enabling online per-step updates and lower variance [^src4].

**TD(λ) / Eligibility Traces**: Eligibility traces z_t propagate credit backward to recently visited states. The λ-return G_t^λ = (1−λ) Σ_{n=1}^∞ λ^{n-1} G_{t:t+n} averages all n-step returns. λ=0 → TD(0); λ=1 → Monte Carlo. Sarsa(λ) extends to control. True Online TD(λ) achieves exact forward-backward view equivalence [^src4].

## Distinctions from supervised learning

"Reinforcement learning is different from supervised learning, the kind of learning studied in most current research in the field of machine learning" — it is not told which actions to take, must discover them through interaction [^src4].

| | Supervised | RL |
|---|---|---|
| Signal | Label per example | Reward signal (possibly delayed) |
| Data | Fixed dataset | Generated by agent–environment interaction |
| Credit assignment | Immediate | Over many time steps (temporal credit assignment) |
| Exploration | None needed | Explicit: must try new actions to discover rewards |

"One of the challenges that arise in reinforcement learning, and not in other kinds of learning, is the trade-off between exploration and exploitation" [^src4]. The agent must exploit past knowledge to earn reward while exploring to find better actions.

## Historical milestone: TD-Gammon (Tesauro, 1992)

**TD-GAMMON** combined temporal-difference learning (TD(λ)) with a multi-layer neural network trained entirely by self-play from a random initial network [^src2]. Starting from scratch with no human expert knowledge beyond the rules of backgammon, TD-Gammon reached world-class play after ~1.5M self-play games — the first RL system to achieve expert human performance in a complex game. TD-Gammon's opening move recommendations also changed human expert theory; positions it preferred differently from convention were later validated by human grandmasters [^src2]. The system demonstrated that function approximation (neural nets) + TD learning could scale to large state spaces (~10²⁰ states), prefiguring deep RL (DQN, AlphaGo) by two decades. See [/ai-engineering/ai-history.md](/ai-engineering/ai-history.md) for broader context.

## Practical challenges

- **Sample efficiency**: RL often needs millions of environment steps; supervised learning needs far less data for similar task complexity.
- **Sparse rewards**: many environments give reward only at terminal states — the agent must perform a long correct sequence before receiving any learning signal.
- **Exploration–exploitation tradeoff**: too much exploitation = stuck in local optima; too much exploration = slow convergence.
- **The deadly triad**: function approximation + bootstrapping + off-policy training can cause divergence; addressed by gradient-TD methods [^src4].
- **Curse of dimensionality**: DP methods grow exponentially with state variables; RL approximation methods are designed to circumvent this [^src3].

## Connections to other corpus pages

- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — RL policy gradient is a form of stochastic gradient ascent.
- [Gaussian Mixture Models](/ai-engineering/gaussian-mixture-models.md) — EM algorithm has structural similarities to policy evaluation/improvement alternation.
- [Dive into Deep Learning](/ai-engineering/sources/dive-into-deep-learning.md) — Chapter 17 is the primary source for the D2L treatment.
- [Algorithms for Reinforcement Learning (Szepesvári)](/ai-engineering/sources/algorithms-for-reinforcement-learning.md) — rigorous treatment of TD(λ), gradient TD, LSTD, Q-learning convergence, actor-critic, and PAC-MDP exploration algorithms. [^src3]
- [Reinforcement Learning: An Introduction (Sutton & Barto)](/ai-engineering/sources/reinforcement-learning-introduction.md) — definitive 548pp textbook; primary source for formal MDP definitions, all core algorithms, and historical context. [^src4]

---

[^src1]: [D2L Part 36 — Reinforcement Learning (MDPs, Value Iteration)](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-36.md)
[^src2]: [The Quest for Artificial Intelligence — Part 25 (Ch. 29: TD-GAMMON, reinforcement learning applications)](../../raw/pdf/pdf-the-quest-for-artificial-intelligence-a-history-of-part-25.md) — Nils Nilsson (Cambridge, 2010)
[^src3]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-01.md — Csaba Szepesvári, *Algorithms for Reinforcement Learning* (Morgan & Claypool, 2009; updated 2019)
[^src4]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-02.md — Richard S. Sutton & Andrew G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018 — Ch. 1 core definitions, notation, exploration/exploitation
[^src5]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-05.md — Ch. 3: Finite MDPs; return and episodes; policies and value functions; Bellman equations
[^src6]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-06.md — Ch. 3 §3.6: Optimal policies and value functions; Bellman optimality equations
[^src7]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-07.md — Ch. 4: Dynamic programming; value iteration; GPI
[^src9]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-09.md — Ch. 6: TD learning; SARSA; Q-learning; TD(0)
[^src3b]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-03.md — Ch. 1 §1.7: Early history — three threads, Watkins Q-learning
