---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-accelerating-laguna-xs-2-inference-with-vllm-speculators-and-afda11cd.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - Laguna XS.2
  - Laguna
  - Poolside
  - DFlash
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# Laguna XS.2

**TL;DR.** Laguna XS.2 is Poolside's first open-weight model in the Laguna family — a 33B-A3B Mixture-of-Experts model built for agentic coding and long-horizon software tasks. Red Hat AI and Poolside collaborated on serving/inference optimization: first-class [[ai-engineering/vllm|vLLM]] integration, a **DFlash** speculative-decoding draft model, and quantized checkpoints via LLM Compressor [^src1].

## DFlash speculative decoding

DFlash is described as the current state of the art in speculative decoding, moving beyond the Eagle-3 paradigm toward faster, parallel drafting that reduces inter-token latency [^src1].

- **Draft model**: small, 5-layer, 0.6B parameters, trained using the Speculators library.
- **Mechanism**: uses hidden-state inputs from the target Laguna XS.2 model to predict a **block of tokens in a single forward pass** (parallel block drafting, vs. token-by-token autoregressive drafting). Laguna XS.2 then verifies the block with a single pass; this verification step guarantees identical generation quality to running Laguna XS.2 alone [^src1].
- **Result**: predicts 8 tokens per forward pass; when verified, delivers tokens **2–3x faster with no loss in generation quality** [^src1].
- **Training data**: 500k samples from Ultrachat 200k SFT and Magpie-Align, with prompts resampled and responses regenerated from Laguna XS.2 (thinking enabled). Trained 6 epochs, cosine LR schedule, max LR 6e-4, sequence length 8192, 3072 block positions randomly sampled per sequence [^src1].

## Quantized checkpoints

Poolside also released quantized Laguna XS.2 checkpoints built with **LLM Compressor**, in FP8, NVFP4, and INT4/INT8 variants using the compressed-tensors format, for deployment flexibility across hardware/latency/memory constraints [^src1]. See [[ai-engineering/quantization|Quantization]].

## Related

- [[ai-engineering/vllm|vLLM]] — serving engine with first-class Laguna XS.2 integration
- [[ai-engineering/quantization|Quantization]] — LLM Compressor quantized checkpoints (FP8/NVFP4/INT4/INT8)
- [[ai-engineering/mixture-of-experts|Mixture of Experts]] — Laguna XS.2's 33B-A3B MoE architecture
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Accelerating Laguna XS.2 Inference with vLLM, Speculators, and LLM Compressor](../../raw/web/web-accelerating-laguna-xs-2-inference-with-vllm-speculators-and-afda11cd.md) — vLLM blog, 2026-05-28
