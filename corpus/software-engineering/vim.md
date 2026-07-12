---
type: entity
domain: software-engineering
status: draft
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
updated: 2026-07-12
---

# Vim

**TL;DR**: Vim is a highly configurable modal text editor released by Bram Moolenaar in 1991, descending from vi and qed. Its philosophy centers on composability — motions, operators, and text objects combine to produce powerful keyboard-driven editing with minimal keystrokes. **vim-galore** (★17,889) is the canonical all-things-Vim reference covering intro, basics, usage, tips, commands, and scripting [^src1].

## Philosophy

Vim adheres to the modal editing philosophy: "multiple modes and the meaning of keys changes according to the mode" [^src1]. This has a key advantage: "you don't have to break your fingers by holding several keys at once, most of the time you simply press them one after the other." Advanced users develop muscle memory — "complex operations are done using only a few key presses" — which reduces cognitive load [^src1].

## Modes

| Mode | Purpose |
|---|---|
| **Normal** | Navigation, editing commands |
| **Insert** | Type text |
| **Visual** | Select text (charwise, linewise, blockwise) |
| **Command-line** | Ex commands (`:w`, `:q`, `:s/find/replace/`) |
| **Operator-pending** | Awaiting a motion after an operator |

Vim has 12 modes total; 6 can be mapped [^src1].

## Composable editing model

The core grammar is **operator + motion** or **operator + text object**:

- `d` (delete) + `w` (word) = `dw` — delete next word
- `c` (change) + `i(` (inner parentheses) = `ci(` — change everything between parentheses
- `d` (delete) + `ap` (around paragraph) = `dap` — delete entire paragraph

Operators and motions both accept a count prefix: `2gUw` makes the rest of the current word and the next one uppercase [^src1].

**Text objects** work on surrounding regions rather than directional spans: `i` for inner, `a` for around. `diw` deletes the current word; `d2a(` removes the 2 inner pairs of parentheses and everything between them [^src1].

## Buffers, windows, and tabs

Three distinct levels of workspace [^src1]:

- **Buffer** — text loaded into memory, possibly associated with a file. May be active (visible), hidden, loaded, listed, or unnamed.
- **Window** — a viewport onto a buffer. Windows can be split vertically or horizontally. The same buffer can appear in multiple windows.
- **Tab page** — a collection of windows. Use tabs for multiple window layouts, not for "open files" as in other editors.

The buffer list is global and accessible from any tab [^src1].

## Registers

Registers are named clipboard slots. Yanking copies text in; pasting extracts it. Key register types [^src1]:

| Type | Character | Notes |
|---|---|---|
| Unnamed | `"` | Last yank or deletion |
| Numbered | `0`–`9` | `0` = last yank; `1`–`9` = deletion history queue |
| Named | `a`–`z`, `A`–`Z` | User-controlled; uppercase appends to lowercase |
| Read-only | `:`, `.`, `%` | Last command, last inserted text, current filename |
| Black hole | `_` | Discards without affecting other registers (`"_dd`) |
| Clipboard | `+`, `*` | System clipboard integration |
| Expression | `=` | Evaluates VimL at paste time (`<c-r>=5+5<cr>` inserts "10") |

Yank with `y`, paste with `p` (after cursor) or `P` (before). Vim distinguishes charwise and linewise visual selections [^src1].

## Marks

Marks remember a position (line + column) in a file [^src1]:

- **Lowercase** (`a`–`z`) — local to the current file
- **Uppercase** (`A`–`Z`) — global file marks, can switch buffers on jump
- **Automatic** — `''`/` `` ` `` ` (position before last jump), `'.` (last change), `'^` (last insertion stop), `'<`/`'>` (visual selection bounds)

Jump to a mark with `'m` (first non-blank of line) or `` `m `` (exact column). Marks can be used in ranges: `:'a,'bd` deletes from mark `a` to mark `b` [^src1].

## Motions and ranges

**Motions** move the cursor: `h/j/k/l`, `w/b/e`, `/pattern`, `G`, `%`, `()`/`{}`. All take a count: `2?the<cr>` jumps to the second last occurrence of "the" [^src1].

**Ranges** scope Ex commands to specific lines. Common forms [^src1]:

| Range | Lines |
|---|---|
| `%` | All lines (sugar for `1,$`) |
| `.` | Current line |
| `$` | Last line |
| `'<,'>` | Last visual selection (auto-inserted by `V:`) |
| `/^foo/,$` | From next line matching `^foo` to end |

`,` vs `;` as separator: with `,` the second address is relative to current line; with `;` it is relative to the first address [^src1].

## Undo tree

Vim's undo history is a **tree**, not a queue. Undoing then making a new change creates a branch; no history is lost [^src1]:

```
ifoo<esc>
obar<esc>
obaz<esc>
u
oquux<esc>
```

Results in the tree `foo → bar → baz` and `foo → bar → quux`. Two traversal modes:
- **Branch-wise** (`u`/`<c-r>`) — up/down the current branch
- **Time-wise** (`g-`/`g+`) — backwards/forwards in chronological order, crossing branches

`:earlier 2d` goes to text state from 2 days ago; `:earlier 1f` to the last file-save state [^src1].

## Changelist and jumplist

- **Changelist** — last 100 change positions; navigate with `g;` (older) / `g,` (newer)
- **Jumplist** — last 100 cursor jumps (triggered by `'`, `` ` ``, `G`, `/`, `?`, `n`, `N`, `%`, etc.); navigate with `<c-o>` (older) / `<c-i>` (newer)

Each window has its own jumplist; splitting copies it [^src1].

## Macros

Macros record keystrokes into a register for replay [^src1]:

1. `q<register>` — start recording (e.g., `qq`)
2. Perform keystrokes
3. `q` — stop recording
4. `[count]@q` — execute macro count times

Macros are stored in named registers and can be edited like text [^src1].

## Mappings

`:map` family defines key bindings per mode. The critical rule: **always use non-recursive mappings** (`nnoremap`, `inoremap`, etc.) unless recursion is intentional — recursive mappings expand the right-hand side through existing mappings, causing hard-to-debug chains [^src1].

| Recursive | Non-recursive | Modes |
|---|---|---|
| `:nmap` | `:nnoremap` | Normal |
| `:imap` | `:inoremap` | Insert |
| `:xmap` | `:xnoremap` | Visual |
| `:cmap` | `:cnoremap` | Command-line |
| `:omap` | `:onoremap` | Operator-pending |

**Mapleader** is a configurable placeholder (default `\`) for custom mappings: `nnoremap <leader>h :helpgrep<space>`. Set the mapleader before defining mappings; existing mappings won't update retroactively [^src1].

## Autocommands

Autocmds trigger actions on Vim events (buffer open/save, filetype detection, startup, etc.):

```vim
autocmd FileType ruby setlocal shiftwidth=2 softtabstop=2
```

Vim itself "relies extensively on autocmds" — filetype detection, syntax highlighting, and plugin hooks all use the autocmd system [^src1]. Autocmds of the same event fire in creation order.

## Quickfix and location lists

Both hold file-position entries (path + line + optional column + description), typically from compiler errors or grep results [^src1]:

| Feature | Quickfix | Location list |
|---|---|---|
| Count | One global list | One per window |
| Open | `:copen` | `:lopen` |
| Next | `:cnext` | `:lnext` |

Common workflow: `:grep! foo` + `:copen` to jump through all matches.

## Key commands for scripting

- `:global` / `:vglobal` — execute a command on all lines matching (or not matching) a pattern
- `:normal` — execute normal-mode commands from the command line (useful in scripts)
- `:execute` — evaluate a string as an Ex command (enables dynamic command construction)
- `:redir` / `execute()` — capture command output into a variable [^src1]

## Configuration

Vim reads `~/.vimrc` or `~/.vim/vimrc` at startup. The latter is preferred for version-controlling the entire configuration as a directory [^src1]. Feature sets (`tiny`, `small`, `normal`, `big`, `huge`) control which features are compiled in; `:version` shows the current build's features and patch level.

**Compatible mode** (vi-compatible defaults) is active unless a vimrc exists or Vim is started with `-N`. Compatible mode should be disabled [^src1].

## Completion

Insert-mode completions are triggered via `<c-x>` prefix [^src1]:

| Mapping | Completion type |
|---|---|
| `<c-x><c-n>` | Keywords from current file |
| `<c-x><c-f>` | File names |
| `<c-x><c-]>` | Tags |
| `<c-x><c-o>` | Omni (filetype-specific: struct members, class methods) |
| `<c-n>` / `<c-p>` | Generic keyword completion (respects `'complete'` option) |

## Neovim

Neovim is a fork of Vim that adds Lua scripting, async job control, and a clean API — the basis for modern plugin ecosystems (LSP clients, Tree-sitter, etc.). vim-galore covers both Vim and Neovim [^src1].

## Temporary files

Vim creates several file types to protect work [^src1]:

- **Swap files** (`.swp`) — unsaved changes; protect against crashes
- **Backup files** — previous version of a saved file
- **Undo files** — persistent undo tree across sessions
- **Viminfo** — command history, marks, registers between sessions

## Plugin ecosystem

vim-galore maintains a curated plugin list by topic [^src1]:

- **Fuzzy finders**: fzf, ctrlp.vim, denite.nvim
- **LSP**: coc.nvim, vim-lsp, languageclient-neovim
- **Version control**: vim-fugitive, vim-gitgutter, vim-signify
- **Completion**: YouCompleteMe, deoplete.nvim, asyncomplete.vim
- **Plugin managers**: vim-plug, dein.vim, vim-pathogen

## Getting started

```sh
$ vimtutor   # interactive built-in tutorial
```

Recommended learning path: complete `vimtutor` → create a minimal vimrc → learn basics → add plugins only after understanding native Vim capabilities [^src1].

## See also

- [Terminal / CLI Tools](/software-engineering/terminal-cli-tools.md) — Vim lives in the terminal
- [Xonsh](/software-engineering/xonsh.md) — Python-superset shell where Vim could be the configured editor

---

[^src1]: [vim-galore (mhinz)](../../raw/github/github-mhinz-vim-galore.md)
