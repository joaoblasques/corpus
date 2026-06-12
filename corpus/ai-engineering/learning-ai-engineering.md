---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/email-2026-06-09-how-i-d-learn-ai-from-scratch-in-2026.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-04-16-becoming-a-data-ai-engineer-the-complete-guide.md
    channel: inbox
    ingested_at: 2026-06-12
aliases:
  - learning AI
  - learning AI engineering
  - AI learning path
  - becoming an AI engineer
  - learn AI from scratch
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-06-12
updated: 2026-06-12
---

# Learning AI Engineering

**TL;DR**: Two learning paths from opposite ends — a non-technical "go deep on one tool" ladder (Jeff Su) and a data-engineer's "RAG is the ETL of AI" curriculum (Alejandro Aboy). They converge on the same load-bearing claims: **context beats prompts**, **start small and iterate to production**, and **the data/context work is 80% of the project** [^src1][^src2].

## Path 1: The generalist ladder (context over prompts)

For non-technical users, the recommended progression is three levels [^src1]:

1. **Pick one tool and go deep.** Models have converged ("the difference for the average user is negligible") and skills transfer across them, so depth on one (ChatGPT, Claude, or Gemini) beats jumping around. Default to the most powerful model you have access to — the weak default models are cheapest for the vendor, not best for real work [^src1].
2. **Context beats prompts.** The one framework worth keeping is **Outcome + Context (OC)**: "the right context always beats the perfect prompt" because modern models infer role, format, and tone on their own given a clear outcome [^src1]. Three ways to supply context, easiest first: name a framework ("use the Pyramid Principle"), share real examples, connect your tools (email, Drive, Slack). Then **save** it in a Project/Gem so you stop re-explaining recurring work [^src1].
3. **Build an AI system.** Connect projects so the AI spots cross-project patterns and updates itself from feedback. Tools laddered by commitment: Gemini Spark (zero setup) → [[ai-engineering/claude-cowork|Claude Cowork]] (non-technical) → [[ai-engineering/claude-code|Claude Code]]/Codex ("Cowork on steroids," needs comfort with code) [^src1].

> A pro tip that doubles as a context-engineering rule: "Use .md (Markdown) files instead of PDFs whenever you can. They're easier for the AI to read and cheaper to process." [^src1]

The "context beats prompts" claim is the beginner-facing version of [[ai-engineering/context-engineering|Context Engineering]] — and the explicit note that "I haven't said a word about prompting... your prompt is no longer the biggest factor" complements (and slightly overstates against) [[ai-engineering/prompt-engineering|Prompt Engineering]].

## Path 2: The data-engineer's curriculum (RAG is the ETL of AI)

Alejandro Aboy organizes a year of building production agents into one path, anchored on the claim that **"RAG is the most direct on-ramp because the mental model is identical to ETL"** [^src2]:

- **RAG fundamentals** (vector DBs, embeddings, similarity search with metadata filters) — "the data engineering part defines 80% of the project. Don't rush it." Fine-tune only if prompting and RAG fall short, and "100 precise examples outperform 1,000 mediocre ones" [^src2]. See [[ai-engineering/rag|RAG]], [[ai-engineering/vector-database|Vector Database]].
- **Security as an architecture decision** — structured outputs for reliability, prompt-injection prevention, least privilege / scoped tools: "scope your agent's permissions at the architecture stage. An agent can't drop a production table it doesn't have access to" [^src2]. See [[ai-engineering/agent-security|Agent Security]], [[ai-engineering/structured-outputs|Structured Outputs]].
- **MCP & Skills** — Skills framed as "progressive disclosure for agents"; "[[ai-engineering/mcp|MCP]] changed how I work across the full stack." See [[ai-engineering/agent-skills|Agent Skills]].

**Production lessons** (hard-won) [^src2]:
- "Less system prompt equals more consistency." A 1,000-line prompt cut to 250 made users say "now it gets what you want" — the same minimalism as [[ai-engineering/context-window-management|Context Window Management]] and [[ai-engineering/claude-md-conventions|CLAUDE.md conventions]].
- "Tool design is critical because each description is a prompt itself" — see [[ai-engineering/tool-calling|Tool Calling]].
- "pgvector is probably all you need for RAG." Model updates will break your agent — "pin versions, always have a rollback plan."
- **MetadataOps**: "Documentation is now a prompt. Vague metadata equals hallucinations." Add "Can an AI understand this?" to your definition of done [^src2].

## Where the two paths agree

| Claim | Generalist framing [^src1] | Engineer framing [^src2] |
|---|---|---|
| Context > prompts | "The right context beats a perfect prompt" | "Context engineering is just data modelling with a new name" |
| Start small, iterate | Pick one tool, go deep, then build a system | Start with RAG, fine-tune only if it falls short |
| Data/context is the work | Save context in Projects; feed real examples | "The data engineering part defines 80% of the project" |
| Less is more | Clear outcome over a long describing paragraph | 1,000-line prompt → 250 lines, more consistent |

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — the discipline both paths converge on
- [[ai-engineering/rag|RAG]] — the data-engineer's on-ramp; "the ETL of AI"
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — the lever both paths de-emphasize relative to context
- [[ai-engineering/agent-skills|Agent Skills]] — "progressive disclosure for agents"
- [[ai-engineering/claude-cowork|Claude Cowork]] / [[ai-engineering/claude-code|Claude Code]] — the recommended "build a system" tools
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How I'd Learn AI From Scratch in 2026](../../raw/email/email-2026-06-09-how-i-d-learn-ai-from-scratch-in-2026.md) — Jeff Su
[^src2]: [Becoming a Data & AI Engineer — The Complete Guide](../../raw/email/email-2026-04-16-becoming-a-data-ai-engineer-the-complete-guide.md) — Alejandro Aboy, The Pipe & The Line
