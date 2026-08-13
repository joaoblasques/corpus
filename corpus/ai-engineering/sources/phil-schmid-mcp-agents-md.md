---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-how-to-correctly-use-mcp-servers-with-your-ai-agents-4bbb2c88.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-writing-a-good-agents-md-fad595b7.md
    channel: web
    ingested_at: 2026-08-13
aliases:
  - Phil Schmid MCP servers
  - Phil Schmid AGENTS.md
tags:
  - corpus/ai-engineering
  - source
  - mcp
  - agents-md
  - coding-agents
  - context-engineering
created: 2026-08-13
updated: 2026-08-13
---

# Phil Schmid: MCP Server Patterns and Writing Good AGENTS.md

TL;DR: Two posts by Philipp Schmid (HuggingFace) covering (1) how to use MCP servers without context bloat, and (2) how to write AGENTS.md files that actually help coding agents rather than hurting them — backed by ETH Zurich research.

## How to Correctly Use MCP Servers [^mcp]

MCP servers "are not dead. But blindly enabling them bloats your context, which leads to higher cost and worse performance." Unlike agent skills, MCP servers don't provide progressive disclosure by default — every tool is injected every time unless you apply a usage pattern.

**Two patterns:**

**1. Explicit (inline) MCP — opt-in, user-driven**
- Servers stay inactive until the user @mentions them in a prompt (e.g., `@github`, `@slack`).
- The agent: resolves the @mention → fetches tool schemas from the server → injects into `tools[]` of the API request → forwards to the model.
- Nothing loads unless requested; context surface stays small.
- *When to use*: MCP usage is occasional and user-driven — one-off data retrieval from Slack or GitHub.

**2. Subagent-scoped MCP — always-on, least-privilege**
- MCP servers declared in a subagent's config, automatically available at runtime alongside native tools (read_file, run_command, etc.).
- Use `allowed_tools` to scope to specific tools within a server without forking the server.
- *When to use*: the use case dictates the tools (e.g., a code review agent always needs GitHub; a support agent always needs Zendesk). The MCP servers are part of what the agent *is*, not something a user opts into per request.[^mcp]

## Writing a Good AGENTS.md [^agents]

Backed by "Evaluating AGENTS.md" (ETH Zurich, 2025) and HumanLayer experience.

**The data on AGENTS.md performance:**
- Auto-generated AGENTS.md files reduce task success rates by ~3% on average while increasing inference cost by over 20%.
- Human-written AGENTS.md files only marginally improve performance (~4%), and still increase cost by up to 19% due to extra steps.
- Stronger models don't generate better context files — GPT-5.2-generated files improved one benchmark 2% but degraded another by 3%.
- Codebase overviews in AGENTS.md don't help agents navigate faster (same step count with or without).
- BUT: instructions ARE followed — unnecessary requirements make tasks harder, increasing reasoning tokens by 14–22%.
- Tools mentioned in AGENTS.md get used 160× more often than unmentioned tools.

**What to include:**
- The WHAT: tech stack, project structure, what each part does (critical for monorepos).
- The WHY: project purpose and key component intent.
- The HOW: how to build, test, verify — especially non-obvious tooling (e.g., `uv` instead of `pip`, `bun` instead of `npm`).

**What NOT to include:**
- Detailed codebase overviews / directory listings — agents discover structure themselves.
- Code style guidelines — use linters; they're faster, cheaper, and deterministic.
- Task-specific instructions that only apply sometimes.
- Auto-generated content.

**Structure guidance:**
- Keep under 300 lines; HumanLayer keeps theirs under 60.
- Use progressive disclosure: keep task-specific docs in separate files and list them in AGENTS.md with brief descriptions.
- Prefer pointers over embedded code snippets (avoid stale copies).
- Write it yourself, deliberately — "a bad line in AGENTS.md cascades into bad plans, bad code, and bad results across every session."[^agents]

## Cross-links

- [/ai-engineering/README.md](/ai-engineering/README.md)
- [/ai-engineering/sources/agents-md-what-belongs-there-and-what-wastes-context-ce.md](/ai-engineering/sources/agents-md-what-belongs-there-and-what-wastes-context-ce.md) — related AGENTS.md guidance

---

[^mcp]: raw/_inbox/web-how-to-correctly-use-mcp-servers-with-your-ai-agents-4bbb2c88.md — philschmid.de/use-mcp-servers
[^agents]: raw/_inbox/web-writing-a-good-agents-md-fad595b7.md — philschmid.de/writing-good-agents
