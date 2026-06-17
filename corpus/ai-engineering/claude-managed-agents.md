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
[^src3]: [Building agents that reach production systems with MCP](../../raw/notes/notes-clippings-building-agents-that-reach-production-systems-with-mcp.md) — Anthropic engineering
