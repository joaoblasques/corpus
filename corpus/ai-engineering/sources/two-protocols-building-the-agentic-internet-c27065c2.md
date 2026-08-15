---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-two-protocols-building-the-agentic-internet-c27065c2.md
    channel: web
    ingested_at: 2026-08-15
aliases:
  - agentic internet
  - MCP vs A2A
  - Agent-to-Agent protocol
  - AgentCard
  - A2A protocol
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-15
updated: 2026-08-15
url: https://blog.apify.com/mcp-a2a-agentic-internet/
origin: obsidian-list
---

# Two Protocols Building the Agentic Internet

**TL;DR** — Two protocols are standardizing how AI agents find tools and coordinate with each other: MCP (Anthropic, Nov 2024) handles agent↔tool connections (vertical); A2A (Google, Apr 2025) handles agent↔agent delegation (horizontal). Both were donated to the Agentic AI Foundation in 2025 and are now vendor-neutral.[^src1]

## The distinction

- **MCP**: client-server model. The agent is the client; tools/data/services are servers. The agent decides exactly which tool to invoke and manages the entire workflow.[^src1]
- **A2A**: orchestrator-to-sub-agent model. An orchestrator agent hands a task to a sub-agent and trusts it to handle execution. The sub-agent has its own reasoning, tools, and workflow — the orchestrator only manages outcomes, not steps. Agents can also coordinate as peers.[^src1]

"MCP is vertical: an agent reaches down to a tool or data source that serves it. A2A is horizontal: an agent reaches across to another agent it can delegate to."[^src1]

## A2A technical primitives

**AgentCards**: a JSON document published at `/.well-known/agent-card.json`. Machine-readable description of what the agent can do, inputs/outputs it accepts, and how to authenticate. Orchestrators fetch this to evaluate sub-agents before delegating.[^src1]

**Tasks**: the unit of work. Lifecycle states: `submitted → working → input-required → completed → failed → canceled → rejected`. Sub-agents stream live progress back. If additional credentials are needed mid-task, the task moves to `auth-required` and pauses rather than failing silently.[^src1]

Technical foundation: HTTP, JSON-RPC 2.0, and streamable HTTP for live updates.[^src1]

## When A2A earns its place

For simple setups, MCP alone can handle multi-agent coordination. A2A adds value at scale: "when an organization runs many agents across different vendors and frameworks, coordinating them through individual MCP connections becomes unmanageable."[^src1]

## Example workflow

Orchestrator (competitor analysis) → A2A → research sub-agent → MCP → web scrapers, search APIs, content extractors → structured results → orchestrator. "The orchestrator never touched the tools directly; the research agent never saw the broader workflow."[^src1]

## Governance

Both MCP and A2A were donated to the **Agentic AI Foundation** in 2025, removing Anthropic and Google as unilateral roadmap controllers. Vendor-neutral governance lets the broader industry build on them with confidence.[^src1]

## See also

- [MCP](/ai-engineering/mcp.md) — full MCP concept page
- [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) — orchestration patterns
- [Agentic Workflow](/ai-engineering/agentic-workflow.md)

---

[^src1]: [Two protocols building the agentic internet](../../../raw/web/web-two-protocols-building-the-agentic-internet-c27065c2.md) — Apify blog, 2026-06-29
