---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/youtube-BZ0w0JhPQ9o-pi-coding-agent-free-course.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/_inbox/youtube-2HtqFVLgjLI-how-software-engineers-actually-use-coding-agents-in-2026.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Pi agent
  - pi-agent
  - Pi coding agent
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Pi Agent

**TL;DR.** Pi is an open-source, minimal AI coding agent designed around "just enough harness" — four tools, a system prompt under 1,000 tokens, no permission prompts by default, and TypeScript extensibility. It targets senior developers who want a coding agent they can fully understand, customize, and run against any model via OpenRouter or Ollama [^src1].

## Core philosophy: minimal harness

Pi's design bet is the inverse of Claude Code's feature-richness: "you should be able to read the entire codebase in an afternoon" [^src1]. The harness is intentionally small because a small harness is auditable, forkable, and less likely to fight the developer.

**The four built-in tools** [^src1]:
- `read` — read a file or directory listing
- `bash` — run shell commands
- `edit` — make file edits (patch format)
- `write` — write a new file

That's the entire tool surface. No web search, no memory, no browser — everything else is composed from these primitives via skills or extensions.

**System prompt size**: under 1,000 tokens (compared to Claude Code's ~20,000+). The tradeoff: Pi starts faster and uses less context per turn; it also lacks Claude Code's built-in discipline around complex patterns [^src1].

## Session forking (branching)

Pi's distinctive harness feature is **session forking** — creating a copy of a conversation at any point to explore an alternative approach without losing the main thread [^src1].

Use cases [^src1]:
- Try two different implementations of a feature in parallel
- Explore a "riskier" approach without committing to it
- Create a clean-room review session that starts from the same context but has no memory of how the code was written

Forking is built into the core Pi CLI; no plugin required. The parent session and the fork share the same initial context but diverge from the branch point forward.

## Extensions (TypeScript)

Pi extensions are TypeScript files that add new tools, modify the system prompt, or hook into session lifecycle events [^src1]. Extension points:

| Extension type | What it does |
|---|---|
| New tool | Adds a callable function to Pi's tool surface (e.g. a browser tool, a test runner, a database query) |
| System prompt augmentation | Injects domain-specific context (project conventions, coding style) at session start |
| Session lifecycle hooks | Runs code on session start, after each turn, or on session end (memory persistence, logging) |

Extensions are installed as files in `.pi/extensions/` and are loaded automatically at session start. A single-file extension is common (200–300 lines for a substantial tool).

## Skills

Pi skills follow the same SKILL.md format as Claude Code skills — a directory with a `SKILL.md` frontmatter + body [^src1]. Invoked with a slash command: `/my-skill`.

The key difference from Claude Code: Pi has no built-in skills. Every skill must be written or imported. This forces intentionality — you install only what you use, and you understand what you're installing. See [[ai-engineering/agent-skills|Agent Skills]] for the general discipline.

## System prompt customization

Pi's system prompt is fully replaceable (not just appendable) [^src1]. Workflow:

1. Copy the default system prompt from the Pi repository
2. Modify to match your project or team conventions
3. Set `PI_SYSTEM_PROMPT` env var or pass via `--system-prompt` flag

This makes Pi suitable for creating **specialized agents**: replace the default system prompt with a domain-specific one (security auditor, database engineer, API designer) and Pi becomes that specialist. See the "Specialist agent profiles" pattern in [[ai-engineering/agent-skills|Agent Skills]].

## Model support

Pi supports any model accessible via:
- **OpenRouter** — routes to any frontier model (Claude, GPT-4o, Gemini, Llama)
- **Ollama** — local models; Pi runs fully offline with the right model pulled
- **Direct API** — Claude API, OpenAI API, etc.

**No native Anthropic subscription support**: Pi requires an API key (usage-based billing), not a Claude.ai subscription [^src1]. This makes Pi cost-transparent (you see every token used) but requires API access rather than a flat-rate subscription.

## Comparison with Claude Code

From a practitioner walkthrough [^src1][^src2]:

| Dimension | Pi | Claude Code |
|---|---|---|
| **Tool surface** | 4 tools | ~20 built-in tools |
| **System prompt** | <1,000 tokens | ~20,000+ tokens |
| **Permission prompts** | None by default | Prompts on each write/bash |
| **Extensibility** | TypeScript files | Skills, hooks, plugins, MCP |
| **Session branching** | Built-in | `/branch` flag (2026 addition) |
| **Model support** | Any (OpenRouter/Ollama/API) | Claude API / claude.ai subscription |
| **Learning curve** | Low (read the whole codebase) | High (many concepts) |
| **Target audience** | Senior devs who want control | Teams wanting full features |
| **Open source** | Yes | No |

Pi's appeal to senior developers (confirmed by 2026 survey data [^src2]) is the **understanding + control** combination: you know exactly what the agent has access to, what it will do, and you can modify any part of it. Claude Code's appeal is the **feature depth + polish** combination: everything is already built, battle-tested, and maintained.

## Adoption profile

From the 2026 coding agent survey [^src2]:
- Gaining traction specifically with **senior developers** — more than with junior devs or non-technical practitioners
- Often used as a **secondary agent** alongside Claude Code: Pi for tasks requiring deep customization or offline operation; Claude Code for polished interactive work
- The minimal harness philosophy has influenced other tools; Claude Code's `--bare` flag (skip all auto-loading, ~10× faster startup) is a response to the same "I want to control what's loaded" demand

## See also

- [[ai-engineering/agent-skills|Agent Skills]] — Pi skill format is compatible with the SKILL.md open standard
- [[ai-engineering/agentic-coding|Agentic Coding]] — survey data on Pi adoption and comparison context
- [[ai-engineering/claude-code|Claude Code]] — the primary alternative; comparison table above
- [[ai-engineering/agent-harness|Agent Harness]] — minimal vs. maximal harness philosophy
- [[ai-engineering/gemini-cli|Gemini CLI]] — another open-source coding agent alternative
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Pi Coding Agent — Free Course](../../raw/_inbox/youtube-BZ0w0JhPQ9o-pi-coding-agent-free-course.md) — YouTube
[^src2]: [How Software Engineers Actually Use Coding Agents in 2026](../../raw/_inbox/youtube-2HtqFVLgjLI-how-software-engineers-actually-use-coding-agents-in-2026.md) — YouTube
