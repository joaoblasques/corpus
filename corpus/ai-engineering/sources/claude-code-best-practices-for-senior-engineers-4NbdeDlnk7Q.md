---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-4NbdeDlnk7Q-claude-code-best-practices-for-senior-engineers.md
    channel: youtube
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - youtube-quick-intake
  - claude-code
  - prompt-engineering
  - context-management
created: 2026-07-02
updated: 2026-08-22
provisional: false
youtube_video_id: 4NbdeDlnk7Q
url: https://youtu.be/4NbdeDlnk7Q
channel_name: Shruti Kapoor
playlist: Corpus_queue
published: 2026-06-25
transcript_status: ok
---

# Claude Code Best Practices for Senior Engineers

> **Source** (YouTube · Shruti Kapoor · 2026-06-25). [watch on YouTube](https://youtu.be/4NbdeDlnk7Q) · [transcript](../../../raw/youtube/youtube-4NbdeDlnk7Q-claude-code-best-practices-for-senior-engineers.md)

**TL;DR:** Five concrete practices — plan mode first, CLAUDE.md for persistent context, skills/MCP for external best practices, context-management commands, and hooks for guaranteed enforcement — close the gap between naive one-shot prompting and production-quality AI-assisted engineering.

---

## Context: the naive-prompt failure mode

Without explicit best-practice context, Claude defaults to generic patterns learned from public repos. The transcript demonstrates this with a basic React component prompt: the output had duplicate items, no keyboard accessibility (arrow-key navigation broken), a monolithic file structure, `useEffect` for data fetching, and no component reusability.[^1]

The core problem: "Claude doesn't know what stack you prefer and what your best practices are."[^1]

---

## Best practice 1: Gather requirements and start in plan mode

Work like an engineer: gather requirements, define technical specs, design architecture, *then* implement.[^1] Concretely:

- Switch Claude Code to **plan mode** before writing any code.
- Use the **highest available model** for planning (Fable 5 used in the demo). The author runs plan mode in the browser to access a subscription tier with Fable 5, separate from the IDE session.[^1]
- Write a **structured prompt** specifying: tech stack (React + TypeScript), data-fetching library (TanStack Query), API to call, explicit UI requirements (grid layout, card fields), exclusion rules (no Shorts, no duplicates), and pagination strategy (infinite scroll via TanStack's infinite query + page token).[^1]

The plan output included: a data model (channel, video, video page, YouTube API error types), a query strategy keyed on channel handle, reusable/composable components (channel explorer, search bar, video feed, video grid, video card), and explicit dependency list.[^1] The second attempt used TanStack Query instead of `useEffect`, and produced modular components.[^1]

---

## Best practice 2: Provide context via CLAUDE.md

Claude does not retain context across sessions. `CLAUDE.md` is the mechanism to persist best practices so every session — and every team member — starts from a common baseline rather than a blank slate.[^1]

Immediately after planning (while context is fresh), ask Claude to generate a `CLAUDE.md` covering:[^1]

- Common bash commands for the project
- Tech stack choices (React, TypeScript, Next.js App Router)
- Code style rules (e.g. no default exports)
- Architectural decisions and their rationale (why TanStack Query over alternatives)
- Hard rules (no skipping accessibility, no committing secrets)

The file belongs in a `.claude/` directory. Once present, Claude loads it automatically, so it "already knows the coding formats … and the style guide."[^1]

This also enables **team sharing**: distributing `CLAUDE.md` gives all team members the same AI coding context without re-explaining the architecture each session.[^1]

---

## Best practice 3: Use skills and MCP for external context

`CLAUDE.md` covers project-specific practices; skills and MCP servers bring in *external* best practices and tooling.[^1]

**Skills** are community/vendor-authored practice files dropped into `.claude/skills/`. The Vercel React best practices repo is cited as a high-quality source.[^1] Install selectively (only the files you need) rather than the full `agent-skills` package to control token usage.[^1]

**MCP servers** highlighted:[^1]
- **CodeRabbit MCP** — code review, security vulnerability detection.
- **Figma MCP** — converts a Figma file into high-fidelity UI code without manual implementation. Works best once `CLAUDE.md` and skills are in place so Claude writes to the project's style guide while applying the design.[^1]
- **Knip (Follow skill)** — dead-code detection; addresses AI's known weakness of generating code without removing stale code.[^1]

---

## Best practice 4: Manage context deliberately

With large models like Fable, context fills quickly. Two commands and one architectural pattern:[^1]

- **`/compact`**: compresses conversation history while retaining what Claude was working on. Use when switching tasks within the same project. After compacting, token usage dropped from a full window to 27.8k/200k in the demo.[^1]
- **`/clear`**: wipes the session entirely. Use when starting a new feature where prior context is irrelevant. Skills and `CLAUDE.md` reload automatically, so this is not a full reset.[^1]
- **Sub-agents for side tasks**: spawn a sub-agent (e.g. to write tests) to keep the main thread unblocked. "Free up the main thread of Claude code so you can continue … by writing code and then spawn a new agent … that can do side tasks."[^1]

Note: loading many skills or many MCP tools consumes substantial tokens. `/context` shows the breakdown.[^1]

---

## Best practice 5: Use hooks for guaranteed enforcement

`CLAUDE.md` is followed roughly 80% of the time — it is advisory. For rules that must run on every file write, use **hooks** in `settings.local.json`.[^1]

Hooks are specified as `PostToolUse` (runs after every edit) or `PreToolUse` (runs before). Examples from the demo:[^1]

- Run **Prettier** on every file Claude writes (formatting).
- Run **TypeScript type-checking** on every file Claude edits.

Pre-tool hooks can enforce hard prohibitions (e.g. block `DROP TABLE`, prevent committing secrets).[^1]

---

## Bonus: test guardrails

"Make sure that you're putting up guardrails for Claude to test your code against as it is writing it."[^1] Concretely: spawn a sub-agent to write the test suite. This ensures new code is validated against existing functionality. The human should still author and review test suites — AI-only test authorship is flagged as insufficient.[^1]

---

## Summary of practices

| # | Practice | Mechanism |
|---|---|---|
| 1 | Plan before implementing | Plan mode + highest model + structured prompt |
| 2 | Persist team best practices | `.claude/CLAUDE.md` |
| 3 | Load external best practices + tooling | Skills (`.claude/skills/`) + MCP servers |
| 4 | Control context consumption | `/compact`, `/clear`, sub-agents |
| 5 | Enforce non-negotiable rules | Hooks in `settings.local.json` |

---

[^1]: Shruti Kapoor, "Claude Code Best Practices for Senior Engineers," YouTube, 2026-06-25. [https://youtu.be/4NbdeDlnk7Q](https://youtu.be/4NbdeDlnk7Q)
