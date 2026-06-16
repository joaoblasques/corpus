---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/from-firefighting-to-building-how-ai-agents-restored-our-tea.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - Grab ADW multi-agent system
  - From firefighting to building
  - Grab AI agents data warehouse
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-16
updated: 2026-06-16
---

# Grab — From Firefighting to Building (multi-agent data-warehouse support)

**TL;DR.** A Grab engineering case study on a production [[ai-engineering/multi-agent-systems|multi-agent system]] that automates "quick question" support for the Analytics Data Warehouse (ADW) team [^src1]. The team supported 1,000+ monthly users over 15,000+ tables (~50% of all data-lake queries) and was spending ~40% of its time (~2 days/week) on repetitive requests — answering data-definition questions, tracing sources, running quality checks, basic enhancements [^src1]. The deployed system "autonomously answers simpler questions and collaboratively addresses more complex requests," reclaiming several FTEs of bandwidth and hundreds of hours monthly [^src1].

## Architecture: two pathways, five agents

A Slack request is categorized into one of two streams [^src1]:

- **Enhancement requests** → a single **Enhancement Agent** that interacts with GitLab, Apache Spark, and Airflow to propose and test code changes [^src1].
- **General/investigation questions** → a **Classifier** routes to specialist agents, whose findings a **Summarizer** combines [^src1].

The four investigation agents [^src1]:

- **Classifier** — parses the question, detects guardrail violations (PII, out-of-scope), and decides which specialists run and in what sequence.
- **Data Agent** — enhances context with table/column metadata, executes guarded queries (PII detection, command validation), validates schemas to avoid hallucinations, retrieves sample data.
- **Code Search Agent** — traces column transformations and table lineage through the codebase, generating plain-language explanations (e.g. tracing a column back through 5 transformation steps).
- **On-call Agent** — searches Slack for outages, checks observability platforms for pipeline health/logs/retries, validates data-quality metrics, produces incident notes and initial RCA.
- **Summarizer Agent** — reconciles conflicting findings into a coherent, concise answer before human review.

## Design decisions

- **Specialists over a monolith.** They explicitly chose multi-agent over one "Super AI" because "maintainability and accuracy mattered more than shaving off a few seconds of latency" [^src1]; the tradeoff table notes the monolith is hard to debug and changes affect everything, while multi-agent adds sequential-execution latency and coordination complexity [^src1].
- **Decoupling brain from hands.** "By decoupling the 'brain' (the LLM) from the 'hands' (the specialized agents and tools), we created a system that is both capable and easy to debug" [^src1].
- **Tech stack.** FastAPI + [[ai-engineering/langgraph|LangGraph]] (for cyclical multi-agent state/handoffs), Redis (caching/sessions) + PostgreSQL (persistent memory: conversation history and agent metadata), plus internal platforms Hubble (metadata catalog), Genchi (data-quality observability), and Lighthouse (pipeline health) [^src1].

## Production hardening (six challenges)

This is the synthetically rich core — lessons mapping directly to corpus concepts:

1. **Excessive context** ([[ai-engineering/context-window-management|context-window management]]). Context accumulates as it passes agent-to-agent. Mitigations: `tiktoken` token tracking, intelligent summarization of earlier messages when limits are exceeded (keeping recent/critical context unsummarized), RAG context pruning (smaller LLMs extract only relevant code snippets; query filters return only top results), and a **handoffs pattern** where a central orchestrator cleans/prunes context between agents [^src1].
2. **Excessive tool usage.** An initial 30+ generic API-style tools bloated prompts; they redesigned tools around real usage — including only decision-relevant fields, aggressively truncating verbose outputs, and streamlining descriptions [^src1]. (Echoes [[ai-engineering/codegraph|CodeGraph]]'s and the broader [[ai-engineering/agent-cost-management|agent-cost]] thesis: tool-call/output bloat is the bottleneck.)
3. **Risky code executions** ([[ai-engineering/agent-security|agent security]]). Layered guardrails: input classification (PII, out-of-scope), SQL validation before execution (PII-column checks, no DELETE/DROP/TRUNCATE/UPDATE, slow-query detection, schema validation), timeout protection, and Enhancement-Agent controls (no direct commits to main — all via MRs, mandatory human review, test environment first) [^src1].
4. **Ensuring user trust.** A human-in-the-loop review step lets reviewers Approve, Reject, Refine, Re-route to a sub-agent, or Annotate; annotations are saved for continuous improvement [^src1].
5. **Balancing speed and quality.** Rather than withholding answers until reviewed, responses post immediately marked **"unreviewed,"** with on-call engineers reviewing/modifying after — preserving both speed and the feedback loop [^src1].
6. **Closing the feedback loop** ([[ai-engineering/agent-evaluation|agent evaluation]]). Annotations become an active improvement engine: random annotations seed offline eval test cases, pattern analysis surfaces systemic routing/agent/hallucination issues, annotation-rate quality metrics detect regressions, and annotated failures feed prompt refinement and fine-tuning [^src1].

## Impact

Order-of-magnitude reduction in resolution time, support backlog "effectively eliminated," simple inquiries resolved autonomously within minutes (vs. hours), and several FTEs of bandwidth reclaimed for proactive roadmap work [^src1]. The stated closing principles: specialists over generalists, trust through transparency (human review + annotated feedback), and augmentation of repetitive tasks [^src1].

## Relationships

- A real-world deployment of [[ai-engineering/multi-agent-systems|multi-agent systems]] using the supervisor/handoff pattern, built on [[ai-engineering/langgraph|LangGraph]].
- Its hardening playbook touches [[ai-engineering/context-window-management|context management]], [[ai-engineering/agent-security|agent security]], [[ai-engineering/agent-evaluation|agent evaluation]], and [[ai-engineering/agent-cost-management|agent cost]] — a useful end-to-end production reference.
- Source: Grab Engineering blog (`engineering.grab.com/from-firefighting-to-building`) [^src1].

[^src1]: [From firefighting to building: How AI agents restored our team's core productivity](../../../raw/web/from-firefighting-to-building-how-ai-agents-restored-our-tea.md)
