---
type: entity
domain: ai-engineering
status: draft
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
updated: 2026-07-07
---

# FunctionGemma

**TL;DR.** FunctionGemma is a Google-released 270M-parameter Gemma variant purpose-built to be fine-tuned for task-specific tool calling, not used as a direct dialogue model [^src2]. [LM Studio](/ai-engineering/lm-studio.md) added native support in v0.3.36 [^src1] and published a walkthrough for fine-tuning it with [Unsloth](/ai-engineering/unsloth.md) and serving the result locally [^src2].

## Model characteristics

- **Size**: 270M parameters — "remarkably small size makes it suitable to run efficiently on nearly any device" [^src2].
- **Intended use**: tool-use/function-calling specialization for agent workflows, tool use, and application backends [^src2].
- **Not a dialogue model**: explicitly not intended for direct dialogue; the base model fails to produce a useful tool call without fine-tuning [^src2].

## Fine-tuning workflow

The canonical path uses [Unsloth](/ai-engineering/unsloth.md) LoRA fine-tuning, with LM Studio as the local inference target [^src2].

### Step 1 — Fine-tune with Unsloth

Unsloth provides starter notebooks (Colab or local Jupyter/VS Code) that handle data prep, LoRA fine-tuning, tokenization, and chat templates. GPU support covers NVIDIA, AMD, and Intel; Apple Silicon fine-tuning is not yet supported via Unsloth [^src2].

### Step 2 — Export to GGUF

Two export paths [^src2]:

- **Option A (Unsloth native)**: use Unsloth's built-in GGUF/llama.cpp conversion to Q8_0, F16, or BF16; save locally or push to Hugging Face.
- **Option B (manual merge)**: merge LoRA adapters into the base model (FP16), save the merged model, then run a separate GGUF conversion and choose a quantization level (e.g. Q8_0, Q4_K_M).

### Step 3 — Import into LM Studio

```
lms import <path/to/model.gguf>
```

LM Studio auto-detects the model and lists it under "My Models." Manual import via the model directory structure is a fallback if `lms import` fails [^src2].

### Step 4 — Serve for local API usage

Two serving options [^src2]:

- **GUI**: load the model and start the server from the LM Studio interface.
- **CLI**: run `lms ls` to find the model identifier, `lms load <model identifier>` to load it (optional `--ttl <seconds>` for auto-unload), then `lms server start` to expose the local API.

## Before/after fine-tuning

LM Studio's example task: ask the model to describe the solar system using a Wikipedia search tool. Before fine-tuning the base model fails to generate a helpful response; after ~10 minutes of fine-tuning it successfully invokes the Wikipedia search tool. The source recommends fine-tuning for at least one hour for improved results [^src2].

## Related

- [LM Studio](/ai-engineering/lm-studio.md) — local inference app; added native support in v0.3.36 and published the fine-tuning walkthrough
- [Unsloth](/ai-engineering/unsloth.md) — fine-tuning toolkit (LoRA, GGUF export) used to specialize FunctionGemma
- [DiffusionGemma](/ai-engineering/diffusiongemma.md) — another Gemma-family variant (diffusion-based, unrelated architecture)
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [LM Studio 0.3.36](../../raw/web/web-lm-studio-0-3-36-80332211.md) — LM Studio blog
[^src2]: [How to fine-tune FunctionGemma and run it locally](../../raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md) — LM Studio blog
