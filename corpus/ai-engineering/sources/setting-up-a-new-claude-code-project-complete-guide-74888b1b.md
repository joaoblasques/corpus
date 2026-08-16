---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-setting-up-a-new-claude-code-project-the-complete-guide-74888b1b.md
    channel: web
    ingested_at: 2026-08-16
aliases:
  - Claude Code setup guide
  - WHY/WHAT/HOW framework
  - CLAUDE.md best practices
  - .claude/rules
  - MCP setup
  - skills setup
  - Explore Plan Implement Commit
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-16
updated: 2026-08-16
url: https://www.builder.io/blog/setting-up-claude-code-project
origin: obsidian-list
---

# Setting Up a New Claude Code Project: The Complete Guide

**TL;DR** — Claude Code's native installer (no Node.js required) is now the standard. The real setup value comes from CLAUDE.md, .claude/skills/, and MCP servers, not from installation. A focused CLAUDE.md under 60–80 lines improves Claude's output more than any other configuration step.[^src1]

## Installation

Use the native installer — the npm method is deprecated:[^src1]

- macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`
- Homebrew: `brew install --cask claude-code` (no auto-update)
- WinGet: `winget install Anthropic.ClaudeCode`

After installing, `claude --version` to verify; run `claude` in any project directory to authenticate via OAuth. WSL is preferred on Windows for full Bash tool sandboxing.

## First session pattern

Follow the Explore, Plan, Implement, Commit workflow:[^src1]

1. Navigate to project, run `claude`
2. `/init` to bootstrap a CLAUDE.md (Claude scans project structure)
3. Explore before coding — ask Claude to summarize architecture
4. Use plan mode (Shift+Tab) to preview proposed changes before implementation
5. Review Claude output like a PR from a capable-but-fallible colleague

Key commands: `/help`, `/clear` (new conversation, keeps CLAUDE.md), `/compact` (compress context), `/config`.

## CLAUDE.md configuration

The WHY/WHAT/HOW framework (popularized by a HumanLayer post that earned 748 HN points):[^src1]

- **WHY**: what the project does and the problem it solves
- **WHAT**: tech stack, dependencies, project structure
- **HOW**: build, test, lint commands and verification steps

Constraints:[^src1]
- Keep to 60–80 lines; beyond that Claude deprioritizes instructions
- Keep code style rules out of CLAUDE.md — use linters/formatters instead
- Use `@imports` to reference external docs (chain up to 5 levels deep)
- `.claude/rules/**` directory: modular topic-specific rules, can be path-scoped via YAML frontmatter
- `CLAUDE.local.md`: personal overrides, auto-gitignored, not shared with team
- Auto-memory at `~/.claude/projects/<project>/memory/` accumulates patterns across sessions

## Skills

Custom skills live in `.claude/skills/` as directories with `SKILL.md` files (YAML frontmatter + instructions). Skills replace the older `.claude/commands/` approach but both still work. Claude loads skill name/description at session start, full content on invocation — keeps context window lean.[^src1]

Community ecosystem: over 1,300 community-built skills across Claude Code Plugins and Claude Plugins Directory.

## MCP configuration

Three scopes:[^src1]
- Local (default): private to user, stored in user config
- Project (`.mcp.json`): shared with team via git
- User (`~/.claude/`): available across all projects

Add via `claude mcp add` or `.mcp.json`. Keep to 5–6 servers per project; each consumes context window space. Store credentials as env vars, not raw strings in `.mcp.json` (which goes in version control). Recommended starters: Context7 (up-to-date API docs), Playwright (browser automation), a database connector.

## Best practices

- Initialize git first (safety net for rolling back any Claude change)[^src1]
- Use feature branches for AI-driven changes; review diff before merging
- Treat CLAUDE.md as a living document — update after architectural decisions
- Release channels: `latest` (default, newest features), `stable` (one week behind, skips regressions — better for production)
- Boris Cherny (engineering lead on Claude Code at Anthropic): start "surprisingly vanilla," add complexity only when you hit a real need

[^src1]: [Setting Up a New Claude Code Project: The Complete Guide](../../../raw/web/web-setting-up-a-new-claude-code-project-the-complete-guide-74888b1b.md) — Builder.io, 2026-06-29
