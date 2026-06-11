---
type: hub
domain: ai-engineering
status: draft
tags:
  - corpus/ai-engineering
  - hub
created: 2026-05-07
updated: 2026-06-09
---

# AI Engineering

Domain covering LLM internals, agent design, context management, prompt engineering, and AI system architecture.

## Pages

### Concepts
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
- [[ai-engineering/vector-database|Vector Database]] — concept · stub · storage layer for embedding vectors; used in RAG and agent long-term memory

### Entities
- [[ai-engineering/langgraph|LangGraph]] — entity · stub · production framework for stateful multi-agent workflows
- [[ai-engineering/langsmith|LangSmith]] — entity · draft · agent engineering platform for debugging, evaluation, and observability

### Syntheses
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis · draft · how tool results feed the context loop; the compounding-window problem
- [[ai-engineering/optimizing-claude|Optimizing a Claude Setup]] — synthesis · draft · context economy as the organizing principle; skills, sub-agents, concise specs; filed back from a query

### Sources
- [[ai-engineering/sources/how-ai-agents-and-skills-work|How AI agents & Claude skills work]] — source · draft · Isenberg × Ras Mic; skills, progressive disclosure, less-is-more context

## Sources ingested
- [[03_Resources/Articles/Context Engineering|Context Engineering]] — stub article note, 2025-10-27
- [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]] — YouTube course study note, 2026-03-16
- [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]] — YouTube course study note (LangChain, 49 min), 2026-03-15
- [[03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial|AI Tools - Local RAG Complete Tutorial]] — YouTube tutorial (Dev It, 15 min), 2026-03-16
- [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]] — YouTube explainer (3Blue1Brown, 7 min), 2026-03-16
- [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]] — YouTube explainer (AI educator, 8 min), 2026-03-16
- [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]] — YouTube tutorial (Builder Methods, 15 min), 2026-03-16
- [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — YouTube podcast (Greg Isenberg × Ras Mic, 35 min), 2026-04-08
