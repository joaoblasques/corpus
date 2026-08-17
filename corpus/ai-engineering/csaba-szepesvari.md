---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-01.md
    channel: pdf
    ingested_at: 2026-07-22
aliases:
  - Csaba Szepesvári
  - Csaba Szepesv´ari
  - Szepesvari
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-22
updated: 2026-08-17
---

# Csaba Szepesvári

ML researcher specializing in reinforcement learning theory. Author of *Algorithms for Reinforcement Learning*, published in the Synthesis Lectures on Artificial Intelligence and Machine Learning series by Morgan & Claypool Publishers (originally June 9, 2009; last updated March 12, 2019). [^rl-p01]

## Work

*Algorithms for Reinforcement Learning* covers the theory and algorithms for RL systems that build on dynamic programming. The book's scope spans:

- **Value prediction**: Temporal difference learning (tabular TD(0), every-visit Monte-Carlo, TD(λ)), function approximation variants, gradient TD learning, and least-squares methods (LSTD). [^rl-p01]
- **Control**: Q-learning in finite MDPs and with function approximation, actor-critic methods, online and active learning in bandits and MDPs. [^rl-p01]
- **Theory**: Convergence analysis grounded in stochastic approximation, two-timescale stochastic approximation, PAC-learning, and bias-variance tradeoff. [^rl-p01]

The abstract states the goal is "to develop efficient learning algorithms, as well as to understand the algorithms' merits and limitations." [^rl-p01]

## Framing of reinforcement learning

The book defines RL as "a learning paradigm concerned with learning to control a system so as to maximize a numerical performance measure that expresses a long-term objective." [^rl-p01] The distinguishing feature from supervised learning is that only partial feedback is given to the learner, and predictions may have long-term effects by influencing the future state of the system. [^rl-p01]

## Related pages

- [/ai-engineering/reinforcement-learning.md](/ai-engineering/reinforcement-learning.md)
- [/ai-engineering/sources/algorithms-for-reinforcement-learning.md](/ai-engineering/sources/algorithms-for-reinforcement-learning.md)

[^rl-p01]: raw/pdf/pdf-algorithms-for-reinforcement-learning-part-01.md — Title page, abstract, and table of contents
