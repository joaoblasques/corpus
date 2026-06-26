---
type: hub
domain: software-engineering
status: draft
tags:
  - corpus/software-engineering
  - hub
created: 2026-05-07
updated: 2026-06-25
---

# Software Engineering

Domain covering software engineering practice from foundational CS through deployment infrastructure — data structures, code design principles, API frameworks, distributed systems patterns, and container orchestration. Renamed from software-architecture 2026-05-22 to reflect actual scope.

## Pages

### Entities
- [[software-engineering/fastapi|FastAPI]] — entity · draft · Python API framework; Pydantic validation, dependency injection via Depends(), JWT auth, SQLAlchemy integration
- [[software-engineering/kubernetes|Kubernetes]] — entity · draft · container orchestration; Pod/Deployment/Service/Namespace; runtime platform for microservices
- [[software-engineering/xonsh|Xonsh]] — entity · draft · a Python-superset shell; objects/imports/stdlib alongside cd, pipes, and aliases
- [[software-engineering/insforge|InsForge]] — entity · draft · all-in-one open-source backend operated by a coding agent via MCP or CLI + Skills
- [[software-engineering/git-basics|Git Basics]] — entity · draft · distributed VCS; DAG commit model, branching (sticky notes), HEAD, reset/revert/rebase, reflog, PR workflow, Oh Shit Git
- [[software-engineering/kan|Kan]] — entity · stub · open-source Trello alternative; Next.js + tRPC + Drizzle + Better Auth stack
- [[software-engineering/vim|Vim]] — entity · stub · modal text editor; vim-galore reference; composable motions/operators/text-objects; Neovim extension
- [[software-engineering/usertour|Usertour]] — entity · stub · open-source user onboarding platform; product tours, checklists, NPS surveys; TypeScript; alternative to Appcues/Userflow
- [[software-engineering/react|React]] — entity · stub · JavaScript UI library; JSX; component model; React Enlightenment (FrontendMasters) reference
- [[software-engineering/bun|Bun]] — entity · stub · all-in-one JS/TS toolkit; runtime + package manager + test runner + bundler; Node.js compatible

### Concepts
- [[software-engineering/terminal-cli-tools|Terminal / CLI Tools]] — concept · draft · Mac terminal keyboard shortcuts; core bash commands; navigation, history, process control
- [[software-engineering/microservices|Microservices]] — concept · draft · architectural style decomposing systems into small independent services; pitfalls, granularity, data management
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — concept · draft · eight fallacies; sourced failure modes for network reliability, latency, topology change, and security; fallacies 3/6/7/8 awaiting dedicated source
- [[software-engineering/software-design-principles|Software Design Principles]] — concept · draft · 8 code-level principles (SRP, cohesion, loose coupling, DI, open/closed, simplicity) separating maintainable from fragile code
- [[software-engineering/data-structures|Data Structures and Big O Notation]] — concept · draft · time complexity classes and trade-off table for 8 core data structures
- [[software-engineering/algorithms|Algorithms (Strategies, Not Tricks)]] — concept · draft · six interview categories: recursion, linear/binary search, sorting, pathfinding (Dijkstra), MST (Prim's), dynamic programming / memoization; strategies-not-tricks framing
- [[software-engineering/cap-theorem|CAP Theorem]] — concept · draft · pick CP or AP under network partitions; CAP vs ACID consistency
- [[software-engineering/ai-risk-architecture|AI Risk Architecture]] — concept · draft · data/output/action risk; risk is a system property, not a component
- [[software-engineering/engineering-craft|Engineering Craft]] — concept · draft · resourcefulness, curiosity, persistence; seniority redefined under AI, staying-current habits (innovation budget), learning loops (mutual amplification, adversarial mentor)
- [[software-engineering/cognitive-debt|Cognitive Debt and Cognitive Surrender]] — concept · stub · erosion of understanding from over-deferring to AI; cognitive surrender, three models of debt (Storey), the orchestration tax
- [[software-engineering/compiler-warning-management|Compiler-Warning Management]] — concept · draft · Git's `false_but_the_compiler_does_not_know_it_` trick; suppress a specific false-positive warning without disabling it globally; eliminated under LTO
- [[software-engineering/local-first-sync-architecture|Local-First Sync Architecture]] — concept · draft · browser-as-database + optimistic mutations + granular reactivity; server as sync target not source of truth (reverse-engineered from Linear)
- [[software-engineering/test-case-reduction|Test-Case Reduction]] — concept · draft · automatically shrink a failing input to a minimal reproducer via an interestingness test; ddmin/creduce/Shrink Ray; steering beyond input length

### Concepts (continued)
- See also: [[software-engineering/go-programming-language|Go]], [[software-engineering/javascript-fundamentals|JavaScript]] under Languages above; [[software-engineering/terminal-cli-tools|Terminal/CLI]] and [[software-engineering/vim|Vim]] under tools

### Syntheses
- [[software-engineering/ai-assisted-development|AI-Assisted Development]] — synthesis · draft · fundamentals under AI; the write→review shift; deterministic guardrails for AI code

### Languages and tools
- [[software-engineering/go-programming-language|Go Programming Language]] — concept · draft · statically typed, compiled; goroutines; 120x faster than Python; zero-value defaults; error-as-return-type pattern; use-case matrix (backend/infra/CLI yes; data science/frontend no)
- [[software-engineering/javascript-fundamentals|JavaScript Fundamentals]] — concept · draft · web language; var/let/const scoping; template literals; clean-code-JS; npm; 3 algorithm+quiz reference repos; 15-project learning-by-building curriculum

### System design and infrastructure
- [[software-engineering/system-design-fundamentals|System Design Fundamentals]] — concept · draft · scaling strategies; load balancing algorithms; SQL vs NoSQL selection; REST/GraphQL/gRPC; ACID; frontend patterns (microfrontends, BFF, CDN, design systems, API gateway); OSI protocols; auth vs authz
- [[software-engineering/ci-cd|CI/CD, Progressive Delivery, and GitOps]] — concept · draft · CI/CD maturity ladder; canary/blue-green/feature flags; GitOps four pillars; platform teams; roll-forward over rollback; GitHub Actions (events/jobs/steps/runners/actions)

### Sources
- [[software-engineering/sources/software-engineers-guidebook|The Software Engineer's Guidebook]] — source · draft · Gergely Orosz; full career arc from new dev to staff; six-part reference book
- [[software-engineering/sources/go-course-boot-dev|Go Course with Bonus Projects (boot.dev / freeCodeCamp)]] — source · draft · Lane Wagner; 100+ lessons + 7 projects; Textio running example; RSS-aggregator capstone (chi/sqlc/Goose, API-key auth)
- [[software-engineering/sources/go-full-course-tech-with-tim|Go Programming Full Course (Tech With Tim)]] — source · draft · 21-lesson syntax-first course; slice internals, value/pointer receivers, goroutines + channels

## Sources ingested
- [[03_Resources/Articles/Disasters in a Microservices World|Disasters I've Seen in a Microservices World]] — article note, João Alves / Hey World, 2025-10-30
- [[03_Resources/Study Notes/Python - Production Code Principles Senior Developer|Python - Production Code Principles Senior Developer]] — YouTube tutorial (Tech With Tim, 29 min), 2026-03-16
- [[03_Resources/Study Notes/Data Structures and Big O Notation Explained|Data Structures and Big O Notation Explained]] — YouTube tutorial (Sajjaad Khader, 16 min), 2025-03-06
- [[03_Resources/Study Notes/Python - FastAPI Complete Course with Auth and Database|Python - FastAPI Complete Course with Auth and Database]] — YouTube course (Tech With Tim, 125 min), 2026-03-16
- [[03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners|DevOps - Kubernetes Complete Course for Beginners]] — YouTube course (TechWorld with Nana, 216 min), 2026-03-16
