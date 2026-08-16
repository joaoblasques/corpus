---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-agent-native-the-next-architecture-for-software-9da21efb.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - agent-native architecture
  - agent-native apps
tags:
  - corpus/ai-engineering
  - source
  - agent-native
  - software-architecture
  - human-ai-collaboration
created: 2026-07-02
updated: 2026-08-16
provisional: false
url: https://www.builder.io/blog/agent-native-architecture
origin: obsidian-list
---

# "Agent-Native: The Next Architecture for Software"

**Source:** Builder.io blog · [https://www.builder.io/blog/agent-native-architecture](https://www.builder.io/blog/agent-native-architecture)

**TL;DR:** Agent-native architecture builds software so humans and AI agents share the same actions, data, permissions, and context — removing the forced trade-off between a polished human UI and a fully agent-operable product. It defines five core principles and contrasts with SaaS, raw agents, and internal tools.

---

## The Problem: Two Bad Trade-offs

Traditional software forces a choice between two compromises.[^src]

> "Most software today gives you one of two compromises: a polished interface an agent cannot fully use, or a powerful agent with no real interface for humans."[^src]

- **SaaS**: polished UI and clear workflows, but agent access is partial or bolted on after the fact. A chatbot in the corner can summarize or draft, but it cannot reliably use the same workflows or change the product through the same primitives as the UI.[^src]
- **Raw agents** (e.g. Claude Projects, general-purpose coding agents): broad, flexible, natural-language control, but start as a blank canvas with no durable workflows, no obvious starting points, no domain-specific interface.[^src]

Both gaps point toward a third category: agent-native apps, which combine the structure of SaaS with the flexibility of raw agents.[^src]

---

## AI-enabled → AI-native → Agent-native

The source defines a three-stage spectrum:[^src]

| Stage | Definition | Test | Example |
|---|---|---|---|
| AI-enabled | AI features present; product works without them | Remove AI — does product still work? | Project management app with an AI summary button |
| AI-native | AI is central to the product's value | Remove AI — does product collapse? | Coding assistant, image generator, chat-first research tool |
| Agent-native | AI is central AND a full human-facing interface shares the same actions, data, and permissions | Can both UI and agent operate the same workflows? | Email client where user and agent can archive, draft, label, and route through the same underlying actions |

"Agent-native goes one step further: AI is central, and the product still has a real interface for humans."[^src]

**Historical analogy:** mobile-native apps were not desktop websites squeezed onto small screens; they were designed around the constraints of mobile (touch, camera, location, intermittent attention) from the start. Agent-native is the same kind of architectural shift — not SaaS with AI squeezed in.[^src]

---

## The Five Architectural Principles

### 1. Agent UI Parity
Anything the UI can do, the agent can do. And anything the agent does should be visible, inspectable, or controllable through the product's interface, logs, permissions, or state.[^src]

The agent must call the same underlying capability that powers the product — not screen-scrape the UI or use a fragile side-channel.[^src]

*Example:* An agent-native email app lets the agent draft replies, inspect threads, apply labels, archive notifications, route messages, and pull CRM context — all through the same primitives a human uses.[^src]

### 2. One Shared Action Model
Agent UI parity only works if the same capability is not rebuilt for every surface. Traditional software creates drift: a UI action, an API endpoint, an automation hook, an LLM tool definition, a CLI command — each copy diverges.[^src]

The solution is to define each action once (e.g. "archive an email", "create a dashboard"), then expose it to the UI, agent tools, external clients, and other agents through protocol routing.[^src]

> "Define the action once … From that single definition, the UI can call it, the agent can see it as a tool, external clients can reach it, and other agents can route to it."[^src]

A single action definition can become a UI mutation, an agent tool, an HTTP endpoint, a CLI command, an MCP tool, and an A2A tool simultaneously.[^src]

### 3. Shared State and Context Awareness
The agent must know what the user is looking at: current view, selection, active filters, what changed while the agent was working.[^src]

In practice this means: the UI writes navigation state as the user moves through the app; a `view-screen` action gives the agent a fresh snapshot; a `navigate` action lets the agent move the UI when asked. Both sides read and write the same database-backed state.[^src]

The source recommends a deliberately simple coordination pattern: actions write to SQL, a version counter increments, and the UI polls and invalidates the right data. "The database is the coordination layer between the human interface and the agent."[^src]

### 4. Protocol Readiness
Agent-native apps are software nodes that agents and other apps can use. They should expose capabilities through standard agent protocols (MCP, A2A) so that other tools (e.g. Claude Code, Cursor, Codex) can understand and operate them.[^src]

This is not a one-off integration project. If actions are the shared unit of product behavior, exposing them to MCP, A2A, a CLI, or an internal API becomes a routing problem rather than a second product.[^src]

*Example:* an analytics app routing to a slide app to turn a dashboard into a deck; a calendar coordinating with an email app to propose meeting times.[^src]

### 5. Governed Execution
The agent must act inside the same permission model as the product. If the user cannot access a record, the agent cannot access it on their behalf. If an action requires confirmation, the agent must respect that boundary.[^src]

"The product is trustworthy because those actions are scoped, reviewable, and reversible where needed."[^src]

---

## Growth Layers (as apps mature)

The five principles define the minimum. As agent-native apps move from demos to repeated work, additional capabilities matter:[^src]

**SQL-backed workspaces:** AGENTS.md for shared instructions, LEARNINGS.md for durable team memory, personal memory, skills, custom sub-agents, scheduled jobs, and connected MCP servers — all stored in SQL (not a local filesystem), scoped by person or organization, and editable inside the app.[^src]

**Runtime tools:** private dashboards, calculators, monitors, or small interactive utilities the agent creates inside the app without a code change, build, or deploy. These fill the gap between permanent product features and one-off chat responses.[^src]

**Automations:** event-triggered or scheduled workflows ("When an enterprise lead books a meeting, post to Slack"; "Every Monday, summarize last week's support threads") using the same actions, permissions, and audit surfaces as the rest of the product.[^src]

**Observability:** progress state, notifications, traces, feedback, evals, cost/latency metrics. The source calls these essential rather than enterprise extras, because agent failures are qualitatively different from normal SaaS failures — an agent may choose the wrong tool, skip a step, spend too much, or be confused by stale context.[^src]

---

## Cloneability

"Cloneability is where the agent-native idea becomes practical for developers and teams."[^src]

SaaS products make data feel rented. Agent-native apps push in the other direction: clone the software, own the code, own the database, change the product when the default shape no longer fits.[^src]

> "When you own the database and have an agent, you can ask questions the original developers never thought to answer."[^src]

This is the economic and practical argument against one-size-fits-all SaaS.[^src]

---

## Comparison Table

The source provides a full comparison across dimensions:[^src]

| Dimension | Traditional SaaS | Raw agents | Agent-native |
|---|---|---|---|
| Who controls it? | Vendor | User (prompts + tools) | Developer/team (app, data, agent) |
| Human UI quality | Usually strong | Usually absent | Full product UI |
| Agent access | Partial, bolted on | Broad but unstructured | Full, through app's own actions |
| Data ownership | Vendor database | Depends on tools | Your database, schema, exports |
| Context awareness | UI state hidden from agent | Manual prompting | Agent sees view, selection, app state |
| Observability | Product analytics, limited agent traces | Chat history + tool logs | Progress, traces, evals, feedback, cost, latency |

---

## Example App Categories

The source illustrates agent-native patterns across five categories:[^src]

- **Email**: agent can summarize threads, draft replies, apply labels, archive notifications, route messages — through the same inbox the user operates.
- **Analytics**: ask for a dashboard in natural language, inspect visually, edit it directly; chart, query, and agent analysis all belong to the same application.
- **Calendar**: scheduling work (find a time, reschedule, protect focus blocks, coordinate across teammates) accessible to both user and agent through the same actions; coordinates with email/contacts apps.
- **Video clips**: viral shareability preserved; agent can cut, summarize, title, organize, and route videos through the same primitives.
- **Motion video**: natural language control over a composition model (add title card, change easing, render MP4) without losing the timeline/preview UI.

---

## Getting Started

Two paths described:[^src]

- **Individual path**: clone a template at agent-native.com/templates using your own LLM key; the blank canvas problem disappears when the agent lives inside a working app.
- **Team path**: requires hosting, database management, auth, permissions, branching, governance, and shared key provisioning. Builder.io is positioned as the team governance layer.

"One shared LLM key can power many owned apps" is cited as a meaningful cost-model difference from per-seat SaaS subscriptions.[^src]

---

[^src]: Builder.io, "Agent-Native: The Next Architecture for Software," https://www.builder.io/blog/agent-native-architecture (collected 2026-06-29). Source file: `raw/web/web-agent-native-the-next-architecture-for-software-9da21efb.md`.
