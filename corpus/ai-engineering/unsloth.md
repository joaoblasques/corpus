---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-finetune-gemma-with-unsloth-7508cf36.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-unsloth-fixing-gemma-bugs-83cc4e6a.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-unsloth-gradient-checkpointing-4x-longer-context-windows-41aa4fad.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-finetune-llama-3-with-unsloth-874ddb0c.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-finetune-phi-3-with-unsloth-2e7d3c85.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-finetune-gemma-2-with-unsloth-2a306483.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-finetune-mistral-nemo-with-unsloth-80d57a28.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-finetune-llama-3-1-with-unsloth-4eca0b7c.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-unsloth-x-ycombinator-979219d6.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-fine-tune-llama-3-2-vision-with-unsloth-16376271.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-llama-3-2-vision-fine-tuning-with-unsloth-d41b7f19.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/web/web-qwen-2-5-coder-fine-tuning-with-unsloth-b5ba9d9d.md
    channel: web
    ingested_at: 2026-07-03
aliases:
  - Unsloth
  - unsloth-ai
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-03
---

# Unsloth

**TL;DR.** Unsloth is a fine-tuning toolkit that makes training modern LLMs 2–2.5× faster and uses 50–70% less VRAM than Hugging Face + Flash Attention 2, through custom Triton/CUDA kernels and LoRA optimizations. It supports a wide range of models (Llama, Gemma, Mistral, Phi, Qwen, Llama Vision), works on consumer hardware including free Colab T4 GPUs, and exports trained adapters as GGUF for use in [[ai-engineering/lm-studio|LM Studio]] or llama.cpp. YC-backed; ~2M monthly Hugging Face downloads as of late 2024 [^src10].

## Core approach

Unsloth achieves its speedups through three primary mechanisms:

1. **Optimized kernels**: custom Triton and CUDA kernels rewrite the backward/forward pass for LoRA-patched attention and FFN layers, avoiding redundant memory reads/writes that stock implementations do [^src2].
2. **LoRA-centric fine-tuning**: the toolkit is built around LoRA/QLoRA — it applies optimized low-rank adapters to the target model rather than full fine-tuning, enabling very large models to be trained on single-GPU consumer hardware [^src2].
3. **Custom gradient checkpointing** (added April 2024): Unsloth implemented its own gradient checkpointing instead of using PyTorch's built-in, enabling 4× longer context windows within the same VRAM budget [^src4]. For example, on an A100 the Llama 3 8B context window grew from 7,000 to 48,000 tokens.

## Performance benchmarks by model

All benchmarks are vs. Hugging Face + Flash Attention 2 on comparable hardware [^src1][^src2][^src3][^src5][^src6][^src7][^src8][^src9][^src11][^src12][^src13]:

| Model | Speed improvement | VRAM reduction | Notes |
|---|---|---|---|
| Gemma 7B | 2.43× faster | 57.5% less | A100 40K vs HF's 7K tokens context [^src2] |
| Llama 3 8B | 2× faster | 63% less | A100; 48K vs 7K tokens context [^src5] |
| Llama 3 70B | 1.8× faster | 68% less | A100 [^src5] |
| Phi-3 | similar to above range | similar | split Q/K/V attention matrices fix for better 4-bit quantization accuracy [^src6] |
| Gemma 2 9B | 2× faster | 63.2% less | Collaborated with Gemma team to fix bugs [^src7] |
| Mistral NeMo 12B | competitive | competitive | Runs on free Colab T4 GPU [^src8] |
| Llama 3.1 8B | 2.1× faster | 60% less | 128K context support [^src9] |
| Llama 3.2 Vision (1B/3B/11B) | 2× faster | 60% less | Vision + multimodal fine-tuning [^src11] |
| Llama 3.2 Vision (90B) | 1.5–2× faster | 70% less | 4–8× longer context [^src12] |
| Qwen 2.5 Coder | 2× faster | 60% less | Code-generation model support [^src13] |

## Hardware support

- **NVIDIA**: fully supported (T4 free Colab, A100, consumer cards) [^src1]
- **AMD and Intel GPUs**: supported [^src1]
- **Apple Silicon**: local fine-tuning not yet supported; a separate notebook targets that case [^src1]
- Most model fine-tuning walkthroughs provide ready-made notebooks for both free Colab and local execution [^src2]

## Model-specific workarounds

Unsloth ships Llamafied/patched model versions to handle architecture quirks before fine-tuning [^src6][^src3]:

- **Gemma**: multiple bugs in the original Hugging Face implementation were found and fixed collaboratively (March 2024) [^src3]
- **Phi-3**: the original Phi-3 packs Q/K/V attention matrices together, which degrades 4-bit quantization accuracy; Unsloth Llamafies Phi-3 to split these matrices [^src6]
- **Gemma 2**: collaborated with the Gemma team to fix architecture-specific training issues (2024) [^src7]

## GGUF export workflow

After fine-tuning, Unsloth provides two export paths to GGUF for local inference [^src1]:

1. **Direct GGUF conversion**: `model.save_pretrained_gguf(...)` exports directly at a chosen quantization (Q8_0, F16, BF16).
2. **LoRA merge + convert**: `model.save_pretrained_merged(...)` merges the LoRA adapters into the base model at FP16, then a separate step converts to any quantization level (e.g., Q4_K_M for smaller file sizes).

The exported GGUF is importable into [[ai-engineering/lm-studio|LM Studio]] via `lms import <path/to/model.gguf>` [^src1].

## Company / ecosystem

- **Founders**: Daniel and Michael Han [^src3]
- **Y Combinator**: accepted into YC, announced late 2024 [^src10]
- **Hugging Face downloads**: ~2 million monthly at YC announcement time [^src10]
- **Multi-GPU**: beta available at YC announcement [^src10]
- **Unsloth Studio**: a GUI product announced at the same time as YC backing; waitlisted [^src10]

## Related

- [[ai-engineering/lm-studio|LM Studio]] — local inference app; the fine-tuned GGUF output is imported and served here
- [[ai-engineering/functiongemma|FunctionGemma]] — the model fine-tuned in LM Studio's Unsloth walkthrough
- [[ai-engineering/quantization|Quantization]] — GGUF quantization levels (Q8_0, F16, BF16, Q4_K_M) used when exporting an Unsloth fine-tune
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How to fine-tune FunctionGemma and run it locally](../../raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md) — LM Studio blog
[^src2]: [Fine-tune Gemma with Unsloth](../../raw/web/web-finetune-gemma-with-unsloth-7508cf36.md) — Unsloth blog, 2024
[^src3]: [Unsloth — Fixing Gemma bugs](../../raw/web/web-unsloth-fixing-gemma-bugs-83cc4e6a.md) — Unsloth blog, Mar 2024
[^src4]: [Unsloth gradient checkpointing — 4× longer context windows](../../raw/web/web-unsloth-gradient-checkpointing-4x-longer-context-windows-41aa4fad.md) — Unsloth blog, Apr 2024
[^src5]: [Fine-tune Llama 3 with Unsloth](../../raw/web/web-finetune-llama-3-with-unsloth-874ddb0c.md) — Unsloth blog
[^src6]: [Fine-tune Phi-3 with Unsloth](../../raw/web/web-finetune-phi-3-with-unsloth-2e7d3c85.md) — Unsloth blog
[^src7]: [Fine-tune Gemma 2 with Unsloth](../../raw/web/web-finetune-gemma-2-with-unsloth-2a306483.md) — Unsloth blog
[^src8]: [Fine-tune Mistral NeMo with Unsloth](../../raw/web/web-finetune-mistral-nemo-with-unsloth-80d57a28.md) — Unsloth blog
[^src9]: [Fine-tune Llama 3.1 with Unsloth](../../raw/web/web-finetune-llama-3-1-with-unsloth-4eca0b7c.md) — Unsloth blog
[^src10]: [Unsloth × Y Combinator](../../raw/web/web-unsloth-x-ycombinator-979219d6.md) — Unsloth blog, late 2024
[^src11]: [Fine-tune Llama 3.2 Vision with Unsloth](../../raw/web/web-fine-tune-llama-3-2-vision-with-unsloth-16376271.md) — Unsloth blog
[^src12]: [Llama 3.2 Vision fine-tuning with Unsloth](../../raw/web/web-llama-3-2-vision-fine-tuning-with-unsloth-d41b7f19.md) — Unsloth blog
[^src13]: [Qwen 2.5 Coder fine-tuning with Unsloth](../../raw/web/web-qwen-2-5-coder-fine-tuning-with-unsloth-b5ba9d9d.md) — Unsloth blog
