---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-01.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-02.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-03.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-04.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-05.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-06.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-07.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-08.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-09.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-10.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-11.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-12.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-13.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-patterns-predictions-and-actions-a-story-about-mac-part-14.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - Patterns Predictions and Actions
  - Hardt Recht
  - mlstory
  - PPA
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-23
updated: 2026-07-23
---

# Patterns, Predictions, and Actions: A Story about Machine Learning

**TL;DR**: A graduate-level ML textbook by Moritz Hardt and Benjamin Recht (mlstory.org, 2022, 309 pp.) that unifies supervised learning, causality, sequential decision making, and fairness under the lens of 1960s pattern classification. Distinctive for: grounding modern ML in the Duda-Hart lineage; a full causality chapter (structural causal models + potential outcomes); rigorous RL and dynamic programming; and sustained attention to datasets, benchmarks, and social harms.

## Chapter structure

| Ch | Title | Parts | Key content |
|---|---|---|---|
| 1 | Introduction | 1 | Halley's life table (1693); history from perceptron to modern ML; pattern classification as unifying paradigm |
| 2 | Fundamentals of prediction | 2 | Minimum error rule; loss functions; risk; Neyman-Pearson Lemma; ROC curves; three non-discrimination criteria; COMPAS |
| 3 | Supervised learning | 3 | ERM; perceptron; convergence via stability (V&C 1974) |
| 4 | Features | 3–4 | Measurement theory; Belmont Report; quantization; tensors; one-hot; overparameterization; kernel functions; universal approximation |
| 5 | Optimization | 4–5 | Gradient descent; convexity; SGD (1/√T rate); tricks (shuffling, step decay, momentum); implicit regularization; representer theorem |
| 6 | Generalization | 5–6 | Generalization gap; double descent; stability; VC dimension; Rademacher complexity; margin bounds |
| 7 | Deep learning | 6–7 | Layer types; backpropagation; vanishing gradients; residual connections (ResNets); batch/group normalization; Neural Tangent Kernel |
| 8 | Datasets | 7–8 | Train-test paradigm; TIMIT; UCI; Highleyman's data; MNIST; ImageNet; adaptivity problem; leaderboard principle; representational harm; de-anonymization |
| 9 | Causality | 9 | Structural causal models; do-operator; causal graph structures (forks/mediators/colliders); backdoor criterion; potential outcomes |
| 10 | Causal inference in practice | 10–11 | Counterfactuals; RCTs; propensity scores; double ML; heterogeneous treatment effects; quasi-experiments; IV |
| 11 | Sequential decision making | 11 | Dynamical systems; MDPs; dynamic programming; Q-function; Bellman equation; LQR; MPC; partial observation; Kalman filtering |
| 12 | Reinforcement learning | 11–12 | Certainty equivalence; PAC/regret; multi-armed bandits; contextual bandits; Q-learning; policy gradient; REINFORCE; limits of RL in feedback loops |
| 13 | Epilogue | 13 | Window tax (Goodhart's Law); Lucas critique; distribution shift; limits of dynamic modeling; beyond pattern classification |
| 14 | Mathematical background | 13–14 | Notation; positive definite matrices; Taylor's theorem; Jacobians; probability; Bayes' Rule; estimation; Hoeffding's inequality |

## Key claims by section

### Ch1 — Introduction: ML rooted in pattern classification [^ppa-p01]

The book traces modern ML to 1960s **pattern classification** (Rosenblatt's perceptron, 1957; Duda & Hart textbook lineage), not to AI symbolic reasoning. The ML cycle is: propose pattern classes → gather data for each → learn a classifier. Halley's 1693 life table is introduced as the ur-example of prediction-from-data. The text explicitly frames ML as "predictions" (outputs of learned classifiers) coupled to "actions" (decisions taken on those predictions).

> "We named our course and this book after this theme of patterns, predictions, and actions." [^ppa-p01]

### Ch2 — Fundamentals of prediction: Neyman-Pearson and fairness [^ppa-p02]

The **minimum error rule** selects the class with highest posterior probability. **Risk** is expected loss; the **Neyman-Pearson Lemma** proves the likelihood ratio test maximizes TPR at any fixed FPR. ROC curves must be concave and lie above the diagonal; AUC aggregates across all operating points and is treated with skepticism. Three **non-discrimination criteria** (Chouldechova 2017, Kleinberg et al. 2017):

| Criterion | Formal statement | Informal |
|---|---|---|
| Independence | R ⊥ A | Same accept rate across groups |
| Separation | R ⊥ A \| Y | Same TPR/FPR across groups |
| Sufficiency | Y ⊥ A \| R | Same PPV across groups |

These three are mutually incompatible unless base rates are equal (the COMPAS/ProPublica impossibility result). [^ppa-p02]

### Ch3 — Supervised learning: ERM and stability [^ppa-p03]

**Empirical Risk Minimization (ERM)**: find h ∈ H minimizing (1/n) Σ loss(h(xᵢ), yᵢ). The **perceptron** convergence theorem (Novikoff 1962): if data is linearly separable with margin γ and ‖x‖ ≤ R, the perceptron makes at most (R/γ)² mistakes. Generalization via **stability** (Vapnik & Chervonenkis 1974): a learning algorithm that doesn't change much when a single training example changes will generalize. [^ppa-p03]

### Ch4 — Features: measurement and overparameterization [^ppa-p04]

Measurement is theory-laden (Hand 2010; Belmont Report for human subjects). Features include images as tensors, one-hot encoding, template matching, and lifting functions (polynomial features, kernels). **Overparameterized models** (d > n parameters > samples) can interpolate training data exactly and still generalize — the minimum Euclidean norm solution. Kernel functions (polynomial, Gaussian/RBF, arcsine, ReLU) satisfy Mercer's condition. **Universal approximation** (Cybenko 1989): a single hidden layer neural network with enough sigmoidal units approximates any continuous function on a compact set. [^ppa-p04]

### Ch5 — Optimization: SGD as the universal workhorse [^ppa-p05]

**Gradient descent** for convex functions converges at rate O(1/T). **SGD** (stochastic gradient descent) converges at rate O(1/√T) — the standard result. Key tricks: random reshuffling, step-size decay, mini-batching, momentum. **Implicit regularization**: SGD on overparameterized models converges to the minimum Euclidean norm solution, which coincides with the **representer theorem** prediction. The convex function cookbook: (1) non-negative weighted sum of convex functions is convex; (2) composition with affine map is convex; (3) max over convex functions is convex; (4) pointwise limit of convex functions is convex; (5) if f is convex, so is g(x) = f(Ax+b). [^ppa-p05]

### Ch6 — Generalization: double descent and stability bounds [^ppa-p06]

The **generalization gap** = test error − train error. Classical bias-variance picture breaks down with overparameterization: the **double descent** curve shows test error rises at the interpolation threshold (d ≈ n) then falls again as model grows larger. Theories:

- **Algorithmic stability** (Bousquet & Elisseeff 2002): average stability ε implies expected generalization gap ≤ ε. Uniform stability implies high-probability bound.
- **VC dimension** (Vapnik & Chervonenkis): with m ≥ O(VCdim(H)/ε²) samples, ERM achieves ε-generalization.
- **Rademacher complexity**: tighter data-dependent bound.
- **Margin bounds**: ensemble methods (boosting) generalize because margins grow after convergence. [^ppa-p06]

**SGD generalization** (Hardt, Recht, Singer 2016): one-pass SGD with η step size on T examples has uniform stability ≤ 2η·T/n, giving O(η) generalization gap — explaining why early stopping regularizes. [^ppa-p06]

### Ch7 — Deep learning: backpropagation and residual connections [^ppa-p07]

Layer types: fully connected, convolutions, recurrent, attention (self-attention). **Backpropagation** = automatic differentiation via the chain rule on computation graphs. **Vanishing gradients**: gradient magnitude shrinks exponentially with depth in standard deep nets; **residual connections** (He et al. 2016, ResNets) fix this with skip connections x → x + F(x), allowing gradient to flow directly. Normalization: **Batch Normalization** (Ioffe & Szegedy 2015) normalizes per-feature over the batch; **Group Normalization** (Wu & He 2018) normalizes per-group for small batch sizes. **Neural Tangent Kernel** (Jacot et al. 2018): infinite-width networks behave like kernel methods. [^ppa-p07]

### Ch8 — Datasets: benchmarks, harms, and the adaptivity problem [^ppa-p08]

The **train-test paradigm** originated with Bledsoe (1959) for Highleyman's character data. Dataset timeline: Highleyman's data (1959) → UCI Repository (David Aha, 1987) → MNIST (LeCun et al. 1998, 60K train/10K test) → ImageNet/ILSVRC-2012 (Deng et al. 2009, labeled by 49K MTurk workers). The **adaptivity problem**: reusing a test set causes overfitting via leaderboard climbing. Proposition 9/10 (Dwork et al. 2015): an adaptive analyst can overfit a holdout with O(n) queries. The **Ladder algorithm** (Blum & Hardt 2015) enables safe leaderboard reuse. **Model similarity** (Mania et al. 2019): models with similar training accuracy predict similarly under distribution shift — explaining ImageNet accuracy vs. new-test-set linear relationship. Harms: representational harm (Buolamwini & Gebru 2018 — facial analysis disparate accuracy by race/gender), de-anonymization (Netflix Prize — Narayanan & Shmatikov 2008), copyright (Levendowski 2018). Human baselines on ImageNet (5.1% error) are misleading because human labelers used the ImageNet label taxonomy. [^ppa-p08]

### Ch9 — Causality: structural causal models [^ppa-p09]

Motivation via UC Berkeley 1973 admissions (Simpson's paradox). A **structural causal model** consists of assignments Xᵢ = fᵢ(parents(Xᵢ), Uᵢ) for independent noise variables Uᵢ, inducing a **causal graph** (DAG). The **do-operator**: do(X=x) means substituting a constant for X in the SCM, cutting incoming edges — observation ≠ action. Causal graph structures: **forks** (X ← Z → Y, Z is a confounder), **mediators** (X → Z → Y, Z mediates), **colliders** (X → Z ← Y, conditioning on Z opens a spurious path = Berkson's paradox). The **backdoor criterion** (Pearl): a set Z blocks all backdoor paths from X to Y iff Z contains no descendants of X and blocks all paths entering X via an arrow into X. Randomization eliminates confounding by removing incoming edges to the treatment variable. [^ppa-p09]

### Ch10 — Causal inference in practice [^ppa-p10]

**Potential outcomes** framework (Neyman 1923, Rubin 2005): for each unit i, Y₀(i) and Y₁(i) denote outcomes under control/treatment; the individual treatment effect τ(i) = Y₁(i) − Y₀(i) is never observed (fundamental problem). The **average treatment effect** (ATE) is estimable under SUTVA + consistency + ignorability. Counterfactuals in SCMs: three-step abduction → action → prediction. RCTs: odds ratio, risk ratio, vaccine effectiveness. Propensity score e(x) = P(T=1|X=x) — used in **inverse propensity score weighting** to de-confound. **Double machine learning** (partially linear SCM): Y = τT + g(X) + ε; T = m(X) + δ; partial out X effects via ML on Y and T separately, then regress residuals. Heterogeneous treatment effects via **causal forests** (Wager & Athey 2018). Quasi-experiments: **regression discontinuity** (treatment assigned by threshold) and **instrumental variables** (IV; β = Cov(Z,Y)/Cov(Z,T); judge instruments example). Validity caveat: observational causal assumptions are unverifiable from data; interference (SUTVA failures) is endemic in social/online settings. [^ppa-p10]

### Ch11 — Sequential decision making and dynamic programming [^ppa-p11]

A **dynamical system** has state Xₜ, control action Uₜ, noise Wₜ, and reward Rₜ. This is equivalent to a structural equation model. A **Markov Decision Process** (MDP) uses probabilistic transition P[Xₜ₊₁|Xₜ,Uₜ]. Sequential decision making finds policies πₜ(Xₜ) maximizing expected cumulative reward. **Dynamic programming** — the principle of optimality — defines the Q-function recursively via **Bellman's equation**: Qₜ→T(x,u) = E[Rₜ + max_{u'} Q_{t+1→T}(Xₜ₊₁, u')]. Discounted infinite-horizon DP yields time-invariant policy. Tabular MDPs: O(S²A) per Bellman update. **Linear Quadratic Regulator** (LQR): linear dynamics + quadratic cost → optimal policy is linear state feedback K = (B⊤MB)⁻¹B⊤MA; M solves the Discrete Algebraic Riccati Equation. **Model Predictive Control** (MPC): re-solve a finite-horizon open-loop problem at each step, execute first action. **Partial observation** (POMDPs): static output feedback is NP-hard; POMDPs are PSPACE-hard. Practical heuristic: **separation principle** — filter state estimate (Kalman filter for linear Gaussian systems), then solve control as if estimate were exact. [^ppa-p11]

### Ch12 — Reinforcement learning: certainty equivalence and limits [^ppa-p12]

**Certainty equivalence** (Simon 1956, Theil 1957): estimate unknown model parameters, plug them in as if exact. For LQR, certainty-equivalence achieves optimal regret O(√T) (Mania et al. 2019). For tabular MDPs, certainty-equivalence achieves near-optimal sample complexity O(SA/(1−γ)³/ε²). **Multi-armed bandit**: explore-then-commit achieves O(T^{2/3}) gap-independent regret; successive elimination achieves O(√T·log T); UCB achieves O(log T) gap-dependent regret. **Contextual bandits**: reduce to prediction — greedy algorithm achieves sublinear regret when prediction error shrinks. **Approximate Dynamic Programming**: Q-learning (stochastic approximation on Bellman equations); Q-learning with function approximation; SARSA(λ). **Policy gradient / REINFORCE**: log-likelihood trick yields unbiased gradient of expected reward; high variance; deep RL = add neural networks. **Limits**: LQR with marginally stable closed-loop is arbitrarily sensitive to model-error in B. LQG (partially observed LQR + Kalman filter) paradox: better sensing → more fragile to model mismatch. "Improving prediction will increase sensitivity to modeling errors in some other part of the engineering pipeline." [^ppa-p12]

### Ch13 — Epilogue: distribution shift and the limits of prediction [^ppa-p13]

The 1696 **window tax** (King William III) illustrates Goodhart's Law: the tax made window count a target, which broke the wealth correlation. Predictions change populations (the Lucas critique of macroeconomic dynamic modeling). **Distribution shift** degrades even best-performing models. Pattern classification has re-emerged multiple times over 70 years. Stein's 1989 "Respect the Unstable" warning about the gap between mathematical tractability and physical consequences applies directly to RL. The book ends by noting that causality and RL are not panaceas without domain knowledge, and invokes Newton/Halley as an analogy for a future conceptual break from pattern classification. [^ppa-p13]

### Ch14 — Mathematical background [^ppa-p14]

Reference chapter: positive definite/semidefinite matrices; Taylor's theorem (multivariable mean-value form); Jacobians; chain rule. Probability: Bernoulli and Gaussian random vectors; conditional probability; Bayes' Rule; law of iterated expectation. Estimation: plug-in estimators (sample mean, sample covariance, least-squares); Hoeffding's inequality; convergence rate O(d/n) for least-squares (parameter-to-sample ratio governs estimation error, unlike classification bounds which can be dimension-free). [^ppa-p14]

## Unique angles vs. existing corpus

Relative to [Machine Learning](/ai-engineering/machine-learning.md) and [Reinforcement Learning](/ai-engineering/reinforcement-learning.md):

1. **Pattern classification lineage** — explicitly roots modern ML in 1960s Duda & Hart tradition, not the 1980s AI/statistics tradition.
2. **Causality chapter** — most ML textbooks omit or defer causality; this is an integrated structural treatment (SCMs, do-operator, potential outcomes in one arc).
3. **Sequential decision making framing** — RL is presented as the harder sequential extension of prediction, not a separate paradigm.
4. **Datasets as scientific objects** — Ch8 treats dataset curation and benchmark longevity as a scientific practice with formal analysis (adaptivity theorem, Ladder algorithm).
5. **Fairness impossibility** — the three-criterion impossibility result is stated formally and traced to real COMPAS controversy.
6. **LQG fragility paradox** — better estimation → more fragile control; a concrete warning against over-optimizing prediction components independently.

## See also

- [Machine Learning](/ai-engineering/machine-learning.md) — existing concept page; this source deepens ERM, double descent, stability bounds, and fairness
- [Reinforcement Learning](/ai-engineering/reinforcement-learning.md) — existing concept page; this source adds certainty equivalence optimality, LQG fragility, bandit algorithms
- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — SGD convergence and implicit regularization
- [Support Vector Machines](/ai-engineering/support-vector-machines.md) — margin bounds and hinge loss
- [AI History](/ai-engineering/ai-history.md) — perceptron history, Rosenblatt 1957

---

[^ppa-p01]: [Patterns, Predictions, and Actions — Part 1/14 (Introduction, Ch1)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-01.md) — Hardt & Recht, mlstory.org 2022
[^ppa-p02]: [Patterns, Predictions, and Actions — Part 2/14 (Ch2: Fundamentals of prediction)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-02.md)
[^ppa-p03]: [Patterns, Predictions, and Actions — Part 3/14 (Ch3: Supervised learning)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-03.md)
[^ppa-p04]: [Patterns, Predictions, and Actions — Part 4/14 (Ch4: Features)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-04.md)
[^ppa-p05]: [Patterns, Predictions, and Actions — Part 5/14 (Ch5: Optimization)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-05.md)
[^ppa-p06]: [Patterns, Predictions, and Actions — Part 6/14 (Ch6: Generalization)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-06.md)
[^ppa-p07]: [Patterns, Predictions, and Actions — Part 7/14 (Ch7: Deep learning)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-07.md)
[^ppa-p08]: [Patterns, Predictions, and Actions — Part 8/14 (Ch8: Datasets)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-08.md)
[^ppa-p09]: [Patterns, Predictions, and Actions — Part 9/14 (Ch9: Causality)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-09.md)
[^ppa-p10]: [Patterns, Predictions, and Actions — Part 10/14 (Ch10: Causal inference in practice)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-10.md)
[^ppa-p11]: [Patterns, Predictions, and Actions — Part 11/14 (Ch11: Sequential decision making)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-11.md)
[^ppa-p12]: [Patterns, Predictions, and Actions — Part 12/14 (Ch12: Reinforcement learning)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-12.md)
[^ppa-p13]: [Patterns, Predictions, and Actions — Part 13/14 (Ch13: Epilogue + Ch14: Mathematical background)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-13.md)
[^ppa-p14]: [Patterns, Predictions, and Actions — Part 14/14 (Bibliography, index)](../../../raw/pdf/pdf-patterns-predictions-and-actions-a-story-about-mac-part-14.md)
