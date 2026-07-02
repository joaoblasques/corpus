---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/how-llms-actually-work.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/web/web-elastic-expert-parallelism-in-vllm-e7f766b6.md
    channel: web
    ingested_at: 2026-07-02
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

## Expert parallelism: static vs. elastic (vLLM)

At serving time, MoE models are typically distributed via **expert parallelism (EP)** — experts are spread across GPUs and tokens are dispatched only to the GPUs holding their selected experts, rather than sharding each expert. Wide-EP deployments (EP spanning many workers) maximize KV-cache capacity for high-concurrency or long-context workloads such as RL rollouts and multiturn agentic conversations [^src2].

In [[ai-engineering/vllm|vLLM]], EP was historically **static**: capacity was fixed at deployment start, and adapting to demand required a slow full restart that could drop traffic. **Elastic Expert Parallelism (Elastic EP)** changes this by letting vLLM resize its data-parallel (DP) worker count at runtime — which resizes the shared EP group and redistributes experts accordingly — via a single `POST /scale_elastic_ep` call, with minimal interruption to serving [^src2].

- Scaling is implemented as a coordinated state machine: new ranks join via *standby* communication groups (independent of the active ones) while the old topology keeps serving; a synchronized *switch* then promotes standby to active (releasing/re-warming CUDA graphs and `torch.compile` state); an EPLB (expert-parallel load-balancer) reshuffle moves the actual expert weights onto the new layout [^src2].
- Scale-**down** reshuffles experts off departing ranks *before* removing them, since those ranks may still own expert weights that need to migrate first [^src2].
- This runtime-reconfiguration path is described as a **core building block for fault tolerance**: recovering from a failed rank uses the same scale-down (remove + redistribute) → scale-up (add replacement capacity) sequence, without restarting the whole deployment [^src2]. An alternate EP communication backend, **NIXL EP**, makes this incremental (`connect_ranks()`/`disconnect_ranks()`) and adds EP-side failure detection [^src2].
- Current implementation is scoped to `tensor_parallel_size=1`, one API server, no DBO/MoE-drafter support yet, and depends on the Ray DP backend [^src2].

See [[ai-engineering/vllm|vLLM]] for the fuller Elastic EP write-up (scale-up/scale-down flow detail, cross-rank barrier coordination) and [[ai-engineering/vllm-semantic-router|vLLM Semantic Router]] for routing decisions that sit in front of MoE serving capacity like this.

## See also

- [[ai-engineering/transformer|Transformer]] — MoE replaces the dense feed-forward network inside transformer layers
- [[ai-engineering/llm|LLM]] — MoE is a scaling strategy for the parameter count of modern LLMs
- [[ai-engineering/claude-models|Claude Model Lineup]] — frontier model families where dense-vs-MoE is a live architectural choice
- [[ai-engineering/vllm|vLLM]] — serving engine with expert-parallel, Elastic EP runtime scaling, and quantized MoE execution backends
- [[ai-engineering/minimax-m3|MiniMax M3]] — MXFP8-quantized MoE model with day-0 vLLM support
- [[ai-engineering/vime|vime]] — RL post-training framework with MoE-specific train-inference alignment (R3 routing replay)

---

[^src1]: [How LLMs Actually Work](../../raw/web/how-llms-actually-work.md)
[^src2]: [Elastic Expert Parallelism in vLLM](../../raw/web/web-elastic-expert-parallelism-in-vllm-e7f766b6.md) — vLLM blog, 2026-05-14
