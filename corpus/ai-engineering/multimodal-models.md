---
type: concept
domain: ai-engineering
status: draft
aliases:
  - LMM
  - large multimodal model
  - multimodal AI
  - CLIP
  - Flamingo
  - multimodal
tags:
  - corpus/ai-engineering
  - llm-internals
  - multimodality
  - vision-language
sources:
  - path: raw/web/web-multimodality-and-large-multimodal-models-lmms-427578c7.md
    channel: web
    title: Multimodality and Large Multimodal Models (LMMs)
  - path: raw/web/web-open-challenges-in-llm-research-d184c921.md
    channel: web
    title: Open Challenges in LLM Research
  - path: raw/web/web-multimodal-data-integration-architecture-best-practices-e4e6f9d3.md
    channel: web
    title: Multimodal Data Integration Architecture Best Practices
confidence: 0.9
last_confirmed: 2026-08-12
created: 2026-08-12
updated: 2026-08-12
---

# Multimodal Models (LMMs)

**TL;DR**: Large Multimodal Models (LMMs) extend LLMs to process multiple data modalities (text, image, audio, video). CLIP (2021) established contrastive multimodal pretraining; Flamingo (2022) demonstrated few-shot visual QA in a full LMM. Key driver: text data is running out; multimodal data is far more abundant.

## Why multimodality

1. **Required for many use cases**: healthcare (text notes + imaging), robotics, e-commerce (images + descriptions), manufacturing.
2. **Performance ceiling of text-only models**: "text-based models require so much text that there's a realistic concern that we'll soon run out of Internet data to train text-based models. Once we run out of text, we'd need to leverage other data modalities."[^challenges]
3. **Accessibility**: multimodal interfaces let users interact via text, voice, or camera; can enable visually impaired people to navigate the real world.[^lmm]

## Data modalities

| Modality | Notes |
|---|---|
| Text | Most powerful for outputs (generalizes to many tasks) |
| Image | Most versatile for inputs (can represent text, tables, audio spectrograms, videos) |
| Audio | Mostly voice-based in ML today; non-speech use cases (music gen) still niche |
| Video | Usually treated as a sequence of images; audio component often dropped — significant information loss (88% of TikTok users say sound is essential)[^lmm] |
| Tabular | Convertible to images (charts) or processed directly |
| Graphs, 3D | Less mature modalities |

Any digital format can theoretically be represented as bitstrings/bytestrings; a model that learns from bytestrings directly could handle any modality.[^lmm]

## CLIP (OpenAI, 2021)

**Architecture**: two encoders (image encoder + text encoder) trained jointly via contrastive learning on (image, text) pairs. Both encoders project to the same embedding space; matched pairs are trained to be close, unmatched pairs to be distant.[^lmm]

**Training signal**: natural language supervision — no manual label annotation needed. Trained on 400M (image, text) pairs scraped from the web.

**Key innovation**: zero-shot transfer. By phrasing classification as "which text description matches this image?", CLIP generalizes to any image classification task without task-specific fine-tuning.

**Foundation role**: CLIP's image encoder is used as the vision component in many subsequent multimodal systems (LLaVA, BLIP-2, etc.).[^lmm]

## Flamingo (DeepMind, 2022)

**Architecture**: a frozen pre-trained language model backbone with cross-attention layers inserted at intervals. Visual tokens are produced by a pre-trained vision encoder (similar to CLIP) and injected into the LM via these cross-attention layers. The LM itself remains frozen; only the cross-attention layers are trained.[^lmm]

**Key result**: strong few-shot visual question answering with only a handful of image+text examples in the prompt.

**Design insight**: interleaving visual inputs with the text stream (alternating images and text in one sequence) allows the model to handle complex multi-image tasks.

## BLIP-2, LLaVA, and later work

Post-Flamingo models focus on cheaper training via adapters:[^lmm]
- **BLIP-2** (Salesforce, 2023): querying transformer (Q-Former) bridges frozen image encoder and frozen LM — only the Q-Former is trained.
- **LLaVA** (2023): visual instruction tuning — fine-tunes a vision-language model on instruction-following data (image + natural language instructions).
- **LLaMA-Adapter V2**: lightweight adapter approach (~1M parameters added to a frozen LLaMA).

## Multimodal outputs

Text-to-image (Dall-E, Stable Diffusion, Midjourney) produces unimodal image outputs. True multimodal output models (generating both text and images interleaved) are a research direction still maturing as of the source date.[^lmm]

## Research challenges

Chip Huyen's assessment (2023): "Multimodality, IMO, is so powerful and yet so underrated."[^challenges] Three multimodal tasks for LMMs:
1. Image generation (text → image)
2. Text generation with visual context (visual QA — text + images → text)
3. Vision-language understanding (classification, grounding, etc.)

## Cross-links

- [/ai-engineering/chip-huyen.md](/ai-engineering/chip-huyen.md) — source author
- [/ai-engineering/generation-configs.md](/ai-engineering/generation-configs.md) — sampling mechanics that apply to multimodal generation as well
- [/data-engineering/semantic-layer.md](/data-engineering/semantic-layer.md) — structured data modality (tabular) as one input to multimodal systems

---

[^lmm]: raw/web/web-multimodality-and-large-multimodal-models-lmms-427578c7.md
[^challenges]: raw/web/web-open-challenges-in-llm-research-d184c921.md
