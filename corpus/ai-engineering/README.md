---
type: hub
domain: ai-engineering
status: draft
tags:
  - corpus/ai-engineering
  - hub
created: 2026-05-07
updated: 2026-06-15
---

# AI Engineering

Domain covering LLM internals, agent design, agentic coding, context & prompt engineering, the Claude tooling stack, and AI system architecture. Substantially expanded in the 2026-06-12 email-backlog ingest (wave 2). Two sub-hubs organize the larger clusters: [[ai-engineering/agentic-coding|Agentic Coding]] (coding agents, harness, skills) and [[ai-engineering/claude-cowork|Claude Cowork]] (the Cowork product + toolkit). The 2026-06-15 YouTube-course + email-backlog ingest added the AI-fundamentals base ([[ai-engineering/ai-fundamentals|AI Fundamentals]], [[ai-engineering/machine-learning|Machine Learning]], [[ai-engineering/neural-network|Neural Networks]], [[ai-engineering/statistics-for-ml|Statistics for ML]]) and the product/workflow layer ([[ai-engineering/ai-product-management|AI Product Management]], [[ai-engineering/agentic-workflow|Agentic Workflows]], [[ai-engineering/vibe-coding|Vibe Coding]]).

## Pages

### Concepts
- [[ai-engineering/ai-fundamentals|AI Fundamentals]] — concept · draft · classical + modern AI scaffold: search, logic, uncertainty, optimization, learning
- [[ai-engineering/machine-learning|Machine Learning]] — concept · draft · supervised/unsupervised/RL; overfitting; RAG-vs-fine-tuning
- [[ai-engineering/neural-network|Neural Networks]] — concept · draft · perceptron→backprop→CNN/RNN; reasoning & multimodal models
- [[ai-engineering/statistics-for-ml|Statistics & Probability for ML]] — concept · draft · distributions, inference, regression — the math under ML
- [[ai-engineering/agentic-workflow|Agentic Workflows]] — concept · draft · describe-what-not-how; WAT framework; deterministic vs non-deterministic
- [[ai-engineering/vibe-coding|Vibe Coding]] — concept · draft · vibe coding vs spec-driven development; "ask me questions first"
- [[ai-engineering/agi|AGI]] — concept · stub · ANI/AGI/ASI; the AGI-by-2030 forecast; future-of-work framing
- [[ai-engineering/context-engineering|Context Engineering]] — concept · draft · dynamically building and optimizing LLM inputs at inference time
- [[ai-engineering/ai-agent|AI Agent]] — concept · draft · LLM + tools + memory + orchestration in an iterative loop
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — concept · draft · patterns for multiple cooperating agents (sequential, parallel, supervisor, data-driven)
- [[ai-engineering/tool-calling|Tool Calling]] — concept · draft · how LLMs request and receive tool execution results
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — concept · draft · online/offline evaluation, LLM-as-judge, golden datasets, production feedback loop
- [[ai-engineering/rag|RAG]] — concept · draft · retrieval-augmented generation; solving LLM knowledge cutoff and hallucination via context injection
- [[ai-engineering/llm|LLM]] — concept · draft · next-token prediction, parameters, training phases (pre-training + RLHF)
- [[ai-engineering/transformer|Transformer]] — concept · stub · attention-based architecture underlying all modern LLMs
- [[ai-engineering/agent-memory|Agent Memory]] — concept · draft · short-term (context window) + long-term (vector DB / CLAUDE.md) memory tiers
- [[ai-engineering/mcp|MCP]] — concept · stub · Model Context Protocol; coordination layer for agents, tools, and memory
- [[ai-engineering/context-window-management|Context Window Management]] — concept · draft · compaction, sub-agents, resets; what to keep/compress/drop when context fills
- [[ai-engineering/agent-skills|Agent Skills]] — concept · draft · skill.md files, progressive disclosure, recursive skill-building; skills vs always-on AGENTS.md
- [[ai-engineering/vector-database|Vector Database]] — concept · draft · storage layer for embedding vectors; HNSW, indexing at scale; used in RAG and agent memory
- [[ai-engineering/agent-harness|Agent Harness]] — concept · draft · the scaffolding around the model; "harness > model"; the ratchet, harness-as-a-service
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — concept · draft · crafting instructions/examples/XML to steer output; distinct from context-engineering
- [[ai-engineering/agent-security|Agent Security]] — concept · draft · prompt injection, guardrails, defense-in-depth, agent auth
- [[ai-engineering/structured-outputs|Structured Outputs]] — concept · draft · schema-enforced LLM output (Instructor); tokenization (tiktoken)
- [[ai-engineering/agentic-search|Agentic Search]] — concept · draft · AI-native/agent-orchestrated retrieval; grep-vs-vector + harness nuance
- [[ai-engineering/agent-testing|Agent Testing]] — concept · draft · verification loops, Playwright, agent honesty / bug-regression evidence
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — concept · draft · CLAUDE.md/AGENTS.md/cursor rules; attention budget; cross-platform skills/plugins
- [[ai-engineering/agent-ui|Agent UI]] — concept · draft · chat + workbench shells for agent-centric apps
- [[ai-engineering/claude-api|Claude API]] — concept · draft · Claude Messages API in Python; system prompts, structured output

### Entities
- [[ai-engineering/langgraph|LangGraph]] — entity · stub · production framework for stateful multi-agent workflows
- [[ai-engineering/langsmith|LangSmith]] — entity · draft · agent engineering platform for debugging, evaluation, and observability
- [[ai-engineering/claude-code|Claude Code]] — entity · draft · Anthropic CLI coding agent; harness, large-codebase practices, model config, security review
- [[ai-engineering/claude-cowork|Claude Cowork]] — entity · draft · **sub-hub** · Cowork desktop product; workspace folder, CLAUDE.md/MEMORY.md, Toolkit/workstations
- [[ai-engineering/anthropic|Anthropic]] — entity · draft · the lab: company, funding/valuation, learning resources
- [[ai-engineering/claude-models|Claude Model Lineup]] — entity · draft · Claude family (Haiku → Sonnet → Opus → Fable/Mythos); aliases, 1M context, Opus 4.8, Fable 5/Mythos 5
- [[ai-engineering/web-scraping|Scrapling (Web Scraping)]] — entity · stub · adaptive Python scraper; MCP extract-before-LLM token minimization
- [[ai-engineering/hermes|Hermes]] — entity · stub · self-hosted coding agent run on a VPS, controlled over Telegram; phone-first "lead developer"

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

### Cross-domain (primary home in data-engineering)
- [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] — synthesis · AI-assisted dbt / data workflows
- [[data-engineering/ai-observability-data-pipeline|AI Observability as a Data Pipeline]] — synthesis · LLM-eval as a data pipeline
- [[data-engineering/agentic-data-modeling|Agentic Data Modeling]] — synthesis · AI agents for schema design & change-impact analysis

## Sources ingested
- [[03_Resources/Articles/Context Engineering|Context Engineering]] — stub article note, 2025-10-27
- [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]] — YouTube course study note, 2026-03-16
- [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]] — YouTube course study note (LangChain, 49 min), 2026-03-15
- [[03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial|AI Tools - Local RAG Complete Tutorial]] — YouTube tutorial (Dev It, 15 min), 2026-03-16
- [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]] — YouTube explainer (3Blue1Brown, 7 min), 2026-03-16
- [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]] — YouTube explainer (AI educator, 8 min), 2026-03-16
- [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]] — YouTube tutorial (Builder Methods, 15 min), 2026-03-16
- [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — YouTube podcast (Greg Isenberg × Ras Mic, 35 min), 2026-04-08
