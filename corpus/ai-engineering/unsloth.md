---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# Unsloth

**TL;DR.** Unsloth is a fine-tuning toolkit that reduces training time and VRAM usage by optimizing training kernels and LoRA workflows, described as "one of the fastest ways to fine-tune modern LLMs on consumer hardware or cloud GPUs" [^src1]. [[ai-engineering/lm-studio|LM Studio]] uses it as the recommended fine-tuning step in its [[ai-engineering/functiongemma|FunctionGemma]] walkthrough [^src1].

## Details

- **Hardware support**: NVIDIA, AMD, and Intel GPUs [^src1].
- **Apple Silicon**: local fine-tuning with Unsloth is not yet supported on Apple Silicon; Apple Silicon users are pointed to a separate notebook for that case [^src1].
- **Workflow**: ready-made starter notebooks (Colab or local Jupyter/VS Code) load a base model, apply optimized LoRA fine-tuning, and handle tokenization/chat templates automatically for supported models [^src1].
- **Export**: Unsloth includes native GGUF/llama.cpp conversion (to Q8_0, F16, or BF16), or LoRA adapters can be merged into the base model and converted to GGUF separately at a chosen quantization level [^src1].

## Related

- [[ai-engineering/lm-studio|LM Studio]] — local inference app; the fine-tuned GGUF output is imported and served here
- [[ai-engineering/functiongemma|FunctionGemma]] — the model fine-tuned in LM Studio's Unsloth walkthrough
- [[ai-engineering/quantization|Quantization]] — GGUF quantization levels (Q8_0, F16, BF16, Q4_K_M) used when exporting an Unsloth fine-tune
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How to fine-tune FunctionGemma and run it locally](../../raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md) — LM Studio blog
