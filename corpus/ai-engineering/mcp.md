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
aliases:
  - MCP
  - Model Context Protocol
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-12
---

# MCP (Model Context Protocol)

**TL;DR**: A structured coordination protocol that defines how agents, tools, and memory communicate — replacing ad-hoc prompting with a standardized interface for tool calls, memory access, and context sharing [^src1].

## What it does

MCP replaces chaotic back-and-forth prompt engineering in multi-agent systems with a formal protocol layer. Governs [^src1]:
- **Tool calls** — structured request/response format for tool invocation
- **Memory access** — how agents read and write to memory stores
- **Context sharing** — how context is passed between agents or from tools back to the orchestrator

Described as "essential for scalable multi-agent systems" [^src1].

> [unsourced — please verify]: MCP was introduced by Anthropic as an open standard; this source describes its purpose but not its origin.

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

## See also

- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — MCP is the coordination layer for multi-agent architectures
- [[ai-engineering/tool-calling|Tool Calling]] — MCP standardizes how tool calls are structured
- [[ai-engineering/agent-memory|Agent Memory]] — MCP governs memory access protocols
- [[ai-engineering/agent-security|Agent Security]] — scoped permissions and OAuth (e.g. Metabase) limit tool blast radius
- [[ai-engineering/claude-code|Claude Code]] — MCP client; configures servers via `claude mcp add`

---

[^src1]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
[^src2]: [Behind Substack Author MCP: Resources, Prompts, and Tools Explained](../../raw/web/behind-substack-author-mcp-resources-prompts-and-tools-expla.md)
[^src3]: [Building a Substack Agent with SKILLs and MCP](../../raw/web/building-a-substack-agent-with-skills-and-mcp.md)
[^src4]: [Desktop Commander MCP](../../raw/web/github-wonderwhy-er-desktopcommandermcp-this-is-mcp-server-f.md)
[^src5]: [Metabase MCP server documentation](../../raw/web/mcp-server-metabase-documentation.md)
[^src6]: [nao MCP servers](../../raw/web/github-getnao-nao-mcp-servers.md)
