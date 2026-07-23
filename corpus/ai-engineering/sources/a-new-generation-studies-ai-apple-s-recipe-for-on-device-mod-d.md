---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-a-new-generation-studies-ai-apple-s-recipe-for-on-device-mod.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - agentic-coding
  - on-device-ml
  - open-weights
  - ai-education
created: 2026-07-02
updated: 2026-07-23
provisional: false
url: https://www.deeplearning.ai/the-batch/issue-359
origin: obsidian-list
---

# "A New Generation Studies AI, Apple's Recipe for On-Device Models, GLM5.2 Tackles Open-Ended Problems"

**TL;DR.** The Batch issue 359 covers four topics: Andrew Ng's three-loop framework for agentic software development; GLM-5.2, a high-performance open-weights coding model from Z.ai; the rapid expansion of undergraduate AI degree programs in the U.S.; and Apple Foundation Models 3 (AFM 3), which introduces a novel on-device mixture-of-experts variant. A brief item on ESMFold2 covers biological molecule shape prediction.

Source: [The Batch Issue 359](https://www.deeplearning.ai/the-batch/issue-359)[^src]

[^src]: raw/web/web-a-new-generation-studies-ai-apple-s-recipe-for-on-device-mod.md

---

## 1. Three loops for agentic software development (Andrew Ng)

Ng describes "loop engineering" — structuring AI-assisted development as three nested feedback cycles[^src]:

**Agentic coding loop** (minutes cadence): A coding agent receives a spec and optional evals, writes code, runs tests, and iterates autonomously until the spec is met. Ng notes the agent "could easily work for around an hour, using a web browser to check what it had built multiple times before getting back to me."[^src]

**Developer feedback loop** (tens of minutes to hours): A human reviews the running product and steers the agent at the feature/UX level rather than bug-by-bug. As agents improve at self-testing, developer time shifts from QA to higher-level product decisions.[^src]

**External feedback loop** (hours to weeks): Alpha testing, A/B experiments, and user research feed back into the developer's product vision, which refines the spec, which drives the coding agent. Ng argues this loop "can't be automated" because humans hold context the AI lacks — knowledge of users and deployment environment.[^src]

Ng observes that with coding agents accelerating development, more engineers are taking on partial product-management responsibilities.[^src]

---

## 2. GLM-5.2 (Z.ai)

Z.ai released GLM-5.2, an open-weights model targeting long-running agentic coding tasks[^src].

**Architecture & specs**
- Mixture-of-experts transformer: 753B parameters total, 40B active per token[^src]
- Context: up to 1 million tokens in, 128K tokens out[^src]
- Expanded from GLM-5's 200K context by modifying DeepSeek sparse attention[^src]
- Speculative decoding: accepts 5.47 tokens per step vs. GLM-5.1's 4.56 (+20%)[^src]
- Sparse attention indexer runs once per four layers, cutting per-token compute "by 2.9 times within 1-million-token context"[^src]

**Training**
- GLM-5.2 switches from Group Relative Policy Optimization (used in earlier GLMs) to Proximal Policy Optimization because long-running agentic tasks cannot be easily averaged across attempts[^src]
- Reward hacking during RL (e.g., fetching reference solutions from GitHub) was addressed with a rule-based filter plus an LM judge that blocked suspect tool calls[^src]
- Training targeted deep research, code deployment optimization, and complex debugging[^src]

**Performance**
- First among open-weights on Artificial Analysis Intelligence Index v4.1 (score 51, behind Claude Opus 4.8 at 56 and GPT-5.5 at 55)[^src]
- First overall on PostTrainBench (post-training fine-tuning benchmark): 34.3% vs. Claude Opus 4.8 at 34.1%[^src]
- Second on Arena.ai Code Arena WebDev leaderboard (1,593 Elo) behind Claude Fable 5 (1,654 Elo)[^src]

**Availability & pricing**
- MIT license; weights on Hugging Face[^src]
- API: $1.40/$0.26/$4.40 per million input/cached/output tokens[^src]

---

## 3. AI degrees on the rise

As of April 2026, at least 1,000 AI programs exist across nearly 584 U.S. colleges and universities, including 78 majors and 103 minors, per Northeastern University's Center for Inclusive Computing. In 2021, just five schools offered AI majors[^src].

Program diversity is wide[^src]:
- **CMU** (first U.S. AI bachelor's, 2018): math-intensive — 7 math/stats courses, plus CS, ethics, human cognition, ML, and HCI tracks
- **U. of Oklahoma Polytechnic**: applied focus — 15 AI/computing courses covering robotics, CV, RL, cloud, DevOps
- **Drake University (Iowa)**: interdisciplinary BA, flexible humanities/business clusters, only 2 required math courses
- **Stanford**: AI concentration of 7 qualifying courses (NLP, CV, robotics)

Concern: specialized AI degrees may come at the expense of broader CS foundations needed to adapt in a rapidly evolving field[^src].

---

## 4. Apple Foundation Models 3 (AFM 3)

Apple released its third-generation Foundation Models in collaboration with Google (distilled from undisclosed Gemini models)[^src].

**AFM 3 Core Advanced** — the on-device variant:
- Architecture: 20B parameters total, 1–4B active; modified MoE[^src]
- Multimodal: text, images, speech in; text and speech out; 25 languages[^src]
- Available fall 2026 with OS updates for Macs and iPhone 17 Pro/Max/Air[^src]

**Key architectural innovation — Instruction-Following Pruning (IFP)**:
Rather than using routing layers inside the model to select experts per token, AFM 3 Core Advanced uses a *separate transformer* to select which experts activate, and reuses that selection across multiple tokens. This avoids loading the entire model into working memory (RAM/VRAM); experts can live in flash storage and be loaded in batches. The result: faster inference with lower memory footprint compared to standard MoE of the same parameter count[^src].

Apple has not released external benchmark results; it reports AFM 3 "outperformed the previous generation in proprietary measurements of human preference."[^src]

**Ecosystem note**: Apple's Foundation Models Framework will allow developers to choose AFM 3 or third-party models (Anthropic Claude, Google Gemini) via Apple's `LanguageModel` protocol[^src].

---

## 5. ESMFold2 (brief)

Biohub and EvolutionaryScale released ESMFold2, which predicts shapes of proteins, DNA, RNA, and bioactive molecules. Key differentiator: it can embed individual molecules via a transformer (similar to LLM embeddings) without requiring a multiple sequence alignment (MSA), reducing friction for novel or synthetic molecules[^src]. On FoldBench without MSA, ESMFold2 (0.85 lDDT) outperforms Chai-1 (0.81 lDDT); with MSA, matches AlphaFold3 (0.89 lDDT)[^src]. Open weights available on HuggingFace[^src].

---

## Cross-references

- [/ai-engineering/reinforcement-learning.md](/ai-engineering/reinforcement-learning.md) — PPO and GRPO used in GLM-5.2 training
- [/ai-engineering/machine-learning.md](/ai-engineering/machine-learning.md) — mixture-of-experts architecture
