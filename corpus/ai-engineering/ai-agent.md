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
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
  - path: raw/web/agent-mode-autonomous-ai-agents-for-real-world-tasks.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-13-agents-in-action-1-what-is-an-ai-agent.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/web/github-pickle-pixel-applypilot-ai-agent-that-applies-to-jobs.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-q00-ouroboros-agent-os-stop-prompting-start-specifyin.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/episode-295-agentic-architecture-why-files-aren-t-always-eno.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/pi-coding-agent.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/pi-coding-agent-2ef78af5.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/pi-coding-agent-49b08ba6.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-10-how-to-build-a-serverless-ai-agent-with-pi.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/github-mvanhorn-last30days-skill-ai-agent-skill-that-researc.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/youtube/youtube-kwSVtQ7dziU-skill-issue-andrej-karpathy-on-code-agents-autoresearch-and.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - ai agent
  - agentic AI
  - LLM agent
  - agent mode
  - autonomous agent
  - agent OS
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-12
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

## Mental model: agents are new employees, not magic boxes

A complementary framing for *working with* agents [^src4]: LLMs don't reason the way humans do — they **predict tokens**, mapping input onto a vector space and returning the closest resemblance. The implication is operational, not philosophical: an agent "will mimic you perfectly, but you've given it nothing to mimic" unless you supply a worked example. So treat a new agent like a **new employee** — give it the workflow, let it fail, correct it, and codify the result (see [[ai-engineering/agent-skills|Agent Skills]] for the recursive skill-building loop this motivates).

The same source reframes capability: with strong models, differentiation now comes from **the harness, tools, and context** around the model, plus the user's unique workflow — not from model choice alone [^src4]. See [[ai-engineering/context-engineering|Context Engineering]].

## Production concerns

- **Security**: sandbox code execution (Docker, strict limits); whitelist safe libraries; validate inputs, scan outputs for PII/keys [^src1]
- **Reliability**: circuit breakers for infinite loops; retry with exponential backoff; structured outputs over raw text [^src1]
- **Quality/latency/cost triangle**: more powerful model = better quality + higher cost; parallel agents = lower latency + higher cost; caching = lower cost + potential staleness [^src1]

## Agent mode & autonomous task agents

"Agent mode" is the productized form of the agent loop: a single chat surface ("What would you like to do?") that accepts a goal and runs autonomously toward it [^src5]. The pattern's reach is shown by **ApplyPilot**, a fully autonomous, open-source job-application agent that "applied to 1,000 jobs in 2 days" via a 6-stage pipeline — discover, enrich, score, tailor, cover-letter, auto-apply [^src6]. Its auto-apply stage is concrete agentic execution: Claude Code drives a Chrome instance through a Playwright MCP server, navigating forms, uploading documents, answering screening questions, and submitting hands-free [^src6]. Design notes worth generalizing [^src6]:

- **Staged + independent**: each stage runs alone or as a pipeline, with a `--dry-run` that fills forms without submitting — a safety gate for autonomous browser action.
- **Parallelism via workers** (`-w N`) for both discovery and browser submission.
- **Bounded fabrication**: the resume-tailoring stage reorganizes and emphasizes but "never fabricates" — a guardrail baked into the prompt contract.

The quality/latency/cost triangle and the security concerns below apply directly to such autonomous agents (CAPTCHA-blocked applications "fail gracefully" rather than escalating) [^src6].

Another agent-mode pattern is **agent-as-search-orchestrator**: `/last30days` is a skill that, given any topic, has the agent first *resolve who matters* (X handles, GitHub repos, subreddits, YouTube channels) and then fan out parallel searches across a dozen walled-garden platforms (Reddit, X, YouTube, TikTok, HN, Polymarket, GitHub), scoring results by real engagement and synthesizing one cited brief [^src11]. The framed unlock is exactly the agentic loop applied to retrieval: "Not one better search engine. A dozen disconnected platforms, bridged by an agent" — each platform has its own API and auth, but an agent with the user's keys can query them all at once [^src11]. It runs cross-harness via the open Agent Skills CLI (50+ hosts) and is distributed as both a Claude Code marketplace plugin and an `npx skills` package (see [[ai-engineering/agent-skills|Agent Skills]]) [^src11]. This is also a concrete [[ai-engineering/agentic-search|Agentic Search]] instance.

## The agent harness: minimal, self-modifying runtimes

A growing view holds that with strong models, differentiation comes from the **harness** — the runtime, tools, and context around the model — not the model alone (see [[ai-engineering/context-engineering|Context Engineering]]). **Pi** is an open-source exemplar: "a minimal agent harness" whose thesis is "adapt Pi to your workflows, not the other way around" [^src7]. Defining properties [^src7]:

- **Skips defaults like sub-agents and plan mode** — you ask Pi to build them, or install a package that adds them. Extensions are TypeScript modules with access to tools, commands, events, and the TUI.
- **Self-modifying**: "Have Pi manipulate itself in place, hit `/reload`, and keep going." The agent can add its own commands, tools, and providers on the fly.
- **Four run modes**: interactive TUI, print/JSON (for scripts), RPC (JSON over stdin/stdout), and SDK (embed in apps).
- **Context-engineering surface**: minimal system prompt, `AGENTS.md` project instructions, `SYSTEM.md` per-project prompt override, customizable compaction, and on-demand skills with progressive disclosure that doesn't bust the prompt cache [^src7].

This harness is deployable as a **serverless agent**: app code is separated from cloud memory (GitHub for app/agent files, cloud object storage for data), wrapped in a thin web chat UI, and deployed to a cloud run target with shared-password protection [^src8]. Pi is also a first-class backend in multi-runtime tools like Boring UI (see [[ai-engineering/agent-ui|Agent UI]]) and Ouroboros (below).

## Spec-driven agent OS

A distinct architectural layer treats agent work as an **operating system**: a replayable, observable, policy-bound execution contract rather than ad-hoc prompting. **Ouroboros** is "the Agent OS for replayable, specification-first AI coding workflows" with a five-phase loop — **interview → seed → execute → evaluate → evolve** [^src9]. Core ideas [^src9]:

- **"Most AI coding fails at the input, not the output"** — the bottleneck is human clarity, not model capability. A Socratic interview exposes hidden assumptions before any code is written.
- **Two mathematical gates**: an *Ambiguity Score* (≤ 0.2 weighted-clarity threshold) must be met before a Seed spec is generated; an *Ontology Convergence* score (≥ 0.95 similarity across generations) decides when the evolutionary loop stops.
- **Immutable seed spec** locks intent so architecture doesn't drift mid-build; a 3-stage evaluation gate (Mechanical → Semantic → Multi-Model Consensus) replaces "looks good" QA.
- **OS layering**: a stable kernel (Seed, Ledger, Runtime, MCP) under user-level plugins (PR ops, Jira sync, releases) under a terminal shell — every action becomes a ledger-recorded, replayable event regardless of which LLM executes it [^src9].

Ouroboros and Pi both target **runtime portability** — one workflow spec, many execution engines (Claude Code, Codex, Gemini, Copilot, Pi, and more) [^src7][^src9]. This is the agent-side analog of the cross-platform convention work in [[ai-engineering/claude-md-conventions|CLAUDE.md & Agent Instruction Conventions]].

## Agents for data engineers

An introductory framing of agents specifically for the DE context [^src12]:

**The agent loop** (observe → decide → act → incorporate → repeat):
1. **Observe** — the agent reads its current state: query results, error messages, file contents, tool outputs.
2. **Decide** — based on observation, it chooses the next action (call a tool, write a file, run a query).
3. **Act** — executes the decision (writes SQL, calls an API, moves a file).
4. **Incorporate** — adds the result back to the context window.
5. **Repeat** — until the goal state is reached or a stop condition fires.

**DAG vs agent**: a data pipeline DAG (Airflow, Prefect) is *static* — tasks are pre-defined; the graph doesn't change at runtime. An agent pipeline is *dynamic* — it decides the next step based on what it has observed so far. DAGs are better for high-reliability, predictable workflows; agents are better for exploratory, adaptive tasks (e.g. data quality investigation, schema discovery) [^src12].

**Autonomy levels** (not binary):
- Level 0: human executes each step with AI suggestions.
- Level 1: AI suggests; human approves before each action.
- Level 2: AI acts autonomously within a bounded scope (e.g. query optimization within one schema).
- Level 3: fully autonomous end-to-end (rare in production data environments today).

**Four building blocks** [^src12]:
1. **Tools** — functions the agent can call (run SQL, call API, read file, write file).
2. **MCP** — the protocol for connecting agents to tools and data stores without custom integration per tool. See [[ai-engineering/mcp|MCP]].
3. **Memory** — what the agent retains across steps: short-term (context window), long-term (vector DB, files, database rows). See [[ai-engineering/agent-memory|Agent Memory]].
4. **Sub-agents** — orchestration of specialized agents: one for schema discovery, one for SQL generation, one for QA, coordinated by a parent agent.

## Files vs database: the agent-memory architecture debate

A live debate concerns whether a folder of files is sufficient agent state, or whether agents need a database [^src10]. The "files are all you need" position (Karpathy's evolving-markdown LLM knowledge base, LlamaIndex) is contrasted with the limits of file-based workflows and **massive context windows that "tend to collapse"** as they fill [^src10]. The same source reinforces the **model-vs-harness** framing and "context rot and tool loadouts" as first-order concerns [^src10]. See [[ai-engineering/agent-memory|Agent Memory]] and [[ai-engineering/context-window-management|Context Window Management]] for the underlying mechanics.

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — the highest-leverage skill in agent development
- [[ai-engineering/agent-skills|Agent Skills]] — codifying workflow into on-demand skills; the recursive build loop
- [[ai-engineering/tool-calling|Tool Calling]] — how agents interact with tools
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — patterns for multiple cooperating agents
- [[ai-engineering/langgraph|LangGraph]] — recommended framework for production multi-agent systems
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: how tool results feed the context loop and why context engineering governs tool call design
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — full treatment of evaluation patterns
- [[ai-engineering/langsmith|LangSmith]] — platform for agent observability and evaluation
- [[ai-engineering/agent-memory|Agent Memory]] — short-term (context window) and long-term (vector DB) memory
- [[ai-engineering/mcp|MCP]] — coordination protocol for agents, tools, and memory
- [[ai-engineering/agent-ui|Agent UI]] — chat + workbench shells for agent-centric apps (Boring UI on Pi)
- [[ai-engineering/claude-md-conventions|CLAUDE.md & Agent Instruction Conventions]] — configuring the harness; cross-platform portability
- [[ai-engineering/agent-testing|Agent Testing]] — verification loops that keep autonomous agents honest
- [[data-engineering/README|Data Engineering]] — how agents are applied in data pipelines

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src2]: [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]]
[^src3]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
[^src4]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src5]: [Agent Mode — Autonomous AI Agents for Real-World Tasks](../../raw/web/agent-mode-autonomous-ai-agents-for-real-world-tasks.md)
[^src6]: [Pickle-Pixel/ApplyPilot — AI agent that applies to jobs](../../raw/web/github-pickle-pixel-applypilot-ai-agent-that-applies-to-jobs.md)
[^src7]: [Pi — a minimal agent harness](../../raw/web/pi-coding-agent.md)
[^src8]: [How to Build a Serverless AI Agent with Pi](../../raw/email/email-2026-06-10-how-to-build-a-serverless-ai-agent-with-pi.md)
[^src9]: [Q00/ouroboros — the Agent OS for spec-first AI coding workflows](../../raw/web/github-q00-ouroboros-agent-os-stop-prompting-start-specifyin.md)
[^src10]: [Episode 295: Agentic Architecture — Why Files Aren't Always Enough](../../raw/web/episode-295-agentic-architecture-why-files-aren-t-always-eno.md)
[^src11]: [mvanhorn/last30days-skill — AI agent skill that researches any topic across platforms](../../raw/web/github-mvanhorn-last30days-skill-ai-agent-skill-that-researc.md) — GitHub
[^src12]: [Agents in Action #1 — What is an AI Agent? (Pipeline to Insights)](../../raw/email/email-2026-06-13-agents-in-action-1-what-is-an-ai-agent.md)
[^src13]: [Skill Issue: Andrej Karpathy on Code Agents, Auto-Research, and...](../../raw/youtube/youtube-kwSVtQ7dziU-skill-issue-andrej-karpathy-on-code-agents-autoresearch-and.md) — No Priors podcast, YouTube
