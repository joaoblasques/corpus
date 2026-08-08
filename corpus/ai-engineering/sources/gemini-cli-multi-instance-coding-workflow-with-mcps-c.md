---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-study-notes-gemini-cli-multi-instance-coding-workflow-with-mcps.md
    channel: notes
    ingested_at: 2026-07-10
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - gemini-cli
  - mcp
  - multi-agent
created: 2026-07-10
updated: 2026-08-08
provisional: false
url: 
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
---

# Gemini CLI — Multi-Instance Coding Workflow with MCPs

**TL;DR:** Run three parallel Gemini CLI instances, each with its own isolated context, to handle independent coding tasks simultaneously. MCP integration uses the same `.gemini/settings.json` format as Claude Desktop. Model throttling under load auto-downgrades Gemini 2.5 Pro to Flash unless explicitly configured otherwise.[^1]

---

## Shell Mode Controls

Gemini CLI exposes a shell-mode escape hatch[^1]:

| Key | Effect |
|-----|--------|
| `!` | Enter shell mode — commands execute directly, bypassing the model |
| `!` again | Return to agent mode |
| `\` + Enter | Insert newline in prompt without submitting |
| `@filename` | Attach a file to the current context |

---

## Multi-Instance Strategy

Open **three separate terminal panes**, each running `gemini`. Each instance handles an independent task with its own context.[^1]

**Why separate contexts matter:**
- Changes in one instance don't pollute another's context window
- Each instance stays focused on its assigned task
- Work can continue in any instance without context bleed from other panes[^1]

**Demo tasks run in parallel (from source):**
1. Fix a validation bug (weights field accepting string instead of list)
2. Write documentation for local UV setup
3. Add a new `random_sample` tool[^1]

---

## Model Throttling Behavior

Gemini 2.5 Pro auto-downgrades to Gemini 2.5 Flash under load:

> "Slow response times detected. Switching to Flash."[^1]

Flash is faster but less capable. To prevent unwanted downgrades, specify preferred models explicitly in `gemini.md`.[^1]

---

## MCP Configuration

Config file location: `.gemini/settings.json` in the project directory.[^1]

```json
{
  "mcpServers": {
    "server-name": { ... }
  }
}
```

The format is compatible with Claude Desktop MCP configs.[^1]

---

## Key Observations

- Gemini may use `literal_eval` for code parsing — reject this in favor of `json.loads`[^1]
- For shell commands, may require explicit guidance toward the correct runner (e.g., `uv run` instead of bare `python`)[^1]
- `always allow` tool calls to let Gemini run autonomously without per-call confirmation[^1]
- Model generates tests alongside new tools automatically[^1]

---

## Free Tier

Google account authentication (no API key required) allows up to **1,000 requests/day** free.[^1]

---

[^1]: `raw/notes/notes-03-resources-study-notes-gemini-cli-multi-instance-coding-workflow-with-mcps.md`
