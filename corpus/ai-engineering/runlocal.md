---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-dcdb413d.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-99927538.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-94e161ca.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-2f012a92.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-a4e37e78.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-caad93c2.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-ac4596df.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-a5000279.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-fbd141be.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-2a373f8f.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-6c5a69ff.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-cba19f6e.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - RunLocal
  - runlocal.blog
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-04
updated: 2026-07-04
---

# RunLocal

**TL;DR.** RunLocal (runlocal.blog) is an independent editorial site covering open-weight LLM deployment on consumer hardware — guides for [Ollama](/ai-engineering/ollama.md), [LM Studio](/ai-engineering/lm-studio.md), [llama.cpp](/ai-engineering/llama-cpp.md); model/tool comparisons; GGUF quantization guidance; Apple Silicon vs. NVIDIA hardware analysis; and a local model picker [^src1]. Content is aimed at readers who already understand the basics and want the part the announcement omitted [^src2].

## Coverage areas

- **Model picker** — filterable by task, hardware, license, size [^src1]
- **Tool directory** — Ollama, LM Studio, llama.cpp, and other runtimes with strengths/weaknesses [^src3]
- **Install guides** — step-by-step for Ollama (beginner, ~10 min), LM Studio (beginner, ~12 min), llama.cpp (intermediate, ~20 min, source build) [^src4]
- **Blog** — long-form: GGUF quantization explained, Apple Silicon vs NVIDIA comparison [^src2]
- **Glossary** — plain-English definitions of local AI terms [^src5]
- **OpenSUSE/SUSE coverage** — SUSE's enterprise AI stack on top of Rancher Prime [^src6]

## Key guides

### Ollama guide (beginner)
"The fastest way to get a local LLM running with one command." RAM-to-model-size rule of thumb: 8B ≈ 5 GB (Q4), 14B ≈ 9 GB, 32B ≈ 20 GB, 70B ≈ 42 GB [^src4]. Apple Silicon uses unified memory; NVIDIA setups need the model to fit in VRAM for full speed, otherwise spill to RAM with substantial latency penalty.

### LM Studio guide (beginner)
"The most polished desktop client for running open weights on your machine." Niche: evaluate several models against the same prompts side-by-side before committing. Ollama is faster for one-shot chat; vLLM is for concurrent-user production serving; LM Studio sits in between for evaluation [^src7].

### llama.cpp guide (intermediate)
Build from source for latest performance work (often weeks ahead of distribution packages), non-standard quantization schemes, or high-throughput scripted inference without a daemon [^src8]. See [llama.cpp](/ai-engineering/llama-cpp.md).

### GGUF quantization guide
Default recommendation: Q4_K_M. Step up to Q5_K_M if RAM allows; Q8_0 for near-lossless quality. IQ-prefixed variants (importance-based quantization) offer better quality-per-bit for code and math [^src9]. See [llama.cpp](/ai-engineering/llama-cpp.md) for full guide.

### Apple Silicon vs. NVIDIA (2026)
Apple Silicon wins on total working-set per dollar and silence/heat; NVIDIA wins on raw tokens-per-second-per-dollar at datacenter scale. The M3 Ultra at 192 GB unified memory can load a 70B model at Q5_K_M fully on-GPU [^src10].

## Related

- [Ollama](/ai-engineering/ollama.md) — primary runtime covered
- [LM Studio](/ai-engineering/lm-studio.md) — desktop client covered
- [llama.cpp](/ai-engineering/llama-cpp.md) — engine underlying most tools
- [Quantization](/ai-engineering/quantization.md) — GGUF quantization
- [Local AI Agents](/ai-engineering/local-ai-agents.md) — running local agents on this hardware
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [RunLocal — Local AI on your own hardware (picker)](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-dcdb413d.md) — runlocal.blog
[^src2]: [RunLocal — Local AI on your own hardware (blog)](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-caad93c2.md) — runlocal.blog
[^src3]: [RunLocal — Local AI on your own hardware (tools)](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-94e161ca.md) — runlocal.blog
[^src4]: [RunLocal — Local AI on your own hardware (guides)](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-2f012a92.md) — runlocal.blog
[^src5]: [RunLocal — Local AI on your own hardware (glossary)](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-ac4596df.md) — runlocal.blog
[^src6]: [RunLocal — Local AI on your own hardware (openSUSE)](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-a4e37e78.md) — runlocal.blog
[^src7]: [LM Studio setup and side-by-side model evaluation](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-2a373f8f.md) — RunLocal, 2026-05
[^src8]: [Build and run llama.cpp from source](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-fbd141be.md) — RunLocal, 2026-05
[^src9]: [Choosing a GGUF quantization without lying to yourself](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-6c5a69ff.md) — RunLocal, 2026-05
[^src10]: [Apple Silicon or NVIDIA for local LLMs in 2026](../../raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-cba19f6e.md) — RunLocal, 2026-05
