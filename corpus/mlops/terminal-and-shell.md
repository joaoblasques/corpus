---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-3L8htHUzAI4-terax-one-developer-built-an-ai-terminal-better-than-warp.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - terminal setup
  - shell setup
  - zsh
  - Alacritty
  - iTerm2
  - Powerlevel10k
  - nerd font
  - dotfiles
  - terminal emulator
  - WezTerm
  - Ghostty
  - Warp
tags:
  - corpus/mlops
  - concept
created: 2026-06-15
updated: 2026-06-25
confidence: 0.9
---

# Terminal & Shell

**TL;DR**: How to turn a default terminal into a fast, productive development environment: pick a **terminal emulator** (Alacritty for minimal/fast/cross-platform, or iTerm2 for features), a **shell** (zsh, the macOS default), a **prompt theme** (Powerlevel10k), a **nerd font** for icons, and a layer of zsh plugins and hacks [^src1][^src2][^src3]. The emulator draws the window; the shell runs the commands; the prompt/plugins make it ergonomic.

## Layers of a terminal setup

| Layer | Choice | Notes |
|---|---|---|
| Package manager | Homebrew | installs everything below on macOS [^src1][^src2] |
| Emulator | **Alacritty** or iTerm2 | Alacritty = minimal, fast, cross-platform (works on Linux too); iTerm2 = more built-in features many users don't need [^src1][^src2] |
| Shell | **zsh** | macOS default; check with `echo $0` [^src1] |
| Prompt theme | **Powerlevel10k** | `p10k configure` wizard; lean/rainbow styles [^src1][^src2] |
| Font | **MesloLGS Nerd Font** | required for prompt icons to render [^src1][^src2] |
| Multiplexer | tmux | windows/panes/sessions — see [CLI Tools](/mlops/cli-tools.md) |

## Alacritty configuration

Config lives in `~/.config/alacritty/alacritty.toml` (TOML); it auto-reloads on save [^src1]. Common settings [^src1]:

- `window.padding`, `window.decorations = "Buttonless"` (minimal look), `window.opacity`/`blur`.
- `[env] TERM = "xterm-256color"` — required for correct colors inside tmux/Neovim.
- `[font] normal.family` set to the nerd font; theme via an `import` array pointing at a themes file.

> A creator-reported migration: switched **from iTerm2 to Alacritty** for speed and simplicity, and moved **off Oh My Zsh to manual setup** because Oh My Zsh is "overkill" and "can slow down the terminal" [^src1]. An earlier setup by the same creator used iTerm2 + Oh My Zsh [^src2] — note the trajectory toward lighter tooling over time.

## zsh plugins & completion

- **zsh-autosuggestions** — suggests commands from history; accept with the right-arrow key [^src1][^src2].
- **zsh-syntax-highlighting** — colors valid vs. invalid commands as you type [^src1][^src2].
- **History search on arrow keys** — bind up/down to `history-search-backward`/`forward` so they filter by the prefix already typed [^src1].
- Oh My Zsh bundles plugins (e.g. `web-search` to Google from the shell) but adds weight [^src2].

## zsh power-user hacks

Once you outgrow Oh My Zsh and write your own config, zsh has deep built-ins [^src3]:

- **`edit-command-buffer`** widget — open the current command in `$EDITOR` (Neovim) to fix it with editor keybindings; bound to `Ctrl-X Ctrl-E` [^src3].
- **Undo / redo** — `Ctrl-_` undoes the last line-editor action (zsh has undo) [^src3].
- **`magic-space`** — bind to space to expand history references (e.g. `sudo !!`) *before* running, avoiding "Russian roulette" on what the previous command was [^src3].
- **`chpwd` hook** — run a command on every `cd`; used to auto-load a Python venv, a Nix dev shell, or `nvm use` on entering a project dir [^src3]. Only one `chpwd` function may be defined — use `add-zsh-hook` for multiple behaviors [^src3].
- **Suffix aliases** (`alias -s go=nvim`) — open a file by typing only its name, dispatched by extension [^src3].
- **Global aliases** (`alias -g NE='2>/dev/null'`) — usable anywhere in a command, not just at the start; convention: uppercase names [^src3].
- **`zmv`** — pattern-based batch move/rename (`autoload zmv`); `-n` dry-run, `-i` interactive [^src3].
- **Named directories** (`hash -d yt=~/projects/youtube`) — reference as `~yt` [^src3].
- **Custom widgets** via `zle`, and **`bindkey -s`** to insert boilerplate (e.g. a hotkey that types `git commit -m ""` with the cursor between the quotes) [^src3].

## Zinit-based zsh setup (alternative to Oh My Zsh)

**Zinit** is a lightweight zsh plugin manager — faster than Oh My Zsh with more control [^src5]:

```zsh
# ~/.zshrc — bootstrap Zinit
ZINIT_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/zinit/zinit.git"
[ ! -d "$ZINIT_HOME" ] && mkdir -p "$(dirname $ZINIT_HOME)" && \
  git clone --depth=1 https://github.com/zdharma-continuum/zinit "$ZINIT_HOME"
source "$ZINIT_HOME/zinit.zsh"

# Powerlevel10k (with JetBrains Mono Nerd Font)
zinit ice depth=1; zinit light romkatv/powerlevel10k

# The "Big Three" plugins
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions

# fzf integration (Ctrl-r reverse search → fuzzy, Ctrl-p/n to navigate)
source <(fzf --zsh)
zinit light Aloxaf/fzf-tab          # fuzzy tab completion menu
```

Key Powerlevel10k settings for a "zenful" setup: **Pure** style, transient prompt (removes prior headers), sparse spacing, instant prompt enabled [^src5].

### History configuration (critical for autosuggestions to work cross-session)

```zsh
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt APPEND_HISTORY SHARE_HISTORY HIST_IGNORE_SPACE
setopt HIST_IGNORE_ALL_DUPS HIST_SAVE_NO_DUPS HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
# Ctrl-p/n filtered by prefix
bindkey '^p' history-search-backward
bindkey '^n' history-search-forward
```

Zinit's `ice` command adds modifiers to the next plugin call (like "ice added to a drink") — e.g. `depth=1` → shallow git clone [^src5].

## macOS terminal: essential commands

50 macOS terminal commands worth knowing [^src6]:

| Category | Command | Notes |
|---|---|---|
| **System** | `caffeinate` | Keep Mac awake while terminal is running; `Ctrl-C` to stop |
| **Clipboard** | `pbcopy` / `pbpaste` | Copy stdin to clipboard; paste clipboard to stdout |
| **Network** | `ifconfig en0 \| grep inet` | Get IP address |
| | `traceroute example.com` | Trace path through internet routers |
| | `dig example.com` | DNS lookup |
| | `security find-generic-password -w -s "SSID"` | Retrieve a saved Wi-Fi password |
| **Files** | `ditto src dst` | macOS enhanced `cp`; preserves metadata |
| | `qlmanage -p file` | Quick Look preview from terminal |
| | `diff file1 file2` | Compare two files |
| **Processes** | `ps ax` | All running processes |
| | `top -o rsize` | Sort by memory usage |
| | `kill -9 <PID>` | Force-kill a process |
| **Misc** | `say "text"` | Text-to-speech |
| | `uptime` | How long since last boot |
| | `shutdown -r now` | Restart from terminal |

**Homebrew** is the prerequisite for most modern tools on macOS — "the missing package manager" [^src6]. See [Dev Environment Stack](/mlops/dev-environment-stack.md).

**TouchID for sudo** (requires `/etc/pam.d/sudo` edit): add `auth sufficient pam_tid.so` below the first comment line — `sudo` prompts use Touch ID instead of the password [^src6].

## AI-native terminal alternatives

Beyond traditional terminal emulators, a class of AI-native terminals is emerging:

- **[Terax](/mlops/terax.md)** — open-source, Tauri 2 + Rust, ~7 MB, <300 ms cold start; bundles terminal + code editor + file sidebar + browser + AI agent (Vercel AI SDK, any model). Agent proposes edits as reviewable diffs. Reviewer compared it favorably to Warp. Pre-1.0 with some rough edges (NeoVim crash, no sidebar keyboard nav) [^src4].
- **Warp** — commercial AI terminal; 58k+ GitHub stars; more mature but closed-source and VC-backed.
- **WezTerm** — fast, cross-platform, GPU-accelerated (used by the Terax reviewer as their personal choice alongside NeoVim) [^src4].
- **Ghostty** — modern cross-platform terminal emulator, referenced alongside WezTerm and NeoVim as high-performance alternatives.

The key distinction between tools like Terax and multi-agent setups via tmux: Terax's agent is scoped to code/files; tmux-based multi-agent setups give agents control of the whole terminal including panes and sessions [^src4].

## See also

- [CLI Tools](/mlops/cli-tools.md) — fzf, zoxide, eza, bat, tmux, etc., installed into this environment
- [tmux](/mlops/tmux.md) — terminal multiplexer for persistent sessions and multi-agent workflows
- [Terax](/mlops/terax.md) — AI-native terminal (Tauri 2 + Rust, 7 MB, built-in agent)
- [VPS for Agents](/mlops/vps-for-agents.md) — running terminal-based agents on a remote always-on server
- [Dev Environment Stack](/mlops/dev-environment-stack.md) — the shell + OS is Layer 1; Homebrew is the Layer-2 package manager here
- [Git](/mlops/git.md) — dotfiles (incl. this config) are version-controlled with git
- [MLOps hub](/mlops/README.md)

---

[^src1]: [How To Make Your Boring macOS Terminal Amazing With Alacritty (Josean Martinez)](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md) — Alacritty install [[01:21](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=01:21)], window config [[03:37](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=03:37)], Powerlevel10k [[05:48](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=05:48)], plugins [[10:37](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=10:37)]
[^src2]: [How To Make Your Boring Mac Terminal So Much Better (Josean Martinez)](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md) — iTerm2 + Oh My Zsh [[01:45](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md#t=02:11)], Powerlevel10k [[02:37](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md#t=02:37)], plugins [[07:31](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md#t=07:31)]
[^src3]: [10 Zsh hacks I wish I knew about sooner (Dreams of Code)](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md) — edit-command-buffer [[00:53](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=00:53)], undo [[02:10](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=02:10)], magic-space [[02:36](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=02:36)], chpwd [[03:55](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=03:55)], suffix aliases [[07:50](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=07:50)], global aliases [[09:10](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=09:10)], zmv [[11:19](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=11:19)], bindkey -s [[15:14](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=15:14)]
[^src4]: [Terax: One Developer Built an AI Terminal Better Than Warp (Better Stack)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md) — [00:00](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=00:00) overview; [01:09](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=01:09) Tauri vs Electron; [04:58](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=04:58) verdict; [05:18](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-terax-ai-terminal-report.md#t=05:18) vs CMUX
[^src5]: [This Zsh config is perhaps my favorite one yet (Dreams of Autonomy)](../../raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md) — [01:43](../../raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md#t=103) Zinit setup; [03:30](../../raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md#t=210) Powerlevel10k; [08:16](../../raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md#t=496) big three plugins; [10:03](../../raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md#t=603) history config; [13:34](../../raw/youtube/youtube-ud7YxC33Z3w-this-zsh-config-is-perhaps-my-favorite-one-yet.md#t=814) fzf-tab
[^src6]: [50 macOS Tips and Tricks Using Terminal (NetworkChuck)](../../raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md) — [00:26](../../raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md#t=26) WiFi passwords; [03:59](../../raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md#t=239) Linux commands on macOS; [08:30](../../raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md#t=510) Homebrew; [10:47](../../raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md#t=647) TouchID for sudo
</content>
