---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-model-routing-choosing-the-right-model-for-the-job.md
    channel: notes
    ingested_at: 2026-07-14
aliases:
  - model routing
  - dynamic model selection
tags:
  - corpus/ai-engineering
  - source
  - model-routing
  - cost-optimization
  - inference
created: 2026-07-14
updated: 2026-08-10
provisional: false
url: https://www.linkedin.com/pulse/7-ai-terms-youll-hear-lot-this-year-alex-wang
origin: obsidian
---

# Model Routing — Choosing the Right Model for the Job

**TL;DR:** Model routing dynamically selects which AI model handles a given task rather than relying on a single model for everything — the primary lever for balancing cost, latency, and quality in production AI systems.

**Source:** Alex Wang, "7 AI Terms You'll Hear a Lot This Year" (LinkedIn Pulse) [^wang2026]

---

## Definition

Model routing is "the practice of dynamically selecting which AI model should handle a task, instead of relying on a single model for everything." [^wang2026]

---

## Why It Matters

Early AI applications commonly depended on one model, but that approach "quickly becomes expensive and inefficient." [^wang2026] Different tasks require different capabilities, and not every request needs the most powerful — or most expensive — model. Routing allows a system to match model capability to task demand across three dimensions:

- **Cost** — cheaper, smaller models handle simpler requests
- **Latency** — faster models serve time-sensitive tasks
- **Quality** — more capable models are reserved for complex or high-stakes tasks

---

## Key Tools and Platforms

Two platforms are cited as concrete implementations:

- **OpenRouter** — routes requests between models from different providers
- **Perplexity** — dynamically selects models depending on the query [^wang2026]

The source notes that many production AI products already run "multiple models behind the scenes, with routing logic deciding which one handles each request." [^wang2026]

---

## Trajectory

The source characterizes model routing as a directional shift: "single-model architectures are giving way to multi-model systems," and routing is expected to "become a standard pattern in production AI." [^wang2026]

---

## Corpus relations

- [Agent Cost Management](/ai-engineering/agent-cost-management.md) — routing is one concrete lever for the cost control discussed there; picking a cheaper model per task is the same tradeoff viewed from the spend side
- [vLLM Semantic Router](/ai-engineering/vllm-semantic-router.md) — a concrete implementation of the routing pattern this source describes
- ["7 AI Terms You'll Hear a Lot This Year" (Alex Wang)](/ai-engineering/seven-ai-terms-2026-alex-wang.md) — shared-provenance synthesis: this page and siblings all derive from the same article and do not corroborate each other
- [AI Engineering hub](/ai-engineering/README.md)

---

[^wang2026]: Alex Wang, "7 AI Terms You'll Hear a Lot This Year," LinkedIn Pulse, 2026. Source file: `raw/notes/notes-03-resources-articles-model-routing-choosing-the-right-model-for-the-job.md`.
