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
  - path: raw/github/github-aaif-goose-goose.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube--QznXY_pJvw-ai-agents-love-clis.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/_inbox/youtube-kwRTUw8pb2c-agentic-ai-systems-clearly-explained.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-ZaPbP9DwBOE-don-t-learn-ai-agents-without-learning-these-fundamentals.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-LNkAW4SSgdY-the-complete-guide-to-ai-agents-in-2026-and-how-to-actually.md
    channel: youtube
    ingested_at: 2026-06-29
  - path: raw/_inbox/youtube-sNvuH-iTi4c-ai-agents-in-38-minutes-complete-course-from-beginner-to-pro.md
    channel: youtube
    ingested_at: 2026-06-30
  - path: raw/_inbox/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md
    channel: youtube
    ingested_at: 2026-06-30
  - path: raw/_inbox/youtube-d5tfH90-zNk-the-basics-of-ai-agents.md
    channel: youtube
    ingested_at: 2026-06-30
  - path: raw/_inbox/youtube-UsfpzxZNsPo-python-essentials-for-ai-agents-tutorial.md
    channel: youtube
    ingested_at: 2026-06-30
  - path: raw/_inbox/youtube-MnG0ugK2JAI-build-your-own-ai-agent-full-course-with-openai-langchain-re.md
    channel: youtube
    ingested_at: 2026-06-30
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

## 4-level agentic framework

A taxonomy for categorizing the sophistication of an AI system, from passive chatbots to autonomous multi-agent harnesses [^src17]:

| Level | Name | Characteristics |
|---|---|---|
| **1** | Chatbot | Passive, static, one-turn response. Waits for input; no memory, no tool use, no autonomy. Classic chat interface. |
| **2** | AI Workflow | Deterministic automation pipeline (N8N, Zapier, Make). Steps are pre-defined by the human. The LLM processes at defined nodes, but the control flow is fixed — no branching or model-driven decisions. |
| **3** | Agentic Workflow | Model decides the execution path. Uses the **ReAct loop** (Reason + Act): the LLM reasons about what to do, calls a tool, observes the result, reasons again, repeats. Claude Code, Codex, Cursor are Level 3. |
| **4** | Agentic AI System | Full autonomous runtime: harness + persistent memory + skill library + MCP tool access + long-running session. The agent can run for hours/days without human input. Hermes, OpenClaw, Claude Managed Agents are Level 4. |

**Key boundaries**:
- Level 1→2: determinism added (structured workflow, not one-shot response)
- Level 2→3: model makes control-flow decisions (non-deterministic execution path)
- Level 3→4: persistence and compounding memory (the agent remembers across sessions and self-improves)

Level 3 vs. Level 4 is where practitioners diverge in tooling choices: Level 3 uses embedded code agents (Claude Code inside your IDE); Level 4 uses standalone harnesses that run continuously on a VPS or cloud environment [^src17].

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

See [Agent Evaluation](/ai-engineering/agent-evaluation.md) for full treatment of evaluation patterns, golden datasets, and the production feedback loop.

## Mental model: agents are new employees, not magic boxes

A complementary framing for *working with* agents [^src4]: LLMs don't reason the way humans do — they **predict tokens**, mapping input onto a vector space and returning the closest resemblance. The implication is operational, not philosophical: an agent "will mimic you perfectly, but you've given it nothing to mimic" unless you supply a worked example. So treat a new agent like a **new employee** — give it the workflow, let it fail, correct it, and codify the result (see [Agent Skills](/ai-engineering/agent-skills.md) for the recursive skill-building loop this motivates).

The same source reframes capability: with strong models, differentiation now comes from **the harness, tools, and context** around the model, plus the user's unique workflow — not from model choice alone [^src4]. See [Context Engineering](/ai-engineering/context-engineering.md).

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

Another agent-mode pattern is **agent-as-search-orchestrator**: `/last30days` is a skill that, given any topic, has the agent first *resolve who matters* (X handles, GitHub repos, subreddits, YouTube channels) and then fan out parallel searches across a dozen walled-garden platforms (Reddit, X, YouTube, TikTok, HN, Polymarket, GitHub), scoring results by real engagement and synthesizing one cited brief [^src11]. The framed unlock is exactly the agentic loop applied to retrieval: "Not one better search engine. A dozen disconnected platforms, bridged by an agent" — each platform has its own API and auth, but an agent with the user's keys can query them all at once [^src11]. It runs cross-harness via the open Agent Skills CLI (50+ hosts) and is distributed as both a Claude Code marketplace plugin and an `npx skills` package (see [Agent Skills](/ai-engineering/agent-skills.md)) [^src11]. This is also a concrete [Agentic Search](/ai-engineering/agentic-search.md) instance.

## The agent harness: minimal, self-modifying runtimes

A growing view holds that with strong models, differentiation comes from the **harness** — the runtime, tools, and context around the model — not the model alone (see [Context Engineering](/ai-engineering/context-engineering.md)). **Pi** is an open-source exemplar: "a minimal agent harness" whose thesis is "adapt Pi to your workflows, not the other way around" [^src7]. Defining properties [^src7]:

- **Skips defaults like sub-agents and plan mode** — you ask Pi to build them, or install a package that adds them. Extensions are TypeScript modules with access to tools, commands, events, and the TUI.
- **Self-modifying**: "Have Pi manipulate itself in place, hit `/reload`, and keep going." The agent can add its own commands, tools, and providers on the fly.
- **Four run modes**: interactive TUI, print/JSON (for scripts), RPC (JSON over stdin/stdout), and SDK (embed in apps).
- **Context-engineering surface**: minimal system prompt, `AGENTS.md` project instructions, `SYSTEM.md` per-project prompt override, customizable compaction, and on-demand skills with progressive disclosure that doesn't bust the prompt cache [^src7].

This harness is deployable as a **serverless agent**: app code is separated from cloud memory (GitHub for app/agent files, cloud object storage for data), wrapped in a thin web chat UI, and deployed to a cloud run target with shared-password protection [^src8]. Pi is also a first-class backend in multi-runtime tools like Boring UI (see [Agent UI](/ai-engineering/agent-ui.md)) and Ouroboros (below).

## Spec-driven agent OS

A distinct architectural layer treats agent work as an **operating system**: a replayable, observable, policy-bound execution contract rather than ad-hoc prompting. **Ouroboros** is "the Agent OS for replayable, specification-first AI coding workflows" with a five-phase loop — **interview → seed → execute → evaluate → evolve** [^src9]. Core ideas [^src9]:

- **"Most AI coding fails at the input, not the output"** — the bottleneck is human clarity, not model capability. A Socratic interview exposes hidden assumptions before any code is written.
- **Two mathematical gates**: an *Ambiguity Score* (≤ 0.2 weighted-clarity threshold) must be met before a Seed spec is generated; an *Ontology Convergence* score (≥ 0.95 similarity across generations) decides when the evolutionary loop stops.
- **Immutable seed spec** locks intent so architecture doesn't drift mid-build; a 3-stage evaluation gate (Mechanical → Semantic → Multi-Model Consensus) replaces "looks good" QA.
- **OS layering**: a stable kernel (Seed, Ledger, Runtime, MCP) under user-level plugins (PR ops, Jira sync, releases) under a terminal shell — every action becomes a ledger-recorded, replayable event regardless of which LLM executes it [^src9].

Ouroboros and Pi both target **runtime portability** — one workflow spec, many execution engines (Claude Code, Codex, Gemini, Copilot, Pi, and more) [^src7][^src9]. This is the agent-side analog of the cross-platform convention work in [CLAUDE.md & Agent Instruction Conventions](/ai-engineering/claude-md-conventions.md).

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
2. **MCP** — the protocol for connecting agents to tools and data stores without custom integration per tool. See [MCP](/ai-engineering/mcp.md).
3. **Memory** — what the agent retains across steps: short-term (context window), long-term (vector DB, files, database rows). See [Agent Memory](/ai-engineering/agent-memory.md).
4. **Sub-agents** — orchestration of specialized agents: one for schema discovery, one for SQL generation, one for QA, coordinated by a parent agent.

## Files vs database: the agent-memory architecture debate

A live debate concerns whether a folder of files is sufficient agent state, or whether agents need a database [^src10]. The "files are all you need" position (Karpathy's evolving-markdown LLM knowledge base, LlamaIndex) is contrasted with the limits of file-based workflows and **massive context windows that "tend to collapse"** as they fill [^src10]. The same source reinforces the **model-vs-harness** framing and "context rot and tool loadouts" as first-order concerns [^src10]. See [Agent Memory](/ai-engineering/agent-memory.md) and [Context Window Management](/ai-engineering/context-window-management.md) for the underlying mechanics.

## Goose: open-source agentic framework (AAIF)

Goose (★50K GitHub) is an open-source general-purpose agentic AI framework, transferred to the Agentic AI Foundation (AAIF) at the Linux Foundation [^src14]. Originally built by Anthropic + Block, now community-governed.

Key properties [^src14]:
- Written in Rust (performance + memory safety for long-running agents)
- 15+ model providers supported (Anthropic, OpenAI, Gemini, local Ollama, etc.)
- Supports both MCP (Model Context Protocol) and ACP (Agent Communication Protocol) for inter-agent messaging
- Designed for tool-using, long-horizon tasks
- Extension marketplace for community tools
- CLI-first; runs in terminal

**ACP (Agent Communication Protocol)**: a layer on top of HTTP that lets agents communicate with each other in a structured way. Enables multi-agent coordination without a custom orchestration layer [^src14]. Distinct from MCP (which connects agents to tools/data); ACP connects agents to other agents.

## See also

- [Context Engineering](/ai-engineering/context-engineering.md) — the highest-leverage skill in agent development
- [Agent Skills](/ai-engineering/agent-skills.md) — codifying workflow into on-demand skills; the recursive build loop
- [Tool Calling](/ai-engineering/tool-calling.md) — how agents interact with tools
- [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) — patterns for multiple cooperating agents
- [LangGraph](/ai-engineering/langgraph.md) — recommended framework for production multi-agent systems
- [Tool Calling & Context Engineering](/ai-engineering/tool-calling-and-context-engineering.md) — synthesis: how tool results feed the context loop and why context engineering governs tool call design
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — full treatment of evaluation patterns
- [LangSmith](/ai-engineering/langsmith.md) — platform for agent observability and evaluation
- [Agent Memory](/ai-engineering/agent-memory.md) — short-term (context window) and long-term (vector DB) memory
- [MCP](/ai-engineering/mcp.md) — coordination protocol for agents, tools, and memory
- [Agent UI](/ai-engineering/agent-ui.md) — chat + workbench shells for agent-centric apps (Boring UI on Pi)
- [CLAUDE.md & Agent Instruction Conventions](/ai-engineering/claude-md-conventions.md) — configuring the harness; cross-platform portability
- [Agent Testing](/ai-engineering/agent-testing.md) — verification loops that keep autonomous agents honest
- [Data Engineering](/data-engineering/README.md) — how agents are applied in data pipelines

---

[^src1]: [AI Agents - Complete Course Beginner to Pro](/03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md)
[^src2]: [LangSmith - Debugging and Evaluating AI Agents](/03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md)
[^src3]: [AI Dev - Agentic AI Architecture Explained](/03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained.md)
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
[^src14]: [aaif-goose/goose — Goose AI agent (★50K)](../../raw/github/github-aaif-goose-goose.md) — AAIF / Linux Foundation, GitHub
[^src15]: [AI Agents LOVE CLIs](../../raw/youtube/youtube--QznXY_pJvw-ai-agents-love-clis.md) — Maximilian Schwarzmüller, YouTube
[^src16]: [Agents in Action #1 — What is an AI Agent?](../../raw/email/email-2026-06-13-agents-in-action-1-what-is-an-ai-agent.md) — Pipeline to Insights email
[^src17]: [Agentic AI Systems Clearly Explained](../../raw/youtube/youtube-kwRTUw8pb2c-agentic-ai-systems-clearly-explained.md) — Simon Scrapes, YouTube; 4-level framework (chatbot→workflow→agentic-workflow→agentic-AI-system)
[^src18]: [Don't Learn AI Agents Without Learning These Fundamentals](../../raw/youtube/youtube-ZaPbP9DwBOE-don-t-learn-ai-agents-without-learning-these-fundamentals.md) — KodeKloud, YouTube; corroborates core loop, component architecture, and agent vs simple LLM call decision criteria
[^src19]: [The Complete Guide to AI Agents in 2026 (and How to Actually Build One)](../../raw/youtube/youtube-LNkAW4SSgdY-the-complete-guide-to-ai-agents-in-2026-and-how-to-actually.md) — Tech With Tim, YouTube; 4-level framework (chat→tools→workflows→agents), corroborates framework from [^src17]
[^src20]: [AI Agents in 38 Minutes — Complete Course from Beginner to Pro](../../raw/youtube/youtube-sNvuH-iTi4c-ai-agents-in-38-minutes-complete-course-from-beginner-to-pro.md) — Marina Wyss (Senior Applied Scientist, Amazon), YouTube, Dec 2025; complexity/precision matrix, task decomposition, guardrails, ReAct loop, 4 design patterns
[^src21]: [AI Agents Full Course 2026 — Master Agentic AI (2 hours)](../../raw/youtube/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md) — Nick Saraev, YouTube, 2026; MCP multi-model orchestration, self-modifying AGENTS.md, platform comparison

## Why AI agents love CLIs (the GUI → CLI reversal)

A historical inversion: computing went from terminal UIs (1970s) to rich GUIs (1990s–2000s), but AI agents are driving a trend *back* to text-only, terminal-first interaction [^src15].

**Why CLIs fit agents better than GUIs** [^src15]:
- GUI interaction requires screenshot → locate element → click → screenshot again — token-intensive and slow
- Agents have been RL-trained on vast CLI usage: standard Linux commands, piping, chaining, `--help` discovery
- CLIs are just thin wrappers around APIs — the same principle that drove API-first design in traditional software applies here
- Agents can use `--help` to learn a completely new CLI tool even if it wasn't in training data

**The trend** [^src15]: more companies are releasing CLIs to make their services agent-accessible. Example: Google released the Google Workspace CLI in early 2026 specifically because existing tools (Gawk CLI by Peter Steinberger) had demonstrated demand before an official one existed. MCP servers fill the same role where no CLI exists — but CLIs are predicted to be the dominant integration pattern long-term.

**Practical implication** [^src15]: "They also saw that they can use `--help` to learn more about a tool, and that puts them in a great position with new tools as well." Just pointing an agent at a CLI tool and telling it about `--help` is sufficient — no explicit instruction manual needed.

**Data format preference** [^src15]: agents prefer plain text → Markdown → JSON over rich HTML or binary formats. Documentation pages that offer a "copy as plain text" button are already optimized for agent consumption.

## Use-case selection matrix

A two-axis framework for deciding when an agent is worth building (Marina Wyss, Amazon Applied Science) [^src20]:

| | Low Precision | High Precision |
|---|---|---|
| **High Complexity** | ⭐ Best early wins | ✓ High-value (legal, healthcare docs, financial compliance) |
| **Low Complexity** | Overkill | Simple automation (no agent needed) |

**Best starting point**: high complexity + lower precision. You get agent leverage on hard tasks without being blocked by needing perfect output every time [^src20].

Concrete examples: invoice extraction → database (high complexity, moderate precision); customer email response with account lookup (high complexity, lower precision for first draft); legal research with case citations (high complexity, high precision) [^src20].

## Task decomposition methodology

Marina Wyss's practitioner method for designing an agent's task steps [^src20]:

1. **Start with how you'd do the task yourself.** Write out the actual human workflow.
2. **For each step, ask: "Can an LLM do this?"** If no, split it smaller until yes.
3. **Each step should be small, checkable, and clear.** When output is poor, you know exactly which step to improve.

Example for essay writing → agent steps: generate outline (LLM), generate search terms (LLM), call web search API (tool), fetch pages (tool), write draft (LLM), self-critique draft (second LLM call), revise (LLM) [^src20].

The key property: each step's input and output are verifiable independently. Compare: "write an essay" (one opaque step, no diagnostic surface) vs. the decomposed version (6 steps, each inspectable) [^src20].

## Guardrails

Three types of quality gates between agent output and final delivery [^src20]:

| Type | What it checks | How |
|---|---|---|
| **Code snippets** | Deterministic: format, length, schema, required fields | Fast, cheap; prefer whenever the check can be expressed in code |
| **LLM judge** | Nuanced: factual consistency, tone, citation coverage | A second LLM rates output on a rubric; on failure, agent revises with the judge's explanation |
| **Human in the loop** | High-stakes: consequential decisions, public-facing content | Agent stops and asks for approval before continuing |

Most production systems use at least two types [^src20]. The LLM-judge pattern creates a self-correction loop: judge flags failure → agent gets explanation → agent revises and tries again [^src20].

See [Generator–Evaluator Separation](/ai-engineering/generator-evaluator-separation.md) for the principle behind the LLM-judge pattern, and [Agent Evaluation](/ai-engineering/agent-evaluation.md) for the full evaluation discipline.

## Multi-agent MCP orchestration (platform routing)

A multi-model architecture from Nick Saraev's 2026 course: Claude Code acts as orchestrator while other models serve as specialized workers connected via MCP [^src21]:

| Role | Model | Primary strength |
|---|---|---|
| Orchestrator | Claude (Sonnet/Opus) | Interpretability, context reading, orchestration |
| UI/frontend worker | Gemini | Frontend/multimodal tasks |
| Backend/TDD worker | GPT/Codex | Backend code, test-driven development |

Each model connects via its own MCP server; Claude routes tasks by matching capability fit. This instantiates the [orchestrator-subagent](/ai-engineering/multi-agent-systems.md) pattern across different LLM providers [^src21].

## Self-modifying agent instructions

Nick Saraev's pattern for compounding agent improvement over time [^src21]:

1. Human corrects an agent output
2. Agent appends the preference rule to its instruction file (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`)
3. Next session, the rule loads automatically — the agent doesn't repeat the mistake

Different platforms read different files: Claude reads `CLAUDE.md`, Gemini reads `GEMINI.md`, Codex reads `AGENTS.md`. In a multi-model setup, each model reads its own file and accumulates its own preference history [^src21]. See [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md).
