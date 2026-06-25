---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-z7xyZQVK4Dg-build-anything-with-tmux-here-s-how.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - terminal multiplexer
  - tmux sessions
  - tmux panes
  - tmux windows
  - persistent terminal
tags:
  - corpus/mlops
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# tmux

**TL;DR** — tmux is a terminal multiplexer: it runs and manages multiple terminal sessions from one window, keeps those sessions **alive after you disconnect**, and lets you reattach from any device. For agentic engineering in 2026 it is the critical persistence layer — the only way to run long-lived AI agents (Codex, Claude Code) for hours or days without keeping a laptop open or on a specific network [^src1][^src2].

> "Tmux is the one tool that every single agentic engineer needs." [^src1]

## Three-level hierarchy

| Level | Analogy | Purpose |
|---|---|---|
| **Session** | whole workspace | top-level container; survives disconnects |
| **Window** | browser tab | a full-screen terminal within a session |
| **Pane** | split screen | subdivisions of a window |

tmux can **persist, spawn, read, and write** terminal sessions programmatically, meaning one agent can observe another agent's pane — the feature that makes multi-agent coordination possible [^src1].

## Core commands

```bash
# Create / attach
tmux new -s <name>       # new named session
tmux attach -t <name>    # reattach to named session
tmux ls                  # list active sessions
tmux kill-server         # kill all sessions

# Inside tmux (prefix = Ctrl-b)
Ctrl-b d                 # detach (session stays alive)
Ctrl-b %                 # split pane horizontally
Ctrl-b "                 # split pane vertically
Ctrl-b <arrow>           # move between panes

# Enable mouse (non-negotiable for usability)
echo "set -g mouse on" >> ~/.tmux.conf
```

Mouse support is described as "non-negotiable" — without it, pane navigation requires memorizing every keyboard shortcut [^src1].

## Install

```bash
# macOS
brew install tmux

# Ubuntu/Debian (on a VPS)
apt update && apt install tmux -y
```

## The VPS pattern

The highest-value tmux workflow is **tmux on a VPS, not locally** [^src1][^src2]:

1. Provision a cheap always-on VPS (e.g. Hostinger KVM2 — recommended in both sources as affordable and sufficient for multiple agents).
2. SSH in: `ssh root@<ip>`.
3. Create a named tmux session: `tmux new -s agents`.
4. Launch agents (Codex CLI, Claude Code) in panes.
5. Detach (`Ctrl-b d`) — agents keep running.
6. Close SSH, laptop lid, whatever. Agents continue.
7. Reconnect from laptop or phone via SSH and `tmux attach -t agents`.

Advantages over local execution [^src2]:
- VPS "doesn't go to sleep" — 24/7, hardwired connection, data-center speeds.
- Disconnected SSH = lost task locally; on VPS + tmux = task keeps running.
- Phone control via Termius (mobile SSH client) → trigger and monitor from anywhere.
- Scheduling via cron + `codex exec` — VPS as an unattended automation box.

> "A virtual private server doesn't go to sleep. It's available 24/7 in a secure environment with a hardwired connection." [^src2]

## Multi-agent use pattern

Agents run in parallel panes within one session [^src1]:

```bash
# Session: agents
# Window 1
# ┌────────────────┬────────────────┐
# │  Codex (feat A)│  Claude (feat B)│
# │  --yolo        │  --dangerously- │
# │                │  skip-perms     │
# ├────────────────┴────────────────┤
# │  Monitor / ls / git status      │
# └────────────────────────────────┘
```

Slash goal feature (Codex/Hermes): fire a long-running goal, detach, come back hours later to results [^src1][^src2].

## Cron scheduling on a VPS

Codex has no built-in scheduler; cron fills that gap [^src2]:

```bash
# Codex writes this cron entry for you if asked:
# crontab entry → runs daily at 09:00
0 9 * * * codex exec "review all PRs in <repo> and commit a status markdown"
```

`codex exec` is the non-interactive headless invocation — the primitive for scripting and scheduling [^src2].

## Device-code auth on headless VPS

Avoid embedding expensive API keys on a VPS. Both Codex CLI and Claude Code support **device-code auth** against an existing subscription [^src2]:

```bash
codex  # → "Sign in with device code" → paste code in browser → done
claude # → "Subscription" → paste code → done
```

## Gotchas

- Copy in tmux: hold `Option` (macOS) while selecting to bypass tmux's own selection and reach the system clipboard [^src2].
- Multiple simultaneous attachments to the same session are possible (e.g. laptop + phone) — both see and can type into the same terminal [^src2].
- `tmux kill-server` stops *all* sessions — use `exit` inside a pane to close only that pane.

## See also

- [[mlops/terminal-and-shell|Terminal & Shell]] — Alacritty/zsh/Powerlevel10k, the desktop-side complement
- [[mlops/cli-tools|CLI Tools]] — fzf, zoxide, and other productivity tools in the same layer
- [[mlops/vps-for-agents|VPS for Agents]] — full VPS provisioning + agent workflow context
- [[mlops/README|MLOps hub]]

---

[^src1]: [Build Anything with Tmux, Here's How (David Ondrej)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md) — [00:06](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=00:06) what tmux is; [03:27](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=03:27) sessions/windows/panes; [03:46](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=03:46) multi-agent substrate; [11:03](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=11:03) multi-agent demo
[^src2]: [I Gave Codex a 24/7 Server — Now It Codes While I Sleep (Tim Ruscica / Tech With Tim)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md) — [02:42](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=02:42) VPS rationale; [13:32](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=13:32) tmux install + session persistence; [16:05](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=16:05) phone control; [20:34](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=20:34) cron automation
