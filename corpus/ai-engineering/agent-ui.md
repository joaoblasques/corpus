---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/github-hachej-boring-ui-build-agent-powered-apps-without-rei.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/notion-where-teams-and-agents-work-together.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - agent UI
  - agent-centric apps
  - agent-powered apps
  - chat and workbench
  - Boring UI
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# Agent UI

**TL;DR**: When software can understand intent and act, the traditional SaaS surface (buttons, forms, pages, dashboards) collapses to two surfaces: **Chat** — tell the agent what to do — and **Workbench** — inspect, steer, and refine the results [^src1]. An "agent UI" is the shell that exposes both and lets the agent control the workbench directly. Boring UI is a reference implementation of this pattern.

## The collapse to chat + workbench

Traditional SaaS is built around workflows users drive by hand. Agents change that: "every app collapses to two surfaces" — a chat to issue intent and a workbench to inspect and refine [^src1]. The Boring UI core provides "a workbench the agent can control and reshape" [^src1].

The load-bearing design axiom: **the agent and the user interact with the same core primitives through the same interfaces** [^src1]. There is a single file API shared by the frontend file tree and the agent's filesystem tools; the agent "sees the workspace the same way the user does" and acts on it through dedicated UI tools [^src1]. This is the agent-native-parity principle made concrete — any surface the user sees, the agent can drive.

## Architecture

Boring UI is built on the Pi agent harness (see [[ai-engineering/ai-agent|AI Agent]]) and organizes around four components [^src1]:

| Component | Role |
|---|---|
| Web Frontend | Chat + workspace UI (React + Vite) |
| Web Backend | API layer shared by frontend and agent tools (Node.js) |
| Pi Harness | Agent runtime (the `AgentHarness` loop) |
| Sandbox | Isolated filesystem + execution runtime |

The **UiBridge** links frontend and backend: the agent or server posts commands (`openFile`, `openPanel`, `openSurface`) and the workbench dispatches them — "how the agent drives the UI without touching the DOM" [^src1]. The agent loop "knows nothing about files, shells, or UI — only `AgentTool[]`"; **Workspace** and **Sandbox** abstractions decide where those tools actually run [^src1]:

- **Workspace** — filesystem abstraction (`readFile`, `writeFile`, `readdir`, `watch`) with `NodeWorkspace` (local `node:fs`) and `VercelSandboxWorkspace` (remote over HTTP) adapters.
- **Sandbox** — shell-execution abstraction with `direct` (no isolation), `bwrap` (Linux bubblewrap isolation), and `vercel-sandbox` (Firecracker VM) adapters.

Sandbox and Workspace are always created as a pair so they share one filesystem [^src1]. `AgentHarness` is an interface, not a hardcoded dependency — "the design leaves room for swapping in a different harness later" [^src1].

## Plugins: extending the shell

The reuse mechanism is a plugin system that *extends Pi's* rather than inventing a new one — "any Pi plugin works out of the box inside Boring UI" [^src1]. A plugin is a Node package with two manifest blocks [^src1]:

- `pi.*` — agent side: `extensions`, `skills`, `prompts`, `systemPrompt` (hot-reloadable via `/reload`).
- `boring.*` — UI side: `front` (panels, command-palette actions, catalogs, surface resolvers) and `server` (boot-time agent tools + HTTP routes).

What a plugin can add: **panels** (arbitrary React panes — editors, charts, tables), **left tabs** (persistent sidebars), **commands** (palette entries triggered by user *or* agent), **catalogs** (faceted data explorers the agent can surface), **agent tools** (schema-defined model capabilities), and **skills + prompts** [^src1]. See [[ai-engineering/agent-skills|Agent Skills]].

## Example: a whole app as one plugin

`boring-macro` / **MacroAnalyst** is a macroeconomic-research agent implemented as a single Boring UI plugin: it fetches live time series from a database of 800,000+ series, writes and runs Python transforms it chooses, and renders interactive chart decks in the workbench — "from data access, to analysis, to visualization, to presentation generation… all orchestrated through one agent-centric interface" [^src1]. This illustrates the pattern's reach: data exploration, ad-hoc transformation, and slide generation behind one chat + workbench shell.

## Deployment

The full app ships two targets sharing the same `createCoreApp` factory: **Fly.io** (Docker container + Postgres) and **Vercel** (serverless function for agent routes + edge static assets) [^src1]. It also "runs fully locally: no auth, no database… just a stateless agent + workspace running directly on your machine" [^src1].

## Teams and agents working together

The broader direction is collaborative surfaces where teams and agents share one workspace — Notion positions itself as a place "where teams and agents work together" [^src2]. (Source content was JavaScript-gated and not extractable beyond this framing.) The convergent signal across Boring UI and such products is the same: agents become first-class participants in the same workspace humans use, not a separate chat bolted on.

## Related

- [[ai-engineering/ai-agent|AI Agent]] — Pi is the harness Boring UI builds on; agent-mode and serverless deployment
- [[ai-engineering/agent-skills|Agent Skills]] — the skill/plugin layer that customizes the shell
- [[ai-engineering/mcp|MCP]] — tool/coordination layer the harness can integrate

---

[^src1]: [hachej/boring-ui — build agent-powered apps without reinventing the shell](../../raw/web/github-hachej-boring-ui-build-agent-powered-apps-without-rei.md)
[^src2]: [Notion — where teams and agents work together](../../raw/web/notion-where-teams-and-agents-work-together.md)
