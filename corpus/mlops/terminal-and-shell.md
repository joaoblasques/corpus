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
tags:
  - corpus/mlops
  - concept
created: 2026-06-15
updated: 2026-06-15
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
| Multiplexer | tmux | windows/panes/sessions — see [[mlops/cli-tools|CLI Tools]] |

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

## See also

- [[mlops/cli-tools|CLI Tools]] — fzf, zoxide, eza, bat, tmux, etc., installed into this environment
- [[mlops/dev-environment-stack|Dev Environment Stack]] — the shell + OS is Layer 1; Homebrew is the Layer-2 package manager here
- [[mlops/git|Git]] — dotfiles (incl. this config) are version-controlled with git
- [[mlops/README|MLOps hub]]

---

[^src1]: [How To Make Your Boring macOS Terminal Amazing With Alacritty (Josean Martinez)](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md) — Alacritty install [[01:21](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=01:21)], window config [[03:37](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=03:37)], Powerlevel10k [[05:48](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=05:48)], plugins [[10:37](../../raw/youtube/youtube-uOnL4fEnldA-how-to-make-your-boring-macos-terminal-amazing-with-alacritt.md#t=10:37)]
[^src2]: [How To Make Your Boring Mac Terminal So Much Better (Josean Martinez)](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md) — iTerm2 + Oh My Zsh [[01:45](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md#t=02:11)], Powerlevel10k [[02:37](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md#t=02:37)], plugins [[07:31](../../raw/youtube/youtube-CF1tMjvHDRA-how-to-make-your-boring-mac-terminal-so-much-better.md#t=07:31)]
[^src3]: [10 Zsh hacks I wish I knew about sooner (Dreams of Code)](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md) — edit-command-buffer [[00:53](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=00:53)], undo [[02:10](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=02:10)], magic-space [[02:36](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=02:36)], chpwd [[03:55](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=03:55)], suffix aliases [[07:50](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=07:50)], global aliases [[09:10](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=09:10)], zmv [[11:19](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=11:19)], bindkey -s [[15:14](../../raw/youtube/youtube-3fVAtaGhUyU-10-zsh-hacks-i-wish-i-knew-about-sooner.md#t=15:14)]
</content>
