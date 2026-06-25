---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/github-addyosmani-gemini-cli-tips.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Gemini CLI
  - gemini-cli
  - Google Gemini CLI
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Gemini CLI

**TL;DR.** Gemini CLI is Google's open-source agentic coding CLI — the Gemini counterpart to Claude Code. It uses `GEMINI.md` as its persistent context file (analogous to `CLAUDE.md`), supports custom slash commands, MCP server extension, memory recall, checkpointing/restore, and a headless/scripting mode. The Addy Osmani tip collection (2,382★) documents ~30 power-user patterns [^src1].

## Core concepts

### GEMINI.md (persistent context)

`GEMINI.md` is the Gemini CLI equivalent of `CLAUDE.md` — a markdown file in the project root that is auto-loaded at session start, providing persistent project context [^src1]. Key differences from `CLAUDE.md`:
- Supports `@file` and `@folder` references to pull in additional context files on demand
- Can include `## Tools` and `## Constraints` sections that Gemini interprets as capability/permission declarations
- Is checked into the repo and shared with the team

### Custom slash commands

Gemini CLI supports project-level and user-level custom slash commands stored in `.gemini/commands/` (project) or `~/.gemini/commands/` (user) [^src1]. The format is a markdown file with a frontmatter block declaring the command name, description, and optional tool permissions.

Custom commands are the Gemini CLI equivalent of Claude Code skills — load on demand, describe the workflow, and invoke with a slash prefix. See [[ai-engineering/agent-skills|Agent Skills]] for the cross-tool concept.

### MCP extension

Gemini CLI supports MCP servers in `~/.gemini/mcp.json` (user-level) or `.gemini/mcp.json` (project-level) [^src1]. Standard MCP configuration format:
```json
{
  "mcpServers": {
    "myserver": {
      "command": "npx",
      "args": ["my-mcp-server"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

Tool approval: Gemini CLI prompts for tool approval on first use in a session; auto-approve is configurable per server.

## Key tips (30 documented by Addy Osmani)

### Context and memory
- **Memory recall**: Gemini CLI maintains a per-project memory store; use `/memory add "fact"` to explicitly store facts and `/memory` to view the current store [^src1]
- **Context files**: `@include path/to/file.md` in a prompt or in `GEMINI.md` pulls file content into context — the GEMINI.md version is always-on, the prompt version is on-demand
- **`/compress`**: compresses conversation history when context fills, similar to Claude Code's `/compact` [^src1]

### Checkpointing
- **`/checkpoint`**: saves the current session state (conversation + file state) to a named checkpoint [^src1]
- **`/restore <name>`**: restores a checkpoint — enables rollback to any prior state without `git reset`
- Checkpoints are stored in `.gemini/checkpoints/`; each is a JSON snapshot of the session

### Headless mode and scripting
- **`gemini -p "task"`**: non-interactive mode for one-shot tasks, scripted pipelines, and CI integration [^src1]
- **`--output json`**: returns structured JSON responses for programmatic consumption
- **`--no-confirm`**: runs without approval prompts (equivalent to Claude Code's `--dangerously-skip-permissions`)
- Environment variable `GEMINI_NONINTERACTIVE=true` disables all interactive prompts

### VS Code integration
- Gemini CLI is available as a VS Code extension (Gemini Code Assist); same `GEMINI.md` and command system applies within the IDE [^src1]
- The extension uses the same MCP configuration as the CLI — no separate config needed

### Telemetry and privacy
- Telemetry is enabled by default; `telemetryEnabled: false` in `~/.gemini/config.json` disables it [^src1]
- Models used: Gemini 2.5 Pro (default); configurable to Gemini 2.5 Flash (faster, cheaper) via `--model gemini-2.5-flash`
- Free tier: 60 requests/minute via the Gemini API free tier; Pro tier: higher limits

### GitHub Action
- Gemini CLI ships an official GitHub Action (`google-gemini/gemini-cli-action`) for CI integration [^src1]
- Trigger patterns: PR creation, push to branch, comment trigger (`/gemini review`)
- Outputs: PR comments, file changes committed directly, or structured JSON for downstream steps

## Comparison with Claude Code

| Dimension | Gemini CLI | Claude Code |
|---|---|---|
| **Context file** | `GEMINI.md` | `CLAUDE.md` |
| **Slash commands** | `.gemini/commands/` | `.claude/skills/` |
| **Checkpointing** | Built-in (`/checkpoint`) | `/rewind` (session-level) |
| **Memory** | `/memory` command | Auto-memory + `MEMORY.md` |
| **Headless mode** | `gemini -p` | `claude -p` |
| **MCP** | `.gemini/mcp.json` | `claude mcp add` / `.mcp.json` |
| **Model** | Gemini 2.5 Pro/Flash | Claude Sonnet/Opus/Fable |
| **Open source** | Yes | No |
| **Free tier** | Yes (API free tier) | No (subscription) |

The conceptual parallels are close enough that practitioners use both tools: Gemini CLI for tasks using Google Workspace connectors (Google Docs, Sheets, Drive) and Claude Code for everything else [^src1].

## See also

- [[ai-engineering/claude-code|Claude Code]] — primary comparison; parallel architecture
- [[ai-engineering/agent-skills|Agent Skills]] — slash commands in Gemini CLI are the same concept as skills
- [[ai-engineering/mcp|MCP]] — MCP server support is shared infrastructure across all major coding CLIs
- [[ai-engineering/pi-agent|Pi Agent]] — another open-source coding agent alternative
- [[ai-engineering/agentic-coding|Agentic Coding]] — landscape comparison of coding agents
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [addyosmani/gemini-cli-tips — ~30 power-user tips for Gemini CLI](../../raw/_inbox/github-addyosmani-gemini-cli-tips.md) — Addy Osmani, GitHub ★2,382
