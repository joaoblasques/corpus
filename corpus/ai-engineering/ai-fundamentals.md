---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - AI fundamentals
  - artificial intelligence
  - classical AI
  - GOFAI
  - search algorithms
  - constraint satisfaction
  - types of AI
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# AI Fundamentals (Classical & Modern)

**TL;DR**: Artificial intelligence is the broad field of getting computers to do things that appear intelligent — searching for solutions, representing knowledge, reasoning under uncertainty, optimizing, and learning from data [^src1]. Modern LLMs sit at one end of a much older tree whose classical branches (search, logic, constraint satisfaction, probabilistic reasoning) still underpin how agents plan and reason [^src1]. This page is the foundational scaffold; deeper branches live in [Machine Learning](/ai-engineering/machine-learning.md), [Neural Networks](/ai-engineering/neural-network.md), [LLM](/ai-engineering/llm.md), and [Transformer](/ai-engineering/transformer.md).

## The scope of the field

CS50's AI curriculum frames the field as six progressive areas: **search** (find a solution path), **knowledge** (represent facts and draw inferences), **uncertainty** (reason with probabilities), **optimization** (find the best among many solutions), **learning** (improve from data and experience), and **neural networks + language** (modern statistical AI) [^src1]. "Anytime you see a computer do something that appears to be intelligent or rational — recognizing a face, playing a game better than people, understanding language — these are all examples of AI" [^src1].

Historically the field is older than the hype: the term *artificial intelligence* was coined by John McCarthy at the **1956 Dartmouth Conference**; Alan Turing's 1950 **Turing test** (a machine passes if its conversation is indistinguishable from a human's) was the first serious proposal in AI's philosophy [^src2]. Milestones cited: ELIZA chatbot (1961), IBM **Deep Blue** beating Garry Kasparov at chess (1997), Stanley winning the DARPA Grand Challenge (2005), IBM **Watson** winning Jeopardy (2011) [^src2].

## Search

A *search problem* has an initial state, actions, a transition model, a goal test, and a path cost; the agent searches for a path from start to goal [^src1]. Examples: 15-puzzle, maze solving, driving directions, game moves [^src1]. Uninformed vs informed strategies:

| Strategy | Idea |
|---|---|
| **Depth-first (DFS)** | Explore deepest frontier node first (stack); may not find shortest path |
| **Breadth-first (BFS)** | Explore shallowest frontier node first (queue); finds shortest path, costs memory |
| **Greedy best-first** | Expand the node a *heuristic* estimates is closest to goal |
| **A\*** | Expand on `cost-so-far + heuristic`; optimal when the heuristic is admissible (never overestimates) |

**Adversarial search** handles two-player games: **Minimax** assigns values to terminal states and assumes each player optimizes their own outcome; **alpha-beta pruning** discards branches that cannot affect the result; depth-limiting with an evaluation function makes large games tractable [^src1].

## Knowledge & logic

A *knowledge-based agent* represents facts in a **knowledge base** and uses **inference** to derive new conclusions [^src1]. Propositional logic + **model checking** (enumerate possible worlds, check entailment) and inference rules let the agent prove what *must* be true given what it knows [^src1]. This is the symbolic ("GOFAI") tradition that complements the statistical one.

## Uncertainty

When facts are only probable, AI uses probability theory — **Bayesian networks** model conditional dependence among variables, and **Markov models / Markov chains** model state sequences where the next state depends only on the current one [^src1]. (The probability machinery itself — distributions, Bayes' theorem, expectation — is in [Statistics & Probability for ML](/ai-engineering/statistics-for-ml.md).)

## Optimization

Finding the best solution under constraints: local search (hill-climbing, simulated annealing), linear programming, and **constraint satisfaction problems (CSPs)** — variables, domains, and constraints, solved with backtracking and arc-consistency (e.g. Sudoku, scheduling, map coloring) [^src1].

## Types of AI (capability framing)

A common taxonomy distinguishes **Artificial Narrow Intelligence** (task-specific, all systems today), **Artificial General Intelligence** (human-level across domains — see [AGI](/ai-engineering/agi.md)), and **Artificial Super Intelligence** (beyond human) [^src2]. AI is the umbrella; **machine learning** is the subset that learns from data; **deep learning** is the subset of ML using multi-layer neural networks [^src2].

## The 10 concepts that bridge classical AI to LLM engineering

A practitioner's reduction of "what every AI engineer should know in 2026" maps the classical scaffold onto the LLM stack [^src3]: **LLMs**, **tokens & context windows**, **AI agents**, **MCP**, **RAG**, **fine-tuning**, **context engineering**, **reasoning models**, **multimodal AI**, and **mixture of experts** [^src3]. Two framings worth keeping: *"if you're a software engineer in 2026 and you don't understand what an LLM is, it's like being a web developer in 2010 who doesn't know what an API is"* and *"the engineers who master context engineering are the ones companies are really wanting to hire"* [^src3]. Each maps to a corpus page below.

## See also

- [Machine Learning](/ai-engineering/machine-learning.md) — the learning-from-data branch (supervised/unsupervised/RL)
- [Neural Networks](/ai-engineering/neural-network.md) — perceptrons, backprop, CNN/RNN
- [Statistics & Probability for ML](/ai-engineering/statistics-for-ml.md) — the probability and inference substrate
- [LLM](/ai-engineering/llm.md) · [Transformer](/ai-engineering/transformer.md) — the modern statistical-AI core
- [AI Agent](/ai-engineering/ai-agent.md) — search + reasoning realized as an LLM agent loop
- [Learning AI Engineering](/ai-engineering/learning-ai-engineering.md) — how to learn this stack
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Harvard CS50's AI with Python (full course)](../../raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md) — Brian Yu, [02:44](../../raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md#t=2:44)
[^src2]: [Artificial Intelligence Full Course](../../raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md) — Edureka, [02:25](../../raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md#t=2:25)
[^src3]: [AI was HARD until I Learned these 10 Concepts](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md) — Maddy Zhang
