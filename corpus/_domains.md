---
type: domain-registry
---
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
- **provisional**: false
- **Graduated**: 2026-07-22
- **Created**: 2026-06-09
- **Rationale**: The engineering substrate for building ML/software systems — development environment setup, version control and ML-artifact handling, GPU/compute provisioning, and infrastructure-as-code. Conceptually distinct from the three content domains: ai-engineering covers LLM internals and agents; data-engineering covers ETL/data modeling; software-engineering covers code design and application architecture. None covers how the underlying engineering environment and infrastructure are provisioned and operated.
- **Seeded by**: 4 sources (Batch 4) — AIEFS course Phase 00 lessons 01 (dev-environment), 02 (git & collaboration), 03 (GPU & cloud), plus a startdataengineering.com IaC/Terraform article.
- **Graduation rationale**: 30-day review (due 2026-07-09) run late on 2026-07-22 at user request. 41 pages, sources now span email/github/notes/pdf/web/youtube channels — well past the single-course-origin concern that held the flag. Zero lint failures.

### productivity
- **Status**: active
- **provisional**: false
- **Graduated**: 2026-07-22
- **Created**: 2026-06-12
- **Rationale**: Personal/professional effectiveness for knowledge workers — mental models, time and focus management, note-taking/second-brain practice, working with stakeholders, learning how to learn. Standard rule: 13 sources in the wave-3 email-backlog cluster; fits no engineering domain, conceptually distinct.
- **Note**: this entry was missing from the registry despite being logged as created 2026-06-12 (decision-log entry present, registry section entry absent) — added retroactively 2026-07-22 alongside its graduation.
- **Graduation rationale**: 30-day review (due 2026-07-12) run late on 2026-07-22 (registry gap meant it was never tracked). 10 pages across 6 distinct channels (inbox/youtube/github/email/web). Zero lint failures.

### blockchain
- **Status**: active
- **provisional**: false
- **Graduated**: 2026-07-22
- **Created**: 2026-06-17
- **Rationale**: A coherent cryptocurrency/blockchain-fundamentals cluster (12 substantive sources from a nakamoto.ghost.io primer: money history, the cypherpunks, Satoshi, Bitcoin, proof-of-work, public-key crypto, hash functions, Merkle trees, P2P networking, zero-knowledge proofs) that fits none of the engineering/AI/business domains. Well above the 3-source bar on creation. Distinct subject matter (distributed consensus, cryptographic primitives, monetary theory).
- **Seeded by**: 12 sources (Obsidian Clippings drain, batch 5), collected from `00_Inbox/Clippings/scrape/`.
- **Graduation rationale**: 30-day review (due 2026-07-17) run late on 2026-07-22 at user request. 29 pages across 4 independent origins (nakamoto.ghost.io, Ben-Sasson proof-systems survey, Mastering Bitcoin, Mastering Ethereum) — the single-origin concern that held the flag no longer applies. Zero lint failures.

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
- [2026-06-12] create | productivity | Standard rule: 13 sources in the wave-3 email-backlog cluster (mental models, time/focus, note-taking, working effectively, stakeholder management) fitting no engineering domain; conceptually distinct. Provisional; 30-day review 2026-07-12. User confirmed wave-3 scope (remote-control session).
- [2026-06-12] create | ai-business | Standard rule: 11 sources (career growth, interviews, monetizing technical skills, AI's impact on jobs/consulting). Supersedes the 2026-05-07 "career" rejection (revisit threshold was a 2nd career source; now 11). Provisional; 30-day review 2026-07-12. User confirmed wave-3 scope.
- [2026-06-25] create | trading | Standard rule: 5 sources (one "Auto trading" YouTube playlist: agentic trading bots, Alpaca API, Pine Script, Polymarket, self-improving agents). Provisional; 30-day review 2026-07-25.
- [2026-07-22] graduate | mlops | 30-day review (due 2026-07-09) run late at user request. 41 pages, multi-channel sourcing (email/github/notes/pdf/web/youtube) supersedes the single-course-origin concern. Zero lint failures.
- [2026-07-22] graduate | blockchain | 30-day review (due 2026-07-17) run late at user request. 29 pages, 4 independent origins (nakamoto.ghost.io, Ben-Sasson survey, Mastering Bitcoin, Mastering Ethereum). Zero lint failures.
- [2026-07-22] delete | trading | User request, ahead of its 2026-07-25 provisional review — still single-origin (one playlist), 8 pages, zero query activity since creation. Deleted `corpus/trading/` (README + 8 pages + sources/) entirely; no cross-domain links pointed into it, so no repair needed. Not a merge — content was scoped narrowly enough (AI-driven trading bots) that no existing domain is a natural home; deletion over silent fold.
- [2026-07-22] graduate | productivity | 30-day review (due 2026-07-12) run late — the domain's registry section entry was missing entirely (decision-log create entry existed, registry entry didn't), so the review was never triggered. Added the missing registry entry and graduated in the same pass: 10 pages, 6 distinct channels (inbox/youtube/github/email/web). Zero lint failures. User requested active growth going forward — see book_discover.yaml `relevant_sections` addition same date.
- [2026-06-17] create | blockchain | Standard rule: 12 substantive crypto/blockchain-fundamentals sources (nakamoto.ghost.io primer) fitting no existing domain; coherent and distinct. User confirmed during the Obsidian Clippings drain. Provisional one cycle (single-origin seed); 30-day review 2026-07-17.
- [2026-06-25] create | trading | Standard rule: 5 substantive AI-trading-bot sources (one "Auto trading" YouTube playlist) fitting no existing domain; distinct (broker APIs, market microstructure, strategy encoding, arbitrage). Created autonomously under §0 delegation during the 455-source big-backlog batch ingest (Wave 1). Provisional one cycle (single-origin seed); 30-day review 2026-07-25.

---

## Rejected / consolidated domains

- [2026-05-07] rejected | career | Only 1 source (remote-job-boards-data-tech-roles-100k.md). File deferred to raw/web/; no corpus page created. Revisit threshold: 2nd career-related source.
