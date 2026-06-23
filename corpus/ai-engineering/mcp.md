---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/behind-substack-author-mcp-resources-prompts-and-tools-expla.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/building-a-substack-agent-with-skills-and-mcp.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-getnao-nao-mcp-servers.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-wonderwhy-er-desktopcommandermcp-this-is-mcp-server-f.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/mcp-server-metabase-documentation.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-building-agents-that-reach-production-systems-with-mcp.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-how-to-set-up-your-claude-connectors-mcp.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-new-connectors-in-claude-for-everyday-life.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-09-04-mcp-helps-but-how.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/web-sdks-model-context-protocol.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/web/web-mcp-apps-model-context-protocol.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-elicitation-model-context-protocol.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-github-cloudflare-mcp-mcp-server-for-the-cloudflare-api.md
    channel: web
    ingested_at: 2026-06-23
aliases:
  - MCP
  - Model Context Protocol
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-23
---

# MCP (Model Context Protocol)

**TL;DR**: A structured coordination protocol that defines how agents, tools, and memory communicate — replacing ad-hoc prompting with a standardized interface for tool calls, memory access, and context sharing [^src1].

## SDK support tiers

Official MCP SDKs as of mid-2026 [^src11]:

| Tier | Languages | Status |
|---|---|---|
| **Tier 1** | TypeScript, Python, C#, Go | Fully maintained, production-ready |
| **Tier 2** | Java, Rust | Supported, may lag behind Tier 1 |
| **Tier 3** | Swift, Ruby, PHP | Community-maintained |
| **TBD** | Kotlin | Planned |

MCP SDKs surpassed **300 million downloads/month** as of mid-2026 (up from 100M at start of year) [^src7].

## What it does

MCP replaces chaotic back-and-forth prompt engineering in multi-agent systems with a formal protocol layer. Governs [^src1]:
- **Tool calls** — structured request/response format for tool invocation
- **Memory access** — how agents read and write to memory stores
- **Context sharing** — how context is passed between agents or from tools back to the orchestrator

Described as "essential for scalable multi-agent systems" [^src1].

> [unsourced — please verify]: MCP was introduced by Anthropic as an open standard; this source describes its purpose but not its origin.

## Architecture: Host / Client / Server

MCP is structured as three components [^src10]:

- **MCP Host** — where the agent "lives": a chat interface (e.g. a customer-support assistant), an IDE extension (a code co-pilot), or a backend orchestrator coordinating multiple agents. The host handles the conversation and coordinates the flow [^src10].
- **MCP Client** — the middle layer that parses user prompts, discovers available tools/resources, sends structured instructions to the LLM, and handles tool calls + returns results. One client can connect to one or many servers, all using the same protocol [^src10].
- **MCP Server** — where the functionality lives: wraps a SQL/NoSQL database, a public API, GitHub, local filesystems, or internal company tools, and exposes a machine-readable catalog of what's available (see the [three server primitives](#the-three-server-primitives) below) [^src10].

**Runtime loop.** A typical request flows: user prompt → host → client queries the server for the tool list → client sends the prompt + tool catalog to the LLM → LLM selects a tool and supplies arguments → client invokes it via the server → server executes (DB query, API call) and returns the result → agent responds to the user [^src10]. The loop is modular and dynamic: "No need to redeploy when new tools are added. No hardcoded schemas" [^src10].

**Enterprise value.** This addresses real production pain points [^src10]:
- **Tool discovery at runtime** — agents query the server for available tools and adapt on the next call; no hardcoded schemas, no redeploy when a function is added [^src10].
- **Standardized interfaces across systems** — every server uses the same protocol, so one client talks to many servers without juggling per-service integration styles [^src10].
- **Modularity + team ownership** — each department (DevOps, Support, Finance) owns and manages its own server: secure, versionable, sandboxed [^src10].
- **LLM-native orchestration** — designed for AI rather than retrofitted; agents discover tools, chain calls, retry, and reason across multi-step workflows. Plays with frameworks like LangChain and LangGraph [^src10].

## The three server primitives

An MCP server exposes three kinds of asset; the LLM decides when and how to use them, and success "relies on how well defined those resources, tools and prompts are" [^src2]:

| Primitive | What it is | When to use |
|---|---|---|
| **Tools** | What the AI can *run* — fetch data, call APIs, read files | Real-time data needed, different inputs each time, calling external APIs [^src2] |
| **Prompts** | What the AI can *follow* — reusable multi-step workflows packaged as code, naming which tools to use | Multi-step workflows that work consistently; encoding expertise into repeatable processes [^src2] |
| **Resources** | What the AI can *read* — static docs, setup guides, integration patterns | Documentation that changes rarely; context without API calls [^src2] |

**The "One Thing" principle.** Each piece should do one thing: one resource = one documentation topic, one prompt = one workflow outcome, one tool = one operation. "If you need 'and' or 'or' to describe what a function does, it probably has more than one responsibility" [^src2]. Violating this cascades into failures and confused AI; a clear single purpose means the AI knows exactly when to call it. A good reality check: ask for the same thing a few times — if the AI always picks the same tool, the definitions are right [^src2]. Tools should return JSON-structured data to keep debugging and formatting predictable [^src2].

**Prompts vs. Skills.** MCP prompts overlap with the Agent Skills pattern — "this is how MCP prompts can be used" [^src2]. In a worked Substack agent, MCP tools are *what the agent can do* while Skills are *how and when* to use them (analysis frameworks, output format, orchestration), collapsing a 50+ line system prompt to one line of identity [^src3]. The combination is the point: "MCP gives you the tools. SKILLs tell the agent how to use them" [^src3]. An agent can also *be* an MCP server — AgentOS wraps the whole agent (skills + tools + orchestration) behind a single `run_agent` MCP tool [^src3].

## Transports: stdio vs. HTTP

MCP servers run locally or remotely [^src2]:
- **stdio** — local only; the server runs as a subprocess of the client (Claude Desktop, Cursor), configured in `claude_desktop_config.json` or `mcp.json`. Use for personal productivity tools, local file processing, development [^src2].
- **HTTP (Streamable HTTP)** — the server runs remotely, accessible from anywhere including Claude mobile. Use for sharing, team collaboration, public APIs, no local file access [^src2].

## Real MCP servers

- **Desktop Commander** — turns the AI into a full dev environment: terminal command execution, process management, full filesystem operations, in-memory code execution (Python/Node/R), and native Excel/PDF/DOCX support, all via MCP [^src4]. Uses host client subscriptions rather than API token costs [^src4]. Ships security hardening (symlink-traversal prevention, command blocklist, Docker isolation) and comprehensive audit logging — but documents that directory restrictions and command blocking "can be bypassed," and recommends the Docker install for production isolation [^src4]. A `fileWriteLineLimit` (default 50) deliberately forces the AI into smaller edits to save tokens and avoid lost work at message limits [^src4]. Installs across Claude Desktop, Cursor, Windsurf, VS Code, Claude Code, Codex, and more [^src4].
- **Metabase MCP server** — Streamable HTTP transport; lets AI clients query Metabase "scoped to the connecting person's permissions" [^src5]. Clients authenticate via OAuth 2.0 against Metabase's own embedded OAuth server (discover endpoints → register client → user consents → scoped token) [^src5]. Exposes tools like `search`, `read_resource`, `construct_query`/`execute_query`, `execute_sql` (gated on native-query permission), and `visualize_query` for inline charts; the MCP server provides tools while the *client* supplies the AI, so Metabase token usage is unaffected [^src5].
- **nao MCP servers** — a library of MCP servers for data integrations (Metabase, Fivetran), configured via `npx`; default JSON output, switchable to Markdown with a `--md` flag [^src6].

## Production patterns for MCP servers (Anthropic guidance)

Anthropic's engineering team documented patterns for building MCP integrations that hold up in production [^src7]:

### Three integration paths
- **Direct API calls** — agent writes HTTP requests in a code-execution sandbox. Works for one agent↔one service; hits an M×N problem at scale (each pair needs its own auth handling and tool descriptions) [^src7].
- **CLI** — agent runs a shell command. Fast and lightweight in local sandboxed environments; fails for mobile, web, or cloud-hosted platforms that don't expose a container [^src7].
- **MCP** — a remote server exposes capabilities once; any compatible client (Claude, ChatGPT, Cursor, VS Code) connects. "The integration is portable, and provides the semantics needed for a feature-rich agent integration" [^src7]. Recommended for production agents.

The MCP SDKs surpassed 300 million downloads/month as of mid-2026 (up from 100M at start of year) [^src7].

### Server-side design patterns

**Group tools around intent, not endpoints.** Fewer well-described tools outperform exhaustive API mirrors: "a single `create_issue_from_thread` tool beats `get_thread` + `parse_messages` + `create_issue` + `link_attachment`" [^src7]. See the One Thing principle above.

**Code orchestration for large surfaces.** When a service requires hundreds of distinct operations, expose a thin tool surface that accepts code: the agent writes a script, the server runs it in a sandbox, only the result returns [^src7]. Cloudflare's MCP server (Code Mode) demonstrates this pattern at scale [^src14]:

- **~1,100 tokens total** for the full tool surface (vs. ~1.17M tokens if all 2,500 API endpoints were exposed as individual MCP tools).
- **Three tools**: `cloudflare_docs` (fetch documentation for a specific API or concept), `cloudflare_ai_search` (semantic search across the docs corpus), `cloudflare_execute` (run code against the Workers runtime via the Workers Preview API for safe execution).
- **Spec lives server-side** via the Dynamic Worker Loader API — the agent fetches the spec for the specific service it needs (Workers, KV, R2, D1, DNS) at runtime rather than loading all specs upfront.
- The model writes Workers JavaScript (or Python for Workers Python support), the server executes it in an isolated preview environment, and only the result returns to context — "bring the code to the API, not the API to the code" [^src14].

This pattern generalizes: any service with >50 distinct operations benefits from a code-execution surface over an exhaustive tool list. The token reduction is typically 100–1000× [^src7][^src14].

**MCP Apps (interactive responses).** An official protocol extension that lets a tool return an interactive interface rendered inline in the chat [^src7][^src12]. Servers shipping MCP apps see "meaningfully higher adoption and retention" than text-only servers [^src7].

Technical model for MCP Apps [^src12]:
- A **sandboxed iframe** is rendered within the MCP client's UI (Claude.ai, Claude Code). The sandbox prevents the app from accessing the parent DOM, user conversations, or credentials.
- Bidirectional communication via **JSON-RPC `postMessage`** — the app sends data to the tool and receives structured responses, enabling real-time interactive UIs.
- Launched from a tool's description via `_meta.ui.resourceUri` — the client detects this field and renders the URI in the iframe instead of showing a text result.
- The app context preserves state during a user interaction, enabling multi-step workflows without losing progress.

Five documented use cases [^src12]: **complex data visualization** (interactive charts, graphs, dashboards); **configuration forms** (structured input for complex parameters); **rich media presentation** (images, formatted docs); **real-time monitoring** (live-updating views of ongoing processes); **multi-step workflows** (wizard-style UIs for complex operations).

Security boundary: the iframe sandbox attribute prevents the app from accessing the parent DOM or other conversations. The MCP server runs with the user's permissions, but the app cannot read conversation context directly — it only receives data explicitly passed through the `postMessage` channel [^src12].

**Elicitation.** Lets a server pause mid-tool call to ask the user for input [^src7][^src13]. Two modes:

- **Form mode** — the server sends a JSON Schema; the client renders a native input form. Schema constraints: flat objects only (no nested schemas, no arrays), primitive types only (string, number, integer, boolean, enum). Required fields are marked in the schema and the form enforces them [^src13].
- **URL mode** — out-of-band flow; the server provides a URL for the client to open in a browser. Used for OAuth authorization, payment flows, and anything requiring a browser context [^src13].

**Three-action response model** [^src13]:
- `accept` — user submitted the form; `content` contains the response matching the schema.
- `decline` — user explicitly skipped this input request (the tool continues without the input).
- `cancel` — user aborted the task entirely; the server should stop processing.

Servers must handle all three actions. Unhandled `cancel` leads to hung sessions. The MCP spec recommends clients visually distinguish which server is requesting data to mitigate phishing (a malicious server prompting for credentials under a trusted server's appearance) [^src13].

**Standardized auth via CIMD.** Client ID Metadata Documents give users "a fast first-time auth flow and far fewer surprise re-auth prompts." Supported in MCP SDKs, Claude.ai, and Claude Code [^src7].

### Client-side context efficiency

**Tool search — 85% token reduction.** Load tool definitions on demand rather than all upfront. In Anthropic's testing, tool search cuts tool-definition tokens by 85%+ while maintaining high selection accuracy [^src7].

**Programmatic tool calling — 37% token reduction.** Process tool results in a code-execution sandbox rather than returning raw to the model. The agent loops, filters, and aggregates in code; only the final output reaches context [^src7].

### Skills + MCP = plugin

**Bundle a skill alongside each MCP server** so the agent gets both raw capabilities and an opinionated playbook for using them. Canva, Notion, and Sentry already publish skills next to their connectors in the Claude directory [^src7]. The MCP community is building an official extension to deliver skills directly from servers, so the client inherits expertise automatically, versioned with the API [^src7].

Plugins for Claude Code bundle skills, MCP servers, hooks, LSP servers, and specialized subagents in one distributable package [^src7].

## Claude Connectors: practical setup patterns

Claude's **connector directory** is the UI layer for MCP — pre-configured one-click integrations that expose live tool data without copy-pasting [^src8]. Two connector types:

- **Pre-configured (one-click)**: browse the directory in Claude Settings → Connectors, click Connect, and authorize via OAuth. Includes Notion, HubSpot, Canva, Gmail, Google Drive, Stripe, and more; new ones land most weeks [^src8].
- **Custom MCP servers**: (a) remote URL — paste the server's Streamable HTTP URL into Settings → Connectors → Add custom connector; (b) Claude Code — run `claude mcp add <name> <url>` or add to `.mcp.json`; (c) local repo — clone, start the server (`npx`/`node`), point Claude at the local address [^src8].

**The over-connection anti-pattern.** "Only connect tools you use weekly. Every connector adds to Claude's context, so a bloated list slows it down and muddies its choices. Three to five live connectors beats thirty idle ones" [^src8].

**Chaining connectors (the real value).** Individual connectors save a tab; chaining them in one prompt replaces a whole process. Example: Calendly books a meeting → Gong captures and summarizes the call → PandaDoc drafts the proposal → Gamma turns it into a deck [^src8]. The pattern: read before write (ask a connector to report first; only let it write/post once the read is trusted), name the tool explicitly in the prompt to remove ambiguity when multiple connectors are live, and give read-only OAuth scopes where available [^src8].

**Marketing/sales connector landscape (as of mid-2026)**: HubSpot, Salesforce, Pipedrive, Apollo, Clay, Gong, Outreach, PandaDoc, Calendly, Lusha, Vibe Prospecting, Gamma, GA4, Meta Ads, Google Ads, Shopify, Klaviyo, Mailchimp, Semrush, Canva, Hotjar, Stripe (33 total in one documented stack) [^src8].

## Consumer connectors (everyday-life expansion)

As of mid-2026 the Claude connector directory has grown to 200+ connectors spanning design, finance, productivity, and health [^src9]. The connector model has expanded beyond work tools to everyday-life apps: AllTrails, Audible, Booking.com, Instacart, Intuit Credit Karma, Intuit TurboTax, Resy, Spotify, StubHub, Taskrabbit, Thumbtack, Tripadvisor, Uber, Uber Eats, and Viator [^src9].

**Dynamic connector suggestions.** Claude now surfaces the right connector for what you're doing — without you typing the name — and presents both when multiple connectors could answer the same question. "Ask Claude to recommend a weekend hike, and AllTrails will surface trails nearby that match your preferences" [^src9]. Refinements (shorter trail, dog-friendly) continue in the same thread.

**Privacy model.** Claude is ad-free (no paid placements). Your data from a connected app is not used to train models, and the app doesn't see your other conversations. Disconnect any connector at any time. Before booking or purchasing on your behalf, Claude is designed to check with you first [^src9].

**Multi-connector workflows** observed in practice [^src9]: a product manager pulls a query from Amplitude, turns it into a Canva deck, and drops the link into Asana for the team — all in a single conversation. Connectors are available on all plans; mobile is in beta.

## See also

- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — MCP is the coordination layer for multi-agent architectures
- [[ai-engineering/tool-calling|Tool Calling]] — MCP standardizes how tool calls are structured
- [[ai-engineering/agent-memory|Agent Memory]] — MCP governs memory access protocols
- [[ai-engineering/agent-security|Agent Security]] — scoped permissions and OAuth (e.g. Metabase) limit tool blast radius
- [[ai-engineering/claude-code|Claude Code]] — MCP client; configures servers via `claude mcp add`
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — uses MCP for external system access; Vaults handle OAuth tokens per session
- [[ai-engineering/claude-cowork|Claude Cowork]] — the end-user product surface where consumer connectors are most active
- [[data-engineering/semantic-layer|Semantic Layer]] (data-engineering) — an MCP server (`MCPSemanticModel`/FastMCP) can expose a governed semantic layer as LLM-queryable tools, constraining the model to validated aggregations

---

[^src1]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
[^src2]: [Behind Substack Author MCP: Resources, Prompts, and Tools Explained](../../raw/web/behind-substack-author-mcp-resources-prompts-and-tools-expla.md)
[^src3]: [Building a Substack Agent with SKILLs and MCP](../../raw/web/building-a-substack-agent-with-skills-and-mcp.md)
[^src4]: [Desktop Commander MCP](../../raw/web/github-wonderwhy-er-desktopcommandermcp-this-is-mcp-server-f.md)
[^src5]: [Metabase MCP server documentation](../../raw/web/mcp-server-metabase-documentation.md)
[^src6]: [nao MCP servers](../../raw/web/github-getnao-nao-mcp-servers.md)
[^src7]: [Building agents that reach production systems with MCP](../../raw/notes/notes-clippings-building-agents-that-reach-production-systems-with-mcp.md) — Anthropic engineering
[^src8]: [How to Set Up Your Claude Connectors (MCP)](../../raw/notes/notes-clippings-how-to-set-up-your-claude-connectors-mcp.md) — practitioner guide (33-connector marketing/sales stack)
[^src9]: [New connectors in Claude for everyday life](../../raw/notes/notes-clippings-new-connectors-in-claude-for-everyday-life.md) — Anthropic announcement
[^src10]: [MCP Helps, But How?](../../raw/email/email-2025-09-04-mcp-helps-but-how.md) — Alex Wang, "Learn AI Together" (LinkedIn)
[^src11]: [MCP SDKs — Model Context Protocol official docs](../../raw/web/web-sdks-model-context-protocol.md)
[^src12]: [MCP Apps — Model Context Protocol](../../raw/web/web-mcp-apps-model-context-protocol.md) — Anthropic
[^src13]: [Elicitation — Model Context Protocol](../../raw/web/web-elicitation-model-context-protocol.md) — Anthropic
[^src14]: [Cloudflare MCP Server (Code Mode)](../../raw/web/web-github-cloudflare-mcp-mcp-server-for-the-cloudflare-api.md) — Cloudflare
