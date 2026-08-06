---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-study-notes-ai-tools-gemini-cli-web-ui-for-browser-access.md
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

# AI Tools - Gemini CLI Web UI for Browser Access

**TL;DR**: A fork of the Claude Code Web UI that replaces Claude Code with Gemini CLI as the backend, providing browser-based access to Gemini CLI — including on mobile — without requiring terminal comfort.[^1]

## What It Is

Gemini CLI Web UI is a fork of the Claude Code Web UI with Gemini CLI as the backend.[^1] Its key value proposition: "Gemini CLI is completely free with Gemini 2.5 Pro — this UI makes it accessible without staying in the terminal."[^1]

## Features

- **Project management**: add project directories, manage sessions per project[^1]
- **Model selection**: choose from available Gemini models via settings[^1]
- **YOLO mode**: enable all tools without per-action confirmation[^1]
- **Notification sound**: plays on task completion, useful for long runs[^1]
- **Selective tool permissions**: allow or disallow specific tools[^1]
- **File attachment**: add specific files or images to prompts[^1]
- **Source control view**: view diffs and commit messages[^1]
- **Image upload**: supports multimodal prompts[^1]
- **Responsive**: works on mobile[^1]

## Setup

```bash
git clone <gemini-cli-webui-repo>
cd gemini-cli-webui
npm install
cp .env.example .env
npm start  # runs on port 4090
```

Login credentials are created on first run. Wraps an existing Gemini CLI setup (free tier or API key).[^1]

## Use Cases

- Alternative to Codex/Jules for background async task execution[^1]
- Host on a server, start tasks, then check progress later from a phone[^1]
- Access Gemini CLI without terminal comfort[^1]

## Comparison to Claude Code Web UI

Analogous to how Claudia provides a UI for Claude Code, this project bridges Gemini CLI's terminal-only default interface with browser access.[^1] Gemini CLI itself is fully free with generous limits.[^1]

[^1]: `raw/notes/notes-03-resources-study-notes-ai-tools-gemini-cli-web-ui-for-browser-access.md`
