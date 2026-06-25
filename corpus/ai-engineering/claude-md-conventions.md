---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/github-abhishekray07-claude-md-templates-claude-md-best-prac.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-multica-ai-andrej-karpathy-skills-a-single-claude-md.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-17-multica-ai-andrej-karpathy-skills-a-single-claude-md-file-to.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/cursor-rules-in-action-how-our-engineers-use-it-at-atlan.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-04-17-cross-platform-agent-skills-guide-claude-code-codex-cursor-c.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/github-cursor-plugins-cursor-plugin-specification-and-offici.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-everyinccompound-engineering-plugin-official-compound-engine.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/youtube/d8BGxfW3Vj4-the-karpathy-claude-md-file-that-43-000-developers-installed.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-claude-code-karpa-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - CLAUDE.md
  - AGENTS.md
  - cursor rules
  - .mdc rules
  - agent instruction files
  - claude.md best practices
  - cross-platform skills
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-25
---

# CLAUDE.md & Agent Instruction Conventions

**TL;DR**: Coding agents read project conventions from markdown instruction files — `CLAUDE.md` (Claude Code), `AGENTS.md` (generic), and `.cursor/rules/*.mdc` (Cursor). The governing constraint is an **attention budget**: every line competes for a model's limited reliable-instruction capacity, so these files must be lean, assertive, and scoped [^src1]. A parallel goal is making the same conventions portable across agents (Claude Code, Codex, Cursor, Copilot) [^src3].

## The file hierarchy (Claude Code)

Claude Code reads instructions from three scopes, concatenated into context at session start [^src1]:

| File | Scope | Use for |
|---|---|---|
| `~/.claude/CLAUDE.md` | Global (every project) | Personal preferences — "always run tests", "ask before committing". Keep under ~15 lines |
| `.claude/CLAUDE.md` | Project (committed to git) | Stack, structure, commands, team conventions, domain knowledge |
| `./CLAUDE.local.md` | Local (gitignored) | Personal overrides — your terminal, your MCP servers |

Files are concatenated, not overridden; on conflict the model follows the **last** one read, and `CLAUDE.local.md` loads after `CLAUDE.md` so personal notes get the final word at each level [^src1]. Subdirectory `CLAUDE.md` files (e.g. `src/auth/CLAUDE.md`) load **on demand** only when working in that directory, keeping the root file lean [^src1].

## The attention budget — why less is more

Claude Code's system prompt already contains ~50 instructions — "a third of the ~150–200 instruction limit frontier models can reliably follow" [^src1]. The practical benchmark: if a project `CLAUDE.md` exceeds ~80 lines (HumanLayer keeps theirs under 60), the model "starts ignoring parts of it" [^src1]. This is the same context-rot constraint covered in [[ai-engineering/context-window-management|Context Window Management]].

### What to put where

| Rule | Scope | Why |
|---|---|---|
| "Run tests after changes" | Global | Wanted everywhere |
| "Use shadcn/ui components" | Project | Team convention |
| "Never use `any` in TypeScript" | Project | Team standard |
| "Prices are in `src/lib/config`" | Project | Domain knowledge |
| "I use Ghostty terminal" | Local | Only you need it |

### Anti-patterns to cut [^src1]

- **Personality instructions** ("be a senior engineer", "think step by step") — wastes tokens; the harness already has strong system instructions.
- **`@-mentioning` docs** — `@docs/api-guide.md` embeds the whole file every session. Instead pitch when to read it: "For Stripe issues, see `docs/stripe-guide.md`."
- **Formatting rules a formatter already enforces** — use a hook, not a `CLAUDE.md` line. (But concrete style rules like "2-space indentation" are valid if you have *no* formatter.)
- **Duplicate rules** across global and project files.

### Advisory vs deterministic

`CLAUDE.md` is **advisory** — the model may or may not follow it. For guarantees (formatting, key-leak checks), use **hooks**, which the harness executes deterministically [^src1]. Auto-memory (`~/.claude/projects/<project>/memory/`) also loads at session start; don't hand-write things the agent learns on its own [^src1].

## The self-improvement loop

The single most impactful habit: after every correction, end with *"Update CLAUDE.md so you don't make that mistake again"* — the file becomes a living document that gets smarter each session [^src1]. Cursor has a direct analog: `/Generate Cursor Rules` turns a productive chat into a reusable `.mdc` rule [^src2].

## Cursor rules (`.cursor/rules/*.mdc`)

Cursor stores conventions as `.mdc` files in `.cursor/rules/`, with four activation types [^src2]:

| Rule type | When applied | Best for |
|---|---|---|
| **Always** | Every interaction | Core project patterns, meta-rules |
| **Auto Attached** | File-pattern (glob) match | File-specific rules (e.g. all `.ts` files) |
| **Agent Requested** | When the AI judges it relevant (needs a good description) | Workflows, processes |
| **Manual** | Invoked explicitly with `@rule-name.mdc` | Specialized one-off helpers |

Atlan's engineers recommend every AI-native project cover four rule kinds: **Project** (what the project is, structure), **Tech Stack** (how the team writes code), **Micro Workflow** (team habits — logging, feature flags, migrations), and **Meta Rules** (how to prioritize/resolve conflicts between rules) [^src2].

**Writing philosophy** [^src2]:
- **Be assertive, not suggestive** — "Always define TypeScript interfaces for component props", not "Consider using interfaces". LLMs don't handle nuance; vague rules get ignored.
- **Place important context last** — LLMs prioritize the end of a rule file; order as *what → how → why*.
- **Extract reusable patterns** with `@include ../shared/setup.md` to stay DRY.
- **~1 concept per rule, under 50–80 lines.** Review monthly — "rules are code".

Note the convergent benchmark: both Claude Code and Cursor land on **~80 lines / one concept** as the ceiling before instructions get dropped [^src1][^src2].

## The Karpathy-derived CLAUDE.md

A widely-shared single `CLAUDE.md` (43,000+ installs in its first week, per one video breakdwon) distills Andrej Karpathy's observations on LLM coding pitfalls — that models "make wrong assumptions… and just run along with them without checking" and "like to overcomplicate code… implement a bloated construction over 1000 lines when 100 would do" [^src4][^src7]. Four principles address these [^src4]:

| Principle | Addresses |
|---|---|
| **Think Before Coding** | State assumptions, present interpretations, push back, stop when confused |
| **Simplicity First** | No speculative features/abstractions; "if 200 lines could be 50, rewrite it" |
| **Surgical Changes** | Touch only what the request requires; don't refactor or delete pre-existing dead code |
| **Goal-Driven Execution** | Transform "fix the bug" into "write a failing test, then make it pass" |

The fourth captures Karpathy's "give it success criteria and watch it go" — strong, verifiable criteria let the model loop independently (see [[ai-engineering/agent-testing|Agent Testing]]) [^src4]. It ships both as a Claude Code plugin and as a `CLAUDE.md`, plus a committed `.cursor/rules/karpathy-guidelines.mdc` so the same rules apply in Cursor — an early example of cross-platform convention sharing [^src4].

**Observed behavioral differences with vs without the Karpathy CLAUDE.md** [^src7]:

- *Think Before Coding*: without the skill, Claude assumes and builds; with it, Claude asks clarifying questions before starting, producing more accurate first-pass implementations.
- *Simplicity First*: vanilla Claude adds 50+ lines for a filter feature; Karpathy-Claude adds 20 lines with deliberate decisions against unnecessary complexity.
- *Surgical Changes*: vanilla Claude often fails to persist changes (code "doesn't have the right update mechanism"); Karpathy-Claude touches only what was asked, leaving unrelated code untouched.
- *Goal-Driven Execution*: rather than imperative step-by-step commands, declare the goal (e.g. "user should be able to select an icon for each agent") and Claude self-directs — the declarative vs imperative shift Karpathy describes.

The core insight: changing from **imperative** (commanding agents how to do things) to **declarative** (declaring the desired outcome) consistently extracts better results from agentic workflows [^src7].

## Cross-platform conventions

The newer frontier is keeping one set of conventions working across **Claude Code, Codex, Cursor, Copilot, and Antigravity** [^src3]. The pattern: a central, version-controlled monorepo of agent skills that each tool picks up automatically, so changes "stay in sync everywhere" without per-tool reconfiguration [^src3]. See [[ai-engineering/agent-skills|Agent Skills]] for the skill mechanic this builds on.

**Cursor plugins** formalize this on Cursor's side: each plugin is a directory with a `.cursor-plugin/plugin.json` manifest and may contain `skills/` (`SKILL.md` with frontmatter), `rules/` (`.mdc` files), and `mcp.json` — bundling skills, rules, and MCP servers into one installable, marketplace-distributable unit [^src5]. Notable official plugins include `continual-learning` (incremental transcript-driven `AGENTS.md` memory updates), `cli-for-agent` (patterns for CLIs agents can run reliably), and `orchestrate` (fan tasks across parallel cloud agents) [^src5].

## Cross-platform plugins at scale: the Compound Engineering model

The Compound Engineering plugin (EveryInc) demonstrates the mature form of cross-platform convention sharing: a single plugin that installs across Claude Code, Cursor, Codex, GitHub Copilot, Factory Droid, Qwen Code, OpenCode, Pi, Gemini CLI, and Kiro via one marketplace command [^src6]. The mechanics reveal the portability model [^src6]:

- **Claude Code / Cursor / Copilot CLI** — native plugin install: `claude /plugin marketplace add EveryInc/compound-engineering-plugin`, then `/plugin install compound-engineering`. Claude Code-compatible plugin manifests are reused directly by Copilot and Droid with format translation.
- **Codex** — requires an additional `bunx @every-env/compound-plugin install compound-engineering --to codex` step because Codex's native plugin spec does not yet install custom agents (only skills); the Bun step fills the gap.
- **Converter-backed targets** (OpenCode, Pi, Gemini, Kiro) — a TypeScript installer (`bunx @every-env/compound-plugin install ... --to <target>`) converts the Claude Code-compatible plugin format during install.

The plugin ships 37 skills and 51 agents. The core convention it distributes is the compound engineering loop (brainstorm → plan → work → review → compound), implemented as slash commands with accompanying review and research agents. Each `/ce-compound` run saves a learning to `docs/` with YAML frontmatter; `/ce-plan` searches that directory on every run — conventions compound across sessions [^src6].

This illustrates the current state of cross-platform portability: the base layer (Claude Code's plugin manifest + `SKILL.md` format) is the lingua franca, but different harnesses require adapter steps as their native plugin specs evolve [^src6]. See [[ai-engineering/agentic-coding|Agentic Coding]] for the full Compound Engineering methodology.

## Related

- [[ai-engineering/agent-skills|Agent Skills]] — progressive disclosure; skills vs always-on instruction files
- [[ai-engineering/context-window-management|Context Window Management]] — the attention-budget constraint
- [[ai-engineering/agent-testing|Agent Testing]] — the verification loop Goal-Driven Execution depends on
- [[ai-engineering/ai-agent|AI Agent]] — instruction files configure the agent's harness

---

[^src1]: [abhishekray07/claude-md-templates — CLAUDE.md best practices](../../raw/web/github-abhishekray07-claude-md-templates-claude-md-best-prac.md)
[^src2]: [Cursor Rules in Action: How Our Engineers Use It at Atlan](../../raw/web/cursor-rules-in-action-how-our-engineers-use-it-at-atlan.md)
[^src3]: [Cross-Platform Agent Skills Guide: Claude Code, Codex, Cursor & Copilot](../../raw/email/email-2026-04-17-cross-platform-agent-skills-guide-claude-code-codex-cursor-c.md)
[^src4]: [multica-ai/andrej-karpathy-skills — A single CLAUDE.md file](../../raw/web/github-multica-ai-andrej-karpathy-skills-a-single-claude-md.md)
[^src5]: [cursor/plugins — Cursor Plugin Specification and Official Plugins](../../raw/web/github-cursor-plugins-cursor-plugin-specification-and-offici.md)
[^src6]: [EveryInc/compound-engineering-plugin — Official Compound Engineering plugin](../../raw/notes/notes-clippings-everyinccompound-engineering-plugin-official-compound-engine.md) — EveryInc, GitHub
[^src7]: [The Karpathy CLAUDE.md File That 43,000 Developers Installed](../../raw/youtube/d8BGxfW3Vj4-the-karpathy-claude-md-file-that-43-000-developers-installed.md) — Jay E, YouTube
[^src8]: [Claude Code + Karpathy's Obsidian = New Meta](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-claude-code-karpa-report.md) — YouTube (notes report)
