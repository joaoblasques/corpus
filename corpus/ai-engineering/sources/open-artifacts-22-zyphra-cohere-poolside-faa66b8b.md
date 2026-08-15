---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-latest-open-artifacts-22-zyphra-cohere-and-poolside-are-expa-faa66b8b.md
    channel: web
    ingested_at: 2026-08-15
aliases:
  - open artifacts 22
  - Zyphra
  - Poolside Laguna-M.1
  - Cohere Command A+
  - NVIDIA Nemotron 3 Ultra
  - OpenMDW license
  - open model ecosystem diversity
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-15
updated: 2026-08-15
url: https://www.interconnects.ai/p/artifacts-22-zyphra-cohere-and-poolside
origin: obsidian-list
---

# Latest Open Artifacts (#22): Zyphra, Cohere, and Poolside

**TL;DR** — The open model ecosystem is diversifying away from a handful of Chinese players toward a broader range of Western, sovereign, and product-company actors. Three categories of motivations: pure model makers, Big Tech (upsell + GPU ecosystem), and product companies releasing specialized models.[^src1]

## Ecosystem diversity thesis

"A year ago, open artifacts and the open model landscape more broadly were dominated by a handful of (Chinese) players. This has shifted, with us increasingly featuring more niche companies all over the world."[^src1]

**Three actor categories**[^src1]:
- **Pure model makers**: frontier-chasing (DeepSeek, Zhipu, MiniMax, Poolside, Arcee, Zyphra); sovereign AI players (Cohere, Sovereign, Mistral, Trillion Labs)
- **Big Tech**: Qwen (Alibaba — upsells closed models), Gemma (Google), NVIDIA (benefits from flourishing open ecosystem → GPU demand)
- **Product companies**: JetBrains, Zed, Krea, Photoroom — niche specialized models for their product needs; open-sourcing doesn't hurt their bottom line

Thesis: "more companies will develop a long-tail of models and the number of companies chasing the absolute, open frontier will diminish."[^src1]

## Notable releases in this batch

**NVIDIA Nemotron-3-Ultra-550B-A55B**: LatentMoE architecture; most training data is open source; adopts **OpenMDW license** — a new license tailored specifically for model weights and data (MIT/Apache are software licenses that don't technically apply to weights).[^src1]

**Cohere Command A+** (`command-a-plus-05-2026-bf16`): 218B-A25B MoE; multimodal + multilingual + agentic; released under **Apache 2.0** (previous iterations used non-commercial license). Usable on a single B200 at 4-bit quantization.[^src1]

**GLM-5.2** (zai-org): "genuinely usable for everyday work, not a huge regression compared to the best closed models." Download numbers roughly in line with GLM-5 post-release.[^src1]

**ZAYA1-74B-preview** (Zyphra): 74B-A4B MoE; trains on AMD GPUs; "insider tip in the research community due to their tech reports with interesting architecture choices."[^src1]

**Laguna-M.1** (Poolside): Apache 2.0; Poolside commits to open releases going forward — "Open weights are now our default."[^src1]

**Kimi-K2.7-Code** (Moonshot AI): token-efficiency focused update to Kimi.[^src1]

## On restrictions

"Attempts to slow or ban this ecosystem are not only futile, as the history of tech-related bans has shown, but also unsafe and anti-freedom."[^src1]

## See also

- [Mixture of Experts](/ai-engineering/mixture-of-experts.md)
- [Laguna XS.2](/ai-engineering/laguna-xs2.md) (Poolside)
- [Nemotron 3 Ultra](/ai-engineering/nemotron-3-ultra.md)

---

[^src1]: [Latest open artifacts (#22): Zyphra, Cohere, and Poolside](../../../raw/web/web-latest-open-artifacts-22-zyphra-cohere-and-poolside-are-expa-faa66b8b.md) — interconnects.ai, 2026-06-29
