---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Herder
  - Herder multiplexer
  - Herda Plus
  - herder workspaces
tags:
  - corpus/mlops
  - entity
created: 2026-06-26
updated: 2026-06-26
---

# Herder

**TL;DR** — Herder is a modern terminal multiplexer that takes tmux as its starting point (same prefix model, same splits/tabs) and adds three things tmux lacks out of the box: **project-oriented workspaces**, **built-in agent awareness** (it detects running coding agents and surfaces their state), and a **thin-client remote mode** that streams a server-side session back to your local terminal with local keybindings and clipboard [^src1]. It separates session state from process state, so a layout survives even when the server is stopped — where "if your tmux server dies, everything dies, unless you use a plugin to restore" [^src1]. Reviewed at version 0.7.

## Install and start

```bash
brew install herder      # macOS
curl ... | sh            # macOS / Linux
# PowerShell for Windows; NixOS also supported
herder                   # start / reattach
```

Config is read from a `config.toml` in Herder's config directory; `herder` regenerates default config to edit from [^src1].

## tmux-style core, remappable

Herder uses a **prefix** for keymaps (default `Ctrl-B`, same as tmux) — "as an everyday tmux user, this feels right at home"; everything is remappable in `config.toml`, and `prefix ?` lists all bindings including remaps [^src1].

| Action | Default keymap |
|---|---|
| Detach (keep running) | `prefix Q` |
| New / rename / close tab | `prefix C` / `prefix shift-T` / `prefix X` |
| Move / jump tabs | `prefix N`·`prefix P` / `prefix 1`,`2`,`3` |
| Split vertical / horizontal | `prefix V` / `prefix -` |
| Navigate panes (vim) | `prefix H`/`J`/`K`/`L` (remappable to `Ctrl-H/J/K/L`) |
| Resize / maximize / copy-mode | `prefix R` / `prefix Z` / `prefix [` |
| Settings / reload config | `prefix S` / `prefix shift-R` |

Vim-style keybindings are built into pane navigation, resize, and copy/select mode — "we shouldn't really need a plugin for things like this" [^src1]. Caveat: Herder's binds take precedence, so a `Ctrl-H/J/K/L` remap can collide with vim-tmux-navigator-style setups [^src1].

**Mouse support is on out of the box** (tmux requires enabling it in config and is "pretty basic" even then): click to switch tabs, right-click a pane to split/zoom/swap, and drag-to-resize [^src1].

## Workspaces (not sessions) as the organizing unit

Instead of tmux's flat sessions, Herder's primary container is a **workspace**: "a container for your tabs and panes, but it's built around projects." Workspaces are less isolated than tmux sessions but "much better suited for organizing different projects and agents side by side" — one for the main project, one for a side project, one for notes, one for testing agents, each keeping its own tabs, panes, and agent states in the sidebar [^src1].

Workspace keymaps: create `prefix shift-N`, close `prefix shift-D`, rename `prefix shift-W`, list/go-to `prefix G`, and a **workspace picker / nav mode** (`prefix W`) for jumping by number or arrow keys [^src1].

A separate **session** is the top-level container holding multiple workspaces: `herder session attach <name>`, `herder session list` (defaults to `default`), `herder session stop`, delete-after-stop. Sessions can't be renamed and have no switch keybind — "Herder leans more on workspaces" [^src1].

## Agent awareness (the differentiator)

The feature that separates Herder from tmux for agentic work: **it automatically detects coding agents running inside a workspace and shows their state** — working/running, idle, blocked (needs your permission), or done [^src1]. States are visible in the sidebar and in the go-to/list views, and can be filtered — "if you have more than 10 windows running agents everywhere… this is going to help you a lot." Agents keep running after you detach [^src1].

Relevant config [^src1]:
- **Resume Agents on Restore** (default `false`) — automatically resumes *supported* agents into their native conversation sessions after a server restart.
- **Show agent labels on pane borders** — displays the detected agent name on the pane.
- Supported agents are listed in the settings **integrations** tab (Hermes and Codex are shown as supported; Grok is not) [^src1].

This makes Herder a candidate persistence/observability layer for the same long-running-agent workflows that today run on [[mlops/tmux|tmux]] — see [[ai-engineering/long-running-agents|Long-Running Agents]].

## Remote mode (thin client)

Rather than SSHing into a box and running the multiplexer there (limited to the remote machine's keybindings and clipboard), Herder offers a **remote thin-client mode** from the local machine [^src1]:

```bash
herder --remote <server>                 # stream the remote Herder UI locally
herder --remote <server> --session <name>
```

"This streams the full interface back to your local terminal… now you're using your local key bindings with better clipboard support." Herder must be installed on the server [^src1].

## Custom commands and the Herda Plus plugin

Custom key commands run an **executable program** (not shell built-ins — `cd`/`ls`/`echo` won't work since commands aren't run through a shell); configured under `key.commands` in `config.toml`. Examples: open a file explorer (`prefix shift-E`, yazi), run a script, or open lazygit in a repo [^src1].

The **Herda Plus** plugin (requires v7.0) adds two fuzzy-list systems [^src1]:
- **Quick actions** (`prefix Y`) — all custom actions in one fuzzy-searchable list, with nestable selections; "you don't actually need to waste any key bindings."
- **Projects** (`prefix shift-O`) — jump to a directory *and* spin up a workspace pre-configured with the tabs, panes, working directory, and agents you want running immediately. Includes **Git Worktree** integration. Each action/project is a TOML file (`name`, `description`, `command`/`working_dir`).

## See also

- [[mlops/tmux|tmux]] — the incumbent Herder is modeled on and competes with; tmux's VPS-persistence pattern applies equally here
- [[mlops/terminal-and-shell|Terminal & Shell]] — the desktop terminal/shell layer Herder runs inside
- [[mlops/cli-tools|CLI Tools]] — lazygit, yazi, fzf and the other tools Herder's custom commands invoke
- [[mlops/terax|Terax]] — an adjacent "AI-native terminal" entity in the same dev-setup cluster
- [[ai-engineering/long-running-agents|Long-Running Agents]] — why agent-aware, persistent multiplexers matter
- [[mlops/README|MLOps hub]]

---

[^src1]: [The New Age of Modern Terminal Multiplexer Herder (Seth Phaeno)](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md) — [00:00](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=00:00) install + tmux inspiration; [00:53](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=00:53) session vs process state; [02:14](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=02:14) tabs/panes keymaps; [05:26](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=05:26) workspaces; [08:12](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=08:12) agent awareness; [13:12](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=13:12) remote mode; [14:40](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md#t=14:40) custom commands + Herda Plus plugin
