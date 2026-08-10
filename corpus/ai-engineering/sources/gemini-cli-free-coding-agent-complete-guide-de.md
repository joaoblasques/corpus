---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-study-notes-gemini-cli-free-coding-agent-complete-guide.md
    channel: notes
    ingested_at: 2026-07-10
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-10
updated: 2026-08-10
provisional: false
url: 
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
---

# Gemini CLI — Free Coding Agent Complete Guide

**TL;DR**: Gemini CLI is a free terminal-based coding agent powered by Gemini 2.5 Pro. It excels at adding features and modifying existing codebases; struggles with greenfield projects. At 1,000 requests/day on the free tier, it delivers substantial API value at zero cost.

---

## Free Tier

The free tier uses Gemini 2.5 Pro (Google's most advanced model at time of writing) with the following limits:[^1]

- **Rate limit**: 60 requests/minute
- **Daily limit**: 1,000 requests/day
- **Context window**: 1 million tokens
- **Cost**: $0 — authenticate with a Google account, no API key needed
- Equivalent to ~$180+ of API value per day at commercial pricing[^1]

---

## Key Features

### Built-in Google Search

The agent can run Google searches directly from the terminal — e.g. querying current weather or version-specific library names. The search tool is called automatically when relevant.[^1]

### MCP Server Support

MCP servers are configured via `.gemini/settings.json`. Press `Ctrl+T` to view all connected servers. Supported integrations include Context7 (live docs), image/video generation, Notion, and Gmail.[^1]

### Gemini.md — Persistent Memory File

Acts as the Gemini equivalent of CLAUDE.md: a project-level rules and context file.[^1] Memory commands:
- `memory show` — display current stored rules
- `memory update` — update stored rules
- The agent learns and stores rules automatically when corrected during a session.[^1]

### Interactive vs. Single-Shot Mode

- `gemini` → interactive chat interface
- `gemini -p "your prompt"` → single-shot request, suitable for scripting[^1]

---

## Real-World Test Results

Three tests were run against actual projects:[^1]

| Task | Result |
|---|---|
| Small bug fix (UI scrolling) | ✅ Pass |
| Medium feature (memory tab with CRUD on existing project) | ✅ Pass |
| New project from scratch | ❌ Fail — UI quality below Lovable-style output |

Key finding from source: "Gemini CLI thrives with context. On existing projects, it's excellent. For brand new projects from scratch, it struggles."[^1]

---

## AI-Driven Task Development Workflow

Workflow described in source for iterative feature development:[^1]

1. Screenshot what you want to build.
2. Paste screenshot + context into Gemini.
3. Ask for a plan first: "Review the plan before implementing."
4. After approval: "Go off and implement."
5. For each correction → update `gemini.md` with the new rule.

---

## Context7 MCP Integration

Asking Gemini to "use Context7" triggers a pull of live library documentation, preventing stale training-data issues for version-sensitive queries.[^1]

---

[^1]: `raw/notes/notes-03-resources-study-notes-gemini-cli-free-coding-agent-complete-guide.md` (notes/obsidian, collected 2026-07-10)
