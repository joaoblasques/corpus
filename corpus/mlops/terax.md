---
type: entity
domain: mlops
status: stub
sources:
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-3L8htHUzAI4-terax-one-developer-built-an-ai-terminal-better-than-warp.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Terax terminal
  - AI-native terminal
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Terax

**TL;DR** — Terax is an open-source, AI-native terminal built by solo developer Krinter using **Tauri 2 + Rust** backend and **React + Xterm.js (WebGPU) + CodeMirror 6** frontend. Key specs: ~**7 MB** app, **<300 ms cold start**, bundles a multi-tab terminal, code editor, file-preview sidebar, and embedded browser. Has a built-in agent (Vercel AI SDK, any model including local) that reads the entire codebase and proposes edits as **reviewable accept/reject diffs** [^src1].

> "It's amazing what can be done nowadays by a single developer using AI and many open source tools — this almost rivals Warp, which was built by a whole company and has VC funding." [^src1]

## Architecture

| Layer | Technology | Role |
|---|---|---|
| App framework | **Tauri 2** (not Electron) | No bundled Chromium → saves ~200 MB; uses OS webview |
| Backend | **Rust** | PTY, filesystem, process management |
| Frontend | **React** | UI rendering only |
| Terminal engine | **Xterm.js + WebGPU** | Same as VS Code terminal |
| Code editor | **CodeMirror 6** | Syntax highlighting for most languages |
| AI agent | **Vercel AI SDK** | Any model — OpenAI, Claude, or local; keys in OS native keyring |

## Features

- File sidebar auto-navigates on `cd` — no `ls` needed
- Multi-tab + pane splits
- Agent reads whole codebase, shows context usage, supports session history
- `plan` mode → `TERAX.md` (analogous to `CLAUDE.md`) — project context file
- `build` mode → accepts/rejects diffs one-by-one
- "Privacy tab" hidden from AI agent
- Built-in browser with common-ports shortcut list (dev server on one tab, code on another)
- Vim mode, custom agent instructions, reusable prompts in settings

## Known limitations (pre-1.0)

- NeoVim crashes inside Terax
- No keyboard navigation for the left sidebar (mouse only)
- No `Cmd+` zoom
- Cross-origin browser pages blocked by `X-Frame-Options` (iframes) [^src1]

## Positioning vs. competitors

| Tool | Focus |
|---|---|
| **Terax** | Agentic *development* environment — agent scoped to code files |
| **Warp** | AI terminal with company/VC backing, 58k+ GitHub stars |
| **CMUX** | Agent controls the *whole terminal* (tabs/panes/sidebar) — for multi-agent workflows |

> "With Terax the agent is only scoped to look at the code and files… if you want agents to open browsers and spin up sub-agents, check out CMUX." [^src1]

## See also

- [[mlops/terminal-and-shell|Terminal & Shell]] — alternative terminals (Alacritty, WezTerm, Ghostty)
- [[mlops/cli-tools|CLI Tools]] — tmux (for multi-agent via terminal multiplexing)
- [[mlops/vps-for-agents|VPS for Agents]] — running agents remotely rather than in a local terminal
- [[mlops/README|MLOps hub]]

---

[^src1]: [Terax: One Developer Built an AI Terminal Better Than Warp (Better Stack channel)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md) — [00:00](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=00:00) overview; [01:09](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=01:09) Tauri vs Electron; [02:47](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=02:47) plan/build modes; [04:58](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=04:58) verdict; [05:18](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=05:18) vs CMUX
