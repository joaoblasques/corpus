---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - CLI tools
  - command-line tools
  - terminal tools
  - modern unix tools
  - zoxide
  - ripgrep
  - fzf
  - fd
  - bat
  - eza
  - tmux
  - jq
tags:
  - corpus/mlops
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# CLI Tools

**TL;DR**: A curated set of modern command-line tools that replace or augment legacy Unix utilities and make a terminal-based workflow faster. The recurring theme across three independent creators: **drop-in replacements for `cd`/`grep`/`find`/`cat`/`ls` with sane defaults** (ignore `.gitignore`, color, speed), plus a **fuzzy finder (`fzf`) and a multiplexer (`tmux`) as the two highest-leverage additions** [^src1][^src2][^src3]. Relevant now because AI coding agents (Claude Code, Gemini CLI) operate inside the terminal, making terminal fluency "more important than ever" [^src1].

## Legacy-replacement tools

| Modern tool | Replaces | Key wins |
|---|---|---|
| **zoxide** (`z`) | `cd` | fuzzy-matches against visited dirs; `z studio app` jumps to a deep path [^src1][^src3] |
| **ripgrep** (`rg`) | `grep` | "fast af"; respects `.gitignore`, recursive + color by default [^src1] |
| **fd** | `find` | faster, intuitive (`fd auth`), respects `.gitignore`, `--exclude` flag [^src1] |
| **bat** | `cat` | syntax highlighting, themes (e.g. Tokyo Night) [^src3] |
| **eza** | `ls` | colors, git status, icons, `--tree` view [^src3] |

The shared design philosophy: the legacy tools require flags (`grep -r --color`, `find -type f`) for behavior the modern tools enable by default, and they search noise like `node_modules` unless told otherwise [^src1][^src3]. A common pattern is to **alias the old name to the new tool** (`alias ls="eza ..."`, `alias cd="z"`) to keep muscle memory while gaining functionality [^src3].

## fzf — the fuzzy finder (force multiplier)

`fzf` is a fuzzy finder that filters any input list interactively; its power is in composition with other commands [^src1][^src2][^src3]:

- **`Ctrl-T`** — fuzzy-insert a file path into the current command [^src3].
- **`Ctrl-R`** — fuzzy-search shell history (cited as a major speedup) [^src2][^src3].
- **`**<Tab>`** — trigger completion for `cd`, `kill -9`, `ssh`, `export`, `unalias` [^src3].
- **Previews**: pair with `bat` (file preview) and `eza --tree` (dir preview) [^src3].

> **Gotcha (production caveat)**: don't become dependent on `fzf` before mastering plain `history`/`find`/`grep` — on a remote server where `fzf` isn't installed, `Ctrl-R` muscle memory leaves you stuck [^src2]. Master the fundamentals first.

## tmux — terminal multiplexer

`tmux` spawns multiple terminals as panes, windows, and sessions navigable from one screen [^src1][^src2]. Cited as having "the biggest impact" / "tmux is my window manager" [^src1][^src2]:

- **Keyboard-driven & app-agnostic** — bindings work regardless of terminal emulator, so switching emulators costs no relearning [^src1].
- **Session persistence** — reattach (`tmux a`) after a disconnect; critical over SSH so long-running tasks survive dropped connections [^src1].
- **Automation** — its CLI lets you script window creation (e.g. open a new git worktree + Claude Code agent in a fresh session) [^src1].

> **Contradiction (keybindings)**: one source builds a heavily customized tmux config with non-default bindings [^src1]; another argues emphatically to **never change the default keybindings** so they work on any machine in a production outage [^src2]. The disagreement is workflow philosophy (personalization vs. portability), not a factual conflict — both agree tmux is foundational.

## SSH (beyond login)

SSH is under-used as "just login"; its highest-leverage feature is **port forwarding** (`ssh -L 8080:localhost:8080 host`), which tunnels a local port to a service (even a container) on a remote machine — combine with tmux for multiple simultaneous tunnels [^src2]. One-off remote commands (`ssh host 'cat /etc/os-release'`) avoid an interactive session [^src2].

## Secrets & data tools

- **pass** (password-store) — "the standard Unix password manager"; GPG-encrypted files versioned in git, pushable to a remote repo; load secrets as env vars without writing them to shell history [^src1][^src2]. See [[mlops/git|Git]] (pass uses git under the hood).
- **Doppler** — a secrets-management platform; `doppler run -- <cmd>` injects per-environment secrets without storing them in a local `.env` (safer around AI agents that may read `.env` files) [^src1].
- **jq** — filter/transform JSON via stdin; staple for debugging and shell-script automation [^src1].
- **GitHub CLI (`gh`)** — perform GitHub actions (repos, issues, PRs) without leaving the terminal; pairs with agentic AI to auto-generate PR descriptions [^src1].
- **tldr** — community-maintained, example-first help pages as a friendlier alternative to `man` [^src3].
- **delta** — better git diffs; reuses the `bat` theme; supports side-by-side [^src3].
- **stow** (GNU Stow) — symlink-manages dotfiles so they can be git-versioned and reused across machines [^src1].
- **thefuck** — autocorrects the previous mistyped command [^src3].
- **Fabric** — a CLI wrapper for calling LLMs with reusable "patterns" (extract ideas, create summary); chainable via Unix pipes [^src2]. Configured here against the [[ai-engineering/claude-api|Claude/Anthropic API]] (see [[ai-engineering/README|AI Engineering]] for LLM specifics).

## See also

- [[mlops/terminal-and-shell|Terminal & Shell]] — where these tools are installed and configured (Alacritty, zsh, Powerlevel10k, fzf/zoxide/eza setup)
- [[mlops/linux-commands|Linux Commands]] — the legacy commands (`grep`, `find`, `cat`, `ls`) these tools replace
- [[mlops/git|Git]] — `gh` CLI and `pass`/`delta` build on git
- [[mlops/dev-environment-stack|Dev Environment Stack]] — these are Layer-1 system-foundation tooling
- [[mlops/README|MLOps hub]]

---

[^src1]: [10 CLI apps that have actually improved the way I work in the terminal (Dreams of Code)](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md) — zoxide [[01:20](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=01:20)], rg [[03:32](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=03:32)], fd [[06:09](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=06:09)], tmux [[08:18](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=08:18)], gh [[13:28](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=13:28)], Doppler [[14:46](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=14:46)], pass [[16:29](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=16:29)], jq [[18:39](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=18:39)], stow [[20:00](../../raw/youtube/youtube-EJ6uvqhKR4M-10-cli-apps-that-have-actually-improved-the-way-i-work-in-th.md#t=20:00)]
[^src2]: [5 CLI Tools That Actually Changed How I Work in 2026 (Mischa van den Burg)](../../raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md) — fzf [[00:00](../../raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md#t=00:00)], tmux/keybindings [[02:35](../../raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md#t=06:32)], SSH port-forward [[10:02](../../raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md#t=10:02)], pass [[14:22](../../raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md#t=14:22)], Fabric [[17:07](../../raw/youtube/youtube-tmnd3M1k5Jw-5-cli-tools-that-actually-changed-how-i-work-in-2026.md#t=17:07)]
[^src3]: [7 Amazing CLI Tools You Need To Try (Josean Martinez)](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md) — fzf [[00:25](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=00:25)], fd [[03:59](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=03:59)], bat [[06:25](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=06:25)], delta [[09:00](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=09:00)], eza [[10:16](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=10:16)], tldr [[12:52](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=12:52)], thefuck [[13:45](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=13:45)], zoxide [[14:40](../../raw/youtube/youtube-mmqDYw9C30I-7-amazing-cli-tools-you-need-to-try.md#t=14:40)]
</content>
</invoke>
