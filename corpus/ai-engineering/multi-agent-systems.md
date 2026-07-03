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
  - path: raw/email/email-2026-05-28-how-grab-reclaimed-hundreds-of-data-engineering-hours-with-m.md
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
  - path: raw/web/web-github-nicobailon-pi-subagents-pi-extension-for-async-subage.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-notion-q-a-claude-managed-agents-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/github/github-crewaiinc-crewai-examples.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/web/web-when-to-use-multi-agent-systems-and-when-not-to-claude.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-orchestrate-teams-of-claude-code-sessions-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/_inbox/youtube-ow1we5PzK-o-the-multi-agent-architecture-that-actually-ships-luke-alvoei.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-zFw19qGAeGo-build-3-production-ai-agents-in-python-full-course-agentspan.md
    channel: youtube
    ingested_at: 2026-06-29
  - path: raw/_inbox/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md
    channel: youtube
    ingested_at: 2026-06-30
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
  - Factory Missions
  - factory missions architecture
  - validation contract
  - droid whispering
  - creator-verifier pattern
  - delegation pattern
  - direct communication pattern
  - negotiation pattern
  - broadcast pattern
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-25
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

A practitioner caution on *when* to add agents [^src2]: don't stand up "15 sub-agents, 30 skills" before you have working single-agent workflows. The recommended path is to **start with one main agent**, build up skills through hands-on iteration, and add a sub-agent only once a workflow is proven and the sub-agent will carry real skills and context. The guiding phrase: scale for productivity, not for what looks cool. A purpose-built sub-agent (e.g. one for marketing, one for business) earns its coordination cost; a speculative fleet does not. See [Agent Skills](/ai-engineering/agent-skills.md) for the skill-building prerequisite.

## Local-agent teams (org chart, chief-of-staff, start lean)

[Local AI agents](/ai-engineering/local-ai-agents.md) form teams the same way: each agent gets a specialized function and the team produces "something greater than the sum of its parts" — e.g. a research team scouting stocks plus a software team building product [^src11] [09:26](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=9:26). Two practitioner patterns recur in production local-agent fleets:

- **A chief-of-staff (manager) agent.** Rather than the human supervising every worker, a dedicated manager agent checks for blockers at the start and end of each day and only escalates what it can't resolve — "I don't want to manage the agents" [^src12] [06:30](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=6:30). Workers surface a **blocked** status (missing tool/API access) into an **autonomy log** the manager maintains. This is the supervisor/coordinator pattern (§ above) promoted to a standing role.
- **Start lean — fire agents that aren't earning their keep.** A documented fleet was *cut in half* after the operator hit rate limits and realized "if you were just more efficient and structured agents better... you don't need like 10" [^src12] [07:23](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=7:23). This is the same scale-for-productivity-not-for-looks discipline as the §Adoption caution, validated under real rate-limit pressure. [Paperclip](/ai-engineering/paperclip.md) is a control plane built specifically to run such an org-chart of agents; [OpenClaw](/ai-engineering/openclaw.md) shows the complementary cost lever of routing each agent to a different model.

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
- **Context discipline across handoffs.** "In multi-agent systems, context grows quickly." The orchestrator cleans context between agents — "removes unnecessary tokens and invokes the next agent" — tracks tokens with [tiktoken](/ai-engineering/structured-outputs.md), summarizes earlier messages on overflow while preserving the original question, and prunes [RAG](/ai-engineering/rag.md) context (small LLMs extract snippets rather than passing whole files). See [Context Window Management](/ai-engineering/context-window-management.md).
- **Fewer, sharper tools.** An early version had 30+ generic-API tools whose descriptions and outputs bloated the prompt; redesigning tools around real usage and trimming outputs improved responsiveness. See [Tool Calling](/ai-engineering/tool-calling.md).
- **Guardrails assuming agents are *not* safe.** Classifier PII checks, SQL validation (blocks risky DDL/DML, enforces timeouts), and no direct commits to main — all Enhancement-Agent changes go through reviewed MRs in a test environment. See [Agent Security](/ai-engineering/agent-security.md).
- **Human review designed in, not bolted on.** Reviewers approve/reject/refine/re-route/annotate; answers post immediately but are labeled **"unreviewed"** so users get speed without false authority. Annotations feed offline evals — "tested against real failure cases rather than only synthetic examples." See [Agent Evaluation](/ai-engineering/agent-evaluation.md).

Stack: FastAPI, [LangGraph](/ai-engineering/langgraph.md) (chosen because the agents "needed to loop, pass work to each other... and maintain state"), Redis, PostgreSQL [^src3].

## Worked implementations (GenAI_Agents)

NirDiamant's `GenAI_Agents` (52+ tutorials) is a large reference catalog of agent and multi-agent implementations, the majority built on [LangGraph](/ai-engineering/langgraph.md) for stateful workflow orchestration [^src4]. Recurring multi-agent shapes across the collection: supervisor/coordinator + specialist workers (ATLAS academic system: Coordinator/Planner/Notewriter/Advisor), role-based crews (AutoGen research team: admin/developer/planner/executor/QA; OpenAI Swarm blog team: researcher/planner/writer/editor), and CrewAI inventory agents [^src4]. The catalog also pairs with companion resources on RAG (40+ notebooks) and agent memory (30 notebooks on vector stores, graphs, Mem0, Zep) — see [Agent Memory](/ai-engineering/agent-memory.md) [^src4].

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

## pi-subagents: open-source async subagent system

**pi-subagents** (`pi install npm:pi-subagents`) is an open-source Pi extension that adds eight specialized built-in agents, each scoped to a distinct role [^src7]:

| Agent | Role | Notes |
|---|---|---|
| **scout** | Fast local reconnaissance | File reads, grep, structure — doesn't write code |
| **researcher** | Web and docs research | Searches external sources; returns findings |
| **planner** | Implementation planning | Produces a plan only; never edits code |
| **worker** | Implements + validates | Writes code, runs checks, escalates if blocked |
| **reviewer** | Code review + small fixes | Returns findings with severity; can apply nits |
| **context-builder** | Builds `context.md` + `meta-prompt.md` | Prepares session context for subsequent agents |
| **oracle** | Second opinion / devil's advocate | Challenges assumptions; never edits code |
| **delegate** | Lightweight general-purpose | Quick tasks that don't fit a specialist role |

**Key patterns** [^src7]:
- **Parallel reviewers**: run multiple reviewer agents on the same code simultaneously (e.g. security-lens reviewer + correctness reviewer), then merge findings — the same adversarial verification pattern as [Generator–Evaluator Separation](/ai-engineering/generator-evaluator-separation.md).
- **Review loops**: worker → reviewer → worker cycle until reviewer is satisfied.
- **Foreground vs background**: agents can run in the background while you continue working.
- **Model overrides**: each agent can be assigned a different model (e.g. planner on Opus, worker on Sonnet).

## When to use multi-agent systems (Anthropic guidance)

Anthropic identifies three core justifications for adding agents to a system [^src10]:

1. **Context pollution** — a single-agent task accumulates too much irrelevant context over many turns, degrading quality. Subagents with bounded context windows solve this: each agent gets only the context it needs for its subtask. Example: a code search agent reads dozens of files; its synthesized finding returns to the main agent, not the raw file contents.
2. **Parallelization** — independent subtasks can run concurrently, reducing wall-clock time. Example: N unit tests written in parallel, or N files analyzed simultaneously.
3. **Specialization** — tasks require different expertise, models, or permission scopes. Example: a planning agent uses Opus 4.8 (deeper reasoning); an execution agent uses Sonnet 4.6 (faster, cheaper); a verification agent gets read-only permissions.

**Token cost trade-off** [^src10]: multi-agent systems use 3–10× more tokens than a single-agent approach for the same task. The additional cost is justified only when the quality or speed gains justify it — context pollution, true parallelism, or specialization requirements must be present.

**Context-centric vs problem-centric decomposition** [^src10]: the standard instinct is to decompose by problem domain ("have a research agent and a writing agent"). A more principled approach is to decompose by context: "what information does each phase need, and would co-mingling that information hurt quality?" This produces tighter agent boundaries with less irrelevant context leakage.

**Verification subagent pattern** [^src10]: add an explicit verification agent whose only job is to check the primary agent's output against criteria. The key property: "the verifier runs in its own context window, so it is not influenced by the reasoning the primary agent used to produce the output." This is the Generator-Verifier pattern (§ Five coordination patterns) applied as a default component. Without it, the primary agent tends to verify its own work using the same reasoning that produced it — the self-preferential bias that [Dynamic Workflows](/ai-engineering/claude-code.md) was designed to counter.

**Tool Search Tool (85% token reduction)** [^src10]: loading all tool definitions upfront costs disproportionate tokens when only a fraction of tools are used per turn. The Tool Search Tool loads tool definitions on demand: the model describes what capability it needs; the Tool Search Tool returns matching tool definitions; the model calls the tool. In Anthropic's testing this reduces tool-definition tokens by 85%+ while maintaining high selection accuracy. See [MCP](/ai-engineering/mcp.md) (§ Client-side context efficiency) for the same optimization applied to MCP tool sets.

## 30-40 parallel task pattern (Notion)

The Notion case study (Eric Liu, PM) documents a production implementation where **30-40 agent tasks run simultaneously** inside Notion's task board [^src8]. The orchestrator pattern: a Notion "ready to start" column triggers individual Claude sessions per task; team members collaborate on shared output in real time. Claude picks up context from connected design system, API docs, and PRDs automatically. "12 hours of prototyping work collapse into about 20 minutes." — This is the orchestrator-subagent pattern (§ above) at production scale, with the orchestrator being the task board state machine rather than a Claude agent itself.

## Factory Missions (production multi-agent coding system)

Factory (company: Luke Alvoeiro) ships **Missions** — a production multi-agent system for enterprise software development. It provides a concrete architecture for how multi-agent systems actually ship code at enterprise scale [^src13].

### 5 communication patterns

Factory identifies five patterns for how agents communicate, with distinct selection criteria [^src13]:

| Pattern | Description | When to use |
|---|---|---|
| **1. Delegation** | Orchestrator assigns work to a worker; worker completes and returns | Default pattern; clear task decomposition, bounded output |
| **2. Creator-Verifier** | One agent creates; a separate agent verifies against criteria | Quality-critical output; evaluation criteria can be made explicit |
| **3. Direct Communication** | Two agents message each other without orchestrator mediation | Tight collaboration where intermediate orchestration adds latency |
| **4. Negotiation** | Agents iterate back-and-forth to resolve ambiguity or tradeoffs | Competing constraints (speed vs. quality, coverage vs. precision) |
| **5. Broadcast** | One agent publishes to many receivers | Status updates, context that all workers need simultaneously |

### 3-role architecture (Orchestrator / Workers / Validators)

Factory Missions uses three role types, not two [^src13]:

- **Orchestrator** — plans the mission, decomposes into tasks, assigns to workers, aggregates results
- **Workers** — execute bounded tasks; each worker owns a specific piece of the codebase or workflow
- **Validators** — two independent validator types:
  - **Scrutiny validators**: tests, lint, code-review agents — automated correctness checks
  - **User-testing validators**: computer-use agents that fill forms, click buttons, navigate flows — behavioral correctness checks

### Validation contract written during planning

The key discipline: the **validation contract is written during the planning phase, before any code is written** [^src13]. The contract defines what "correct" means independently of the implementation — so validators are not influenced by the implementation choices and cannot rationalize a wrong implementation as "good enough."

This is the same generator-evaluator separation principle as the Anthropic taxonomy above (§ Five coordination patterns, Generator-Verifier), extended to two validator types (automated + behavioral).

### Serial execution with internal parallelism

Factory Missions runs worker tasks **serially by default** with internal parallelism only for read-only operations [^src13]. The reasoning: parallel writes to the same codebase cause merge conflicts; serial writes with structured handoffs between workers eliminate the conflict surface. Read-only phases (analysis, search, context-gathering) run in parallel within each serial task.

The longest Factory Mission documented: **16 days** — a single coordinated run with workers handing off context through structured artifacts [^src13].

### Droid whispering

"**Droid whispering**" is the Factory team's term for the skill of selecting the right model for each role in a multi-agent system [^src13]. Different agents benefit from different model strengths: a planner might use Opus (deep reasoning); a search/indexing worker might use Sonnet (speed, cost); a validator might use a specialized code-eval model. Getting this assignment right is presented as a craft skill, not a configuration detail.

### Mission Control UI

Factory provides a **Mission Control** visual interface showing each agent, its current state, task assignments, and the full handoff log — the same monitoring problem that motivates [OpenClaw](/ai-engineering/openclaw.md)'s Mission Control and [Paperclip](/ai-engineering/paperclip.md)'s project-management UI [^src13].

## See also

- [AI Agent](/ai-engineering/ai-agent.md) — single-agent building block
- [Agent Skills](/ai-engineering/agent-skills.md) — the skills a sub-agent should carry before it's worth creating
- [LangGraph](/ai-engineering/langgraph.md) — recommended framework for stateful multi-agent workflows
- [MCP](/ai-engineering/mcp.md) — coordination protocol for tool calls, memory, and context sharing across agents
- [Claude Code](/ai-engineering/claude-code.md) — subagent invocation patterns, custom agent definitions, Agent Teams
- [Agent Harness](/ai-engineering/agent-harness.md) — the harness layer that enables multi-agent orchestration

---

[^src1]: [AI Agents - Complete Course Beginner to Pro](/03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md)
[^src2]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src3]: [How Grab Reclaimed Hundreds of Data Engineering Hours With Multi-Agent AI](../../raw/email/email-2026-05-28-how-grab-reclaimed-hundreds-of-data-engineering-hours-with-m.md) — Chief Data Tinkerer
[^src4]: [NirDiamant/GenAI_Agents — 52+ tutorials and implementations](../../raw/web/github-nirdiamant-genai-agents-50-tutorials-and-implementati.md) — GitHub
[^src5]: [How and when to use subagents in Claude Code](../../raw/notes/notes-clippings-how-and-when-to-use-subagents-in-claude-code.md) — Anthropic
[^src6]: [Multi-agent coordination patterns: Five approaches and when to use them](../../raw/notes/notes-clippings-multi-agent-coordination-patterns-five-approaches-and-when-t.md) — Cara Phillips et al., Anthropic
[^src7]: [pi-subagents — Pi extension for async subagents (GitHub)](../../raw/web/web-github-nicobailon-pi-subagents-pi-extension-for-async-subage.md) — nicobailon
[^src8]: [Notion Q&A — Claude Managed Agents](../../raw/web/web-notion-q-a-claude-managed-agents-claude-by-anthropic.md) — Eric Liu, Notion PM
[^src9]: [crewAIInc/crewAI-examples — Official CrewAI workflow examples (6K★)](../../raw/github/github-crewaiinc-crewai-examples.md) — crewAIInc, GitHub
[^src10]: [When to use multi-agent systems — and when not to](../../raw/web/web-when-to-use-multi-agent-systems-and-when-not-to-claude.md) — Anthropic
[^src11]: [Local AI Agents In 26 Minutes](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md) — Tina Huang, YouTube
[^src12]: [Paperclip: Agent Collab Made Easy](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md) — The Next New Thing, YouTube
[^src13]: [The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro (Factory)](../../raw/_inbox/youtube-ow1we5PzK-o-the-multi-agent-architecture-that-actually-ships-luke-alvoei.md) — AI Engineer channel, YouTube
[^src14]: [Build 3 PRODUCTION AI Agents in Python — Full Course (AgentSpan)](../../raw/_inbox/youtube-zFw19qGAeGo-build-3-production-ai-agents-in-python-full-course-agentspan.md) — Tech With Tim, YouTube

## AgentSpan: production Python multi-agent framework

AgentSpan (from Orcs) is an open-source, free Python framework designed around the 7 requirements for production-ready AI agents [^src14]:

**Seven production requirements** [^src14]:
1. **Durability** — if the agent crashes, it recovers and continues (not restarts from scratch)
2. **Retries** — failed steps retry automatically before exiting
3. **Human-in-the-loop** — agents can delegate back to a human (approve task, press button) and wait
4. **Observability** — real-time dashboard of agent state, tool calls, tokens, duration per step
5. **Long-running tasks** — handles 20-minute to 2-hour tasks natively; no timeouts
6. **Scale** — built-in queue system for running many agents concurrently
7. **Testing** — repeatable test flows

**Architecture** [^src14]: Worker (code you write) + AgentSpan server (handles state, orchestration, retries). The server stores all agent state — if the worker crashes, it reconnects and continues from the last checkpoint. Works with LangGraph, OpenAI SDK, Google ADK, or AgentSpan's own Python framework.

**Three agent types built in the course** [^src14]:
1. Conversational agent with memory
2. RAG-based agent (queries a structured knowledge source)
3. Multi-agent orchestrator running agents concurrently toward a shared goal

**Observability dashboard** includes: full log per agent, clickable turn-by-turn inspection (input, output, JSON, summary), token counts, reason-for-stop, duration [^src14]. This is the visibility property that simple LangChain agents lack — you have no idea what's happening without it.

**Deployment**: deploy the AgentSpan server + your workers. Infrastructure concern collapses to those two things; no need to rebuild queue, retry, or state-persistence infrastructure from scratch [^src14].

## Cross-LLM MCP orchestration (platform routing)

A 2026 practitioner pattern uses Claude as the **orchestrator** while other LLMs serve as **specialized workers** connected via MCP, each routed by capability strength [^src15]:

| Role | Model | Primary strength |
|---|---|---|
| Orchestrator | Claude (Sonnet/Opus) | Interpretability, context reading, orchestration judgment |
| UI/frontend worker | Gemini | Frontend/multimodal generation |
| Backend/TDD worker | GPT/Codex (OpenAI) | Backend code, test-driven development |

Each worker connects via its own MCP server; Claude routes tasks by matching the task type to model strength. This is the orchestrator-subagent pattern (§ above) extended across different LLM providers rather than being confined to one [^src15].

**When to use this pattern**: tasks that have genuinely distinct subtask types that benefit from different model capabilities (e.g., a full-stack feature requiring UI design, API code, and test generation). For homogeneous workloads, sticking to one model is simpler [^src15].

## Self-modifying agent instruction files

Multi-agent systems can compound their quality over time through self-modification of per-platform instruction files [^src15]:

1. **Human corrects agent output** ("Don't structure it like that, do it like this")
2. **Agent appends the preference rule** to its instruction file (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`)
3. **Rule loads at next session start** — the agent doesn't repeat the mistake

In a cross-model setup, each model maintains its own instruction file. Over time, each file becomes a behavioral profile for that model's role in the system — preferences discovered through correction accumulate without requiring prompts to repeat them [^src15].

This is the organizational analog of the "compounds across sessions" property of [Agent Memory](/ai-engineering/agent-memory.md) applied to behavioral conventions rather than factual context. See [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md) for the file format.

[^src15]: [AI Agents Full Course 2026 — Master Agentic AI (2 hours)](../../raw/_inbox/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md) — Nick Saraev, YouTube, 2026; cross-LLM MCP orchestration, self-modifying instruction files
