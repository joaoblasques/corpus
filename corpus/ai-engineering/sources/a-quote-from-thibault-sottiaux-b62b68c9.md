---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/web/web-a-quote-from-thibault-sottiaux-b62b68c9.md
    channel: web
    ingested_at: 2026-07-21
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-21
updated: 2026-07-21
provisional: false
url: https://simonwillison.net/2026/Jul/16/bad-codex-bug/#atom-everything
origin: obsidian-list
---

# A quote from Thibault Sottiaux

> **Quick intake** (obsidian-list). [open source](https://simonwillison.net/2026/Jul/16/bad-codex-bug/#atom-everything)

- GPT-5.6 unexpectedly deletes files under a specific combination of conditions.
- The conditions are: full access mode enabled and Codex run **without** sandboxing protections (including without auto review), the model attempting to override the `$HOME` env var to define a temp directory, and then "an honest mistake" deleting `$HOME` instead.
- A recent Codex bug identified and described by Thibault Sottiaux, via Simon Willison, 16 Jul 2026.

This is a documented case of harm from ordinary model error rather than an adversary — see [Agent Execution Isolation](/ai-engineering/agent-execution-isolation.md), which cites this incident as evidence that sandboxing defends against mistakes, not only [prompt injection](/ai-engineering/agent-security.md).

**Key topics**
- GPT-5.6
- Codex bug
- file deletions
- sandboxing protections
- $HOME env var
- Thibault Sottiaux
