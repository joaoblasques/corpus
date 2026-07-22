---
type: hub
domain: software-engineering
status: draft
tags:
  - corpus/software-engineering
  - hub
created: 2026-05-07
updated: 2026-07-21
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
- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — concept · draft · time complexity classes and trade-off table for 8 core data structures; hashing (open/closed, tombstones), 2-3 trees, self-organizing lists, implicit data structures, deque
- [Functional and Persistent Data Structures](/software-engineering/functional-persistent-data-structures.md) — concept · draft · purely functional structures that maintain old versions; lazy evaluation resolves amortization-persistence conflict; binomial heaps, finger trees
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
- [Simplicity as an Engineering Constraint in the AI Age](/software-engineering/simplicity-as-engineering-constraint.md) — synthesis · draft · taste as the only remaining check on complexity once AI removes friction; architecture-over-discipline; AI as pipe not platform; single-source, confidence 0.6

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
- [Matters Computational (Arndt)](/software-engineering/sources/matters-computational.md) — source · complete · 978pp reference: bit wizardry, permutations, FFT/NTT/Walsh/Haar/Hartley transforms, combinatorial generation, fast arithmetic; full C++ FXT library
- [Algorithms and Complexity (Wilf, 1994)](/software-engineering/sources/algorithms-and-complexity-wilf.md) — source · draft · Herbert Wilf; 139p; recursion/FFT, network flow (Ford-Fulkerson), number theory, NP-completeness; free educational use
- [Algorithms (Erickson, 2019)](/software-engineering/sources/algorithms-erickson.md) — source · draft �� Jeff Erickson (UIUC); 472p; recursion → divide-and-conquer → DP → greedy → graph algorithms → MST → shortest paths → network flow → NP-hardness; CC BY 4.0
- [Data Structures and Algorithm Analysis in C++ (Shaffer, Ed. 3.2)](/software-engineering/sources/algorithms-shaffer-c.md) — source · draft · Clifford Shaffer (Virginia Tech); 615p; ADT philosophy, data structures, sorting, hashing, B-trees, graphs, NP-completeness; free PDF
- [Data Structures and Algorithm Analysis in Java (Shaffer, Ed. 3.2)](/software-engineering/sources/algorithms-shaffer-java.md) — source · draft · Java edition of Shaffer's DSA textbook; same content as C++ edition; 601p; free PDF; parts 17-30 cover searching/hashing, indexing/2-3 trees, graphs, MST, lower bounds, limits of computation
- [Purely Functional Data Structures (Okasaki, CMU 1996)](/software-engineering/sources/purely-functional-data-structures-okasaki.md) — source · draft · CMU PhD thesis; functional/persistent data structures; lazy evaluation resolves amortization-persistence conflict; binomial heaps, finger trees, numerical representations
- [Algorithms and Data Structures (Nievergelt & Hinrichs, Global Text)](/software-engineering/sources/algorithms-nievergelt.md) — source · draft · open-access CC BY 3.0 textbook; implicit data structures; algorithm animation emphasis; EBNF/syntax diagrams
- [Data Structures — Wikipedia Compilation (2010)](/software-engineering/sources/data-structures-wikipedia.md) — source · draft · 503-page Wikipedia-sourced reference survey; deque/A-Steal work-stealing; bit fields and type safety
- [Learning Algorithm (PDF, 327 pages)](/software-engineering/sources/learning-algorithm.md) — source · draft · compact algorithms reference; interval scheduling, BFS/Dijkstra/Floyd-Warshall, Hoare/Lomuto quicksort, KMP string matching
- [Efficient Algorithms on Texts (Crochemore & Rytter, 1994)](/software-engineering/sources/text-algorithms.md) — source · draft · suffix trees, DAWG, KMP/BM/Aho-Corasick, palindromes (Rad table, palstars), 2D pattern matching, LZ compression, shortest common superstring; all 20 parts ingested
- [The Design of Approximation Algorithms (Williamson & Shmoys, 2011)](/software-engineering/sources/design-of-approximation-algorithms.md) — source · draft · graduate textbook; greedy (set cover, submodular (1−1/e)), LP rounding (vertex cover 2-approx), randomized rounding (MAX SAT, MAX CUT), SDP rounding (Goemans-Williamson 0.878 MAX CUT), primal-dual, cuts/metrics, iterated rounding, PCP hardness; all 34 parts ingested
- [Code Simplicity: The Fundamentals of Software (Kanat-Alexander, 2012)](/software-engineering/sources/code-simplicity.md) — source · draft · software design laws: Equation of Software Design (V>M), Law of Change (YAGNI), Law of Defect Probability (DRY, ~1 defect/100 lines), Law of Simplicity (individual pieces); 3 of 4 parts ingested

## Sources ingested
- [Disasters I've Seen in a Microservices World](/03_Resources/Articles/Disasters in a Microservices World.md) — article note, João Alves / Hey World, 2025-10-30
- [Python - Production Code Principles Senior Developer](/03_Resources/Study Notes/Python - Production Code Principles Senior Developer.md) — YouTube tutorial (Tech With Tim, 29 min), 2026-03-16
- [Data Structures and Big O Notation Explained](/03_Resources/Study Notes/Data Structures and Big O Notation Explained.md) — YouTube tutorial (Sajjaad Khader, 16 min), 2025-03-06
- [Python - FastAPI Complete Course with Auth and Database](/03_Resources/Study Notes/Python - FastAPI Complete Course with Auth and Database.md) — YouTube course (Tech With Tim, 125 min), 2026-03-16
- [DevOps - Kubernetes Complete Course for Beginners](/03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md) — YouTube course (TechWorld with Nana, 216 min), 2026-03-16

<!-- AUTO-INDEX:START (generated by bin/corpus_heal.py hubs — do not edit inside) -->

## Pages in this domain

### Concepts (30)
- [AI Risk Architecture](/software-engineering/ai-risk-architecture.md)
- [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md)
- [CAP Theorem](/software-engineering/cap-theorem.md)
- [CI/CD, Progressive Delivery, and GitOps](/software-engineering/ci-cd.md)
- [Cognitive Debt and Cognitive Surrender](/software-engineering/cognitive-debt.md)
- [Compiler-Warning Management (Git's `false_but_the_compiler_does_not_know_it_`)](/software-engineering/compiler-warning-management.md)
- [Complexity Theory and NP-Completeness](/software-engineering/complexity-theory.md)
- [Concurrency and Threads](/software-engineering/concurrency-and-threads.md)
- [Container Patterns (Single-Node)](/software-engineering/container-patterns.md)
- [CPU Scheduling](/software-engineering/cpu-scheduling.md)
- [Data Structures and Big O Notation](/software-engineering/data-structures.md)
- [Distributed File Systems](/software-engineering/distributed-file-systems.md)
- [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md)
- [Engineering Craft](/software-engineering/engineering-craft.md)
- [File Systems](/software-engineering/file-systems.md)
- [Functional and Persistent Data Structures](/software-engineering/functional-persistent-data-structures.md)
- [Go Programming Language](/software-engineering/go-programming-language.md)
- [JavaScript Fundamentals](/software-engineering/javascript-fundamentals.md)
- [Local-First Sync Architecture](/software-engineering/local-first-sync-architecture.md)
- [Microservices](/software-engineering/microservices.md)
- [Operating Systems Fundamentals](/software-engineering/operating-systems.md)
- [OS Security](/software-engineering/os-security.md)
- [Scatter/Gather Pattern](/software-engineering/scatter-gather-pattern.md)
- [signal processing algorithms](/software-engineering/signal-processing-algorithms.md)
- [Software Design Principles](/software-engineering/software-design-principles.md)
- [System Design Fundamentals](/software-engineering/system-design-fundamentals.md)
- [Terminal / CLI Tools](/software-engineering/terminal-cli-tools.md)
- [Test-Case Reduction](/software-engineering/test-case-reduction.md)
- [Virtual Machine Monitors (VMMs / Hypervisors)](/software-engineering/virtual-machine-monitors.md)
- [Virtual Memory](/software-engineering/virtual-memory.md)

### Entities (10)
- [Bun](/software-engineering/bun.md)
- [FastAPI](/software-engineering/fastapi.md)
- [Git Basics](/software-engineering/git-basics.md)
- [InsForge — backend platform for agentic coding](/software-engineering/insforge.md)
- [Kan](/software-engineering/kan.md)
- [Kubernetes (k8s)](/software-engineering/kubernetes.md)
- [React](/software-engineering/react.md)
- [Usertour](/software-engineering/usertour.md)
- [Vim](/software-engineering/vim.md)
- [Xonsh — a Python-superset shell](/software-engineering/xonsh.md)

### Syntheses (2)
- [AI-Assisted Development](/software-engineering/ai-assisted-development.md)
- [Simplicity as an Engineering Constraint in the AI Age](/software-engineering/simplicity-as-engineering-constraint.md)

<details>
<summary>Source summaries (79)</summary>

- ["2024-05-25-15-54-25 - move-base-up by josephmachado · Pull Request #17 · josephmachado/simple_dbt_project"](/software-engineering/sources/2024-05-25-15-54-25-move-base-up-by-josephmachado-pull-reque-ee.md)
- ["A Guide to Multi-Tenancy: Benefits and Challenges"](/software-engineering/sources/a-guide-to-multi-tenancy-benefits-and-challenges-e55e9184.md)
- ["Disasters I've seen in a microservices world, part II"](/software-engineering/sources/disasters-i-ve-seen-in-a-microservices-world-part-ii-doc.md)
- ["Guitar - 3 Easy Jazz Standards (Stormy Monday, Blue Bossa, Blue in Green)"](/software-engineering/sources/guitar-3-easy-jazz-standards-stormy-monday-blue-bossa-blue-i-doc.md)
- ["Senior Engineer Mindset — Ownership, Systems Thinking, and Ego Dissolution"](/software-engineering/sources/senior-engineer-mindset-ownership-systems-thinking-and-ego-d-doc.md)
- ["The Next Two Years of Software Engineering: Five Critical Questions"](/software-engineering/sources/the-next-two-years-of-software-engineering-five-critical-que-ac.md)
- [14 More lessons from 14 years at Google](/software-engineering/sources/14-more-lessons-from-14-years-at-google-e.md)
- [21 Engineering Career Lessons from 14 Years at Google](/software-engineering/sources/21-engineering-career-lessons-from-14-years-at-google-e.md)
- [21 Lessons from 14 Years at Google](/software-engineering/sources/21-lessons-from-14-years-at-google-e.md)
- [30 Vim commands you NEED TO KNOW (in just 10 minutes)](/software-engineering/sources/30-vim-commands-you-need-to-know-in-just-10-minutes-RSlrxE21l_k.md)
- [5 Simple Habits for Writing Clean Code](/software-engineering/sources/5-simple-habits-for-writing-clean-code-cde.md)
- [6 security settings every GitHub maintainer should enable this week](/software-engineering/sources/6-security-settings-every-github-maintainer-should-enable-th-ab782b95.md)
- [6 Software Engineering Challenges & Ways To Overcome Them](/software-engineering/sources/6-software-engineering-challenges-ways-to-overcome-them-7af11149.md)
- [A quote from Armin Ronacher](/software-engineering/sources/a-quote-from-armin-ronacher-7d60c1dd.md)
- [Algorithms (Erickson, 2019)](/software-engineering/sources/algorithms-erickson.md)
- [Algorithms and Complexity (Wilf, 1994)](/software-engineering/sources/algorithms-and-complexity-wilf.md)
- [Algorithms and Data Structures (Nievergelt & Hinrichs, Global Text Project)](/software-engineering/sources/algorithms-nievergelt.md)
- [All Python Syntax in 25 Minutes – Tutorial](/software-engineering/sources/all-python-syntax-in-25-minutes-tutorial-PNSIWjWAA7o.md)
- [Announcing Guides](/software-engineering/sources/announcing-guides-3eabcba3.md)
- [Bass - 10 Basslines That Teach Scales](/software-engineering/sources/bass-10-basslines-that-teach-scales-cae.md)
- [Career - 5 Boring Certifications for Tech Career Growth](/software-engineering/sources/career-5-boring-certifications-for-tech-career-growth-doc.md)
- [Claude Code - Session Timing Strategy to Double Productivity](/software-engineering/sources/claude-code-session-timing-strategy-to-double-productivity-dc.md)
- [Claude Code Productivity Tips from the SaaS Trenches](/software-engineering/sources/claude-code-productivity-tips-from-the-saas-trenches-ada.md)
- [Code Review Best Practices](/software-engineering/sources/code-review-best-practices-acce.md)
- [Code Simplicity: The Fundamentals of Software (Kanat-Alexander, 2012)](/software-engineering/sources/code-simplicity.md)
- [Coming Soon - Kai Waehner](/software-engineering/sources/coming-soon-kai-waehner-3fd775a7.md)
- [Data Structures and Algorithm Analysis in C++ (Shaffer, Ed. 3.2)](/software-engineering/sources/algorithms-shaffer-c.md)
- [Data Structures and Algorithm Analysis in Java (Shaffer, Ed. 3.2)](/software-engineering/sources/algorithms-shaffer-java.md)
- [Data Structures — Wikipedia Reference Compilation (2010)](/software-engineering/sources/data-structures-wikipedia.md)
- [Designing Distributed Systems (Brendan Burns, O'Reilly, 2018)](/software-engineering/sources/burns-designing-distributed-systems.md)
- [Dev - 9-Step Coding Project Planning Process](/software-engineering/sources/dev-9-step-coding-project-planning-process-ce.md)
- [Dev - Vibe Coding 3-Stage Planning Method](/software-engineering/sources/dev-vibe-coding-3-stage-planning-method-ed.md)
- [Devin The AI Software Engineer Coding AI Agent Builds & Deploys Full Stack Apps From Prompt For FREE](/software-engineering/sources/devin-the-ai-software-engineer-coding-ai-agent-builds-deploy-mV1SAj9qXtU.md)
- [DevOps - Starship Terminal Prompt Configuration](/software-engineering/sources/devops-starship-terminal-prompt-configuration-cfa.md)
- [DevOps - Terminal Customization Oh My Zsh Powerlevel10k](/software-engineering/sources/devops-terminal-customization-oh-my-zsh-powerlevel10k-eee10.md)
- [Efficient Algorithms on Texts (Crochemore & Rytter, 1994)](/software-engineering/sources/text-algorithms.md)
- [From 0 to IDE in NEOVIM from scratch | FREE COURSE // EP 1](/software-engineering/sources/from-0-to-ide-in-neovim-from-scratch-free-course-ep-1-zHTeCSVAFNY.md)
- [Fundamentals of Backend Architecture - How to Design Scalable Software](/software-engineering/sources/fundamentals-of-backend-architecture-how-to-design-scalable--Qa-7iWxDz1A.md)
- [Git & GitHub Tutorial | Visualized Git Course for Beginner & Professional Developers in 2024](/software-engineering/sources/git-github-tutorial-visualized-git-course-for-beginner-profe-S7XpTAnSDL4.md)
- [Git - Worktrees in Under 5 Minutes](/software-engineering/sources/git-worktrees-in-under-5-minutes-e.md)
- [Give Me 15 Minutes — 80% of Obsidian](/software-engineering/sources/give-me-15-minutes-80-of-obsidian-bda.md)
- [Guitar - Acoustic Guitar Effects Without Amp Tonewood](/software-engineering/sources/guitar-acoustic-guitar-effects-without-amp-tonewood-ed.md)
- [Guitar - Complementing Chords in Rhythm Playing](/software-engineering/sources/guitar-complementing-chords-in-rhythm-playing-a.md)
- [Guitar - Connecting Chords and Scales in Key of A](/software-engineering/sources/guitar-connecting-chords-and-scales-in-key-of-a-a.md)
- [Guitar - H.E.R. Songwriting Method for Chord Progressions](/software-engineering/sources/guitar-h-e-r-songwriting-method-for-chord-progressions-e.md)
- [Guitar - How to Write Catchy Hooks](/software-engineering/sources/guitar-how-to-write-catchy-hooks-doc.md)
- [Guitar - Jazz Chord System Joe Pass Approach](/software-engineering/sources/guitar-jazz-chord-system-joe-pass-approach-aac.md)
- [Guitar - Juicy Chord Voicings (Chord Tone Priorities)](/software-engineering/sources/guitar-juicy-chord-voicings-chord-tone-priorities-e.md)
- [Guitar - Lead Guitar Triad Approach](/software-engineering/sources/guitar-lead-guitar-triad-approach-aac.md)
- [Guitar - Looper Pedal Beginner Guide](/software-engineering/sources/guitar-looper-pedal-beginner-guide-de.md)
- [Guitar - Playing Any Melody by Ear](/software-engineering/sources/guitar-playing-any-melody-by-ear-ea.md)
- [Guitar - Relearning Soloing Through Chord Changes](/software-engineering/sources/guitar-relearning-soloing-through-chord-changes-cae.md)
- [Guitar - Robbie Krieger and The Doors Sound](/software-engineering/sources/guitar-robbie-krieger-and-the-doors-sound-d.md)
- [Guitar - Slide Guitar Quick Tips](/software-engineering/sources/guitar-slide-guitar-quick-tips-doc.md)
- [Guitar - Ultimate Fretboard System Rectangle and Stack](/software-engineering/sources/guitar-ultimate-fretboard-system-rectangle-and-stack-ac.md)
- [How I Play Guitar (In This Economy) — Budget Digital Rig Guide](/software-engineering/sources/how-i-play-guitar-in-this-economy-budget-digital-rig-guide-de.md)
- [How I would learn music production (If I had to start over in 2026)](/software-engineering/sources/how-i-would-learn-music-production-if-i-had-to-start-over-in-3RjQ1WjAl7Q.md)
- [How to NOT Fail a System Design Interview (By a Data Engineer)](/software-engineering/sources/how-to-not-fail-a-system-design-interview-by-a-data-engineer-WQBc2mY9Jng.md)
- [Learning Algorithm (PDF, 327 pages)](/software-engineering/sources/learning-algorithm.md)
- [macOS - Aerospace Tiling Window Manager with Leader Key](/software-engineering/sources/macos-aerospace-tiling-window-manager-with-leader-key-e.md)
- [macOS - Simple Window Management with Raycast](/software-engineering/sources/macos-simple-window-management-with-raycast-aca.md)
- [Matt Pocock’s Agentic Engineering Workflow (just copy him)](/software-engineering/sources/matt-pocock-s-agentic-engineering-workflow-just-copy-him-nQwJVHCtDDY.md)
- [Matters Computational: Ideas, Algorithms, Source Code (Joerg Arndt)](/software-engineering/sources/matters-computational.md)
- [Obsidian Markdown Made Ridiculously Simple](/software-engineering/sources/obsidian-markdown-made-ridiculously-simple-e.md)
- [ostep operating systems three easy pieces](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md)
- [Purely Functional Data Structures (Okasaki, CMU 1996)](/software-engineering/sources/purely-functional-data-structures-okasaki.md)
- [Python - Complete Beginner Course 5 Hours TechWorld with Nana](/software-engineering/sources/python-complete-beginner-course-5-hours-techworld-with-nana-aa.md)
- [Refactoring Techniques Guide](/software-engineering/sources/refactoring-techniques-guide-de.md)
- [Software Engineering at Google — Key Lessons on Code That Lasts](/software-engineering/sources/software-engineering-at-google-key-lessons-on-code-that-last-e.md)
- [Software Engineering Best Practices MOC](/software-engineering/sources/software-engineering-best-practices-moc-c.md)
- [Software Engineering in the Age of AI](/software-engineering/sources/software-engineering-in-the-age-of-ai-a.md)
- [SOLID Principles in Practice](/software-engineering/sources/solid-principles-in-practice-acce.md)
- [Source: Go Programming — Full Course (Tech With Tim)](/software-engineering/sources/go-full-course-tech-with-tim.md)
- [Source: Go Programming — Golang Course with Bonus Projects (boot.dev / freeCodeCamp)](/software-engineering/sources/go-course-boot-dev.md)
- [Source: The Software Engineer's Guidebook (Gergely Orosz)](/software-engineering/sources/software-engineers-guidebook.md)
- [The best TUIs - powerful terminal apps](/software-engineering/sources/the-best-tuis-powerful-terminal-apps-_fLmA4fjiAE.md)
- [The C.R.A.F.T.E.D. Prompt Framework for Software Engineers](/software-engineering/sources/the-c-r-a-f-t-e-d-prompt-framework-for-software-engineers-eee.md)
- [The Design of Approximation Algorithms (Williamson & Shmoys, 2011)](/software-engineering/sources/design-of-approximation-algorithms.md)
- [Why I Love Using Vim To Write Code](/software-engineering/sources/why-i-love-using-vim-to-write-code-o4X8GU7CCSU.md)

</details>

<!-- AUTO-INDEX:END -->
