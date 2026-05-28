---
type: concept
domain: ai-engineering
status: stub
sources:
  - path: 03_Resources/Study Notes/AI - How Large Language Models Work.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - Transformer
  - transformer architecture
  - attention mechanism
  - self-attention
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
---

# Transformer

**TL;DR**: The neural network architecture (Google, 2017) underlying all modern LLMs. Enables parallel processing of entire sequences via attention — each token attends to every other token to update its meaning in context [^src1].

## Processing steps

1. **Embedding** — each token → dense vector encoding its meaning
2. **Attention** — all embeddings interact; each updates based on context (e.g., "bank" shifts meaning based on surrounding words like "river" vs "account") [^src1]
3. **Feedforward layer** — per-position neural network; stores additional language patterns
4. **Repeat** — stack many layers; final vector → probability distribution over vocabulary

## Why it matters

Pre-Transformer architectures (RNNs, LSTMs) processed sequences token-by-token, preventing parallelization. The Transformer processes the full sequence in parallel, enabling GPU-scale training on internet-sized corpora [^src1].

Behavior is emergent — the architecture defines the framework; the billions of weights determine what the model actually does [^src1].

## See also

- [[ai-engineering/llm|LLM]] — the Transformer is the architecture underlying all modern LLMs
- [[ai-engineering/context-engineering|Context Engineering]] — attention is what makes context-window structure matter; tokens attend across the full window

---

[^src1]: [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]]
