---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-announcing-day-0-support-for-nvidia-nemotron-3-ultra-on-vllm-bc7c306b.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - Nemotron 3 Ultra
  - NVIDIA Nemotron 3 Ultra
  - Nemotron
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# Nemotron 3 Ultra

**TL;DR.** Nemotron 3 Ultra is NVIDIA's open-weight frontier reasoning model, built for long-running autonomous agent workflows (planning, tool calling, error recovery, multi-step orchestration). It combines a hybrid Transformer-Mamba Mixture-of-Experts architecture with multi-token prediction and NVFP4 precision, and shipped with **Day-0 support in [vLLM](/ai-engineering/vllm.md)** [^src1].

## Architecture

- **Mixture of Experts, hybrid Transformer-Mamba** — 550B total parameters, 55B active parameters [^src1].
- **Context length**: up to 1M tokens [^src1].
- **Modalities**: text input, text output [^src1].
- **Mamba layers** improve sequence efficiency for long-context workloads; **Transformer layers** preserve precise recall when agents need to retrieve specific facts from large context windows [^src1].
- **Latent MoE** — supports more efficient expert routing across reasoning, code generation, tool calls, and domain-specific logic [^src1].
- **Multi-Token Prediction (MTP)** — predicts multiple future tokens per forward pass, reducing generation time for long outputs and multi-turn workflows [^src1].
- **NVFP4 precision** — the same NVFP4 checkpoint runs on both NVIDIA Hopper and Blackwell GPUs via specialized quantization kernels, letting one checkpoint serve both architectures [^src1]. See [Quantization](/ai-engineering/quantization.md).

## Training and role in vLLM's own development loop

Nemotron 3 Ultra was **post-trained with multi-environment reinforcement learning** for reasoning and agentic behavior, using NVIDIA NeMo RL and Gym across many agent harnesses — not just single-turn chat [^src1]. Notably, vLLM itself was part of the training and evaluation loop: within NeMo RL, vLLM served as the generation backend for RL rollouts (efficient sampling, scalable inference, integration with NeMo Gym for multi-step/multi-turn training environments), and vLLM also powered the evaluation loop used to track training progress [^src1].

## Deployment

| Precision | Supported GPUs |
|---|---|
| BF16 | 8x GB200/B200/GB300/B300, 16x H100, 8x H200 |
| NVFP4 | 4x GB200/B200/GB300/B300, 8x H100 |

Served through vLLM with an OpenAI-compatible API; open weights, open data, and open recipes for customization [^src1].

## Benchmarked positioning

Per NVIDIA/vLLM's own reported figures (vLLM config: 10k/2k ISL/OSL, batch size 1), Nemotron 3 Ultra leads other open models on agentic benchmarks (agent productivity, coding, instruction following) and sits in the leading-accuracy/leading-throughput quadrant, claiming up to 30% cost savings vs. other leading open models [^src1]. These are vendor-reported numbers, not independently verified.

## Related

- [vLLM](/ai-engineering/vllm.md) — serving engine providing Day-0 support; also used as Nemotron 3 Ultra's RL rollout/eval backend
- [Quantization](/ai-engineering/quantization.md) — NVFP4 precision path
- [Mixture of Experts](/ai-engineering/mixture-of-experts.md) — Latent MoE routing
- [MiniMax M3](/ai-engineering/minimax-m3.md) — another day-0 vLLM model with a hybrid long-context attention design
- [Olmo](/ai-engineering/olmo.md) — Ai2's matched transformer/hybrid model pair; token-level study of where hybrid (attention+recurrent) architectures beat pure attention
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Announcing Day-0 Support for NVIDIA Nemotron 3 Ultra on vLLM](../../raw/web/web-announcing-day-0-support-for-nvidia-nemotron-3-ultra-on-vllm-bc7c306b.md) — vLLM blog, 2026-06-04
