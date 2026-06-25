---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-w0S-khYCaB4-creating-your-own-agentic-os-is-easy-insanely-powerful.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-IVGjBxqygmI-why-ai-agents-need-an-operating-system.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-zElKhlFkqU4-5-skills-to-build-an-ai-operating-system-like-the-1-full-gui.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-DXcVT07bQ6g-what-is-an-ai-operating-system-and-why-every-business-will-n.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-ntvkDnk_5jA-how-to-build-a-personal-agentic-operating-system.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-0WDkwMxj13s-i-turned-claude-opus-4-8-into-my-entire-ai-operating-system.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-bCljOfCH8Ms-build-sell-claude-code-operating-systems-2-hour-course.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-vvDdTPFhCp8-how-to-build-your-ai-operating-system-with-claude-code-full.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-IevmGCVo9Pw-create-your-own-personal-claude-ai-system-that-makes-your-wo.md
    channel: youtube
    ingested_at: 2026-06-23
  - path: raw/youtube/youtube-JnQcPzjC6Vo-i-gave-pi-access-to-obsidian-and-i-m-not-looking-back.md
    channel: youtube
    ingested_at: 2026-06-21
  - path: raw/youtube/youtube-Bgxsx8slDEA-stop-using-claude-code-without-an-agentic-os.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-8QQ_INxAhRs-i-turned-claude-fable-into-the-ultimate-second-brain.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-how-to-build-your-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-claude-code-karpa-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-stop-using-claude-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-built-karpathy-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-kwSVtQ7dziU-skill-issue-andrej-karpathy-on-code-agents-autoresearch-and.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-pfPi04pIfaw-claude-code-agentic-os-unstoppable.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-h0HYpONXgjk-stop-using-obsidian-this-simple-second-brain-setup-actually.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-DTCyvo6cC54-every-level-of-a-claude-second-brain-explained.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube--MbKLZGndfY-how-to-build-your-agentic-os-with-claude-code-4-layer-setup.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-rRa9td4oe7k-how-i-use-obsidian-claude-cowork-to-run-my-life.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-obsidian-vault-de-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-how-to-build-a-pe-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-rZX1OYetbSM-how-to-build-your-own-ai-operating-system-full-stack-explain.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-AkdFKnufNQo-claude-code-runs-my-business-13-workflows.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - AI OS
  - AIOS
  - agentic OS
  - agentic operating system
  - AI operating system
  - me.md
  - vault map
  - skill map
  - ideaverse
  - ACE (Atlas Calendar Efforts)
  - Nick Milo AI OS
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-21
updated: 2026-06-25
---

# AI Operating System

**TL;DR.** An AI Operating System (AIOS) is a structured folder/file system around an AI coding agent that provides persistent context, memory, skills, and connections — enabling compounding, tool-agnostic intelligence. "An agentic OS is just clever context management" [^src1]. The key insight: the model is the engine, but context is the fuel — "context is king, not the AI model. Everyone has access to the same models" [^src6].

## What it is

An AIOS is built from plain text files — identity configs, memory records, skill definitions — inside a project folder that any AI coding agent reads at session start. The files persist across sessions; the agent's state does not.

"Every one of these agentic tools are doing the same thing under the hood: reading text files that define who you are, what you know, what you can do, and what you remember, and what you can reach" [^src5].

Because the OS is just text files, it is **tool-agnostic**: switching from Claude Code to Codex to any new agent takes minutes — "all you have to do is point the tool to the same folder" [^src5][^src7].

## Core architecture

### Three-layer OS kernel (infrastructure view)

IBM's framing: the AIOS sits between AI agents and infrastructure as a coordination kernel [^src2]:

| Layer | Contents |
|---|---|
| AI Agents | Task execution, planning, reasoning |
| **Agent OS Kernel** | Scheduler/Orchestrator · Memory Manager · Tool Manager · Identity Manager · Observability · Guardrails |
| Infrastructure | File systems, databases, networks, APIs |

The kernel provides six services [^src2]:
- **Scheduler / Orchestrator** — coordinates which agent runs when
- **Memory Manager** — manages short-term (context window), long-term (knowledge base / files), and episodic (past sessions) memory
- **Tool Manager** — sandboxes tool calls; controls what agents can touch
- **Identity Manager** — issues short-lived tokens; maintains audit trail
- **Observability** — logs, traces, and metrics for debugging agent behavior
- **Guardrails / Governance** — ensures agents stay on task and in scope

> "Without it, agents are brilliant but unreliable. With it, agents become infrastructure you can actually trust." [^src2]

### Seven-layer practitioner model

From the AI Daily Brief's agent OS training program, focused on knowledge workers [^src5]:

1. **Identity** — who you are, your roles, rules enforced on every interaction
2. **Knowledge** — what you know: domain expertise, business data, reference docs
3. **Memory** — what persists: decisions made, preferences, outcomes across sessions
4. **Tools / MCP** — what the agent can reach: APIs, data sources, services via [[ai-engineering/mcp|MCP]]
5. **Skills / Workflows** — encoded procedures: how you write, analyze, communicate
6. **Cadence / Routines** — when things happen: scheduled tasks, updates, digests
7. **Team / Permissions** — who else can access the OS and at what scope

### Four-C's framework (practitioner implementation)

Used by practitioners building production AIOS on Claude Code [^src6][^src7]:

| C | Meaning | Example |
|---|---|---|
| **Context** | What it knows | Business background, customer data, strategy docs |
| **Connections** | What it can touch | Calendar, Slack, email, databases via MCP |
| **Capabilities** | How you work | Skill files encoding your writing style, processes |
| **Cadence** | When things happen | Scheduled updates, digests, background routines |

### Nine-component breakdown

The most granular practitioner model [^src1]:

1. **Static context** — identity file, brand context; loads at every session start
2. **Memory system** — 6 levels: from CLAUDE.md (session scope) to cross-tool shared memory
3. **Skills** — short, modular (<200 lines each), progressively disclosed on demand
4. **Skill chaining / systems** — skills that invoke other skills; reusable playbooks
5. **Multi-level planning** — from today's task list to long-horizon project arcs
6. **Multi-client architecture** — parent CLAUDE.md + per-client-level overrides
7. **Predictable output folders** — structured outputs that accumulate over time
8. **Remote access** — Telegram bot or VPS connected to the Claude Code environment
9. **Channels** — phone/mobile access to the same running OS

## Why context compounds

"The AI agent you have after 6 months is far more powerful than the one you start with" [^src3] — because every decision, outcome, and procedure can be written to the memory layer and made available to every future session.

Each skill you encode means less re-explaining. Each MCP connection means one less copy-paste. Each routine that runs on schedule means work happens without manual trigger. "Context compounds because the more you and your team use AI and the earlier you start, the more context it builds." [^src3]

## Three-component minimal setup

The simplest mental model for getting started [^src8]:

| Component | Purpose | Example files |
|---|---|---|
| **Context folder** | Who you are and how you work | `CLAUDE.md`, brand docs, customer profiles |
| **Skills** | Encoded capabilities (how to do specific tasks) | `skills/write-linkedin-post.md` |
| **Workspace** | Organized outputs by project | `projects/youtube/`, `clients/acme/` |

"Nothing compounds, nothing grows, and every day it feels like you always have to start from scratch" — without this structure [^src8].

## Obsidian as an agent memory layer

Obsidian's CLI lets agents search notes with semantic awareness — tags, frontmatter, wikilinks — rather than raw grep [^src9]. The result: "the agent can pick notes, not lines" [^src9]. Agents can read, write, and search notes; this turns a personal knowledge base into a structured long-term memory store with the same interface as any other directory.

"One thing I keep noticing with AI tooling is that people reach for bigger models before fixing the surrounding system. If your agent has weak memory, poor retrieval, or no useful grounding, a larger model usually just gives you more expensive confusion." [^src9]

**The symbiosis framing** [^src18]: agents and Obsidian complement each other at their respective weak points — "agents don't remember anything, but Obsidian does; Obsidian has no hands to take action, but Claude/Codex can act on the folder structure." The pair addresses each other's deficiencies exactly.

See [[ai-engineering/agent-memory|Agent Memory]] for the full taxonomy of memory tiers.

## Agentic logging: the time audit

Beyond capture, agents can log activities throughout the day — timestamping what you work on as it happens [^src18]. Using Claude hooks, each agent task automatically appends a log entry. The result is an honest accounting of where time goes, built from activity data rather than self-reported estimates. This is described as "a huge productivity unlock" — you can't improve what you don't measure.

The agentic OS as workspace extends further: enabling Obsidian's built-in (disabled-by-default) web viewer turns it into a full workspace, showing dev server output (localhost:3000) alongside notes and the terminal agent. Sidebar web apps (Slack, Telegram, Spotify) can be pinned like browser tabs — creating a unified work environment within Obsidian [^src18].

**Custom plugin pattern** [^src18]: the Obsidian vault can serve as the backend for a custom Obsidian plugin (a mini dashboard app). Built with Codex, using Obsidian notes + a database as the backend. Config-driven, note-backed views — schedule, calendar, metrics snapshots all stored as notes. Core thesis: "don't just collect notes — build systems. Capture → memory → activity logging → dashboards/optics that actually drive decisions."

## Key gotchas

- **Statelessness is the default.** "If you open a new session in Claude Code, what does it have? It loads in its global rules, CLAUDE.md. Otherwise it would be a complete beginner every time." [^src6] The OS makes each new session intelligent from line one.
- **Context has a cost.** "Think about your tokens like money." [^src6] Load only what the current task needs; skills should be invoked on demand rather than always-on. See [[ai-engineering/context-engineering|Context Engineering]] for the "less is more" discipline.
- **Build iteratively ("layers and not leaps").** [^src4] Start with identity + one skill; add connections, routines, and team access over weeks. An AIOS built in one weekend is a project; one built over months is infrastructure.
- **Tool-agnostic by design.** "Models will be replaced. API endpoints might be deprecated." [^src7] The text-file foundation survives tool churn; migrating to a new agent is pointing it at the same folder.

## Three-step agentic OS build (domain/skill/automation model)

One practitioner framework breaks AIOS construction into domain → task → skill → automation [^src10]:

1. **Domains**: break life/work into domains (research, content, productivity, community, etc.)
2. **Tasks → Skills**: for each domain, enumerate recurring discrete tasks. Each task becomes a skill. The skill ensures the same execution path every time — "you're not guessing every single time and hoping that Claude code does the same thing it did yesterday" [^src10].
3. **Automations**: tasks that happen regularly become either *local automations* (cron jobs on the local machine) or *remote automations* (cloud-hosted routines). Claude Code decides which type is appropriate when given the goal [^src10].

**Observability layer**: a visual dashboard outside the terminal for non-terminal users on the team; skills and automations become clickable buttons [^src10].

**Memory layer**: Obsidian vault as the structured store. Three subfolders per the Karpathy pattern: `raw/` (staging/research), `wiki/` (codified articles from raw), `output/` (deliverables — slide decks, reports) [^src10].

## Four-layer agentic OS (technical model)

A parallel technical breakdown used in toolchain presentations [^src11]:

| Layer | Component | Description |
|---|---|---|
| 1 | **CLAUDE.md** | Persistent memory loaded every session; identity, rules, project context, optional memory section with write access. "Not a prompt. It's a job description your agent never forgets." Keep under 200 lines. |
| 2 | **MCP servers** | Connects Claude to every tool in the stack; 12,000+ servers indexed by Pulse MCP (May 2026), ~97M SDK downloads/month. Anthropic donated the protocol to the Linux Foundation (Dec 2025). |
| 3 | **Hooks** | Shell scripts bound to agent lifecycle events (PreToolUse / PostToolUse / UserPromptSubmit); "like Git hooks, but for your AI agent." Make the OS reactive without polluting the reasoning loop. |
| 4 | **Subagents** | Specialized workers scoped to a domain, reading the foundation and using the tools. |

Build order: CLAUDE.md → GitHub + filesystem MCP (covers 80% of use cases) → one PostToolUse notification hook → first subagent for the most repetitive task. "Everything reads down. Everything acts up." [^src11]

## Second-brain vs. AIOS distinction

Some practitioners distinguish second brain (knowledge layer) from AIOS (execution layer) [^src12]:

- **Second brain** (knowledge): Does the system know what's going on in your business, your clients, your projects? Can you ask it questions? Requires static context + live connections.
- **AIOS** (capabilities + cadence): On top of the knowledge layer, do you have encoded skills? Do those skills run as automations when you're not watching?

The four-C's sequence maps to this: Context (who) → Connections (live data) → Capabilities (skills) → Cadence (automations) [^src12].

**CLAUDE.md as a router, not a monologue.** Rather than prose descriptions, the `CLAUDE.md` acts as a navigation map: `path/to/skills`, `path/to/wiki`, `path/to/hotcache`, `path/to/master_index`. The agent reads the map and drills to the relevant file rather than loading all context upfront [^src12].

**Context compounding check**: pulse-check question — "If you opened your Claude Code right now and asked it something about you and your business, would you get an answer that sounds like a stranger or like a teammate or co-founder?" [^src12]

## The Karpathy LLM-Wiki pattern (layered memory architecture)

A synthesis of the AIOS memory debate [^src13]:

- **CLAUDE.md** = identity (who the agent is per session)
- **Obsidian wiki** = reasoning over a connected knowledge graph (how the agent thinks)
- **Pinecone / vector store** = flat exact recall for large archives (transcripts, emails)
- **NotebookLM** = deep research

Obsidian RAG "breaks in 5 places" at scale: index grows linearly/expensively, no semantic search, summaries drift, fills context window, doesn't scale past small/medium datasets. Fix: layered architecture where each tool handles what it's suited for [^src13].

The compounding mechanic: one new source updates 10–15 linked wiki pages, ironing out contradictions — so every future query reads richer knowledge. Traditional RAG re-fetches chunks and forgets; here the wiki layer accumulates [^src13].

## Anti-pattern: the slot machine

"Most people use Claude Code like a slot machine — random prompts on random tasks and ultimately getting random results" [^src14]. The AIOS is the structural fix: by providing consistent context (CLAUDE.md identity), live data connections, and reusable skills, the same prompt reliably produces the same quality result rather than depending on a lucky draw from the model's distribution.

The corollary from [[ai-engineering/agentic-coding|Agentic Coding]]: Karpathy's shift from 20% to ~0% code-writing was not about prompting better — it was about framing tasks as **macro actions** (high-level outcomes) and providing agents with the right environment (repositories checked out, permissions pre-granted, parallel sessions running). Token throughput becomes the new GPU utilization metric: an idle subscription is evidence the AIOS isn't running enough concurrent work [^src16].

## 4-layer AIOS with Claude Code (nyndra pattern)

A 30-minute setup pattern for a production agentic OS using four layers [^src17]:

| Layer | Component | Role |
|---|---|---|
| 1 | `CLAUDE.md` | Foundation — identity, rules, live context, long-term memory; loaded every session; "what makes Claude know your world" |
| 2 | MCP (12,000+ servers) | External connections — tools, APIs, data sources; MCP donated to Linux Foundation December 2025; 97M SDK downloads/month |
| 3 | Hooks (3 event types) | Automation — `pre-tool-use`, `post-tool-use`, `user-prompt-submit`; intercept and augment any tool call or prompt |
| 4 | Subagents | Delegation — parallel task execution, role-specialized agents, code-review agents |

**MCP milestone** [^src17]: MCP was donated to the Linux Foundation in December 2025, signaling its status as an open standard (similar to the transition of Docker or Kubernetes). The 97M SDK downloads/month figure (as of mid-2026) makes it effectively the default protocol for agentic tool connectivity.

**Hooks as automation layer** [^src17]: hooks transform Claude Code from a "reply to prompts" tool to an OS that acts on events. A hook can inject context before any tool call, validate outputs after a write, or augment user prompts with live context before they reach the model.

**Key framing** [^src17]: "A chatbot is a conversation. An agentic OS is infrastructure." The distinction is persistence, composability, and event-driven execution — the same properties that distinguish an OS from a REPL.

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — the theoretical foundation; an AIOS is applied context engineering
- [[ai-engineering/agent-memory|Agent Memory]] — the memory layer within an OS; typed memory tiers
- [[ai-engineering/agent-skills|Agent Skills]] — the skills layer; SKILL.md patterns, progressive disclosure
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — the identity layer; CLAUDE.md as OS navigation map
- [[ai-engineering/mcp|MCP]] — the connections layer; how the OS reaches external tools
- [[ai-engineering/long-running-agents|Long-Running Agents]] — OS-level cadence and scheduling
- [[ai-engineering/claude-code|Claude Code]] — the primary host for personal AIOS implementations
- [[ai-business/monetizing-code|Monetizing Code]] — business angle: selling AI OS services

---

[^src1]: [Creating Your Own Agentic OS Is Easy — Insanely Powerful](../../raw/youtube/youtube-w0S-khYCaB4-creating-your-own-agentic-os-is-easy-insanely-powerful.md) — Simon Scrapes, YouTube
[^src2]: [Why AI Agents Need an Operating System](../../raw/youtube/youtube-IVGjBxqygmI-why-ai-agents-need-an-operating-system.md) — IBM Technology, YouTube
[^src3]: [5 Skills to Build an AI Operating System Like the #1 (Full GUI)](../../raw/youtube/youtube-zElKhlFkqU4-5-skills-to-build-an-ai-operating-system-like-the-1-full-gui.md) — Ben AI, YouTube
[^src4]: [What Is an AI Operating System? (And Why Every Business Will Need One)](../../raw/youtube/youtube-DXcVT07bQ6g-what-is-an-ai-operating-system-and-why-every-business-will-n.md) — Liam Ottley, YouTube
[^src5]: [How To Build a Personal Agentic Operating System](../../raw/youtube/youtube-ntvkDnk_5jA-how-to-build-a-personal-agentic-operating-system.md) — AI Daily Brief (Nofar Gaspar), YouTube
[^src6]: [I Turned Claude Opus 4.8 Into My Entire AI Operating System](../../raw/youtube/youtube-0WDkwMxj13s-i-turned-claude-opus-4-8-into-my-entire-ai-operating-system.md) — Nate Herk, YouTube
[^src7]: [Build & Sell Claude Code Operating Systems (2+ Hour Course)](../../raw/youtube/youtube-bCljOfCH8Ms-build-sell-claude-code-operating-systems-2-hour-course.md) — Nate Herk, YouTube
[^src8]: [How to Build Your AI Operating System with Claude Code (Full Guide)](../../raw/youtube/youtube-vvDdTPFhCp8-how-to-build-your-ai-operating-system-with-claude-code-full.md) — Riccardo Vandra, YouTube
[^src9]: [I Gave Pi Access to Obsidian And I'm Not Looking Back](../../raw/youtube/youtube-JnQcPzjC6Vo-i-gave-pi-access-to-obsidian-and-i-m-not-looking-back.md) — DevOps Toolbox, YouTube
[^src10]: [Stop Using Claude Code Without an Agentic OS](../../raw/youtube/youtube-Bgxsx8slDEA-stop-using-claude-code-without-an-agentic-os.md) — Chase AI, YouTube
[^src11]: [How to Build Your Agentic OS with Claude Code (4-Layer Setup)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-how-to-build-your-report.md) — nyndra AI, YouTube (notes report)
## Nick Milo's 3-layer AI OS (ideaverse + maps + tool)

Nick Milo (Linking Your Thinking) describes a three-layer AIOS designed to be **tool-agnostic** — portable across Claude, Codex, Gemini, or any future AI [^src13]:

**Layer 1 — Ideaverse** (Obsidian): the user's own thinking. ACE folder structure: Atlas (knowledge/ideas/reference), Calendar (time-anchored notes, journals), Efforts (projects, tasks). Plain Markdown files — readable by any tool, owned by the user.

**Layer 2 — Maps and manuals** (the translation layer): three AI-facing documents that let the agent navigate the vault without scanning all notes:
- **`me.md`**: portable identity file. Tells any AI who the user is, how they think, how to work with them. Lives at the root of the pointed folder. `CLAUDE.md` is a one-liner: "go immediately to me.md." The CLAUDE.md is Claude-specific; me.md is not.
- **Vault map**: answers "how should AI move through your notes?" — a master table of contents + navigation manual. Lets the agent isolate relevant files and skip the rest (critical when vault = 17K+ notes).
- **Skill map**: lists what skills exist, what they do, and when to use them. Skills live in the user's own folder (not inside Claude), so they travel with the user to any AI tool.

**Layer 3 — AI tool** (Claude Cowork): the outermost layer — swappable. Point Cowork at the knowledge folder. At session start, fire a prompt: "Read me.md in Ideaverse. Then review the vault map and skill map for relevant context. Confirm you've read, then await instruction." — use a keyboard shortcut (TextExpander) to inject this without retyping [^src13].

**Why tool-agnostic matters** [^src13]: "If Claude goes away tomorrow, I could instantly swap it out with Codex, with an open-source model, with whatever I need. I have all my files, skills, and AI core documents built to go with me." The AI tool is rented; the files are owned.

**AIOS folder**: a separate `AIOS/` folder within the vault for AI-generated content, isolated from first-person notes. "If I'm generating AI content, I want to always be able to quickly isolate it, clear it out when necessary, and that way always keep my thoughts and ideas very clean." [^src13]

**Sample capabilities** [^src13]: morning daily brief (weather, what happened yesterday, open tasks, book momentum, top 2–3 priorities today — generated by a "daily brief" skill pulling from Gmail, calendar, task manager); open note sections with curly brackets for async notes to the AI.

[^src12]: [I Turned Claude Fable Into The Ultimate Second Brain](../../raw/youtube/youtube-8QQ_INxAhRs-i-turned-claude-fable-into-the-ultimate-second-brain.md) — Nate Herk, YouTube
[^src13]: [How I Use Obsidian + Claude Cowork to Run My Life — Nick Milo](../../raw/youtube/youtube-rRa9td4oe7k-how-i-use-obsidian-claude-cowork-to-run-my-life.md) — Nick Milo (Linking Your Thinking), YouTube
[^src13]: [Claude Code + Karpathy's Obsidian = New Meta](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-claude-code-karpa-report.md) — YouTube (notes report)
[^src14]: [Stop Using Claude Code Without an Agentic OS (notes report)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-stop-using-claude-report.md) — Chase AI, YouTube (processed report)
[^src15]: [I Built Karpathy's LLM Wiki in Obsidian (notes report)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-built-karpathy-report.md) — Cody Bontecou, YouTube (processed report)
[^src16]: [Skill Issue: Andrej Karpathy on Code Agents, Auto-Research, and...](../../raw/youtube/youtube-kwSVtQ7dziU-skill-issue-andrej-karpathy-on-code-agents-autoresearch-and.md) — No Priors podcast, YouTube
[^src17]: [How to Build Your Agentic OS with Claude Code (4-Layer Setup)](../../raw/youtube/youtube--MbKLZGndfY-how-to-build-your-agentic-os-with-claude-code-4-layer-setup.md) — nyndra AI, YouTube
[^src18]: [Obsidian Vault Deep Dive! Custom Plugins + Agentic Loops | My Full System](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-obsidian-vault-de-report.md) — YouTube (notes report); Obsidian+agent symbiosis, agentic logging, custom plugin pattern

## Seven-layer Agent OS (Nufar Gaspar / AI Daily Brief)

A practitioner-built agent OS framing for non-technical knowledge workers, platform-neutral (works with Claude Code, Codex, or any harness) [^src19]:

1. **Identity** — SOUL.md / agents.md / copilot instructions: who you are, communication style, rules enforced every time
2. **Context** — 3–5 single-page dated files (stakeholders, strategy, operating principles): context no model can supply on its own
3. **Skills** — reusable "when X, do Y, output Z" instruction sets — one file per procedure
4. **Memory** — deliberate direction of what the tool remembers across sessions; add specialized memory for decisions and relationships
5. **Connections** — MCPs, CLIs, APIs to reach real systems; start read-only, add write access only after weeks of trust
6. **Verification** — 3–5 quick checks per job; periodic retrospects of the whole OS (agents fail by being "confidently and wrongly right" [^src19])
7. **Automations** — top of the stack; only automate trusted manual workflows, produce drafts not direct outputs, always log

**Compounding payoff** [^src19]: "The first agent is hard — a weekend's work. Every later agent takes an afternoon because it inherits the foundation." The tool-neutral design means the same text-file OS ports to any future harness without migration or rebuild.

**The core thesis** [^src19]: "Every agentic tool is becoming every other agentic tool." As Cursor adds agents and Claude Code adds memory, tool choice matters less than the portable text-file foundation underneath.

## Full-stack AI OS architecture (Dave Ebbelaar)

Technical blueprint for a production AI platform. Three architectural layers sit above the AIOS core building blocks [^src20]:

| Layer | Pattern | Use case |
|---|---|---|
| 1 — Trigger-based | Webhooks + API endpoints + event-driven (FastAPI) | Email arrives → action; form submitted → workflow |
| 2 — Scheduled | Cron jobs (Celery Beat or equivalent) | Every Tuesday 9 am: competitor analysis → report |
| 3 — Agent layer | User-invoked via chat (WhatsApp/Slack/Claude Code) | Dynamic, conversational task execution |

**Infrastructure stack** [^src20]: FastAPI (endpoints), Caddy (HTTPS proxy), Redis (in-memory queue), Celery (task workers), Docker Compose (deployment). Claude Agent SDK spins up Claude Code instances as cloud workers.

**Key design principle** [^src20]: "Layer one and two run around the clock while you're on the beach. Layer three is where you spend the most time automating personal tasks." Layers one and two are more reliable for business-critical processes because they run without human intervention; layer three is conversational and dynamic.

**Security pattern** [^src20]: every webhook requires signature verification before processing; store raw event in DB, then async dispatch to worker — never lose data, never process unverified input.

**The "install not rebuild" principle** [^src20]: an AI OS should work like a traditional OS — install new capability as a new module without rebuilding the whole system. Reverse-engineer open-source AIOS repos to extract ideas; build only what you can maintain.

## Claude Code as full business OS: 13 workflow patterns

Practitioner example of running an entire business through Claude Code [^src21]:

| # | Workflow | Mechanism |
|---|---|---|
| 1 | Lead generation | Apify scrapers → AnymailFinder → spreadsheet |
| 2 | Pre-call research brief | Firecrawl + Apify → one-page brief |
| 3 | Proposals & decks | PDF/PPT skills → branded output |
| 4 | Content ideas | Competitor scraping + upvote/downvote feedback loop |
| 5 | Content atomizer | One idea → 18 posts across platforms |
| 6 | Image/thumbnail gen | OpenAI image API / Nano Banana via Claude Code |
| 7 | AI SEO ranking | Data for SEO MCP → gap analysis → publish |
| 8 | Skills from SOPs | Walk Claude through a process once → reusable skill file |
| 9 | Scheduled automation | Skill + cron = background execution |
| 10 | Research & learning | Firecrawl → synthesized report |
| 11 | CRM management | Meeting transcripts → action items → CRM updates |
| 12 | Knowledge base | Second brain + RAG for client insights |
| 13 | Reporting | Auto-generated reports from live data |

**The "skills as SOPs" model** [^src21]: any process repeated in delivery gets codified into a skill (markdown file). Skills are an open standard — portable across Claude Code, Codex, or any harness. Skills point to a brand folder rather than embedding static text, so changes propagate automatically.

[^src19]: [How To Build a Personal Agentic Operating System](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-how-to-build-a-pe-report.md) — Nufar Gaspar / AI Daily Brief, processed notes report; primary source for 7-layer model (Identity→Context→Skills→Memory→Connections→Verification→Automations)
[^src20]: [How to Build Your Own AI Operating System (Full Stack Explained)](../../raw/youtube/youtube-rZX1OYetbSM-how-to-build-your-own-ai-operating-system-full-stack-explain.md) — Dave Ebbelaar, YouTube; primary source for 3-layer technical architecture + FastAPI/Redis/Celery stack
[^src21]: [Claude Code RUNS My Business (13 WORKFLOWS)](../../raw/youtube/youtube-AkdFKnufNQo-claude-code-runs-my-business-13-workflows.md) — Brad / AI & Automation, YouTube; primary source for 13-workflow business OS pattern
