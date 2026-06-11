# Research: LLM-wiki ingest best practices (grounding for CLAUDE.md v0.6)

- **Date:** 2026-06-11
- **Purpose:** Ground the v0.6 optimized batch-ingest pipeline and claim-lifecycle enhancements in external best practice. Three parallel web-research passes; key findings + sources below.

## 1. Karpathy's LLM-wiki pattern + v2 iterations

- **Three layers** (raw sources / LLM-owned wiki / human schema) and **three ops** (ingest, query, lint). Rationale: *"the tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping"* — LLMs do cross-referencing/updating tirelessly. A single source typically touches **10–15 wiki pages**; touching only 1–2 signals under-extraction.
- **rohitg00 "LLM Wiki v2"** — names what breaks at scale (flat index unmanageable beyond 100–200 pages; no claim lifecycle; noise accumulates) and adds: per-claim **confidence + provenance + confidence decay**, **typed entity extraction + typed relationships**, **supersession over deletion**, **contradiction detection on write**, **quality scoring before filing**, consolidation tiers, hybrid search beyond a flat index.
- **Astro-Han `karpathy-llm-wiki`** — Agent-Skills implementation; explicit **cascade pass**, three-way routing (merge / new page / cross-link), separate `Sources:` vs `Raw:` fields.
- **Practitioner consensus:** lower the source-summary bar — per-source summaries are what keep the wiki queryable without reading full files; scale ceiling ~100–300 pages.
- Sources: [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), [X post](https://x.com/karpathy/status/2039805659525644595), [rohitg00 v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2), [Astro-Han repo](https://github.com/Astro-Han/karpathy-llm-wiki), [Starmorph guide](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide), [MindStudio](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code).

## 2. KM architecture for many domains (hub-and-spoke / MOC / Zettelkasten / PARA)

- **MOC split at the "mental squeeze point"** — group a sub-cluster into a section at ~5 spokes; spin a sub-hub at ~15. **Shallow nesting** (3 levels: index → hub → page; 4 only in large domains).
- **Orphan = 0 inbound hub links.** Notes can have multiple MOC memberships; cross-domain note = one primary page linked from the secondary hub; true bridges = `synthesis` pages.
- **Top-level domain soft cap ~10** → consolidation review beyond. **New domain only ≥3 distinct sources** (stricter than MOC's 5-note rule — keep).
- **Zettelkasten:** emergent atomicity (create stubs on ingest, split in lint, don't block ingestion); digital links + stable slugs replace folgezettel IDs; promote pages to hubs by link-degree.
- **PARA** organizes by *actionability*, conflicting with topic-domains — keep on separate layers (PARA/raw = source layer; corpus = topic layer); PARA hints never override topic placement.
- **Aliases** are the load-bearing dedup mechanism; **tags = orthogonal facets only**, never structural. Mature page link floor: ≥1 hub + ≥2 lateral/source links.
- Sources: [Obsidian Rocks MOC](https://obsidian.rocks/maps-of-content-effortless-organization-for-notes/), [dsebastien MOC guide](https://www.dsebastien.net/2022-05-15-maps-of-content/), [LYT](https://www.linkingyourthinking.com/), [zettelkasten.de atomicity](https://zettelkasten.de/posts/principle-of-atomicity-difference-between-principle-and-implementation/), [Forte Labs PARA](https://fortelabs.com/blog/para/), [Obsidian folders-vs-links-vs-tags](https://forum.obsidian.md/t/folders-vs-linking-vs-tags-the-definitive-guide-extremely-short-read-this/78468).

## 3. Batch-ingesting a large heterogeneous backlog

- **Cluster first** on condensed records (title + tags + first paragraph) — fits one long-context window for 136 items. LLM thematic grouping allows multi-cluster membership; plan a reduction/merge step.
- **Route by cluster, not source** — decide domain once per cluster, inherit to members. Pass `_domains.md` as the ontology constraint to prevent runaway category creation.
- **Dedup globally before writing** — "blocking is 10× more important than matching." Build a canonical entity registry `{slug → aliases, domain, page}`; cosine ≥0.90 → LLM arbitration. Prevents duplicate pages before they're written.
- **Process cluster-by-cluster** to keep each domain's dedup/linking context hot.
- **Cross-linking:** intra-cluster first → existing pages via registry/index → mandatory hub link. **Embedding proposes, LLM confirms** against page text (never auto-link on cosine alone — avoids hallucinated links).
- **Safe parallelism:** **one-writer-per-domain**; Coordinator owns shared files (`_index`, `_log`, `_domains`, `_config`); workers return deltas. Hub-and-spoke, not mesh.
- **Pitfalls + mitigations:** over-extraction (cap 3–10 entities/source); shallow pages (stub only with ≥1 link + ≥1 citation); hallucinated cross-links (LLM-confirm); unverifiable claims (citation gate); contradictions (→ synthesis page); structural drift (min-3-sources, ontology constraint, lint consolidation).
- Sources: [Semantic Entity Resolution (TDS)](https://towardsdatascience.com/the-rise-of-semantic-entity-resolution/), [Entity Resolution at Scale](https://medium.com/@shereshevsky/entity-resolution-at-scale-deduplication-strategies-for-knowledge-graph-construction-7499a60a97c3), [LLM-Assisted Topic Reduction for BERTopic](https://arxiv.org/html/2509.19365v1), [Hallucination-Resistant RE](https://arxiv.org/pdf/2508.14391), [Grounded KG Extraction (AEVS)](https://www.mdpi.com/2073-431X/15/3/178), [Multi-Agent Orchestration Guide](https://www.augmentcode.com/guides/multi-agent-orchestration-architecture-guide).

## How this shaped CLAUDE.md v0.6

- §8.1 batch path → the Phase 0–5 cluster-based pipeline + Coordinator-owns-shared-files rule (findings 3).
- §4 + §7.1 claim-lifecycle (`confidence`, `last_confirmed`, `supersedes`/`superseded_by`, contradiction-on-write, typed relationships) (findings 1, rohitg00 v2).
- Reinforced existing rules: min-3-source domains, aliases-as-dedup, no-orphans/hub-links, summary threshold lowered, 10–15 page cascade target.
