---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-dario-amodei-the-urgency-of-interpretability.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/github/github-labmlai-inspectus.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - interpretability
  - mechanistic interpretability
  - superposition
  - sparse autoencoders
  - SAE
  - circuits
  - features
  - MRI for AI
  - attention visualization
  - Inspectus
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-23
updated: 2026-06-25
---

# Interpretability

**TL;DR**: Mechanistic interpretability is the program to understand how neural networks compute — decomposing model weights into human-readable "features" and tracing how they combine into "circuits" that implement specific behaviors. Dario Amodei's 2026 essay argues this is "the most urgent priority in AI safety research," with a goal of producing an "MRI for AI" by 2027 [^src1].

## The problem: opaque reasoning

LLMs are black boxes — they accept inputs, produce outputs, and "we cannot peer inside" to understand the reasoning [^src1]. This matters for safety: we want AI to reason correctly, be honest, and have good values, but currently have no reliable way to verify this from the inside. Interpretability is the research program to change that.

## Superposition: how models store knowledge

The core mystery: networks store more concepts than they have neurons, via overlapping representations [^src1]. A single neuron participates in multiple concepts simultaneously, with different patterns of activation mapping to different meanings. Brute-force searches ("find the dishonesty neuron") don't work; a more principled decomposition is needed.

## Sparse autoencoders: finding features

Key empirical breakthrough: **sparse autoencoders (SAEs)** applied to Claude 3 Sonnet discovered approximately **30 million distinct features** [^src1]. An SAE is trained to reconstruct the model's activations from a much smaller set of active directions at any given moment — the "sparse" constraint forces it to find the natural atomic units the model uses.

These features are interpretable: they activate for specific concepts, tokens, or patterns — proper nouns, programming constructs, emotional valence, abstract concepts like "deception" [^src1].

## Circuits: how features combine

Features combine into **circuits** — specific computation patterns where certain features systematically activate others [^src1]. Example: "Dallas" feature → "Texas state" feature → "Austin (capital)" feature, tracing how the model reasons about US city-state relationships.

Circuits are where behavior becomes auditable: you can trace the computational pathway and verify it's reasoning correctly rather than pattern-matching.

## The 2027 goal: "MRI for AI"

> "Our goal is to have a system that can look inside a model and tell you, with confidence, whether it is reasoning correctly, being honest, or pursuing certain goals — the way an MRI can tell you what's happening in a brain." [^src1]

Target: by 2027, interpretability tools capable of auditing a model's reasoning for a given decision with sufficient resolution to catch misaligned values or deceptive reasoning before deployment.

## The race condition

"There is a race between interpretability research and model capability" [^src1]. As models get more capable, their internal representations become more complex and harder to interpret. If capabilities advance faster than interpretability, we'll deploy increasingly capable models with decreasing insight into what they're actually doing.

Amodei's argument: "The right response is to fund interpretability to run faster, not to slow down capabilities research." The goal isn't parity — it's a meaningful lead for interpretability over capability so there's always audit coverage for deployed model generations.

## Three policy actions

Beyond research, Amodei advocates [^src1]:
1. **Accelerate interpretability research** — fund it as a core safety priority, not a nice-to-have.
2. **Light-touch transparency legislation** — require model developers to publish interpretability audits before frontier deployments; optional disclosure for current generation, mandatory for next.
3. **Export controls on chips to China** — prevent training frontier models without the interpretability infrastructure to audit them.

## Inspectus: LLM analytics visualization tool

**Inspectus** (labmlai/inspectus, 714★) is a Python library for visualizing LLM internals — attention mechanisms, token distributions, and weight statistics — in Jupyter notebooks [^src2]:

```python
pip install inspectus
import inspectus
inspectus.attention(attn, tokens)  # 2-4D tensor or HuggingFace attentions
```

**Three visualization types** [^src2]:

| Type | What it shows | Use case |
|---|---|---|
| **Attention visualization** | Attention matrix, query/key token heatmaps, dimension heatmap across layers/heads | Understanding which tokens a model attends to; debugging attention patterns |
| **Token visualization** | Per-token metrics (loss, entropy) with multiple metric support and dropdown selector | Identifying high-loss tokens, entropy profiles, training signal distribution |
| **Distribution plot** | Statistical distribution of arbitrary series data with configurable percentile bands | Identifying outliers in training losses (e.g. MNIST training) |

**Attention visualization components** [^src2]:
- **Attention Matrix** — pairwise attention scores between all token pairs; interactive (click to filter by query or key token)
- **Query Token Heatmap** — sum of attention from each query to selected key tokens
- **Key Token Heatmap** — sum of attention to each key from selected query tokens
- **Dimension Heatmap** — attention scores normalized across layers and heads

Works with HuggingFace transformers (pass `output_attentions=True`) and custom attention maps (NumPy arrays). The interactive interface is rendered natively in Jupyter; no external server required.

Inspectus is in the "practitioner tool for attention debugging" category rather than the "mechanistic interpretability research" category. Where sparse autoencoders and circuits are research tools for understanding *what features models compute*, Inspectus is a diagnostic tool for understanding *which tokens models attend to* during inference — useful for debugging attention patterns in fine-tuned or deployed models.

## See also

- [Anthropic](/ai-engineering/anthropic.md) — the lab conducting this research; Dario Amodei is co-founder and CEO
- [LLM](/ai-engineering/llm.md) — the subject of interpretation; neural networks being decoded
- [Agent Security](/ai-engineering/agent-security.md) — safety audit tools are the intended downstream application

---

[^src1]: [Dario Amodei: The Urgency of Interpretability](../../raw/web/web-dario-amodei-the-urgency-of-interpretability.md) — Dario Amodei, Anthropic
[^src2]: [labmlai/inspectus — LLM Analytics](../../raw/github/github-labmlai-inspectus.md) — labmlai, GitHub ★714
