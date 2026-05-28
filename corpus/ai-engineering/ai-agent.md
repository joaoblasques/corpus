---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md
    channel: notes
    ingested_at: 2026-05-07
  - path: 03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md
    channel: notes
    ingested_at: 2026-05-21
  - path: 03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - ai agent
  - agentic AI
  - LLM agent
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-05-21
---

# AI Agent

**TL;DR**: An LLM operating in an iterative loop — reasoning, calling tools, observing results, and repeating — rather than producing a single one-shot response [^src1].

## Core loop

```
Model reasons → calls tool or produces output → observes result → repeats until goal achieved
```

Analogous to how humans actually work: plan → draft → revise → refine [^src1].

An alternative framing with four named steps [^src3]:

| Step | What happens |
|---|---|
| **Perceive** | Gather data from APIs, databases, web search, sensors |
| **Reason** | LLM plans steps, selects tools; may invoke RAG for real-time data |
| **Act** | Execute — API calls, code, shell commands, notifications |
| **Learn** | Store outcomes to long-term memory; improve at similar tasks |

The "Learn" step distinguishes agentic AI from reactive chatbots (one prompt → one answer with no state carryover) [^src3].

## Four key components

| Component | Role |
|---|---|
| LLM | The reasoning engine |
| Tools | Functions the agent can call |
| Memory | Short-term (context window) + long-term (vector DB / external storage) |
| Orchestration layer | Controls the loop, routing, and state |

## When to use an agent vs a simple LLM call

| Use Agent | Use Simple LLM |
|---|---|
| Multi-step reasoning required | Single Q&A |
| Needs external data or tools | Self-contained response |
| Decision branching required | Linear task |
| Requires validation loops | One-shot generation |

Cost of adding agents: complexity + latency + cost. Default to the simplest solution [^src1].

## Evaluation

Don't ship without measuring [^src1]. Use two complementary evaluation loops:

| Mode | When | What |
|---|---|---|
| **Online** | Live production | Sample-based eval of real traces; catches regressions in prod |
| **Offline** | Pre-deployment | Run against golden dataset; compare vs baseline |

Key metrics: task success rate, tool call accuracy, latency and cost per task, retrieval quality [^src1].

**LLM-as-judge** pattern: use a second LLM to evaluate agent output against quality criteria (accuracy, helpfulness, safety) [^src1][^src2].

**Context window growth** degrades agent quality across turns — thread-level evaluation catches this; a naive per-call eval misses it [^src2].

See [[ai-engineering/agent-evaluation|Agent Evaluation]] for full treatment of evaluation patterns, golden datasets, and the production feedback loop.

## Production concerns

- **Security**: sandbox code execution (Docker, strict limits); whitelist safe libraries; validate inputs, scan outputs for PII/keys [^src1]
- **Reliability**: circuit breakers for infinite loops; retry with exponential backoff; structured outputs over raw text [^src1]
- **Quality/latency/cost triangle**: more powerful model = better quality + higher cost; parallel agents = lower latency + higher cost; caching = lower cost + potential staleness [^src1]

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — the highest-leverage skill in agent development
- [[ai-engineering/tool-calling|Tool Calling]] — how agents interact with tools
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — patterns for multiple cooperating agents
- [[ai-engineering/langgraph|LangGraph]] — recommended framework for production multi-agent systems
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: how tool results feed the context loop and why context engineering governs tool call design
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — full treatment of evaluation patterns
- [[ai-engineering/langsmith|LangSmith]] — platform for agent observability and evaluation
- [[ai-engineering/agent-memory|Agent Memory]] — short-term (context window) and long-term (vector DB) memory
- [[ai-engineering/mcp|MCP]] — coordination protocol for agents, tools, and memory

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src2]: [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]]
[^src3]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
