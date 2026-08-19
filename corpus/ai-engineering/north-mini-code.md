---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-introducing-north-mini-code-coheres-first-model-for-develope.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - North Mini Code
  - north-mini-code
  - Cohere North Mini Code
confidence: 0.9
last_confirmed: 2026-08-19
tags:
  - entity
  - model
  - coding-model
  - cohere
created: 2026-08-19
updated: 2026-08-19
---

# North Mini Code

**TL;DR**: North Mini Code is Cohere's first developer-focused model — a 30B-parameter Mixture-of-Experts (3B active parameters) model optimized for agentic coding tasks, released under Apache 2.0 on HuggingFace.

## Specs

- **Architecture**: 30B-parameter MoE, 3B active parameters
- **License**: Apache 2.0
- **Release**: 2026 (via HuggingFace)
- **Optimized for**: agentic software engineering tasks, terminal-based workflows, complex code generation[^cohere]

## Benchmarks

On Artificial Analysis' Coding Index: score 33.4, outperforming Qwen3.5 (35B-A3B), Gemma 4 (26B-A4B), Devstral Small 2 (24B Dense), and larger models including Nemotron 3 Super (120B-A12B), Mistral Small 4 (119B-A6B), Devstral 2 (123B). Ranks among strongest open-source coding models in its size class.[^cohere]

## Context

This is the first model in Cohere's new "North" model family. The "Mini Code" designation indicates it is a smaller, developer-focused variant targeting agentic coding harness use cases, not just completion.

## Related

- [/ai-engineering/local-ai-agents.md](/ai-engineering/local-ai-agents.md)
- [/ai-engineering/agentic-coding.md](/ai-engineering/agentic-coding.md)

[^cohere]: Cohere Labs, "Introducing North Mini Code: Cohere's First Model For Developers," huggingface.co/blog/CohereLabs, 2026. `raw/_inbox/web-introducing-north-mini-code-coheres-first-model-for-develope.md`
