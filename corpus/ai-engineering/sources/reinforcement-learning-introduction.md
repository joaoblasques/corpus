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
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-12.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-13.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-14.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-15.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-16.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-17.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-18.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-19.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-20.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-21.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-22.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-23.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-24.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-25.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-26.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-27.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-28.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-29.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-30.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-31.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-32.md
    channel: pdf
    ingested_at: 2026-07-24
  - path: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-33.md
    channel: pdf
    ingested_at: 2026-07-24
aliases:
  - Reinforcement Learning An Introduction
  - Sutton Barto
  - RL textbook
  - RL Introduction
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-23
updated: 2026-07-24
---

# Reinforcement Learning: An Introduction (Sutton & Barto, 2018)

**TL;DR**: 548-page definitive RL textbook by Richard S. Sutton and Andrew G. Barto (MIT Press, 2nd edition, 2018/2020; CC BY-NC-ND 2.0). Organized in three parts: tabular methods (Part I, Ch. 2–8), approximate solution methods (Part II, Ch. 9–13), and "Looking Deeper" covering psychology, neuroscience, applications, and frontiers (Part III, Ch. 14–17). The standard graduate reference for RL; most contemporary deep RL builds directly on foundations laid here. All 33 parts ingested (complete). [^rl-p01]

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

**Prioritized sweeping** (Ch. 8.4): prioritizes backups for state-action pairs with large expected value changes using a priority queue. On maze tasks, prioritized sweeping reduces updates needed by 5–10× vs. unprioritized Dyna-Q; handles stochastic environments via expected updates. [^rl-p12]

**Expected vs. sample updates** (Ch. 8.5): expected updates are uncorrupted by sampling error but require b times more computation (b = branching factor). Sample updates can achieve near-expected-update accuracy with a small fraction of b updates, especially for large stochastic branching factors and large state spaces. [^rl-p12]

**Trajectory sampling** (Ch. 8.6): distributes updates according to the on-policy distribution rather than exhaustive sweeps. Provides large speed advantages early (up to 10x faster convergence for large sparse problems) by focusing on reachable relevant states; may hurt in the long run as commonly-visited states already have near-correct values. [^rl-p12]

**Real-time dynamic programming (RTDP)** (Ch. 8.7): on-policy trajectory sampling version of value iteration. For stochastic shortest-path problems, RTDP converges to an optimal policy for all relevant states without visiting every state infinitely often — demonstrated requiring only ~50% of DP's updates on a racetrack example. [^rl-p12]

**Decision-time planning** (Ch. 8.8–8.11): planning focused on the current state. Heuristic search, rollout algorithms, and MCTS are all decision-time methods. [^rl-p13]

**Monte Carlo Tree Search (MCTS)** (Ch. 8.11): planning at decision time using simulation; builds a lookahead tree incrementally via four-step iterations: (1) **Selection** — tree policy (e.g. UCB) traverses to leaf; (2) **Expansion** — add child nodes for unexplored actions; (3) **Simulation** — rollout policy completes the episode; (4) **Backup** — returns backed up through tree. Only a subset of the state-action space (near the current state) is maintained; all nodes are discarded after action selection. MCTS responsible for Go improvement from weak amateur to grandmaster level (2005–2015); extended with neural networks in AlphaGo. [^rl-p13]

### Function Approximation (Ch. 9–10)

Parameterize value function: v̂(s, w) ≈ v_π(s). **Mean Square Value Error (VE)**: VE(w) = Σ_s μ(s) [v_π(s) − v̂(s,w)]². Minimize by stochastic gradient descent on VE. [^rl-p01]

**Semi-gradient TD**: update w toward bootstrapped targets; not true gradient descent since target also depends on w. Linear methods: v̂(s,w) = w⊤ x(s) where x(s) is a feature vector; converges near the VE optimum under on-policy distribution. [^rl-p01]

**State aggregation** (Ch. 9.3): groups states; one weight per group. A special case of SGD where the gradient is 1 for the state's group and 0 elsewhere. Produces staircase approximations; biased toward frequently-visited states within each group per the on-policy distribution μ. [^rl-p14]

**Feature construction for linear methods** (Ch. 9.5) [^rl-p15]:
- **Tile coding**: partition the state space into overlapping grids (tilings); each tile = one binary feature. Allows flexible generalization/discrimination control by mixing stripe, diagonal, and rectangular tilings. Hashing reduces memory requirements by random collapsing with little performance loss.
- **Radial basis functions (RBFs)**: generalize coarse coding; continuous-valued features xi(s) = exp(−|s − ci|² / 2σi²). Natural for continuous state spaces; more computationally expensive than tile coding.

**Artificial neural networks** (ANN): nonlinear function approximator; backpropagation computes gradients; combined with TD gives deep RL. Prefigured by Tesauro's TD-Gammon (backgammon, ≈10²⁰ states, 1992). [^rl-p01]

### Off-policy Methods with Approximation — The Deadly Triad (Ch. 11)

Instability/divergence can arise when combining: **(1) function approximation + (2) bootstrapping + (3) off-policy training**. None of the three alone causes divergence; all three together (the "deadly triad") can. [^rl-p01]

**Bellman error (BE) minimization** (Ch. 11.5): minimizing the mean-square Bellman error requires two independent samples of the next state (the residual-gradient algorithm); in practice only one sample is obtained per interaction step, making naive minimization biased. The A-presplit example shows BE minimization can converge to systematically wrong values even for deterministic problems. Semi-gradient TD converges to better values empirically than BE-minimizing methods in many cases. [^rl-p18]

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

## Part III — Looking Deeper (Ch. 14–17)

### Psychology (Ch. 14)

RL has deep connections to animal learning psychology. The **Rescorla-Wagner model** of classical conditioning is a supervised error-correction rule (equivalent to LMS/Widrow-Hoff); it explains blocking (prior learning blocks new CS learning when the prediction error is already near zero). The TD model of classical conditioning extends Rescorla-Wagner to within-trial temporal dynamics, predicting earlier and earlier reward prediction signals as conditioning proceeds. [^rl-p22]

**Shaping** (Skinner): starting with easily-achieved rewards and gradually moving toward the target reward signal; an essential technique in animal training and computational RL for sparse reward problems. [^rl-p30]

### Neuroscience (Ch. 15)

**Dopamine / TD error correspondence** (Schultz, Dayan, Montague 1997): phasic activity of dopamine neurons in the basal ganglia matches the TD prediction error δ. Before conditioning, dopamine fires at reward; after, dopamine fires at the earliest reward-predicting stimulus; at reward omission, dopamine dips below baseline. This correspondence was discovered computationally — TD learning developed years before these neuroscience experiments were conducted. [^rl-p25]

The **neural actor-critic** interpretation: the actor (policy) maps to frontal cortex/striatum; the critic (value) maps to the ventral striatum/nucleus accumbens; dopamine delivers δ as a teaching signal to both. The anatomy and physiology of the mammalian brain fits actor-critic algorithms particularly well. [^rl-p25]

Discrepancies exist: when reward arrives earlier than expected, dopamine neuron activity does not show the negative TD error predicted at the original expected time. Addressed by microstimulus representations (Ludvig, Sutton, Kehoe 2008) which fit better than complete serial compound (CSC) representations. [^rl-p25]

### Applications (Ch. 16)

- **TD-Gammon** (Tesauro 1992/1995): backgammon at world-class level via self-play TD(λ) + neural net; ≈10²⁰ states; prefigures deep RL
- **Watson's Daily-Double wagering** (IBM Jeopardy! 2011): RL for optimal bet sizing
- **Atari DQN** (DeepMind 2015): human-level video game play from raw pixels via Q-learning + CNN
- **AlphaGo / AlphaGo Zero** (Silver et al. 2016/2017): MCTS + policy/value neural networks; AlphaGo Zero learns entirely from self-play without human data

### Frontiers (Ch. 17)

**General Value Functions (GVFs)** and **option framework** (Sutton et al.): temporally extended actions (options) with intra-option policies and termination conditions enable planning and learning at multiple timescales. GVFs generalize value functions to arbitrary prediction targets (not just discounted cumulative reward), supporting off-policy simultaneous learning of many predictions. [^rl-p30]

**Reward design** (Ch. 17.4): intrinsically motivated RL — reward signals sensitive to internal factors (motivational states, learning progress) enable an agent to control its own cognitive architecture. Inverse reinforcement learning recovers the expert's reward signal from behavior; bilevel optimization (analogous to evolution acting on the RL agent's reward signal) can yield reward functions better than intuitive hand-design. [^rl-p30]

**Remaining frontier issues** (Ch. 17.5): (1) sample efficiency gap vs. human learning; (2) representation learning (where do state/feature representations come from?); (3) hierarchical RL; (4) model-based vs. model-free integration; (5) reward design and goal specification; (6) multi-agent / multi-task learning. [^rl-p30]

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
[^rl-p12]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-12.md — Ch. 8.4–8.7: Prioritized sweeping; expected vs. sample updates; trajectory sampling; RTDP
[^rl-p13]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-13.md — Ch. 8.8–8.11: Decision-time planning; heuristic search; rollout algorithms; Monte Carlo Tree Search
[^rl-p14]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-14.md — Ch. 9: On-policy prediction with approximation; SGD; state aggregation; 1000-state random walk example
[^rl-p15]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-15.md — Ch. 9.5: Feature construction; tile coding; radial basis functions; hashing
[^rl-p16]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-16.md — Ch. 9 continued; linear methods; LSTD; convergence near VE optimum
[^rl-p17]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-17.md — Ch. 10: On-policy control with approximation; episodic semi-gradient Sarsa; mountain car example; average reward
[^rl-p18]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-18.md — Ch. 11.5: Bellman error minimization; residual-gradient algorithm; A-presplit counterexample; BE vs. VE failure modes
[^rl-p19]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-19.md — Ch. 11: Off-policy methods with approximation; gradient-TD methods (GTD2, TDC); convergence proofs
[^rl-p20]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-20.md — Ch. 11 continued; emphatic-TD; importance sampling for off-policy approximation
[^rl-p21]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-21.md — Ch. 12: Eligibility traces; λ-return; TD(λ); True Online TD(λ); Sarsa(λ); forward/backward view equivalence
[^rl-p22]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-22.md — Ch. 14: Psychology; Rescorla-Wagner model; blocking; TD model of classical conditioning; trial-level vs. real-time representations
[^rl-p23]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-23.md — Ch. 13: Policy gradient methods; REINFORCE; actor-critic; softmax for continuous actions; policy gradient theorem
[^rl-p24]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-24.md — Ch. 14 continued; TD model of classical conditioning extended; within-trial temporal dynamics; CSC representation
[^rl-p25]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-25.md — Ch. 15: Neuroscience; dopamine/TD error correspondence; Schultz-Dayan-Montague 1997; early-reward discrepancy; neural actor-critic
[^rl-p26]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-26.md — Ch. 15 continued; neural actor-critic architecture; reward prediction error hypothesis; basal ganglia circuitry
[^rl-p27]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-27.md — Ch. 16: Applications; TD-Gammon; Watson; Atari DQN; AlphaGo / AlphaGo Zero; MCTS + neural net integration
[^rl-p28]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-28.md — Ch. 16 continued; AlphaGo Zero self-play training details; policy/value network architecture
[^rl-p29]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-29.md — Ch. 17: Frontiers; temporal abstraction; options framework; General Value Functions (GVFs); multi-step predictions
[^rl-p30]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-30.md — Ch. 17.4–17.5: Reward design; shaping; imitation learning; inverse RL; bilevel optimization; remaining frontier issues
[^rl-p31]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-31.md — Ch. 17 continued; intrinsically motivated RL; multi-agent issues; future directions
[^rl-p32]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-32.md — References (A–W); complete bibliography
[^rl-p33]: raw/_inbox/pdf-reinforcement-learning-an-introduction-part-33.md — References (W–Z) and Index
