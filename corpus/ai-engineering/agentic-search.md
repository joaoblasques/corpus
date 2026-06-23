---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/agentic-search-models.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-05-28-but-context-first-a-field-guide-to-ai-native-search.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - agentic search
  - AI-native search
  - agentic search models
  - agentic retrieval
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# Agentic Search

**TL;DR**: A shift from the thick, hand-built retrieval monolith (embeddings + rerankers + query classifiers wired together programmatically) to an LLM agent that *orchestrates* a few thin retrieval primitives, seeing the whole task end-to-end [^src1]. The retrieval method (grep vs vector) matters, but the **agent harness** — how results reach the model — can matter just as much [^src3].

## From monolith to orchestration

The traditional search stack is a "thick monolith" built over 1–2 decades: queries flow in, business rules classify them, one or more backends are searched, results are post-processed and reranked [^src1]. Each piece (reranker, query classifier) sees only its slice, "ignorant of the whole" [^src1].

Agentic search **unbundles** this. An agent built on a frontier model (GPT-5, Sonnet) knows it has tools and is given context to solve the user's query. The underlying search tools become "thin wrappers on our backend indices"; the model orchestrates a solution rather than running a fixed series of reductive steps [^src1].

> "Agentic search unbundles the retrieval stack. The parts still matter. But the whole can be managed by a single, intelligent model." [^src1]

## AI-native search vs a search box with an LLM bolted on

AI-native search is "the structural fix … a system that interprets what you actually mean and retains what actually matters" — not a search box with a language model attached [^src2]. Today's models remember keywords but not relationships: they find the three emails mentioning "Priya" but cannot tell you her blocker got fixed, so the deal is alive again [^src2]. Closing that gap is treated as an architecture problem (structured memory + hybrid retrieval), not a bigger-model problem — see the 3.6-bit memorization ceiling in [[ai-engineering/agent-memory|Agent Memory]] [^src2].

The retrieval stage of AI-native search uses **hybrid search** blending three signals [^src2]:

- **Semantic meaning** — finds the right cluster even without exact words.
- **Keyword matching** — for precise terms ("SOC 2") you do not want fuzzed.
- **Graph traversal** — follows relationships outward, hop by hop, filtered by time.

This is the surgeon-not-hoarder pattern: locate the nodes the question touches and pull only the relevant subgraph, instead of jamming the full history into the prompt (which "Lost in the Middle" shows is unreliable) [^src2].

## Agentic search models (the last 20%)

Frontier models handle the 80% case — they understand queries with general knowledge and surface defensible results [^src1]. But the last 20% is the non-obvious, domain-specific knowledge: that "bistro tables" means small outdoor tables in *this* furniture store, not restaurant equipment [^src1]. Frontier models think of "search" as near-flawless web search; narrow-domain backends are not Google [^src1].

**Agentic search models** are LLMs trained specifically to control the search task in a domain. They can be smaller, faster, and cheaper to deploy than frontier models [^src1]:

| Model | Source | Note |
|---|---|---|
| SID-1 | SID | First mover; smaller size, lower latency vs GPT-5 for agentic search |
| Waldo | Glean | — |
| (corpus-tailored) | Charcoal | Tailors to your corpus |

The envisioned future: stop building complex query + reranking pipelines; deploy basic, scalable retrieval primitives (keyword search, an embedding model, a few filters) and let a domain-tuned agentic search model orchestrate them [^src1]. An embedding solves only similarity; an agentic search model could span query understanding through hybrid search [^src1]. (These models are "too slow today to drive site search," but the author expects that to change [^src1].)

## The harness matters more than the search

A PwC study, *"Is Grep All You Need?"*, ran 116 LongMemEval questions across 4 harnesses, 5 models, and 2 retrieval methods [^src3]. Two findings, and they qualify each other:

**1. Plain lexical grep often beats vector search** for long-memory conversational QA — by up to 23 points. LongMemEval answers hinge on exact entities, names, dates that appear verbatim; exact string matching nails them while embeddings smooth them into similarity space and miss the literal token [^src3].

- Lexical grep: 83.6–93.1% across harness-model pairs; vector: 62.9–83.6% [^src3].
- Biggest gap: Gemini 3.1 Flash-Lite on Chronos scored 86.2% (grep) vs 62.9% (vector) [^src3].

**2. The harness is the hidden variable.** Hold model and corpus fixed, swap only the harness, and accuracy moves double digits. Claude Opus 4.6 scored 93.1% on Chronos vs 76.7% on Claude Code with identical corpus and retrieval — a 16-point swing from the wrapper alone [^src3]. The cleanest demonstration is delivery mode: switching from inline (results dropped into context) to file-based (agent fetches from disk) "could invert or erase the lexical advantage without any change to the corpus" — GPT-5.4 on Codex CLI dropped from 93.1% inline to 55.2% file-based [^src3].

**Caveat — grep does not always win.** The result is scoped to long-term conversational memory QA where answers live as exact tokens. The authors are explicit it "may not transfer to scientific synthesis, paraphrased retrieval, or tasks where semantic generalization is the whole point" — settings that play to vector search's strengths. A noise-injection scaling experiment showed vector occasionally pulling ahead with non-monotonic curves, so "grep always wins" is the wrong takeaway [^src3].

> "Before reaching for an embedding index, try grep, and pay as much attention to how results reach the model as to how they are retrieved." [^src3]

This nuance — both sides of grep-vs-vector, plus harness as the deciding variable — lives here rather than as a separate synthesis page. See [[ai-engineering/agent-harness|Agent Harness]] for the broader claim that the harness around an agent often does more for or against you than the model inside it.

## See also

- [[ai-engineering/rag|RAG]] — agentic search orchestrates retrieval primitives; hybrid search and re-ranking originate there
- [[ai-engineering/agent-harness|Agent Harness]] — result delivery, prompting, and tool framing rival the retrieval method
- [[ai-engineering/agent-memory|Agent Memory]] — AI-native search and graph memory share the hybrid-retrieval-over-subgraph pattern
- [[ai-engineering/vector-database|Vector Database]] — the embedding-index half of the grep-vs-vector comparison
- [[ai-engineering/embeddings|Embeddings]] — why exact tokens (names, IDs, "SOC 2") get smoothed away, the root cause behind grep beating vector on verbatim QA

---

[^src1]: [The New Agentic Search Models](../../raw/web/agentic-search-models.md)
[^src2]: [But Context First: A Field Guide to AI-Native Search](../../raw/email/email-2026-05-28-but-context-first-a-field-guide-to-ai-native-search.md)
[^src3]: [Is Grep All You Need? The Harness Matters More Than the Search](../../raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md)
