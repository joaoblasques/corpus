---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - vLLM
  - vllm
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# vLLM

**TL;DR.** vLLM is an open-source LLM inference-serving engine and ecosystem. Beyond the core serving runtime (scheduler, paged KV cache, prefix caching, chunked prefill, speculative decoding), the vLLM project has grown a family of adjacent tools: [[ai-engineering/vllm-semantic-router|vLLM Semantic Router]] for request-level model routing, and [[ai-engineering/vime|vime]] for RL post-training. vLLM ships day-0 support for major new model architectures, including sparse-attention long-context models ([[ai-engineering/minimax-m3|MiniMax M3]]) and diffusion language models ([[ai-engineering/diffusiongemma|DiffusionGemma]]) [^src1][^src2][^src3].

## Serving engine internals (as exercised by day-0 model integrations)

- **Scheduler + paged KV cache** — manages per-request cache blocks; extended via hooks (e.g. `ModelState`) rather than forked for new model architectures [^src2].
- **Prefix caching** — reuses cached KV for shared prompt prefixes across requests [^src1][^src2].
- **Chunked prefill** — splits very long prompts into chunks so one giant prefill doesn't monopolize the engine [^src1].
- **Speculative decoding data path** — a mature subsystem (draft tokens proposed, verified in a batch, accepted/rejected) that other features can be built on top of. [[ai-engineering/diffusiongemma|DiffusionGemma]]'s diffusion denoising loop reuses this path by treating each denoising step's canvas as a set of draft tokens that are fully accepted or rejected together [^src2]. [[ai-engineering/minimax-m3|MiniMax M3]] uses EAGLE3 speculative decoding for latency reduction [^src1].
- **Tensor/expert parallelism (TP/EP)** — splits attention, projections, and MoE experts across GPUs [^src1].
- **Multi-backend hardware support** — NVIDIA (H100/H200/GB200/B300), AMD ROCm (MI300/MI350), with backend-specific attention kernel selection (e.g. FlashAttention/FlashInfer on NVIDIA vs. Triton/AITER on AMD) [^src1][^src2].

## ModelState abstraction (model runner v2)

Introduced to support [[ai-engineering/diffusiongemma|DiffusionGemma]], `ModelState` lets a model define custom input preparation and per-request state without forking the model runner [^src2]:

| Hook | Purpose |
|---|---|
| `prepare_inputs()` | Build/modify per-request input embeddings (e.g. apply self-conditioning) |
| `prepare_attn()` | Set per-request attention metadata (e.g. causal vs. bidirectional) |
| `custom_sampler()` | Swap in a model-specific sampler |
| `add_request()`/`remove_request()` | Initialize/tear down per-request custom state |

A model self-registers its `ModelState` via `get_model_state_cls()` on the model class — no changes to the shared scheduler, model runner, or other infrastructure are required. The vLLM team frames this as a blueprint for adding future non-autoregressive architectures (e.g. more diffusion LLMs) [^src2].

## Day-0 model support pattern

vLLM's "day-0" releases pair a new open-weight model with same-day serving support, including: architecture-specific attention kernels, tool-call/reasoning-output parsers, speculative decoding draft models, quantized checkpoint validation, and deployment recipes across accelerators. Both [[ai-engineering/minimax-m3|MiniMax M3]] (sparse attention, 1M-token context) and [[ai-engineering/diffusiongemma|DiffusionGemma]] (diffusion decoding) required non-trivial engine extensions rather than being drop-in autoregressive models [^src1][^src2].

## Ecosystem projects

- [[ai-engineering/vllm-semantic-router|vLLM Semantic Router]] — request routing control plane (signals → decisions → model selection) sitting in front of vLLM and other backends.
- [[ai-engineering/vime|vime]] — RL post-training framework pairing Megatron training with vLLM as the rollout/inference backend.

## Related

- [[ai-engineering/mixture-of-experts|Mixture of Experts]] — MoE execution is a first-class vLLM serving concern (expert parallelism, quantized MoE backends)
- [[ai-engineering/ollama|Ollama]] — contrasting local-first single-user serving tool vs. vLLM's production/datacenter serving focus
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning](../../raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md) — vLLM blog, 2026-06-12
[^src2]: [DiffusionGemma: The First Diffusion LLM (dLLM) Natively Supported in vLLM](../../raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md) — vLLM blog, 2026-06-10
[^src3]: [Announcing vime: A Simple, Stable, and Efficient RL Framework for LLMs](../../raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md) — vLLM blog, 2026-06-09
