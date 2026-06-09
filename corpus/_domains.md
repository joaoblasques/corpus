# Domains

> The canonical list of active wiki domains. Maintained by Claude on every domain change (create / merge / split). Past decisions inform future routing.

## Active domains

### ai-engineering
- **Status**: active
- **provisional**: false
- **Created**: 2026-05-07
- **Rationale**: Covers LLM internals, agent design, context management, prompt engineering, and AI system architecture. Created under standard rule with 2 sources (Context Engineering, AI Agents course); conceptually distinct from data-engineering.
- **Expected sources**: YouTube playlists on LLM/agent topics, articles on prompting, RAG, multi-agent systems.

### data-engineering
- **Status**: active
- **provisional**: false
- **Graduated**: 2026-05-21
- **Created**: 2026-05-07
- **Rationale**: Covers ETL/ELT pipelines, Spark, Iceberg, dbt, Airflow, data modeling, and cloud data infrastructure. Seeded with 1 source (SCD2/Spark/Iceberg article).
- **Graduation rationale**: 12 pages, 6 sources after Batch 2 ingest — well above 3-source threshold. All pages draft status; zero orphans; zero contradictions. Growth confirmed via DE playlists and DataExpert bootcamp material as predicted.

### software-engineering
- **Status**: active
- **provisional**: false
- **Graduated**: 2026-05-22
- **Renamed from**: software-architecture (2026-05-22)
- **Created**: 2026-05-07
- **Scope**: Software engineering practice spanning foundational CS through deployment infrastructure — data structures, code design principles (SRP, loose coupling, dependency injection), API frameworks, distributed systems patterns, and container orchestration.
- **Exclusion constraint**: Primarily language syntax or framework intros without a design or pattern angle do not route here — a source must engage with how software is designed, structured, or operated. FastAPI is included because its source treats dependency injection, request validation, and auth as design patterns. Data pipeline and ETL tools route to data-engineering; AI/ML frameworks route to ai-engineering.
- **Graduation rationale**: 5 sources, 6 content pages after Batch 3 ingest; ≥3 source threshold exceeded (same criteria as data-engineering graduation). 5 pages draft; distributed-systems-fallacies is stub at 15 days (past 14-day lint threshold) — stub-expansion commitment: sufficient content exists across microservices.md and kubernetes.md to draft an expansion without a new primary source; to be resolved in next wiki session. Zero orphans; zero contradictions. 8-page floor not applied — introduced in Batch 3 brief but absent from schema and prior graduation precedent. Renamed simultaneously with graduation.

### mlops
- **Status**: active
- **provisional**: true
- **Created**: 2026-06-09
- **Rationale**: The engineering substrate for building ML/software systems — development environment setup, version control and ML-artifact handling, GPU/compute provisioning, and infrastructure-as-code. Conceptually distinct from the three content domains: ai-engineering covers LLM internals and agents; data-engineering covers ETL/data modeling; software-engineering covers code design and application architecture. None covers how the underlying engineering environment and infrastructure are provisioned and operated.
- **Seeded by**: 4 sources (Batch 4) — AIEFS course Phase 00 lessons 01 (dev-environment), 02 (git & collaboration), 03 (GPU & cloud), plus a startdataengineering.com IaC/Terraform article.
- **Expected sources**: remaining lessons of "AI Engineering from Scratch" (Phase 00 setup-and-tooling continues; Phase 8 fine-tuning, data-management/DVC, and deployment phases explicitly referenced as upcoming), plus DevOps/infra articles. User confirmed growth (Batch 4 survey).
- **Provisional review**: at 30 days (2026-07-09) — if still under 3 *distinct* sources, propose merge or removal. Currently 4 sources across 2 origins, so the standard ≥3 threshold is already met on count; provisional flag retained one cycle because 3 of 4 sources share a single origin (one course).

---

## Decision log

Each entry: `[YYYY-MM-DD] action | domain | rationale`.

- [2026-05-07] create | ai-engineering | Standard rule: 2 sources, conceptually distinct from DE. User confirmed.
- [2026-05-07] create | data-engineering | Provisional rule: 1 source; user confirmed growth via DE playlists/bootcamp.
- [2026-05-21] graduate | data-engineering | 12 pages, 6 sources after Batch 2; provisional threshold (≥3 sources) exceeded. All pages draft; zero orphans; zero contradictions.
- [2026-05-07] create | software-architecture | Provisional rule: 1 source; user confirmed growth via reading patterns.
- [2026-05-22] rename | software-architecture → software-engineering | Actual post-Batch-3 scope (CS fundamentals → code design → API frameworks → distributed systems → container orchestration) more accurately described as software engineering than architecture. Renamed and graduated simultaneously.
- [2026-05-22] graduate | software-engineering | 5 sources, 6 content pages; ≥3 source threshold met. Same qualitative criteria as data-engineering graduation. distributed-systems-fallacies stub flagged for expansion (next session).
- [2026-05-07] defer | career (candidate) | remote-job-boards file moved to raw/web/ without corpus page. <3 sources to justify domain. Revisit when 2nd career source arrives.
- [2026-06-09] create | mlops | Provisional rule: 4 sources (AIEFS Phase 00 lessons 01/02/03 + IaC/Terraform article) that fit no existing domain; coherent "engineering substrate / infra & tooling" cluster. User confirmed via Batch 4 survey + new-domain question. Provisional flag retained one cycle (3 of 4 sources share one origin); 30-day review 2026-07-09.

---

## Rejected / consolidated domains

- [2026-05-07] rejected | career | Only 1 source (remote-job-boards-data-tech-roles-100k.md). File deferred to raw/web/; no corpus page created. Revisit threshold: 2nd career-related source.
