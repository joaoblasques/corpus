---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - LangSmith
tags:
  - corpus/ai-engineering
  - entity
created: 2026-05-21
updated: 2026-05-21
---

# LangSmith

**TL;DR**: An agent engineering platform for debugging, evaluating, and shipping reliable AI agents to production. Core workflow: **Observe → Evaluate & Curate → Redeploy** [^src1].

## What it is

LangSmith addresses the core challenge of AI agents being non-deterministic — bugs live in the agent's *reasoning*, not just the code. Traditional stack traces don't surface reasoning failures; deep tracing of LLM calls, tool usage, and decision logic is required [^src1].

Built by LangChain. Commonly used with [LangGraph](/ai-engineering/langgraph.md).

## Setup

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<key>
LANGCHAIN_PROJECT=<project-name>
```

## Core features

| Feature | What it does |
|---|---|
| **Trace view** | Hierarchical steps: LLM calls, tool invocations, guardrails, inputs/outputs |
| **Waterfall view** | Latency breakdown per step; identify bottlenecks |
| **Thread view** | Multi-turn conversations; see context window growth across turns |
| **Online evaluators** | Real-time eval of production traces — LLM-as-judge, custom code, thread-level |
| **Offline evaluation** | Dataset + experiment runner; compare new version against prod baseline |
| **Insights & monitoring** | Aggregate failure-mode clustering, error rates, tool call frequency |
| **Automations** | Auto-route traces to annotation queues based on score thresholds or thumbs-down |
| **Prompt Hub** | Version control for prompts — pull by name + commit ID in production code |

## Debugging workflow

1. Spot issue via monitoring dashboard or online evaluator score drop
2. Filter traces (Polly AI assistant or manual filters)
3. Diagnose — trace view (reasoning), waterfall (latency), thread view (multi-turn)
4. Identify root cause — prompt? tool selection? model? architecture?
5. Pull failing LLM call into playground, iterate prompt, save to Prompt Hub
6. Add example to dataset, run experiment vs baseline
7. Deploy

"Observability is non-negotiable for AI agents — you can't debug what you can't see." [^src1]

## See also

- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — evaluation patterns LangSmith implements (LLM-as-judge, golden datasets, online vs offline)
- [AI Agent](/ai-engineering/ai-agent.md) — the systems LangSmith instruments
- [LangGraph](/ai-engineering/langgraph.md) — sibling LangChain product; commonly used together

---

[^src1]: [LangSmith - Debugging and Evaluating AI Agents](/03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md)
