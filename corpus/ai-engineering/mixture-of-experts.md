---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/how-llms-actually-work.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - Mixture of Experts
  - MoE
  - mixture-of-experts
  - experts
  - router network
  - sparse model
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Mixture of Experts (MoE)

**TL;DR**: An architectural variant where a transformer layer's single dense feed-forward network is replaced by **many parallel expert FFNs plus a tiny router** that picks which experts process each token. Total parameter count grows substantially, but compute per token stays low because only a few experts run — the standard way to scale parameter count without scaling inference cost in proportion [^src1].

## How it works

Some modern frontier models replace the dense [[ai-engineering/transformer|Transformer]] FFN with MoE. Instead of one feed-forward network per layer, the model has many parallel FFNs (the **experts**) and a tiny **router network** that picks which experts process each token [^src1].

> Mixture of Experts means the model has several feed-forward networks and routes each token through only a few of them. [^src1]

The router activates only a small subset of experts per token, so:

- **Total parameter count goes up substantially** — more stored capacity [^src1].
- **Compute per token grows much more slowly** — only the few activated experts run [^src1].

This is what lets a model keep growing its parameter count without making inference cost grow in proportion [^src1].

## Mixtral 8x7B (worked example)

- **8 experts per layer; only 2 activated** for any given token [^src1].
- **46.7 billion total parameters**, but only **~12.9 billion used per token** [^src1].

This sparse-activation pattern has become a common option for very large models [^src1].

## Where it fits

MoE is one of the choices that defines a model's **configuration** (alongside layer count, head count, dense-vs-MoE), distinct from the trained weights and post-training [^src1]. It is part of the converged 2023–2025 "modern transformer" stack — appearing in some of the largest models — that would have looked exotic five years earlier [^src1].

## See also

- [[ai-engineering/transformer|Transformer]] — MoE replaces the dense feed-forward network inside transformer layers
- [[ai-engineering/llm|LLM]] — MoE is a scaling strategy for the parameter count of modern LLMs
- [[ai-engineering/claude-models|Claude Model Lineup]] — frontier model families where dense-vs-MoE is a live architectural choice
- [[ai-engineering/vllm|vLLM]] — serving engine with expert-parallel and quantized MoE execution backends
- [[ai-engineering/minimax-m3|MiniMax M3]] — MXFP8-quantized MoE model with day-0 vLLM support
- [[ai-engineering/vime|vime]] — RL post-training framework with MoE-specific train-inference alignment (R3 routing replay)

---

[^src1]: [How LLMs Actually Work](../../raw/web/how-llms-actually-work.md)
