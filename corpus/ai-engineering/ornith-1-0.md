---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-ornith-1-0-self-scaffolding-llms-for-agentic-coding-08519a83.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - Ornith-1.0
  - ornith
  - self-scaffolding LLM
  - DeepReinforce Ornith
confidence: 0.85
last_confirmed: 2026-08-19
tags:
  - entity
  - model
  - coding-model
  - open-weights
  - local-ai
created: 2026-08-19
updated: 2026-08-19
---

# Ornith-1.0

**TL;DR**: Ornith-1.0 is the first model release from DeepReinforce — an open-weights (MIT license) self-scaffolding LLM family for agentic coding, built on Gemma 4 and Qwen 3.5. Notable for strong benchmark performance in its size class.

## Model family

Variants: 9B Dense, 31B Dense, 35B MoE, 397B MoE. Built on top of pretrained Gemma 4 (Apache 2.0) and Qwen 3.5 (Apache 2.0). Achieves state-of-the-art among open-source models of comparable size on coding benchmarks.[^simonw-ornith]

## "Self-scaffolding" framing

The "self-scaffolding" concept refers to the model being trained/designed to manage agent harness control flow itself — rather than relying on an external harness layer to manage context and tool calling. The degree to which this is implemented vs. aspirational is [unsourced — based on paper framing only].

## Practitioner impressions

Simon Willison ran `ornith-1.0-35b-Q4_K_M.gguf` (20GB GGUF) via LM Studio, hooked up to the [Pi agent harness](/ai-engineering/pi-agent.md): "Initial impressions are very good — it seems to be able to run the agent harness over many tool calls in a proficient way."[^simonw-ornith]

## License compatibility

Both base models (Gemma 4 Apache 2.0, Qwen 3.5 Apache 2.0) are compatible with MIT licensing for the derivative Ornith-1.0 models — the older Gemma Terms of Use (which had additional commercial restrictions) do not apply to Gemma 4.[^simonw-ornith]

## Related

- [/ai-engineering/local-ai-agents.md](/ai-engineering/local-ai-agents.md)
- [/ai-engineering/pi-agent.md](/ai-engineering/pi-agent.md)
- [/ai-engineering/lm-studio.md](/ai-engineering/lm-studio.md)

[^simonw-ornith]: Simon Willison link blog, "Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding," simonwillison.net, 2026-06-29. `raw/_inbox/web-ornith-1-0-self-scaffolding-llms-for-agentic-coding-08519a83.md`
