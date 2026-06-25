---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-98CM_Yq867c-my-new-terminal-daily-driver-supacode-for-macos.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Supacode
  - supacode
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Supacode

**TL;DR**: A macOS agent harness and session manager built on LibGhosty that provides a sidebar-based project directory manager, Git and CI awareness, and deep integration with Claude Code and Pi — designed for developers running parallel agentic coding sessions [^src1].

## What it is

Supacode is a macOS terminal multiplexer / session manager positioned as the harness layer on top of coding agents like Claude Code and Pi. It is **not** an agent itself — it is the environment that organizes, monitors, and controls agent sessions [^src1].

**Foundation**: LibGhosty (the library underlying Ghostty terminal) [^src1].

## Core features

**Sidebar with project directory management** [^src1]: each project directory gets a persistent entry in the sidebar. Sessions are linked to directories, not random terminals. Navigate between projects by clicking rather than `cd`-ing through a terminal.

**Git and PR awareness** [^src1]:
- Current branch visible in the session header
- PR status shown (open, review requested, approved, merged)
- CI check status shown (passing, failing, running)
- The notch displays live PR/CI status — replaces checking the GitHub tab

**Hooks into Claude Code and Pi** [^src1]: Supacode reads and extends `settings.json` and hooks into the agent lifecycle. Per-project script configs allow different startup behaviors per repo (e.g., auto-run `/init` in a legacy codebase, skip in a greenfield project).

**Supacode CLI** [^src1]: an agent-callable CLI that lets Claude Code or Pi manage the Supacode session from inside the agent loop. Enables agents to: create new tabs, switch projects, check PR status, trigger repo-level scripts.

**OAuth to GitHub** [^src1]: connects to GitHub for PR and CI visibility; sessions inherit the GitHub identity without re-auth.

## Why it matters

The core value proposition: running multiple coding agents in parallel (à la Karpathy's multi-monitor Codex setup in [[ai-engineering/agentic-coding|Agentic Coding]]) becomes manageable when the harness layer organizes them rather than relying on raw terminal windows. Each agent in its own Supacode session has its own context about the project's branch, PR, and CI state [^src1].

The Supacode CLI inversion — agent calls CLI to manage its own environment — is a new pattern: the agent becomes a first-class actor in session management, not just a passive occupant of a terminal [^src1].

## Alternatives mentioned

- **Cmux** — tmux-based session manager; simpler, no Git/CI integration
- **Ghostty** — the terminal LibGhosty is extracted from; Supacode is a Ghostty wrapper/extension

## Relationship to other pages

- [[ai-engineering/agent-harness|Agent Harness]] — Supacode is a specialized harness for the macOS developer environment
- [[ai-engineering/claude-code|Claude Code]] — primary agent that Supacode integrates with
- [[ai-engineering/agentic-coding|Agentic Coding]] — the parallel agent paradigm Supacode enables operationally

---

[^src1]: [Supacode — LibGhosty-based agent session manager](../../raw/youtube/youtube-98CM_Yq867c-my-new-terminal-daily-driver-supacode-for-macos.md) — YouTube
