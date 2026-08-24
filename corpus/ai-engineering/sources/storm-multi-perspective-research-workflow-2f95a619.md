---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-how-to-build-a-multi-perspective-ai-research-workflow-using-2f95a619.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - STORM method
  - STORM multi-agent research
  - Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking
  - Stanford NLP STORM
  - multi-perspective AI research
  - expert persona research
  - Domain Expert persona
  - Skeptic persona
  - Practitioner persona
  - Newcomer persona
  - persona friction
  - pre-writing writing phases
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
confidence: 0.8
last_confirmed: 2026-08-24
---

# STORM: Multi-Perspective AI Research Workflow

**TL;DR**: STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking) is a Stanford NLP Group method that assigns five distinct expert personas to interrogate a topic from different angles before synthesis. In controlled evaluations, STORM-generated outlines scored ~25% better on organization quality than single-prompt or standard RAG approaches [^src1].

## Core insight

Single-prompt AI research produces one perspective — one framing, one set of assumptions, one voice. Real research comes from a conversation between experts with different backgrounds, priorities, and blind spots. When a Wikipedia editor writes a comprehensive article, they implicitly represent multiple stakeholder viewpoints; STORM replicates that process using AI agents [^src1].

The key mechanism is **deliberate friction between perspectives**: when a skeptic and an advocate both ask questions about the same topic, the gaps between their questions reveal things a single agent would never think to look for [^src1].

## Two phases

1. **Pre-writing** — multiple expert personas generate questions, gather information, and synthesize into a shared outline
2. **Writing** — a synthesis agent uses the outline and gathered information to produce a coherent document

The intermediate outline step — where a dedicated agent builds structured output from all persona questions and retrieved content — is what separates STORM from a multi-prompt approach. Skipping it degrades output significantly [^src1].

## The five expert personas

Each persona generates 5–10 questions independently before seeing the other personas' questions. Independent generation is essential — allowing later personas to see earlier output collapses the multi-perspective benefit [^src1].

### Domain Expert
Asks precise, technical questions; understands established literature; pushes for accuracy; identifies what is already known and fills foundational knowledge gaps [^src1].

Prompt framing: "You are a specialist with deep expertise in [topic]. Your job is to identify the most important facts, definitions, and established knowledge. Ask questions that a subject matter expert would find meaningful."

### Skeptic
Questions assumptions, looks for counterevidence, challenges consensus views. The skeptic is what separates STORM from simple summarization — it actively looks for what might be wrong, overstated, or contested [^src1].

Prompt framing: "You are a critical analyst reviewing this topic. Identify claims that may be exaggerated, contested, or missing important nuance. Ask questions that surface limitations, risks, and counterarguments."

### Practitioner
Cares about real-world application — how it is actually used, what common implementation failures are, what works in practice vs theory [^src1].

Prompt framing: "You are a professional who regularly works with [topic]. Your questions focus on practical application, implementation challenges, and what experienced practitioners know that textbooks don't cover."

### Journalist (narrative/context)
Brings narrative instinct — asks about context, history, key players, and "so what." Ensures final output is readable, not just accurate [^src1].

Prompt framing: "You are an investigative journalist covering this topic. Ask questions that reveal surprising facts, historical context, key figures, and the human story behind the subject."

### Newcomer
Asks questions experts forget to answer — identifies jargon needing unpacking, conceptual leaps needing bridging, foundational knowledge assumed but not stated. Without a newcomer persona, research outputs typically have accessibility gaps [^src1].

Prompt framing: "You are someone encountering this topic for the first time. Ask questions that uncover basic definitions, common misconceptions, and the foundational concepts needed to understand the subject."

## Six-step workflow

1. **Initialize topic brief** — define research scope, target audience, depth, constraints, output format; passed to every persona as shared context
2. **Persona question generation** — each persona independently generates 5–10 questions
3. **Information retrieval** — persona questions drive retrieval (web search or document store); results tagged by persona
4. **Perspective synthesis** — synthesis agent reviews all persona questions and retrieved content, produces a structured outline
5. **Full draft generation** — writing agent uses outline and source material to produce the document
6. **Quality review** (optional) — review agent or human editor checks internal consistency, tone, sourcing

## Key implementation principles

**Grounded personas with constraints** [^src1]: each persona prompt should define:
- What they care about (goal)
- What they are skeptical of (bias)
- What they will ignore (blind spot)
- Required output format

Vague personas produce vague questions. "You are a skeptic" is too broad; "You are a risk analyst whose job is to identify failure modes, skeptical of claims lacking empirical backing, generating 8 questions that probe risks and limitations" is useful.

**Cross-examination layer** (optional but effective) [^src1]: after question generation, show each persona the other personas' questions and ask them to identify gaps or challenge framing. Produces a second synthesis layer.

**Temperature and model selection** [^src1]: the skeptic benefits from higher temperature (more unexpected angles); the domain expert benefits from lower temperature (precision). Mixing models per persona (stronger reasoning models for skeptic, faster models for initial generation) can balance cost and quality.

## Common failure modes

**Persona collapse** [^src1]: multiple personas produce nearly identical questions. Causes: topic brief too narrow, persona prompts too similar, model defaulting to "safe" framing. Fix: add explicit contrast language — "Do NOT ask questions a domain expert would ask."

**Collapsing the workflow** [^src1]: asking one agent to "pretend to be all five personas." The personas must generate questions independently before seeing each other's output — otherwise later personas are influenced by earlier ones.

**Skipping the outline step** [^src1]: jumping from question generation to final writing loses the synthesis that structures the content from multiple perspectives into a coherent whole.

**Identical source material across personas** [^src1]: if all personas draw from the same search results, the multi-perspective structure produces diversity in framing but not content. Let different personas run different queries where possible.

**Over-engineering** [^src1]: five personas is the practical default. Beyond five, returns diminish — more cost and latency for marginal gain. If output seems one-dimensional at five personas, the issue is usually persona prompt quality, not persona count.

## When to use STORM

**Use when** [^src1]:
- Topic is complex enough that different expertise levels surface meaningfully different information
- Research must hold up to scrutiny from multiple audiences
- Output needs to be both accurate and accessible
- Audience has diverse backgrounds

**Skip when** [^src1]:
- Need a quick factual answer (single well-engineered prompt with RAG is faster and cheaper)
- Topic is narrow and well-defined enough that all perspectives converge quickly
- Speed matters more than depth
- Audience is highly homogeneous

**Cost estimate** [^src1]: a typical STORM run — five personas, 8 questions each, retrieval, synthesis — uses ~10,000–30,000 tokens total; at mid-tier API pricing roughly $0.05–$0.30 per research run.

## STORM vs functional decomposition

STORM's distinguishing feature is **perspective decomposition** rather than functional decomposition. Frameworks like CrewAI or task-delegation patterns break work into functional subtasks (research agent, writing agent). STORM breaks work into perspective subtasks — the same task is approached from multiple viewpoints before synthesis [^src1].

This makes STORM particularly effective for topics where a single "correct" framing does not exist. For tasks with a clear linear solution path, functional decomposition is often more efficient [^src1].

## See also

- [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) — STORM is a five-persona fan-out followed by synthesis, which maps to the fan-out/fan-in pattern in the orchestration taxonomy
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — STORM-generated outlines were validated with human raters; the 25% improvement claim is from a controlled evaluation against standard RAG baselines

---

[^src1]: [How to Build a Multi-Perspective AI Research Workflow Using the STORM Method](../../../raw/web/web-how-to-build-a-multi-perspective-ai-research-workflow-using-2f95a619.md) — MindStudio blog, collected 2026-07-01; Stanford NLP STORM, five expert personas, six-step workflow, failure modes, cost estimates
