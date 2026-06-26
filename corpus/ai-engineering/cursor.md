---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Cursor
  - Cursor IDE
  - Cursor agent
  - Composer
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-26
updated: 2026-06-26
---

# Cursor

**TL;DR** — Cursor is an AI code editor (a VS Code fork) whose draw is not the models — it runs the same frontier models as everyone else — but the **coding harness the Cursor team builds around them**. One practitioner's stated reason for choosing it over Claude Code or Codex: "while it's using the same models, it has a coding harness… that I just find works a lot better" [^src1]. It is the recurring counterpoint to [[ai-engineering/claude-code|Claude Code]] in the [[ai-engineering/agentic-coding|agentic coding]] tool landscape, and was cited as a breakout commercial success ($100M in its first year, ~$2B valuation) in [[ai-business/ai-business-models|AI Business Models]].

## Harness, not model

Cursor exposes a per-agent **model selector** with the frontier Claude/GPT models plus its own **Composer** model. Observed settings in a real build [^src1]:
- pick the model (e.g. Opus 4.8; Fable 5 when available)
- **fast mode** toggle, **thinking mode**, and the **1M-context** window
- a reasoning-**effort** dial — "medium… is kind of the sweet spot"; higher (high / extra-high) is slower

Model-by-task practice: a frontier Claude model for building from scratch, switching to "GPT 5.5" for large refactors or repeated mistakes, and a faster model (Composer 2.5) for UI-only changes [^src1]. Running agents in Cursor "is not going to be absolutely free" — it bills usage [^src1].

## Workflow surfaces

- **Views**: a default chat-only "agents" view vs a file-visible view; the practitioner prefers seeing the code being written rather than just chatting [^src1].
- **Rules** — Cursor generates rule files in a `rules/` folder that are always injected into the prompt (e.g. "always commit after any major change"), the Cursor analogue of [[ai-engineering/claude-md-conventions|CLAUDE.md conventions]] [^src1].
- **Agent skills + MCP servers** — install a tool's skills with one terminal command and they appear in Cursor; MCP servers are added to `.cursor/mcp` (GitHub MCP, ImageKit MCP shown), then connected/authenticated via the command palette (`Cmd/Ctrl+Shift+P` → "MCP: Open MCP Settings") [^src1]. Installing a vendor's skills + MCP server means the agent learns the tool without the user pasting docs.
- **Multi-agent / multitask mode** — spins up multiple sub-agents in parallel; useful on a well-structured project but "sometimes it just goes crazy… makes it a little bit unmaintainable" [^src1].
- **Dictation** — Whisper Flow voice-to-text works natively, including file tagging, to speed up long planning prompts [^src1].

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the workflow discipline (research-first, context files, skills+MCP, iterative prompt-and-debug) Cursor is used inside; see the "real AI coding workflow" section
- [[ai-engineering/claude-code|Claude Code]] — the CLI agent Cursor is most often compared against
- [[ai-engineering/mcp|MCP]] — the connector layer Cursor adds via `.cursor/mcp`
- [[ai-engineering/agent-skills|Agent Skills]] — the installable skills Cursor consumes
- [[ai-engineering/vibe-coding|Vibe Coding]] · [[ai-engineering/spec-driven-development|Spec-Driven Development]] — the plan-first posture the workflow depends on
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [My Real AI Coding Workflow (build anything) (Tech With Tim)](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md) — [03:59](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=239) Cursor + model selector setup; [05:45](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=345) why Cursor (harness over model); [10:25](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=625) installing skills + MCP servers; [14:13](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=853) rules
