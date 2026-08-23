---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-impressions-from-visiting-openai-anthropic-cursor-cadb0581.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - cloud agents
  - cloud-based agents
  - hosted agents
  - agents in the cloud
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-23
updated: 2026-08-23
---

# Cloud Agents

**TL;DR.** Cloud agents are AI agents that run on cloud infrastructure rather than a local developer machine — removing setup friction, enabling parallel execution, and making long-running autonomous tasks practical. As of mid-2026, all three major AI coding harness companies (Anthropic, OpenAI, Cursor) are betting heavily on this pattern as the next major shift in how AI-assisted work is structured. [^1]

## The problem local agents have

Running agents locally has several practical costs: [^1]
- **Setup friction**: connecting to internal MCP servers, configuring skills, tweaking per-machine settings
- **Tool context-switching**: opening a separate app (even Claude Code) vs. just mentioning the agent in an existing channel
- **Machine dependency**: long-running tasks require keeping the machine open and powered
- **Parallelism limits**: running multiple agents heats up the CPU and slows the whole system

## Why cloud agents are emerging now (mid-2026)

The Pragmatic Engineer's hypothesis, based on lab visits: four factors converged simultaneously [^1]:

1. **Coding models hit "good enough"**: before Opus 4.5 / GPT-5.4, models couldn't reliably code autonomously, making long-running tasks pointless
2. **MCP and skills matured**: context injection patterns are now well understood and widely deployed
3. **1M-token context windows**: sufficient context to run complex long-horizon tasks without hitting limits
4. **Cloud GPU capacity**: providers built enough GPU clusters to support large-scale agent deployment

## What each lab is shipping

**Anthropic — Claude Managed Agents**: A hosted service for long-running agents built over six months. Key properties: no setup, no tool context-switching, runs in cloud indefinitely. Also the infrastructure behind the "Claude Tag" Slack integration (mention Claude in a Slack channel → cloud agent picks up the task). See [Claude Managed Agents](/ai-engineering/claude-managed-agents.md). [^1]

**OpenAI — Codex Cloud Agents**: OpenAI acquired Ona (formerly Gitpod), the leading cloud development environment (CDE) provider, to provide sandboxed persistent environments for Codex agents. Goal: "expand Codex beyond work tied to a single device or active session" for tasks lasting hours to days. Hiring an engineering team specifically for the Cloud Agents platform. [^1]

**Cursor — Cloud Agents**: Released at end of 2025; a major focus area in 2026. Runs agents in isolated VMs with full development environments that can iterate toward merge-ready PRs without intervention. Supports iOS app for managing cloud agents from anywhere. [^1]

**OpenClaw — Crabbox**: A community-built solution by Peter Steinberger for running OpenClaw agents in the cloud, motivated by the same problem (local agents overheating CPU). [^1]

## Engineering challenges specific to cloud agents

- **No feedback channel**: locally-running agents surface warnings and errors to a human; cloud agents have no such real-time loop. Cursor's solution: periodic "confessions" where the agent reports issues to the infra team [^1]
- **Node termination mid-task**: moving agent execution from a failed node to another is a non-trivial distributed systems problem [^1]
- **Long-running session management**: checkpointing, reconnect-to-session, progress visibility across asynchronous gaps [^1]

## Non-developer adoption

Cloud agents lower the bar for non-developer use. At OpenAI, more than 95% of non-engineers use Codex (not ChatGPT) internally as of mid-2026. Cloud delivery — no installation, no configuration — is a key enabler. [^1]

## Engineering work shift

At Anthropic and Cursor, a growing share of engineering effort goes into agent execution environments, context scaffolding, and infrastructure — not model training. The agent environment is becoming the primary leverage point. [^1]

## See also

- [Claude Managed Agents](/ai-engineering/claude-managed-agents.md) — Anthropic's cloud agent platform
- [Long-Running Agents](/ai-engineering/long-running-agents.md) — patterns for agents running over extended time
- [Agent Harness](/ai-engineering/agent-harness.md) — the scaffolding layer that wraps cloud agents
- [MCP](/ai-engineering/mcp.md) — protocol enabling agents to connect to external systems

---

[^1]: [Impressions from Visiting OpenAI, Anthropic & Cursor — The Pragmatic Engineer](../../raw/web/web-impressions-from-visiting-openai-anthropic-cursor-cadb0581.md)
