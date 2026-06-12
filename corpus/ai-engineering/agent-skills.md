---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
  - path: raw/web/what-s-the-real-deal-about-skills-this-is-not-a-mcp-is-dead.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-zazencodes-agent-skills-a-central-version-controlled.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-zazencodes-agent-skills-a-central-version-controlled-dac91b4a.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-luongnv89-asm-the-universal-skill-manager-for-ai-codi.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - agent skills
  - Claude skills
  - skills
  - progressive disclosure
  - skill.md
  - recursive skill building
  - skill manager
  - SKILL.md
  - skills-as-SDLC
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-09
updated: 2026-06-12
---

# Agent Skills

**TL;DR**: A *skill* is a modular capability file (`skill.md`) with a name, a description, and a body of instructions. Its key property is **progressive disclosure**: only the name and description sit in the context window; the full body loads on-demand when the agent decides the skill is relevant. This makes skills far cheaper than `AGENTS.md`/`CLAUDE.md` files, which are re-injected into context on every turn [^src1].

## Progressive disclosure — the core mechanic

A skill file has three parts: name, description, and body ("a bunch of info") [^src1]. When the file exists, only the name + description enter the context window. When the agent recognizes — from the description — that it needs the skill, it then reads the rest [^src1].

Concrete token contrast from the source: one 116-line "code structure" skill measured **944 tokens**. As an `AGENTS.md` file that 944 tokens is added *every single turn*; as a skill, only the name + description load up front — **53 tokens** — until the skill is actually invoked [^src1] [3:39](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=3:39>).

## Skills vs AGENTS.md / CLAUDE.md

The source argues most always-on context files are unnecessary: **"95% of people don't need this"** [^src1]. The reasoning:

- Models are already good and the **codebase itself is context** — telling the agent "this code base uses React" is redundant because it can read the code [^src1].
- An `AGENTS.md`/`CLAUDE.md` file is re-added to context on *every* turn, spending its full token cost repeatedly (e.g. a 1,000-line file ≈ 7,000 tokens per run) [^src1].
- The legitimate ~5% case: **proprietary information or a personal methodology** that genuinely must be referenced on every turn [^src1].

> Note: this is one practitioner's opinionated stance (Ras Mic). It concerns *what to put in always-on context*, not a claim that project-level instruction files have no use. Contrast with [[ai-engineering/context-engineering|Context Engineering]] sources that treat CLAUDE.md as valuable long-term memory.

## Recursively building skills (the recommended method)

The anti-pattern: identify a workflow, then immediately hand-write the skill. The source calls this "the worst thing you can do" because the skill captures no experience of a *successful run* [^src1].

The recommended loop [^src1] [9:34](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=9:34>):

1. **Identify the workflow.**
2. **Walk the agent through it step-by-step** — like mentoring a new employee; let it act, correct it, build a successful run *in context*.
3. **After a successful run, tell the agent to review what it did and write the skill** — now it has the context of what success looks like.
4. **It will still fail at gaps.** When it does, ask it *why it failed* (it reports the error descriptively), pass the failure back, have it fix the cause.
5. **After the fix works, tell it: "update the skill so this doesn't happen again."**
6. **Repeat.** The source's eight-source report generator took ~5 iterations of this loop to become reliable.

Mental model behind the method: LLMs **don't think — they predict tokens**, mapping input onto a vector space and returning the closest resemblance [^src1]. So an agent "will mimic you perfectly, but you've given it nothing to mimic" unless you supply a worked example. Treat agents like new employees, not magic boxes. See [[ai-engineering/ai-agent|AI Agent]].

## Don't download other people's skills

Two reasons [^src1] [12:34](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=12:34>):

- **Security**: a downloaded skill is an easy attack vector.
- **Context**: a third-party skill lacks *your* successful-run context — the thing that makes a skill work. Reviewing others' skills to learn from them is fine; installing them wholesale is not.

## Relationship to context efficiency

Skills are fundamentally a [[ai-engineering/context-window-management|context window management]] technique: progressive disclosure keeps the window lean, and a leaner window is both cheaper and more performant (the model degrades as the window fills). See [[ai-engineering/context-window-management|Context Window Management]] and [[ai-engineering/context-engineering|Context Engineering]].

## Skills as the cure for context rot

A second source frames skills primarily as the remedy for **context rot** — the failure mode where, after "70 tools, 5 MCP connections... RAG capabilities for 5K documents and 7 pages system prompts," the agent "starts not giving a f*** about the instructions" [^src2]. Skills fix this because they are "reusable prompts that Agents can load ON DEMAND" rather than at startup [^src2]. The reframing of system-prompt architecture: **"Your system prompt now becomes the identity and sitemap of what your Agents can do, and SKILLs are guidance to execute certain actions"** [^src2].

The most-emphasized point in this source: skills don't just store reusable prompts — **they tell the agent *how* and *when* to use its tools**. "You can configure a tool and specify what the tool does, but a skill can tell the agent how and when to use" it [^src2]. This makes skills complementary to, not a replacement for, [[ai-engineering/mcp|MCP]] and [[ai-engineering/rag|RAG]]: combine them to keep the system prompt lean while giving the agent deep capabilities on demand [^src2]. The named hard part is the same as in the YouTube source — writing the *description* well enough that the agent invokes the skill in the right situation [^src2].

## Anatomy and the anti-rationalization (description) problem

Across sources the file shape is consistent: a directory whose name matches the skill, containing `SKILL.md` with YAML frontmatter (`name`, `description`, optionally `version`, `license`, `allowed-tools`, `effort`) followed by markdown instructions; optional `references/` (extra markdown) and `scripts/` (executable code in any language) sit alongside [^src2] [^src4]. The load order is the disclosure mechanism: only the frontmatter `description` enters context first; the body and helper files load when the skill fires [^src2].

The recurring failure mode is **rationalizing a bad description** — a skill that is well-written but never gets picked up (or fires at the wrong time) because its description doesn't clearly state *when* to use it. "Failing to explain that properly will take all the advantages from these assets" [^src2]. This is the skills-side analogue of the SDLC discipline below: the description is the contract.

## Skills-as-SDLC and skill managers

As teams accumulate skills across multiple agents, skill management becomes its own software-development-lifecycle problem (create → develop → audit → test → publish), and tooling has emerged to handle it.

**Central version control (zazencodes/agent-skills)**: keep all skills for different tools in one Git repo and symlink them into each agent's skill folder, so "either way, you're changing the same files" [^src3]. The canonical folder is `agents/` (→ `~/.agents/skills`), with `claude/` as a required mirror (→ `~/.claude/skills`) "because Claude Code doesn't read `~/.agents/skills`"; other agents (codex, copilot, cursor, gemini) are opt-in [^src3]. A `setup_symlinks.py` script backs up existing system skills, copies them into the repo, and replaces each system directory with a symlink back [^src3].

**Universal skill manager (luongnv89/asm)**: a TUI+CLI to "install, search, audit, and organize all your agent skills — everywhere," across 19 providers (Claude Code, Codex, OpenClaw, Cursor, Windsurf, Cline, Gemini CLI, Antigravity, etc.) [^src4]. It addresses skills "scattered everywhere... installed three times" with no visibility and risky manual installs [^src4]. The full lifecycle: `asm init` (scaffold), `asm link` (symlink for live-editing iteration), `asm audit security` / `asm eval` (score), `asm install github:user/repo`, and `asm publish` (security audit → signed manifest → PR to the registry) [^src4].

**Security and verification are first-class.** Both managers treat installing third-party skills as an attack surface (consistent with the YouTube source's "don't download other people's skills" security point). asm's scanner flags shell execution, network access, credential exposure, and obfuscation *before* install [^src4]. Its automated **verification** requires four criteria for a verified badge: valid frontmatter (`name`+`description`), ≥20 characters of body instruction, no malicious patterns (`atob()`, suspicious base64, hex escapes, hardcoded `API_KEY`/`SECRET_KEY`/`PASSWORD`), and proper directory structure [^src4]. The ecosystem is large: asm's catalog indexes 2,800+ skills, including Anthropic's official skills (95,957★), superpowers (89,816★), and everything-claude-code (81,392★) [^src4]. (everything-claude-code is the harness system covered in [[ai-engineering/agent-harness|Agent Harness]].)

**Where to find/learn skills**: the official Anthropic marketplace via `/plugin marketplace add anthropics/skills` (pre-installed in claude.ai), plus `skill-creator` — "a skill... that creates skills" following Anthropic's formatting/packaging best practices [^src2]. The recommended single learning resource is Anthropic's "Agent Skills" Deep Learning course [^src2].

## See also

- [[ai-engineering/context-window-management|Context Window Management]] — why a lean window matters; sub-agents
- [[ai-engineering/context-engineering|Context Engineering]] — "less is more"; supply unique workflow, not general knowledge
- [[ai-engineering/ai-agent|AI Agent]] — token-predictor mental model; agents as new employees
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — scaling from one agent to sub-agents *for productivity*
- [[ai-engineering/agent-harness|Agent Harness]] — skills as a harness context technique; everything-claude-code
- [[ai-engineering/agentic-coding|Agentic Coding]] — skills as "the unit of reusable expertise"
- [[ai-engineering/mcp|MCP]] — skills tell the agent *how/when* to use MCP tools
- [[ai-engineering/rag|RAG]] — combine skills with RAG/MCP on demand
- [[ai-engineering/sources/how-ai-agents-and-skills-work|Source: How AI agents & Claude skills work]]
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src2]: [What's the real deal about SKILLs (This is not a 'MCP is dead' post)](../../raw/web/what-s-the-real-deal-about-skills-this-is-not-a-mcp-is-dead.md) — Alejandro Aboy, The Pipe and the Line
[^src3]: [agent-skills: a central, version-controlled home for coding agent skills](../../raw/web/github-zazencodes-agent-skills-a-central-version-controlled.md) — zazencodes/agent-skills, GitHub
[^src4]: [agent-skill-manager (asm): the universal skill manager for AI coding agents](../../raw/web/github-luongnv89-asm-the-universal-skill-manager-for-ai-codi.md) — luongnv89/asm, GitHub
