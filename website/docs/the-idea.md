# The Idea

!!! abstract "TL;DR"
    Corpus applies the "LLM-Wiki" pattern to personal knowledge: raw sources flow in, an agent extracts and cross-links the ideas into a durable web of citable pages. The discipline that makes it trustworthy — instead of just fast — is provenance: every non-trivial claim cites its source, disagreements get a synthesis page instead of a silent pick, and stale claims are marked superseded rather than quietly overwritten.

---

## The LLM-Wiki pattern

The core insight, popularized by Andrej Karpathy's LLM-Wiki experiments, is this: language models are better editors than they are filing cabinets. Rather than asking an LLM to *remember* things across sessions, you give it source documents and ask it to *derive* a structured knowledge layer — one that a human (or a future LLM session) can read, verify, and extend.

The difference matters enormously at scale. A chat history is ephemeral and unstructured. A wiki of derived pages is persistent, searchable, and — crucially — auditable. You can read any page and trace every claim back to the source it came from.

Corpus extends this pattern in two directions. First, it covers multiple intake channels (email, video transcripts, PDFs, vault notes, web articles) and keeps them separated as immutable raw material. Second, it treats the agent as an autonomous maintainer with explicit rules for domain creation, entity deduplication, claim lifecycle, and lint — not just a one-shot summarizer.

---

## Why a self-organizing KB beats a folder of notes

The classic personal knowledge-management problem is not capture — it's retrieval and decay.

Notes pile up. Without cross-linking, each note is an island. Without an index, you can't find what you captured. Without a maintenance discipline, newer notes contradict older ones silently. And without provenance, you can't tell whether the idea you "know" came from something you read carefully or from a half-remembered summary you wrote at 11pm.

Corpus addresses all four failure modes simultaneously:

| Failure mode | Corpus response |
|---|---|
| **Islands** | Every ingest creates or updates entity/concept pages and links them from the domain hub — no orphans permitted |
| **No index** | A catalog index (`_index.md`) is updated on every ingest; the agent selects from it by topic on every query |
| **Silent drift** | Newer sources that contradict existing claims trigger a `synthesis` page, not a silent overwrite |
| **No provenance** | Every non-trivial claim cites its source; uncited claims are marked `[unsourced — please verify]` |

The self-organizing dimension comes from the domain rules. The agent routes each source into one of a small set of active domains, creates new domains only when the evidence justifies it, and merges or splits domains when lint detects drift. The knowledge graph shapes itself around what actually arrives, not around a taxonomy someone designed in advance.

---

## Provenance: the one non-negotiable

Provenance is not a nice-to-have. It's the discipline that separates a knowledge base from a hallucination buffer.

Every corpus page that makes a non-trivial claim links it to the source it came from, using inline footnote citations:

```markdown
Self-attention scales quadratically with context length [^src1].

[^src1]: [Attention is All You Need](../../raw/web/attention-is-all-you-need.md)
```

When a claim appears in multiple sources, all are cited. When sources disagree, the agent does not pick the one it finds more plausible — it creates a `synthesis` page that names the disagreement, cites both sides, and leaves the resolution open for the human maintainer or for future sources to settle.

!!! note "Why this matters"
    An unsourced corpus page is indistinguishable from a confident hallucination. The citation requirement forces the agent to be honest about what it knows and where it learned it. It also makes the corpus auditable years later, when the sources themselves may have changed.

Sources that are too short, too sparse, or too procedural to yield citable claims don't produce pages — they get stamped as processed and move on. The corpus grows only from signal.

---

## The claim lifecycle

Knowledge ages. A fact that was accurate in one source may be contradicted by a newer one. A page that was a useful stub at creation may never grow. Corpus manages this explicitly rather than letting it rot quietly.

Each corpus page can carry three lifecycle fields in its frontmatter:

```yaml
confidence: 0.85          # 0.0–1.0; lowered when sources conflict
last_confirmed: 2026-03-12  # most recent date a source reconfirmed the claims
supersedes:
  - corpus/ai-engineering/old-concept.md
```

When a newer source confirms existing claims, `last_confirmed` updates and confidence can rise. When it contradicts them, confidence drops until the disagreement is resolved — either by a synthesis page or by a superseding page that explicitly replaces the old one.

**Supersession over deletion** is the key discipline here. The agent never silently overwrites a stale page. Instead it marks the old page `superseded_by:` pointing to the replacement, and marks the replacement `supersedes:` pointing back. The stale stub stays, with a forward link and a timestamp. The history stays auditable.

!!! tip "Why keep the stale stub?"
    Because what you believed before is part of the knowledge history. The contradiction between an old page and its replacement is itself interesting — it tells you where your understanding changed and why.

The combination of provenance, synthesis pages for disagreements, and explicit supersession means the corpus degrades gracefully as the world changes. It doesn't pretend to be always-current. It tells you when it is and when it isn't.

---

## Three layers, cleanly separated

The architecture enforces a hard boundary between sources and derived knowledge:

- **`raw/`** — immutable source documents. The agent reads them but never edits their content. A source is stamped with three metadata fields after ingest (`corpus_ingested`, `corpus_ingested_at`, `corpus_pages`) and nothing else.
- **PARA-native vault paths** — source files that already have a canonical home in the maintainer's vault, cited in place rather than copied.
- **`corpus/`** — the derived knowledge layer. The agent owns this entirely. No other tool writes here without coordination.

This separation means you can always go back to the original source to verify a claim. It also means the corpus is a pure output — if it were lost, it could be regenerated from `raw/`.

**Next:** [How It Works](how-it-works.md) — the pipeline from raw source to published corpus page.
