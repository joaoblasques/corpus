---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-clippings-claude-managed-agents-get-to-production-10x-faster.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-built-in-memory-for-claude-managed-agents.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-new-in-claude-managed-agents-self-hosted-sandboxes-and-mcp-t.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-new-in-claude-managed-agents-dreaming-outcomes-and-multiagen.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-introducing-the-claude-platform-on-aws.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-scaling-managed-agents-decoupling-the-brain-from-the-hands.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-asana-claude-managed-agents-case-study-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-claude-managed-agents-overview.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-claude-managed-agents-get-to-production-10x-faster-claude.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-using-agent-memory.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/_inbox/web-notion-q-a-claude-managed-agents-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-rakuten-claude-managed-agents-case-study-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-sentry-claude-managed-agents-case-study-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-vibecode-claude-platform-api-case-study-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-claude-legal-solutions-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-claude-managed-agents-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-dreams.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-run-claude-managed-agents-on-daytona.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-claude-code-s-new-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/web/web-multiagent-sessions.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-ehg4fhydTgs-how-to-build-24-7-claude-agents-easy.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/web/web-self-hosted-sandboxes.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-build-a-claude-managed-agent-with-vercel-sandbox-vercel-know.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-set-up-claude-managed-agents-cloudflare-sandbox-sdk-docs.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-github-modal-labs-claude-managed-agents-modal-sandbox-claude.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - Claude Managed Agents
  - Managed Agents
  - CMA
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-17
updated: 2026-06-25
---

# Claude Managed Agents

**TL;DR.** Claude Managed Agents is a suite of composable, cloud-hosted APIs from Anthropic for building and deploying production agents without building infrastructure. It provides sandboxed execution, long-running sessions, multi-agent coordination, scoped permissions, and built-in memory — all backed by a purpose-built orchestration harness. Available in public beta on the Claude Platform; priced at standard token rates plus $0.08 per session-hour of active runtime [^src1].

## The problem it solves

Building a production agent requires: sandboxed code execution, checkpointing, credential management, scoped permissions, and end-to-end tracing — "months of infrastructure work before you ship anything users see" [^src1]. Managed Agents handles the complexity: you define tasks, tools, and guardrails; the platform runs the harness, manages context, and recovers from errors [^src1].

Internal testing on structured file generation showed Managed Agents improved task-success rates by up to 10 points over a standard prompting loop, with the largest gains on the hardest problems [^src1].

## Core capabilities

| Capability | Description |
|---|---|
| **Production-grade agents** | Secure sandboxing, authentication, and tool execution handled by the platform |
| **Long-running sessions** | Operate autonomously for hours; progress persists through disconnections |
| **Multi-agent coordination** | Agents can spin up and direct other agents (research preview) |
| **Trusted governance** | Scoped permissions, identity management, execution tracing |
| **Built-in memory** | Filesystem-based cross-session memory (see below) |

## Built-in memory

Memory on Managed Agents mounts directly onto a filesystem so Claude uses the same bash and code-execution capabilities that make it effective at agentic tasks [^src2]. This architecture is deliberate: "our latest models save more comprehensive, well-organized memories and are more discerning about what to remember for a given task" [^src2].

**Key memory features** [^src2]:
- **Portable stores** — memories are files; developers can export them and manage them via API
- **Scoped sharing** — stores can be shared across multiple agents with different access scopes (e.g., org-wide read-only, per-user read-write)
- **Concurrent access** — multiple agents can work against the same store without overwriting each other
- **Full audit log** — every write is tracked (which agent, which session); rollback to earlier version or redact content from history
- **Session events** — memory updates surface in the Claude Console as session events, so developers can trace what an agent learned and where it came from

### Portable memory for OAuth credentials

**Vaults** in Managed Agents let developers register a user's OAuth tokens once, then reference the vault by ID at session creation — the platform injects the right credentials into each MCP connection and refreshes them automatically, with no secret store to build [^src3].

## Production examples

Teams self-reporting 10x faster deployment across diverse use cases [^src1]:

- **Notion** — task board orchestrator: moving a task to "ready to start" in Notion automatically invokes a Claude session. Eric Liu (PM): "12 hours of prototyping work collapse into about 20 minutes." 30-40 tasks run in parallel; Claude picks up context from connected pages, design system, API docs, and PRDs automatically. Skills are auto-maintained from thumbs-up/thumbs-down feedback. "Humans as editors and reviewers, not doers" [^src8].
- **Rakuten** — Yusuke Kaji (GM AI for Business): deploys specialist agents (engineering, product, sales, marketing, finance) within one week each. Slack/Teams/Kanban integration; mobile voice control. 97% drop in first-pass critical errors; cost and latency down 30%+. Key shift from task-based to goal-based delegation: "delegate goals not tasks." Organizational learning: "individual learning becomes organizational learning instantly." Power users called "Galileo" manage teams of agents; Shoko Sakamoto's FinOps pipeline is one example [^src9].
- **Asana** — AI Teammates built with Claude Opus 4.6 + Managed Agents; marketing campaign review cycle dropped from days to 15 minutes; first deployed: Campaign Brief Writer + Launch Planner agents. Governance model: admin-level visibility into agent task history, no training data use, purpose-scoped tool access [^src6].
- **Sentry** — Indragie Karunaratne (Senior Director Engineering AI/ML): 1 engineer shipped the initial integration; weeks instead of months. Data residency via Vertex AI (minimize data outside Google Cloud). Seer performs root-cause analysis → Claude agent writes the fix → PR opened. "Developer's job shifts from writing the fix to reviewing it." Quote: "from Seer's root cause analysis straight to a Claude agent that writes the fix and opens a PR" [^src10].
- **Vibecode** — Riley Brown + Ansh Nanda co-founders: mobile-first (phone), uses Claude Code programmatically as the complete engine for React Native/Expo code generation, backend creation, multi-file orchestration. Grew 3x to $10M ARR since adopting Opus 4.5. Example use cases: marketplace app for land sales in Australia; virtual sensory board for children with autism. Managed Agents described as "10x quicker" [^src11].
- **Netflix** — agents carry context across sessions, including insights that took multiple turns to uncover and corrections from a human mid-conversation [^src2].
- **Wisedocs** — document-verification pipeline uses cross-session memory to spot recurring document issues; verification speed up 30% [^src2].

## Claude for Legal

Claude for Legal is a suite of plugins, connectors, and integrations for legal teams available on Team and Enterprise plans (no training data use) [^src12].

**Practice area plugins**: Commercial Legal, Corporate Legal, Intellectual Property, Litigation, Employment Legal, Privacy Legal, Regulatory Legal, AI Governance Legal, Law Student, Legal Clinic, and more [^src12].

**Connectors** [^src12]:
- Contract lifecycle: Docusign, Ironclad
- Document management: iManage, NetDocuments
- Legal research: Thomson Reuters
- Deal rooms: Box/Intralinks (data room access for due diligence)

**Microsoft integration**: Claude for Word (draft, redline, summarize) and Outlook (draft correspondence, review contracts) [^src12].

**Key use cases** [^src12]:
- Research briefs and due diligence document review (data room)
- SOW drafting and outside counsel billing review
- Compliance gap analysis
- Contract comparison and redline

Custom skills and connectors are extensible for firm-specific workflows [^src12]. A subset of practice-area plugins (Commercial Legal, Corporate Legal, Litigation, Product Legal) are also deployable as Managed Agents via the Claude Platform — see [[ai-engineering/claude-cowork|Claude Cowork]] for the Cowork legal vertical integration.

## Self-hosted sandboxes and MCP tunnels

Two new enterprise-oriented capabilities extend agent execution control [^src3]:

**Self-hosted sandboxes** — the agent loop (orchestration, context management, error recovery) stays on Anthropic's infrastructure while *tool execution* moves to your own configured environment. Benefits [^src3]:
- Sensitive files, packages, and services stay inside your network perimeter.
- Network policies, audit logging, and security tooling already in place apply natively.
- You control compute: resource sizing and runtime image are set on your side.

Supported sandbox providers (as of mid-2026): **Cloudflare** (microVMs + lighter weight isolates, zero-trust secrets injection, customizable egress proxies); **Daytona** (long-running stateful sandboxes, SSH / authenticated preview URL access, pause-and-restore); **Modal** (sub-second startup, scales to hundreds of thousands of concurrent sandboxes, CPU/GPU on demand); **Vercel** (VM security + VPC peering, credential injection at the network boundary — secrets never enter the sandbox) [^src3].

Self-hosted sandboxes: public beta. Run your own infrastructure or a managed provider.

**MCP tunnels** — agents reach MCP servers inside a private network without exposing them to the public internet. A lightweight gateway makes a single outbound connection: no inbound firewall rules, no public endpoints, traffic encrypted end-to-end. Internal databases, private APIs, knowledge bases, and ticketing systems become tools agents can call [^src3]. MCP tunnels: managed from workspace settings in the Claude Console by org admins; research preview (request access).

## Dreaming, outcomes, and multiagent orchestration

Three additional capabilities for self-improving, quality-aware agents [^src4]:

### Dreaming (self-improvement between sessions)

**Dreaming** is a scheduled process that reviews past sessions and memory stores, extracts patterns, and curates memories so agents improve over time [^src4]. Key properties:
- Surfaces patterns a single agent can't see: recurring mistakes, workflows agents converge on, preferences shared across a team.
- Restructures memory to stay high-signal as it grows.
- Control knob: dreaming can update memory automatically, or you can review changes before they land.
- Especially useful for long-running work and multiagent orchestration.

"Memory lets each agent capture what it learns *as it works*. Dreaming refines that memory *between sessions*, pulling shared learnings across agents and keeping it up-to-date." [^src4]

Real-world result: Harvey (legal AI) used dreaming for long-form drafting agents; completion rates went up ~6x in their tests [^src4].

### Outcomes (rubric-driven self-correction)

**Outcomes** let you write a rubric describing what success looks like; a separate grader evaluates the output against your criteria in its own context window, so it isn't influenced by the agent's reasoning [^src4]. When the output falls short, the grader pinpoints what needs to change and the agent takes another pass.

In internal benchmarks, outcomes improved task success by up to 10 points over a standard prompting loop, with the largest gains on the hardest problems; file generation improved +8.4% (docx) and +10.1% (pptx) [^src4]. Works for both objective criteria and subjective quality (brand voice, visual guidelines).

Outcomes is a production instance of [[ai-engineering/generator-evaluator-separation|generator–evaluator separation]] — the grader runs in its own context so it isn't influenced by the agent's reasoning, the same principle behind the 3-agent GAN harness in [[ai-engineering/agent-harness|Agent Harness]].

Wisedocs (document verification) used outcomes to grade reviews against internal guidelines; reviews now run 50% faster while staying aligned with team standards [^src4].

### Multiagent orchestration

A lead agent breaks the job into pieces and delegates each one to a specialist with its own model, prompt, and tools. Specialists work in parallel on a shared filesystem and contribute to the lead agent's overall context [^src4]. The lead agent can check back in mid-workflow because events are persistent. Full step-by-step tracing is visible in the Claude Console.

Netflix's platform team used this pattern: an analysis agent processes logs from hundreds of builds across different sources in parallel and surfaces only patterns worth acting on [^src4]. Spiral (writing agent) uses a Haiku lead agent to field requests and delegate drafting to parallel Opus subagents; outcomes enforce editorial quality before drafts are returned [^src4].

## Claude Platform on AWS

As of mid-2026, Claude Managed Agents (and the full Claude Platform) is available on AWS with AWS IAM authentication, CloudTrail audit logging, and billing through a single AWS invoice. New features ship same-day as the native Claude API [^src5]. This is distinct from Claude on Amazon Bedrock: the Platform on AWS is operated by Anthropic (data processed outside the AWS boundary); Bedrock keeps AWS as the data processor within the AWS boundary [^src5].

## Architecture: Brain, Hands, and Session

Scaling Managed Agents to production requires separating three concerns that the naive single-process model conflates [^src6]:

- **Brain** — the LLM reasoning and decision-making. Stateless; swappable; can be scaled independently.
- **Hands** — the code that executes tool calls (bash, filesystem, APIs). Lives in a container or sandbox; should not hold session state.
- **Session** — the log, memory, and checkpoints. Lives *outside* both brain and hands, persisted in the platform.

The harness leaves the container: `execute(name, input) → string` is the only interface between brain and hands [^src6]. This gives three operational benefits:
1. **Security boundary** — API tokens and credentials never enter the sandbox; the harness injects them from outside.
2. **TTFT improvement** — p50 time-to-first-token dropped ~60%, p95 >90% when session logs are stored externally (the model no longer re-reads the full session on every turn) [^src6].
3. **Pets → cattle** — sessions become disposable and restartable; a crashed agent resumes from the last checkpoint rather than starting over.

**Session control API** for long-running agents [^src6]:
- `wake(sessionId)` — re-attach to a paused session (e.g. after a webhook or async wait).
- `getSession(id)` — retrieve the current state log.
- `emitEvent(type, payload)` — push structured events into the session stream (used for human-in-the-loop gates and audit logging).

This architecture supports a "many brains, many hands" model where thousands of short-lived execution containers share a single long-lived session log, and the brain layer scales independently from tool execution.

## Memory API (using-agent-memory)

The Memory API for Managed Agents exposes filesystem-based memory through standard read/write operations. The full API surface [^src7]:
- **create/read/update/delete** — CRUD on memory entries at `/mnt/memory/`.
- **version** — access previous versions of a memory entry; full history retained.
- **redact** — permanently remove a specific version from history (compliance / PII removal).
- **Up to 2000 memories per store** before requiring garbage collection or tiering.
- **Prompt injection risk on read_write stores** — any content written by an external system can become an injection vector if the agent reads it without sanitization. Prefer `read_only` stores for shared contexts.

## Dreams API (async memory consolidation)

The Dreams API is a **research-preview async job** that reads an existing memory store plus past session transcripts and produces a *new* memory store with duplicates merged, stale entries replaced, and new insights surfaced — without modifying the inputs [^src13].

**API shape** [^src13]:
```python
dream = client.beta.dreams.create(
    inputs=[
        {"type": "memory_store", "memory_store_id": store_id},
        {"type": "sessions", "session_ids": [session_a, session_b]},
    ],
    model="claude-opus-4-8",
    instructions="Focus on coding-style preferences; ignore one-off debugging notes.",
)
```
Status lifecycle: `pending` → `running` → `completed` / `failed` / `canceled`. Sessions-per-dream limit: **100**. Instructions max: **4,096 characters**. Supported models: claude-opus-4-8, claude-opus-4-7, claude-sonnet-4-6. Billed at standard token rates [^src13].

The `instructions` field steers *what* to synthesize (focus areas, content to preserve, output conventions) — high-level guidance only. Targeted line-level edits should be applied to the output store via the Memory Stores API after the dream completes [^src13].

Required beta headers: `managed-agents-2026-04-01` (all Managed Agents requests) + `dreaming-2026-04-21` (Dreams specifically) [^src13].

## Daytona self-hosted sandbox integration

Self-hosted sandbox with Daytona allows running the CMA loop with a Daytona sandbox as the execution environment [^src14]. Architecture:

- **Anthropic** (API + agentic loop) ← orchestrator → **Daytona** (sandbox with filesystem/shell)
- Filesystem and shell tool calls route to Daytona; web tools and MCP servers remain Anthropic server-side [^src14].

**Sandbox lifecycle** [^src14]:
- Idle-stop: sandbox pauses after idle period; filesystem persists through pauses.
- 30-day delete timer after creation; resettable via API.
- `session.metadata` keys for Daytona integration: `daytona.snapshot_name`, `daytona.sandbox_id`.

Orchestrator patterns: long-poll (synchronous wait) or webhook (async callback when session completes) [^src14].

## The CMA mental model ("The Loop")

The core mental model for building with Claude Managed Agents — as introduced in Anthropic's open-source "launch your agent" skill [^src15]:

- **Goal, not a task** — give Claude a *goal*; it often finds a better path than explicit step-by-step instructions.
- **The loop cycle** — Goal → think → pick tools → attempt → grade against success criteria → retry until passing → present output.
- **Three inputs every loop needs** — Context (what you already know), Goal (what you're achieving), Success (what the ideal outcome looks like).
- **No platform fees** — CMA charges API costs only; the agent loop runs on Anthropic's infrastructure at no additional hosting cost.
- **Interview-first building** — the skill interviews you to nail down the success rubric before making any API calls.

Boris Cherny (Claude Code creator): "I don't prompt Claude anymore. My job is to write loops." [^src15]

Real-world cost calibration: a live demo of a daily news digest agent ran 28 minutes, consumed ~27M tokens, and cost ~$12 — and failed its rubric because the managed environment couldn't access Reddit directly. The loop surfaced the fix: switch to web-search-only tools [^src15].

## Claude.ai waitlist status

As of mid-2026, the CMA waitlist page [^src16] lists two limited research-preview features:
- **MCP tunnels** — requires opt-in via the research preview.
- **Dreaming** — async memory consolidation (see Dreams API above); research preview.

## Pricing

Standard Claude Platform token rates + **$0.08 per session-hour** of active runtime [^src1].

## Multiagent sessions (Managed Agents API)

The multiagent API layer for coordinating networks of agents in a session [^src17]:

**Architecture** [^src17]:
- **Coordinator**: one controlling agent that manages the session; max 1 level of depth (coordinators cannot spawn coordinators)
- **Roster**: up to 20 uniquely named agents (pinned to specific model versions) per session; each agent maintains an isolated context window
- **Threads**: communication channels between coordinator and roster agents; max 25 concurrent threads active at once
- **Shared resources**: agents in a session share filesystem access and vault credentials; each gets its own context window

**MCP and credentials scoping** [^src17]:
- MCP servers are scoped per agent (each agent gets its own MCP configuration)
- Vault credentials are scoped per session (all agents in a session share the same OAuth tokens)

**Event stream** (for cross-thread visibility) [^src17]:
- `session.thread_created` — a thread started
- `session.thread_status_changed` — thread state transition (idle/active/completed/failed)
- `agent.thread_message_received` / `agent.thread_message_sent` — for monitoring individual agent I/O

**Cross-thread communication for blocking** [^src17]: when an agent needs human approval or coordinator input, it posts to the primary thread (visible to the user) rather than staying in its own thread. The event `session.thread_status_changed` with `blocking` status signals that a thread is waiting for input.

**Thread persistence** [^src17]: unlike subagents, threads are persistent within a session — the coordinator can return to a thread started 30 minutes earlier to follow up, without re-creating context.

## Cloud Routines — limits and constraints

Platform limits for scheduled Routines (cloud-hosted prompts without a running machine) [^src18]:

| Plan | Runs/day | Infrastructure |
|---|---|---|
| Pro | 5 | Anthropic cloud |
| Max | 15 | Anthropic cloud |
| Team / Enterprise | 25 | Anthropic cloud |

**Resources per run** [^src18]: 4 vCPUs, 16GB RAM, 30GB disk. Repo is cloned fresh; filesystem is destroyed at run completion.

**Statefulness** [^src18]: Routines are stateless between runs (no session memory carries forward). Git commits made during a run persist in the connected repository; everything else is ephemeral. Branches persist; the cloud environment is destroyed.

**Network access** [^src18]:
- **Trusted**: access to a vetted set of Anthropic-approved domains only (safe for most use cases)
- **Full**: unrestricted network access (risk: a compromised or manipulated prompt could exfiltrate data); choose trusted for compliance-sensitive workloads

**What Routines can't do** [^src18]: access browser cookies (stateless), read local files, use OS-specific tools, or run indefinitely (each run has a time limit).

## Self-hosted tool execution (customer infrastructure option)

Managed Agents supports running tool execution on the customer's own infrastructure via the **self-hosted sandboxes** feature [^src19]. In this mode, the model (at Anthropic) decides what tools to call; execution happens in the customer's environment:

- **EnvironmentWorker** — customer-side worker process that polls for tool call requests and executes them locally
- **AgentToolContext** — context object carrying request metadata and session state, passed to each tool execution
- **MCP tunnel alternative** — instead of polling, expose tools as an MCP server and connect via tunnel; same model-side experience, different implementation
- **Security benefit**: private data never leaves the customer trust boundary. This directly addresses the [[ai-engineering/agent-security|lethal trifecta]] risk model (private data + untrusted content + exfiltration) — the exfiltration surface shrinks when execution stays inside the customer perimeter [^src19].

## Vercel Sandbox integration (control + compute plane pattern)

Vercel Sandbox is the execution layer for CMA when tool execution must reach private infrastructure or handle per-customer credentials [^src20].

**Brain/Hands architecture** [^src20]:
- Anthropic hosts the **brain**: Claude, the tool-calling loop, skills, and memory.
- Vercel provides the **hands**: a Next.js control plane (webhook handler) + ephemeral Vercel Sandbox microVMs (tool execution).

**Two-plane pattern** [^src20]:
1. **Control plane** (Vercel Function): receives `session.status_run_started` webhooks from Anthropic; spawns one Vercel Sandbox per session.
2. **Compute plane** (Vercel Sandbox): the spawned VM attaches to the session's event stream, executes tool calls (`run_shell`, `read_file`, etc.), posts results back, and exits when the session ends.

**Credential brokering at the firewall** [^src20]: the environment key never enters the VM. Vercel Sandbox injects credentials on outbound requests scoped to the current session via a network policy: `outbound calls to /v1/sessions/<sessionId>/...` get the `Authorization: Bearer <key>` header injected at the firewall; any other destination gets no auth and is rejected. `console.log(process.env)` inside the sandbox reveals nothing — the key isn't in the process environment.

**Snapshot prebuilding** [^src20]: installing the Anthropic SDK on every sandbox spawn would add latency. The pattern is to build one snapshot with the runner + SDK pre-installed; every subsequent sandbox boots from that snapshot with no install step. Rebuild whenever `sandbox/runner.ts` or the SDK version changes.

**When to use Vercel Sandbox** [^src20]:
- Tools need to reach internal databases, private APIs, or services not publicly accessible.
- SaaS context: per-customer credentials must be injected at the firewall, not passed as env vars (preventing sandbox code from reading them).
- Egress control: a domain allowlist prevents exfiltration of private data processed by the agent.

## Cloudflare Sandbox integration (MicroVM + Dynamic Workers)

Cloudflare provides a self-managed environment for CMA where the agent loop runs on Anthropic while execution infrastructure runs in the customer's Cloudflare account [^src21].

**Two sandbox backends** [^src21]:
- **MicroVM (Containers)**: a full Linux environment with bash and arbitrary processes. Use for complex multi-step tool execution requiring a real OS.
- **Dynamic Workers (isolates)**: cold-start in milliseconds, a fraction of a container session's cost. Use for lightweight, fast tool execution.

**Capabilities exposed** [^src21]:

| Capability | Description |
|---|---|
| Private service connectivity | Connect to internal services over Workers VPC and Mesh without public internet exposure |
| Egress control | Per-session egress policy: inject credentials into outbound requests, restrict to specific domains, write proxy middleware |
| Agent Email | Each session gets its own email address via Cloudflare Email Service |
| Browser Run tools | Headless browsers with session recordings for audit trail |
| Custom tools | Add tools by editing `src/tools/custom-tools.ts` — no additional infrastructure required |
| Dashboard | Built-in UI for managing agents, viewing sessions, logs, and SSH into MicroVM sandboxes |

**Deployment model** [^src21]: open-source template — fork the repo, deploy to Cloudflare, customize. The control plane is a Workers-based webhook handler. When Anthropic sends `session.status_run_started`, the control plane assigns the session a sandbox (MicroVM or isolate per agent configuration), routes outbound traffic through a per-session egress policy, and persists state across session sleeps.

**When to choose Cloudflare** [^src21]: when you need Cloudflare binding access (R2, D1, KV, Vectorize, Queues), per-agent sandbox type selection (isolate vs MicroVM), or the agent must interact with the browser (Browser Run tools). Daytona is better for long-running stateful sandboxes; Vercel is better for TypeScript-native teams needing low-latency egress to AWS workloads.

## Real-world implementation: Amplitude Design Agent

Amplitude built a Design Agent on Claude Managed Agents + Cloudflare in two days [^src22]:

**Architecture** (three parts) [^src22]:
1. Claude Managed Agents — handles reasoning, tool use, and multi-step generation; no custom orchestration, prompt chaining, or retry logic written by the team.
2. Cloudflare Workers — hosts the UI and the thin agent interaction wrapper. Cold starts negligible, instant preview links.
3. R2 — stores generated artifacts (HTML mockups) with stable URLs for sharing.

**Key insight**: brand context + design system tokens baked into the system prompt transformed generic Claude HTML output into on-brand output — "the difference between generic Claude output and Claude-with-context output is drastic" [^src22]. Using the Google Design MD format for structured brand markdown in the system prompt.

**Iteration loop** [^src22]: the agent's system prompt is the primary iteration surface — each behavior change is a prompt edit that takes minutes and immediately affects output quality. Instrumented with Amplitude Analytics from day one. Sessions hit 2,219 artifacts in the first weeks; 2-4× more viewers than makers (healthy sharing signal).

**London keynote additions** [^src23]: two new features announced at Code with Claude London 2026:
- **Self-hosted sandboxes**: execute work on your own server instead of Anthropic-managed infrastructure.
- **MCP tunnels**: access internal MCP servers behind a firewall without public internet exposure. Agents access private data warehouse or feature-flag services via tunnel.anthropic.com URLs.

**Advisor strategy** (announced London 2026): split execution from advising at the API level — a small model executes, a large model (Opus) advises when needed. Updates the `tools` array on the Messages API. Eve Legal reported frontier quality at 5× lower cost [^src23].

## See also

- [[ai-engineering/mcp|MCP]] — agents connect to external systems via MCP; Vaults handle OAuth credentials per session
- [[ai-engineering/agent-memory|Agent Memory]] — filesystem-based memory is the pattern Managed Agents extends to production
- [[ai-engineering/long-running-agents|Long-Running Agents]] — the underlying agent patterns Managed Agents operationalizes at scale
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — multi-agent coordination is available in research preview
- [[ai-engineering/claude-code|Claude Code]] — Managed Agents integrates with Claude Code via the built-in `claude-api` skill
- [[ai-engineering/ai-agent|AI Agent]] — core agent concepts underlying Managed Agents

---

[^src1]: [Claude Managed Agents: get to production 10x faster](../../raw/notes/notes-clippings-claude-managed-agents-get-to-production-10x-faster.md) — Anthropic announcement
[^src2]: [Built-in memory for Claude Managed Agents](../../raw/notes/notes-clippings-built-in-memory-for-claude-managed-agents.md) — Anthropic announcement
[^src3]: [New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels](../../raw/notes/notes-clippings-new-in-claude-managed-agents-self-hosted-sandboxes-and-mcp-t.md) — Anthropic announcement
[^src4]: [New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration](../../raw/notes/notes-clippings-new-in-claude-managed-agents-dreaming-outcomes-and-multiagen.md) — Anthropic announcement
[^src5]: [Introducing the Claude Platform on AWS](../../raw/notes/notes-clippings-introducing-the-claude-platform-on-aws.md) — Anthropic announcement
[^src6]: [Scaling Managed Agents: Decoupling the Brain from the Hands](../../raw/web/web-scaling-managed-agents-decoupling-the-brain-from-the-hands.md) — Anthropic engineering
[^src7]: [Built-in Memory for Claude Managed Agents (Anthropic docs)](../../raw/web/web-using-agent-memory.md) — Anthropic
[^src8]: [Notion Q&A — Claude Managed Agents](../../raw/_inbox/web-notion-q-a-claude-managed-agents-claude-by-anthropic.md) — Eric Liu, Notion PM
[^src9]: [Rakuten — Claude Managed Agents case study](../../raw/_inbox/web-rakuten-claude-managed-agents-case-study-claude-by-anthropic.md) — Yusuke Kaji, Rakuten
[^src10]: [Sentry — Claude Managed Agents case study](../../raw/_inbox/web-sentry-claude-managed-agents-case-study-claude-by-anthropic.md) — Indragie Karunaratne, Sentry
[^src11]: [Vibecode — Claude Platform API case study](../../raw/_inbox/web-vibecode-claude-platform-api-case-study-claude-by-anthropic.md) — Vibecode
[^src12]: [Claude Legal Solutions](../../raw/_inbox/web-claude-legal-solutions-claude-by-anthropic.md) — Anthropic
[^src13]: [Dreams — Claude Managed Agents docs](../../raw/web/web-dreams.md) — Anthropic
[^src14]: [Run Claude Managed Agents on Daytona](../../raw/web/web-run-claude-managed-agents-on-daytona.md) — Anthropic
[^src15]: [Claude Code's NEW Open Source Repo Builds Effective AI Agents in MINUTES!](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-claude-code-s-new-report.md) — YouTube (processed report)
[^src16]: [Claude Managed Agents — Claude by Anthropic (waitlist page)](../../raw/web/web-claude-managed-agents-claude-by-anthropic.md) — Anthropic
[^src17]: [Multiagent sessions — Managed Agents API docs](../../raw/web/web-multiagent-sessions.md) — Anthropic
[^src18]: [24/7 Claude Agents and Routines — Scheduling Deep Dive](../../raw/youtube/youtube-ehg4fhydTgs-how-to-build-24-7-claude-agents-easy.md) — YouTube
[^src19]: [Self-hosted sandboxes for Managed Agents](../../raw/web/web-self-hosted-sandboxes.md) — Anthropic
[^src20]: [Build a Claude Managed Agent with Vercel Sandbox](../../raw/web/web-build-a-claude-managed-agent-with-vercel-sandbox-vercel-know.md) — Vercel Knowledge Base
[^src21]: [Set up Claude Managed Agents · Cloudflare Sandbox SDK docs](../../raw/web/web-set-up-claude-managed-agents-cloudflare-sandbox-sdk-docs.md) — Cloudflare
[^src22]: [How We Built a Design Agent at Amplitude with Claude Managed Agents and Cloudflare](../../raw/web/web-how-we-built-a-design-agent-at-amplitude-with-claude-managed.md) — Will Newton, Amplitude
[^src23]: [Code with Claude London 2026: Opening Keynote](../../raw/youtube/youtube-6amLO7I9xdg-code-with-claude-london-2026-opening-keynote.md) — Anthropic, YouTube
[^src24]: [modal-labs/claude-managed-agents-modal-sandbox — CLI + Slackbot integration examples](../../raw/web/web-github-modal-labs-claude-managed-agents-modal-sandbox-claude.md) — Modal Labs, GitHub
