---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - MiniMax M3
  - MiniMax-M3
  - MiniMax Sparse Attention
  - MSA
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# MiniMax M3

**TL;DR.** MiniMax M3 is a model family (BF16 and MXFP8 checkpoints) built for million-token-context, native multimodal reasoning, coding/agentic workflows, and controllable thinking behavior. Its core architectural change is **MiniMax Sparse Attention (MSA)** — a hybrid dense/sparse attention design that makes 1M-token context practical to serve [^src1]. [[ai-engineering/vllm|vLLM]] shipped day-0 serving support for it.

## MiniMax Sparse Attention (MSA)

Instead of every query attending densely over the full KV cache, MSA uses an index path to score fixed **128-token KV blocks** and selects only the top-scoring blocks per query/GQA-group for the real attention computation [^src1]:

1. **Score** candidate KV blocks with a small index head.
2. **Select** top blocks (learned top-k scoring combined with configured block rules — the current recipe uses `init_blocks=0`, `local_blocks=1`, i.e. a deterministic local window plus indexer-scored top-k for the rest).
3. **Run** online-softmax attention over only the selected blocks.

This bounds per-token attention work regardless of total context length, which is what makes the 1M-token window practical to serve rather than just theoretically supported [^src1].

## Support matrix (vLLM day-0)

| Capability | vLLM support |
|---|---|
| 1M-token context | `--max-model-len`, block-size 128 recipes, prefix caching, chunked prefill, MSA kernels |
| MSA | Hybrid attention backend, indexer-score kernels, top-k block selection, sparse GQA prefill/decode |
| MXFP8 weights | DeepGEMM MXFP8 MoE backend (Blackwell-class), Marlin MXFP8 (Hopper-class) |
| Native multimodality | Model-specific multimodal preprocessing path |
| Tool/reasoning outputs | `minimax_m3` tool parser, `minimax_m3` reasoning parser, `thinking_mode` chat-template control |
| EAGLE3 speculative decoding | Day-0 recipe with draft model `Inferact/MiniMax-M3-EAGLE3` |

MXFP8 describes only weight/MoE execution — it does **not** mean the KV cache is MXFP8; KV-cache dtype is validated as a separate roadmap item [^src1].

## Deployment knobs that matter

- `--block-size 128` — aligns vLLM cache blocks with MSA's sparse block granularity.
- `--tensor-parallel-size` / `--enable-expert-parallel` — split attention, projections, and MoE experts across GPUs.
- NVIDIA: MSA on default attention backend; vision encoder on FlashInfer (`--mm-encoder-attn-backend FLASHINFER`). Verified on H200, GB200, B300.
- AMD ROCm: MSA on Triton (`--attention-backend TRITON_ATTN`); vision encoder on AITER FlashAttention (`--mm-encoder-attn-backend ROCM_AITER_FA`). Verified on MI350 and MI300 series.

## Validation results (B300 snapshot)

| Dimension | Result |
|---|---|
| GSM8K strict / flexible accuracy | 91.51% / 91.66% |
| ShareGPT @256 throughput | 8,530 tok/s |
| ShareGPT @256 TPOT | 56.0 ms |
| Speculative Sonnet TPOT (concurrency 1/16/64) | 4.51 / 9.04 / 14.36 ms |
| Speculative acceptance on Sonnet | ~67%, mean accept length ~3.0 |

These are engineering-validation numbers, not an official benchmark ranking [^src1].

## RL post-training

MiniMax M3 also has day-0 GRPO (Group Relative Policy Optimization) post-training support in NVIDIA NeMo RL, using vLLM as a non-colocated generation/rollout backend — the same serving work that enables inference also drives RL rollouts [^src1].

## Related

- [[ai-engineering/vllm|vLLM]] — serving engine providing day-0 support
- [[ai-engineering/mixture-of-experts|Mixture of Experts]] — M3's MXFP8 MoE execution path
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning](../../raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md) — vLLM blog, 2026-06-12
