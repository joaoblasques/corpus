---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-ornith-1-0-self-scaffolding-llms-for-agentic-coding-08519a83.md
    channel: web
    ingested_at: 2026-08-19
  - path: raw/_inbox/web-self-scaffolding-ai-models-how-ornith-1-0-writes-its-own-age-bf993fd0.md
    channel: web
    ingested_at: 2026-08-22
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

Self-scaffolding means the model generates a custom Python execution harness *as the first step* in task execution — before working on the task itself. The generated harness includes: tool selection and sequencing logic, state management (how outputs from step N pass to N+1), conditional branches with task-specific recovery, and termination criteria. Harness is discrete and inspectable before execution begins. [^mindstudio-ornith]

The key distinction from ordinary code generation: the code is the *execution environment* for finding the solution, not the solution itself — a meta-level operation where the model reasons about how it should solve the task and encodes that reasoning into a runnable structure. [^mindstudio-ornith]

Previously marked "aspirational" based on paper framing only; second source (MindStudio analysis) provides implementation detail confirming the harness-generation-first design. Confidence updated.

## Practitioner impressions

Simon Willison ran `ornith-1.0-35b-Q4_K_M.gguf` (20GB GGUF) via LM Studio, hooked up to the [Pi agent harness](/ai-engineering/pi-agent.md): "Initial impressions are very good — it seems to be able to run the agent harness over many tool calls in a proficient way."[^simonw-ornith]

## License compatibility

Both base models (Gemma 4 Apache 2.0, Qwen 3.5 Apache 2.0) are compatible with MIT licensing for the derivative Ornith-1.0 models — the older Gemma Terms of Use (which had additional commercial restrictions) do not apply to Gemma 4.[^simonw-ornith]

## Related

- [/ai-engineering/local-ai-agents.md](/ai-engineering/local-ai-agents.md)
- [/ai-engineering/pi-agent.md](/ai-engineering/pi-agent.md)
- [/ai-engineering/lm-studio.md](/ai-engineering/lm-studio.md)

[^simonw-ornith]: Simon Willison link blog, "Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding," simonwillison.net, 2026-06-29. `raw/_inbox/web-ornith-1-0-self-scaffolding-llms-for-agentic-coding-08519a83.md`
[^mindstudio-ornith]: MindStudio Blog, "Self-Scaffolding AI Models: How Ornith 1.0 Writes Its Own Agent Harness," mindstudio.ai, 2026-06-30. `raw/_inbox/web-self-scaffolding-ai-models-how-ornith-1-0-writes-its-own-age-bf993fd0.md`
