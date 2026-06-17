---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md
    channel: notes
    ingested_at: 2026-05-07
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
  - path: raw/_inbox/email-2026-05-28-how-grab-reclaimed-hundreds-of-data-engineering-hours-with-m.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/web/github-nirdiamant-genai-agents-50-tutorials-and-implementati.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-how-and-when-to-use-subagents-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - multi-agent
  - multi-agent system
  - agent orchestration
  - sub-agents
  - brain-hands separation
  - specialist agents
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-17
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

## Adoption: scale for productivity, not for looks

A practitioner caution on *when* to add agents [^src2]: don't stand up "15 sub-agents, 30 skills" before you have working single-agent workflows. The recommended path is to **start with one main agent**, build up skills through hands-on iteration, and add a sub-agent only once a workflow is proven and the sub-agent will carry real skills and context. The guiding phrase: scale for productivity, not for what looks cool. A purpose-built sub-agent (e.g. one for marketing, one for business) earns its coordination cost; a speculative fleet does not. See [[ai-engineering/agent-skills|Agent Skills]] for the skill-building prerequisite.

## Case study: Grab's specialist-agent support system

Grab's Analytics Data Warehouse team (1,000+ monthly users, 15,000+ tables) was spending ~40% of engineering time on repetitive "quick question" support; they replaced it with a multi-agent system, dropping resolution from hours to minutes and reclaiming several FTEs [^src3]. The design validates several patterns on this page at production scale.

**Separate the reasoning layer from the action layer** — "the 'brain' is decoupled from the 'hands'" [^src3]. The LLM interprets and plans; specialist agents do the work. A **Classifier** routes each Slack question to the agents it needs, then a **Summarizer** merges findings [^src3]:

| Agent | Job |
|---|---|
| **Data Agent** | Queries Trino/Hive/Delta Lake; validates SQL before execution |
| **Code Search Agent** | Traces transformations and table lineage in GitLab |
| **On-call Agent** | Checks incidents, pipeline health, Slack/Confluence |
| **Enhancement Agent** | Drafts pipeline code changes as merge requests (human-approved) |

**Why specialists beat one giant agent** [^src3]: a monolith means "every new tool increases prompt complexity," and a failure is hard to localize across classification, data access, code search, reasoning, or summarization. Specialists are independently improvable and debuggable — "the choice was obvious. When replacing a manual process that used to take hours, a few minutes of agent coordination is not a serious downside." This is the supervisor/worker pattern with a classifier-driven router on top.

**Production lessons** (each maps to a pitfall above) [^src3]:
- **Context discipline across handoffs.** "In multi-agent systems, context grows quickly." The orchestrator cleans context between agents — "removes unnecessary tokens and invokes the next agent" — tracks tokens with [[ai-engineering/structured-outputs|tiktoken]], summarizes earlier messages on overflow while preserving the original question, and prunes [[ai-engineering/rag|RAG]] context (small LLMs extract snippets rather than passing whole files). See [[ai-engineering/context-window-management|Context Window Management]].
- **Fewer, sharper tools.** An early version had 30+ generic-API tools whose descriptions and outputs bloated the prompt; redesigning tools around real usage and trimming outputs improved responsiveness. See [[ai-engineering/tool-calling|Tool Calling]].
- **Guardrails assuming agents are *not* safe.** Classifier PII checks, SQL validation (blocks risky DDL/DML, enforces timeouts), and no direct commits to main — all Enhancement-Agent changes go through reviewed MRs in a test environment. See [[ai-engineering/agent-security|Agent Security]].
- **Human review designed in, not bolted on.** Reviewers approve/reject/refine/re-route/annotate; answers post immediately but are labeled **"unreviewed"** so users get speed without false authority. Annotations feed offline evals — "tested against real failure cases rather than only synthetic examples." See [[ai-engineering/agent-evaluation|Agent Evaluation]].

Stack: FastAPI, [[ai-engineering/langgraph|LangGraph]] (chosen because the agents "needed to loop, pass work to each other... and maintain state"), Redis, PostgreSQL [^src3].

## Worked implementations (GenAI_Agents)

NirDiamant's `GenAI_Agents` (52+ tutorials) is a large reference catalog of agent and multi-agent implementations, the majority built on [[ai-engineering/langgraph|LangGraph]] for stateful workflow orchestration [^src4]. Recurring multi-agent shapes across the collection: supervisor/coordinator + specialist workers (ATLAS academic system: Coordinator/Planner/Notewriter/Advisor), role-based crews (AutoGen research team: admin/developer/planner/executor/QA; OpenAI Swarm blog team: researcher/planner/writer/editor), and CrewAI inventory agents [^src4]. The catalog also pairs with companion resources on RAG (40+ notebooks) and agent memory (30 notebooks on vector stores, graphs, Mem0, Zep) — see [[ai-engineering/agent-memory|Agent Memory]] [^src4].

## Subagents vs Agent Teams (Claude Code)

The Claude Code documentation draws a sharp distinction between two coordination modes [^src5]:

| Mode | Scope | Communication | Cost |
|---|---|---|---|
| **Subagents** | Within a single session; report back to the main conversation | Subagents cannot talk to each other — only back to parent | Lighter |
| **Agent Teams** | Coordinate across separate sessions | Agents message each other directly | Heavier, more expensive |

Use subagents when tasks are independent and results return to a single orchestrator. Escalate to Agent Teams only when agents need to actively coordinate with each other during execution [^src5].

**Custom subagent definition format** (`.claude/agents/agent-name.md` or `~/.claude/agents/`) [^src5]:

```markdown
---
name: security-reviewer
description: Reviews code changes for security vulnerabilities,
  injection risks, auth issues, and sensitive data exposure.
  Use proactively before commits touching auth, payments, or user data.
tools: Read, Grep, Glob
model: sonnet
---

You are a security-focused code reviewer. Return prioritized findings
with file:line references and a recommended fix for each.
```

The `description` field is what the orchestrator uses to decide when to delegate automatically — "Reviews code for security issues before commits" routes better than "security expert" [^src5]. A too-large custom agent roster reduces automatic delegation reliability; most teams settle on a handful of well-scoped agents [^src5].

## See also

- [[ai-engineering/ai-agent|AI Agent]] — single-agent building block
- [[ai-engineering/agent-skills|Agent Skills]] — the skills a sub-agent should carry before it's worth creating
- [[ai-engineering/langgraph|LangGraph]] — recommended framework for stateful multi-agent workflows
- [[ai-engineering/mcp|MCP]] — coordination protocol for tool calls, memory, and context sharing across agents
- [[ai-engineering/claude-code|Claude Code]] — subagent invocation patterns, custom agent definitions, Agent Teams

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src2]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src3]: [How Grab Reclaimed Hundreds of Data Engineering Hours With Multi-Agent AI](../../raw/email/email-2026-05-28-how-grab-reclaimed-hundreds-of-data-engineering-hours-with-m.md) — Chief Data Tinkerer
[^src4]: [NirDiamant/GenAI_Agents — 52+ tutorials and implementations](../../raw/web/github-nirdiamant-genai-agents-50-tutorials-and-implementati.md) — GitHub
[^src5]: [How and when to use subagents in Claude Code](../../raw/notes/notes-clippings-how-and-when-to-use-subagents-in-claude-code.md) — Anthropic
