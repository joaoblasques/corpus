---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - DiffusionGemma
  - diffusion language model
  - dLLM
  - diffusion LLM
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# DiffusionGemma

**TL;DR.** DiffusionGemma is Google's 26B-parameter **discrete diffusion language model (dLLM)** built on the Gemma4 backbone — the first dLLM natively supported in [vLLM](/ai-engineering/vllm.md). Unlike autoregressive transformers that generate one token at a time left-to-right, it generates tokens by iteratively denoising a fixed-length 256-token canvas, refining many tokens in parallel per forward pass [^src1].

## Why it's architecturally different

Standard decoder LLMs are causal-attention, one-token-at-a-time. DiffusionGemma instead:

- Denoises a **256-token canvas** at a time, trading memory-bandwidth pressure for extra compute — attractive at low batch sizes where spare compute is plentiful and bandwidth is the bottleneck.
- Uses the **same Gemma4 backbone weights in two modes**: an **encoder mode** (causal attention, writes to KV cache — used for prefill and to "commit" a finished block) and a **decoder mode** (bidirectional attention, reads-only KV cache — the denoising mode, where every canvas position attends to every other position) [^src1].
- Generation is left-to-right **across blocks** (each new block conditions on all previously committed tokens) but parallel **within a block** (all 256 positions denoise simultaneously) [^src1].

## Sampling loop

1. Prompt prefilled in encoder mode.
2. Canvas initialized to random tokens; state set to denoising.
3. Each denoising step runs the backbone in decoder mode, samples a candidate token at every position, and decides which positions to "keep" (accept) vs. discard and re-randomize.
4. Once the canvas stops changing, a final encoder pass commits it (writes KV, emits the 256 tokens), and the next block starts fresh.

### Entropy-bound denoising
Confidence per position is measured by the entropy of its predicted token distribution. Each step walks positions from most-confident to least, **accepting tokens until accumulated entropy exceeds a fixed budget**; the rest are discarded and re-randomized for the next step. Convergence: the argmax prediction stops changing for a couple of consecutive steps and mean entropy falls below threshold, or a hard step-limit is hit — the committed tokens are the clean argmax prediction, not the noisy sampled canvas [^src1].

### Self-conditioning
Between steps the model is conditioned on its **own previous prediction**: the full softmax distribution (not hard tokens) from the previous step is converted into a probability-weighted average of token embeddings and added, via a small gated MLP, onto the canvas embeddings before the next pass. Active only in decoder/denoise mode; zeroed on encoder prefill/commit passes [^src1].

## vLLM implementation

- Built on [vLLM](/ai-engineering/vllm.md)'s **`ModelState` abstraction** (model runner v2) — see [vLLM](/ai-engineering/vllm.md) for the general hook mechanism.
- **Reuses vLLM's speculative decoding data path**: each denoising step's canvas is treated as a large set of draft tokens that are fully accepted or fully rejected together, requiring minimal changes to the scheduler/model runner. Support for sampling 0 tokens (vs. speculative decoding's usual "always sample one bonus token") was added, controlled by `ModelState` [^src1].
- **Automatic prefix caching works unmodified** — because the encoder mode uses ordinary causal attention and writes KV exactly as an autoregressive model would, shared prompt prefixes are reused across requests with no diffusion-specific changes [^src1].
- **Dynamic per-sequence causal attention**: previously, causality was a batch-wide property in vLLM (every request in a forward pass shared the same mask type). DiffusionGemma requires per-request causal (encoder) vs. bidirectional (denoise) masks within the *same* batched forward pass — implemented in both Triton Attention and FlashAttention 4 backends by replacing the single boolean `causal` argument with a per-request tensor [^src1].
- **Sliding-window attention** made symmetric for canvas tokens: a causal request keeps a one-sided window (self + W tokens before), while a denoising canvas token attends to W tokens on *both* sides (total window 2W+1) [^src1].

## Quantized checkpoints

FP8 (dynamic activations) and NVFP4 (weights + activations) checkpoints created via LLM Compressor, published on RedHatAI's Hugging Face hub, validated on AIME 2025, GPQA Diamond, and GSM8k [^src1].

## Performance

Benchmarked at batch size 1 (`vllm bench serve`): the FP8 model reaches **1,288 generation tokens/sec on H200** (~6× a standard autoregressive baseline, ~3× a multi-token-prediction baseline) and **1,008 tok/s on H100** (~5× and ~2.6× respectively) — DiffusionGemma's architecture is aimed specifically at low-latency interactive use [^src1].

## Related

- [vLLM](/ai-engineering/vllm.md) — serving engine; `ModelState` abstraction introduced for this integration
- [Transformer](/ai-engineering/transformer.md) — the Gemma4 backbone DiffusionGemma reuses, run in two attention modes
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [DiffusionGemma: The First Diffusion LLM (dLLM) Natively Supported in vLLM](../../raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md) — vLLM blog, 2026-06-10
