---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - VS Code
  - Visual Studio Code
  - vscode
  - code editor
tags:
  - corpus/mlops
  - entity
created: 2026-06-15
updated: 2026-06-15
---

# VS Code

**TL;DR**: Visual Studio Code is Microsoft's "lightweight but powerful" code editor. Its core mental model is **folder-as-project**: most of its power comes from opening a *folder* (a workspace), not a single file, then working across the files inside it via the sidebar panels, integrated terminal, command palette, and extensions [^src1].

## Opening: file vs. folder vs. CLI

- **File** vs. **folder** — opening a single file gives you an editor; opening a folder loads the whole project into the Explorer so you can work across all its files [^src1].
- **`code .`** — launch VS Code on the current directory from the terminal. If `code` is "command not found", run *Shell Command: Install 'code' command in PATH* from the command palette, then relaunch the terminal [^src1].
- An unsaved file shows a dot on its tab; save with `Cmd/Ctrl-S`, or *Save All* (`Opt+Cmd+S`) [^src1].

## Sidebar panels

| Panel | Purpose |
|---|---|
| **Explorer** | file/folder tree of the open project; add files/dirs, refresh, collapse-all [^src1] |
| **Search** | global text search across all project files; case-match, whole-word, regex, and find-and-replace (replace is destructive — it saves the files) [^src1] |
| **Source Control** | built-in git integration: stage, commit, write messages [^src1] |
| **Run & Debug** | step through code line-by-line; configure a debugger per language (Node.js, Chrome/Edge for web) [^src1] |
| **Extensions** | add functionality; official (Microsoft) and third-party extensions (Python, C/C++, Jupyter, Live Server) [^src1] |

## Integrated terminal

*Terminal → New Terminal* opens a shell rooted at the open folder; on modern macOS the default is zsh [^src1]. You can run commands against the project directory and keep **multiple terminals** open side-by-side (e.g. one for frontend, one for the backend server) [^src1]. See [[mlops/terminal-and-shell|Terminal & Shell]].

## Search bar & command palette

The top search bar is multi-purpose [^src1]:

- **Go to File** (`Cmd/Ctrl-P`) — fuzzy-open a file by name.
- **Command Palette** (`Shift+Cmd/Ctrl-P`) — run any command exposed by VS Code or an extension; "anything you can do in the UI or menus, you can do in the command palette" [^src1].

## Settings: user vs. workspace

Settings apply at two scopes [^src1]:

- **User** — global default across all projects.
- **Workspace** — per-folder overrides of the user settings (e.g. enable autosave only for this project).

`files.autoSave` (e.g. `afterDelay`), font size/family, and tab size are commonly tuned settings [^src1].

## See also

- [[mlops/terminal-and-shell|Terminal & Shell]] — VS Code's integrated terminal runs your configured shell
- [[mlops/git|Git]] — VS Code's Source Control panel wraps git
- [[ai-engineering/claude-code|Claude Code]] — terminal-native coding agent, an alternative/complement to an editor like VS Code (ai-engineering)
- [[mlops/README|MLOps hub]]

---

[^src1]: [The Only VS Code Tutorial You Will Ever Need (The Common Coder)](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md) — open file/folder [[01:44](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=01:44)], `code .` in PATH [[05:37](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=05:37)], panels [[07:23](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=07:23)], search/replace [[10:00](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=10:00)], integrated terminal [[16:03](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=16:03)], command palette [[19:30](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=19:30)], settings [[21:13](../../raw/youtube/youtube-YIqF5STcc0Q-the-only-vs-code-tutorial-you-will-ever-need.md#t=21:13)]
</content>
