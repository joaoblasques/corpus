---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/web/web-lm-studio-0-3-36-80332211.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - Function Gemma
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# FunctionGemma

**TL;DR.** FunctionGemma is a Google-released 270M-parameter variant of Gemma, purpose-built to be fine-tuned for task-specific tool calling rather than used as a direct dialogue model [^src2]. [LM Studio](/ai-engineering/lm-studio.md) added native support for it in v0.3.36 [^src1], and LM Studio published a walkthrough for fine-tuning it with [Unsloth](/ai-engineering/unsloth.md) and serving the result locally [^src2].

## Details

- **Size**: 270M parameters — small enough to run on nearly any device [^src2].
- **Intended use**: tool-use/function-calling specialization for agent workflows and application backends; explicitly *not* intended for direct dialogue [^src2].
- **Fine-tuning path**: Unsloth LoRA fine-tuning → GGUF conversion → import into LM Studio via `lms import`. LM Studio's own example shows the base model failing to produce a useful tool call before fine-tuning, and successfully invoking a Wikipedia search tool after ~10 minutes of fine-tuning [^src2].

## Related

- [LM Studio](/ai-engineering/lm-studio.md) — local app that added native support and published the fine-tuning walkthrough
- [Unsloth](/ai-engineering/unsloth.md) — fine-tuning toolkit used to specialize FunctionGemma
- [DiffusionGemma](/ai-engineering/diffusiongemma.md) — another Gemma-family variant (diffusion-based, unrelated architecture)
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [LM Studio 0.3.36](../../raw/web/web-lm-studio-0-3-36-80332211.md) — LM Studio blog
[^src2]: [How to fine-tune FunctionGemma and run it locally](../../raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md) — LM Studio blog
