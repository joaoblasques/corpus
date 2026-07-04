---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-fbd141be.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-6c5a69ff.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-cba19f6e.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - llama.cpp
  - llama-cpp
  - ggml
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-04
updated: 2026-07-04
---

# llama.cpp

**TL;DR.** llama.cpp is the reference C/C++ inference implementation for GGUF-quantized language models — the engine underneath [Ollama](/ai-engineering/ollama.md) and [LM Studio](/ai-engineering/lm-studio.md) [^src1]. Building from source gives maximum control over backend acceleration and quantization schemes; it tends to be the fastest path on Apple Silicon [^src1].

## When to use llama.cpp directly

> "Use the upstream binaries when you want the latest performance work (recent releases are often weeks ahead of distribution packages), when you need a quantization scheme that downstream wrappers do not expose, or when you want to script a high-throughput inference workflow without an extra daemon. Casual chat needs do not justify the build step; Ollama exists for that." [^src1]

## GGUF quantization guide

GGUF is llama.cpp's model format. Quantization rewrites 16-bit weights into fewer bits [^src2]:

- **Q4_K_M** — good default: 4-bit weights, K-quant (slightly higher quality), Medium variant. Fits ~5 GB for 8B models.
- **Q5_K_M** — higher quality, ~6 GB for 8B. Best balance for Apple Silicon with headroom.
- **Q8_0** — 8-bit; near-lossless for most tasks; requires more RAM but perplexity close to F16.
- **Q2_K** — very small; noticeable quality loss; use only when RAM is the hard constraint.
- **IQ-prefixed (IQ3_XS, IQ4_XS etc.)** — imatrix-based importance quantization; better quality-per-bit than pure K-quants on code and math tasks [^src2].

"Most users pick one almost at random, run with it for months, and never compare." [^src2]

**Practical decision rule**: start at Q4_K_M; step up to Q5_K_M if you have 20–30% more RAM than the Q4 size; step up to Q8_0 if you prioritize quality and RAM is not a constraint; only step down to Q2/Q3 when fitting the model in RAM is the hard requirement [^src2].

## Apple Silicon vs. NVIDIA

Apple Silicon has **unified memory** — CPU, GPU, and neural engine share one pool. An M3 Ultra with 192 GB can run a 70B model at Q5_K_M fully on-GPU [^src3]. Discrete-GPU (NVIDIA) requires the model to fit in VRAM for full speed; spilling to system RAM incurs substantial latency penalty [^src3].

On raw token throughput per dollar, NVIDIA datacenter cards win; Apple Silicon wins on total working-set per dollar and silence/heat [^src3].

## Related

- [Ollama](/ai-engineering/ollama.md) — built on llama.cpp; wraps it with model management and an OpenAI-compatible API
- [LM Studio](/ai-engineering/lm-studio.md) — uses llama.cpp underneath; adds GUI, model browser, side-by-side evaluation
- [LocalAI](/ai-engineering/localai.md) — LocalAI's `llama.cpp` backend for GGUF models
- [Quantization](/ai-engineering/quantization.md) — broader quantization concepts (NVFP4, INT8 etc.)
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Build and run llama.cpp from source](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-fbd141be.md) — RunLocal blog, 2026-05
[^src2]: [Choosing a GGUF quantization without lying to yourself](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-6c5a69ff.md) — RunLocal blog, 2026-05
[^src3]: [Apple Silicon or NVIDIA for local LLMs in 2026](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-cba19f6e.md) — RunLocal blog, 2026-05
