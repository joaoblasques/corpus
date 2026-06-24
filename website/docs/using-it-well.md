# Using It Well

The corpus has only two verbs: **feed it** and **ask it**. Both reward a little technique. This page is the practical guide to doing each well.

---

## Phrasing good queries

The system answers by **matching your question to topic pages**, then reading them. So the whole game is: help it find the right pages, and tell it what kind of answer you want.

### The three habits that matter most

**1. Name the thing specifically.** The more concrete the noun, the better the match.

- ✗ "Tell me about AI" — too broad; matches everything and nothing.
- ✓ "What do my sources say about **mixture-of-experts**?" — lands on a real page.

**2. Use the words your sources use.** The corpus tracks nicknames (GPT-4 / gpt4 / "GPT 4"), but exact terms hit hardest. If you saved things calling it "MoE," try "MoE."

**3. Say what *shape* of answer you want.** A definition? A comparison? A list of gotchas? The disagreement? Tell it.

### Query patterns the system is built for

| You want… | Phrase it like… |
|---|---|
| Recall | "What do my sources say about **context engineering**?" |
| Compare / synthesize | "How do my notes compare **RAG vs fine-tuning**?" |
| Find the conflict | "Where do my sources **disagree** about agent memory?" |
| Connect ideas | "What's the relationship between **parquet** and **columnar storage** in what I've read?" |
| Scoped recall | "**In my data-engineering pages**, what are the gotchas with X?" |

### Two phrasings that keep it honest

- Start with **"what do *my sources* say…"** — this keeps it in recall mode, and anything pulled from the web gets clearly labelled `[fresh — not yet in corpus]` rather than blended in.
- **Treat it as a conversation.** Ask a broad question, then drill: "now just that one source's take," "now the counterargument."

### How to read the answer

- A claim **with a citation** = from your corpus, verifiable. Trust it.
- `[fresh — not yet in corpus]` = a web gap-fill, less vetted; it gets properly ingested later.
- **"Coverage is thin"** is a gift — it's telling you which domain to feed next.
- If it offers to **save the synthesis** as a page, say yes when the answer is a keeper.

### Don't ask it

Real-time questions ("latest news on X"), pure general knowledge it never ingested, or anything where you need the *exact* original wording — for that, go read the source. The corpus is a map, not the territory.

---

## Feeding a new domain well

A **domain** is just a topic folder. The key insight: domains *emerge* from clusters — you don't declare them, you feed them into existence.

**1. Feed a *cluster*, not a single item.** One article becomes a page somewhere; it doesn't make a domain. Feed **three or more related sources** so the topic has enough mass to stand on its own. Below that bar, the system folds it into a neighbour.

**2. Curate at the source — your playlists and labels *are* the sorting.** When you put videos in a themed playlist or label your email, you are pre-organising, and the system routes by that. Organise where you save, and the domain forms itself.

**3. Quality over volume.** A focused domain of twenty strong sources beats a bloated two hundred. Feed substantive things (a deep talk, a thorough article) over thin ones (a tweet, a listicle) — and leave the noise out. A playlist of hobby videos does not belong in a technical corpus.

**4. Feed in a loop, don't dump.** The rhythm that works:

> feed a cluster → let the nightly ingest distill it → query it → see the thin spots → feed the thin spots → repeat

Don't drop fifty sources at once expecting magic. Feed a handful, let it compound, and let the corpus tell you what it's missing (that "coverage is thin" signal).

**5. Don't force the name — let it route.** If you're unsure something is a real area, just feed the sources and let the system place them. They'll either crystallise into a new domain (if distinct and numerous) or land as pages in an existing one. Both are correct; under-grown domains get folded back automatically.

### A worked example: starting a `robotics` domain

- **Days 1–3:** add four or five solid robotics talks to a "Robotics" playlist; label two robotics newsletters.
- **Overnight:** the ingest distills them, and a `robotics` domain forms (three distinct sources clears the bar).
- **Then ask it:** "what do my sources say about robot learning?" — you instantly see what's covered and what's thin.
- **Fill the gap:** thin on hardware? Feed three hardware sources. It compounds.

### Feeding anti-patterns

- One source, expecting a domain → it's just a page.
- Off-topic or low-quality sources → they dilute the domain.
- The *same* thing fed five ways → de-duplication collapses it; feed five *different* angles instead.
- Never querying → you never see the gaps, and the feed-then-query loop breaks.

---

**The one-line version:** *Name the thing and say what answer you want; curate at the source, feed clusters not singles, then query early and often — the queries show you exactly where to feed next.*
