---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-study-notes-gemini-cli-deep-dive-with-mcps.md
    channel: notes
    ingested_at: 2026-07-10
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-10
updated: 2026-08-08
provisional: false
url: 
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
---

# Gemini CLI — Deep Dive with MCPs

**TL;DR:** Three walkthroughs demonstrate Gemini CLI's built-in tools (Google Search, Web Fetch, file I/O), the DuckDuckGo MCP (real URL return), and the HuggingFace + Context7 MCPs (Gradio Spaces access, live docs). Together these three layers cover most development needs.[^1]

---

## Walkthrough 1: Next.js Chat App (Built-in Tools)

A streaming Gemini chat app with markdown rendering and model selector was built and deployed to Google Cloud Run using Gemini CLI's built-in tools.[^1]

**Built-in tools:**

| Tool | Purpose |
|---|---|
| Google Search | Find latest versions and current API model names |
| Web Fetch | Pull content from a specific full URL |
| File read/write | Autonomous file editing |

**Practical tips from the source:**

- Use Google Search first for anything version-specific — LLMs have stale training data.[^1]
- Pass screenshots via `@/path/to/local/image`; images must be local, not web URLs.[^1]
- Screenshots help debug UI issues the model cannot see from code alone.[^1]
- A low `max_output_tokens` default causes streaming to appear broken.[^1]

**Memory persistence:** Gemini CLI can save a summary of a long conversation to `gemini.md` for reuse in future sessions; it cannot save the full conversation, only a summary.[^1]

---

## Walkthrough 2: DuckDuckGo MCP

**Problem:** Built-in Google Search returns redirect URLs, not raw URLs.[^1]

**Solution:** The DuckDuckGo MCP returns real URLs.[^1]

**Setup pattern (from source):**

```bash
python -m venv .venv && source .venv/bin/activate
uv pip install duckduckgo-mcp-server
```

Config goes in `.gemini/settings.json` under `mcpServers`.[^1] Any Claude Desktop MCP config works in Gemini CLI with the same format.[^1]

---

## Walkthrough 3: HuggingFace + Context7 MCPs

**HuggingFace MCP:** Exposes Gradio Spaces as callable tools — examples given include a Studio Ghibli image filter and Flux image generation.[^1]

**Context7 MCP:** Pulls live library documentation into context during development. The source describes the pattern as telling Gemini "use Context7 for ADK docs," which causes it to fetch current Python ADK documentation rather than relying on stale training data.[^1] The source calls it "the standard go-to MCP for any active library development."[^1]

A Google ADK agent was built as the demo, tested with ADK Web UI.[^1]

---

## Key Insight

> "Google search is built-in but gives redirect URLs. DuckDuckGo MCP gives real URLs. Context7 keeps docs current."[^1]

These three layers — built-in tools, DuckDuckGo MCP, Context7 MCP — together "cover most development needs" per the source.[^1]

---

[^1]: raw/notes/notes-03-resources-study-notes-gemini-cli-deep-dive-with-mcps.md
