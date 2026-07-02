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

## [2026-06-17 21:05] ingest | "articles to process" — 3 held cross-domain articles
- web-the-10x-data-team-the-markdown-team → data-engineering/ai-impact-on-data-engineering (Markdown Team: 3 new data-team jobs)
- web-stop-writing-markdown-in-obsidian-do-this-instead → productivity/obsidian-pkm (Markdown 2.0 / notes-as-software, HTML-in-Obsidian)
- web-designing-synthetic-datasets → ai-engineering/synthetic-data (NEW page; Google Simula framework)
- new pages (1): ai-engineering/synthetic-data
- their URLs struck from "articles to process.md"; remaining paywalled/auth-walled URLs deleted from the list per user request (not tracked)
- lint: clean

## [2026-06-17 21:30] ingest | "articles to process" — 3 pasted notes (then file emptied)
- 3 substantive pasted snippets extracted to raw/notes and ingested before clearing the vault file:
  - notes-how-to-compete-with-ai → ai-business/technical-career (10-principle compete-with-cheap-AI framing, Jevons paradox, expertise-as-files)
  - notes-remote-software-engineering-job-guide → ai-business/ai-job-search (5-phase remote SWE hiring guide)
  - notes-boris-cherny-14-hidden-claude-code-features → ai-engineering/claude-code (7 net-new flags/features + the verify-your-output tip)
- low-value pasted bits (DE cheatsheet already covered, ChatGPT LinkedIn prompts, command list) NOT ingested
- 00_Inbox/Clippings/articles to process.md then emptied per user request (recoverable from vault git history)
- lint: clean

## [2026-06-18T08:09] config | scheduled run
- collectors:
  - gmail: 1 collected · status=ok
  - obsidian: 0 collected · status=ok
  - youtube: 20 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 0 ingested · 6 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs

## [2026-06-18 12:51] config | add PDF collector (collect-pdf)
- new channel `pdf` → raw/pdf/; watch dir = Google Drive My Drive/CorpusInbox/PDFs (synced locally)
- bin/collect_pdf.py + bin/pdf_client.py (collect + file); pymupdf4llm extraction; text-only
  (low-text guard at 50 words), content_sha dedup, move-to-_processed gated on corpus_ingested
- wired into scheduled_run collection phase; .gitignore raw/pdf/*
- spec: docs/superpowers/specs/2026-06-18-pdf-collector-design.md

## [2026-06-18 00:00] query (origin: claudesidian) | Open-source AI agents/frameworks for data engineering (like Datus-agent) for a Databricks+AWS MBTA OTP lakehouse: text-to-SQL, agentic modeling, dbt/Spark copilots, DQ/orchestration agents — maturity, license, solo-DE fit, and agents-vs-Claude-Code
- gap: Corpus covers the agentic-DE *patterns* well (claude-code-for-data-engineering, agentic-data-modeling, progressive-disclosure-analytics-agents, Grab multi-agent DW) but names none of the specific OSS text-to-SQL agent products with maturity/license: Datus-agent, Vanna, WrenAI, Dataherald. Fetched 4 repos; GitHub star counts not captured in rendered README.
- queued: raw/_inbox/github-datus-ai-datus-agent-the-future-of-data-engineering-a.md, raw/_inbox/github-vanna-ai-vanna-chat-with-your-sql-database-accurate-t.md, raw/_inbox/github-canner-wrenai-give-ai-agents-the-context-to-query-bus.md, raw/_inbox/github-dataherald-dataherald-interact-with-your-sql-database.md

## [2026-06-18 14:19] config | Gmail label collection + post-ingest un-label/archive
- /collect-email now also collects 9 corpus labels (CORPUS_LABELS in bin/gmail_client.py);
  labeled emails carry gmail_corpus_labels and are NOT archived on collect
- new `gmail_client.py reap-labels` removes matched label(s) + INBOX after corpus_ingested;
  wired into scheduled_run after the ingest phase. Starred flow unchanged.
- spec: docs/superpowers/specs/2026-06-18-gmail-label-collection-design.md

## [2026-06-18 14:35] query | data-engineering agents landscape (build-time vs consume-time)
- operation: file-back (synthesis authored from a /query gap; user interactively reviewed + approved)
- question: Survey OSS AI agents/frameworks for data engineering (Datus-agent, Vanna, WrenAI, Dataherald, dbt Agent Skills/MCP, Databricks Genie/Lakeflow); make build-time vs consume-time (text-to-SQL) central; recommend for a solo DE building a portfolio lakehouse
- new page: corpus/data-engineering/data-engineering-agents-landscape.md (synthesis)
- gap web sources queued (channel web, via_query; drain on next Branch-A ingest): WrenAI (Canner/WrenAI), Vanna (vanna-ai/vanna), Dataherald (Dataherald/dataherald), Datus-agent (Datus-ai/Datus-agent), dbt MCP (dbt-labs/dbt-mcp), Databricks Genie (docs.databricks.com). First four were already queued (claudesidian); dbt-mcp + genie fetched this session.
- corpus pages cited: ai-impact-on-data-engineering, claude-code-for-data-engineering, databricks (+ wikilinks to pipeline-layers, semantic-layer, data-quality, dbt, medallion-architecture, mcp, agent-skills, claude-md-conventions, claude-code)
- index + DE hub README updated; counts 183->184 pages, 440->446 sources
- origin: claudesidian vault query (provenance). Recommendation: build with Claude Code + CLAUDE.md + Skills + DQ-as-hooks; optionally one OSS text-to-SQL (WrenAI/Vanna) as a demo layer on finished marts.

## [2026-06-18 14:55] ingest | Gmail-label lifecycle demo — "The 7 deadly sins of prompting" (Ruben Hassid)
- source: raw/email/email-2025-08-24-sins.md (channel email, label Prompting), ingested into ai-engineering/prompt-engineering.md (7 sins + R-E-X framework)
- FIRST live end-to-end of the gmail-label feature on a real email: marked gmail_corpus_labels:[Prompting] → reap-labels gated (nothing-to-reap before ingest) → ingested+stamped → reap-labels removed the Prompting label + archived the email in Gmail (verified: labelIds Prompting-gone). 0 errors.
- lint: clean

## [2026-06-18 15:05] query | file-back: The Portfolio Project That Lands a DE Role
- operation: /query file-back (synthesis authored on explicit user approval)
- origin: claudesidian (delegated from the Obsidian vault; user interactively reviewed + approved the file-back per step 7)
- question: what makes a data-engineering portfolio project genuinely impressive to hiring managers in 2026, for a self-taught DE switcher building ONE end-to-end Databricks+AWS showcase (DE roles only)
- coverage: COVERED by existing corpus — answered from 10 pages, no web gap, nothing queued, no gap log
- new pages: [corpus/data-engineering/portfolio-project-that-lands-a-de-role.md (synthesis)]
- pages drawn on: data-engineer-role, data-engineering-best-practices, de-portfolio-projects, medallion-architecture, data-quality, idempotent-pipelines, cicd-for-data-infrastructure, databricks, sources/aws-duckdb-etl-fargate, ai-business/technical-career
- index/hub: _index.md (+1 page → 185; recent-additions entry) ; data-engineering/README.md (synthesis added, updated→2026-06-18)
- notes: surfaces the honest tension that Databricks is the corpus's own "overkill" case for a solo sub-500GB project, framing the Databricks+AWS choice as a deliberate learning/signal decision with day-one cost guardrails

## [2026-06-18 15:30] ingest | review-queue clearance — 10 deferred emails (no citable content)
- cleared the /ingest-auto deferral queue (raw/_inbox/_REVIEW.md): 10 emails, none with §7-citable content
- 6 G1 (promos/personal/transactional): Decathlon voucher, Shakers promo, Nick-Spisak AI-skill promo, Gmail storage notice, tour-leader admin, family cabin email
- 4 UNCERTAIN (container/pointer): TLDR Dev + TLDR Data digests (articles ingest separately as raw/web companions), Google declutter promo, AWS-masterclass bare youtu.be pointer
- resolution: stamped corpus_ingested: true + corpus_pages: [] and filed to raw/email/ (no corpus pages created — fabricating from these would breach §7 provenance)

## [2026-06-19T02:17] config | scheduled run
- collectors:
  - gmail: 6 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 15 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 0 ingested · 6 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs

## [2026-06-19 09:45] ingest | Data Pipeline Design Patterns #1 — Data Flow
- source: raw/email/email-2025-08-13-data-pipeline-design-patterns-1-data-flow.md (+ companion raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md)
- channel: email → web companion
- domain: data-engineering
- pages touched: [data-flow-patterns (new), data-ingestion-patterns, idempotent-pipelines]
- new pages: [data-engineering/data-flow-patterns.md]
- notes: ingest-auto run; source/sink replayability+overwritability, extraction/behavioral/structural taxonomy

## [2026-06-19 09:45] ingest | [DE 101] #11 — Scale your data pipelines
- source: raw/email/email-2025-08-16-de-101-11-scale-your-data-pipelines.md (+ companion raw/web/how-to-scale-your-data-pipelines-start-data-engineering.md)
- channel: email → web companion
- domain: data-engineering
- pages touched: [scaling-data-pipelines (new)]
- new pages: [data-engineering/scaling-data-pipelines.md]
- notes: ingest-auto run; vertical vs horizontal (independent processes / distributed); strategy-selection questions

## [2026-06-19 09:45] ingest | [DE 101] #12 — How to land a high-paying data job
- source: raw/email/email-2025-08-19-de-101-12-how-to-land-a-high-paying-data-job.md (+ companions raw/web/10-skills-to-ace-…, raw/web/5-steps-to-land-…)
- channel: email → web companions (2)
- domain: data-engineering
- pages touched: [data-engineering-interview (new)]
- new pages: [data-engineering/data-engineering-interview.md]
- notes: ingest-auto run; 10 interview skills (SQL-first) + 5-step job search

## [2026-06-19 09:45] ingest | [DE 101] #9 — Data project to impress hiring managers
- source: raw/email/email-2025-08-10-de-101-9-data-project-to-impress-hiring-managers.md (+ companion raw/web/designing-a-data-project-to-impress-hiring-managers-start-da.md)
- channel: email → web companion
- domain: data-engineering
- pages touched: [de-portfolio-projects]
- new pages: []
- notes: ingest-auto run; show-not-tell, live-dashboard-in-resume tactic (corroborating source)

## [2026-06-19 09:45] ingest | [DE 101] #10 — Set up your data project
- source: raw/email/email-2025-08-13-de-101-10-set-up-your-data-project.md (+ companion raw/web/build-data-engineering-projects-with-free-template-start-dat.md)
- channel: email → web companion
- domain: data-engineering
- pages touched: [de-portfolio-projects, cicd-for-data-infrastructure]
- new pages: []
- notes: ingest-auto run; dev-workflow toolchain (Docker/Terraform/GHA/pytest/black/isort/flake8/mypy)

## [2026-06-19 09:45] ingest | Infrastructure as Code for Data Engineers
- source: raw/email/email-2025-08-10-infrastructure-as-code-for-data-engineers.md
- channel: email (full-body article)
- domain: mlops
- pages touched: [infrastructure-as-code, terraform]
- new pages: []
- notes: ingest-auto run; 5 IaC tool types, why-DEs-use-IaC, Terraform BSL→OpenTofu + modules/providers. 6 ingested, 6 deferred this run.

## [2026-06-19T10:03] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 17 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 6 ingested · 6 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs

## [2026-06-19 10:20] ingest | review-queue clearance — 12 deferred items (no citable content)
- cleared the /ingest-auto deferral queue: 12 items (10 email + 2 youtube), none §7-citable
- 4 PT personal/transactional (IRS e-Fatura, Lovevery skip, 2× Saude ministry), 2 youtube (1 title-only, 1 music-theory with no matching domain), 6 course-promo/video-teaser emails (Jupyter-AI, vibe-code Replit, Skool check-in, self-serve-data-platform, SCD-101, 3-strategy-killers) whose substance is behind unfetched low-utility links
- resolution: stamped corpus_ingested: true + corpus_pages: [] and filed to raw/email|raw/youtube
- NOTE: self-serve-data-platform + 3-strategy-killers are genuine DE topics whose articles/videos were not fetched (low-utility score) — re-fetchable on request

## [2026-06-19 11:30] ingest | ingest-auto safe pass — 20 DE/ML newsletter emails (19 ingested, 1 deferred)
- batch: explicit 20-file list (StartDataEngineering DE-101 #1–#8 + SDE one-offs, Kahan Data Solutions video teasers, Joe Reis "Practical Data Modeling", Vivek Bharti "Practical ML Series")
- channel: email → raw/email/ (moved 19 stamped files from raw/_inbox/; deferred file left in inbox)
- domains: data-engineering (17 sources), mlops (2 sources)
- new pages (2): corpus/data-engineering/requirements-gathering.md (SDE requirements article + Kahan output-led engineering), corpus/mlops/model-serving.md (Flask real-time API + Airflow batch inference)
- substantive enrichments (6): data-modeling-meaning (theory-vs-reality org dimension — Joe Reis), data-quality (code-tests-vs-DQ-checks timing distinction), pipeline-layers (application-DB vs analytics-DB / OLTP-vs-OLAP), data-ingestion-patterns (landing/raw zone), sql-intermediate-results (CTEs as a dbt tell), de-portfolio-projects (free Airflow+Postgres+Metabase template + Docker dev ergonomics)
- corroborating source-bumps (8; content already in corpus via web companions, last_confirmed refreshed): data-orchestration (#8), pipeline-coding-patterns (#7), sql-window-functions (#2), data-engineer-role (#1), dbt (#5), python-for-data-engineering (#3), data-engineering-best-practices (#4), data-engineering-interview (5-steps)
- hubs updated: data-engineering/README (+requirements-gathering), mlops/README (+model-serving)
- deferred (1): email-2025-07-30-free-data-engineering-101-e-book.md → UNCERTAIN (promotional book download/TOC spanning whole DE-101 curriculum; not a single-topic article)
- pages: 2 created, 16 updated (14 content pages + 2 hubs)
- notes: ingest-auto run; 19 processed, 1 deferred. Most DE-101 emails are earlier (Jul/Aug 2025) deliveries of articles already ingested via fetched raw/web companions — ingested as corroborating provenance + last_confirmed, not fabricated content.

## [2026-06-19T10:49] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 17 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 19 ingested · 1 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 6 stubs

## [2026-06-19 12:30] ingest | ingest-auto safe pass — 20 DE label emails (12 ingested, 8 deferred)
- batch: explicit 20-file list (Vu Trinh internals, Pipeline to Insights real-time/batch-vs-stream, SeattleDataGuy columnar, Zach Wilson AI roadmap, Julien Hurault BSL+MCP, Orchestra, + 4 pointer→web companions: local-data-platform, vutrinh dbt_example, copilot-agent-mode, datatalksclub zoomcamp)
- channel: email → raw/email/ (moved 12 stamped emails from raw/_inbox/; 4 pointer companions stamped in place in raw/web/); deferred files left in inbox
- domains: data-engineering (11 sources), ai-engineering (1 source — Copilot)
- new pages (7): data-engineering/bigquery.md, data-engineering/redshift.md, data-engineering/cloud-data-warehouse-internals.md (synthesis), data-engineering/stream-processing.md, data-engineering/orchestra.md, ai-engineering/github-copilot.md, data-engineering/sources/data-engineering-zoomcamp.md
- major enrichments: kafka (Vu Trinh internals: offsets/segments/page-cache/sequential-access/zero-copy-sendfile/batching, producer acks+partitioner, consumer pull/offset-commit/groups/rebalancing, object-storage trend WarpStream/AutoMQ/Redpanda/KIP-1150), parquet (columnar-why, ORC, bit-packing/delta encoding, Uber ZSTD + Criteo), snowflake (cross-warehouse view), databricks (Photon internals + Delta WAL), storage-fundamentals (column vs hybrid format; vectorization vs code specialization), semantic-layer (Boring Semantic Layer + MCP / MCPSemanticModel), ai-impact-on-data-engineering (Zach Wilson risk-by-skill map + AI codegen prompt pattern), data-engineering-best-practices (AI-era checklist corroboration), de-portfolio-projects (Orchestra ELT project + local Terraform+Docker platform), mlops/terraform (Docker-provider local platform), data-orchestration (Dagster/Prefect alternatives)
- light cross-links: etl-pipeline→stream-processing, data-engineering-interview→stream-processing, dbt→orchestra, mcp↔semantic-layer, data-engineer-role→zoomcamp
- hubs updated: data-engineering/README (+stream-processing, +bigquery, +redshift, +orchestra, +cloud-data-warehouse-internals, +zoomcamp source), ai-engineering/README (+github-copilot)
- deferred (8) → raw/_inbox/_REVIEW.md:
  - UNCERTAIN: email-2025-07-05-11-prepare-for-your-data-engineering-interview (teaser, no fetched companion; target "10 skills" already in data-engineering-interview)
  - UNCERTAIN: email-2025-07-03-the-subtle-art-of-data-modeling-example (Kahan video teaser, no transcript/companion)
  - UNCERTAIN: email-2025-07-03-data-modeling-w-dbt-dimensions-part-1-3 (Kahan video teaser, no transcript/companion)
  - UNCERTAIN: email-2025-06-28-10-data-project-to-impress-hiring-managers (teaser, no fetched companion; covered by de-portfolio-projects)
  - UNCERTAIN: email-2025-05-31-6-project-elt-data-pipeline-with-dbt (teaser, no fetched companion; dbt ELT already covered)
  - UNCERTAIN: email-2025-05-30-build-ai-agents-in-databricks-using-claude (fetched companion is itself only a video teaser — no substantive article body)
  - UNCERTAIN: email-2025-05-17-data-engineer-handbook-bootcamp-introduction (pointer; companion fetch-failed — nothing to extract)
  - UNCERTAIN: email-2025-04-17-pipeline-to-insights-ananth-packkildurai-and-seattledataguy (Substack social-notes digest; multiple authors, no fetched companion)
- pages: 7 created, ~16 updated (14 content pages + 2 hubs)
- notes: ingest-auto run; 12 processed, 8 deferred. Interactive manual pass. Pointer sources resolved to fetched raw/web companions and cited from the companion. No new domains.

## [2026-06-19T11:20] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 15 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 12 ingested · 8 deferred · status=ok
- lint:
  - 0 broken wikilinks · 1 broken citations · 0 orphans · 7 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-19 13:10] ingest | ingest-auto safe pass (20 candidates → 15 ingested, 5 deferred)
- channel: email (Gmail label backlog: Data Engineering / databricks / dbt / spark, ML/MLOps/ML Engineering)
- domains: mlops, data-engineering, ai-engineering
- mode: headless (sources stamped, left in raw/_inbox/ for orchestrator relocation; no file moves)
- mlops cluster (Marvelous MLOps "End-to-end MLOps with Databricks", lectures 2–10 + Practical-ML Pt 2):
  - new: mlflow, databricks-development, databricks-asset-bundles, ci-cd-for-ml, model-monitoring, production-ml-workflow
  - updated: model-serving (Databricks Model Serving: serverless REST/scale-to-zero/autoscale units, 3 architectures, A/B sticky assignment), drift-detection (cross-link + Lakehouse drift-metrics note), uv (course usage), README
  - sources: email-2025-07-29-developing-on-databricks, -07-30-getting-started-with-mlflow, -07-31-logging-and-registering-models-with-mlflow, -08-01-model-serving-architectures, -08-02-lecture-6-deploying-model-serving-endpoint-a-b-testing-on-da, -08-03-lecture-7-databricks-asset-bundles, -08-04-ci-cd-deployment-strategies, -08-05-introduction-to-ml-monitoring, -08-06-lecture-10-implementing-model-monitoring-in-databricks, -06-29-build-a-spam-classifier-like-a-production-ml-engineer
- data-engineering cluster:
  - new: data-transformation (the "T" in ETL), small-scale-pipeline-design
  - updated: apache-spark (MapReduce origin, RDD 5 properties/immutability/lineage, Driver/Executor architecture, modes, Job→Stage→Task/DAG, narrow vs wide deps/shuffle), dbt, medallion-architecture, data-quality, README
  - sources: email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr, -04-16-pipeline-design-and-implementation-for-small-scale-projects, -06-26-if-you-re-learning-apache-spark-this-article-is-for-you
- ai-engineering cluster:
  - new: openai (Apr-2025 dev lineup: o3/o4-mini, GPT-4.1 family 1M ctx, Codex CLI, Evals API, audio)
  - updated: mcp (host/client/server triad + runtime loop; stub→draft in index), README
  - sources: email-2025-09-04-mcp-helps-but-how, -04-17-our-most-powerful-reasoning-models-gpt-4-1-codex-cli-and-new
- deferred (5) → raw/_inbox/_REVIEW.md:
  - UNCERTAIN: email-2025-07-17-a-simple-4-step-process-for-dbt-models (Kahan Data Solutions video teaser; no transcript/fetched companion)
  - UNCERTAIN: email-2025-07-16-data-modeling-w-dbt-tests-part-3-3 (Kahan video teaser; no transcript/fetched companion)
  - UNCERTAIN: email-2025-07-11-dbt-vs-stored-procedures-3-key-differences (Kahan video teaser; no transcript/fetched companion)
  - UNCERTAIN: email-2025-07-01-databricks-github-actions-a-blueprint-for-your-automated-ci (pointer; no fetched companion — nothing to extract)
  - UNCERTAIN: email-2025-07-17-build-a-spam-classifier-like-a-production-ml-engineer (pointer; companion fetch-failed — same article captured via the 06-29 Medium copy)
- pages: 9 created, 11 updated (8 content pages + 3 hubs)
- notes: ingest-auto run; 15 processed, 5 deferred via 3 parallel per-domain workers (coordinator-owned _index/_log/stamps). No new domains; no contradictions.

## [2026-06-19T11:42] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 15 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 15 ingested · 5 deferred · status=ok
- lint:
  - 0 broken wikilinks · 1 broken citations · 0 orphans · 8 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-19 12:10] ingest | labeled-backlog finish — triage-clear 14 deferred + reap
- after the labeled-backlog drain (46 ingested across 3 batches), 14 remaining labeled emails were agent-deferred for legit §7 reasons: duplicates of existing coverage (dbt, dimensional-modeling, de-portfolio-projects, data-engineering-interview, spam-classifier already in mlops/production-ml-workflow) or teasers/pointers with no fetchable companion
- resolution: stamped corpus_ingested + corpus_pages:[], filed to raw/email, reaped (14 un-labeled + archived)
- remaining labeled backlog: 2 substantive (15-productivity-hacks, introduction-to-mlops) → small --max 2 ingest

## [2026-06-19 14:30] ingest | Introduction to MLOps
- source: raw/email/email-2025-07-28-introduction-to-mlops.md
- channel: email
- domain: mlops
- pages touched: [corpus/mlops/mlops-principles.md, corpus/mlops/README.md]
- new pages: [corpus/mlops/mlops-principles.md]
- notes: ingest-auto run (interactive, 2 named files); 2 processed, 0 deferred. Marvelous MLOps course lecture 1 — foundational "what is MLOps" page (definition, production meaning, traceability/reproducibility, supporting pillars, tooling-by-category, MLOps vs DevOps, Databricks mapping). Lectures 2–10 ingested previously.

## [2026-06-19 14:30] ingest | 15 Productivity Hacks Every Engineer & Manager Should Know
- source: raw/email/email-2025-06-01-15-productivity-hacks-every-engineer-manager-should-know.md
- channel: email
- domain: productivity
- pages touched: [corpus/productivity/time-and-focus-management.md, corpus/productivity/README.md]
- new pages: [corpus/productivity/time-and-focus-management.md]
- notes: ingest-auto run (interactive, 2 named files); 2 processed, 0 deferred. pointer:false; sole fetched companion is a CodeRabbit sponsor page — extracted from email body, companion not ingested. New time/focus concept page (systems planning, time blocking, context-switching, notifications, maker vs manager time, deep work, prioritization, procrastination, breaks).

## [2026-06-19T14:23] config | scheduled run
- collectors:
  - gmail: 4 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 15 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 2 ingested · 0 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 8 stubs

## [2026-06-19 14:40] config | raise nightly ingest throughput to --max 50
- 2am job (com.corpus.daily) was running `scheduled_run run` at the default --max 6, so collection (gmail/obsidian/youtube/pdf) outpaced ingestion ~3:1 → ~250-source collected-but-not-ingested backlog
- raised to `--max 50 --timeout 5400` in automation/com.corpus.daily.plist.template; reinstalled via install_schedule.sh (2am schedule unchanged). Drains the backlog in ~1 week, then keeps pace. Opus cost runs at 2am (off-peak).

## [2026-06-19 15:00] config | hybrid ingest models — nightly Sonnet, interactive Opus
- nightly 2am job now sets SCHEDULED_RUN_INGEST_MODEL=claude-sonnet-4-6 (EnvironmentVariables in com.corpus.daily.plist.template) so the unattended bulk ingest runs on Sonnet — draws from a separate/larger weekly pool, preserving the scarce Opus weekly budget for interactive daytime work
- interactive/manual ingests still default to Opus (no change); periodic Opus synthesis+lint pass remains on-demand to upgrade connections / catch contradictions
- validated: `claude --model claude-sonnet-4-6 --print` resolves on the subscription (no API key). Revert: delete the EnvironmentVariables block + reinstall

## [2026-06-19 15:30] config | _config.md scheduled-automation section rewritten (was stale)
- the "Scheduled automation" section was outdated (said --max 20, 08:00, single job). Rewrote to document BOTH LaunchAgents accurately: com.corpus.daily (02:00, collect+ingest+reap, --max 50 --timeout 5400, Sonnet ingest) and com.corpus.weekly-synthesis (Tue 13:00, probe-guarded leftover-Opus synthesis). Added subscription-not-API note, CORPUS_JOB install, and tuning levers.

## [2026-06-19 15:00] query (origin: claudesidian) | Three advanced agentic patterns and how they interrelate: continuous-iteration agent loops (Ralph), dynamic/adaptive workflows vs static DAGs, and dreaming/sleep-time compute
- gap: Pillars 1-2 fully covered (ralph-loop, long-running-agents, agentic-workflow). Pillar 3 partial: 'dreaming' covered only as the Claude Managed Agents product feature; the general sleep-time compute paradigm (anticipatory pre-computation during idle, raw->learned context, cost amortization across related queries, Letta MemGPT 2.0 dual primary+sleep-time agent design) was the gap.
- queued: raw/_inbox/sleep-time-compute-beyond-inference-scaling-at-test-time.md, raw/_inbox/sleep-time-compute.md

## [2026-06-20 12:00] ingest | ingest-auto batch — 39 sources, 5 domains
- source: raw/_inbox/ (39 source files; see corpus_pages stamps on each)
- channel: youtube (27), email (10), web (6) [note: `email-2026-06-16-9-software-engineering-skills` counted once; used in 2 pages]
- domains: ai-engineering (17 sources), mlops (7), data-engineering (7), ai-business (3), productivity (3), mixed-4-in-new-pages (2)
- pages touched: [corpus/ai-engineering/ai-presentation-tools.md (NEW), corpus/ai-engineering/spec-driven-development.md (NEW), corpus/data-engineering/dlt.md (NEW), corpus/mlops/networking-fundamentals.md (NEW), corpus/ai-engineering/llm.md, corpus/ai-engineering/agentic-coding.md, corpus/ai-engineering/claude-models.md, corpus/ai-engineering/agent-skills.md, corpus/ai-engineering/learning-ai-engineering.md, corpus/ai-engineering/ai-product-management.md, corpus/ai-engineering/machine-learning.md, corpus/ai-engineering/ai-agent.md, corpus/mlops/linux-commands.md, corpus/mlops/cli-tools.md, corpus/mlops/infrastructure-as-code.md, corpus/mlops/production-ml-workflow.md, corpus/data-engineering/dbt.md, corpus/data-engineering/data-engineering-best-practices.md, corpus/data-engineering/data-quality.md, corpus/data-engineering/medallion-architecture.md, corpus/ai-business/monetizing-code.md, corpus/ai-business/ai-consulting-playbook.md, corpus/ai-business/technical-career.md, corpus/productivity/ai-augmented-knowledge-work.md, corpus/productivity/mental-models.md, corpus/ai-engineering/README.md, corpus/data-engineering/README.md, corpus/mlops/README.md]
- new pages: [corpus/ai-engineering/ai-presentation-tools.md, corpus/ai-engineering/spec-driven-development.md, corpus/data-engineering/dlt.md, corpus/mlops/networking-fundamentals.md]
- notes: ingest-auto run (headless); 50 processed (39 ingested + 11 deferred — see raw/_inbox/_REVIEW.md); split across 2 context windows due to compaction. Sources stamped; files left in raw/_inbox/ per headless mode (orchestrator relocates via channel: field).

## [2026-06-20T11:31] config | scheduled run
- collectors:
  - gmail: 3 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 18 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 39 ingested · 11 deferred · status=ok
- lint:
  - 0 broken wikilinks · 1 broken citations · 0 orphans · 8 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-21 02:00] ingest | Creating Your Own Agentic OS Is Easy (Insanely Powerful)
- source: raw/youtube/youtube-w0S-khYCaB4-creating-your-own-agentic-os-is-easy-insanely-powerful.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: [corpus/ai-engineering/ai-operating-system.md]
- notes: ingest-auto run; 20 processed, 0 deferred

## [2026-06-21 02:00] ingest | Why AI Agents Need an Operating System
- source: raw/youtube/youtube-IVGjBxqygmI-why-ai-agents-need-an-operating-system.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run; AI OS concept cluster (9 sources → 1 new page)

## [2026-06-21 02:00] ingest | 5 Skills to Build an AI Operating System
- source: raw/youtube/youtube-zElKhlFkqU4-5-skills-to-build-an-ai-operating-system-like-the-1-full-gui.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run

## [2026-06-21 02:00] ingest | What Is an AI OS and Why Every Business Will Need It
- source: raw/youtube/youtube-DXcVT07bQ6g-what-is-an-ai-operating-system-and-why-every-business-will-n.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run

## [2026-06-21 02:00] ingest | How to Build a Personal Agentic Operating System
- source: raw/youtube/youtube-ntvkDnk_5jA-how-to-build-a-personal-agentic-operating-system.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run; 7-layer model source

## [2026-06-21 02:00] ingest | I Turned Claude Opus 4.8 Into My Entire AI Operating System
- source: raw/youtube/youtube-0WDkwMxj13s-i-turned-claude-opus-4-8-into-my-entire-ai-operating-system.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run; 4C's framework source

## [2026-06-21 02:00] ingest | Build & Sell Claude Code Operating Systems (2-Hour Course)
- source: raw/youtube/youtube-bCljOfCH8Ms-build-sell-claude-code-operating-systems-2-hour-course.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run

## [2026-06-21 02:00] ingest | How to Build Your AI Operating System with Claude Code (Full)
- source: raw/youtube/youtube-vvDdTPFhCp8-how-to-build-your-ai-operating-system-with-claude-code-full.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run; 3-component model source

## [2026-06-21 02:00] ingest | I Gave Pi Access to Obsidian and I'm Not Looking Back
- source: raw/youtube/youtube-JnQcPzjC6Vo-i-gave-pi-access-to-obsidian-and-i-m-not-looking-back.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-operating-system.md]
- new pages: []
- notes: ingest-auto run; Obsidian as memory layer source

## [2026-06-21 02:00] ingest | Stop Selling AI Agents, Sell AI Operating Systems Instead
- source: raw/youtube/youtube-i79Xyi1RjUo-stop-selling-ai-agents-sell-ai-operating-systems-instead-hug.md
- channel: youtube
- domain: ai-business
- pages touched: [corpus/ai-business/monetizing-code.md]
- new pages: []
- notes: ingest-auto run; AI OS as productized service, 6 revenue streams

## [2026-06-21 02:00] ingest | Introducing Claude Sonnet 4.6
- source: raw/web/web-introducing-sonnet-4-6.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-models.md, corpus/ai-engineering/computer-use.md, corpus/ai-engineering/agent-security.md]
- new pages: []
- notes: ingest-auto run; Sonnet 4.6 official launch post

## [2026-06-21 02:00] ingest | Introducing Claude Opus 4.8
- source: raw/web/web-introducing-claude-opus-4-8.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-models.md]
- new pages: []
- notes: ingest-auto run; Super-Agent benchmark, CursorBench, Messages API change

## [2026-06-21 02:00] ingest | Effective Context Engineering for AI Agents
- source: raw/web/web-effective-context-engineering-for-ai-agents.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/context-engineering.md]
- new pages: []
- notes: ingest-auto run; Anthropic authoritative definition; context rot; system-prompt altitude

## [2026-06-21 02:00] ingest | Mitigating the Risk of Prompt Injections in Browser Use
- source: raw/web/web-mitigating-the-risk-of-prompt-injections-in-browser-use.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/agent-security.md, corpus/ai-engineering/computer-use.md]
- new pages: []
- notes: ingest-auto run; 1% attack success rate; Claude for Chrome beta

## [2026-06-21 02:00] ingest | Adaptive Thinking
- source: raw/web/web-adaptive-thinking.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-models.md]
- new pages: []
- notes: ingest-auto run; per-model support table; manual budget_tokens → 400 error on Opus 4.7+

## [2026-06-21 02:00] ingest | Anthropic Economic Index Report
- source: raw/web/web-anthropic-economic-index-report-uneven-geographic-and-enterp.md
- channel: web
- domain: ai-business
- pages touched: [corpus/ai-business/ai-and-the-job-market.md]
- new pages: []
- notes: ingest-auto run; 40% US employees use AI; Singapore AUI 4.57x; API users 77% automation

## [2026-06-21 02:00] ingest | SDKs — Model Context Protocol
- source: raw/web/web-sdks-model-context-protocol.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/mcp.md]
- new pages: []
- notes: ingest-auto run; SDK tier table (T1-T3); 300M downloads/month

## [2026-06-21 02:00] ingest | How to Land a DevOps Job
- source: raw/email/email-2026-06-15-how-to-land-a-devops-job.md
- channel: email
- domain: ai-business
- pages touched: [corpus/ai-business/ai-job-search.md]
- new pages: []
- notes: ingest-auto run; 6-step model; step 1 = only 30% of equation

## [2026-06-21 02:00] ingest | Only for Devs Trying to Get Interviews
- source: raw/email/email-2026-06-14-only-for-devs-trying-to-get-interviews.md
- channel: email
- domain: ai-business
- pages touched: [corpus/ai-business/ai-job-search.md, corpus/ai-business/ai-and-the-job-market.md]
- new pages: []
- notes: ingest-auto run; Greenhouse: +111% apps/role, +412% apps/recruiter (2022–2025)

## [2026-06-21 02:00] ingest | 2026 Free Data Analyst Bootcamp (Alex The Analyst)
- source: raw/youtube/youtube-cnjhHZNJEDk-2026-free-data-analyst-bootcamp-24-hours-for-free-sql-excel.md
- channel: youtube
- domain: data-engineering
- pages touched: [corpus/data-engineering/data-engineering-interview.md]
- new pages: []
- notes: ingest-auto run; DA vs DE emphasis comparison; SQL #1 on both tracks

## [2026-06-21T12:14] config | scheduled run
- collectors:
  - gmail: 1 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 20 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 20 ingested · 0 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 8 stubs

## [2026-06-22T02:13] config | scheduled run
- collectors:
  - gmail: 3 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 1 collected · status=ok
  - youtube: 22 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 2 stubs

## [2026-06-22 13:39] config | GitHub repo collection (starred repos)
- new collector: bin/collect_github.py + bin/github_client.py (gh CLI); wired into the 2am run
- collects starred repos as one repo-digest each (README + docs + overview), deduped by repo:,
  leaves stars in place; channel github -> raw/github. Spec: docs/superpowers/specs/2026-06-22-github-repo-collection-design.md

## [2026-06-22T14:41] config | scheduled run
- collectors:
  - gmail: 2 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 20 collected · status=ok
  - youtube: 22 collected · status=ok
  - github: 93 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=You've hit your session limit · resets 5pm (Europe/Lisbon)
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 2 stubs

## [2026-06-23 12:00] ingest | ingest-auto batch (30 sources, ai-engineering cluster)
- sources: raw/_inbox/web-mcp-apps-model-context-protocol.md, raw/_inbox/web-elicitation-model-context-protocol.md, raw/_inbox/web-github-cloudflare-mcp-mcp-server-for-the-cloudflare-api.md, raw/_inbox/web-auto-mode-for-claude-code-claude.md, raw/_inbox/web-manage-multiple-agents-with-agent-view-claude-code-docs.md, raw/_inbox/web-orchestrate-subagents-at-scale-with-dynamic-workflows-claude.md, raw/_inbox/web-using-claude-code-session-management-and-1m-context-claude.md, raw/_inbox/youtube-IevmGCVo9Pw-create-your-own-personal-claude-ai-system-that-makes-your-wo.md, raw/_inbox/web-trendaitm-and-anthropic-advance-ai-powered-vulnerability-det.md, raw/_inbox/web-sentinelone-unveils-wayfinder-frontier-ai-services-to-proact.md, raw/_inbox/web-crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-and-q.md, raw/_inbox/web-project-glasswing-securing-critical-software-for-the-ai-era.md, raw/_inbox/web-claude-cowork-anthropics-agentic-ai-for-knowledge-work.md, raw/_inbox/web-built-in-memory-for-claude-managed-agents-claude.md, raw/_inbox/web-harness-design-for-long-running-application-development.md, raw/_inbox/web-scaling-managed-agents-decoupling-the-brain-from-the-hands.md, raw/_inbox/web-asana-claude-managed-agents-case-study-claude-by-anthropic.md, raw/_inbox/web-claude-managed-agents-overview.md, raw/_inbox/web-claude-managed-agents-get-to-production-10x-faster-claude.md, raw/_inbox/web-using-agent-memory.md, raw/_inbox/web-compound-engineering-how-every-codes-with-agents.md, raw/_inbox/web-the-factory-model-how-coding-agents-changed-software-enginee.md, raw/_inbox/web-the-code-agent-orchestra-what-makes-multi-agent-coding-work.md, raw/_inbox/web-agent-harness-engineering.md, raw/_inbox/web-introducing-claude-4.md, raw/_inbox/web-introducing-claude-opus-4-7.md, raw/_inbox/web-pricing.md, raw/_inbox/web-dario-amodei-the-urgency-of-interpretability.md, raw/_inbox/web-writing-effective-tools-for-ai-agentsusing-ai-agents.md, raw/_inbox/web-prompting-best-practices.md
- channel: web (29), youtube (1)
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/mcp.md, corpus/ai-engineering/claude-code.md, corpus/ai-engineering/context-window-management.md, corpus/ai-engineering/agent-security.md, corpus/ai-engineering/anthropic.md, corpus/ai-engineering/claude-cowork.md, corpus/ai-engineering/agent-memory.md, corpus/ai-engineering/claude-managed-agents.md, corpus/ai-engineering/agent-harness.md, corpus/ai-engineering/compound-engineering.md, corpus/ai-engineering/agentic-coding.md, corpus/ai-engineering/claude-models.md, corpus/ai-engineering/interpretability.md, corpus/ai-engineering/tool-calling.md, corpus/ai-engineering/prompt-engineering.md, corpus/ai-engineering/ai-operating-system.md, corpus/ai-engineering/README.md]
- new pages: [corpus/ai-engineering/compound-engineering.md, corpus/ai-engineering/interpretability.md]
- deferred: youtube-72zAHA5j3-4-ableton-with-claude-supercharged-with-osc-and-mpc.md (G1), youtube-8QQZNbWuR0M-claude-ableton-live-changes-everything-for-producers.md (G1), youtube-zYrFIX4z9lY-ableton-and-claude-synchronisation.md (G1), web-bun-is-a-fast-javascriptall-in-one-toolkit.md (UNCERTAIN)
- notes: ingest-auto headless run; 30 processed, 4 deferred; files stamped in raw/_inbox/ (headless mode — orchestrator relocates)

## [2026-06-23T02:51] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 3 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 17 collected · status=ok
  - github: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 30 ingested · 4 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 2 stubs

## [2026-06-23 12:15] query (origin: claudesidian) | Healthcare data engineering showcase: feature store vs vector DB vs Delta decision; PHI de-id, FHIR, ICD-10/SNOMED/LOINC, health DQ; medallion for health->ML features; Spark/dbt/Airflow tooling
- gap: Corpus covers medallion, vector DB, DAMA data-quality, feature-store concept (online/offline store), and dbt/Spark/Airflow tooling. ZERO healthcare-specific coverage (FHIR resources, HIPAA de-identification, ICD-10/SNOMED/LOINC, OMOP CDM). Queued FHIR + OMOP (good extracts); HHS de-id page returned nav chrome only.
- queued: raw/_inbox/overview-clinical.md, raw/_inbox/standardized-data-the-omop-common-data-model.md, raw/_inbox/methods-for-de-identification-of-phi.md

## [2026-06-23 14:00] lint | weekly Opus synthesis+lint pass (Medium, scoped to 30 week-changed pages + neighbours)
- scope: 30 pages changed in the last week (ai-engineering cluster + data-engineering + ai-business + mlops + software-engineering)
- citations/links: fixed 1 mislabeled wikilink (compound-engineering: `[[agentic-coding|spec-driven development]]` → `[[spec-driven-development|Spec-Driven Development]]`); no broken citations or broken targets found across the 30 pages
- cross-links added (typed): compound-engineering ↔ spec-driven-development (extends with learning-capture step); github-copilot → openai (multi-model provider); + new-synthesis links from agent-harness, claude-managed-agents, claude-models, computer-use, compound-engineering, cognitive-debt
- contradictions: none new; the Miessler-vs-Euclid disagreement already named+resolved in ai-and-the-job-market
- new synthesis: [[ai-engineering/generator-evaluator-separation|Generator–Evaluator Separation]] — names the week's cross-source convergence that a model can't reliably grade itself (self-preferential bias); ties 3-agent GAN harness, Managed-Agents Outcomes, computer-use advisor, Fable loop engineering, compound-engineering review, cognitive-surrender anti-pattern. All claims cite raw sources; linked from 6 neighbours (no orphan)
- index: +1 page (215→216); sources unchanged (598; synthesis cites already-ingested sources)

## [2026-06-23 15:30] lint | weekly synthesis+lint pass (Medium) — DE / MLOps / blockchain / productivity / ai-business clusters
- scope: the week's ~90 changed pages; ai-engineering cluster already handled in the earlier same-day pass (generator-evaluator-separation), so this pass focused on the data-engineering, mlops, blockchain, productivity and ai-business pages. Run as 4 parallel disjoint-file domain workers (Coordinator-owns-shared-files, §8.1 v0.6); Coordinator serialized index/log/synthesis.
- citations/links: fixed 2 broken citations — `working-with-stakeholders.md` `sources:` listed two `raw/_inbox/...` paths that no longer exist (files moved to `raw/email/`); corrected `path:` + `channel: inbox`→`email`. No other broken targets across the cluster (PARA-native `03_Resources/...` wikilinks resolve to the external vault by design).
- cross-links added (typed): 27 total — DE warehouse/streaming (databricks↔stream-processing complements, kafka→storage-fundamentals builds-on object storage, parquet↔apache-spark/cloud-data-warehouse-internals); DE patterns (14 across data-engineer-role, data-engineering-interview, data-transformation, pipeline-coding-patterns, requirements-gathering, scaling-data-pipelines, sql-window-functions); mlops (model-monitoring↔data-quality complements, networking-fundamentals→terraform); blockchain (PoW uses hash-functions/PKC, cypherpunks predecessor-of satoshi); ai-business job pages interlink.
- contradictions (recorded, not silently overwritten): (1) data-engineering-best-practices "check only source+final, skip intermediates" vs data-quality/data-flow-patterns "DQ between every layer"; (2) idempotent-pipelines "SCD2 maintains idempotency" vs scd2 "considered harmful" — already mutually cross-linked and reconciled in-page (single-run idempotent vs backfill-chaining), no new synthesis needed; (3) monetizing-code promo-flagged "one week ahead is enough" vs technical-career/ai-and-the-job-market depth-is-the-moat thesis.
- new syntheses (2, naming unfilled cross-source themes; every non-trivial claim cited; each linked from ≥2 neighbours + domain hub, no orphans):
  - [[data-engineering/compute-storage-decoupling|Compute–Storage Decoupling]] — warehouses (Vu Trinh internals), lakehouse (Delta WAL over object storage), and streaming (tiered/diskless Kafka) converge on separating compute from object storage. Cites 3 raw sources.
  - [[mlops/environment-promotion|Environment Promotion (dev → acc → prd)]] — ML CI/CD + data-infra CI/CD + Databricks Asset Bundles share four invariants (humans-only-in-dev, env-scoped state, CI-check→human-gated prod apply, machine identity). Cites 3 raw sources.
- index: +2 pages (216→218); sources unchanged (598; both syntheses cite already-ingested sources).

## [2026-06-23 15:40] lint | consolidation pass (Opus, leftover weekly capacity)
- new page: corpus/ai-engineering/embeddings.md — implicit concept (defined inline across rag/transformer/vector-database/agentic-search/agent-memory, no own page); consolidates token vs sentence/doc embeddings, similarity metrics, quantization cost, 3 failure modes
- matured: corpus/ai-engineering/transformer.md (draft → mature; confidence 0.9; last_confirmed 2026-06-23)
- cross-links added across 5 ai-engineering pages; embeddings linked from the domain hub
- verify gate: an independent Sonnet content-critic ran before commit and caught a fabricated quote (invented 5,000/10M figures) + a misattributed "temporal knowledge graph" framing on embeddings.md — both corrected to what the cited sources support

## [2026-06-23 16:10] ingest | claude-watch deep-analysis note (5 Claude Connectors)
- source: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-5-claude-connecto-report.md (channel notes; vault_origin youtube_raw/.../5-claude-connectors-.../report.md)
- domain: ai-engineering
- pages touched: corpus/ai-engineering/claude-cowork.md (new Connectors section + [^src24])
- notes: first ingest after Phase-4 enablement (collect-obsidian guard dropped; reaper folder-aware). Reaping this note git-rms report.md + 5 sibling frames (whole-folder reap). Ledger gate (~/.config/watch/yt_deepen_done.jsonl) confirmed: video -h2C65Qd9Mg in ledger, absent from yt_watch_queue → no re-queue.

## [2026-06-24 00:00] ingest | ingest-auto batch (50 candidates: 30 ingested, 20 deferred)
- source: raw/_inbox/ (30 sources stamped; 20 deferred to _REVIEW.md)
- channel: web / email / inbox
- domain: ai-engineering (all 30 sources)
- pages touched: corpus/ai-engineering/claude-code.md, corpus/ai-engineering/claude-cowork.md, corpus/ai-engineering/claude-managed-agents.md, corpus/ai-engineering/agent-security.md, corpus/ai-engineering/compound-engineering.md, corpus/ai-engineering/vibe-coding.md, corpus/ai-engineering/mcp.md, corpus/ai-engineering/agentic-workflow.md, corpus/ai-engineering/claude-models.md, corpus/ai-engineering/multi-agent-systems.md, corpus/ai-engineering/agent-skills.md, corpus/ai-engineering/long-running-agents.md, corpus/ai-engineering/agentic-coding.md, corpus/ai-engineering/claude-api.md, corpus/ai-engineering/anthropic.md, corpus/ai-engineering/spec-driven-development.md, corpus/ai-engineering/computer-use.md, corpus/ai-engineering/README.md
- new pages: none
- notes: ingest-auto run; 30 processed, 20 deferred. 18 existing pages enriched. Topics: Claude Code permission modes/Channels/security-review/Artifacts, Cowork Dispatch/OTel/Research, Managed Agents case studies (Notion/Rakuten/Sentry/Vibecode)/Claude for Legal, agent-security (Palo Alto Unit 42/Wiz Red Agent), compound-engineering plugin inventory + Montaigne, vibe-coding non-technical practitioners, MCP Channels protocol, pi-ask-user decision-gating, web search models, pi-subagents, Enterprise Analytics API, CONTEXT→COPY→DESIGN website spec, computer-use macOS reference implementation.

## [2026-06-24T03:17] config | scheduled run
- collectors:
  - gmail: 4 collected · status=ok
  - obsidian: 53 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 21 collected · status=ok
  - github: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 30 ingested · 20 deferred · status=ok
- lint:
  - 1 broken wikilinks · 33 broken citations · 0 orphans · 2 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-24 14:30] config | X bookmarks channel added
- channel: `x` (X/Twitter bookmarks via X API v2, OAuth2 user-context)
- dedup: `tweet_id` in source frontmatter
- reap: un-bookmarks only after `corpus_ingested: true` (separate step via `bin/x_client.py reap`)
- setup: create `bin/x_app.json` (client_id + redirect_uri), run `python3 bin/x_client.py auth` once
- token secrets: `bin/x_token.json` and `bin/x_app.json` gitignored (added to `.gitignore`)
- status if unconfigured: `not configured`; run continues without blocking

## [2026-06-25 14:00] ingest | big-backlog batch — Wave 1 (productivity, ai-business, mlops, trading, blockchain)
- sources: 71 (36 youtube incl. 44 whisper-rescued, 9 notes, 8 email, 8 web, 7 github, 3 pdf)
- channels: youtube, notes, email, web, github, pdf
- domains: productivity, ai-business, mlops, trading (NEW), blockchain
- method: §8.1 cluster pipeline; Coordinator (Opus) + 6 Sonnet workers (4 parallel Round A + 2 sequential Round B for sharded ai-business/mlops); one-writer-per-domain
- new pages: 30 — trading/{README,ai-trading-agents,self-improving-agents,arbitrage-compression,prediction-markets,alpaca-api,tradingview-pine-script,hyperliquid,polymarket}; blockchain/bittensor; mlops/{tmux,vps-for-agents,cron-scheduling,linux-filesystem,devops-learning-roadmap,designing-ml-systems,made-with-ml,handson-ml3,100-days-of-ml-code,ampernetacle,tilt,terax}; ai-business/{ai-business-models,boring-expert-businesses,selling-to-ai-agents,ai-content-with-voice,harvey,claude-for-startups}; productivity/{decision-making,quartz-ssg}
- updated pages: 24 (learning-to-learn, ai-augmented-knowledge-work, obsidian-pkm, working-with-stakeholders, time-and-focus-management, mental-models, technical-career, monetizing-code, ai-consulting-playbook, ai-job-search, agent-infrastructure, git, terminal-and-shell, mlops-principles, cli-tools, linux-commands, vps-for-agents, tmux, terax, devops-learning-roadmap + 4 hub READMEs)
- new domain: trading (provisional; see _domains.md decision log 2026-06-25)
- notes: part of clearing the 455-source inbox backlog discovered this session. Wave 2 (software-engineering 41 + data-engineering 39) and Wave 3 (ai-engineering 247) to follow. 56 no-citable-content sources to be stamped+filed (corpus_pages:[]) in the final drop pass. Whisper-rescue recovered 44/254 keepers before YouTube re-throttled; remainder auto-recover via the daily job.

## [2026-06-25 14:45] ingest | big-backlog batch — Wave 2 (software-engineering, data-engineering)
- sources: 80 (31 github, 17 pdf, 15 youtube, 10 web, 4 notes, 3 email); 13 no-citable-content stamped corpus_pages:[]
- channels: github, pdf, youtube, web, notes, email
- domains: software-engineering, data-engineering
- method: §8.1 cluster pipeline; 5 Sonnet workers (se×2, de×3), shards sequential within domain, domains parallel; read-smart on github digests
- new pages: 17 — software-engineering/{ci-cd,system-design-fundamentals,go-programming-language,javascript-fundamentals,terminal-cli-tools,git-basics,react,bun,vim,kan,usertour,sources/software-engineers-guidebook}; data-engineering/{modern-data-stack,omop-cdm,fhir,perspective,windsor-ai}
- updated pages: ~35 incl. apache-spark (PySpark RDD/DataFrame/MLlib), stream-processing, dbt, dimensional-modeling (1NF-5NF), python-for-data-engineering, databricks, scd2, medallion-architecture, data-quality, data-orchestration, semantic-layer, software-design-principles, engineering-craft, ai-assisted-development, git-basics, go/js/system-design
- notes: 13 skipped at citation gate (curated link-lists: free-programming-books, awesome-for-beginners, free-for-dev, sindresorhus/awesome, dwyl; thin tools/pointers; PHI landing page). Wave 3 (ai-engineering, 247 sources) is the final wave.

## [2026-06-25 16:30] ingest | big-backlog batch — Wave 3 (ai-engineering) + backlog close-out
- sources: 247 ai-engineering (89 web, 78 youtube, 39 github, 31 notes, 7 email, 1 pdf) + 57 no-citable-content DROPs filed (corpus_pages:[])
- channels: web, youtube, github, notes, email, pdf
- domains: ai-engineering (mature, 63→69 pages)
- method: §8.1 cluster pipeline; 10 sequential Sonnet shards (~25 sources each). SEQUENTIAL within domain (not parallel) to prevent hot-page write collisions on heavily-shared pages (claude-code, agent-skills, mcp, agent-memory). WIP-committed per shard for durability.
- new pages: 6 — pi-agent, gemini-cli, manus, supacode, intent-debt, sleep-time-compute
- updated pages: ~40 incl. claude-code, agent-skills, agent-memory, mcp, claude-cowork, claude-managed-agents, agentic-coding, context-window-management, tool-calling, agent-harness, agent-security, claude-models, rag, ai-operating-system, spec-driven-development, prompt-engineering, agent-cost-management, compound-engineering, context-engineering, computer-use, interpretability, transformer, ai-agent, hermes, anthropic, ai-product-management, learning-ai-engineering, vibe-coding, ralph-loop, github-copilot, claude-md-conventions, prompt-caching, claude-api, agent-evaluation, multi-agent-systems
- post-merge cleanup: 151 citation paths normalized raw/_inbox/→raw/<channel>/; fuzzy-matched 34 worker filename-slips to real sources; 3 notes-channel citations remain unresolved (worker-invented slugs; claim text intact)
- one delta inconsistency: ae_01 worker initially died at session limit (partial writes reverted cleanly via git, re-run fresh); several workers omitted/varied source_map (stamped coarsely from shard touched-pages, _log is authoritative)
- notes: this completes the 455-source inbox backlog discovered 2026-06-25. Total across 3 waves: 398 substantive sources ingested (71+80+247) + 57 drops; 53 new pages + trading domain; ~110 pages enriched. Remaining blocked-keeper YouTube transcripts (210/254) auto-recover via the daily job over time.

## [2026-06-26T08:37] config | scheduled run
- collectors:
  - gmail: 11 collected · status=ok
  - obsidian: 1 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 0 collected · status=failed
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 0 ingested · 6 deferred · status=timeout · error=timeout
- lint:
  - 1 broken wikilinks · 9 broken citations · 0 orphans · 18 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-26 10:30] ingest | ingest-auto manual pass — 6 named inbox emails (2 ingested, 4 deferred)
- sources: 6 email (2 single-author DE articles ingested; 4 multi-topic digest newsletters deferred)
- channel: email
- domain: data-engineering (both ingested sources)
- ingested:
  - email-2026-06-25-i-spent-12-hours-rebuilding-my-junior-year-project-part-2-th.md (Minh Pham / Vu Trinh — dbt transformation layer project)
  - email-2026-06-24-how-i-made-my-data-platform-s-failures-public-and-earned-my.md (Yordan Ivanov / Data Gibberish — data platform status page)
- new pages: 2 — data-engineering/sources/skytrax-dbt-transformation-project (source), data-engineering/data-status-page (concept)
- updated pages: 4 — dbt (manifest-state incremental deploys), cicd-for-data-infrastructure (dbt slim-CI/defer-CD worked example + OIDC), dimensional-modeling (role-playing dimensions + dbt_utils surrogate keys), data-observability (detection→communication / status page); + README hub + _index
- deferred (→ _REVIEW.md): 4 — how-to-get-reliable-results-from-your-llms (TDS The Variable), stealing-is-a-skill-gemini-3-5-flash-... (TLDR Dev), openai-s-custom-chip-tesla-... (TLDR), netflixs-new-batch-compute-... (TLDR Data). All UNCERTAIN: multi-topic digest newsletters spanning many domains; their fetched companions are separate raw/web/ sources that drain individually.
- notes: ingest-auto run; 2 processed, 4 deferred. Stamped + moved both ingested emails to raw/email/. These 6 are the same set the 2026-06-26T08:37 scheduled run deferred on timeout.

## [2026-06-26 12:40] ingest | ingest-auto manual pass (6-file filtered batch)
- sources: 3 — raw/web/6-data-engineering-skills-to-progress-in-the-age-of-ai-start.md (+ its pointer email raw/email/email-2026-06-24-6-data-engineering-skills-to-progress-in-the-age-of-ai.md), raw/email/email-2026-06-24-how-id-make-a-simple-project-stand-out.md
- channels: web, email
- domains: data-engineering, ai-business
- ingested: 2
  - StartDataEngineering "6 Data Engineering Skills To Progress in the Age of AI" (Joseph Machado) — single-article email; content in fetched raw/web/ companion; cited the companion, stamped both email + companion
  - Tech With Tim "how I'd make a simple project stand out" — self-contained email; corroborates existing [^src1] Tech With Tim portfolio advice
- new pages: 0
- updated pages: 3 — data-engineering/ai-impact-on-data-engineering (new "six enduring DE skills" section + src9), data-engineering/data-engineering-best-practices (AI-era corroboration paragraph + src8, last_confirmed→2026-06-26), ai-business/technical-career (portfolio "sharper angle" corroboration + src14)
- deferred (→ _REVIEW.md): 4
  - UNCERTAIN: email-2026-06-24-anthropic-drops-claude-tag.md (The Code digest — many topics/domains)
  - UNCERTAIN: email-2026-06-24-elden-rings-ai-openai-daybreak-fired-by-google-for-workspace.md (TLDR Dev digest — many topics)
  - UNCERTAIN: email-2026-06-23-google-takes-the-hit-in-ai-s-talent-war.md (The Code digest — many topics)
  - UNCERTAIN: notes-...-how-to-build-your-report.md (Dave Ebbelaar full-stack AIOS — already ingested via youtube-rZX1OYetbSM; raw/notes filename collision with the different nyndra "4-Layer Setup" report → move would overwrite)
- notes: ingest-auto run; 2 processed, 4 deferred. Stamped + moved both ingested emails to raw/email/; web companion stamped in place. No new domains; _domains.md untouched.

## [2026-06-26T13:47] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 0 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26T13:48] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=You've hit your session limit · resets 5pm (Europe/Lisbon)
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26T13:48] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=You've hit your session limit · resets 5pm (Europe/Lisbon)
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26T13:49] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=You've hit your session limit · resets 5pm (Europe/Lisbon)
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26T13:49] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 0 deferred · status=failed · error=You've hit your session limit · resets 5pm (Europe/Lisbon)
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26 14:30] ingest | Go full courses (Tech With Tim + freeCodeCamp/boot.dev)
- source: raw/youtube/youtube-V-lI7AmusGs-go-programming-full-course.md, raw/youtube/youtube-un6ZyFkqFKo-go-programming-golang-course-with-bonus-projects.md
- channel: youtube
- domain: software-engineering
- pages touched: [go-programming-language]
- new pages: []
- notes: ingest-auto manual pass (6-file batch); 6 processed, 0 deferred. Integration-completion of an interrupted prior run that wrote pages but did not stamp sources / update index+log. Go page (mature) enriched with both courses: structs/interfaces/channels/mutexes/generics, RSS-aggregator capstone (chi/sqlc/Goose/API-key auth), Textio example, compile-vs-runtime distinction.

## [2026-06-26 14:30] ingest | Claude Design (3 Nate Herk videos)
- source: raw/youtube/youtube-gAoZ95kqG7w-claude-design-just-became-unstoppable.md, raw/youtube/youtube-TcFeSjwTo7g-claude-design-builds-beautiful-3d-websites-instantly-full-tu.md, raw/youtube/youtube-ovabeVoWrA0-claude-design-2-hour-course-beginner-to-pro.md
- channel: youtube
- domain: ai-engineering
- pages touched: [claude-design (new), ai-presentation-tools]
- new pages: [claude-design]
- notes: New entity page — Anthropic Labs design product (launched 2026-04-17, Opus 4.7 vision); design systems/skill.md, in-canvas tweaks/comment/draw/edit, export Canva/PDF/PPT/HTML, hand-off to Claude Code, separate weekly quota, 3D scroll-site workflow, Krieger ex-Figma → Anthropic CPO. ai-presentation-tools updated (Claude Design "now shipped" as approach #1; Gamma trade-off, context-gravity).

## [2026-06-26 14:30] ingest | How to use Claude for Finance (Luke Finance)
- source: raw/youtube/youtube-qLDwThdc3WQ-how-to-use-claude-for-finance-better-than-99-of-people.md
- channel: youtube
- domain: ai-engineering
- pages touched: [claude-for-finance (new)]
- new pages: [claude-for-finance]
- notes: New concept page — 9-stage gated FP&A workflow via the Claude Excel add-in: inventory-before-insight, protected baseline, plan-first, formula-driven/auditable 3-statement+DCF, 13-week cash forecast, model-selection-by-task-type. Cross-linked to prompt-engineering / agentic-workflow / claude-models. ingest-auto run total: 6 processed, 0 deferred, 2 pages created, 2 updated.

## [2026-06-26T17:36] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 0 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26T17:37] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 6 deferred · status=timeout · error=timeout
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26 17:40] ingest | Local-agent cluster (3 "AI Agents" YouTube transcripts)
- sources:
  - raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md
  - raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md
  - raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md
- channel: youtube
- domain: ai-engineering
- pages touched: [local-ai-agents.md (new), openclaw.md (new), paperclip.md (new), multi-agent-systems.md, sources/how-ai-agents-and-skills-work.md, README.md, _index.md]
- new pages: [ai-engineering/local-ai-agents, ai-engineering/openclaw, ai-engineering/paperclip]
- notes: ingest-auto manual pass; 3 processed, 3 deferred. Completed a prior same-day session's partial ingest (pages existed untracked but sources were unstamped/unmoved and index/log unupdated). S_oN3vlzpMw is a re-collected Whisper transcript of the already-ingested Isenberg×Ras-Mic episode — treated as corroborating re-ingest (enriched openclaw.md with its OpenClaw-specific sponsor-vetting/recursive-skill material; added as 2nd source to the source page, last_confirmed refreshed). Stamped + moved all 3 to raw/youtube/.

## [2026-06-26 17:40] ingest | deferrals (ingest-auto)
- DEFER UNCERTAIN: email-2026-06-26-unit-tests-for-taste-ai-native-or-left-behind-drizzles-npm-p.md — TLDR Dev multi-topic digest newsletter; fetched companions span security/ML/dev-tooling/SEO and are separate raw/web/ sources; routing is a judgment call
- DEFER UNCERTAIN: web-claude-code-category-blog-claude-by-anthropic.md — Anthropic blog category index; only post titles + category blurb, no article bodies; nothing citable (extraction would require fabrication per §7/§13)
- DEFER UNCERTAIN: web-agents-category-blog-claude-by-anthropic.md — Anthropic blog category index; only post titles + category blurb, no article bodies; nothing citable (extraction would require fabrication per §7/§13)

## [2026-06-26T17:40] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 6 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-26 18:10] ingest | A Field Guide to Rapidly Improving AI Products (Hamel Husain)
- source: raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md
- channel: web
- domain: ai-engineering
- pages touched: [ai-engineering/error-analysis (new), ai-engineering/sources/field-guide-improving-ai-products (new), ai-engineering/agent-evaluation, ai-engineering/synthetic-data, ai-engineering/ai-product-management, ai-engineering/README]
- new pages: [ai-engineering/error-analysis, ai-engineering/sources/field-guide-improving-ai-products]
- notes: ingest-auto manual pass (6-file filtered batch); 1 processed, 5 deferred. Only substantive single article in the batch; routed to ai-engineering (error analysis + eval discipline). Other 5 deferred as blog/weblog/bio index pages (no citable single-article body) or multi-topic digest.

## [2026-06-26 18:10] ingest | ingest-auto run summary (6-file filtered batch)
- run: 1 ingested · 5 deferred · 2 pages created · 3 pages updated
- deferred: web-the-new-software-lifecycle (UNCERTAIN — addyosmani blog index, already in _REVIEW), web-simon-willisons-weblog (UNCERTAIN — weblog firehose, already in _REVIEW), email-2026-06-25-chinese-grey-market-sells-claude-api-access (UNCERTAIN — The Code digest, already in _REVIEW), web-andrej-karpathy (UNCERTAIN — bio/CV page, new), web-all-databricks-blog (UNCERTAIN — blog index, new)
- notes: 3 of the 5 defers were already recorded in raw/_inbox/_REVIEW.md by an earlier pass today; 2 new defer lines (karpathy, databricks) appended this run.

## [2026-06-26T17:46] config | scheduled run
- collectors:

- ingest:
  - ingest: 1 ingested · 5 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-27 00:00] ingest | batch ingest-auto — 17 sources (16 ai-engineering, 1 data-engineering)
- source: raw/_inbox/ (17 pre-filtered files)
- channel: youtube (15), web (1), github (1)
- domain: ai-engineering (16 sources), data-engineering (1 source)
- pages touched: [corpus/ai-engineering/perplexity-computer.md, corpus/ai-engineering/hermes.md, corpus/ai-engineering/multi-agent-systems.md, corpus/ai-engineering/openclaw.md, corpus/ai-engineering/claude-managed-agents.md, corpus/ai-engineering/agentic-coding.md, corpus/ai-engineering/prompt-engineering.md, corpus/ai-engineering/learning-ai-engineering.md, corpus/ai-engineering/embeddings.md, corpus/ai-engineering/ai-agent.md, corpus/ai-engineering/agent-skills.md, corpus/ai-engineering/README.md, corpus/data-engineering/dbt.md]
- new pages: [corpus/ai-engineering/perplexity-computer.md]
- notes: ingest-auto run resumed after context compaction; 17 processed, 0 deferred; headless mode (stamps in place, orchestrator handles relocation). Key additions: Hermes 5-pillar architecture + loop + Vapi integration (6 sources); Factory Missions 5-pattern taxonomy; Perplexity Computer entity (new); leaked-system-prompts "tool use schema is the moat" finding; Dreams of Code CI/CD Rust agent + Tailscale Aperture; DeepMind concept neurons; 4-level agentic framework; AI blogs list; $700/year CMA cost calc + harnessing framing.

## [2026-06-27T02:35] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 122 collected · status=ok
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 17 ingested · 0 deferred · status=ok
- lint:
  - 1 broken wikilinks · 26 broken citations · 0 orphans · 19 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-26 22:00] ingest | dbt-labs/dbt-core (GitHub README)
- source: raw/github/github-dbt-labs-dbt-core.md
- channel: github
- domain: data-engineering
- pages touched: [data-engineering/dbt]
- new pages: []
- notes: Corroborating + enriching source for the v2.0 section. New: single-self-contained-binary install detail, OS/arch support matrix (macOS/Linux fully supported; Windows x86-64 yes, ARM not yet), branch structure (main=v2.0 alpha, 1.latest=v1). Latest v1 release v1.11.11. Moved to raw/github/ (new channel dir created).

## [2026-06-27 03:30] ingest | Claude.com localized plan pages + AI-agents solutions page
- source: raw/web/web-claude-by-anthropic-90b51f29.md (+ web-untitled-42cbd4cb, web-claude-2c35b97a, web-claude-796a7cce, web-claude-4f6af6b8, web-ai-claude-419e4408)
- channel: web
- domain: ai-engineering
- pages touched: [ai-engineering/claude-plans, ai-engineering/anthropic, ai-engineering/README]
- new pages: [ai-engineering/claude-plans]
- notes: ingest-auto run; 6 processed, 0 deferred. 5 localized claude.com pricing pages (de/fr/it/ja/ko) deduped 5→1 into new claude-plans entity (Free/Pro/Max/Team/Enterprise + Education subscription tiers); distinct from per-token API pricing on claude-models. 6th source (claude.com/ja/solutions/agents) added a Claude Platform/Workbench agents-positioning note to anthropic.md.

## [2026-06-27T09:44] config | scheduled run
- collectors:

- ingest:
  - ingest: 0 ingested · 6 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-27 10:05] ingest | Claude.com localized /solutions/agents variants + Claude for Education
- source: raw/web/web-ai-agents-claude-by-anthropic-47a6f280.md (+ web-ki-agenten-claude-fe3fc652, web-agents-ia-claude-e3fe15ea, web-ai-18438e8f, web-ai-agents-claude-by-anthropic-18c36943, web-claude-b824c3d1)
- channel: web
- domain: ai-engineering
- pages touched: [ai-engineering/anthropic]
- new pages: []
- notes: ingest-auto run; 6 processed, 0 deferred. 5 localized claude.com/solutions/agents variants (en/de/fr/it/ko) consolidated as additional sources on anthropic.md's existing "Claude Platform for AI agents" section (content already ingested earlier via the ja variant web-ai-claude-419e4408); [^src12] repointed to the English canonical URL. 6th source (claude.com/ja/solutions/education) added a new "Claude for Education" section to anthropic.md (learning mode = Socratic tutor, Claude Code as apprenticeship-at-scale, Claude API for research).

## [2026-06-27 10:30] ingest | Claude.com localized /solutions/education + /solutions/coding variants
- source: raw/web/web-education-claude-by-anthropic-16c564ed.md (+ web-bildungswesen-claude-e8df4dcf, web-education-claude-1c0dd8a9, web-claude-372516cb [education en/de/fr/ko]; web-programmierung-claude-bbf1e585, web-claude-469a16cf [coding de/ja])
- channel: web
- domain: ai-engineering
- pages touched: [ai-engineering/claude-for-education, ai-engineering/claude-models, ai-engineering/README]
- new pages: [ai-engineering/claude-for-education]
- notes: ingest-auto run; 6 processed, 0 deferred. 4 localized claude.com/solutions/education variants (en/de/fr/ko) deduped 4→1 into new claude-for-education entity (university-wide program: Socratic learning mode, Claude Code apprenticeship, Claude API for research); page cross-links anthropic.md's existing Education section + the Education plan tier on claude-plans. 2 localized claude.com/solutions/coding variants (de/ja) deduped 2→1 update on claude-models (Fable 5 leads SWE-Bench Pro 80.3% [^src22]; vendor 60×/95% customer-outcome marketing claims flagged as not independent). No new domains; all routing to existing ai-engineering.

## [2026-06-27T09:54] config | scheduled run
- collectors:

- ingest:
  - ingest: 6 ingested · 0 deferred · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs

## [2026-06-27 10:05] ingest | articles to process.md drain (2 web articles)
- sources: raw/web/web-claude-corps.md, raw/web/web-claude-code-is-terrible-at-design.md
- channel: web (via vault list `00_Inbox/Clippings/articles to process.md`)
- domains: ai-business, ai-engineering
- new pages: [ai-business/claude-corps, ai-engineering/sources/claude-code-website-build-workflow]
- pages touched: [ai-business/README, ai-business/claude-for-startups, ai-engineering/claude-design, ai-engineering/sources/claude-code-website-build-workflow, ai-business/claude-corps]
- notes: interactive drain of the fetchable lines from the vault url-list. Claude Corps = Anthropic+CodePath+Social Finance nonprofit fellowship (talent-supply counterpart to claude-for-startups access programs). Charlie Hills = 9-step spec-driven CONTEXT/COPY/DESIGN website-build workflow + structural-donor component rule. 4 lines could NOT be fetched and remain in the file: kaggle (JS-rendered SPA, no HTML body), towardsdatascience (HTTP 403), 2× x.com (auth-walled). The 2 ingested lines struck from the vault file.

## [2026-06-28 00:00] ingest | Anthropic website scrape — claude.com solutions/pricing/platform/customers (30 sources, 6 groups)
- source: raw/web/web-financial-services-claude-by-anthropic-d0841a7c.md + 4 lang variants (ja/ko/fr/de)
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-for-finance.md]
- new pages: []
- notes: ingest-auto run; Anthropic financial services solutions page — LSEG/FactSet/S&P/Morningstar integrations, 4 agent templates, SOC2/FedRAMP compliance, 4 verticals. en primary + ja/ko/fr/de language stamps only.

## [2026-06-28 00:01] ingest | Anthropic website scrape — government solutions (5 sources)
- source: raw/web/web-government-claude-by-anthropic-523b938e.md + 4 lang variants (ja/ko/de/fr)
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-for-government.md, corpus/ai-engineering/README.md]
- new pages: [corpus/ai-engineering/claude-for-government.md]
- notes: ingest-auto run; new entity page: FedRAMP High + IL5 deployment surfaces (API/Claude Gov/app), 3 reasons agencies choose Claude, classified AWS missions. en primary + 4 lang stamps.

## [2026-06-28 00:02] ingest | Anthropic website scrape — pricing (6 sources)
- source: raw/web/web-plans-pricing-claude-by-anthropic-eb3bbaf1.md + 5 lang variants (it/ko/ja/de/fr)
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-plans.md]
- new pages: []
- notes: ingest-auto run; major update to claude-plans.md: platform feature pricing (Managed Agents/web search/code execution), service tiers, US-only 1.1×, fast mode Opus 4.8, prompt caching 5-min TTL, legacy models, @Claude/@Security/Memory/Skills feature flags. en primary + 5 lang stamps.

## [2026-06-28 00:03] ingest | Anthropic website scrape — customer stories (6 sources)
- source: raw/web/web-customer-stories-claude-by-anthropic-980b0e92.md + 5 lang variants (it/ja/ko/de/fr)
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/anthropic.md]
- new pages: []
- notes: ingest-auto run; enterprise customer roster section added: June 2026 new customers (Cox/Kai/Vercel/Box/Quantium/Juno/Cursor/Garvan/delight.ai/Lovable/Replit/Warp/Jakala/Twilio) + established clients (Postman/Stripe/HubSpot/Figma/Spotify/etc). en primary + 5 lang stamps.

## [2026-06-28 00:04] ingest | Anthropic website scrape — startups program (3 sources)
- source: raw/web/web-heute-mit-claude-gestalten-morgen-zum-marktfuhrer-werden-cla-a2d57d64.md + 2 lang variants (ja/ko)
- channel: web
- domain: ai-business
- pages touched: [corpus/ai-business/claude-for-startups.md]
- new pages: []
- notes: ingest-auto run; content already fully covered by existing stub; upgraded status stub→draft; added 3 new source entries. de primary (richest available, no en in the 50 files).

## [2026-06-28 00:05] ingest | Anthropic website scrape — Claude Platform / API features (5 sources)
- source: raw/web/web-claude-platform-claude-by-anthropic-4a8b1dbd.md + 4 lang variants (ja/de/ko/fr)
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/claude-api.md]
- new pages: []
- notes: ingest-auto run; Context Editing feature added to claude-api.md (auto-prunes tool calls/results near context limit). Full Claude Platform feature list: Citations, File API, Skills, Memory, MCP Connectors, Structured Outputs — mostly already in claude-api. en primary + 4 lang stamps.

## [2026-06-28T03:03] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=failed
  - pdf: 0 collected · status=ok
  - youtube: 0 collected · status=failed
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 30 ingested · 20 deferred · status=ok
- lint:
  - 1 broken wikilinks · 25 broken citations · 0 orphans · 20 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-29 00:00] ingest | The New Software Lifecycle (Addy Osmani / Google)
- source: raw/_inbox/web-the-new-software-lifecycle-840140b4.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/sources/the-new-software-lifecycle.md, corpus/ai-engineering/agent-harness.md, corpus/ai-engineering/context-engineering.md]
- new pages: [corpus/ai-engineering/sources/the-new-software-lifecycle.md]
- notes: ingest-auto run (50 pre-filtered files); 10%/90% model/harness split; 6 context types taxonomy; static vs dynamic context; METR study; verification spectrum

## [2026-06-29 00:00] ingest | Agentic Code Review (Addy Osmani)
- source: raw/_inbox/web-agentic-code-review-a6ceec31.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/agentic-coding.md, corpus/software-engineering/cognitive-debt.md]
- new pages: []
- notes: ingest-auto run; Faros AI 22K-dev stats; CodeRabbit 470-PR study; 4-tool heterogeneity experiment (93.4% unique); borrowed confidence; human on the loop; circuit breaker pattern

## [2026-06-29 00:00] ingest | PI Architecture EXPLAINED (Alejandro AO)
- source: raw/_inbox/youtube-gTeujlv8qK0-pi-architecture-explained-agent-loop-tools-tui-and-more.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/pi-agent.md]
- new pages: []
- notes: ingest-auto run; 6-step init sequence; JSONL tree sessions; RPC/SDK access mode

## [2026-06-29 00:00] ingest | Joe Reis data engineering suite (4 sources)
- source: raw/_inbox/web-where-data-engineering-is-heading-in-2026-5-trends-fe513e25.md, web-the-insanity-of-data-education-c2478cdc.md, web-2028-the-great-data-reckoning-73fdab45.md, web-the-reckoning-is-already-here-f010ee9f.md
- channel: web
- domain: data-engineering, ai-business
- pages touched: [corpus/data-engineering/data-modeling-meaning.md, corpus/data-engineering/data-engineer-role.md, corpus/ai-business/ai-and-the-job-market.md]
- new pages: []
- notes: ingest-auto run; 89% pain/59% time pressure/51% ownership void (1,101 survey); bifurcation scenario ($400K+ vs AI reviewer); tribal knowledge survival; Joe Reis reckoning

## [2026-06-29 00:00] ingest | Hermes Agent suite (4 YouTube sources)
- source: raw/_inbox/youtube-y4hiT-j5J24-..., youtube-mTYxpIRK7xA-..., youtube-u6L9aedHqZc-..., youtube-yzlvDnxvi1I-...
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/hermes.md]
- new pages: []
- notes: ingest-auto run; Minimax M3 MSA architecture (1M context at 1/20th compute); $0.60/$2.40 pricing; 24/7 always-on practicality

## [2026-06-29 00:00] ingest | Build 3 Production AI Agents (AgentSpan, Tech With Tim)
- source: raw/_inbox/youtube-zFw19qGAeGo-build-3-production-ai-agents-in-python-full-course-agentspan.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/multi-agent-systems.md]
- new pages: []
- notes: ingest-auto run; 7 production requirements; worker+server architecture; crash recovery; observability dashboard

## [2026-06-29 00:00] ingest | Long-running Agents (Addy Osmani — inbox duplicate)
- source: raw/_inbox/web-long-running-agents-322a7b71.md
- channel: web
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/long-running-agents.md]
- new pages: []
- notes: ingest-auto run; same article as raw/web/long-running-agents.md (already ingested 2026-06-16); source append only

## [2026-06-29 00:00] ingest | The Complete Guide to AI Agents in 2026 (Tech With Tim)
- source: raw/_inbox/youtube-LNkAW4SSgdY-the-complete-guide-to-ai-agents-in-2026-and-how-to-actually.md
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-agent.md]
- new pages: []
- notes: ingest-auto run; 4-level framework corroboration (chat→tools→workflows→agents); existing framework from kwRTUw8pb2c confirmed

## [2026-06-29T03:01] config | scheduled run
- collectors:
  - gmail: 0 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 29 collected · status=ok
  - github_discover: 0 collected · status=ok
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 14 ingested · 9 deferred · status=ok
- lint:
  - 1 broken wikilinks · 44 broken citations · 0 orphans · 20 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-29 03:30] query (origin: helix) | Systematic crypto trend-following / time-series momentum: realistic Sharpe/drawdowns, backtest-overfitting safeguards (walk-forward, Deflated Sharpe Ratio, purged/embargoed CV), fractional-Kelly sizing, volatility targeting
- gap: Corpus 'trading' domain covers only AI-agent trading-bot architecture (cron loops, memory files, Claude Code builds). No quantitative-finance content: no time-series-momentum return/Sharpe evidence, no backtest-overfitting safeguards (walk-forward / Deflated Sharpe / purged-embargoed CV), no Kelly/fractional-Kelly sizing, no volatility targeting. Web top-up blocked: WebSearch permission not granted this session.
- queued: none

## [2026-06-30 00:00] ingest | ingest-auto batch — AI agents cluster (YouTube: Marina Wyss, Nick Saraev, Nate Herk, AI Founders, Marius Arvinte, freeCodeCamp ×2, DLO Brands NotebookLM)
- source: raw/_inbox/ (8 YouTube files — see sources list in ai-agent.md, multi-agent-systems.md, agent-skills.md, notebooklm.md, claude-subagents.md)
- channel: youtube
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/ai-agent.md, corpus/ai-engineering/multi-agent-systems.md, corpus/ai-engineering/agent-skills.md]
- new pages: [corpus/ai-engineering/notebooklm.md, corpus/ai-engineering/claude-subagents.md, corpus/ai-engineering/sources/marina-wyss-ai-agents-course.md, corpus/ai-engineering/sources/nick-saraev-ai-agents-course-2026.md, corpus/ai-engineering/sources/nate-herk-claude-subagents.md, corpus/ai-engineering/sources/ai-founders-claude-notebooklm.md]
- notes: ingest-auto run; 8 YouTube sources → 4 new source pages + 2 new concept/entity pages + 3 updated existing pages

## [2026-06-30 00:01] ingest | ingest-auto batch — dbt Summit 2026 (18 web: speaker bios + training page)
- source: raw/_inbox/web-*-dbt-summit-*.md (18 files: Tristan Handy, Quigley Malcolm, Stefanos Nikolaou, Thomas Antonakis, Sarah Levy, training page + 12 additional bios)
- channel: web
- domain: data-engineering
- pages touched: [corpus/data-engineering/dbt.md]
- new pages: [corpus/data-engineering/sources/dbt-summit-2026-speakers.md]
- notes: ingest-auto run; 20 thin bio pages batched into 1 source page; 5 notable speakers featured; 6 training courses catalogued

## [2026-06-30 00:02] ingest | ingest-auto batch — Joe Reis articles (15 web: 2026 DE survey, job market, lessons, moats, booms/busts, bay area)
- source: raw/_inbox/web-*.md (15 Joe Reis Practical Data Community articles)
- channel: web
- domain: data-engineering, ai-business
- pages touched: [corpus/data-engineering/ai-impact-on-data-engineering.md, corpus/data-engineering/data-modeling-meaning.md, corpus/data-engineering/dbt.md, corpus/ai-business/ai-and-the-job-market.md]
- new pages: [corpus/data-engineering/vibe-engineering.md]
- notes: ingest-auto run; 82% DE daily AI usage (n=1101), 59% modeling pressure, job market data (45%/58% AI posting requirements); vibe engineering concept extracted

## [2026-06-30 00:03] ingest | ingest-auto batch — Addy Osmani cognitive articles (2 web: cognitive-surrender, don-t-outsource-the-learning)
- source: raw/_inbox/web-cognitive-surrender-be38214f.md, raw/_inbox/web-don-t-outsource-the-learning-173a7539.md
- channel: web
- domain: software-engineering
- pages touched: [corpus/software-engineering/cognitive-debt.md]
- new pages: []
- notes: ingest-auto run; Wharton Shaw & Nave study (73% accepted AI wrong answers), MIT EEG study (83%), CHI 2026 LLM framing effect; offloading vs surrender distinction

## [2026-06-30 00:04] ingest | ingest-auto batch — AI transition economics + tokenmaxxing (4 web)
- source: raw/_inbox/web-we-re-in-1905-*.md, raw/_inbox/web-notes-from-the-field-*.md, raw/_inbox/web-why-tokenmaxxing-*.md, raw/_inbox/web-surviving-the-ai-grind-*.md
- channel: web
- domain: ai-business, productivity
- pages touched: []
- new pages: [corpus/ai-business/ai-transition-economics.md, corpus/productivity/tokenmaxxing.md]
- notes: ingest-auto run; Paul David 1905 electricity analogy + field notes; Joe Reis + Eric Weber centaur vs reverse centaur framing

## [2026-06-30 00:05] ingest | ingest-auto batch — productivity + knowledge work (1 youtube: AI Founders Claude+NotebookLM)
- source: raw/_inbox/youtube-yeFNKgRst9o-*.md (already counted in AI agents cluster; also updated ai-augmented-knowledge-work.md)
- channel: youtube
- domain: productivity
- pages touched: [corpus/productivity/ai-augmented-knowledge-work.md]
- new pages: []
- notes: consumer vs founder/engine mode; 3 Claude+NotebookLM chains linked to notebooklm.md

## [2026-06-30T03:11] config | scheduled run
- collectors:
  - gmail: 2 collected · status=ok
  - obsidian: 4 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 24 collected · status=ok
  - github_discover: 0 collected · status=ok
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 41 ingested · 9 deferred · status=ok
- lint:
  - 1 broken wikilinks · 87 broken citations · 0 orphans · 20 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-06-30 14:00] lint | weekly synthesis+lint pass (Medium, Opus) — scoped to the week's 31 changed pages + neighbours
- scope: corpus pages changed in the last week (Joe Reis DE/transition cluster, 2026 AI-agent courses, Claude verticals, local-agents, tmux/Herder, Go, dbt-summit, NotebookLM, subagents)
- citation fixes: repointed all `raw/_inbox/<file>` citations + `sources:` paths to the real channel folder on 13 pages (the auto-ingest moved files `_inbox`→`raw/web`/`raw/youtube` after writing the pages); for the 6 source pages (3-deep) also corrected link depth `../../raw/` → `../../../raw/`; fixed skytrax's `email` footnote depth. All 44 raw-citation links + all frontmatter paths on the touched files now resolve (verified).
  - 2-deep pages: vibe-engineering, tokenmaxxing, notebooklm, claude-subagents, ai-transition-economics, perplexity-computer, openclaw
  - 3-deep source pages: the-new-software-lifecycle, nick-saraev-ai-agents-course-2026, nate-herk-claude-subagents, marina-wyss-ai-agents-course, dbt-summit-2026-speakers, ai-founders-claude-notebooklm, skytrax-dbt-transformation-project
- cross-links (typed): wired the three Joe Reis pages (vibe-engineering ↔ tokenmaxxing ↔ ai-transition-economics) to each other and to the new synthesis; vibe-engineering → dbt-summit (Euno/Sarah Levy "AI context platform"); companion-source links Marina Wyss ↔ Nick Saraev (both 2026 agent courses).
- contradictions: none requiring resolution. Apparent tension (Nate Herk "sub-agents can't talk to each other" vs Nick Saraev "agent chat rooms") is not a contradiction — Herk describes Claude Code's built-in orchestrator↔subagent mechanism; Saraev describes MCP-connected separate agents. Left as-is; both route to multi-agent-systems.
- new synthesis: corpus/data-engineering/data-work-in-the-ai-transition.md — names Joe Reis's 2026 one-argument-three-scales thesis (skills/productivity/architecture) with reverse-centaur as the connective failure mode; 5 sources, every non-trivial claim cited.
- index: Total pages 300→301; added the synthesis to the data-engineering list; Recent-additions entry appended.
- note: corpus-wide lint still reports ~43 other broken citations on pages OUTSIDE this week's scope (same inbox→channel drift from earlier ingests) — out of scope for this bounded pass; flag for a full `lint` run.

## [2026-07-01 00:00] ingest | ingest-auto batch — 27 ingested, 23 deferred
- source: raw/_inbox/ (50 pre-specified files)
- channel: web (all 50)
- domain: data-engineering (primary), ai-engineering, software-engineering, ai-business
- pages touched: [dbt, dbt-fusion, scd2, pipeline-optimization-at-scale, sources/dbt-summit-2026-speakers, data-engineering-interview, duckdb, semantic-layer, apache-spark, matthew-housley, engineering-craft, ai-and-the-job-market, sources/the-mythos-threshold, chip-huyen]
- new pages: [data-engineering/dbt-fusion, data-engineering/pipeline-optimization-at-scale, data-engineering/matthew-housley, ai-engineering/sources/the-mythos-threshold, ai-engineering/chip-huyen]
- notes: ingest-auto run; 50 processed, 27 ingested, 23 deferred. Key ingests: dbt Fusion (Rust engine, SDF acq, 30× speedup), pipeline war stories (Airbnb/Meta Zach Wilson), Joe Reis AGI speculative fiction, Chip Huyen entity, Matthew Housley entity, Comet Spark accelerator, DuckDB 1TB benchmark + zonemap index, DE interview 2025 roadmap+resume tips, engineering-craft AI-equalizer thesis. Deferred: thin newsletter digests, paywall stubs, multi-topic podcasts.

## [2026-07-01T02:55] config | scheduled run
- collectors:
  - gmail: 6 collected · status=ok
  - obsidian: 0 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 18 collected · status=ok
  - github_discover: 0 collected · status=ok
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 27 ingested · 23 deferred · status=ok
- lint:
  - 1 broken wikilinks · 63 broken citations · 1 orphans · 22 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-07-02 00:00] ingest | ingest-auto batch — 25 ingested, 25 deferred
- source: raw/_inbox/ (50 pre-specified files)
- channel: web (all 50)
- domain: ai-engineering (23 Ollama + 1 OpenClaw), data-engineering (ETL-is-Dead), mlops (vLLM TTS)
- pages touched: [corpus/ai-engineering/openclaw.md, corpus/data-engineering/etl-pipeline.md, corpus/mlops/model-serving.md, corpus/ai-engineering/README.md]
- new pages: [corpus/ai-engineering/ollama.md]
- notes: ingest-auto run; 50 processed, 25 ingested, 25 deferred. Key ingests: Ollama entity page (new — 23 blog posts Jul 2025–Jun 2026: new app, cloud models, gpt-oss, model scheduling, web search API, ollama launch, OpenClaw integration, GGUF v0.30, MLX Apple Silicon GA, Anthropic API compat, subagents+web-search in Claude Code, DGX Spark benchmarks, Nemotron 3 Ultra); ECL framework (ETL-is-Dead → etl-pipeline.md); vLLM-Omni TTS engineering patterns (→ model-serving.md: stage separation, torch.compile whole-model, CFM batching, GPU-resident state, model-specific Triton kernel). Deferred: 13 paywalled dataexpert.io Substack stubs, newsletter digests, sweepstakes legal text, dbt stub, vLLM+Ollama blog index pages.

## [2026-07-02T02:43] config | scheduled run
- collectors:
  - gmail: 4 collected · status=ok
  - obsidian: 2 collected · status=ok
  - pdf: 0 collected · status=ok
  - youtube: 17 collected · status=ok
  - github_discover: 0 collected · status=ok
  - github: 0 collected · status=ok
  - x: 0 collected · status=ok
  - links_refetch: 0 refetched · status=ok
- ingest:
  - ingest: 25 ingested · 25 deferred · status=ok
- lint:
  - 1 broken wikilinks · 80 broken citations · 1 orphans · 22 stubs  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py

## [2026-07-02 00:00] ingest | ingest-auto batch — vLLM ecosystem + OpenJarvis (6 sources)
- source: raw/_inbox/ (6 pre-specified files)
- channel: web (all 6)
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/README.md, corpus/ai-engineering/ollama.md, corpus/ai-engineering/local-ai-agents.md, corpus/ai-engineering/mixture-of-experts.md]
- new pages: [corpus/ai-engineering/openjarvis.md, corpus/ai-engineering/vllm.md, corpus/ai-engineering/vllm-semantic-router.md, corpus/ai-engineering/minimax-m3.md, corpus/ai-engineering/diffusiongemma.md, corpus/ai-engineering/vime.md]
- notes: ingest-auto run; 6 processed, 6 ingested, 0 deferred. New vLLM ecosystem cluster: vLLM entity hub (serving engine internals, ModelState abstraction), vLLM Semantic Router (Fusion Mixture-of-Models, Session-Aware Agentic Routing, Themis v0.3 release), MiniMax M3 (MiniMax Sparse Attention, 1M-token context), DiffusionGemma (first diffusion LLM natively in vLLM), vime (RL post-training framework, slime+Megatron+vLLM). Plus OpenJarvis (Stanford Hazy Research local-first agent framework on Ollama) — cross-linked into Ollama and Local AI Agents. All 6 sources routed to existing ai-engineering domain; no contradictions; all new pages linked from domain hub.

## [2026-07-02] ingest | ingest-auto follow-up batch — vLLM ecosystem cluster (6 processed, 6 ingested, 0 deferred)
- source: raw/_inbox/web-announcing-day-0-support-for-nvidia-nemotron-3-ultra-on-vllm-bc7c306b.md
- source: raw/_inbox/web-fast-efficient-llm-inference-with-vllm-a-new-course-with-dee-f75c7aa9.md
- source: raw/_inbox/web-session-aware-agentic-routing-continuity-aware-model-selecti-1950138f.md
- source: raw/_inbox/web-accelerating-vllm-omni-inference-with-autoround-quantization-f55f7ca2.md
- source: raw/_inbox/web-vllm-on-the-dgx-spark-architecture-configuration-and-local-e-543e2b72.md
- source: raw/_inbox/web-accelerating-laguna-xs-2-inference-with-vllm-speculators-and-afda11cd.md
- channel: web (all 6)
- domain: ai-engineering
- pages touched: [corpus/ai-engineering/vllm.md, corpus/ai-engineering/vllm-semantic-router.md, corpus/ai-engineering/README.md]
- new pages: [corpus/ai-engineering/nemotron-3-ultra.md, corpus/ai-engineering/laguna-xs2.md, corpus/ai-engineering/quantization.md]
- notes: ingest-auto run; 6 processed, 6 ingested, 0 deferred. Same-day continuation of the vLLM ecosystem cluster started earlier today. New pages: Nemotron 3 Ultra (NVIDIA's hybrid Transformer-Mamba MoE agentic reasoning model, also used as vLLM's own RL rollout/eval backend), Laguna XS.2 (Poolside's agentic-coding MoE model + DFlash speculative decoder), and Quantization (new concept: AutoRound PTQ for vLLM-Omni, NVFP4 on DGX Spark, LLM Compressor checkpoints for Laguna XS.2 — the memory-headroom-unlocks-parallelism pattern from the AutoRound CFG-Parallel case study). Updated vllm.md with a DGX Spark local single-GPU deployment section (unified-memory flag guidance, sm_121 validation, cold-start JIT warmup) and the DeepLearning.AI "Fast & Efficient LLM Inference with vLLM" course. Updated vllm-semantic-router.md with full SAAR (Session-Aware Agentic Routing) design detail — five-piece router memory, two hard locks as correctness boundaries, evaluated results across 21,600 deterministic turns and live AMD ROCm serving — expanding the passing SAAR mention already present from the Themis v0.3 source. All 6 sources routed to existing ai-engineering domain (G1 clear); no PARA-native collisions (G4); no contradictions with existing pages (G3); page cascade well under 20 (G2). All new pages linked from domain hub; no orphans.

## [2026-07-02T06:26] config | scheduled run
- collectors:

- ingest:
  - ingest: 6 ingested · 0 deferred · status=ok
- youtube_quick:
  - youtube_quick: 0 intake · 0 rescued · 3 skipped · status=ok
- lint:
  - 0 broken wikilinks · 0 broken citations · 0 orphans · 0 stubs
