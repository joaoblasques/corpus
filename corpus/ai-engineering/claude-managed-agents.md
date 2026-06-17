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
aliases:
  - Claude Managed Agents
  - Managed Agents
  - CMA
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-17
updated: 2026-06-17
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

- **Notion** — delegates tasks (code, presentations, spreadsheets) directly inside Notion Custom Agents; dozens of tasks run in parallel while teams collaborate on output.
- **Rakuten** — shipped specialist agents (product, sales, marketing, finance) in Slack/Teams within one week per agent; long-running agents learn from every session via memory and cut first-pass errors by 97% [^src2].
- **Asana** — built AI Teammates that work alongside humans inside Asana projects, shipping advanced features "dramatically faster."
- **Sentry** — paired Seer's root-cause analysis with a Claude-powered agent writing the patch and opening the PR; shipped in weeks instead of months.
- **Netflix** — agents carry context across sessions, including insights that took multiple turns to uncover and corrections from a human mid-conversation [^src2].
- **Wisedocs** — document-verification pipeline uses cross-session memory to spot recurring document issues; verification speed up 30% [^src2].

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

Wisedocs (document verification) used outcomes to grade reviews against internal guidelines; reviews now run 50% faster while staying aligned with team standards [^src4].

### Multiagent orchestration

A lead agent breaks the job into pieces and delegates each one to a specialist with its own model, prompt, and tools. Specialists work in parallel on a shared filesystem and contribute to the lead agent's overall context [^src4]. The lead agent can check back in mid-workflow because events are persistent. Full step-by-step tracing is visible in the Claude Console.

Netflix's platform team used this pattern: an analysis agent processes logs from hundreds of builds across different sources in parallel and surfaces only patterns worth acting on [^src4]. Spiral (writing agent) uses a Haiku lead agent to field requests and delegate drafting to parallel Opus subagents; outcomes enforce editorial quality before drafts are returned [^src4].

## Claude Platform on AWS

As of mid-2026, Claude Managed Agents (and the full Claude Platform) is available on AWS with AWS IAM authentication, CloudTrail audit logging, and billing through a single AWS invoice. New features ship same-day as the native Claude API [^src5]. This is distinct from Claude on Amazon Bedrock: the Platform on AWS is operated by Anthropic (data processed outside the AWS boundary); Bedrock keeps AWS as the data processor within the AWS boundary [^src5].

## Pricing

Standard Claude Platform token rates + **$0.08 per session-hour** of active runtime [^src1].

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
