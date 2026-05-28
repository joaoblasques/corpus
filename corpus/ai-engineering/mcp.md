---
type: concept
domain: ai-engineering
status: stub
sources:
  - path: 03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - MCP
  - Model Context Protocol
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
---

# MCP (Model Context Protocol)

**TL;DR**: A structured coordination protocol that defines how agents, tools, and memory communicate — replacing ad-hoc prompting with a standardized interface for tool calls, memory access, and context sharing [^src1].

## What it does

MCP replaces chaotic back-and-forth prompt engineering in multi-agent systems with a formal protocol layer. Governs [^src1]:
- **Tool calls** — structured request/response format for tool invocation
- **Memory access** — how agents read and write to memory stores
- **Context sharing** — how context is passed between agents or from tools back to the orchestrator

Described as "essential for scalable multi-agent systems" [^src1].

> [unsourced — please verify]: MCP was introduced by Anthropic as an open standard; this source describes its purpose but not its origin.

## See also

- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — MCP is the coordination layer for multi-agent architectures
- [[ai-engineering/tool-calling|Tool Calling]] — MCP standardizes how tool calls are structured
- [[ai-engineering/agent-memory|Agent Memory]] — MCP governs memory access protocols

---

[^src1]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
