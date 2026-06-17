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
  - path: raw/notes/notes-clippings-multi-agent-coordination-patterns-five-approaches-and-when-t.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - multi-agent
  - multi-agent system
  - agent orchestration
  - sub-agents
  - brain-hands separation
  - specialist agents
  - generator-verifier
  - orchestrator-subagent
  - agent teams
  - message bus
  - shared state
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

## Five coordination patterns (Anthropic taxonomy)

Anthropic's engineering team (Cara Phillips et al.) defines five coordination patterns with explicit selection criteria [^src6]. The recommendation: "Start with the simplest pattern that could work, watching where it struggles, and evolving from there." Default starting point: **orchestrator-subagent** — handles the widest range of problems with the least coordination overhead [^src6].

### 1. Generator-Verifier

A generator produces output; a verifier evaluates it against criteria and either accepts or routes back with feedback. Loop continues until accepted or max iterations reached [^src6].

**Use when**: output quality is critical and evaluation criteria can be made explicit — code generation (one writes, one writes-and-runs tests), fact-checking, rubric grading, compliance verification [^src6].

**Failure modes**: verifier told only to check "whether output is good" (no criteria) rubber-stamps the generator ("the illusion of quality control without the substance"); generator-verifier loop stalls if feedback is not actionable (oscillates without converging, needs a max-iteration fallback) [^src6].

### 2. Orchestrator-Subagent

A lead agent plans work, delegates to subagents, and synthesizes results. Subagents complete one bounded task and return results [^src6]. Claude Code uses this pattern internally: the main agent writes code while dispatching read-only subagents in the background to search large codebases [^src6].

**Use when**: task decomposition is clear and subtasks have minimal interdependence [^src6].

**Failure modes**: orchestrator becomes an information bottleneck when subagent findings are relevant to each other (critical details are lost across handoffs); sequential execution unless explicitly parallelized [^src6].

### 3. Agent Teams

Workers stay alive across many assignments, accumulating context and domain specialization. A coordinator assigns work and collects outcomes; workers don't reset between tasks [^src6].

The key distinction from orchestrator-subagent: "The orchestrator spawns a subagent for one bounded subtask, and the subagent terminates after returning a result. Teammates stay alive across many assignments" [^src6].

**Use when**: subtasks are independent and benefit from sustained, multi-step work — e.g. migrating a large codebase service-by-service where each teammate builds familiarity with its assigned service [^src6].

**Failure modes**: teammates operating independently can produce conflicting outputs or duplicate work; shared resources (same file, database) require careful task partitioning and conflict resolution [^src6].

### 4. Message Bus

Agents interact through publish/subscribe primitives via a shared communication layer. New agents can start receiving relevant work without rewiring existing connections [^src6].

**Use when**: workflow emerges from events rather than a predetermined sequence, and the agent ecosystem is likely to grow — e.g. a security operations system where new alert types may emerge requiring new agent types [^src6].

**Failure modes**: tracing a causal chain across five agents is hard without careful logging; LLM-based routers introduce their own failure modes; routing misclassification fails silently [^src6].

### 5. Shared State

Agents read from and write to a persistent store (database, filesystem, document) with no central coordinator. Work begins when the store is seeded; ends when a termination condition is met [^src6].

**Use when**: agents' work is collaborative and findings should flow between them in real time (e.g. a research synthesis system where one agent's discovery of a key researcher immediately informs another agent's investigation) [^src6]. Also the right choice when no single point of failure is acceptable — if any one agent stops, others continue.

**Failure modes**: without explicit coordination, agents may duplicate work or pursue contradictory approaches; reactive loops (Agent A writes → B reads and responds → A sees and responds again) burn tokens without converging. "Systems that treat termination as an afterthought tend to cycle indefinitely or stop arbitrarily" [^src6]. Requires first-class termination conditions: time budget, convergence threshold (no new findings for N cycles), or a designated "am I done?" agent.

### Pattern selection matrix

| Situation | Pattern |
|---|---|
| Quality-critical output, explicit evaluation criteria | Generator-Verifier |
| Clear task decomposition, bounded subtasks | Orchestrator-Subagent |
| Parallel workload, independent long-running subtasks | Agent Teams |
| Event-driven pipeline, growing agent ecosystem | Message Bus |
| Collaborative research, agents share discoveries | Shared State |
| No single point of failure required | Shared State |

**Hybrid pattern**: common in production — orchestrator-subagent for the overall workflow with shared state for a collaboration-heavy subtask; or message bus for event routing with agent team-style workers handling each event type [^src6].

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
[^src6]: [Multi-agent coordination patterns: Five approaches and when to use them](../../raw/notes/notes-clippings-multi-agent-coordination-patterns-five-approaches-and-when-t.md) — Cara Phillips et al., Anthropic
