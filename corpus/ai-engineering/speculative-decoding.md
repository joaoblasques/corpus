---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-eagle-3-1-advancing-speculative-decoding-through-collaborati-35e12237.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-speculators-v0-5-0-dflash-support-and-online-training-a2b78ff3.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - speculative decoding
  - draft-and-verify decoding
  - Eagle 3
  - Eagle 3.1
  - EAGLE
  - DFlash
  - Speculators
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-02
updated: 2026-07-02
---

# Speculative Decoding

**TL;DR.** Speculative decoding accelerates LLM inference by having a small **draft model** propose several candidate tokens, which the large **target model** then verifies in a single batched forward pass — accepting or rejecting the draft in one step instead of running the target model once per token. **Eagle 3** (autoregressive drafting) and **Eagle 3.1** (a robustness-hardened successor) [^src1], and **DFlash** (single-pass block-diffusion drafting) [^src2] are two families of draft-model algorithms trained via the **Speculators** library and served through [vLLM](/ai-engineering/vllm.md)'s speculative-decoding data path. See [Laguna XS.2](/ai-engineering/laguna-xs2.md) for a production DFlash deployment.

## Eagle 3.1: fixing attention drift

Eagle-family drafters generate draft tokens autoregressively — each new draft token attends back through previously generated draft tokens. In production, this degrades under long-context inputs, unfamiliar chat templates, or out-of-distribution system prompts, a failure mode the EAGLE team calls **attention drift**: as speculation depth increases, the drafter's attention progressively shifts away from sink tokens toward its own generated tokens [^src1].

Two contributing causes were identified [^src1]:

- The fused input representation becomes increasingly imbalanced as higher-layer target hidden states dominate the drafter's input.
- Hidden-state magnitude grows across speculation steps because the residual path is unnormalized.

**Eagle 3.1's fix**: add FC (fully-connected) normalization after each target hidden state and before the FC layer, and feed the **post-norm** hidden states into the next decoding step — making the drafter behave more like a recursively-invoked module across steps rather than a stack of appended layers [^src1].

- Fully backward-compatible with existing Eagle 3 checkpoints — draft models upgrade through the same speculative-decoding code path [^src1].
- **Up to 2x longer acceptance length** vs. Eagle 3 in long-context workloads; better training-to-inference extrapolation; higher resilience to chat-template/system-prompt variation [^src1].
- **Benchmark**: an Eagle 3.1 draft model for Kimi K2.6, trained via **TorchSpec** (a training-efficiency framework for speculative-decoding algorithms) and served on Kimi-K2.6-NVFP4 (vLLM, TP=4, GB200, non-disaggregated) on the SPEED-Bench coding dataset, delivered **2.03x higher per-user output throughput at concurrency 1**, staying meaningful at higher concurrency (1.71x at C=4, 1.66x at C=16) [^src1].
- Merged into vLLM main; ships in vLLM's nightly and the upcoming v0.22.0 release [^src1].
- Joint effort of the EAGLE team, the vLLM team, and the TorchSpec team [^src1].

## DFlash: single-pass block-diffusion drafting

DFlash is architecturally distinct from the Eagle family: instead of autoregressive drafting (multiple forward passes, one token at a time), it uses **block diffusion** to generate an entire block of draft tokens of length *B* in a single forward pass, using a **non-causal attention pattern** — queries within a block can attend to every other token in the same block [^src2]. See [Laguna XS.2](/ai-engineering/laguna-xs2.md) for a concrete deployment (0.6B 5-layer draft model, 8 tokens/pass, 2–3x speedup, no quality loss).

- **Training constraint**: naively starting a prediction block at every sequence position blows up the attention mask (memory + compute infeasible for long sequences). Speculators v0.5.0 instead randomly samples a fixed, smaller set of "anchor" positions (from locations that contribute to the training loss) and attaches predicted blocks only to those anchors — keeping mask size independent of sequence length and letting training scale to long contexts [^src2].
- **Performance**: on Gemma 4, DFlash achieves better inter-token latency than both Eagle 3 and a standalone FP8-quantized verifier; combining DFlash with an FP8-quantized verifier compounds the gain further [^src2].
- **Serving**: DFlash models embed a `speculators_config` in `config.json` (target model, speculative-token count, algorithm name) and integrate with vLLM's existing speculative-decoding infrastructure via `vllm serve`, as of PR #38300 (`vllm>=0.20.0`) [^src2].

## Speculators v0.5.0: unified online/offline training

Speculators v0.5.0 migrated fully onto vLLM's native hidden-states-extraction system (introduced in vLLM v0.18.0), removing the earlier custom data-generation pipeline and vLLM's status as a direct Python dependency of the training pipeline [^src2].

- **Online training**: hidden states are extracted on-the-fly — a vLLM server initializes with the base model, training prompts are sent to it for inference, hidden states are extracted and written to disk/ramdisk, the training process loads and deletes them, and the speculator trains on the extracted states [^src2].
- **Offline training**: hidden states are pre-generated and cached to disk, then trained on later, using the same extraction system and data format as online training — new scripts saturate a running vLLM server with requests and persist the results [^src2].
- The two modes are interoperable: partial offline generation can be combined with online generation of the missing states, and an online run can skip clearing its generated files so a first epoch generates once and subsequent epochs reuse the cached files [^src2].
- Training now talks to vLLM over its standard REST API rather than vLLM internals, decoupling the training framework's release cadence from vLLM's internal API changes [^src2].

## Related

- [vLLM](/ai-engineering/vllm.md) — serving engine hosting the speculative-decoding data path both Eagle and DFlash models run through
- [Laguna XS.2](/ai-engineering/laguna-xs2.md) — Poolside's agentic-coding model with a production DFlash deployment
- [MiniMax M3](/ai-engineering/minimax-m3.md) — uses EAGLE3 speculative decoding for latency reduction
- [Quantization](/ai-engineering/quantization.md) — FP8-quantized verifier models combine with DFlash for compounded latency gains
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [EAGLE 3.1: Advancing Speculative Decoding Through Collaboration Between the EAGLE Team, vLLM, and TorchSpec](../../raw/web/web-eagle-3-1-advancing-speculative-decoding-through-collaborati-35e12237.md) — vLLM blog, 2026-05-26
[^src2]: [Speculators v0.5.0: DFlash Support and Online Training](../../raw/web/web-speculators-v0-5-0-dflash-support-and-online-training-a2b78ff3.md) — vLLM blog, 2026-05-28
