---
type: hub
domain: ai-engineering
status: draft
tags:
  - corpus/ai-engineering
  - hub
created: 2026-05-07
updated: 2026-06-17
---

# AI Engineering

Domain covering LLM internals, agent design, agentic coding, context & prompt engineering, the Claude tooling stack, and AI system architecture. Substantially expanded in the 2026-06-12 email-backlog ingest (wave 2). Two sub-hubs organize the larger clusters: [[ai-engineering/agentic-coding|Agentic Coding]] (coding agents, harness, skills) and [[ai-engineering/claude-cowork|Claude Cowork]] (the Cowork product + toolkit). The 2026-06-15 YouTube-course + email-backlog ingest added the AI-fundamentals base ([[ai-engineering/ai-fundamentals|AI Fundamentals]], [[ai-engineering/machine-learning|Machine Learning]], [[ai-engineering/neural-network|Neural Networks]], [[ai-engineering/statistics-for-ml|Statistics for ML]]) and the product/workflow layer ([[ai-engineering/ai-product-management|AI Product Management]], [[ai-engineering/agentic-workflow|Agentic Workflows]], [[ai-engineering/vibe-coding|Vibe Coding]]). The 2026-06-17 batch-1 notes-clippings ingest added [[ai-engineering/claude-managed-agents|Claude Managed Agents]] and expanded core pages. The 2026-06-17 batch-3 notes-clippings ingest further expanded [[ai-engineering/claude-code|Claude Code]] (Bun rewrite example, subagent taxonomy, organizational governance), [[ai-engineering/mcp|MCP]] (33-connector setup guide), [[ai-engineering/claude-cowork|Claude Cowork]] (Projects, mobile, VM isolation), [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] (subagents vs Agent Teams, custom agent definition format), [[ai-engineering/agent-skills|Agent Skills]] (pairwise knowledge/unbook analytics pattern, compound knowledge loop, command templates, domain skill example), [[ai-engineering/agentic-coding|Agentic Coding]] (Compound Engineering methodology), [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] (cross-platform plugin at scale), and [[ai-engineering/agent-harness|Agent Harness]] (3 patterns for building with evolving model intelligence). The 2026-06-17 batch-4 notes-clippings ingest added [[ai-engineering/prompt-caching|Prompt Caching]] (new concept page) and expanded [[ai-engineering/claude-managed-agents|Claude Managed Agents]] (self-hosted sandboxes, MCP tunnels, dreaming, outcomes, multiagent orchestration, AWS platform), [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] (five Anthropic coordination patterns), [[ai-engineering/ai-product-management|AI Product Management]] (PM workflow + Managed Agents for PMs), [[ai-engineering/agent-skills|Agent Skills]] (Anthropic 9-category taxonomy + writing tips), [[ai-engineering/claude-code|Claude Code]] (routines feature + legacy-codebase onboarding case study), [[ai-engineering/mcp|MCP]] (consumer connectors), [[ai-engineering/claude-api|Claude API]] (Platform on AWS), and [[ai-engineering/ralph-loop|Ralph Loop]] (loop engineering generalization). The 2026-06-17 batch-5 notes-clippings ingest enriched [[ai-engineering/claude-code|Claude Code]] (tool design philosophy: AskUserQuestion/TodoWrite→Task/Claude Code Guide subagent, AI-native org norms/JIT planning), [[ai-engineering/agentic-coding|Agentic Coding]] (HTML as agentic output format, AI-native engineering org process norms), [[ai-engineering/context-window-management|Context Window Management]] (official context-rot definition, /rewind mechanics, 1M context branching decision table), [[ai-engineering/optimizing-claude|Optimizing a Claude Setup]] (advisor strategy §7: Sonnet+Opus advisor, benchmarks), [[ai-engineering/claude-api|Claude API]] (advisor tool API snippet and pricing), and [[ai-engineering/rag|RAG]] (RAG vs agentic search design distinction). The 2026-06-17 web-batch-1 ingest (30 sources) enriched [[ai-engineering/agent-memory|Agent Memory]] (typed memory taxonomy: policy/preference/fact/episodic/trace, memory manager, promotion gate, claude-mem plugin), [[ai-engineering/agentic-coding|Agentic Coding]] (solve-by-default mindset, read-less-steer-more, theory-of-constraints worktree workflow, 15-engineer AI-assisted engineering round-up, ecosystem repos), [[ai-engineering/agent-cost-management|Agent Cost Management]] (23 token-conservation habits), [[ai-engineering/claude-code|Claude Code]] (routines production patterns + failure modes, /loop skill for DevOps), [[ai-engineering/rag|RAG]] (beyond-vector-store hybrid architecture, pre-filter pattern, pgvector, post-retrieval enrichment, conversation history as data layer), [[ai-engineering/agent-skills|Agent Skills]] (document-to-skill progression), and added new entity [[ai-engineering/openviking|OpenViking]] (volcengine filesystem-paradigm context database, L0/L1/L2 tiered loading, LoCoMo + HotpotQA benchmarks).

## Pages

### Concepts
- [[ai-engineering/ai-fundamentals|AI Fundamentals]] — concept · draft · classical + modern AI scaffold: search, logic, uncertainty, optimization, learning
- [[ai-engineering/machine-learning|Machine Learning]] — concept · draft · supervised/unsupervised/RL; overfitting; RAG-vs-fine-tuning
- [[ai-engineering/neural-network|Neural Networks]] — concept · draft · perceptron→backprop→CNN/RNN; reasoning & multimodal models
- [[ai-engineering/statistics-for-ml|Statistics & Probability for ML]] — concept · draft · distributions, inference, regression — the math under ML
- [[ai-engineering/agentic-workflow|Agentic Workflows]] — concept · draft · describe-what-not-how; WAT framework; dynamic workflow orchestration patterns (fan-out, tournament, adversarial)
- [[ai-engineering/vibe-coding|Vibe Coding]] — concept · draft · vibe coding vs spec-driven development; "ask me questions first"
- [[ai-engineering/agi|AGI]] — concept · stub · ANI/AGI/ASI; the AGI-by-2030 forecast; future-of-work framing
- [[ai-engineering/context-engineering|Context Engineering]] — concept · draft · dynamically building and optimizing LLM inputs at inference time
- [[ai-engineering/ai-agent|AI Agent]] — concept · draft · LLM + tools + memory + orchestration in an iterative loop
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — concept · draft · patterns for multiple cooperating agents (sequential, parallel, supervisor, data-driven)
- [[ai-engineering/tool-calling|Tool Calling]] — concept · draft · how LLMs request and receive tool execution results
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — concept · draft · online/offline evaluation, LLM-as-judge, golden datasets, production feedback loop
- [[ai-engineering/rag|RAG]] — concept · draft · retrieval-augmented generation; solving LLM knowledge cutoff and hallucination via context injection
- [[ai-engineering/llm|LLM]] — concept · draft · next-token prediction, parameters, training phases (pre-training + RLHF)
- [[ai-engineering/transformer|Transformer]] — concept · draft · attention-based architecture underlying all modern LLMs; tokenize→embed→position→attention→FFN→next-token
- [[ai-engineering/mixture-of-experts|Mixture of Experts]] — concept · draft · sparse FFN variant: many expert networks + router, few activated per token; scale params without scaling compute
- [[ai-engineering/agent-memory|Agent Memory]] — concept · draft · short-term (context window) + long-term (vector DB / CLAUDE.md) memory tiers
- [[ai-engineering/mcp|MCP]] — concept · stub · Model Context Protocol; coordination layer for agents, tools, and memory
- [[ai-engineering/context-window-management|Context Window Management]] — concept · draft · compaction, sub-agents, resets; what to keep/compress/drop when context fills
- [[ai-engineering/agent-skills|Agent Skills]] — concept · draft · skill.md files, progressive disclosure, recursive skill-building; skills vs always-on AGENTS.md
- [[ai-engineering/vector-database|Vector Database]] — concept · draft · storage layer for embedding vectors; HNSW, indexing at scale; used in RAG and agent memory
- [[ai-engineering/agent-harness|Agent Harness]] — concept · draft · the scaffolding around the model; "harness > model"; the ratchet, harness-as-a-service
- [[ai-engineering/long-running-agents|Long-Running Agents]] — concept · draft · agents progressing over hours/days across sessions; three walls, brain/hands/session split, five production patterns
- [[ai-engineering/ralph-loop|Ralph Loop]] — concept · draft · Huntley's Bash-loop coding technique; one task per loop, state on disk, generate-then-backpressure, eventual consistency
- [[ai-engineering/agent-cost-management|Agent Cost Management]] — concept · draft · cost-per-completed-task economics; re-sent context (62% of bills), context rot, the hidden 80%, prompt caching
- [[ai-engineering/prompt-caching|Prompt Caching]] — concept · draft · prefix caching mechanics; cache-safe compaction, defer_loading, cache hit rate as production metric
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — concept · draft · crafting instructions/examples/XML to steer output; distinct from context-engineering
- [[ai-engineering/agent-security|Agent Security]] — concept · draft · prompt injection, guardrails, defense-in-depth, agent auth
- [[ai-engineering/structured-outputs|Structured Outputs]] — concept · draft · schema-enforced LLM output (Instructor); tokenization (tiktoken)
- [[ai-engineering/agentic-search|Agentic Search]] — concept · draft · AI-native/agent-orchestrated retrieval; grep-vs-vector + harness nuance
- [[ai-engineering/agent-testing|Agent Testing]] — concept · draft · verification loops, Playwright, agent honesty / bug-regression evidence
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — concept · draft · CLAUDE.md/AGENTS.md/cursor rules; attention budget; cross-platform skills/plugins
- [[ai-engineering/agent-ui|Agent UI]] — concept · draft · chat + workbench shells for agent-centric apps; CLI agent view
- [[ai-engineering/claude-api|Claude API]] — concept · draft · Claude Messages API in Python; system prompts, structured output
- [[ai-engineering/computer-use|Computer Use]] — concept · draft · Claude perceiving screens and clicking; resolution scaling, thinking effort, prompt-injection defense, context management

### Entities
- [[ai-engineering/langgraph|LangGraph]] — entity · stub · production framework for stateful multi-agent workflows
- [[ai-engineering/langsmith|LangSmith]] — entity · draft · agent engineering platform for debugging, evaluation, and observability
- [[ai-engineering/claude-code|Claude Code]] — entity · draft · Anthropic CLI coding agent; harness, large-codebase practices, model config, security review
- [[ai-engineering/claude-cowork|Claude Cowork]] — entity · draft · **sub-hub** · Cowork desktop product; workspace folder, CLAUDE.md/MEMORY.md, Toolkit/workstations
- [[ai-engineering/anthropic|Anthropic]] — entity · draft · the lab: company, funding/valuation, learning resources
- [[ai-engineering/claude-models|Claude Model Lineup]] — entity · draft · Claude family (Haiku → Sonnet → Opus → Fable/Mythos); aliases, 1M context, Opus 4.8, Fable 5/Mythos 5
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — entity · draft · cloud-hosted composable agent APIs; sandboxed execution, long-running sessions, built-in filesystem memory, multi-agent coordination
- [[ai-engineering/web-scraping|Scrapling (Web Scraping)]] — entity · stub · adaptive Python scraper; MCP extract-before-LLM token minimization
- [[ai-engineering/hermes|Hermes]] — entity · stub · self-hosted coding agent run on a VPS, controlled over Telegram; phone-first "lead developer"
- [[ai-engineering/sandcastle|Sandcastle]] — entity · draft · TypeScript library orchestrating sandboxed AFK coding agents; Docker/Podman/Vercel providers, branch strategies, session resume/fork
- [[ai-engineering/codegraph|CodeGraph]] — entity · draft · local pre-indexed code knowledge graph served over MCP; cuts agent tokens/tool-calls vs. grep/read exploration
- [[ai-engineering/openviking|OpenViking]] — entity · draft · open-source context database by volcengine; filesystem-paradigm RAG with L0/L1/L2 tiered loading, directory recursive retrieval; outperforms Claude Code native memory on LoCoMo benchmark (+23pp accuracy, -63% tokens)

### Syntheses
- [[ai-engineering/agentic-coding|Agentic Coding]] — synthesis · draft · **sub-hub** · coding-agent orchestration; conductor→orchestrator, AX, the verification bottleneck
- [[ai-engineering/learning-ai-engineering|Learning AI Engineering]] — synthesis · draft · two learning paths (generalist ladder + data-engineer curriculum); context > prompts
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis · draft · how tool results feed the context loop; the compounding-window problem
- [[ai-engineering/optimizing-claude|Optimizing a Claude Setup]] — synthesis · draft · context economy as the organizing principle; skills, sub-agents, concise specs; filed back from a query
- [[ai-engineering/ai-product-management|AI Product Management]] — synthesis · draft · GenAI value stack; AIPM taxonomy; "we are all going to be AI managers"

### Sources
- [[ai-engineering/sources/how-ai-agents-and-skills-work|How AI agents & Claude skills work]] — source · draft · Isenberg × Ras Mic; skills, progressive disclosure, less-is-more context
- [[ai-engineering/sources/cs50-ai-with-python|Harvard CS50's AI with Python]] — source · draft · classical+modern AI curriculum (search, logic, ML, neural nets, NLP)
- [[ai-engineering/sources/internal-operating-system-claude-projects|4 Claude Projects / Internal OS]] — source · draft · knowledge+skills+ingest+improve loop = the LLM-Wiki pattern
- [[ai-engineering/sources/grab-multi-agent-data-warehouse-support|Grab — From Firefighting to Building]] — source · draft · production 5-agent system for data-warehouse support; six production-hardening lessons
- [[ai-engineering/sources/boris-cherny-100-percent-claude-code|Boris Cherny — 100% Claude Code]] — source · draft · head of Claude Code: full-agentic workflow, ~5 parallel agents, latent demand, build-for-the-model, "coding is describing"
- [[ai-engineering/sources/beyond-vibe-coding-book|Beyond Vibe Coding (Book)]] — source · draft · 11-chapter practitioner guide; 70% problem thesis, golden rules, autonomous agents, multimodel orchestration

### Cross-domain (primary home in data-engineering)
- [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] — synthesis · AI-assisted dbt / data workflows
- [[data-engineering/ai-observability-data-pipeline|AI Observability as a Data Pipeline]] — synthesis · LLM-eval as a data pipeline
- [[data-engineering/agentic-data-modeling|Agentic Data Modeling]] — synthesis · AI agents for schema design & change-impact analysis

## Sources ingested (Beyond Vibe Coding book — 2026-06-17)
- [Beyond Vibe Coding — TOC](../../raw/notes/notes-toc.md) — 11-chapter structure
- [Ch1 — Introduction: What Is Vibe Coding?](../../raw/notes/notes-01-introduction-what-is-vibe-coding.md)
- [Ch2 — The Art of the Prompt](../../raw/notes/notes-02-the-art-of-the-prompt-communicating-effectively-with-ai.md)
- [Ch3 — The 70% Problem](../../raw/notes/notes-03-the-70-percent-problem-ai-assisted-workflows-that-actuall.md)
- [Ch4 — Beyond the 70%: Maximizing Human Contribution](../../raw/notes/notes-04-beyond-the-70-percent-maximizing-human-contribution.md)
- [Ch5 — Understanding Generated Code: Review, Refine, Own](../../raw/notes/notes-05-understanding-generated-code-review-refine-own.md)
- [Ch6 — AI-Driven Prototyping: Tools and Techniques](../../raw/notes/notes-06-ai-driven-prototyping-tools-and-techniques.md)
- [Ch7 — Building Web Applications with AI](../../raw/notes/notes-07-building-web-applications-with-ai.md)
- [Ch8 — Security, Maintainability, and Reliability](../../raw/notes/notes-08-security-maintainability-and-reliability.md)
- [Ch9 — The Ethical Implications of Vibe Coding](../../raw/notes/notes-09-the-ethical-implications-of-vibe-coding.md) — [cross-domain: ethics/policy; no ai-engineering pages created]
- [Ch10 — Autonomous Background Coding Agents](../../raw/notes/notes-10-autonomous-background-coding-agents.md)
- [Ch11 — Beyond Code Generation: The Future of AI-Augmented Development](../../raw/notes/notes-11-beyond-code-generation-the-future-of-ai-augmented-develop.md)

## Sources ingested (batch-5 additions)
- [Seeing like an agent: how we design tools in Claude Code](../../raw/notes/notes-clippings-seeing-like-an-agent-how-we-design-tools-in-claude-code.md) — Thariq Shihipar, Anthropic, 2026-06-17
- [The advisor strategy: Give Sonnet an intelligence boost with Opus](../../raw/notes/notes-clippings-the-advisor-strategy-give-sonnet-an-intelligence-boost-with.md) — Anthropic, 2026-06-17
- [Using Claude Code: session management and 1M context](../../raw/notes/notes-clippings-using-claude-code-session-management-and-1m-context.md) — Thariq Shihipar, Anthropic, 2026-06-17
- [Using Claude Code: The unreasonable effectiveness of HTML](../../raw/notes/notes-clippings-using-claude-code-the-unreasonable-effectiveness-of-html.md) — Thariq Shihipar, Anthropic, 2026-06-17
- [Running an AI-native engineering org](../../raw/notes/notes-clippings-running-an-ai-native-engineering-org.md) — Anthropic (Claude Code team), 2026-06-17

## Sources ingested
- [[03_Resources/Articles/Context Engineering|Context Engineering]] — stub article note, 2025-10-27
- [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]] — YouTube course study note, 2026-03-16
- [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]] — YouTube course study note (LangChain, 49 min), 2026-03-15
- [[03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial|AI Tools - Local RAG Complete Tutorial]] — YouTube tutorial (Dev It, 15 min), 2026-03-16
- [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]] — YouTube explainer (3Blue1Brown, 7 min), 2026-03-16
- [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]] — YouTube explainer (AI educator, 8 min), 2026-03-16
- [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]] — YouTube tutorial (Builder Methods, 15 min), 2026-03-16
- [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — YouTube podcast (Greg Isenberg × Ras Mic, 35 min), 2026-04-08
