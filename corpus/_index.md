# Corpus Index

> Last updated: 2026-05-22 | Total pages: 37 | Total sources: 19

This file is auto-maintained by Claude. Do not edit by hand.

## Domains

### ai-engineering
- [[ai-engineering/README|AI Engineering]] — hub · draft · LLM internals, agent design, context management
- [[ai-engineering/context-engineering|Context Engineering]] — concept · draft · dynamically building and optimizing LLM inputs at inference time
- [[ai-engineering/ai-agent|AI Agent]] — concept · draft · LLM + tools + memory + orchestration in an iterative loop
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — concept · draft · patterns for multiple cooperating agents
- [[ai-engineering/tool-calling|Tool Calling]] — concept · draft · how LLMs request and receive tool execution results
- [[ai-engineering/langgraph|LangGraph]] — entity · stub · production framework for stateful multi-agent workflows
- [[ai-engineering/langsmith|LangSmith]] — entity · draft · agent engineering platform for debugging, evaluation, and observability
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — concept · draft · online/offline evaluation, LLM-as-judge, golden datasets, production feedback loop
- [[ai-engineering/rag|RAG]] — concept · draft · retrieval-augmented generation; solving LLM knowledge cutoff and hallucination via context injection
- [[ai-engineering/llm|LLM]] — concept · draft · next-token prediction, parameters, training phases (pre-training + RLHF)
- [[ai-engineering/transformer|Transformer]] — concept · stub · attention-based architecture underlying all modern LLMs
- [[ai-engineering/agent-memory|Agent Memory]] — concept · draft · short-term (context window) + long-term (vector DB / CLAUDE.md) memory tiers
- [[ai-engineering/mcp|MCP]] — concept · stub · Model Context Protocol; coordination layer for agents, tools, and memory
- [[ai-engineering/context-window-management|Context Window Management]] — concept · draft · compaction, sub-agents, resets; what to keep/compress/drop when context fills
- [[ai-engineering/vector-database|Vector Database]] — concept · stub · storage layer for embedding vectors; used in RAG pipelines and agent long-term memory
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis · draft · how tool results feed the context loop; compounding-window problem

### data-engineering
- [[data-engineering/README|Data Engineering]] — hub · draft · ETL/ELT, data modeling, Spark, Iceberg
- [[data-engineering/scd2|SCD2]] — concept · draft · history-preserving dimension pattern; valid_from/valid_to + is_current flags
- [[data-engineering/merge-into|MERGE INTO]] — concept · draft · atomic Spark SQL multi-action DML statement
- [[data-engineering/apache-iceberg|Apache Iceberg]] — entity · draft · open table format: ACID, schema evolution, time travel, hidden partitioning
- [[data-engineering/parquet|Apache Parquet]] — entity · draft · binary columnar file format; RLE compression; sort-order optimization
- [[data-engineering/data-lake|Data Lake / Lakehouse]] — concept · draft · object-storage lake + table format metadata wrapper; cost hierarchy
- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — concept · draft · same-input-same-output guarantee; pitfalls, fixes, SCD idempotency
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — concept · draft · fact + dimension tables; SCD types; streak_identifier pattern
- [[data-engineering/postgres|PostgreSQL]] — entity · draft · relational database as full-stack data platform via extensions
- [[data-engineering/kafka|Apache Kafka]] — entity · draft · event streaming platform; topics, partitions, consumer groups, KRaFt
- [[data-engineering/dbt|dbt]] — entity · draft · SQL-first transformation framework; sources vs models; layer materializations
- [[data-engineering/pipeline-layers|Pipeline Layers]] — concept · draft · staging → warehouse → marts ELT separation; Raw DB vs Analytics DB
- [[data-engineering/sql-window-functions|SQL Window Functions]] — concept · draft · ROW_NUMBER/RANK/DENSE_RANK, LAG/LEAD, running aggregates, frame clauses; DE interview reference

### software-engineering
- [[software-engineering/README|Software Engineering]] — hub · draft · foundational CS through deployment infrastructure; design principles, distributed systems, container orchestration
- [[software-engineering/fastapi|FastAPI]] — entity · draft · Python API framework; Pydantic validation, Depends() injection, JWT auth, SQLAlchemy ORM
- [[software-engineering/kubernetes|Kubernetes]] — entity · draft · container orchestration; Pod/Deployment/Service/StatefulSet; microservices runtime
- [[software-engineering/microservices|Microservices]] — concept · draft · service granularity, hype-driven adoption, shared DB misuse, eventual consistency
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — concept · draft · eight fallacies of distributed computing; sourced failure modes for network reliability, latency, security, topology
- [[software-engineering/software-design-principles|Software Design Principles]] — concept · draft · SRP, cohesion, loose coupling, dependency injection, open/closed; 8 principles separating maintainable from fragile code
- [[software-engineering/data-structures|Data Structures and Big O Notation]] — concept · draft · O(1)/O(log n)/O(n)/O(n²) complexity classes; time-complexity trade-off table for 8 core data structures

## Recent additions
- 2026-05-21: [[software-engineering/kubernetes]] (new — Batch 3 File 5)
- 2026-05-21: [[data-engineering/sql-window-functions]] (new — Batch 3 File 4, routed to data-engineering)
- 2026-05-21: [[software-engineering/fastapi]] (new — Batch 3 File 3)
- 2026-05-21: [[software-engineering/data-structures]] (new — Batch 3 File 2)
- 2026-05-21: [[software-engineering/software-design-principles]] (new — Batch 3 File 1)
- 2026-05-21: [[data-engineering/idempotent-pipelines]] (new)
- 2026-05-21: [[data-engineering/dimensional-modeling]] (new)
- 2026-05-21: [[data-engineering/scd2]] (updated, +1 source)
- 2026-05-21: [[data-engineering/parquet]] (new)
- 2026-05-21: [[data-engineering/data-lake]] (new)
- 2026-05-21: [[data-engineering/apache-iceberg]] (updated, +1 source — stub→draft)
- 2026-05-21: [[data-engineering/dbt]] (new)
- 2026-05-21: [[data-engineering/pipeline-layers]] (new)
- 2026-05-21: [[data-engineering/kafka]] (new)
- 2026-05-21: [[data-engineering/postgres]] (new)
- 2026-05-21: [[ai-engineering/vector-database]] (new — lint item F3)
- 2026-05-21: [[ai-engineering/context-window-management]] (new — Batch 1 File 5)
- 2026-05-21: [[ai-engineering/agent-memory]] (new + updated, 2 sources — Files 4–5)
- 2026-05-21: [[ai-engineering/mcp]] (new — File 4)
- 2026-05-21: [[ai-engineering/llm]] (new — File 3)
- 2026-05-21: [[ai-engineering/transformer]] (new — File 3)
- 2026-05-21: [[ai-engineering/rag]] (new — File 2)
- 2026-05-21: [[ai-engineering/langsmith]] (new — File 1)
- 2026-05-21: [[ai-engineering/agent-evaluation]] (new — File 1)
- 2026-05-21: [[ai-engineering/ai-agent]] (updated, +3 sources — Files 1, 4)
- 2026-05-21: [[ai-engineering/context-engineering]] (updated, +1 source — File 5)
- 2026-05-07: [[ai-engineering/README]] (new)
- 2026-05-07: [[ai-engineering/context-engineering]] (new → updated, +1 source)
- 2026-05-07: [[ai-engineering/ai-agent]] (new)
- 2026-05-07: [[ai-engineering/multi-agent-systems]] (new)
- 2026-05-07: [[ai-engineering/tool-calling]] (new)
- 2026-05-07: [[ai-engineering/langgraph]] (new)
- 2026-05-07: [[data-engineering/README]] (new)
- 2026-05-07: [[data-engineering/scd2]] (new)
- 2026-05-07: [[data-engineering/merge-into]] (new)
- 2026-05-07: [[data-engineering/apache-iceberg]] (new)
- 2026-05-07: [[software-engineering/README]] (new)
- 2026-05-07: [[software-engineering/microservices]] (new)
- 2026-05-07: [[software-engineering/distributed-systems-fallacies]] (new)
- 2026-05-07: [[ai-engineering/tool-calling-and-context-engineering]] (new)
