---
type: source
domain: ai-engineering
status: draft
sources:
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
  - Reinforcement Learning An Introduction
  - Sutton Barto
  - RL textbook
  - RL Introduction
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-23
updated: 2026-07-23
---

# Reinforcement Learning: An Introduction (Sutton & Barto, 2018)

**TL;DR**: 548-page definitive RL textbook by Richard S. Sutton and Andrew G. Barto (MIT Press, 2nd edition, 2018/2020; CC BY-NC-ND 2.0). Organized in three parts: tabular methods (Part I, Ch. 2–8), approximate solution methods (Part II, Ch. 9–13), and "Looking Deeper" covering psychology, neuroscience, applications, and frontiers (Part III, Ch. 14–17). The standard graduate reference for RL; most contemporary deep RL builds directly on foundations laid here. [^rl-p01]

## Book structure

**Part I — Tabular Solution Methods (Ch. 2–8)**: State and action spaces small enough for exact array representations. Covers the full spectrum from bandit problems (Ch. 2) through finite MDPs (Ch. 3), dynamic programming (Ch. 4), Monte Carlo methods (Ch. 5), temporal-difference learning (Ch. 6), n-step bootstrapping (Ch. 7), and planning with tabular methods including Dyna and MCTS (Ch. 8). [^rl-p01]

**Part II — Approximate Solution Methods (Ch. 9–13)**: Extends Part I ideas to large/continuous state spaces requiring function approximation. Covers on-policy prediction and control with approximation (Ch. 9–10), off-policy methods with approximation and the deadly triad (Ch. 11), eligibility traces and TD(λ) (Ch. 12), and policy gradient methods (Ch. 13). [^rl-p01]

**Part III — Looking Deeper (Ch. 14–17)**: Connections to animal learning psychology (Ch. 14), neuroscience and dopamine/TD error correspondence (Ch. 15), case studies (TD-Gammon, DQN, AlphaGo/AlphaGo Zero) (Ch. 16), and frontiers including options, reward design, and RL's future (Ch. 17). [^rl-p01]

## Core problem definition

Reinforcement learning is "learning what to do — how to map situations to actions — so as to maximize a numerical reward signal." The learner is not told which actions to take but must discover which actions yield the most reward through trial and error. Two distinguishing features: **trial-and-error search** and **delayed reward**. RL is formalized as the optimal control of incompletely-known Markov decision processes. [^rl-p02]

The four main subelements of an RL system [^rl-p02]:
1. **Policy** (π): mapping from states to action probabilities; the core of the agent — alone sufficient to determine behavior
2. **Reward signal**: immediate scalar feedback; defines the goal; basis for altering the policy
3. **Value function**: predicts long-run cumulative reward from each state; the primary focus of most RL algorithms
4. **Model** (optional): mimics environment dynamics; enables planning (model-based methods); absent in model-free methods

## MDP formalism

A finite MDP is defined by the dynamics function **p(s', r | s, a)** — the probability of transitioning to state s' with reward r, given current state s and action a. The Markov property: the probability of each next state and reward depends only on the immediately preceding state and action, not on earlier history. [^rl-p04]

**Return** (discounted): G_t = R_{t+1} + γ R_{t+2} + γ² R_{t+3} + ... = Σ_{k=0}^{∞} γ^k R_{t+k+1}, where γ ∈ [0,1] is the discount rate. γ=0 → myopic (maximize immediate reward only); γ→1 → farsighted. [^rl-p05]

**Policy and value functions** [^rl-p05]:
- π(a|s): probability of taking action a in state s
- v_π(s) = E_π[G_t | S_t = s]: state-value function — expected return starting from s following π
- q_π(s, a) = E_π[G_t | S_t = s, A_t = a]: action-value function

**Bellman equation for v_π** (3.14): v_π(s) = Σ_a π(a|s) Σ_{s',r} p(s',r|s,a) [r + γ v_π(s')]. Expresses the consistency condition between a state's value and its successors' values; v_π is the unique solution. [^rl-p05]

**Bellman optimality equations**: v*(s) = max_a Σ_{s',r} p(s',r|s,a) [r + γ v*(s')]; q*(s,a) = Σ_{s',r} p(s',r|s,a) [r + γ max_{a'} q*(s',a')]. The optimal policy is greedy with respect to v*. For finite MDPs, v* is the unique solution to the Bellman optimality equation. [^rl-p06]

## Key algorithms

### Dynamic Programming (Ch. 4)

Requires complete and accurate model of the environment dynamics. [^rl-p07]

- **Policy Evaluation**: iteratively applies the Bellman equation to compute v_π for a fixed policy
- **Policy Improvement**: derive a better policy by acting greedily with respect to v_π
- **Policy Iteration**: alternate policy evaluation and improvement until convergence to optimal (π*, v*)
- **Value Iteration**: combines one sweep of policy evaluation and one of policy improvement per sweep; equivalent to turning the Bellman optimality equation into an update rule
- **Generalized Policy Iteration (GPI)**: the general principle — any interleaving of evaluation and improvement converges; underlies nearly all RL methods

Asynchronous DP: update states in any order rather than full sweeps; enables real-time interaction and state-focused computation. [^rl-p07]

### Multi-armed Bandits (Ch. 2)

Nonassociative, purely evaluative feedback — single state, no temporal credit assignment. Key exploration–exploitation methods [^rl-p03][^rl-p04]:
- **ε-greedy**: select greedy action with probability 1−ε; random action with probability ε
- **UCB (Upper Confidence Bound)**: A_t = argmax_a [Q_t(a) + c √(ln t / N_t(a))]; favors uncertain and under-tried actions
- **Gradient Bandit**: learns numerical preferences H_t(a); selects actions via softmax distribution; stochastic gradient ascent on expected reward

### Monte Carlo Methods (Ch. 5)

No model required; learns from complete episodes of experience. [^rl-p08]
- **MC Prediction**: average observed returns following each state visit to estimate v_π
- **MC Control with Exploring Starts (ES)**: all state-action pairs have nonzero probability of being initial; alternate between MC policy evaluation and greedy improvement
- **On-policy MC Control**: uses ε-soft policies to ensure continued exploration without exploring starts
- **Off-policy MC** via importance sampling: learn about target policy π using episodes generated by behavior policy b; weighted importance sampling is lower-variance than ordinary importance sampling

### Temporal-Difference Learning (Ch. 6)

"If one had to identify one idea as central and novel to reinforcement learning, it would undoubtedly be temporal-difference (TD) learning" — combines Monte Carlo (no model needed, learns from experience) and DP (bootstrapping, no waiting for episode end). [^rl-p09]

**TD(0) update**: V(S_t) ← V(S_t) + α [R_{t+1} + γ V(S_{t+1}) − V(S_t)]. The bracketed term is the **TD error** δ_t. TD(0) converges to v_π. [^rl-p09]

**SARSA** (on-policy TD control): Q(S,A) ← Q(S,A) + α [R + γ Q(S',A') − Q(S,A)]; uses actual next action A' selected by current policy. Converges to q* when policy is GLIE (greedy in the limit with infinite exploration). [^rl-p09]

**Q-learning** (off-policy TD control, Watkins 1989): Q(S,A) ← Q(S,A) + α [R + γ max_{a'} Q(S',a') − Q(S,A)]; uses greedy max regardless of actual action taken; directly learns q*. First algorithm to fully integrate dynamic programming with online learning. [^rl-p09]

**Expected SARSA**: uses the expected value of Q(S',·) under current policy rather than the actual A'; generally lower variance than SARSA. [^rl-p09]

**Maximization bias and Double Q-learning**: using the maximum over estimated values as an estimate of the maximum true value yields positive bias. Double Q-learning uses two independent value functions Q1, Q2; one selects the maximizing action, the other evaluates it — unbiased. [^rl-p10]

### n-step Bootstrapping (Ch. 7)

Bridges TD (n=1) and Monte Carlo (n=∞). n-step return: G_{t:t+n} = R_{t+1} + γ R_{t+2} + ... + γ^{n-1} R_{t+n} + γ^n V_{t+n-1}(S_{t+n}). n-step Sarsa, n-step Q(σ) (unifying Sarsa, tree-backup, Expected Sarsa via per-step sampling decision σ_t ∈ {0,1}). [^rl-p11]

### Planning and Learning (Ch. 8)

**Dyna architecture**: integrates learning, planning, and acting. Real experience updates both the model and the value function directly (TD learning); simulated experience from the model also updates the value function (planning). Adding planning steps to real-time TD can dramatically accelerate learning. [^rl-p01]

**Monte Carlo Tree Search (MCTS)**: planning at decision time using simulation; builds a lookahead tree by selective expansion (UCB-based) and random rollouts; used in AlphaGo (combined with neural nets and policy gradient). [^rl-p01]

### Function Approximation (Ch. 9–10)

Parameterize value function: v̂(s, w) ≈ v_π(s). **Mean Square Value Error (VE)**: VE(w) = Σ_s μ(s) [v_π(s) − v̂(s,w)]². Minimize by stochastic gradient descent on VE. [^rl-p01]

**Semi-gradient TD**: update w toward bootstrapped targets; not true gradient descent since target also depends on w. Linear methods: v̂(s,w) = w⊤ x(s) where x(s) is a feature vector; converges near the VE optimum under on-policy distribution. Feature construction: tile coding, Fourier basis, radial basis functions. [^rl-p01]

**Artificial neural networks** (ANN): nonlinear function approximator; backpropagation computes gradients; combined with TD gives deep RL. Prefigured by Tesauro's TD-Gammon (backgammon, ≈10²⁰ states, 1992). [^rl-p01]

### Off-policy Methods with Approximation — The Deadly Triad (Ch. 11)

Instability/divergence can arise when combining: **(1) function approximation + (2) bootstrapping + (3) off-policy training**. None of the three alone causes divergence; all three together (the "deadly triad") can. [^rl-p01]

**Gradient-TD methods** (GTD2, TDC): address the deadly triad via two-timescale stochastic gradient descent on the projected Bellman error; converge under off-policy sampling. [^rl-p01]

**Emphatic-TD methods**: use emphasis weighting to restore the on-policy distribution to off-policy updates; also convergent. [^rl-p01]

### Eligibility Traces / TD(λ) (Ch. 12)

Eligibility traces e_t provide a mechanism to bridge TD and Monte Carlo by propagating credit backward to recently visited states. The **λ-return** G_t^λ = (1−λ) Σ_{n=1}^{∞} λ^{n-1} G_{t:t+n} is a weighted average of all n-step returns. [^rl-p01]

**TD(λ)**: the backward-view algorithm implementing the λ-return. Update: w ← w + α δ_t z_t where z_t = γλ z_{t-1} + ∇v̂(S_t, w). λ=0 → TD(0); λ=1 → Monte Carlo. True Online TD(λ) achieves an exact equivalence between forward and backward views. Sarsa(λ) extends eligibility traces to control. [^rl-p01]

### Policy Gradient Methods (Ch. 13)

Parameterize the policy directly: π(a|s, θ). Optimize by gradient ascent on J(θ) = v_{π_θ}(s₀). [^rl-p01]

**Policy Gradient Theorem**: ∇J(θ) ∝ Σ_s μ(s) Σ_a q_π(s,a) ∇π(a|s,θ). Allows gradient computation without knowing environment dynamics. [^rl-p01]

**REINFORCE** (Williams 1992): Monte Carlo policy gradient. Update: θ ← θ + α γ^t G_t ∇ln π(A_t|S_t,θ). Unbiased but high variance. Adding a baseline b(s) reduces variance without introducing bias: use v̂(s,w) as baseline. [^rl-p01]

**Actor-Critic**: actor = policy π_θ; critic = value estimator v̂(s,w). Critic reduces variance by replacing returns with TD estimates; enables online (per-step) learning rather than episode-level updates. [^rl-p01]

**Softmax policy for continuous actions**: parameterize π as a Gaussian distribution; learn mean and variance as functions of state features. [^rl-p01]

## Notation highlights

The book uses a deliberate notation distinguishing random variables (capital letters: S_t, A_t, R_t) from their instantiations (lowercase: s, a, r). Weight vectors w (value function) and θ (policy) are lowercase bold. The dynamics function p(s',r|s,a) replaces the older P^a_{ss'} and R^a_{ss'} notation. [^rl-p02]

## Historical context

Three threads converge in modern RL [^rl-p03]:
1. **Trial-and-error learning** (from animal psychology — Thorndike's Law of Effect, 1911; computational versions from Turing 1948, Michie 1961, Klopf 1982)
2. **Optimal control / dynamic programming** (Bellman 1957 — Bellman equation, MDPs, curse of dimensionality; Howard 1960 — policy iteration)
3. **Temporal-difference learning** (Samuel's checkers program 1959; Sutton 1988 — TD(λ), convergence proofs; Watkins 1989 — Q-learning, fully uniting all three threads)

The dopamine/TD error correspondence (Schultz, Dayan, Montague 1997) linking RL to neuroscience is one of the book's major themes (Ch. 15). [^rl-p03]

## Applications covered (Ch. 16)

- **TD-Gammon** (Tesauro 1992/1995): backgammon at world-class level via self-play TD(λ) + neural net; ≈10²⁰ states; prefigures deep RL
- **Watson's Daily-Double wagering** (IBM Jeopardy! 2011): RL for optimal bet sizing
- **Atari DQN** (DeepMind 2015): human-level video game play from raw pixels via Q-learning + CNN
- **AlphaGo / AlphaGo Zero** (Silver et al. 2016/2017): MCTS + policy/value neural networks; AlphaGo Zero learns entirely from self-play without human data

## Connections to other corpus pages

- [Reinforcement Learning (concept)](/ai-engineering/reinforcement-learning.md) — conceptual overview enriched by this source
- [Algorithms for Reinforcement Learning (Szepesvári)](/ai-engineering/sources/algorithms-for-reinforcement-learning.md) — rigorous mathematical treatment complementary to Sutton & Barto; covers convergence proofs, PAC-MDP theory, gradient TD

---

[^rl-p01]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-01.md — Table of contents, prefaces, chapter overview; Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018
[^rl-p02]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-02.md — Summary of Notation; Ch. 1: RL definition, four subelements (policy, reward, value function, model), exploration–exploitation, supervised vs. RL
[^rl-p03]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-03.md — Ch. 1 §1.7: Early history of RL — three threads (trial-and-error, optimal control, TD learning); Thorndike, Bellman, Samuel, Klopf, Watkins
[^rl-p04]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-04.md — Ch. 2: Multi-armed bandits; ε-greedy, UCB, gradient bandit algorithms, incremental implementation, nonstationary tracking
[^rl-p05]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-05.md — Ch. 3: Finite MDPs; agent–environment interface, dynamics p(s',r|s,a), returns and episodes, discounting, policies, value functions, Bellman equations
[^rl-p06]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-06.md — Ch. 3 §3.6–3.7: Optimal policies and value functions; Bellman optimality equations; approximation and tabular case
[^rl-p07]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-07.md — Ch. 4: Dynamic programming; value iteration, GPI, asynchronous DP
[^rl-p08]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-08.md — Ch. 5: Monte Carlo methods; MC ES, on-policy MC control, off-policy MC via importance sampling
[^rl-p09]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-09.md — Ch. 6: TD learning; TD(0), SARSA, Q-learning, Expected SARSA; central role of TD in RL
[^rl-p10]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-10.md — Ch. 6 §6.7: Maximization bias and Double Q-learning
[^rl-p11]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-11.md — Ch. 7: n-step bootstrapping; tree-backup algorithm; Q(σ) unifying algorithm
