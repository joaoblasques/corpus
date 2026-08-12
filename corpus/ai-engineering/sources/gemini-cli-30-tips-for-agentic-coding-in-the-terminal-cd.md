---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-gemini-cli-tips-tricks-agentic-coding.md
    channel: notes
    ingested_at: 2026-07-19
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - gemini
  - agentic-coding
  - context-engineering
  - cli
  - cicd
created: 2026-07-19
updated: 2026-08-12
provisional: false
url: https://addyo.substack.com/p/gemini-cli-tips-and-tricks
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
confidence: 0.9
last_confirmed: 2026-08-12
---

# "Gemini CLI: ~30 Tips for Agentic Coding in the Terminal"

**TL;DR:** Gemini CLI is Google's open-source agentic terminal AI assistant built on Gemini 2.5 Pro. It is conversational and agentic — it can run shell commands, edit files, and execute multi-step plans. The free tier via Google Account provides ~60 req/min and 1,000 req/day, making it accessible for local and project use.[^1]

---

## Setup and Authentication

Install via npm: `npm install -g @google/gemini-cli`.[^1]

Two auth modes:[^1]

- **Free tier**: Google Account login — ~60 req/min, 1,000/day; Gemini 2.5 Pro included.
- **API key**: Set `GEMINI_API_KEY` from AI Studio for higher quotas.

---

## Persistent Context: GEMINI.md

The primary mechanism for project-level context is `GEMINI.md`, placed at `.gemini/GEMINI.md`. It is "always loaded" into every session.[^1]

Context is hierarchical: a global `~/.gemini/GEMINI.md` is layered with project-level and subfolder-level files. Commands `/memory show` and `/memory refresh` inspect and reload active context. `/init` generates a starter file.[^1]

This is the Gemini CLI equivalent of the CLAUDE.md pattern used in Claude Code — a file-based persistent context mechanism for [context engineering](/ai-engineering/context-engineering.md).

---

## Custom Slash Commands

Define custom commands as TOML files under `.gemini/commands/`. Example: `test/gen.toml` registers as `/test:gen "requirement"`. Uses `{{args}}` template substitution.[^1]

---

## Interaction Modes

**Safe mode (default):** "All file writes and shell commands prompt for confirmation (Y/n) before executing — no surprise changes."[^1]

**Non-interactive / scripted use:**[^1]

- One-shot: `gemini -p "prompt"`
- Stdin: `echo "prompt" | gemini`

**File referencing with `@`:** Pass file content inline — `gemini -p "Summarize @./report.txt"`.[^1]

**Bang commands (`!`):** Run shell commands from within a Gemini CLI session — `!ls`, `!git status`.[^1]

---

## CI/CD Integration

The non-interactive mode (`gemini -p`) makes Gemini CLI scriptable in pipelines. Combined with file referencing (`@`), it enables automated code review, diff summarization, or test generation steps in CI/CD workflows.[^1]

---

## Relation to Other Agentic CLI Tools

Gemini CLI is a direct alternative to Claude Code and Codex CLI in the terminal-AI-assistant category. Key differentiator: the free tier's access to Gemini 2.5 Pro at no API cost. The GEMINI.md context file mirrors the CLAUDE.md pattern, suggesting convergence on file-based persistent context as the standard for [agentic coding](/ai-engineering/agentic-coding.md) tools.

---

[^1]: raw/notes/notes-03-resources-articles-gemini-cli-tips-tricks-agentic-coding.md — source: https://addyo.substack.com/p/gemini-cli-tips-and-tricks
