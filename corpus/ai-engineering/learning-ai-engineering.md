---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-09-how-i-d-learn-ai-from-scratch-in-2026.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-04-16-becoming-a-data-ai-engineer-the-complete-guide.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/youtube/youtube-msFxQ7OYPj8-how-i-d-learn-ai-from-scratch-in-2026-skip-the-useless-80.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-04-here-s-how-i-d-learn-machine-learning-in-2026.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-02-this-is-how-i-d-use-ai-to-learn-python-in-2026.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-15-the-top-5-skills-for-ai-engineering-curiosity.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/github/github-anthropics-prompt-eng-interactive-tutorial.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-datatalksclub-ai-dev-tools-zoomcamp.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-05aY2LRIC3s-claude-code-full-course-12-hours-build-real-ai-projects-2026.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-zazencodes-ai-engineer-roadmap-notebooks.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-karpathy-s-llm-wi-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-Xg55nTrbYYY-full-claude-tutorial-for-beginners-in-2026-full-course.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-cladius-agentic-ai.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-sumanth077-ai-engineering-toolkit.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - learning AI
  - learning AI engineering
  - AI learning path
  - becoming an AI engineer
  - learn AI from scratch
  - learn machine learning
  - learn AI to learn Python
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-06-12
updated: 2026-06-25
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

## Path 3: The projects → AI-system ladder (the video version)

The video version of Path 1 sharpens the third rung into a concrete three-level model [^src3]:
1. **One model, go deep** — same convergence argument (models cluster in capability; pick by paid-tier access, work-fit, and vibes; always default to the most capable model).
2. **Context in Projects** — a *project* has three parts: instructions (rules that always apply), knowledge files (reference docs), and memory (auto-updated milestones). Prefer `.md` over PDF — "easier for the AI to read and cheaper to process."
3. **An AI system** — connects projects so the AI spots cross-project patterns *and* updates itself from feedback. The tool ladder by setup cost: Gemini Spark (zero setup, pre-connected) → [[ai-engineering/claude-cowork|Claude Cowork]] (non-technical, some setup) → [[ai-engineering/claude-code|Claude Code]]/Codex ("Cowork on steroids," needs code comfort). A model's *model-selector complexity* is "a pretty good signal for who it's for" [^src3].

The **reconcile** move recurs as the self-improvement mechanism: share your edited final draft back, tell the AI to reconcile it with its initial output, and it proposes rules to remember — learnings compound over time [^src3]. This is the consumer-facing version of the [[ai-engineering/agent-harness|harness]] ratchet.

## Path 4: The deep-build curriculum (build it from scratch)

For learners who want to understand AI *internals*, not just call APIs, the `ai-engineering-from-scratch` curriculum (503 lessons, 20 phases) sequences the whole stack bottom-up: math foundations → classical ML → deep-learning core → transformers → LLMs → engineering → tools/protocols → agents [^src5]. Its pedagogy is the **Build It / Use It split** — implement each algorithm from raw math first, then run the same thing through the production library — so "by the time PyTorch shows up, you already know what it's doing under the hood" [^src5]. Every lesson ships a reusable artifact (prompt, skill, agent, MCP server) [^src5]. See [[ai-engineering/ai-fundamentals|AI Fundamentals]], [[ai-engineering/machine-learning|Machine Learning]], [[ai-engineering/neural-network|Neural Networks]].

## The prerequisite ladders (Python, then ML)

Two narrower "how I'd learn X in 2026" guides feed the front of these paths [^src4][^src6]:

- **Python first** — fundamentals (variables, loops, functions, lists/dicts, error handling) until you can write a 40–50 line program *without a tutorial open*; then use AI as a **tutor that gives you reps, not answers** ("make it give you reps instead of answers"); build small projects; learn OOP *after* you feel the mess; pick one direction (AI apps, backend, automation, data) [^src4].
- **ML in the right order** — Python → NumPy/pandas/Matplotlib → the *practical* math you actually need (vectors, distributions, Bayes, gradients — not every proof) → core ML algorithms with scikit-learn → deep learning with PyTorch → production skills (Docker, FastAPI, model serving, monitoring, CI/CD, experiment tracking) [^src6]. Recurring rule: "spend more time building than watching." The math and production layers map to [[ai-engineering/statistics-for-ml|Statistics for ML]] and the [[mlops/README|MLOps]] domain respectively.

## Curiosity as the meta-skill (and the Micro-Retro Loop)

The Top 5 AI Engineering Skills series names **curiosity** as the foundational capability — the one that makes all other skills compound [^src7]:

> "Curiosity is the engine. Every other skill is downstream of it. You can teach someone to prompt or to code; you can't teach them to stay genuinely curious about why something works."

### The Micro-Retro Loop (SKILL.md pattern)

A specific curiosity practice implemented as a reusable skill [^src7]:

After completing any significant AI-assisted task, run a **Micro-Retro** (5–10 minutes):
1. **What did I try?** List the approaches, prompts, and tools used.
2. **What worked?** Which produced high-quality output with low friction?
3. **What didn't?** Where did the AI confuse, hallucinate, or miss intent?
4. **What would I do differently?** The key heuristic update.
5. **Append to `.ai_learnings.md`** — a persistent heuristics file that rides into future sessions.

### The `.ai_learnings.md` file

A single markdown file (ideally in your project root or `~/.config/`) that accumulates hard-won lessons across projects [^src7]. Structure:

```markdown
## What works well
- Giving the model a "here's what done looks like" example before asking it to generate

## Frequent failure modes
- Asking for "clean" code without specifying what clean means
- Not including the error message in the prompt

## Current experiments
- Testing whether adding a JSON schema to the system prompt reduces hallucinations on structured output
```

The payoff: the file becomes a prompt component — include it in future sessions and the model calibrates to your history. This is the personal version of the [[ai-engineering/claude-md-conventions|CLAUDE.md conventions]] pattern for teams [^src7].

### A/B testing approaches

Curiosity operationalized: "don't just try one approach and accept it — run 2–3 variants and compare" [^src7]. Concretely:
- Write the same section with two different prompt styles (role-based vs. outcome-based).
- Compare outputs on the same rubric you'd use to judge any deliverable.
- The faster you cycle through variants, the faster your personal heuristics update.

## Where the paths agree

| Claim | Generalist framing [^src1] | Engineer framing [^src2] |
|---|---|---|
| Context > prompts | "The right context beats a perfect prompt" | "Context engineering is just data modelling with a new name" |
| Start small, iterate | Pick one tool, go deep, then build a system | Start with RAG, fine-tune only if it falls short |
| Data/context is the work | Save context in Projects; feed real examples | "The data engineering part defines 80% of the project" |
| Less is more | Clear outcome over a long describing paragraph | 1,000-line prompt → 250 lines, more consistent |

## AI Engineer Roadmap (zazencodes, Jupyter notebooks)

`zazencodes/ai-engineer-roadmap` (★10, early community project) provides structured Jupyter notebooks covering the hands-on engineering skills needed to move from "knows the concepts" to "can build the thing" [^src11]:

- Notebook series covers: prompt engineering fundamentals, RAG implementation, tool use + function calling, multi-agent orchestration, evaluation patterns
- Executable: each notebook is self-contained and runnable in Google Colab or local Jupyter
- Early project (10 stars) — low signal on community adoption but good structure for self-directed learners who want code-first exposure

Use alongside the Anthropic prompt-eng-tutorial for a code-centric complement to the theory-heavy courses [^src11].

## Karpathy's LLM Wiki setup (Teacher's Tech breakdown)

Teacher's Tech's guide to implementing Karpathy's LLM wiki pattern introduces the 3-layer corpus architecture [^src12]:

1. **Raw layer** — unprocessed source documents (PDFs, articles, transcripts) kept immutable
2. **Wiki layer** — LLM-generated summaries, synthesis pages, and entity pages derived from the raw layer; this is the searchable, queryable knowledge base
3. **Schema layer** — structured data extracted from the wiki (knowledge graph edges, entity lists, claim databases)

Key principles from the guide [^src12]:
- **Compounding**: each ingest makes the corpus richer, not just bigger — summaries reference prior summaries, entities accumulate context across sources
- **Linting**: periodic passes to find orphan pages, stale claims, and duplicate entities; the linter is the quality gate
- **Read-first discipline**: always read the raw file fully before writing corpus pages; paraphrasing without reading produces lossy garbage

See [[ai-engineering/agent-memory|Agent Memory]] for how the LLM wiki pattern relates to RAG and knowledge graph memory architectures.

## See also

- [[ai-engineering/ai-fundamentals|AI Fundamentals]] — the classical-AI base (search, logic, uncertainty) under all of this
- [[ai-engineering/machine-learning|Machine Learning]] · [[ai-engineering/neural-network|Neural Networks]] · [[ai-engineering/statistics-for-ml|Statistics for ML]] — the deep-build prerequisites
- [[ai-engineering/context-engineering|Context Engineering]] — the discipline the paths converge on
- [[ai-engineering/rag|RAG]] — the data-engineer's on-ramp; "the ETL of AI"
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — the lever the paths de-emphasize relative to context
- [[ai-engineering/agent-skills|Agent Skills]] — "progressive disclosure for agents"
- [[ai-engineering/vibe-coding|Vibe Coding]] — the beginner build-and-iterate entry point
- [[ai-engineering/claude-cowork|Claude Cowork]] / [[ai-engineering/claude-code|Claude Code]] — the recommended "build a system" tools
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How I'd Learn AI From Scratch in 2026](../../raw/email/email-2026-06-09-how-i-d-learn-ai-from-scratch-in-2026.md) — Jeff Su
[^src2]: [Becoming a Data & AI Engineer — The Complete Guide](../../raw/email/email-2026-04-16-becoming-a-data-ai-engineer-the-complete-guide.md) — Alejandro Aboy, The Pipe & The Line
[^src3]: [How I'd Learn AI From Scratch in 2026 (skip the useless 80%)](../../raw/youtube/youtube-msFxQ7OYPj8-how-i-d-learn-ai-from-scratch-in-2026-skip-the-useless-80.md) — Jeff Su (video)
[^src4]: [This is how I'd use AI to learn Python in 2026](../../raw/email/email-2026-05-02-this-is-how-i-d-use-ai-to-learn-python-in-2026.md) — Tech With Tim
[^src5]: [ai-engineering-from-scratch](../../raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md) — Rohit Ghumare
[^src6]: [Here's how I'd learn machine learning in 2026](../../raw/email/email-2026-06-04-here-s-how-i-d-learn-machine-learning-in-2026.md) — Tech With Tim
## High-signal learning resources

**Anthropic's Prompt Engineering Tutorial** (★36,609) — 9-chapter Jupyter notebook series from Anthropic's training team [^src8]:
1. Basic Prompt Structure → 2. Being Clear and Direct → 3. Assigning Roles → 4. Separating Data from Instructions → 5. Formatting Output and Speaking for Claude → 6. Precognition (Thinking Step by Step) → 7. Using Examples (Few-Shot Prompting) → 8. Avoiding Hallucinations → 9. Complex Prompts for Power Users

This is the authoritative Anthropic tutorial — interactive, runnable, and regularly updated. Covers both basic and advanced prompting, including prefill and multi-turn prompt construction. Also see [[ai-engineering/prompt-engineering|Prompt Engineering]] for corpus distillation of these techniques [^src8].

**DataTalksClub AI Developer Tools Zoomcamp** (★1,129) — community-run 10-week course [^src9]:
- Covers: Claude Code, GitHub Copilot, Cursor, Windsurf, Gemini CLI, LLM APIs, context engineering, multi-agent patterns.
- Format: weekly homework + peer-graded projects; leaderboard for tracking progress.
- Positioning: focused on *using* tools in real dev workflows, not theoretical AI/ML foundations.

**12-hour Claude Code course** (YouTube) — comprehensive free tutorial covering the full Claude Code lifecycle: setup, project workflow, subagents, hooks, and production patterns [^src10]. Good companion to the interactive Anthropic tutorial above.

**Full Claude beginner course (Productive Dude, 2026)** — walkthrough of every Claude surface area for new users [^src13]: account setup, privacy settings (data-training toggle), web vs. desktop app distinction, projects vs. folders, knowledge base attachment, voice mode, capabilities (memory, tool access, artifacts/visuals), Projects with system instructions, Claude Code, Claude Cowork. Practical orientation for someone starting from zero, useful companion to the 7-continent mental map at [[ai-engineering/claude-cowork|Claude Cowork]].

**cladius/agentic-ai** (★73) — hands-on jumpstart repo for Agentic AI frameworks [^src14]: frameworks covered: ADK, Agno, Bedrock, LangFlow, LangGraph. Approach: single "5-level sample problem" solved across all frameworks. Good for comparing agentic framework APIs against a common problem set.

[^src7]: [The Top 5 Skills for AI Engineering: Curiosity](../../raw/email/email-2026-06-15-the-top-5-skills-for-ai-engineering-curiosity.md)
[^src8]: [anthropics/prompt-eng-tutorial — GitHub ★36,609](../../raw/github/github-anthropics-prompt-eng-interactive-tutorial.md) — Anthropic
[^src9]: [DataTalksClub/ai-dev-tools-zoomcamp — GitHub ★1,129](../../raw/github/github-datatalksclub-ai-dev-tools-zoomcamp.md) — DataTalksClub
[^src10]: [12-hour Claude Code course (YouTube)](../../raw/youtube/youtube-05aY2LRIC3s-claude-code-full-course-12-hours-build-real-ai-projects-2026.md)
[^src11]: [zazencodes/ai-engineer-roadmap — Jupyter notebooks for AI engineering (★10)](../../raw/github/github-zazencodes-ai-engineer-roadmap-notebooks.md) — zazencodes, GitHub
[^src12]: [Karpathy's LLM Wiki Setup Guide](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-karpathy-s-llm-wi-report.md) — Teacher's Tech, YouTube (processed report)
[^src13]: [FULL Claude Tutorial For Beginners in 2026! (FULL COURSE)](../../raw/youtube/youtube-Xg55nTrbYYY-full-claude-tutorial-for-beginners-in-2026-full-course.md) — Productive Dude, YouTube
[^src14]: [cladius/agentic-ai — agentic AI jumpstart (★73)](../../raw/github/github-cladius-agentic-ai.md) — cladius, GitHub; ADK, Agno, Bedrock, LangFlow, LangGraph
[^src15]: [Sumanth077/ai-engineering-toolkit — 100+ libraries and frameworks for LLM engineers (★3,216)](../../raw/github/github-sumanth077-ai-engineering-toolkit.md) — GitHub

## AI Engineering Toolkit (Sumanth077, ★3,216)

A curated reference list of 100+ libraries, frameworks, and tools for production LLM development. Organized by engineering concern [^src15]:

**Tooling categories** [^src15]:
- **Vector databases**: Pinecone (managed), Weaviate (open-source, GraphQL), Qdrant (Rust, filtering), Chroma (embedding DB), PGVector (Postgres extension), Milvus, Redis (vector store)
- **Orchestration & workflows**: LangChain, LlamaIndex, Haystack, Semantic Kernel
- **RAG**: LlamaIndex RAG, LangChain RAG, Haystack RAG
- **Evaluation & testing**: RAGAS (RAG evaluation), TruLens, DeepEval, Langfuse, Promptfoo
- **Model management**: Weights & Biases, MLflow, Comet
- **Data / web scraping**: Crawl4AI, Firecrawl, Playwright, Beautiful Soup
- **Agent frameworks**: AutoGen, CrewAI, LangGraph, Semantic Kernel
- **LLM inference platforms**: Together AI, Fireworks AI, Groq, Replicate
- **Structured generation**: Outlines, Instructor, Guidance
- **Local development**: Ollama, LM Studio, Jan

**Use case**: a quick reference for choosing the right library when building RAG pipelines, agent systems, evaluation harnesses, or local inference setups. Complements [[ai-engineering/rag|RAG]], [[ai-engineering/agent-evaluation|Agent Evaluation]], and [[ai-engineering/llm|LLM]] pages as a practical tooling index.
