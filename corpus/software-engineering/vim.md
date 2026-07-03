---
type: entity
domain: software-engineering
status: stub
sources:
  - path: raw/github/github-mhinz-vim-galore.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Vim
  - Neovim
  - vim-galore
  - Vi
  - vim editor
  - modal editor
tags:
  - corpus/software-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Vim

**TL;DR**: Vim is a highly configurable modal text editor. Its philosophy centers on composability — motions, operators, and text objects combine to produce powerful editing without leaving the keyboard. **vim-galore** (★17,889) is the canonical all-things-Vim reference: intro, basics, usage, tips, commands, and scripting [^src1].

## Core concepts

Vim is a **modal editor** — different keyboard modes for different operations [^src1]:

| Mode | Purpose |
|---|---|
| **Normal** | Navigation, editing commands |
| **Insert** | Type text |
| **Visual** | Select text |
| **Command-line** | Ex commands (`:w`, `:q`, `:s/find/replace/`) |

Key design: "most operations are composable" — an operator (`d` for delete) + a motion (`w` for word) = `dw` (delete next word). The number prefix multiplies: `3dw` deletes 3 words [^src1].

## Key structural concepts (vim-galore scope)

From the vim-galore table of contents [^src1]:

**Basics**:
- **Buffers, windows, tabs** — Vim's three levels of "open files"; a buffer is in memory, a window displays a buffer, tabs organize windows
- **Registers** — named clipboard slots for cut/copy/paste
- **Marks** — position bookmarks within and across files
- **Motions, operators, text objects** — the composable core (`c`, `d`, `y` + `w`, `b`, `e`, `i(`, `a"`, etc.)
- **Autocmds** — event hooks for automating tasks on file open/save/etc.
- **Undo tree** — branching undo history (not linear like most editors)

**Advanced**:
- **Macros** — recorded sequences played back with `@`
- **Global commands** — run a command on every line matching a pattern
- **Quickfix and location lists** — jump through error/search result lists
- **Debugging vimscript** — built-in debugger

## Neovim

Neovim is a fork of Vim that adds Lua scripting, async job control, and a clean API — the basis for many modern plugin ecosystems. vim-galore covers both Vim and Neovim [^src1].

## See also

- [Terminal / CLI Tools](/software-engineering/terminal-cli-tools.md) — Vim lives in the terminal
- [Xonsh](/software-engineering/xonsh.md) — Python-superset shell where Vim could be integrated as the editor

---

[^src1]: [vim-galore (mhinz)](../../raw/github/github-mhinz-vim-galore.md)
