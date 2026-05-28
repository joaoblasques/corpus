# Corpus Log

> Append-only operational log. Chronological, oldest first.

## [2026-05-07] schema | initial bootstrap

- v0.1 schema created
- Empty wiki, awaiting first ingest

## [2026-05-07] schema | v0.2 — softened domain creation rule
- allow provisional domains (1-2 sources) when user confirms expected growth
- lint will auto-flag provisional domains stuck under 3 sources after 30 days
- rationale: user has YouTube playlist evidence proving domains will fill; 3-source proxy unnecessary

## [2026-05-07] domain | ai-engineering created
- rule: standard (2 sources confirmed)
- provisional: false

## [2026-05-07] domain | data-engineering created
- rule: provisional (1 source; user confirmed growth via DE playlists/bootcamp)
- lint review due: 2026-06-06

## [2026-05-07] domain | software-architecture created
- rule: provisional (1 source; user confirmed growth via reading patterns)
- lint review due: 2026-06-06

## [2026-05-07] ingest | deferred | remote-job-boards-data-tech-roles-100k.md
- source: raw/web/remote-job-boards-data-tech-roles-100k.md
- action: deferred — moved to raw/web/ without wiki page
- reason: 1 source insufficient for career domain; no existing domain fits without forcing
- revisit: when 2nd career-related source arrives

## [2026-05-07 01] ingest | Context Engineering
- source: raw/notes/Context Engineering.md (corrected from raw/web/ — reclassified as personal note per §10.4)
- domain: ai-engineering
- pages touched: wiki/ai-engineering/README.md (new), wiki/ai-engineering/context-engineering.md (new)
- new pages: 2
- notes: source is a stub note (<200 words); no source-summary written per §8.1 rule 6; concept page marked stub pending richer source; unsourced claim removed per v0.3 §7 rule

## [2026-05-07] gaps | discovered via query
- RAG — implicit-concept threshold met (referenced in 2+ pages, no page exists)
- agent memory — referenced in ai-agent.md, no concept page; long-term/vector-DB side entirely unreferenced
- context window management strategies — referenced in context-engineering.md as "what to include/compress/drop", no page
- LangSmith — mentioned alongside LangGraph in source, no entity page or cross-reference (low priority)

## [2026-05-07] query | tool calling and context engineering
- synthesis filed: wiki/ai-engineering/tool-calling-and-context-engineering.md
- cross-links added to: ai-agent.md, context-engineering.md, tool-calling.md
- 4 gaps logged above

## [2026-05-07 04] ingest | Disasters I've Seen in a Microservices World
- source: raw/notes/Disasters in a Microservices World.md
- domain: software-architecture (provisional)
- pages touched: software-architecture/README.md (new — hub), software-architecture/microservices.md (new), software-architecture/distributed-systems-fallacies.md (new)
- new pages: 3
- notes: first ingest into provisional software-architecture domain; hub created; no source-summary (~600 words, article note — below §8.1 threshold); source tagged data-engineering and observability but body is entirely about distributed systems architecture — DE tag treated as noise, routing override logged; no DE cross-references made (observability mention is generic, not pipeline-specific); eventual-consistency folded into microservices.md rather than stubbed separately (source signal too thin for standalone page); raw/_inbox/ now empty

## [2026-05-07 03] ingest | SCD2 Table Creation with MERGE INTO in Spark and Iceberg
- source: raw/notes/scd2-table-creation-merge-into-spark-iceberg.md
- domain: data-engineering (provisional)
- pages touched: data-engineering/README.md (new — hub), data-engineering/scd2.md (new), data-engineering/merge-into.md (new), data-engineering/apache-iceberg.md (new)
- new pages: 4
- notes: first ingest into provisional data-engineering domain; hub created; no source-summary (~400 words prose, tutorial article — below §8.1 threshold); Apache Spark not stubbed — too thin signal from this source; 6 connections in source noted on pages as not-yet-ingested

## [2026-05-07 02] ingest | AI Agents - Complete Course Beginner to Pro
- source: raw/notes/AI Agents - Complete Course Beginner to Pro.md
- domain: ai-engineering
- pages touched: context-engineering.md (updated, +1 source), ai-agent.md (new), multi-agent-systems.md (new), tool-calling.md (new), langgraph.md (new), README.md (updated)
- new pages: 4 (ai-agent, multi-agent-systems, tool-calling, langgraph)
- notes: context-engineering.md updated with 4-component breakdown and two citable claims from this source — entity dedup handled correctly; inbox duplicate moved to raw/notes/ (file was copied from Study Notes directly into raw/notes/, inbox copy was redundant)

## [2026-05-07] schema | v0.4 — formalize `provisional` frontmatter field
- §4: documented `provisional` as optional field on hub pages
- rationale: field was being used in practice on data-engineering hub but undocumented; close the gap before more domains adopt it

## [2026-05-07] schema | v0.3 — unsourced claim guidance + raw/notes/ channel
- §7: added paragraph preferring wiki links over unsourced claims; wiki compresses sources, does not invent
- §2: added raw/notes/ to architecture listing
- §10.4: new subsection for first-party PARA vault notes; higher trust signal than web clippings
- retroactive: Context Engineering source moved raw/web/ → raw/notes/; all citations updated

## [2026-05-20] schema | v0.5 — PARA-native ingest + source stamping

- §1: "never modify raw sources" narrowed to allow three-field stamp only
- §2: narrow write exception documented; PARA-native paths layer added (points to wiki/_config.md); raw/notes/ semantics clarified (edge-case / legacy); wiki/_config.md added to wiki/ structure listing
- §4: sources: field changed from flat string to structured object (path, channel, ingested_at, ingested_sha); migration note added
- §6: citation format extended — PARA-native sources cite via Obsidian wikilink; raw-channel sources use relative markdown link; consistency rule added
- §8.1: ingest branched by source location (A: inbox, B: PARA-native, C: raw-channel); stamp step added as step 9; move step demoted to branch-specific step 10; log entry format updated (+channel field)
- §9: PARA-native collision rule added — wiki_ingested check before re-ingest, three options (skip/force-update/append-only), both re-ingest modes update wiki_ingested_at
- §13: three new failure mode lines covering stamp-field abuse and silent re-ingest
- new file: wiki/_config.md — PARA-native paths (03_Resources/Articles/, 03_Resources/Study Notes/), stamp field spec, channel reference table
- rationale: eliminate duplication between raw/<channel>/ and PARA folders for files with a canonical PARA home
- lint-correction: Phase 2 lint surfaced 8 issues against the initial v0.5 draft; fixes for items 1–6, 8 applied as part of the same schema bump. Item 7 (§9 collision rule placement) deferred — known organizational cleanup for future version.
- Phase 2b re-lint surfaced 2 cosmetic findings (§10.2 timestamp path format, §1 cross-reference wording); both fixed for consistency.

## [2026-05-20] schema | migration — raw/notes/ → PARA-native cite-in-place

- retroactive stamps: wiki_ingested_at set to 2026-05-07 (original log ingest date) for all 4 sources
- sources migrated:
  - Context Engineering (Articles/) → wiki/ai-engineering/context-engineering.md
  - Disasters in a Microservices World (Articles/) → wiki/software-architecture/microservices.md, distributed-systems-fallacies.md
  - scd2-table-creation-merge-into-spark-iceberg (Articles/) → wiki/data-engineering/apache-iceberg.md, merge-into.md, scd2.md
  - AI Agents - Complete Course Beginner to Pro (Study Notes/) → wiki/ai-engineering/multi-agent-systems.md, ai-agent.md, tool-calling.md, langgraph.md, context-engineering.md (as src2)
- per-source actions: PARA twin stamped (3 fields); wiki sources: fields migrated to v0.5 structured form; footnote citations changed from raw/ markdown links to PARA-native wikilinks; raw/notes/ copies deleted
- plan correction: AI Agents PARA twin was found in Study Notes/, not Articles/ as predicted by the pre-execution migration plan. Study Notes/ is the correct canonical location (YouTube course study note, not article clip). Both paths are PARA-native per _config.md, so no schema implication.
- raw/notes/ directory is now empty; retained for future edge-case use per CLAUDE.md §10.4

## [2026-05-21 B5] ingest | Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns
- source: 03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md
- channel: notes (PARA-native, Branch B)
- domain: data-engineering
- pages touched: wiki/data-engineering/idempotent-pipelines.md (new — pre-committed), wiki/data-engineering/dimensional-modeling.md (new — pre-committed), wiki/data-engineering/scd2.md (updated, +1 source, 9999-12-31 sentinel + "when to skip SCD" section added), wiki/data-engineering/README.md (updated)
- new pages: 2 (idempotent-pipelines, dimensional-modeling)
- notes: 78-min lecture, synthetically rich. Both pre-commitments fulfilled. Cumulative table design judgment: source does not present cumulative tables as a standalone concept — it uses cumulative SUM as a SQL window function technique within SCD2 construction (streak_identifier). Folded into dimensional-modeling.md rather than a separate page. Airflow `depends_on_past` mentioned; not stubbed — thin signal from this source alone.

## [2026-05-21 B4] ingest | Data Lake Fundamentals - Apache Iceberg and Parquet
- source: 03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md
- channel: notes (PARA-native, Branch B)
- domain: data-engineering
- pages touched: wiki/data-engineering/parquet.md (new — pre-committed), wiki/data-engineering/apache-iceberg.md (updated, +1 source, stub→draft), wiki/data-engineering/data-lake.md (new), wiki/data-engineering/README.md (updated)
- new pages: 2 (parquet, data-lake)
- notes: 59-min video with strong technical depth; prose ~800 words + SQL examples. Below strict source-summary word threshold but synthetically rich — concepts extracted into parquet.md and data-lake.md instead. Pre-commitment fulfilled: parquet.md and apache-iceberg.md are distinct pages (file format vs table format distinction explicitly stated in both). Delta Lake and Hudi mentioned as Iceberg alternatives; not stubbed — single-source, thin signal.

## [2026-05-21 B3] ingest | dbt Data Architecture - Simple Stack Design
- source: 03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design.md
- channel: notes (PARA-native, Branch B)
- domain: data-engineering
- pages touched: wiki/data-engineering/dbt.md (new), wiki/data-engineering/pipeline-layers.md (new), wiki/data-engineering/README.md (updated)
- new pages: 2 (dbt, pipeline-layers)
- notes: 9-min tutorial (~500 words); below source-summary threshold. Pipeline-layers extracted as a separate concept page because the staging/warehouse/marts pattern generalizes beyond dbt. Snowflake mentioned as example warehouse but not stubbed — single-source, thin signal.

## [2026-05-21 B2] ingest | Kafka Tutorial for Beginners - Core Concepts
- source: 03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts.md
- channel: notes (PARA-native, Branch B)
- domain: data-engineering
- pages touched: wiki/data-engineering/kafka.md (new), wiki/data-engineering/README.md (updated)
- new pages: 1 (kafka)
- notes: 18-min tutorial (~600 words); below source-summary threshold (tutorial, not synthesis). ZooKeeper, KRaFt, Kafka Streams mentioned; folded into kafka.md — too thin for standalone entity pages from this source alone.

## [2026-05-21 B1] ingest | Data Engineering - Just Use Postgres
- source: 03_Resources/Study Notes/Data Engineering - Just Use Postgres.md
- channel: notes (PARA-native, Branch B)
- domain: data-engineering
- pages touched: wiki/data-engineering/postgres.md (new), wiki/data-engineering/README.md (updated)
- new pages: 1 (postgres)
- notes: 3-min clip (~200 words); well below source-summary threshold. pgvector cross-link to ai-engineering/vector-database added. Neon hosting mentioned but not stubbed — single-source, thin signal.

## [2026-05-21 05] ingest | Claude Code - Solving the Memory Problem with Context Engineering
- source: 03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering.md
- channel: notes (PARA-native, Branch B)
- domain: ai-engineering
- pages touched: wiki/ai-engineering/context-window-management.md (new — pre-committed), wiki/ai-engineering/agent-memory.md (updated, +1 source; CLAUDE.md-as-long-term-memory framing added; status upgraded stub→draft), wiki/ai-engineering/context-engineering.md (updated, +1 source; CLAUDE.md note + cross-links to context-window-management and agent-memory), wiki/ai-engineering/README.md (updated)
- new pages: 1 (context-window-management)
- notes: pre-commitment fulfilled — context-window-management.md created (distinct from context-engineering.md; covers operational strategies). agent-memory.md now has 2 sources. Source is 15-min tutorial (~500 words); below source-summary threshold. Agent OS product mentioned but not stubbed — insufficient signal for standalone entity page. Sub-agent token savings figures (3,500/7,000/9,000) cited directly in context-window-management.md.

## [2026-05-21 04] ingest | AI Dev - Agentic AI Architecture Explained
- source: 03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained.md
- channel: notes (PARA-native, Branch B)
- domain: ai-engineering
- pages touched: wiki/ai-engineering/agent-memory.md (new), wiki/ai-engineering/mcp.md (new), wiki/ai-engineering/ai-agent.md (updated, +1 source + 4-step loop enrichment), wiki/ai-engineering/multi-agent-systems.md (MCP cross-link added), wiki/ai-engineering/README.md (updated)
- new pages: 2 (agent-memory, mcp)
- notes: source is an 8-min explainer (~400 words); below source-summary threshold. agent-memory.md created now — pre-commitment specifies File 5 must produce it; File 5 will update (+1 source). MCP stub created; unsourced claim about Anthropic origin of MCP marked [unsourced]. CrewAI and AutoGen orchestration frameworks mentioned but not stubbed — single-source, thin signal.

## [2026-05-21 03] ingest | AI - How Large Language Models Work
- source: 03_Resources/Study Notes/AI - How Large Language Models Work.md
- channel: notes (PARA-native, Branch B)
- domain: ai-engineering
- pages touched: wiki/ai-engineering/llm.md (new), wiki/ai-engineering/transformer.md (new), wiki/ai-engineering/README.md (updated)
- new pages: 2 (llm, transformer)
- notes: source is 3Blue1Brown 7-min explainer (~400 words); below source-summary threshold. Created foundational pages for LLM and Transformer — both were referenced throughout the wiki without their own pages. RLHF, backpropagation, attention each have thin single-source signal; folded into llm.md and transformer.md rather than stubbing separately.

## [2026-05-21 02] ingest | AI Tools - Local RAG Complete Tutorial
- source: 03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial.md
- channel: notes (PARA-native, Branch B)
- domain: ai-engineering
- pages touched: wiki/ai-engineering/rag.md (new), wiki/ai-engineering/context-engineering.md (cross-link added), wiki/ai-engineering/README.md (updated)
- new pages: 1 (rag)
- notes: source is a 15-min tutorial (~600 words prose); below §8.1 source-summary threshold. Gap from 2026-05-07 log (RAG — implicit-concept threshold met) now closed. ChromaDB, Pinecone, pgvector, Ollama, Sentence-Transformers mentioned but not stubbed — single-source signal too thin for standalone entity pages; noted in rag.md.

## [2026-05-21 01] ingest | LangSmith - Debugging and Evaluating AI Agents
- source: 03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md
- channel: notes (PARA-native, Branch B)
- domain: ai-engineering
- pages touched: wiki/ai-engineering/langsmith.md (new), wiki/ai-engineering/agent-evaluation.md (new), wiki/ai-engineering/ai-agent.md (updated, +1 source), wiki/ai-engineering/README.md (updated)
- new pages: 2 (langsmith, agent-evaluation)
- notes: source is synthetically rich (agent engineering flywheel, online/offline eval patterns, golden datasets, debugging workflow); source-summary not written — concepts extracted into dedicated pages cover the material more usefully. Gap from 2026-05-07 log (LangSmith entity missing) now closed. Thread-level evaluation finding (context growth degrades agents) added to ai-agent.md evaluation section as [^src2].

## [2026-05-20] schema | gap noted — synthesis pages have no first-class sources model

- observation: filed-back synthesis pages (per §8.2) cite other wiki pages, not raw sources, so `sources:` is structurally inapplicable. Current workaround: `sources: []` on tool-calling-and-context-engineering.md.
- candidate v0.6 amendment: introduce a `derived_from:` field on type=synthesis pages, listing the wiki pages they synthesize. Either alongside or instead of `sources:`. Deferred — not in scope for v0.5 data migration.
- addendum (2026-05-21): `vector-database.md` created as a sources-less concept stub (lint item F3; backed by rag.md, agent-memory.md, context-window-management.md). The `derived_from:` v0.6 amendment would also cover this pattern — concept pages backed by multiple wiki pages rather than a primary source, not just synthesis pages.

## [2026-05-21 C5] ingest | DevOps - Kubernetes Complete Course for Beginners
- source: 03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md
- channel: notes (PARA-native, Branch B)
- domain: software-architecture
- pages touched: wiki/software-architecture/kubernetes.md (new), wiki/software-architecture/microservices.md (cross-links added), wiki/software-architecture/README.md (updated)
- new pages: 1 (kubernetes); Helm, StatefulSet, Docker folded into kubernetes.md — source presents them as components, not standalone subjects
- notes: 216-min course; note ~400 words below source-summary threshold. kubernetes.md cross-links to microservices.md, distributed-systems-fallacies.md, and software-design-principles.md — satisfies graduation criterion (b). Microservices.md also updated with kubernetes back-link + software-design-principles link.

## [2026-05-21 C4] ingest | SQL - Window Functions Reference
- source: 03_Resources/Study Notes/SQL - Window Functions Reference.md
- channel: notes (PARA-native, Branch B)
- domain: data-engineering (routing override from batch assignment: source tags data-engineering explicitly; LAG/SUM OVER used in dimensional-modeling.md streak_identifier pattern; no SQL signal in software-architecture domain)
- pages touched: wiki/data-engineering/sql-window-functions.md (new), wiki/data-engineering/dimensional-modeling.md (cross-link added), wiki/data-engineering/README.md (updated)
- new pages: 1 (sql-window-functions)
- notes: 17-min reference video (~350 words); below source-summary threshold. Cross-link to dimensional-modeling.md adds reverse link from the streak_identifier consumer to the window function source.

## [2026-05-21 C3] ingest | Python - FastAPI Complete Course with Auth and Database
- source: 03_Resources/Study Notes/Python - FastAPI Complete Course with Auth and Database.md
- channel: notes (PARA-native, Branch B)
- domain: software-architecture
- pages touched: wiki/software-architecture/fastapi.md (new), wiki/software-architecture/README.md (updated)
- new pages: 1 (fastapi); auth and DB patterns folded in — source treats them as FastAPI features, not standalone concepts
- notes: 125-min course; note is ~300 words below source-summary threshold. First shared vocabulary between Batch 3 pages: Depends() == dependency injection from software-design-principles.md; cross-link added.

## [2026-05-21 C2] ingest | Data Structures and Big O Notation Explained
- source: 03_Resources/Study Notes/Data Structures and Big O Notation Explained.md
- channel: notes (PARA-native, Branch B)
- domain: software-architecture (routing note: CS fundamentals — weakest fit among options; no existing domain is cleaner)
- pages touched: wiki/software-architecture/data-structures.md (new), wiki/software-architecture/README.md (updated)
- new pages: 1 (data-structures)
- notes: 16-min tutorial (~350 words + time-complexity table); below source-summary threshold. Coherence flag: data-structures.md does not cross-link to microservices.md or distributed-systems-fallacies.md — connects only to software-design-principles.md via encapsulation. This page sits in a different sub-cluster from the distributed-systems pages; domain rename signal beginning to emerge.

## [2026-05-21] domain | data-engineering graduates from provisional after Batch 2 ingest

- 12 pages, 6 sources — well above the 3-source graduation threshold
- All pages draft status; zero orphans; zero contradictions
- provisional: true removed from README.md; _domains.md updated with graduation date and rationale
- Original lint review date (2026-06-06) superseded by early graduation

## [2026-05-21 C1] ingest | Python - Production Code Principles Senior Developer
- source: 03_Resources/Study Notes/Python - Production Code Principles Senior Developer.md
- channel: notes (PARA-native, Branch B)
- domain: software-architecture
- pages touched: wiki/software-architecture/software-design-principles.md (new), wiki/software-architecture/README.md (updated)
- new pages: 1 (software-design-principles)
- notes: 29-min tutorial (~400 words); below source-summary threshold. 8 principles extracted into one concept page — SRP, cohesion, loose coupling, dependency injection, open/closed, portability, defensibility, simplicity. Cross-linked to microservices.md (service-level application of same principles). No alias overlap with existing software-architecture pages; clustering signal is conceptual bridge rather than shared vocabulary.

## [2026-05-21] lint | Apache Spark concept deferred

- Apache Spark referenced in 5 content pages (apache-iceberg.md, merge-into.md, scd2.md, dimensional-modeling.md, README.md) — hits 3-page implicit-concept threshold
- All references are contextual mentions ("Spark SQL", "Spark MERGE INTO"), not substantive coverage of Spark as a subject
- Stub creation deferred; revisit when a Spark-primary source ingests

## [2026-05-22] domain | rename | software-architecture → software-engineering

- mechanics: directory mv wiki/software-architecture/ → wiki/software-engineering/; 64-reference sweep via sed across 7 wiki page frontmatter (domain: + tags:), 28 wikilinks in wiki content, 15 _index.md entries, 1 _domains.md section header, 6 PARA twin wiki_pages: stamp paths
- historical _log.md entries (lines C1–C5 ingest records, B5 migration record) preserved unchanged — references to old slug remain in historical record by design
- rationale: post-Batch-3 domain scope (CS fundamentals → code design → API patterns → distributed systems → container orchestration) accurately described as software engineering, not architecture
- graduation applied simultaneously: provisional → standard (5 sources, ≥3 threshold; same criteria as data-engineering); distributed-systems-fallacies stub expansion committed for next session
- precedent note: §9 lists create/merge/split but not rename; this is the first rename operation. Mechanics: (1) mv directory, (2) sed sweep all live references, (3) preserve _log.md historical entries, (4) update _domains.md section + decision log, (5) update README hub text. §9 amendment deferred — single occurrence, not pattern.

## [2026-05-22] stub-expansion | distributed-systems-fallacies

- page: wiki/software-engineering/distributed-systems-fallacies.md
- status: stub → draft (fulfils commitment logged at 2026-05-22 graduation)
- no new primary sources; expansion drawn from existing wiki cross-references:
  - microservices.md (src1: Disasters in a Microservices World) — fallacies 1+2 (network reliability, latency): failure modes, resilience planning, eventual consistency
  - kubernetes.md (src2: DevOps - Kubernetes Complete Course) — fallacy 4 (Secrets not encrypted by default), fallacy 5 (ephemeral pod IPs → Service stable endpoints)
- src2 added to sources: frontmatter (content derives from it via kubernetes.md cross-reference)
- fallacies 3, 6, 7, 8 listed in structural table [unsourced]; no ingested source covers them — noted explicitly, awaiting dedicated source
- cross-links added both directions: distributed-systems-fallacies.md → microservices.md, kubernetes.md, software-design-principles.md; inbound links already present from all three pages

## [2026-05-22] lint | ai-engineering/langgraph.md stub deferred

- ai-engineering/langgraph.md — stub aged past 14 days as of 2026-05-22. Deferred pending LangGraph-primary source ingest. Pattern matches Apache Spark deferral.

## [2026-05-25] schema | rename: wiki → Corpus

Project renamed from "wiki" to "Corpus" across the entire working tree and PARA-native source frontmatter.
- Directory `wiki/` renamed to `corpus/` via `git mv` (history preserved).
- All in-tree references updated case-preservingly: `wiki`/`Wiki` → `corpus`/`Corpus`.
- corpus/_log.md H1 updated: `# Wiki Log` → `# Corpus Log` (line 1 only; historical entries below unchanged).
- Frontmatter stamp fields renamed in 19 PARA-native source files: `wiki_ingested` → `corpus_ingested`, `wiki_ingested_at` → `corpus_ingested_at`, `wiki_pages` → `corpus_pages`; path values updated `wiki/<domain>/<slug>.md` → `corpus/<domain>/<slug>.md`.
- Schema version unchanged at v0.5. Rename is terminology only; no semantic changes.
- Obsidian feature term "wikilink" / "wikilinks" left intact (§2a class i).
- Karpathy's "LLM-Wiki pattern" left intact as external proper noun (§2a class ii).
- CLAUDE.md line 3: "built on" → "inspired by" (correction applied during rename).
- New `corpus/_about.md` created: long-form rationale for the five subtitle concepts (Personal, Knowledge corpus, Citation discipline, Schema versioning, Synthesis-aware structure).
- README.md given new intro section (§7): replaces title + attribution with `# Corpus` block; body lines 4+ updated via §2 substitutions.
- Historical log entries above (lines 36–269) retain `wiki/` paths as period-accurate records. Forward references use `corpus/`.

Out of scope for this commit (deferred):
- `llm-wiki-system/` parent folder rename
- `.claude/settings.local.json` allow-list path updates
- Git remote rename
- Commit history rewrite
