---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-agents-md-what-belongs-human-authored-context.md
    channel: notes
    ingested_at: 2026-07-15
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
  - context-engineering
  - agents-md
created: 2026-07-15
updated: 2026-08-13
provisional: false
url: https://addyosmani.com/blog/agents-md/
origin: obsidian
---

# AGENTS.md — What Belongs There and What Wastes Context

**TL;DR:** Addy Osmani makes a data-backed case that auto-generating AGENTS.md (or CLAUDE.md) files harms agent performance and inflates costs; only human-authored, non-discoverable context improves results. A clear taxonomy distinguishes what belongs from what should be deleted.[^1]

---

## The Auto-Generation Trap

Using `/init` or LLM tools to generate AGENTS.md introduces redundant information that agents can discover independently, bloating context and reducing task success.[^1] The performance impact is measurable: auto-generated files reduce task success by 2–3% while increasing costs by 20%+.[^1]

The mechanism is an **anchoring effect**: including information in the file biases agents toward those patterns even when outdated, competing with actual task requirements.[^1]

---

## Research Backing

Two studies cited:

- **Lulla et al. (2026):** AGENTS.md reduced runtime by 28.64% and output tokens by 16.58% — but only when human-authored.[^1]
- **ETH Zurich study:** auto-generated files degraded performance; "developer-written files improved success by ~4%."[^1]

---

## Taxonomy: What Belongs vs. What to Delete

**Include (non-discoverable only):**
- Tool choices — e.g., "use `uv` for package management"[^1]
- Non-obvious conventions and operational gotchas[^1]
- Deprecated patterns still in production use that agents would otherwise avoid[^1]
- Custom middleware patterns or architectural landmines[^1]

**Delete:**
- Directory structure descriptions (agents can discover this)[^1]
- Tech stack overviews (discoverable from package files)[^1]
- Module explanations (already in code comments/READMEs)[^1]
- Codebase architecture (already in existing documentation)[^1]

The guiding test: if an agent can discover it by reading the repo, it doesn't belong in AGENTS.md.[^1]

---

## Architecture: Hierarchical Context Loading

Hierarchical AGENTS.md files with task-aware context loading outperform monolithic root-level files.[^1] Scoped files closer to the relevant code surface only what matters for that context.

---

## Maintenance Reality

Static documentation rots. Agent performance degrades with outdated context files over time.[^1] Keeping the file minimal reduces maintenance burden and limits the anchoring damage when content goes stale.[^1]

---

## Related Corpus Pages

- [/ai-engineering/context-engineering.md](/ai-engineering/context-engineering.md) — the broader discipline behind this practice

---

[^1]: Osmani, Addy. "AGENTS.md — What Belongs There and What Wastes Context." <https://addyosmani.com/blog/agents-md/>. Via `raw/notes/notes-03-resources-articles-agents-md-what-belongs-human-authored-context.md`.
