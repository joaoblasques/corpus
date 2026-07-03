---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/github/github-0nn0-terminal-mac-cheatsheet.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - terminal
  - Mac terminal
  - command line
  - bash shortcuts
  - terminal cheatsheet
  - CLI shortcuts
  - terminal shortcuts
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Terminal / CLI Tools

**TL;DR**: The terminal is the primary interface for code, git, package managers, and dev tooling. Keyboard shortcuts dramatically accelerate navigation and editing. The Mac terminal (bash/zsh) shares a common shortcut vocabulary with most Unix-like CLIs [^src1].

## Mac terminal keyboard shortcuts

Reference from `terminal-mac-cheatsheet` (★7,392) [^src1]. Letters shown capitalized for readability only — Caps Lock should be off.

### Navigation shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + A` | Go to beginning of current line |
| `Ctrl + E` | Go to end of current line |
| `Ctrl + L` / `Cmd + K` | Clear the screen |
| `Ctrl + U` | Cut everything backward to line beginning |
| `Ctrl + K` | Cut everything forward to line end |
| `Ctrl + W` | Cut one word backward (space as delimiter) |
| `Ctrl + Y` | Paste whatever was cut by the last cut command |

### Process control

| Shortcut | Action |
|---|---|
| `Ctrl + C` | Kill current process; also clears current line |
| `Ctrl + D` | Exit current shell (no process) or send EOF to running process |
| `Ctrl + Z` | Suspend running process to background; `fg` restores it |

### History

| Shortcut | Action |
|---|---|
| `Up / Down arrows` | Cycle through previous commands |
| `Ctrl + R` | Reverse search command history |

## Core commands

```bash
# File system
ls -la              # list all files with details (hidden too)
cd <path>           # change directory; `cd ..` goes up one
mkdir <name>        # create directory
rm -rf <dir>        # remove directory recursively (destructive)
cp <src> <dst>      # copy file or directory
mv <src> <dst>      # move or rename

# Finding things
find . -name "*.md"            # find files by name pattern
grep -r "pattern" .            # recursive search in files

# File viewing
cat <file>           # print file contents
less <file>          # paginate through file
head / tail -n 20    # first/last 20 lines

# Permissions
chmod +x <file>      # make file executable
```

## See also

- [Git Basics](/software-engineering/git-basics.md) — most git operations happen in the terminal
- [Xonsh](/software-engineering/xonsh.md) — Python-superset shell that extends terminal capabilities

---

[^src1]: [terminal-mac-cheatsheet (0nn0)](../../raw/github/github-0nn0-terminal-mac-cheatsheet.md)
