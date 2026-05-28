---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md
    channel: notes
    ingested_at: 2026-05-07
aliases:
  - multi-agent
  - multi-agent system
  - agent orchestration
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-05-07
---

# Multi-Agent Systems

**TL;DR**: Architectures where multiple AI agents cooperate to complete tasks, each specializing in a sub-problem. Four common patterns; coordination complexity is the main cost [^src1].

## Patterns

### 1. Sequential (Pipeline)
```
Agent A → Agent B → Agent C
```
Simplest and most predictable. Each agent specializes. No coordination overhead [^src1].

### 2. Parallel
Multiple agents run simultaneously; results merged. Reduces latency, adds coordination complexity [^src1].

### 3. Supervisor / Worker
Orchestrator agent delegates to specialized sub-agents.
Example: `Researcher → Drafter → Fact Checker → Editor` [^src1].

### 4. Data-Driven Decomposition
Orchestrator splits task by data partitions (e.g., 100 documents processed in parallel) [^src1].

## Agent communication

Three modes [^src1]:
- **Shared state** — same memory or file visible to all agents
- **Message passing** — explicit output/input handoff between agents
- **Results aggregation** — each agent returns independently; orchestrator merges

## Pitfalls

- Agents may duplicate work if shared state is not managed [^src1]
- Context can drift across many handoffs — long chains lose original intent [^src1]
- More agents = more tokens = more cost [^src1]

## See also

- [[ai-engineering/ai-agent|AI Agent]] — single-agent building block
- [[ai-engineering/langgraph|LangGraph]] — recommended framework for stateful multi-agent workflows
- [[ai-engineering/mcp|MCP]] — coordination protocol for tool calls, memory, and context sharing across agents

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
