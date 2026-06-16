---
type: hub
domain: software-engineering
status: draft
tags:
  - corpus/software-engineering
  - hub
created: 2026-05-07
updated: 2026-06-16
---

# Software Engineering

Domain covering software engineering practice from foundational CS through deployment infrastructure — data structures, code design principles, API frameworks, distributed systems patterns, and container orchestration. Renamed from software-architecture 2026-05-22 to reflect actual scope.

## Pages

### Entities
- [[software-engineering/fastapi|FastAPI]] — entity · draft · Python API framework; Pydantic validation, dependency injection via Depends(), JWT auth, SQLAlchemy integration
- [[software-engineering/kubernetes|Kubernetes]] — entity · draft · container orchestration; Pod/Deployment/Service/Namespace; runtime platform for microservices
- [[software-engineering/xonsh|Xonsh]] — entity · draft · a Python-superset shell; objects/imports/stdlib alongside cd, pipes, and aliases
- [[software-engineering/insforge|InsForge]] — entity · draft · all-in-one open-source backend operated by a coding agent via MCP or CLI + Skills

### Concepts
- [[software-engineering/microservices|Microservices]] — concept · draft · architectural style decomposing systems into small independent services; pitfalls, granularity, data management
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — concept · draft · eight fallacies; sourced failure modes for network reliability, latency, topology change, and security; fallacies 3/6/7/8 awaiting dedicated source
- [[software-engineering/software-design-principles|Software Design Principles]] — concept · draft · 8 code-level principles (SRP, cohesion, loose coupling, DI, open/closed, simplicity) separating maintainable from fragile code
- [[software-engineering/data-structures|Data Structures and Big O Notation]] — concept · draft · time complexity classes and trade-off table for 8 core data structures
- [[software-engineering/algorithms|Algorithms (Strategies, Not Tricks)]] — concept · draft · recursion, binary search (divide & conquer), dynamic programming / memoization; strategies-not-tricks framing
- [[software-engineering/cap-theorem|CAP Theorem]] — concept · draft · pick CP or AP under network partitions; CAP vs ACID consistency
- [[software-engineering/ai-risk-architecture|AI Risk Architecture]] — concept · draft · data/output/action risk; risk is a system property, not a component
- [[software-engineering/engineering-craft|Engineering Craft]] — concept · draft · resourcefulness, curiosity, persistence through difficulty
- [[software-engineering/compiler-warning-management|Compiler-Warning Management]] — concept · draft · Git's `false_but_the_compiler_does_not_know_it_` trick; suppress a specific false-positive warning without disabling it globally; eliminated under LTO
- [[software-engineering/local-first-sync-architecture|Local-First Sync Architecture]] — concept · draft · browser-as-database + optimistic mutations + granular reactivity; server as sync target not source of truth (reverse-engineered from Linear)
- [[software-engineering/test-case-reduction|Test-Case Reduction]] — concept · draft · automatically shrink a failing input to a minimal reproducer via an interestingness test; ddmin/creduce/Shrink Ray; steering beyond input length

### Syntheses
- [[software-engineering/ai-assisted-development|AI-Assisted Development]] — synthesis · draft · fundamentals under AI; the write→review shift; deterministic guardrails for AI code

## Sources ingested
- [[03_Resources/Articles/Disasters in a Microservices World|Disasters I've Seen in a Microservices World]] — article note, João Alves / Hey World, 2025-10-30
- [[03_Resources/Study Notes/Python - Production Code Principles Senior Developer|Python - Production Code Principles Senior Developer]] — YouTube tutorial (Tech With Tim, 29 min), 2026-03-16
- [[03_Resources/Study Notes/Data Structures and Big O Notation Explained|Data Structures and Big O Notation Explained]] — YouTube tutorial (Sajjaad Khader, 16 min), 2025-03-06
- [[03_Resources/Study Notes/Python - FastAPI Complete Course with Auth and Database|Python - FastAPI Complete Course with Auth and Database]] — YouTube course (Tech With Tim, 125 min), 2026-03-16
- [[03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners|DevOps - Kubernetes Complete Course for Beginners]] — YouTube course (TechWorld with Nana, 216 min), 2026-03-16
