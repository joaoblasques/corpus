---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-github-rasbt-local-coding-agent-evals.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - rasbt local-coding-agent-evals
  - Sebastian Raschka coding agent evals
confidence: 0.85
last_confirmed: 2026-08-19
tags:
  - local-ai
  - coding-agents
  - evals
  - ollama
created: 2026-08-19
updated: 2026-08-19
---

# Local Coding Agent Evals (rasbt)

**TL;DR**: A practical eval suite by Sebastian Raschka comparing local coding agent harnesses (Qwen Code, Codex, Claude Code with Ollama-hosted models). Three task packs testing the LLM, the inference engine, and the harness combo separately.

## Repo structure

Three benchmark categories:[^rasbt]

1. **speed-memory-benchmark** — measures Ollama prefill speed, decode speed, wall time, memory use across longer prompts. Tests LLM + inference engine.
2. **hard-tool-reasoning-benchmark** — asks Ollama model to return one tool decision for five harder reasoning tasks (no tool execution). Tests LLM base capability only.
3. **agent-problem-pack** — five small coding tasks for testing an actual coding-agent harness in isolated workspaces, derived from the reasoning tasks above. Tests LLM + harness combo.

## Key design principle

The three benchmark tiers isolate different failure points: base model capability, inference engine performance, and harness quality. This disaggregation is useful for diagnosing where local agent underperformance actually comes from.

## Related

- [/ai-engineering/local-ai-agents.md](/ai-engineering/local-ai-agents.md)
- [/ai-engineering/ollama.md](/ai-engineering/ollama.md)
- [/ai-engineering/llm-evals.md](/ai-engineering/llm-evals.md)

[^rasbt]: Sebastian Raschka, GitHub `rasbt/local-coding-agent-evals`. `raw/_inbox/web-github-rasbt-local-coding-agent-evals.md`
