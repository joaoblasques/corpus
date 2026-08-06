---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-study-notes-ai-tools-claude-code-and-gemini-cli-in-the-terminal-networkc.md
    channel: notes
    ingested_at: 2026-07-05
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-05
updated: 2026-08-06
provisional: false
url: 
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
---

# AI Tools - Claude Code and Gemini CLI in the Terminal (NetworkChuck)

> Source: NetworkChuck study notes via Obsidian vault. [`raw/notes/notes-03-resources-study-notes-ai-tools-claude-code-and-gemini-cli-in-the-terminal-networkc.md`]

## TL;DR

Terminal-based AI tools (Gemini CLI, Claude Code) outperform browser-based AI because they maintain persistent session context and have direct file-system access — eliminating the copy-paste overhead of browser chat workflows.

## The Browser-Based AI Problem

Browser AI creates "scattered context across 20 chats, context loss, copy-pasting notes, switching between Claude/Gemini/GPT to cross-check."[^1] Each new chat starts cold; users must manually re-supply project context.

## Terminal AI Advantages

Per the source, terminal AI agents provide:[^1]

- **Persistent context** within a session
- **File-system access** — read, write, and run commands
- **Project-directory awareness** — the AI sees actual code without copy-pasting
- **End-to-end task chaining** — no context switching between tools

## Gemini CLI

- Available on a free tier using a standard Google account[^1]
- Install via `npm install -g @google/gemini-cli` or `brew install gemini-cli`[^1]
- Authenticates via Google OAuth (browser popup); performs Google searches within the conversation[^1]

## Claude Code

The source characterizes Claude Code as "overpowered" and NetworkChuck's preferred tool.[^1] Key properties noted:

- Requires a Claude subscription (uses API credits)[^1]
- Has shell and file-system access; can execute commands[^1]
- Shares the project-context model with Gemini CLI but described as more capable[^1]

## Key Mechanism: Project-Directory Context Window

Launching either tool inside a project directory gives the agent access to all files in that tree — no manual code pasting required.[^1]

## Windows: WSL Recommendation

The source recommends WSL (Windows Subsystem for Linux) for Windows users, noting that "AI coding agents are built for bash/Linux environments — much better than PowerShell."[^1]

---

[^1]: NetworkChuck study notes — `raw/notes/notes-03-resources-study-notes-ai-tools-claude-code-and-gemini-cli-in-the-terminal-networkc.md`
