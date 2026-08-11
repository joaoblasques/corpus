---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/claude-code-power-user-tips-claude-help-center.md
    channel: web
    ingested_at: 2026-07-14
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-14
updated: 2026-08-11
provisional: false
url: "https://support.claude.com/en/articles/14554000-claude-code-power-user-tips"
origin: web
---

# Claude Code Power-User Tips (Anthropic Help Centre)

> First-party patterns collected from engineers on the Claude Code team at Anthropic. Covers parallel execution, planning, verification, automation, and customisation. [Source](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips)

**TL;DR:** The single most impactful practice is verification—giving Claude a closed feedback loop on its own output. Everything else (parallelism, plan mode, Opus-with-thinking, hooks, skills) compounds on top of that foundation.[^1]

---

## Working in parallel

The biggest productivity unlock the team identifies is running 3–5 sessions concurrently, each in an isolated git worktree.[^2]

- **CLI**: `claude --worktree` (or `claude --worktree my_worktree`); add `--tmux` to launch in a dedicated tmux pane.
- **Desktop app**: Code tab → worktree checkbox.
- **Non-git VCS** (Mercurial, Perforce, SVN): define `WorktreeCreate`/`WorktreeRemove` hooks in `settings.json`.

Navigation tips: named worktrees, shell aliases (`za`, `zb`, `zc`), colour-coded terminal tabs, terminal notifications. A dedicated "analysis" worktree for log-reading keeps it separate from change-making.[^2]

### Subagent worktree isolation

Add `isolation: worktree` to an agent's frontmatter to run it in its own worktree:[^3]

```markdown
# .claude/agents/worktree-worker.md
---
name: worktree-worker
model: haiku
isolation: worktree
---
```

Then prompt: "Migrate all sync IO to async … launch 10 parallel agents with worktree isolation. Each agent should test its changes end to end, then put up a PR."[^3]

### `/batch` for large migrations

`/batch` interviews the user about a migration, fans work to as many worktree agents as needed (dozens or hundreds), and each agent tests changes and opens its own PR independently.[^4]

---

## Planning before building

### Plan mode

`Shift+Tab` cycles into plan mode. Recommended flow: enter plan mode → refine plan → switch to auto-accept edits → Claude executes.[^5]

Team patterns:
- Have one Claude write the plan; spin up a second to review it "as a staff engineer."
- If execution goes sideways, switch back to plan mode and re-plan rather than course-correcting mid-stream.[^5]

### Model: Opus with thinking

The team's position: "It's the best coding model I've ever used … since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."[^6] Less steering + better tool use = faster net throughput despite larger size.

### Effort levels

`/effort` exposes levels: `low`, `medium`, `high`, `xhigh`, `max`, `auto`. Default is `high` on Team/Enterprise/API, `medium` otherwise. The team uses `high` for everything; `xhigh` for complex coding/agentic work; `max` for hard debugging or architecture decisions where unlimited reasoning is warranted—but `max` burns usage limits faster and should be activated per session.[^7]

---

## Prompting effectively

Push-back prompts the team uses:[^8]

- `"Grill me on these changes and don't make a PR until I pass your test."` — forces Claude to validate the developer's understanding before shipping.
- `"Prove to me this works."` — Claude diffs behaviour between `main` and the feature branch.
- `"Knowing everything you know now, scrap this and implement the elegant solution."` — useful after a mediocre first attempt.

Write detailed specs before handing work off; specificity reduces ambiguity and improves output quality.[^8]

### `/btw` for side questions

While Claude is actively working, `/btw` allows a single-turn question with full conversation context but no tool calls, without interrupting the active task.[^9]

---

## Learning with Claude

Claude Code can be configured as a teaching tool:[^10]

- Enable "Explanatory" or "Learning" output style in `/config` to get the *why* behind changes.
- Generate visual HTML presentations or ASCII diagrams for unfamiliar code or protocols.
- Build a spaced-repetition skill: explain your understanding, have Claude ask follow-up questions to fill gaps.[^10]

---

## CLAUDE.md and memory

### Invest in CLAUDE.md

A single `CLAUDE.md` at repo root, checked into git, shared across the team. Key discipline: whenever Claude makes a mistake, add the correction to `CLAUDE.md`.[^11]

After every correction: `"Update your CLAUDE.md so you don't make that mistake again."` — Claude is described as "very good at writing rules for itself."[^11]

### @claude in code reviews

Install the GitHub Action via `/install-github-app`, then tag `@claude` in PR comments to add learnings to `CLAUDE.md` as part of review. This is framed as "Compounding Engineering"—each correction improves every future session.[^12]

### Auto-memory

`/memory` configures the built-in memory system. Auto-memory saves preferences, corrections, and patterns between sessions; written to `~/.claude/projects/<project>/memory/`. This is separate from hand-maintained `CLAUDE.md` files.[^13]

---

## Verification — the #1 tip

> "Giving Claude a way to verify its work will markedly improve the quality of the final result." [^14]

If Claude can close the feedback loop on its own, it iterates until the output is right. Verification form varies by domain (bash commands, test suites, simulators, browser testing), but the principle is domain-agnostic.[^14]

### Chrome extension

For frontend work, install the Claude Code Chrome extension (Chrome or Edge, at `code.claude.com/docs/en/chrome`). Analogy: "if you ask someone to build a website but don't let them use a browser, will it look good?"[^15] The team uses it every time they work on web code.

### Desktop app web server testing

The Claude Desktop app bundles automatic web-server start and built-in browser testing. The same is achievable on CLI/VS Code via the Chrome extension.[^16]

### `/simplify` for code quality

Append `/simplify` to any prompt after making changes. It runs parallel agents reviewing changed code for reuse, quality, efficiency, and `CLAUDE.md` compliance in one pass.[^17]

---

## Commands, skills, and subagents

### Skills for repeated workflows

If a workflow runs more than once a day, turn it into a skill. Skills live at `.claude/skills/<name>/SKILL.md` and are shared with the team (`.claude/commands/` still works but is the legacy path).[^18]

Examples: a `/techdebt` command at session end to find duplicated code; a context-dump command that syncs Slack, GDrive, Asana, and GitHub; analytics-engineer agents that write dbt models and run tests in dev.[^18]

Slash commands can embed inline Bash to pre-compute context (e.g., `git status`) without extra model calls.[^18]

### Subagents for PR workflows

Drop `.md` files into `.claude/agents/`. Each agent can have a custom name, colour, tool set, allowed/disallowed tools, permission mode, and model. Set the session default via `"agent"` in `settings.json` or `claude --agent <name>`. `/agents` to get started.[^19]

`--agent` flag accepts any agent defined in `.claude/agents`; example read-only agent with `tools: Read` and a prompt restricting file edits.[^20]

Appending `"use subagents"` to any request directs Claude to offload sub-tasks, keeping the main agent's context window clean.[^21]

### Code review agents

When a PR opens, Claude can dispatch a team of agents each focused on a different concern (logic, security, performance) and post inline comments. The source notes Anthropic built this internally first; "code output per engineer increased significantly and reviews were the bottleneck."[^22]

---

## Hooks

Hooks run deterministic logic at agent lifecycle points.[^23]

| Event | Common use |
|---|---|
| `PreToolUse` | Dynamically load context on session start |
| `PostToolUse` | Log bash commands; auto-format after Write/Edit |
| `PermissionRequest` | Route prompts to Slack/Opus for review |
| `Stop` | Deterministic checks on long tasks |
| `ContextCompression` | Re-inject critical instructions after compression |

Example `PostToolUse` hook for auto-formatting:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [{ "type": "command", "command": "bun run format || true" }]
  }
]
```
[^24]

---

## Permissions and safety

### Pre-approve common commands

`/permissions` pre-allows safe commands and checks them into `.claude/settings.json`. Full wildcard syntax supported: `"Bash(bun run *)"`, `"Edit(/docs/**)"`. This is the recommended alternative to skipping permissions entirely—fewer prompts with an auditable allowlist.[^25]

### Auto mode

`claude --enable-auto-mode` lets classifiers evaluate each action before it runs—safe operations auto-approve, risky ones still flag. With the flag, `Shift+Tab` cycles: default → acceptEdits → plan → auto.[^26]

### Sandboxing

`/sandbox` opts into the open-source sandbox runtime (file + network isolation). Three modes: sandboxed BashTool with auto-allow, sandboxed BashTool with regular permissions, no sandbox.[^27]

### Long-running tasks

For very long tasks: prompt Claude to verify with a background agent when done; use an agent `Stop` hook for deterministic checks (preferred for auditable workflows). For sandboxed environments: `--permission-mode=dontAsk` or `--dangerously-skip-permissions`.[^28]

---

## Scheduling and recurring tasks

**`/loop`** schedules recurring local tasks for up to 3 days. Team examples:[^29]

```
/loop 5m /babysit     # shepherd PRs
/loop 30m /slack-feedback  # PRs for Slack feedback
/loop 1h /pr-pruner   # close stale PRs
```

**`/schedule`** runs jobs in the cloud—keeps working when the laptop is closed.[^30] Example: daily job that reviews all PRs shipped since yesterday and updates docs, then messages Slack via MCP.

---

## Mobile and remote control

- **Mobile app**: Claude app for iOS/Android, Code tab. iMessage plugin also available (`/plugin install imessage@claude-plugins-official`).[^31]
- **Teleport**: `claude --teleport` continues a cloud session locally; `/remote-control` controls a local session from phone or web. Available on Pro, Max, Team, Enterprise (CLI v2.1.51+).[^32]
- **Dispatch**: secure remote control for Claude Desktop; can use MCPs, browser, and computer for catching up on Slack/email or managing files remotely.[^33]

---

## Tool integrations (MCP)

Connect via `claude mcp add` or `"mcpServers"` in `settings.json`.[^34]

- **Data/analytics**: use `bq` CLI to pull and analyse metrics on the fly; the team notes "I haven't written a line of SQL in 6+ months." Works for any database with a CLI, MCP, or API.[^35]
- **Bug fixing**: enable Slack MCP, paste a bug thread, say "fix"—zero context switching. `"go fix the failing CI tests"` without micromanaging the how.[^36]
- **Plugins**: bundle LSPs (every major language), MCPs, skills, agents, and custom hooks. Install from the Anthropic marketplace or an internal one; check the marketplace reference into `settings.json` for auto-add.[^37]

---

## Customising the environment

- `/config` sets light/dark mode, output style (Explanatory, Learning, or custom), and editor mode (Vim keybindings).[^38]
- `/terminal-setup` enables `Shift+Enter` for newlines in IDE terminals, Warp, Alacritty. Apple Terminal not supported.[^38]
- `/statusline` generates a custom status line from `.bashrc`/`.zshrc`—show model, directory, context, cost, etc.[^39]
- `/color` changes the prompt input colour; useful when 3–5 sessions are open simultaneously.[^39]
- `/keybindings` remaps keys; stored in `~/.claude/keybindings.json`, live-reload.[^39]
- **Voice**: most of the team's coding is done by speaking; "you speak roughly 3× faster than you type, and your prompts get more detailed as a result."[^40] CLI: `/voice` then hold space bar. Desktop: microphone button. macOS: `fn×fn` for system dictation.
- **Spinner verbs**: customisable via `settings.json`; check in to share with the team.[^41]

---

## SDK and multi-repo work

- **`--bare`** for non-interactive SDK use: skips local CLAUDE.md/settings/MCP discovery for ~10× faster startup. The source notes this as "a design oversight" and says the default will flip to `--bare` in a future version.[^42]
- **`--add-dir`** (or `/add-dir`) grants access and permissions to additional folders for cross-repo work; or set `"additionalDirectories"` in `settings.json` for always-on inclusion.[^43]
- **`/branch`** (or `claude --resume <session-id> --fork-session`) forks an existing session.[^44]
- **Setup scripts** for cloud environments run before each new session to install dependencies, configure settings, and set env vars; skipped on resume.[^45]

---

## Relation to corpus pages

- [Claude Code](/ai-engineering/claude-code.md) — first-party (Anthropic help centre) guidance; outranks third-party tips on intended behaviour.
- [How to Maximize Claude Code Effectiveness (Towards Data Science)](/ai-engineering/sources/how-to-maximize-claude-code-effectiveness-towards-data-scien-ce.md) — third-party companion covering the same slash-command/plan-mode surface.
- [Agentic Coding](/ai-engineering/agentic-coding.md) — the practice these tips serve.
- [AI Engineering hub](/ai-engineering/README.md)

---

[^1]: raw/web/claude-code-power-user-tips-claude-help-center.md — "The single most impactful tip in this guide is verification … If you only adopt one practice, make it that one."
[^2]: raw/web/claude-code-power-user-tips-claude-help-center.md — parallel sessions / worktree section.
[^3]: raw/web/claude-code-power-user-tips-claude-help-center.md — subagents with worktree isolation section.
[^4]: raw/web/claude-code-power-user-tips-claude-help-center.md — `/batch` section.
[^5]: raw/web/claude-code-power-user-tips-claude-help-center.md — plan mode section.
[^6]: raw/web/claude-code-power-user-tips-claude-help-center.md — "It's the best coding model I've ever used … almost always faster than using a smaller model in the end."
[^7]: raw/web/claude-code-power-user-tips-claude-help-center.md — effort level section.
[^8]: raw/web/claude-code-power-user-tips-claude-help-center.md — prompting effectively section.
[^9]: raw/web/claude-code-power-user-tips-claude-help-center.md — `/btw` section.
[^10]: raw/web/claude-code-power-user-tips-claude-help-center.md — learning with Claude section.
[^11]: raw/web/claude-code-power-user-tips-claude-help-center.md — CLAUDE.md investment section.
[^12]: raw/web/claude-code-power-user-tips-claude-help-center.md — @claude in code reviews section.
[^13]: raw/web/claude-code-power-user-tips-claude-help-center.md — auto-memory section.
[^14]: raw/web/claude-code-power-user-tips-claude-help-center.md — verification section.
[^15]: raw/web/claude-code-power-user-tips-claude-help-center.md — Chrome extension section; "if you ask someone to build a website but don't let them use a browser, will it look good?"
[^16]: raw/web/claude-code-power-user-tips-claude-help-center.md — Desktop app for web servers section.
[^17]: raw/web/claude-code-power-user-tips-claude-help-center.md — `/simplify` section.
[^18]: raw/web/claude-code-power-user-tips-claude-help-center.md — skills for repeated workflows section.
[^19]: raw/web/claude-code-power-user-tips-claude-help-center.md — subagents for PR workflows section.
[^20]: raw/web/claude-code-power-user-tips-claude-help-center.md — `--agent` for custom system prompts section.
[^21]: raw/web/claude-code-power-user-tips-claude-help-center.md — leveraging subagents at runtime section.
[^22]: raw/web/claude-code-power-user-tips-claude-help-center.md — code review agents section; "code output per engineer increased significantly and reviews were the bottleneck."
[^23]: raw/web/claude-code-power-user-tips-claude-help-center.md — hooks section.
[^24]: raw/web/claude-code-power-user-tips-claude-help-center.md — PostToolUse hook example.
[^25]: raw/web/claude-code-power-user-tips-claude-help-center.md — pre-approve common commands section.
[^26]: raw/web/claude-code-power-user-tips-claude-help-center.md — auto mode section.
[^27]: raw/web/claude-code-power-user-tips-claude-help-center.md — sandboxing section.
[^28]: raw/web/claude-code-power-user-tips-claude-help-center.md — long-running tasks section.
[^29]: raw/web/claude-code-power-user-tips-claude-help-center.md — `/loop` section.
[^30]: raw/web/claude-code-power-user-tips-claude-help-center.md — `/schedule` section.
[^31]: raw/web/claude-code-power-user-tips-claude-help-center.md — mobile section.
[^32]: raw/web/claude-code-power-user-tips-claude-help-center.md — teleport section.
[^33]: raw/web/claude-code-power-user-tips-claude-help-center.md — Dispatch section.
[^34]: raw/web/claude-code-power-user-tips-claude-help-center.md — MCP tool integrations section.
[^35]: raw/web/claude-code-power-user-tips-claude-help-center.md — data and analytics section; "I haven't written a line of SQL in 6+ months."
[^36]: raw/web/claude-code-power-user-tips-claude-help-center.md — bug fixing section.
[^37]: raw/web/claude-code-power-user-tips-claude-help-center.md — plugins section.
[^38]: raw/web/claude-code-power-user-tips-claude-help-center.md — terminal setup and `/config` section.
[^39]: raw/web/claude-code-power-user-tips-claude-help-center.md — status line, color, keybindings section.
[^40]: raw/web/claude-code-power-user-tips-claude-help-center.md — voice input section; "you speak roughly 3× faster than you type."
[^41]: raw/web/claude-code-power-user-tips-claude-help-center.md — spinner verbs section.
[^42]: raw/web/claude-code-power-user-tips-claude-help-center.md — `--bare` section; "a design oversight … the default will flip to --bare."
[^43]: raw/web/claude-code-power-user-tips-claude-help-center.md — `--add-dir` section.
[^44]: raw/web/claude-code-power-user-tips-claude-help-center.md — forking a session section.
[^45]: raw/web/claude-code-power-user-tips-claude-help-center.md — setup scripts section.
