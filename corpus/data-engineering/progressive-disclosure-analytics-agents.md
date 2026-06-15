---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-21-progressive-disclosure-the-core-pattern-for-analytics-agents.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - progressive disclosure
  - analytics agents
  - text2sql
  - three-layer disclosure
  - discover understand execute
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-15
updated: 2026-06-15
---

# Progressive Disclosure for Analytics Agents

**TL;DR.** Most analytics agents load *all* schema and semantic metadata upfront — the fastest path to **context rot** and hallucinated queries [^src1]. **Progressive disclosure** (a Jakob Nielsen UX principle: show only what's needed now, reveal more on demand) applied to agent architecture gives a **three-layer flow: Discover → Understand → Execute** [^src1]. Caveat: dumping the *entire semantic layer* every time is "the same flat-context trap with better guidance," and none of it works if the underlying metadata is garbage [^src1]. (Cross-domain: the agent/context mechanics are owned by [[ai-engineering/context-engineering|ai-engineering]]; this page covers the *data/analytics* application.)

## The problem

Connect an agent to a warehouse and load the full schema — 200 tables, 3,000 columns, every description, all business logic — then ask "Q4 revenue by region?" and 10 tables look equally relevant; the model picks one and executes "with full confidence" [^src1]. Every table description and business rule competes for finite attention; **context rot is a design problem that compounds with every tool/table added** [^src1]. The cognitive overload an LLM hits is the same a human would — but with zero self-awareness that it's wrong [^src1].

## The three layers

Mirroring how a good analyst onboards (schema overview first, then zoom into task-relevant tables, then learn edge cases on demand) [^src1]:

| Layer | What loads | Analogy |
|---|---|---|
| **1. Schema Discovery** | A compressed catalog: domain, table name, grain, one-line summary, key relationships — a "table of contents" | A SKILL's frontmatter / an index [^src1] |
| **2. Semantic Loading** | For *selected* tables only: full column definitions, business logic, edge cases, join paths (e.g. `revenue_net_usd` excludes refunds; test orders filtered) | Reading the chosen chapter [^src1] |
| **3. Query Execution** | Agent plans and runs with the right context in scope (join, filter Q4, sum the correct measure) | Doing the task [^src1] |

"Three layers with progressive depth, and the agent never sees what it doesn't need" [^src1].

## Static semantic layers aren't enough

The [[data-engineering/semantic-layer|semantic layer]] is essential — without clear definitions agents hallucinate confidently — **but loading the whole semantic layer every session is just the flat-context trap again** (50 Cube/dbt/Looker definitions dumped per call) [^src1]. Remedies [^src1]:
- Better **data modeling from scratch**: AI-ready business descriptions, explicit filtering, cleansing noise, pre-computing complex metrics at the model level (without overdoing one-big-table).
- **Avoid ambiguity**: the single greatest source of hallucinated SQL is *metric-selection ambiguity* — cut cases where multiple tables answer the same thing.
- The semantic layer **needs its own index layer** — a compressed representation to decide what to load before loading it. Add the semantic layer's complexity only when modeling complexity demands it ("don't add layers until the simpler approach breaks").

Tools embodying this: **The Boring Semantic Layer** exposes `list_models → describe_model → query_model` over MCP (three-layer, scoped to one library); the LLM writes *semantic queries*, not SQL, so "there's nothing ambiguous left to hallucinate" [^src1].

## Where it already exists

- **Claude Code / claude.ai deferred tools** — the "Tool loaded." message is progressive disclosure: rather than burning tokens loading every tool/MCP schema upfront, the agent calls `ToolSearch`/fetches a schema on demand [^src1]. (This is exactly the mechanism this corpus environment uses.)
- **FastMCP** — a **BM25 search transform** wraps all tools behind `search_tools` (natural-language → ranked top matches load), and **Code Mode** has the agent write Python orchestrating multiple calls in a sandbox so only the final result re-enters context (`get_tags → search_tools → get_schemas → execute`) [^src1].
- **Postgres MCP** — three-layer fix for a 20+-tool context bomb: `list_schemas + list_tables` (names/row counts) → `execute_sql` on selected tables → `get_query_plan` before executing [^src1].
- **OpenMetadata MCP** — `searchEntities → getEntityDetails → impact analysis` is two-layer progressive disclosure out of the box [^src1]. See [[data-engineering/agentic-data-modeling|Agentic Data Modeling]].
- **Pipeline debugging** — scope each MCP log scan to the entity the previous layer pointed to (scheduler → worker → task instance), not "here's everything" [^src1].

## The principle

> Defer loading expensive context until an agent has a reason to load it. Attention is finite — use it wisely [^src1].

Discovering what matters first beats loading everything and filtering noise, and the savings **compound** as agent complexity grows [^src1].

## Related

- [[data-engineering/semantic-layer|Semantic Layer]] — *what* context to give the agent
- [[data-engineering/agentic-data-modeling|Agentic Data Modeling]] — OpenMetadata MCP discovery layers
- [[ai-engineering/context-engineering|Context Engineering]] · [[ai-engineering/agent-skills|Agent Skills]] · [[ai-engineering/mcp|MCP]] (ai-engineering)
- [[ai-engineering/context-window-management|Context Window Management]] — context rot (ai-engineering)
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Progressive Disclosure: The Core Pattern for Analytics Agents](../../raw/email/email-2026-05-21-progressive-disclosure-the-core-pattern-for-analytics-agents.md)
