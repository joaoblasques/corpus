---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-designing-synthetic-datasets-for-the-real-world-mechanism-de.md
    channel: web
    ingested_at: 2026-06-17
aliases:
  - synthetic data
  - synthetic data generation
  - Simula
  - mechanism design (data)
  - seedless data generation
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-17
updated: 2026-06-17
---

# Synthetic Data Generation

**TL;DR**: When real-world data is scarce, private, or domain-specific, models can be trained on AI-generated (synthetic) data — but only rigorous, mechanism-design-based approaches produce production-quality datasets. Google's **Simula** framework reframes synthetic generation as *dataset-level* mechanism design: seedless, agentic, and decomposed into independently controllable axes (taxonomy, local diversity, complexity, quality) [^src1].

## Why synthetic data?

Generalist AI models benefit from internet-scale data, but specialized deployment domains — cybersecurity, legal reasoning, on-device models, medical applications — face data scarcity or privacy constraints that make real-world data inaccessible [^src1]. Existing synthetic approaches have three compounding weaknesses [^src1]:

- **Scalability limits** — reliance on seed data or human prompts caps scale.
- **Lack of explainability** — black-box evolutionary algorithms obscure why data looks the way it does.
- **Entangled parameters** — coverage, complexity, and quality are not independently controlled; tuning one contaminates the others.

Most critically, prior methods optimize *one sample at a time* rather than designing the *dataset as a whole* [^src1].

## Simula: dataset-level mechanism design

Google Research's Simula framework treats data generation as a resource-allocation problem at the dataset level — analogous to mechanism design in economics [^src1]. It is **seedless** (no samples from the target distribution are required to start) and **agentic** (generation quality improves automatically as the underlying model's reasoning capability improves) [^src1].

### Four-step pipeline

| Step | What it does |
|---|---|
| **1. Taxonomy construction** | Build a deep, structured taxonomy of the target domain (e.g., attack types in cybersecurity). This defines the coverage space. |
| **2. Local diversification** | Generate "meta-prompts" — scenarios derived from taxonomy nodes — and produce multiple distinct instantiations per scenario. Prevents *mode collapse* where a concept like "SQL injection" gets repeated in near-identical framings [^src1]. |
| **3. Complexification** | Treat difficulty as an orthogonal axis. A configurable fraction of meta-prompts is refined to be harder, allowing practitioners to shift the difficulty distribution without changing semantic coverage [^src1]. |
| **4. Dual-critic quality check** | Two independent critics assess whether each answer is correct, mitigating sycophancy (models agreeing with plausible-but-wrong outputs) and ensuring correct labels without human intervention [^src1]. |

The decomposition is the key design principle: each axis (coverage, complexity, quality) is independently controllable [^src1].

## Evaluation: reasoning-based metrics

Standard embedding-based metrics (cosine distance) give a high-level signal but limited actionable insight [^src1]. Simula introduces reasoning-first evaluation:

- **Taxonomic Coverage** — measures how well the generated dataset covers the taxonomy.
- **Calibrated Complexity Scoring** — uses LLM-driven batch comparisons to assign chess-style Elo ratings to data points, producing a calibrated difficulty distribution [^src1].

Key empirical finding: "there is no single 'optimal' way to generate data, and the relationship between 'good' data and downstream performance is deeply idiosyncratic" [^src1] — meaning evaluation must be domain-aware, not one-size-fits-all.

## Production deployments at Google

Simula serves as the primary synthetic data engine for several production systems [^src1]:

- **Gemma ecosystem** — ShieldGemma (safety), FunctionGemma (tool use), MedGemma (medical); and on-device + server-side Gemini safety classifiers.
- **User protection** — AI-powered scam detection for Android calls; spam filtering in Google Messages.
- **Enterprise security research** — synthesizing realistic attack scenarios to democratize ML for security teams.
- **Map reading** — teaching models to parse maps through structured, reasoning-driven dataset generation.

Distillation setup used in research: Gemini 2.5 Flash as teacher, Gemma-3 4B as student; datasets up to 512K data points across cybersecurity (CTIBench), legal reasoning (LEXam), math (GSM8k), and multilingual knowledge (Global MMLU) [^src1].

## Relationship to training and fine-tuning

Synthetic data is primarily a **training data** tool — it supplements (or replaces) real-world data for fine-tuning or distillation when real data is unavailable. It is orthogonal to [[ai-engineering/rag|RAG]] (which injects retrieved facts at inference time) and to [[ai-engineering/agent-evaluation|Agent Evaluation]] golden datasets (which test trained models, not train them). The Simula paper explicitly positions synthetic data as foundational for "reinforcement learning from AI feedback (RLAIF)" and edge-device distillation [^src1]. See [[ai-engineering/machine-learning|Machine Learning]] §RAG vs fine-tuning for where fine-tuning and distillation fit in the broader training stack.

## See also

- [[ai-engineering/machine-learning|Machine Learning]] — training paradigms; RAG vs fine-tuning trade-off
- [[ai-engineering/llm|LLM]] — pre-training + RLHF; where synthetic data feeds in
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — evaluation methodology for trained models
- [[ai-engineering/rag|RAG]] — inference-time knowledge injection (complementary, not competing)
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Designing synthetic datasets for the real world: Mechanism design and reasoning from first principles](../../raw/web/web-designing-synthetic-datasets-for-the-real-world-mechanism-de.md) — Tim R. Davidson & Hamza Harkous, Google Research, April 2026
