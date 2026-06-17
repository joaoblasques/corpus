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

## [2026-06-09 13:58] domain | create: mlops (provisional)

- New provisional domain `mlops` created under §9 provisional rule. User confirmed via Batch 4 inbox survey + new-domain question.
- Rationale: 4 inbox sources (AIEFS Phase 00 lessons 01/02/03 + IaC/Terraform article) fit no existing content domain; coherent "engineering substrate / infra & tooling" cluster (environment, version control, compute, IaC).
- provisional: true — retained one cycle because 3 of 4 seed sources share a single origin (one course). 30-day review: 2026-07-09.
- Hub created: corpus/mlops/README.md. _domains.md section + decision-log entry added.

## [2026-06-09 13:58] ingest | Dev Environment — The Four-Layer Stack (AIEFS Phase 00 / 01)

- source: raw/notes/00-01-dev-environment-kb.md
- channel: notes (first-party course KB; Branch A inbox → moved to raw/notes/)
- domain: mlops
- new pages: mlops/dev-environment-stack.md (concept), mlops/uv.md (entity, stub)
- notes: four-layer stack, venv invariant, checks-as-data verify pattern, CUDA-wheel pitfall. uv flagged for expansion when a uv-primary source arrives.

## [2026-06-09 13:58] ingest | Git & Collaboration (AIEFS Phase 00 / 02)

- source: raw/notes/00-02-git-and-collaboration-kb.md
- channel: notes (Branch A inbox → raw/notes/)
- domain: mlops
- new pages: mlops/git.md (entity)
- notes: content-addressed model, branch-per-task workflow, ML-aware .gitignore, DVC/LFS forward-ref (data-management source not yet ingested).

## [2026-06-09 13:58] ingest | GPU Setup and Cloud Options (AIEFS Phase 00 / 03)

- source: raw/notes/00-03-gpu-setup-and-cloud-kb.md
- channel: notes (Branch A inbox → raw/notes/)
- domain: mlops
- new pages: mlops/gpu-and-vram.md (concept), mlops/cloud-gpu-providers.md (concept)
- notes: fp16 VRAM math, training≈6×inference, LoRA (forward-ref to fine-tuning phase), provider pricing snapshot (May 2026, marked drift-prone).

## [2026-06-09 13:58] ingest | How AI agents & Claude skills work (Clearly Explained)

- source: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
- channel: youtube (Branch A inbox → raw/youtube/)
- domain: ai-engineering
- new pages: ai-engineering/agent-skills.md (concept), ai-engineering/sources/how-ai-agents-and-skills-work.md (source summary — substantive 8k-word opinionated talk)
- pages touched: context-window-management.md, context-engineering.md, ai-agent.md, multi-agent-systems.md (+1 source each)
- notes: opinionated practitioner stance (Ras Mic). agent-skills page + context-engineering update flag the tension with corpus sources that treat CLAUDE.md as valuable long-term memory — not presented as settled fact.

## [2026-06-09 13:58] ingest | IaC fundamentals for data engineers

- source: raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md
- channel: web (Branch A inbox → raw/web/)
- domain: mlops
- new pages: mlops/infrastructure-as-code.md (concept), mlops/terraform.md (entity)
- notes: startdataengineering.com (Joseph Machado). Tutorial → no source-summary page (§8.1 step 6 exclusion); concept + entity pages capture it. Cross-linked to data-engineering (provisions S3/EC2/EMR).

## [2026-06-09 14:10] query | how to optimize my Claude setup for efficiency & productivity

- query answered from corpus pages: agent-skills, context-window-management, context-engineering, multi-agent-systems, ai-agent.
- synthesis filed back (user-approved): ai-engineering/optimizing-claude.md (synthesis, sources: [] — derives from corpus pages; provenance transitive).
- gaps surfaced: (1) Claude Code mechanics (slash commands, hooks, settings.json, MCP) lightly covered; (2) no official Anthropic/Claude Code docs ingested; (3) no record of user's actual setup. Logged as highest-leverage next sources to deepen the "Claude" cluster.
- context: executed as sub-project A of the corpus-direction brainstorm (validate the consumption half of the loop). A closed; consumption loop proven end-to-end.
- v0.6 note: this synthesis page is another instance motivating the draft derived_from: field (internal provenance currently expressed only in prose + inline wikilinks).

## [2026-06-09] config | add email channel

- Added `email` channel → `raw/email/` to corpus/_config.md (channel-labels table + email-collection note).
- Created raw/email/ (with .gitkeep).
- Supports the /collect-email collector (sub-project B): captures starred Gmail into raw/_inbox/ (channel email), routed to raw/email/ by Branch A ingest.

## [2026-06-11] schema | v0.5 → v0.6 — optimized batch-ingest pipeline + claim lifecycle

- §8.1 batch path (N>10) rewritten as the cluster-based Phase 0–5 pipeline (pre-flight → survey/cluster → global entity registry → per-cluster ingest → integrate → verify); added the Coordinator-owns-shared-files rule for parallel per-domain workers.
- §4 + new §7.1: v2 claim-lifecycle fields/conventions (`confidence`, `last_confirmed`, `supersedes`/`superseded_by`, contradiction-on-write, typed relationships).
- Grounded in deep research filed at docs/research/2026-06-11-llm-wiki-ingest-best-practices.md (Karpathy LLM-wiki + rohitg00 v2; MOC/Zettelkasten/PARA; large-batch entity-resolution & orchestration).
- Motivation: ingest the 136-source collected backlog (sub-project B output) without structural drift. Pipeline executes immediately after this entry.

## [2026-06-11] ingest | email-backlog wave 1 — data-engineering cluster

- pipeline: v0.6 optimized batch (Phase 0–5), Coordinator + 5 parallel per-batch workers.
- sources: 65 data-engineering sources surveyed → 48 consumed, 17 skipped (promo/digest/stub/Amazon book pages).
- channels: 15 emails (moved raw/_inbox → raw/email, stamped), 33 web captures (stamped in place).
- new pages (13): apache-spark, databricks, duckdb, data-orchestration, open-table-formats, medallion-architecture, change-data-capture, materialized-views, data-quality, query-engine-routing, data-engineer-role, claude-code-for-data-engineering, ai-observability-data-pipeline.
- updated pages (6): dbt (+7 src), dimensional-modeling, scd2, apache-iceberg, data-lake, pipeline-layers.
- source summaries (2): sources/dbt-kimball-project, sources/aws-duckdb-etl-fargate.
- cross-domain (DE-primary, link from ai-engineering later): claude-code-for-data-engineering, ai-observability-data-pipeline.
- notes: data-diff flagged deprecated; CDC page has an [unsourced] marker where the captured email excerpt was truncated; vendor benchmark figures (Databricks/Greybeam) marked vendor-reported. Remaining inbox: 121 sources (ai-engineering + other clusters) for future waves.

## [2026-06-12] ingest | email-backlog wave 2 — ai-engineering cluster

- pipeline: v0.6 optimized batch (Phase 0–5), Coordinator + 6 parallel per-batch workers; planner-led survey/registry first.
- sources: 121 ai-engineering sources surveyed → 96 consumed, ~25 skipped (promo/event/login-stub/off-cluster model cards).
- channels: 27 emails (moved raw/_inbox → raw/email, stamped), 69 web captures (stamped in place).
- domain decision (§9): kept all in ai-engineering (no new domain); added two sub-hubs — agentic-coding (synthesis) and claude-cowork (entity). User-confirmed.
- new ai-engineering pages (13): agent-harness, agentic-coding (sub-hub), claude-code, claude-cowork (sub-hub), anthropic, claude-api, prompt-engineering, agent-security, structured-outputs, agentic-search, agent-testing, claude-md-conventions, agent-ui.
- updated ai-engineering pages (7): agent-skills, mcp (stub→draft), rag, agent-memory, vector-database (stub→draft), agent-evaluation, ai-agent.
- cross-domain (B6, data-engineering-primary): NEW agentic-data-modeling; UPDATED claude-code-for-data-engineering (+6 src). Linked to ai-engineering/claude-code.
- dedup: model releases (Opus 4.8, Fable 5, Mythos 5) kept as sections in anthropic, not separate pages; pi-coding-agent (×3), playwright-testing (×2), cowork (×2), zazencodes-skills (×2) deduped to single pages.
- notes: prompt-engineering kept distinct from context-engineering; grep-vs-vector handled as a section in agentic-search (not a synthesis); a few [unsourced] markers where captured pages were JS-gated/login stubs. ai-engineering now ~38 pages (sub-hubs justified, no split). Remaining inbox: 94 sources (software/mlops/productivity/etc.) for future waves.

## [2026-06-12] ingest | email-backlog wave 3 — distinct clusters (SE + productivity + ai-business)

- pipeline: v0.6 optimized batch, Coordinator + 4 parallel per-cluster workers (disjoint domains).
- scope correction: 342 sources remain un-ingested (not 94); the large DE/AI tail deferred. Wave 3 took the 42 distinct-cluster sources.
- domains: NEW provisional `productivity` and `ai-business` created (§9; ai-business supersedes the 2026-05-07 career rejection). software-engineering topped up; security folded into ai-engineering.
- new pages (13): software-engineering — cap-theorem, ai-assisted-development, ai-risk-architecture, engineering-craft, developer-tooling; productivity — mental-models, learning-to-learn, shipping-and-scope, working-with-stakeholders, ai-augmented-knowledge-work; ai-business — technical-career, monetizing-code, ai-and-the-job-market.
- updated (2): software-design-principles (design-patterns section), ai-engineering/agent-security (offensive AppSec / LLMs-finding-vulns).
- skipped: promo/sponsored newsletters (Hermes, declutter/Google Tips, Fathom), empty landing pages (50-hacks, cowork academy), Instagram/SSD exploit news. 3 mis-bucketed sources (Claude /goal, DIP tutorial, Kafka HOL-blocking) flagged for ai-engineering/software-engineering/data-engineering in later waves.
- corpus now 92 pages across 6 domains. Remaining inbox: 71 sources (mostly DE/AI tail + a few mlops) for future waves.

## [2026-06-12] ingest | email-backlog wave 4 — data-engineering + ai-engineering tail top-up

- pipeline: v0.6 batch, 2 parallel per-domain workers (disjoint domains). Pure top-up — no new domains.
- scope: the clean DE tail (24) + AI tail (29) the wave-1/2 keyword nets missed; ~21 sources consumed, the rest skipped as duplicate email/web pairs, newsletter digests, event/book promos. A messy ~250-source "other" bucket (mostly more dupes/digests + mis-keyworded DE/AI) remains deferred.
- new pages (4): data-engineering — data-ingestion-patterns, incremental-pipeline-design; ai-engineering — learning-ai-engineering (synthesis), web-scraping (stub).
- updated (10): data-engineering — kafka (+share-groups/HOL-blocking), materialized-views (+IVM/DBSP), scd2 (+part-2 datestamping), idempotent-pipelines (+functional DE); ai-engineering — agent-skills, multi-agent-systems (+Grab/GenAI_Agents), context-engineering (+ktx), llm (+DiffusionGemma/Command-A), claude-code (+2.1.139), ai-agent (+agent-mode/ApplyPilot).
- corpus now ~96 pages, 6 domains. Diminishing returns flagged: remaining backlog is largely duplicates/digests of already-covered topics.

## [2026-06-12] schema | v0.6 → v0.7 — collect-obsidian vault-removal exception

- §2 vault-removal exception (the collect-obsidian reaper may delete a vault source after its raw copy is `corpus_ingested`; gated, git-recoverable, never auto-commits); §13 failure-mode bullet; §15 version entry; `_config.md` vault_root + scope.
- Enables the third collector (`collect-obsidian`): copy reference-layer vault notes to raw/_inbox, fetch URL-list links, ingest, then reap originals.

## [2026-06-12 16:30] schema | v0.8 — operationalized §8.2 /query
- §8.2 rewritten as the `/query` operation: LLM index-selection retrieval; read-only coverage gate; labelled web top-up (`[fresh — not yet in corpus]`) auto-queued to `raw/_inbox/` (channel `web`, `via_query`) deduped by `source_url`; gap logging; approval-gated synthesis file-back.
- backed by `.claude/skills/query/SKILL.md` + `bin/query.py` (web-source queue + gap log + CLI).
- config: added `via_query` provenance + `/query` intake note to `corpus/_config.md`.

## [2026-06-15] ingest | youtube + email batch — v0.6 cluster pipeline (4 parallel workers)

- trigger: user — "ingest what we have in the collected buckets" after the full collect-youtube run.
- collection: full `collect-youtube` run removed 27 videos, collected 1107 (but 1064 `blocked` by YouTube transcript rate-limiting + 16 `disabled`); only 30 transcripts came back `ok`. Blocked videos remain in their playlists (removal requires a transcript) — recoverable via a throttled re-collection later.
- scope: 93 ingestable sources (30 youtube-ok + 63 email); 73 routed to workers, 20 pre-skipped (spam/personal/PT-tax-health/promo + 2 off-topic Music Theory). The 1080 transcript-less youtube stubs left in raw/_inbox/.
- pipeline: v0.6 optimized batch (§8.1), Coordinator + 4 parallel per-domain workers (disjoint domains): data-engineering, ai-engineering, mlops, (software-engineering + productivity + ai-business). User confirmed cluster→domain map, cloud-certs→mlops, Music-Theory skip, and one coordinated parallel run.
- new pages (35): ai-engineering (10) — ai-fundamentals, machine-learning, neural-network, statistics-for-ml, ai-product-management, agentic-workflow, vibe-coding, agi, sources/cs50-ai-with-python, sources/internal-operating-system-claude-projects; data-engineering (12) — storage-fundamentals, data-engineering-best-practices, python-for-data-engineering, de-portfolio-projects, cicd-for-data-infrastructure, data-migration-at-scale, data-modeling-meaning, semantic-layer, ingestr, progressive-disclosure-analytics-agents, ai-impact-on-data-engineering, sources/sql-funnel-analysis-project; mlops (9) — cli-tools, terminal-and-shell, vs-code, linux-commands, python, cloud-computing-fundamentals, aws, azure, gcp; software-engineering (1) — algorithms; productivity (1) — obsidian-pkm; ai-business (2) — ai-spreadsheets, ai-job-search.
- updated (~19): ai-eng — learning-ai-engineering, prompt-engineering, agent-harness, agent-security, agent-memory, agentic-coding, agent-skills; DE — dbt, query-engine-routing, materialized-views, kafka, medallion-architecture; mlops — infrastructure-as-code, git; SE — data-structures; ai-business — ai-and-the-job-market; + 6 domain hub READMEs.
- sources ingested: 62 (27 youtube → raw/youtube/, 35 email → raw/email/; many email pointers cited their fetched raw/web/ articles). All stamped corpus_ingested 2026-06-15.
- skipped at citation gate (9): emails that were pure promo / no-fetched-substance (self-serve-data-platform, aws-masterclass forward, learn-to-vibe-code, jupyter-ai, skill-recommendations, ai-knows-vs-does, ais-uneasy-promise [DE-owned], declutter-your-day) + ai-side-hustles youtube (1-line transcript).
- contradictions (in-page per §7.1): tmux-default-keybindings philosophy (cli-tools), "serverless" definition drift (cloud-computing-fundamentals), prompt-vs-context emphasis (learning-ai-engineering). None needed a standalone synthesis.
- verification: 35/35 new pages present; 0 orphans (all hub-linked); 0 cross-domain slug collisions; 0 broken citation paths (428 checked).
- corpus now 131 pages across 6 domains. mlops jumped to 17 pages / 16 new sources — strong graduation candidate at its 2026-07-09 provisional review.
- follow-up: 1064 blocked youtube stubs await a throttled re-collection; collector needs a tweak to re-fetch on `status: blocked` (it currently dedupes by video-id and would skip them as already-collected).


## [2026-06-15 23:14] ingest | ingest-auto safe pass (3 candidates: 2 ingested, 1 deferred)
- mode: interactive safe pass (Branch A, --max 3); oldest-3-by-mtime from raw/_inbox/
- ingested (2):
  - email-2026-06-10-joao-here-s-another-challenge-for-you.md (Tech With Tim) → software-engineering | pages: software-design-principles (updated, +Dependency Inversion Principle worked example: Notifier abstraction, inject concrete notifier) | moved to raw/email/
  - email-2026-06-09-post-call-admin-done-in-one-click.md (Return My Time) → ai-engineering | pages: claude-cowork (updated, +post-call-wrapup skill worked example: Drive/Notion/Gmail connectors, "never send, always draft", calibration-by-correction; operator note: Opus 4.8 now default across Max/Team/API) | moved to raw/email/
- deferred (1): email-2026-06-11-who-s-actually-in-charge-of-ai.md — UNCERTAIN (TDS newsletter digest; no extractable body, topics span multiple domains, real content in separately-fetched linked articles) → raw/_inbox/_REVIEW.md
- new pages: none (2 existing pages updated; +2 sources)
- domains touched: software-engineering, ai-engineering
- verify: no new pages → no orphans; no contradictions (both updates reinforce existing claims); _domains.md NOT modified (unattended-rule respected)
- notes: ingest-auto run; 2 processed, 1 deferred; ~1750 inbox items remain for future runs

## [2026-06-15T23:14] config | scheduled run
- collectors:
  - gmail: 82 collected · status=ok
  - obsidian: 560 collected · status=ok
  - youtube: 1 collected · status=ok
- ingest:
  - ingest: 0 ingested · 0 deferred · status=ok
- commit/push:
  - commit: status=push-failed · sha=417adf4 · error=git push exit 128: fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

## [2026-06-16T06:27] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 6 collected · status=ok
  - youtube: 0 collected · status=ok
- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=claude exit 1
- commit/push:
  - commit: status=nothing-to-commit

## [2026-06-16T07:15] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 2 collected · status=ok
  - youtube: 0 collected · status=ok
- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=claude exit 1
- commit/push:
  - commit: status=nothing-to-commit

## [2026-06-16T08:42] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 2 collected · status=ok
  - youtube: 0 collected · status=ok
- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=claude exit 1
- commit/push:
  - commit: status=committed · sha=9eac409

## [2026-06-16 09:10] ingest | Launching Boring UI
- source: raw/email/email-2026-05-28-launching-boring-ui.md
- channel: email
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/agent-ui.md, corpus/ai-engineering/agent-harness.md]
- new pages: []
- notes: ingest-auto run; 2 processed, 1 deferred. Launch announcement reinforces existing Boring UI coverage (GitHub repo already ingested into agent-ui); added author "why/boring" thesis + skill-sharing-platform vision to agent-ui, and Pi harness (Mario Zechner) attribution to agent-ui + agent-harness (typed link: Boring UI uses Pi). No duplicate Boring UI entity created.

## [2026-06-16 09:10] ingest | AI that knows things vs. AI that does things
- source: raw/email/email-2026-05-30-ai-that-knows-things-vs-ai-that-does-things.md
- channel: email
- domain: ai-business
- pages touched: [corpus/ai-business/monetizing-code.md]
- new pages: []
- notes: ingest-auto run; 2 processed, 1 deferred. Added "AI that does things / assessment as sales mechanism" section to monetizing-code (knows-vs-does distinction, assessment-as-pitch, pull-and-tune prebuilt skills, $0→$200→$1000 ladder). Promo framing flagged (AI Operator Academy course funnel). Same Return My Time sender as src3.

## [2026-06-16 09:10] ingest | ingest-auto deferral
- source: raw/_inbox/email-2026-06-02-instagram-exploit-spying-through-ssds-code-is-cheap.md
- channel: email
- domain: (deferred)
- pages touched: []
- new pages: []
- notes: DEFER UNCERTAIN — TLDR Dev digest spanning security side-channels (Instagram AI-bot exploit, SSD FROST tracking), Unix /proc/mem trivia, AI-coding opinion, D-lang game engine, OSINT tooling, recruiting, jujutsu VCS; no coherent single-domain fit, bulk maps to no existing domain. Linked articles already separate raw/web sources.

## [2026-06-16 16:40] lint | _REVIEW.md deferral-queue resolution (2 items)
- op: manual review pass over raw/_inbox/_REVIEW.md
- items: email-2026-06-11-who-s-actually-in-charge-of-ai.md; email-2026-06-08-como-por-a-ia-a-auditar-os-teus-gastos-sem-dar-cabo-da-tua-p.md
- decision: no corpus page — both are container emails (TDS newsletter digest of teaser blurbs + tracking links; one-line pointer email). No extractable body; fabricating pages would breach §7 provenance.
- disposition: stamped corpus_ingested:true / corpus_pages:[] and filed from raw/_inbox/ to raw/email/. Substantive content already captured as separate raw/web/ fetched sources (drain on their own ingest).
- queue: cleared (raw/_inbox/_REVIEW.md now empty).

## [2026-06-16 18:05] lint | full corpus audit (§8.3, 135 pages, 6 domains)
- scope: deterministic linter + 6 parallel per-domain judgment audits
- deterministic: 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs (clean)
- safe fix applied: removed duplicate `algorithms` alias from software-engineering/data-structures.md (canonical owner is algorithms.md)
- verified-false: agent "missing from README" claims for ai-product-management + 6 data-engineering syntheses — all slugs ARE present in their hubs (linter authoritative: 0 orphans)
- surfaced for approval (not auto-applied): topic-mixed splits (ai-engineering/anthropic.md model-lineup, software-engineering/developer-tooling.md xonsh/compiler-trick/InsForge); productivity shipping-and-scope vs working-with-stakeholders shared-tactic dedupe; implicit-concept pages (Ralph Loop, Lost-in-the-Middle, MoE; partition-pruning, metadata-layer); stale stubs needing source ingestion (langgraph 40d, microservices 40d, transformer, uv); ingestr stub→draft reclassification

## [2026-06-16 19:15] lint | apply approved fixes — split developer-tooling, reclassify ingestr
- split software-engineering/developer-tooling.md (3 unrelated topics) into:
  - xonsh.md (entity) — Python-superset shell [^src1 = email]
  - compiler-warning-management.md (concept) — Git's false_but_the_compiler_does_not_know_it_ trick [^src1 = web]
  - insforge.md (entity) — agent-operated backend platform [^src1 = web, 2 source files]
  content + citations moved verbatim; old page git-rm'd; inbound link in ai-assisted-development.md repointed to insforge; README + _index updated (Total pages 131→133)
- reclassified data-engineering/ingestr.md stub→draft (60-line entity with real content; stubs 6→5)
- deterministic lint after: 0 broken wikilinks · 0 broken citations · 0 orphans · 5 stubs (clean)

## [2026-06-16 20:55] lint | split anthropic.md → company + claude-models lineup
- split ai-engineering/anthropic.md (mixed company + full model lineup) into:
  - anthropic.md (entity) — kept: company, funding/valuation, learning resources (src1-4)
  - claude-models.md (entity, NEW) — model lineup table, Opus 4.8, Fable 5/Mythos 5, launch controversy (src4-9)
  footnote labels preserved across split to avoid transcription drift; bidirectional See-also links; README + _index updated (Total pages 133→134)
- deterministic lint after: 0 broken wikilinks · 0 broken citations · 0 orphans · 5 stubs (clean)

## [2026-06-16 21:05] lint | dedupe productivity shipping-and-scope ↔ working-with-stakeholders
- both pages restated the same email-2026-06-11 mechanics (feedback shift, "critical missing?" closing question, post-launch contract)
- shipping-and-scope.md owns the scoping mechanics; rewrote working-with-stakeholders.md "Manage the relationship after delivery" to delegate the shared tactics to it and keep only the relationship-specific trust framing (still cited to [^src2])
- no provenance lost (delegated mechanics fully cited in shipping-and-scope from the same source); lint clean

## [2026-06-16 21:20] ingest | How I use Hermes as a Lead Developer
- source: raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md
- channel: email
- domain: ai-engineering
- pages touched: [ai-engineering/README.md, ai-engineering/hermes.md, _index.md]
- new pages: [ai-engineering/hermes.md]
- notes: thin sponsored newsletter (video outline); created honest stub entity for the Hermes self-hosted coding agent (VPS/Docker, Telegram control, GitHub Actions deploy), fully cited; disambiguated from the React Native Hermes JS engine in agent-security.md. Stamped + moved source to raw/email/.

## [2026-06-16 21:45] ingest | web-backlog batch (8 sources, 3 parallel domain workers)
- context: ~25 substantive articles were fetched into raw/web/ via email link-following but never ingested (the inbox-only candidate selector never scans raw/web). Wave 1 of draining that backlog.
- method: v0.6 cluster batch ingest; Coordinator + 3 parallel per-domain workers (one writer per domain); new-page focus for quality control; Coordinator integrated shared files + lint-gate.
- ai-engineering (3 new): ralph-loop (fills the flagged "Ralph Loop" implicit-concept gap), long-running-agents, agent-cost-management
- data-engineering (3 new): data-mart, postgresql-views, etl-pipeline
- software-engineering (2 new): local-first-sync-architecture (Linear breakdown), test-case-reduction
- sources stamped (raw/web, corpus_ingested); domain hubs updated by workers; _index/_log by Coordinator. Total pages 135→143, sources 287→295.
- deterministic lint after: 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs (clean). Spot-checked ralph-loop (22 citations, dense per-claim provenance).
- deferred-updates noted by workers (NOT applied this wave): agent-harness + context-window-management could absorb long-running/cost specifics; claude-models has concrete Sonnet 4.6 pricing; postgres.md could cross-ref postgresql-views.

## [2026-06-16 22:05] ingest | web-backlog batch wave 2 (8 sources, 3 parallel domain workers)
- ai-engineering (3 new): sandcastle (entity), codegraph (entity), sources/grab-multi-agent-data-warehouse-support (source case study)
- data-engineering (3 new): redis (entity, 8.8 array type), mondaydb (entity, DuckDB HTAP), graph-databases (concept, RDF vs LPG)
- mlops (2 new): drift-detection (concept), python-built-in-functions (concept, complements python.md)
- Coordinator lint-gate caught + fixed 1 broken citation (sources/ page needs ../../../raw not ../../raw — depth bug); re-lint clean.
- sources stamped; hubs updated by workers; _index/_log by Coordinator. Total pages 143→151, sources 295→303.
- deterministic lint after: 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs (clean).

## [2026-06-16 22:20] ingest | web-backlog batch wave 3 (2 sources, 2 workers)
- ai-business (1 new): ai-economics-bubble (concept) — Zitron's GenAI unit-economics bear case; confidence 0.5 (opinion piece, attributed)
- data-engineering (1 new): pipeline-coding-patterns (concept) — Python code patterns for pipelines
- Coordinator enforced §7 one-verbatim-quote rule on pipeline-coding-patterns (paraphrased the 2nd quote). Total pages 151→153, sources 303→305. Lint clean.

## [2026-06-16 22:40] ingest | how-llms-actually-work → expand transformer + new MoE page
- source: raw/web/how-llms-actually-work.md (rich transformer-internals walkthrough)
- ai-engineering/transformer.md: EXPANDED stub→draft (preserved existing [^src1] study-note citation; added web source as [^src2]) — tokenization, embeddings, RoPE, attention (Q/K/V, softmax, causal masking, induction heads, n² cost), multi-head (GQA, KV cache), FFN (SwiGLU, ROME), residual stream+layernorm, next-token loop. Also fills the flagged lost-in-the-middle reference.
- ai-engineering/mixture-of-experts.md: NEW concept (fills flagged MoE implicit-concept gap) — Mixtral 8x7B router/experts.
- source stamped (→ 2 pages); README updated by worker; _index/_log by Coordinator. Total pages 153→154, sources 305→306. stubs 6→5.
- deterministic lint after: 0 broken wikilinks · 0 broken citations · 0 orphans · 5 stubs (clean).

## [2026-06-16 22:55] ingest | apache-parquet-for-data-engineers → enrich parquet.md
- source: raw/web/apache-parquet-for-data-engineers-optimized-data-storage.md (~5000-word internals deep-dive)
- data-engineering/parquet.md: ADDITIVE enrichment (preserved existing [^src1] study-note content; added web source [^src2]) — physical layout (row groups/column chunks/pages), encoding (dictionary), compression codecs, predicate pushdown via min/max stats, footer metadata, Dremel nested model, data types, limitations. Cross-linked query-engine-routing.
- Coordinator enforced §7 one-quote rule (removed a redundant 2nd quote). source stamped. sources 306→307; pages unchanged.
- deterministic lint after: 0 broken wikilinks · 0 broken citations · 0 orphans · 5 stubs (clean).

## [2026-06-17 09:00] ingest | Certified. (Ruben Hassid) → enrich anthropic.md
- source: raw/email/email-2026-05-06-certified.md
- channel: email
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/anthropic.md]
- new pages: []
- notes: ingest-auto run; 2 processed, 4 deferred. Filled the prior `[unsourced]` Skilljar note in the Learning-resources section with sourced content — Anthropic Academy (anthropic.skilljar.com) three free certs (Claude 101 / AI Fluency: Framework & Foundations [4Ds] / Intro to Claude Cowork); paid "Claude Certifications" flagged as non-endorsed scams; added career-signal angle (Stanford AI Index 78%; PwC ~56% AI-skill wage premium) cross-linked to ai-business/technical-career. Source stamped + moved to raw/email/.

## [2026-06-17 09:00] ingest | Day 7: You built the foundation (Jeff Su Cowork Toolkit) → enrich claude-cowork.md
- source: raw/email/email-2026-05-06-day-7-you-built-the-foundation-here-s-the-shortcut-to-the-re.md
- channel: email
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-cowork.md]
- new pages: []
- notes: ingest-auto run; 2 processed, 4 deferred. Capstone of the Cowork Toolkit 7-day arc (Day 7 recap); added the full Day 1→7 sequence and the canonical routing-conflict edge case (landlord email → Email HQ vs Housing). Largely promotional (Cowork Academy upsell) — extracted only the structural recap. Source stamped + moved to raw/email/.

## [2026-06-17 09:00] ingest | ingest-auto deferrals (4)
- DEFER UNCERTAIN: email-2026-06-02-instagram-exploit... (TLDR Dev digest — multi-topic, content in separate raw/web/ companions)
- DEFER UNCERTAIN: email-2026-05-21-ais-uneasy-promise... (TLDR Data digest — multi-topic, content in separate raw/web/ companions)
- DEFER G1: email-2026-05-15-parabens... (Decathlon PT discount-voucher promo — no domain fit)
- DEFER UNCERTAIN: email-2026-05-14-jonas-busy-declutter... (Google promo tips — no substantive claims; productivity fit too thin)
- notes: all 4 left in raw/_inbox/, unstamped, logged to raw/_inbox/_REVIEW.md.

## [2026-06-17T08:21] config | scheduled run
- collectors:
  - gmail: 6 collected · status=ok
  - obsidian: 3 collected · status=ok
  - youtube: 17 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 2 ingested · 4 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 5 stubs

## [2026-06-17 09:15] ingest | YouTube batch — 12 transcripts (v0.6 cluster pipeline, 4 parallel workers)
- sources: raw/youtube/{youtube-285hnxl9-rk, youtube-4bg64wnkfge, youtube-7jbcvxmj1bs, youtube-nhwp1btg0cw, youtube-qndigzfaufs, youtube-vstjydo88ka, youtube-we7bzvkbcvw, youtube-2wljl9a2cna, youtube-fkcfaapypuq, youtube-vtyx7ex-0ba, youtube-m8hcuiud9xo, youtube-n6t1kgxblqa}.md
- channel: youtube (all collected 2026-06-16 via the 08:00 scheduled run; reboot-interrupted session resumed)
- domains: data-engineering (6), ai-engineering (2), software-engineering (2), ai-business (2)
- new pages (7): data-engineering/dataform, data-engineering/snowflake, data-engineering/sql-intermediate-results, software-engineering/cognitive-debt, ai-business/ai-synthetic-focus-group, ai-business/ai-consulting-playbook, ai-engineering/sources/boris-cherny-100-percent-claude-code
- pages updated (9): apache-iceberg, open-table-formats, dimensional-modeling, data-modeling-meaning, databricks, claude-code, vibe-coding, ai-product-management, agentic-coding, algorithms, engineering-craft (+ cross-link-only on parquet, dbt, materialized-views, postgresql-views, data-structures, monetizing-code)
- routing: CMU Advanced DB lecture (youtube-nhwp1btg0cw) identified as Snowflake → new snowflake.md; SQL views/CTE/temp (youtube-vstjydo88ka) → new sql-intermediate-results.md (cross-mechanism decision framework, avoids dup of postgresql-views/materialized-views); Coda "Goals" demo → enriched ai-product-management + agentic-coding (no Coda entity page; subject is Codex /goal)
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans (cognitive-debt new stub, <14d)
- contradictions surfaced (not overwritten): Cherny's minimal-scaffolding "don't box the model in" stance vs the corpus's harness-emphasis pages (agent-harness/agentic-coding) — documented on the Boris Cherny source page as a tension-to-track, framed as a weighting difference not a factual conflict; no synthesis page created
- notes: 1 rate-limited transcript (youtube-ow3es1af5-y) left unstamped to self-recover via the daily job; 2 low-utility ai-business sources kept tight + confidence:0.5 with promo claims flagged; recurring unverified "92% accuracy vs human focus groups" figure cross-referenced against the existing monetizing-code gotcha rather than treated as corroboration

## [2026-06-17 16:57] config | collect-obsidian include set + inline-link following
- include: +Clippings (top-level), +06_Metadata/Reference; -03_Resources/Articles, -03_Resources/Study Notes (kept PARA-native, never reaped)
- links: note-body inline links now fetched (channel web, via_vault_note; asset/auth filters; cap 10/note)
- raw note filenames disambiguated by parent folder (collision fix)
- spec: docs/superpowers/specs/2026-06-17-obsidian-collector-extension-design.md

## [2026-06-17 17:10] ingest | Obsidian Clippings test batch — 5 notes (collect→ingest→reap cycle)
- source: raw/notes/notes-clippings-{best-practices-for-getting-started-with-claude-cowork, best-practices-for-computer-and-browser-use-with-claude, auto-mode-for-claude-code, agent-view-in-claude-code, a-harness-for-every-task-dynamic-workflows-in-claude-code}.md
- channel: notes (collected via /collect-obsidian from vault top-level Clippings/, --max 5; 25 inline-link web sources also collected, queued in raw/_inbox for the daily drain)
- domain: ai-engineering
- new pages (1): computer-use
- pages updated (5): claude-cowork (getting-started guidance), claude-code (auto mode + agent view + dynamic workflows), agent-harness (self-generating harnesses), agentic-workflow (orchestration patterns), agent-ui (multi-session/agent view)
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans
- cycle: first real run of the new collect→ingest→reap flow on the extended collector (top-level Clippings now in scope). After this commit the 5 vault notes are reaped (git rm, staged not committed in the vault).

## [2026-06-17 17:35] ingest | Obsidian Clippings drain batch 2 — 12 notes (collect→ingest→reap)
- source: raw/notes/notes-clippings-{every-claude-code-command-118, deploying-claude-across-the-enterprise-with-claude-cowork(+-1 dup), collaborate-with-claude-across-excel-powerpoint-word-and-out, claude-for-the-legal-industry, claude-security-is-now-in-public-beta, claude-managed-agents-get-to-production-10x-faster, claude-carousel-generator-prompt(SKIPPED, pages:[]), built-in-memory-for-claude-managed-agents, building-agents-that-reach-production-systems-with-mcp, building-ai-agents-for-the-enterprise, best-practices-for-using-claude-opus-4-7-with-claude-code}.md
- channel: notes (collect-obsidian, top-level Clippings, --max 12; inline-link web sources queued in raw/_inbox)
- domain: ai-engineering
- new pages (1): claude-managed-agents
- updated (6): claude-code (118-command taxonomy + Opus 4.7 usage), claude-models (Opus 4.7), agent-security (Claude Security beta), mcp (production patterns), claude-cowork (enterprise/M365/legal), agent-memory (filesystem memory)
- skipped: claude-carousel-generator-prompt (pure prompt template, no §7-citable claims; stamped corpus_pages:[] and reaped)
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans

## [2026-06-17 17:55] ingest | Obsidian Clippings drain batch 3 — 12 notes (2 parallel workers: ai-engineering ×11, data-engineering ×1)
- channel: notes (collect-obsidian, --max 12); inline-link web sources queued in raw/_inbox
- new pages: 0 (all enrichment)
- ai-engineering updated: claude-code (subagents + large-codebase governance + dynamic-workflows Bun example), mcp (connector setup patterns), multi-agent-systems (subagents vs agent teams), agent-skills (pairwise knowledge/unbook, compound loop, command library, charlie-cfo), agentic-coding (Compound Engineering), claude-md-conventions (cross-platform plugins), agent-harness (3 patterns), claude-cowork (official architecture/Projects/safety)
- data-engineering updated: data-engineer-role (DA→DE transition playbook), de-portfolio-projects (cross-link)
- cross-domain flagged (future DE ingest): self-service-analytics-with-Claude data-foundations layer (semantic layer, offline evals, adversarial SQL reviewer)
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans

## [2026-06-17 18:20] ingest | Obsidian Clippings drain batch 4 — 12 notes (ai-engineering)
- channel: notes (collect-obsidian, --max 12); inline-link web sources queued in raw/_inbox
- new pages (1): prompt-caching
- updated (8): ai-product-management (AI-exponential PM), claude-managed-agents (self-hosted sandboxes, MCP tunnels, dreaming/outcomes, AWS), multi-agent-systems (Anthropic 5-pattern taxonomy), agent-skills (internal catalog + best practices), ralph-loop (loop engineering generalization), claude-code (routines + Skyline onboarding case), mcp (consumer connectors), claude-api (Claude Platform on AWS)
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans

## [2026-06-17 19:05] domain | create blockchain (provisional)
- 12 substantive crypto/blockchain-fundamentals sources (nakamoto.ghost.io primer) surfaced in the Clippings drain; fit no existing domain. 11 pages (hub + 10). Provisional; 30-day review 2026-07-17.

## [2026-06-17 19:05] ingest | Obsidian Clippings drain batch 5 / wave 1 — 31 notes (blockchain ×16, ai-engineering ×13, software-engineering ×2)
- channel: notes (collect-obsidian; 00_Inbox/Clippings/scrape crypto cluster, final 7 top-level Clippings, 06_Metadata/Reference, 03_Resources/Snippets)
- blockchain (NEW): 11 pages (history-of-money, the-cypherpunks, satoshi-nakamoto, bitcoin, proof-of-work, public-key-cryptography, hash-functions, merkle-trees, p2p-networking, zero-knowledge-proofs + README). 4 site-meta skipped (about/contribute/haseeb/index).
- ai-engineering: enriched claude-code (tool design), agentic-coding (HTML output + AI-native org), context-window-management (1M/rewind/compact), optimizing-claude (advisor strategy), claude-api (advisor tool), rag (RAG vs agentic search). 8 low-signal/empty/dup notes skipped-with-pages:[] (founder's playbook teaser, vault-personal Reference notes, empty link stubs, dup commands ref).
- software-engineering: both Snippets skipped (trivial/vault-specific).
- prior step: 422 stale PARA-native (Articles/Study Notes) inbox copies purged from raw/_inbox to prevent erroneous reaping of in-place notes.
- worker path-error fixed by coordinator: blockchain worker wrote to repo-root blockchain/ → moved to corpus/blockchain/.
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans

## [2026-06-17 19:30] ingest | Obsidian Clippings drain wave 2 — "Beyond Vibe Coding" book (11 chapters + TOC)
- source: raw/notes/notes-{toc,01..11}-*.md (03_Resources/Books/Beyond_Vibe_Coding_Book), channel notes
- new pages (1): sources/beyond-vibe-coding-book (source summary)
- updated (7): vibe-coding (70% problem, twelve rules, human-30%), prompt-engineering (antipatterns, ReAct/self-consistency), agent-testing (review-debug-refactor, frameworks table, overconfidence effect), agent-security (vuln categories, empirical rates), long-running-agents (copilot→autopilot, background agents), agentic-coding (multimodel orchestration), agentic-workflow (autonomous task cycle)
- ch9 (ethics/IP/policy) + ch11 (future) captured in source page only; flagged cross-domain (ai-business/ethics)
- coordinator fix: source page (sources/ subfolder) citations corrected ../../ → ../../../raw/notes
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans

## [2026-06-17 19:50] ingest | Obsidian Clippings drain wave 3 — 33 Prompt Templates (triage)
- source: raw/notes/notes-*.md (03_Resources/Prompt Templates), channel notes
- enriched (1): prompt-engineering.md — "Reusable prompt patterns" section (metaprompting, prompt optimizer, two-pass editing, verify-before-ship, task-specific summarization framings), 7 templates cited
- skipped (26): personal canned prompts (article creator, tutors, quiz, summary-family duplicates, vault-maintenance, n8n, etc.) — stamped corpus_pages:[] and reaped
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans
- NOTE: Obsidian vault note backlog fully drained (0 unstamped notes remain in raw/_inbox). 242 inline-link web sources remain queued for the daily ingest.

## [2026-06-17 20:10] config | Bridge: external query origin provenance + headless rule (claudesidian → /query)
- why: claudesidian (Obsidian vault) now delegates knowledge questions to /query so they compound back into the corpus; we want to see which queries came from outside.
- bin/query.py: added origin provenance. `resolve_origin()` reads `$CORPUS_QUERY_ORIGIN` (explicit `--origin` overrides). queue_source stamps `query_origin:` on queued sources; log_gap tags the entry `(origin: <origin>)`. Native in-repo queries leave it unset → unchanged frontmatter/log shape.
- .claude/skills/query/SKILL.md: added "External / headless origin" section — when `$CORPUS_QUERY_ORIGIN` is set, compound the safe way (answer + fetch-and-queue + log-gap) but SKIP step-7 file-back (no synthesis-page authoring in unattended runs); synthesis stays interactive/human-attended.
- tests: +11 in tests/test_query.py (resolve_origin precedence, emit/omit, queue_source arg+env, log_gap tag, CLI threading). Full suite 330 passed.
- vault side (separate repo): CLAUDE.md "Connected Knowledge Corpus" block carries the handoff `cd … && CORPUS_QUERY_ORIGIN=claudesidian claude -p "/query <q>"`. Stale in-vault mirror 03_Resources/llm-wiki-system removed.

## [2026-06-17 20:40] ingest | "articles to process" web-list — 68 URLs (4 parallel domain workers)
- source: raw/web/web-*.md (channel web), collected from 00_Inbox/Clippings/articles to process.md (url-list)
- result: 38 ingested, 27 dups/thin marked processed (corpus_pages:[]), 3 valuable cross-domain held (left in the list for a future targeted pass: the-10x-data-team-markdown → DE, designing-synthetic-datasets → DE/mlops, stop-writing-markdown-obsidian → productivity)
- new pages (6): data-engineering/{data-observability, bi-as-code, clickhouse, data-engineering-team-os}, ai-engineering/openviking, ai-business/agent-infrastructure
- enriched (~30): dbt, apache-spark, change-data-capture, databricks, dimensional-modeling, incremental-pipeline-design, scd2, data-quality, python-for-data-engineering, ai-impact-on-data-engineering, claude-code-for-data-engineering, data-engineering-best-practices; claude-code, agent-memory, agentic-coding, rag, agent-skills, agent-cost-management; technical-career, ai-and-the-job-market; mental-models, working-with-stakeholders
- contradictions surfaced (not resolved): dbt-vs-Lakeflow-SDP (data-eng); AI-will-replace-knowledge-work (Miessler) vs agents-narrative-is-muddled (Euclid VC) (ai-business)
- per user request: processed URLs struck from "articles to process.md" by the reaper; 3 held URLs + auth-walled failures (LinkedIn/x.com) remain
- lint: clean — 0 broken wikilinks · 0 broken citations · 0 orphans
