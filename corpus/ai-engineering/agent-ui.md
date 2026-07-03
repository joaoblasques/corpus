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
  - path: raw/email/email-2026-05-28-launching-boring-ui.md
    channel: email
    ingested_at: 2026-06-16
  - path: raw/notes/notes-clippings-agent-view-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - agent UI
  - agent-centric apps
  - agent-powered apps
  - chat and workbench
  - Boring UI
  - Pi
  - Pi agent harness
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-17
---

# Agent UI

**TL;DR**: When software can understand intent and act, the traditional SaaS surface (buttons, forms, pages, dashboards) collapses to two surfaces: **Chat** — tell the agent what to do — and **Workbench** — inspect, steer, and refine the results [^src1]. An "agent UI" is the shell that exposes both and lets the agent control the workbench directly. Boring UI is a reference implementation of this pattern.

## The collapse to chat + workbench

Traditional SaaS is built around workflows users drive by hand. Agents change that: "every app collapses to two surfaces" — a chat to issue intent and a workbench to inspect and refine [^src1]. The Boring UI core provides "a workbench the agent can control and reshape" [^src1].

The load-bearing design axiom: **the agent and the user interact with the same core primitives through the same interfaces** [^src1]. There is a single file API shared by the frontend file tree and the agent's filesystem tools; the agent "sees the workspace the same way the user does" and acts on it through dedicated UI tools [^src1]. This is the agent-native-parity principle made concrete — any surface the user sees, the agent can drive.

## Why "boring": the design thesis

The framework's creator (Julien Hurault) frames the pattern as the natural endpoint once "AI can now understand user intent and act on it" — for the first time "interfaces can become truly minimal and 'boring'," reduced to "an agent chat on the left" and "a workspace on the right (~ mini IDE)" [^src3]. The name is the thesis: the UI gets boring precisely because the agent absorbs the complexity. He positions Boring UI as the concrete expression of an earlier "IDE for X" bet — "a simple (and boring) web-based mini IDE that lets anyone leverage the power of coding agents … without needing to interact with code directly" [^src3].

The stated long-term direction is a **skill-sharing platform** — "a place where domain experts can share skills, UI primitives, workflows, and packaged knowledge" [^src3] — and **self-buildable UI**: since the agent already has filesystem access, "there's no reason it shouldn't build its own plugins," letting users ship primitives and "the agent handles the last-mile customization" via hot-reloaded plugins [^src3]. This is the agent-native-parity axiom (below) pushed to its limit: the agent doesn't just drive the workbench, it *authors* it.

## Architecture

Boring UI is built on the **Pi** agent harness — an open-source, "super lightweight and built to be highly extensible" runtime by Mario Zechner — integrated via its Node.js SDK so the host can deeply customize Pi's tools and interfaces (e.g. overriding filesystem tools to target the Boring UI sandbox) [^src3]. Pi is **provider-agnostic**: it runs commercial APIs, open-source models, or self-hosted LLM infrastructure, so the shell is not locked to one model vendor [^src3]. See [Agent Harness](/ai-engineering/agent-harness.md). The system organizes around four components [^src1]:

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

What a plugin can add: **panels** (arbitrary React panes — editors, charts, tables), **left tabs** (persistent sidebars), **commands** (palette entries triggered by user *or* agent), **catalogs** (faceted data explorers the agent can surface), **agent tools** (schema-defined model capabilities), and **skills + prompts** [^src1]. See [Agent Skills](/ai-engineering/agent-skills.md).

## Example: a whole app as one plugin

`boring-macro` / **MacroAnalyst** is a macroeconomic-research agent implemented as a single Boring UI plugin: it fetches live time series from a database of 800,000+ series, writes and runs Python transforms it chooses, and renders interactive chart decks in the workbench — "from data access, to analysis, to visualization, to presentation generation… all orchestrated through one agent-centric interface" [^src1]. This illustrates the pattern's reach: data exploration, ad-hoc transformation, and slide generation behind one chat + workbench shell.

## Deployment

The full app ships two targets sharing the same `createCoreApp` factory: **Fly.io** (Docker container + Postgres) and **Vercel** (serverless function for agent routes + edge static assets) [^src1]. It also "runs fully locally: no auth, no database… just a stateless agent + workspace running directly on your machine" [^src1].

## Teams and agents working together

The broader direction is collaborative surfaces where teams and agents share one workspace — Notion positions itself as a place "where teams and agents work together" [^src2]. (Source content was JavaScript-gated and not extractable beyond this framing.) The convergent signal across Boring UI and such products is the same: agents become first-class participants in the same workspace humans use, not a separate chat bolted on.

## CLI multi-session management (Agent view as agent UI)

Claude Code's Agent view is a concrete CLI implementation of the "see all sessions" UI layer [^src4]. Rather than a graphical workbench, the surface is a terminal dashboard:

- `claude agents` (or press left-arrow from any session) opens the list; each row shows session name, status (waiting / running / done), last response content, and last interaction time.
- **Peek mode**: select a session to see the last turn inline; reply without attaching to the full session; press Enter to attach.
- **Background launch**: `claude --bg [task]` starts a session directly in the background; `/bg` sends any running session to the list.

This addresses the core agent-UI problem of multi-session awareness in the command-line context: "one place to manage all your Claude Code sessions" replacing "multiple terminal tabs, a tmux grid, and an overloaded mental ledger" [^src4]. The pattern — a unified session-status view with selective in-place interaction — is the CLI analog of the chat+workbench shell's session panel. See [Claude Code](/ai-engineering/claude-code.md) for the full agent-view mechanics and the fire-and-forget `/goal` combination.

## Related

- [AI Agent](/ai-engineering/ai-agent.md) — Pi is the harness Boring UI builds on; agent-mode and serverless deployment
- [Agent Skills](/ai-engineering/agent-skills.md) — the skill/plugin layer that customizes the shell
- [MCP](/ai-engineering/mcp.md) — tool/coordination layer the harness can integrate

---

[^src1]: [hachej/boring-ui — build agent-powered apps without reinventing the shell](../../raw/web/github-hachej-boring-ui-build-agent-powered-apps-without-rei.md)
[^src2]: [Notion — where teams and agents work together](../../raw/web/notion-where-teams-and-agents-work-together.md)
[^src3]: [Launching Boring UI](../../raw/email/email-2026-05-28-launching-boring-ui.md) — Julien Hurault (Ju Data Engineering Newsletter)
[^src4]: [Agent view in Claude Code](../../raw/notes/notes-clippings-agent-view-in-claude-code.md) — Anthropic announcement
