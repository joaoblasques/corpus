---
type: hub
domain: software-engineering
status: draft
tags:
  - corpus/software-engineering
  - hub
created: 2026-05-07
updated: 2026-07-07
---

# Software Engineering

Domain covering software engineering practice from foundational CS through deployment infrastructure — data structures, code design principles, API frameworks, distributed systems patterns, and container orchestration. Renamed from software-architecture 2026-05-22 to reflect actual scope.

## Pages

### Entities
- [FastAPI](/software-engineering/fastapi.md) — entity · draft · Python API framework; Pydantic validation, dependency injection via Depends(), JWT auth, SQLAlchemy integration
- [Kubernetes](/software-engineering/kubernetes.md) — entity · draft · container orchestration; Pod/Deployment/Service/Namespace; runtime platform for microservices
- [Xonsh](/software-engineering/xonsh.md) — entity · draft · a Python-superset shell; objects/imports/stdlib alongside cd, pipes, and aliases
- [InsForge](/software-engineering/insforge.md) — entity · draft · all-in-one open-source backend operated by a coding agent via MCP or CLI + Skills
- [Git Basics](/software-engineering/git-basics.md) — entity · draft · distributed VCS; DAG commit model, branching (sticky notes), HEAD, reset/revert/rebase, reflog, PR workflow, Oh Shit Git
- [Kan](/software-engineering/kan.md) — entity · stub · open-source Trello alternative; Next.js + tRPC + Drizzle + Better Auth stack
- [Vim](/software-engineering/vim.md) — entity · stub · modal text editor; vim-galore reference; composable motions/operators/text-objects; Neovim extension
- [Usertour](/software-engineering/usertour.md) — entity · stub · open-source user onboarding platform; product tours, checklists, NPS surveys; TypeScript; alternative to Appcues/Userflow
- [React](/software-engineering/react.md) — entity · stub · JavaScript UI library; JSX; component model; React Enlightenment (FrontendMasters) reference
- [Bun](/software-engineering/bun.md) — entity · stub · all-in-one JS/TS toolkit; runtime + package manager + test runner + bundler; Node.js compatible

### Concepts
- [Terminal / CLI Tools](/software-engineering/terminal-cli-tools.md) — concept · draft · Mac terminal keyboard shortcuts; core bash commands; navigation, history, process control
- [Microservices](/software-engineering/microservices.md) — concept · draft · architectural style decomposing systems into small independent services; pitfalls, granularity, data management
- [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md) — concept · draft · eight fallacies; sourced failure modes for network reliability, latency, topology change, and security; fallacies 3/6/7/8 awaiting dedicated source
- [Container Patterns (Single-Node)](/software-engineering/container-patterns.md) — concept · draft · sidecar/ambassador/adapter patterns for containerized distributed systems; reuse philosophy; design principles
- [Scatter/Gather Pattern](/software-engineering/scatter-gather-pattern.md) — concept · draft · fan-out to all leaf nodes, merge partial results; straggler amplification math; replicated-sharded variant
- [Software Design Principles](/software-engineering/software-design-principles.md) — concept · draft · 8 code-level principles (SRP, cohesion, loose coupling, DI, open/closed, simplicity) separating maintainable from fragile code
- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — concept · draft · time complexity classes and trade-off table for 8 core data structures
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md) — concept · draft · six interview categories: recursion, linear/binary search, sorting, pathfinding (Dijkstra), MST (Prim's), dynamic programming / memoization; strategies-not-tricks framing
- [CAP Theorem](/software-engineering/cap-theorem.md) — concept · draft · pick CP or AP under network partitions; CAP vs ACID consistency
- [AI Risk Architecture](/software-engineering/ai-risk-architecture.md) — concept · draft · data/output/action risk; risk is a system property, not a component
- [Engineering Craft](/software-engineering/engineering-craft.md) — concept · draft · resourcefulness, curiosity, persistence; seniority redefined under AI, staying-current habits (innovation budget), learning loops (mutual amplification, adversarial mentor)
- [Cognitive Debt and Cognitive Surrender](/software-engineering/cognitive-debt.md) — concept · stub · erosion of understanding from over-deferring to AI; cognitive surrender, three models of debt (Storey), the orchestration tax
- [Compiler-Warning Management](/software-engineering/compiler-warning-management.md) — concept · draft · Git's `false_but_the_compiler_does_not_know_it_` trick; suppress a specific false-positive warning without disabling it globally; eliminated under LTO
- [Local-First Sync Architecture](/software-engineering/local-first-sync-architecture.md) — concept · draft · browser-as-database + optimistic mutations + granular reactivity; server as sync target not source of truth (reverse-engineered from Linear)
- [Test-Case Reduction](/software-engineering/test-case-reduction.md) — concept · draft · automatically shrink a failing input to a minimal reproducer via an interestingness test; ddmin/creduce/Shrink Ray; steering beyond input length

### Concepts (continued)
- See also: [Go](/software-engineering/go-programming-language.md), [JavaScript](/software-engineering/javascript-fundamentals.md) under Languages above; [Terminal/CLI](/software-engineering/terminal-cli-tools.md) and [Vim](/software-engineering/vim.md) under tools

### Syntheses
- [AI-Assisted Development](/software-engineering/ai-assisted-development.md) — synthesis · draft · fundamentals under AI; the write→review shift; deterministic guardrails for AI code

### Languages and tools
- [Go Programming Language](/software-engineering/go-programming-language.md) — concept · draft · statically typed, compiled; goroutines; 120x faster than Python; zero-value defaults; error-as-return-type pattern; use-case matrix (backend/infra/CLI yes; data science/frontend no)
- [JavaScript Fundamentals](/software-engineering/javascript-fundamentals.md) — concept · draft · web language; var/let/const scoping; template literals; clean-code-JS; npm; 3 algorithm+quiz reference repos; 15-project learning-by-building curriculum

### System design and infrastructure
- [System Design Fundamentals](/software-engineering/system-design-fundamentals.md) — concept · draft · scaling strategies; load balancing algorithms; SQL vs NoSQL selection; REST/GraphQL/gRPC; ACID; frontend patterns (microfrontends, BFF, CDN, design systems, API gateway); OSI protocols; auth vs authz
- [CI/CD, Progressive Delivery, and GitOps](/software-engineering/ci-cd.md) — concept · draft · CI/CD maturity ladder; canary/blue-green/feature flags; GitOps four pillars; platform teams; roll-forward over rollback; GitHub Actions (events/jobs/steps/runners/actions)

### OS and Systems
- [Operating Systems](/software-engineering/operating-systems.md) — concept · draft · process abstraction (machine state, PCB, process API); limited direct execution; mechanism vs policy; fork/exec/wait
- [CPU Scheduling](/software-engineering/cpu-scheduling.md) — concept · draft · FIFO, SJF, STCF, Round Robin, MLFQ, lottery scheduling, multi-CPU scheduling; turnaround vs response time tradeoff
- [Virtual Memory](/software-engineering/virtual-memory.md) — concept · draft · address translation; base+bounds; segmentation; paging; TLBs; multi-level page tables; free-space management; swapping; page replacement (FIFO, LRU, clock algorithm)
- [Virtual Machine Monitors](/software-engineering/virtual-machine-monitors.md) — concept · draft · VMMs/hypervisors; CPU and memory virtualization via limited direct execution; shadow page tables; para-virtualization; Disco/VMware history
- [Concurrency and Threads](/software-engineering/concurrency-and-threads.md) — concept · draft · pthreads API; locks, condition variables; monitors (Mesa semantics); atomicity violations, deadlock (4 conditions + prevention); producer-consumer pattern
- [File Systems](/software-engineering/file-systems.md) — concept · draft · inode layout, crash consistency, journaling (WAL), FFS cylinder groups, LFS append-only log, SSD FTL, RAID 0/1/4/5
- [Distributed File Systems](/software-engineering/distributed-file-systems.md) — concept · draft · NFS stateless protocol; idempotent ops; client-side caching; AFS whole-file caching + callback promises
- [OS Security](/software-engineering/os-security.md) — concept · draft · authentication (MFA, salted hashes), access control (ACL/RBAC/MAC/Unix model), cryptography (symmetric/asymmetric/AEAD), distributed security (Kerberos, TLS/PKI)

- [Complexity Theory and NP-Completeness](/software-engineering/complexity-theory.md) — concept · draft · P vs NP; NP-complete problems; polynomial-time reductions; average-case vs worst-case; approximation algorithms

### Sources
- [OSTEP: Operating Systems — Three Easy Pieces (Arpaci-Dusseau, 2023)](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — source · draft · 47-chapter free textbook; virtualization, concurrency, persistence, security; xv6 lab companion
- [Designing Distributed Systems (Burns, O'Reilly, 2018)](/software-engineering/sources/burns-designing-distributed-systems.md) — source · draft · pattern catalog for container-based distributed systems: sidecar/ambassador/adapter (single-node), replicated/sharded/scatter-gather (multi-node), batch patterns
- [The Software Engineer's Guidebook](/software-engineering/sources/software-engineers-guidebook.md) — source · draft · Gergely Orosz; full career arc from new dev to staff; six-part reference book
- [Go Course with Bonus Projects (boot.dev / freeCodeCamp)](/software-engineering/sources/go-course-boot-dev.md) — source · draft · Lane Wagner; 100+ lessons + 7 projects; Textio running example; RSS-aggregator capstone (chi/sqlc/Goose, API-key auth)
- [Go Programming Full Course (Tech With Tim)](/software-engineering/sources/go-full-course-tech-with-tim.md) — source · draft · 21-lesson syntax-first course; slice internals, value/pointer receivers, goroutines + channels
- [Algorithms and Complexity (Wilf, 1994)](/software-engineering/sources/algorithms-and-complexity-wilf.md) — source · draft · Herbert Wilf; 139p; recursion/FFT, network flow (Ford-Fulkerson), number theory, NP-completeness; free educational use
- [Algorithms (Erickson, 2019)](/software-engineering/sources/algorithms-erickson.md) — source · draft · Jeff Erickson (UIUC); 472p; recursion → divide-and-conquer → DP → greedy → graph algorithms → MST → shortest paths → network flow → NP-hardness; CC BY 4.0

## Sources ingested
- [Disasters I've Seen in a Microservices World](/03_Resources/Articles/Disasters in a Microservices World.md) — article note, João Alves / Hey World, 2025-10-30
- [Python - Production Code Principles Senior Developer](/03_Resources/Study Notes/Python - Production Code Principles Senior Developer.md) — YouTube tutorial (Tech With Tim, 29 min), 2026-03-16
- [Data Structures and Big O Notation Explained](/03_Resources/Study Notes/Data Structures and Big O Notation Explained.md) — YouTube tutorial (Sajjaad Khader, 16 min), 2025-03-06
- [Python - FastAPI Complete Course with Auth and Database](/03_Resources/Study Notes/Python - FastAPI Complete Course with Auth and Database.md) — YouTube course (Tech With Tim, 125 min), 2026-03-16
- [DevOps - Kubernetes Complete Course for Beginners](/03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md) — YouTube course (TechWorld with Nana, 216 min), 2026-03-16
