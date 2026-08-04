---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/github/github-addyosmani-gemini-cli-tips.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-eliasecchig-gemini-cli-git.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-jamubc-gemini-mcp-tool.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/notes/notes-03-resources-study-notes-ai-tools-claude-code-and-gemini-cli-in-the-terminal-networkc.md
    channel: notes
    ingested_at: 2026-07-05
  - path: raw/notes/notes-03-resources-study-notes-ai-tools-gemini-cli-web-ui-for-browser-access.md
    channel: notes
    ingested_at: 2026-07-05
  - path: raw/notes/notes-03-resources-study-notes-claude-code-boost-efficiency-with-gemini-cli-integration.md
    channel: notes
    ingested_at: 2026-07-06
  - path: raw/notes/notes-03-resources-study-notes-gemini-cli-deep-dive-with-mcps.md
    channel: notes
    ingested_at: 2026-07-10
  - path: raw/notes/notes-03-resources-study-notes-gemini-cli-free-coding-agent-complete-guide.md
    channel: notes
    ingested_at: 2026-07-10
  - path: raw/notes/notes-03-resources-study-notes-gemini-cli-multi-instance-coding-workflow-with-mcps.md
    channel: notes
    ingested_at: 2026-07-10
  - path: raw/notes/notes-03-resources-articles-gemini-cli-tips-tricks-agentic-coding.md
    channel: notes
    ingested_at: 2026-07-19
  - path: raw/notes/notes-03-resources-articles-superpowers-agentic-skills-framework-tdd-workflow.md
    channel: notes
    ingested_at: 2026-07-20
aliases:
  - Gemini CLI
  - gemini-cli
  - Google Gemini CLI
  - Antigravity CLI
  - agy
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-25
updated: 2026-08-04
---

# Gemini CLI

**TL;DR.** Gemini CLI is Google's open-source agentic coding CLI — the Gemini counterpart to Claude Code. It uses `GEMINI.md` as its persistent context file (analogous to `CLAUDE.md`), supports custom slash commands, MCP server extension, memory recall, checkpointing/restore, and a headless/scripting mode. The Addy Osmani tip collection (2,382★) documents ~30 power-user patterns [^src1]; a companion article-length guide independently surveys the same ~30 agentic-coding tips, covering setup, authentication, persistent context, custom slash commands, and CI/CD integration [^src11].

## Core concepts

### GEMINI.md (persistent context)

`GEMINI.md` is the Gemini CLI equivalent of `CLAUDE.md` — a markdown file in the project root that is auto-loaded at session start, providing persistent project context [^src1]. Key differences from `CLAUDE.md`:
- Supports `@file` and `@folder` references to pull in additional context files on demand
- Can include `## Tools` and `## Constraints` sections that Gemini interprets as capability/permission declarations
- Is checked into the repo and shared with the team

### Custom slash commands

Gemini CLI supports project-level and user-level custom slash commands stored in `.gemini/commands/` (project) or `~/.gemini/commands/` (user) [^src1]. The format is a markdown file with a frontmatter block declaring the command name, description, and optional tool permissions.

Custom commands are the Gemini CLI equivalent of Claude Code skills — load on demand, describe the workflow, and invoke with a slash prefix. See [Agent Skills](/ai-engineering/agent-skills.md) for the cross-tool concept.

### MCP extension

Gemini CLI supports MCP servers in `~/.gemini/mcp.json` (user-level) or `.gemini/mcp.json` (project-level) [^src1]. Standard MCP configuration format:
```json
{
  "mcpServers": {
    "myserver": {
      "command": "npx",
      "args": ["my-mcp-server"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

Tool approval: Gemini CLI prompts for tool approval on first use in a session; auto-approve is configurable per server.

A deep-dive walkthrough demonstrates the practical MCP surface across three scenarios: building a Next.js chat app, a DuckDuckGo search MCP, and HuggingFace + Context7 MCPs — with the takeaway that the combination of built-in tools, the DuckDuckGo MCP, and Context7 MCPs covers most development needs [^src4]. Gemini CLI also ships built-in Google Search integration as a first-class tool for grounding [^src7].

### Interfaces beyond the terminal

Gemini CLI is not terminal-only. A **Web UI** provides a browser-based interface accessible from any browser, letting users manage projects, select models, and execute tasks without terminal comfort [^src5]. The CLI's own strengths derive from the terminal model: persistent context across a session and direct file-system access are cited as its key productivity advantages, with WSL recommended for Windows users [^src6].

## Key tips (30 documented by Addy Osmani)

### Context and memory
- **Memory recall**: Gemini CLI maintains a per-project memory store; use `/memory add "fact"` to explicitly store facts and `/memory` to view the current store [^src1]
- **Context files**: `@include path/to/file.md` in a prompt or in `GEMINI.md` pulls file content into context — the GEMINI.md version is always-on, the prompt version is on-demand
- **`/compress`**: compresses conversation history when context fills, similar to Claude Code's `/compact` [^src1]

### Checkpointing
- **`/checkpoint`**: saves the current session state (conversation + file state) to a named checkpoint [^src1]
- **`/restore <name>`**: restores a checkpoint — enables rollback to any prior state without `git reset`
- Checkpoints are stored in `.gemini/checkpoints/`; each is a JSON snapshot of the session

### Headless mode and scripting
- **`gemini -p "task"`**: non-interactive mode for one-shot tasks, scripted pipelines, and CI integration [^src1]
- **`--output json`**: returns structured JSON responses for programmatic consumption
- **`--no-confirm`**: runs without approval prompts (equivalent to Claude Code's `--dangerously-skip-permissions`)
- Environment variable `GEMINI_NONINTERACTIVE=true` disables all interactive prompts

### VS Code integration
- Gemini CLI is available as a VS Code extension (Gemini Code Assist); same `GEMINI.md` and command system applies within the IDE [^src1]
- The extension uses the same MCP configuration as the CLI — no separate config needed

### Telemetry and privacy
- Telemetry is enabled by default; `telemetryEnabled: false` in `~/.gemini/config.json` disables it [^src1]
- Models used: Gemini 2.5 Pro (default); configurable to Gemini 2.5 Flash (faster, cheaper) via `--model gemini-2.5-flash`
- Free tier: 60 requests/minute via the Gemini API free tier; Pro tier: higher limits

### GitHub Action
- Gemini CLI ships an official GitHub Action (`google-gemini/gemini-cli-action`) for CI integration [^src1]
- Trigger patterns: PR creation, push to branch, comment trigger (`/gemini review`)
- Outputs: PR comments, file changes committed directly, or structured JSON for downstream steps

## Capability profile and workflows

### Strengths and weaknesses

As a free coding agent, Gemini CLI **excels at adding features and making changes to existing codebases** but **struggles to build new projects from scratch** [^src7]. Its interactive mode drives AI-driven task development against an existing repo [^src7].

### Multi-instance parallelism

Multiple Gemini CLI instances can be run **in parallel**, each with a separate context, for concurrent coding workflows with MCP integration [^src8]. Practical observations from running instances in parallel include **model throttling behavior on Gemini 2.5 Pro**, which pushes workflows toward Gemini 2.5 Flash for the throttle-sensitive instances [^src8].

## Comparison with Claude Code

| Dimension | Gemini CLI | Claude Code |
|---|---|---|
| **Context file** | `GEMINI.md` | `CLAUDE.md` |
| **Slash commands** | `.gemini/commands/` | `.claude/skills/` |
| **Checkpointing** | Built-in (`/checkpoint`) | `/rewind` (session-level) |
| **Memory** | `/memory` command | Auto-memory + `MEMORY.md` |
| **Headless mode** | `gemini -p` | `claude -p` |
| **MCP** | `.gemini/mcp.json` | `claude mcp add` / `.mcp.json` |
| **Model** | Gemini 2.5 Pro/Flash | Claude Sonnet/Opus/Fable |
| **Open source** | Yes | No |
| **Free tier** | Yes (API free tier) | No (subscription) |

The conceptual parallels are close enough that practitioners use both tools: Gemini CLI for tasks using Google Workspace connectors (Google Docs, Sheets, Drive) and Claude Code for everything else [^src1].

## gemini-cli-git — Git as a self-improving agent backend

A companion project that turns a Git repository into an autonomous, self-improving agent using Gemini CLI and GitHub Actions [^src2].

**The core idea**: Git events (open issue, PR comment, merge to main) become the task queue. The agent reads the event, acts, pushes back [^src2]:

| Git event | Agent action |
|---|---|
| Issue opened | Auto-assigned to Gemini; agent reads → implements → opens PR |
| PR comment | Agent reads feedback → revises code → updates PR |
| PR merged to main | Agent learns from the merge; updates its own `AGENTS.md` learnings file |

**Three work modes** [^src2]:
1. **Scheduled**: cron-triggered prompt (check issues, triage, draft solutions)
2. **On-demand**: `@gemini` mention in issue body or PR comment triggers immediate action
3. **Iterative**: back-and-forth PR review conversation until the reviewer approves

**Why this matters**: the merge-to-learn pattern closes a feedback loop that most coding agents leave open — every accepted change teaches the agent something (the learnings file is its persistent memory of "this is what the team actually approves"). [^src2]

Functionally equivalent to the "merge as teaching event" pattern discussed in [Spec-Driven Development](/ai-engineering/spec-driven-development.md).

## See also

- [Claude Code](/ai-engineering/claude-code.md) — primary comparison; parallel architecture
- [Agent Skills](/ai-engineering/agent-skills.md) — slash commands in Gemini CLI are the same concept as skills
- [MCP](/ai-engineering/mcp.md) — MCP server support is shared infrastructure across all major coding CLIs
- [Pi Agent](/ai-engineering/pi-agent.md) — another open-source coding agent alternative
- [Agentic Coding](/ai-engineering/agentic-coding.md) — landscape comparison of coding agents
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [addyosmani/gemini-cli-tips — ~30 power-user tips for Gemini CLI](../../raw/github/github-addyosmani-gemini-cli-tips.md) — Addy Osmani, GitHub ★2,382
[^src2]: [eliasecchig/gemini-cli-git — Turn your Git repo into a self-improving autonomous agent](../../raw/github/github-eliasecchig-gemini-cli-git.md) — GitHub
[^src3]: [jamubc/gemini-mcp-tool — MCP server enabling Claude to interact with Gemini CLI (★2,245)](../../raw/github/github-jamubc-gemini-mcp-tool.md) — GitHub; primary source for Antigravity CLI retirement announcement
[^src4]: [Gemini CLI — Deep Dive with MCPs](/ai-engineering/sources/gemini-cli-deep-dive-with-mcps-c.md) — study note (obsidian quick-intake); Next.js chat app, DuckDuckGo MCP, HuggingFace + Context7 MCP walkthroughs
[^src5]: [AI Tools — Gemini CLI Web UI for Browser Access](/ai-engineering/sources/ai-tools-gemini-cli-web-ui-for-browser-access-acce.md) — study note (obsidian quick-intake)
[^src6]: [AI Tools — Claude Code and Gemini CLI in the Terminal (NetworkChuck)](/ai-engineering/sources/ai-tools-claude-code-and-gemini-cli-in-the-terminal-networkc-ec.md) — study note (obsidian quick-intake)
[^src7]: [Gemini CLI — Free Coding Agent Complete Guide](/ai-engineering/sources/gemini-cli-free-coding-agent-complete-guide-de.md) — study note (obsidian quick-intake)
[^src8]: [Gemini CLI — Multi-Instance Coding Workflow with MCPs](/ai-engineering/sources/gemini-cli-multi-instance-coding-workflow-with-mcps-c.md) — study note (obsidian quick-intake)
[^src9]: [Claude Code — Boost Efficiency with Gemini CLI Integration](/ai-engineering/sources/claude-code-boost-efficiency-with-gemini-cli-integration-ea.md) — study note (obsidian quick-intake)
[^src10]: [Superpowers — Agentic Skills Framework for TDD-First Software Development](/ai-engineering/sources/superpowers-agentic-skills-framework-for-tdd-first-software--f.md) — article note (obsidian quick-intake)
[^src11]: ["Gemini CLI: ~30 Tips for Agentic Coding in the Terminal"](/ai-engineering/sources/gemini-cli-30-tips-for-agentic-coding-in-the-terminal-cd.md) — article note (obsidian quick-intake)

## Gemini CLI retirement and Antigravity CLI successor

On **2026-06-18**, Google retired the Gemini CLI for free, Google AI Pro, Google AI Ultra, and individual Gemini Code Assist users [^src3]. Its successor is the **Antigravity CLI** (`agy`).

**Migration** [^src3]:
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash   # macOS / Linux
```
Run `agy` once to sign in. The gemini-mcp-tool (MCP bridge for Claude Code integration) auto-selects `agy` backend from 2026-06-18.

**Who is unaffected** [^src3]: enterprise / standard-license users or paid-API-key users retain Gemini CLI access unchanged.

## Gemini MCP Tool — Claude Code + Gemini/Antigravity CLI bridge

The `gemini-mcp-tool` (★2,245) is an MCP server that lets Claude Code delegate tasks to Gemini's massive context window (1M+ tokens) via the `@` syntax [^src3].

**Primary use case** [^src3]: large file analysis and full-codebase understanding — tasks where Gemini's 1M token window is a decisive advantage over Claude's smaller context in cost-sensitive situations. "A party of 3" — Claude + Gemini reasoning together on the same task.

**Install** [^src3]: `npm install -g gemini-mcp-tool`, then add to Claude Code's MCP config. The tool auto-detects whether to use `gemini` or `agy` based on the installation date.

**Sub-contractor pattern** [^src9]: the recommended integration pattern is to use Gemini CLI as a **sub-contractor for Claude Code** when a task exceeds Claude's context window — Claude delegates large-analysis / large-codebase-understanding work to Gemini, whose larger context window absorbs the full input, then hands results back. This reinforces the "party of 3" framing above from the tool's own docs [^src3].

## Cross-tool frameworks

Gemini CLI participates in the same agentic-skills ecosystem as other coding agents. **Superpowers** — an agentic skills framework and software-development methodology that guides agents through a deliberate professional workflow emphasizing YAGNI, DRY, and red/green TDD — is published on the Claude Code, Cursor, and **Gemini CLI** plugin marketplaces [^src10], making the same TDD-first workflow portable across all three. See [Agent Skills](/ai-engineering/agent-skills.md) for the underlying skills concept.
