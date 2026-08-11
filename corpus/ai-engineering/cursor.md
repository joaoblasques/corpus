---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Cursor
  - Cursor IDE
  - Cursor agent
  - Composer
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-26
updated: 2026-07-13
---

# Cursor

**TL;DR** — Cursor is an AI code editor (a VS Code fork) whose draw is not the models — it runs the same frontier models as everyone else — but the **coding harness the Cursor team builds around them**. One practitioner's stated reason for choosing it over Claude Code or Codex: "while it's using the same models, it has a coding harness… that I just find works a lot better" [^src1]. The harness-over-model thesis is echoed independently: a separate creator frames the model-vs-harness distinction as central to agentic engineering, arguing a good harness maximizes a model's output, and draws on hands-on use of Cursor and Claude Code to make the point [^ships-100x]. It is the recurring counterpoint to [Claude Code](/ai-engineering/claude-code.md) in the [agentic coding](/ai-engineering/agentic-coding.md) tool landscape, and was cited as a breakout commercial success ($100M in its first year, ~$2B valuation) in [AI Business Models](/ai-business/ai-business-models.md). In tool round-ups it is regularly listed first among GitHub Copilot alternatives, compared alongside Builder.io, Claude Code, Codex, Windsurf, and Zed on features, pricing, and best-fit use case [^copilot-alts].

## Harness, not model

Cursor exposes a per-agent **model selector** with the frontier Claude/GPT models plus its own **Composer** model. Observed settings in a real build [^src1]:
- pick the model (e.g. Opus 4.8; Fable 5 when available)
- **fast mode** toggle, **thinking mode**, and the **1M-context** window
- a reasoning-**effort** dial — "medium… is kind of the sweet spot"; higher (high / extra-high) is slower

Model-by-task practice: a frontier Claude model for building from scratch, switching to "GPT 5.5" for large refactors or repeated mistakes, and a faster model (Composer 2.5) for UI-only changes [^src1]. Running agents in Cursor "is not going to be absolutely free" — it bills usage [^src1].

## Workflow surfaces

- **Views**: a default chat-only "agents" view vs a file-visible view; the practitioner prefers seeing the code being written rather than just chatting [^src1].
- **Rules** — Cursor generates rule files in a `rules/` folder that are always injected into the prompt (e.g. "always commit after any major change"), the Cursor analogue of [CLAUDE.md conventions](/ai-engineering/claude-md-conventions.md) [^src1]. Rules can be auto-created by the agent itself from a natural-language instruction, combined with the GitHub MCP server to auto-push commits [^src1].
- **Agent skills + MCP servers** — install a tool's skills with one terminal command and they appear in Cursor; MCP servers are added to `.cursor/mcp` (GitHub MCP, ImageKit MCP shown), then connected/authenticated via the command palette (`Cmd/Ctrl+Shift+P` → "MCP: Open MCP Settings") [^src1]. Installing a vendor's skills + MCP server means the agent learns the tool without the user pasting docs.
- **Multi-agent / multitask mode** — spins up multiple sub-agents in parallel; "sometimes it just goes crazy… makes it a little bit unmaintainable" but becomes viable when the project has been pre-structured with planning docs and rules [^src1].
- **Dictation** — Whisper Flow voice-to-text works natively, including file tagging, to speed up long planning prompts [^src1].
- **Screenshot / image attachment** — attach a photo of the UI directly in the chat; the practitioner uses this to highlight specific bugs on-screen so the model knows exactly what's broken [^src1].

## Context-file strategy

Before writing any code, the practitioner creates markdown planning and architecture files inside the project via an initial Cursor prompt (telling Cursor what to build, which tools, asking it to produce a plan and ask clarifying questions). These files serve as persistent context across multiple agent chats and enable parallel sub-agents to stay aligned on the same decisions without the user re-explaining them [^src1].

The pattern: (1) initial planning prompt → Cursor generates architecture + asks questions; (2) practitioner answers; (3) context markdown files are committed to the repo; (4) all subsequent prompts — including in multi-agent mode — reference those files automatically [^src1].

Cursor is also cited as a target editor for spec-driven frameworks: the **BMAD method** is a spec-driven development framework structured in two phases — planning and context-engineered development — whose emphasis on context engineering applies across tools including Gemini, Claude Code, and Cursor [^bmad].

Beyond a single tool, one developer's practice is to run **multiple AI coding tools in parallel** — Cursor alongside terminal-based AI and ChatGPT — with the reported payoff being long-term context accumulation across the tools rather than depending on any one [^ai-tools].

## Debugging posture

The practitioner reads the model's tool calls and reasoning in real time to catch wrong directions early and interject before the agent goes too far down an incorrect path [^src1]. When a bug appears: copy the error message, add minimal extra context (e.g., "the upload succeeded but transcription is failing"), and send it — "this is all I do when it fails" [^src1]. Screenshots of the broken UI are attached directly in the chat to localize the problem without lengthy description [^src1].

## Ecosystem tooling

Cursor's session transcripts are a supported input format for third-party tooling. **Claude Replay** is an open-source npm tool that converts AI coding-agent transcripts into self-contained, interactive HTML replay files with zero external dependencies; it supports multiple agent formats — Claude Code, Cursor, and Codex CLI — and offers interactive playback controls plus secret redaction, making it a way to showcase AI-assisted Cursor sessions [^claude-replay].

## See also

- [Agentic Coding](/ai-engineering/agentic-coding.md) — the workflow discipline (research-first, context files, skills+MCP, iterative prompt-and-debug) Cursor is used inside; see the "real AI coding workflow" section
- [Claude Code](/ai-engineering/claude-code.md) — the CLI agent Cursor is most often compared against
- [MCP](/ai-engineering/mcp.md) — the connector layer Cursor adds via `.cursor/mcp`
- [Agent Skills](/ai-engineering/agent-skills.md) — the installable skills Cursor consumes
- [Vibe Coding](/ai-engineering/vibe-coding.md) · [Spec-Driven Development](/ai-engineering/spec-driven-development.md) — the plan-first posture the workflow depends on
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [My Real AI Coding Workflow (build anything) (Tech With Tim)](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md) — [03:59](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=239) Cursor + model selector setup; [05:45](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=345) why Cursor (harness over model); [10:25](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=625) installing skills + MCP servers; [14:13](../../raw/youtube/youtube-gpOfsGW1xRk-my-real-ai-coding-workflow-build-anything.md#t=853) rules

[^ships-100x]: [Why This Dev Ships 100x Faster Than 99% of Engineers (David Ondrej)](sources/why-this-dev-ships-100x-faster-than-99-of-engineers-PzVV4X37ihg.md) — harness-vs-model distinction in agentic engineering; hands-on with Cursor and Claude Code.

[^copilot-alts]: [6 Best GitHub Copilot Alternatives in 2026 (Builder.io)](sources/6-best-github-copilot-alternatives-in-2026-50fcd220.md) — Cursor compared alongside Builder.io, Claude Code, Codex, Windsurf, and Zed on features, pricing, and best use case.

[^bmad]: [AI Coding — BMAD Method Spec-Driven Development Workflow](sources/ai-coding-bmad-method-spec-driven-development-workflow-f.md) — two-phase (planning + context-engineered development) spec-driven framework spanning Gemini, Claude Code, and Cursor.

[^ai-tools]: [AI Tools — Best AI Coding Tools for Developers 2025](sources/ai-tools-best-ai-coding-tools-for-developers-2025-2025.md) — developer review favoring multiple tools (Cursor, terminal AI, ChatGPT) for long-term context accumulation.

[^claude-replay]: [Claude Replay — AI Coding Session to Interactive HTML Replay](sources/claude-replay-ai-coding-session-to-interactive-html-replay-doc.md) — open-source npm tool converting agent transcripts (Claude Code, Cursor, Codex CLI) into self-contained interactive HTML with playback controls and secret redaction.

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [AI's Impact on Data Engineering](/data-engineering/ai-impact-on-data-engineering.md) · _data-engineering_

<!-- RELATED:END -->
