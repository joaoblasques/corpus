---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-github-earendil-works-pi-ai-agent-toolkit-unified-llm-api-ag.md
    channel: web
    ingested_at: 2026-08-19
  - path: raw/_inbox/web-polar-agentic-rl-on-any-harness-at-scale.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - Pi agent
  - pi-coding-agent
  - earendil-works/pi
  - Pi agent harness
confidence: 0.8
last_confirmed: 2026-08-19
tags:
  - entity
  - coding-agent
  - agent-harness
  - local-ai
created: 2026-08-19
updated: 2026-08-19
---

# Pi Agent

**TL;DR**: Pi is an open-source AI agent toolkit by `earendil-works` providing a unified LLM API, an agent loop, a TUI, and a coding agent CLI. It is one of the harnesses validated in the Polar agentic RL paper and used for local model evaluation (e.g., with Ornith-1.0).

## Components

- `@earendil-works/pi-coding-agent` — interactive coding agent CLI
- `@earendil-works/pi-agent-core` — agent runtime with tool calling and state management
- `@earendil-works/pi-ai` — unified multi-provider LLM API (OpenAI, Anthropic, Google, and others)[^pi-github]

## Research context

The Polar RL paper (2026) validated Polar over four coding harnesses: Codex, Claude Code, Qwen Code, and Pi. Using GRPO training, Qwen3.5-4B improved by 6.2 points on SWE-Bench Verified with the Pi harness.[^polar]

Used by Simon Willison for local model evaluation with Ornith-1.0-35B (GGUF via LM Studio).[unsourced — from ornith source in same batch]

## Related

- [/ai-engineering/local-ai-agents.md](/ai-engineering/local-ai-agents.md)
- [/ai-engineering/agent-harness.md](/ai-engineering/agent-harness.md)
- [/ai-engineering/ornith-1-0.md](/ai-engineering/ornith-1-0.md)

[^pi-github]: GitHub, `earendil-works/pi`. `raw/_inbox/web-github-earendil-works-pi-ai-agent-toolkit-unified-llm-api-ag.md`
[^polar]: Polar paper, arxiv.org/abs/2605.24220. `raw/_inbox/web-polar-agentic-rl-on-any-harness-at-scale.md`
