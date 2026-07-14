---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

<p class="hero-eyebrow">A self-tending knowledge base</p>

# A knowledge base that tends itself.

*Sources in. Cited pages out. The agent reads everything, writes it into a cross-linked web of citable pages, and keeps that web consistent as new sources arrive.*

<div class="hero-stats" markdown>
<div class="hero-stat"><div class="hero-stat-n">{{ corpus_stats().pages }}</div><div class="hero-stat-l">Pages</div></div>
<div class="hero-stat"><div class="hero-stat-n">{{ corpus_stats().sources }}</div><div class="hero-stat-l">Sources</div></div>
<div class="hero-stat"><div class="hero-stat-n">{{ corpus_stats().domains }}</div><div class="hero-stat-l">Domains</div></div>
</div>

</div>

---

Most personal knowledge bases decay. Notes pile up, links rot, and the insights you captured last year become ghosts — present in the file system, invisible in practice. Corpus is built on a different premise: the LLM agent is the librarian. It reads every source, extracts what matters, and writes it into a self-organizing web of cross-linked, citable pages — then keeps that web consistent as new sources arrive.

The result compounds. Each new source enriches the pages that are already there. Each query can surface what the corpus knows *and* identify what it doesn't — automatically queuing the gap for the next ingest run.

<div class="corpus-pipeline">
<p class="corpus-pipeline-eyebrow">The pipeline · collect → ingest → cite</p>
<div class="corpus-pipeline-row">
<div class="corpus-pipeline-sources">
<div class="corpus-pipeline-source"><span class="dot" style="background:#4c5e40"></span>Email</div>
<div class="corpus-pipeline-source"><span class="dot" style="background:#a9762a"></span>YouTube</div>
<div class="corpus-pipeline-source"><span class="dot" style="background:#5f6f8a"></span>PDF</div>
<div class="corpus-pipeline-source"><span class="dot" style="background:#7d6f9a"></span>Obsidian</div>
<div class="corpus-pipeline-source"><span class="dot" style="background:#4f7a70"></span>GitHub</div>
</div>
<div class="corpus-pipeline-arrow">→</div>
<div class="corpus-pipeline-step">
<div class="corpus-pipeline-step-title">Inbox</div>
<div class="corpus-pipeline-step-sub">raw/_inbox/</div>
</div>
<div class="corpus-pipeline-arrow">→</div>
<div class="corpus-pipeline-step corpus-pipeline-step-inverted">
<div class="corpus-pipeline-step-title">Ingest agent</div>
<div class="corpus-pipeline-step-sub">reads · extracts · links</div>
</div>
<div class="corpus-pipeline-arrow">→</div>
<div class="corpus-pipeline-step">
<div class="corpus-pipeline-step-title">Corpus pages</div>
<div class="corpus-pipeline-step-sub corpus-pipeline-step-sub-accent">cited · cross-linked</div>
</div>
<div class="corpus-pipeline-arrow">→</div>
<div class="corpus-pipeline-step">
<div class="corpus-pipeline-step-title">Indexes</div>
<div class="corpus-pipeline-step-sub">_index · _log · _domains</div>
</div>
</div>
<p class="corpus-pipeline-caption">Every arrow is automated. Every corpus page cites its sources. Every source is stamped once it's processed — so nothing gets ingested twice.</p>
</div>

---

## The corpus, mapped

Each dot is a page; the larger nodes are the eight domain **hubs**, and the lines are the **citations and cross-links** between pages. This map is **generated from the live corpus on every commit** — it grows as the corpus does.

<div id="corpus-graph"></div>
<p class="graph-caption">Drag to explore · hover a node for its title · {{ corpus_stats().pages }} pages · {{ corpus_stats().domains }} domains · {{ corpus_stats().sources }} sources.</p>

---

<div class="corpus-card-grid" markdown>

<div class="corpus-card" markdown>
<span class="corpus-card-n">01</span>

**[The Idea](the-idea.md)**

Why a self-tending knowledge base beats a folder of notes — and why provenance is the one non-negotiable.

<span class="corpus-card-more">[Read more →](the-idea.md)</span>
</div>

<div class="corpus-card" markdown>
<span class="corpus-card-n">02</span>

**[How It Works](how-it-works.md)**

The end-to-end pipeline: collect → inbox → cluster → ingest → verify. How sources become cited pages.

<span class="corpus-card-more">[Read more →](how-it-works.md)</span>
</div>

<div class="corpus-card" markdown>
<span class="corpus-card-n">03</span>

**[Collectors](collectors.md)**

Five intake channels — email, YouTube, PDF, Obsidian vault, and web — each with its own harvesting logic.

<span class="corpus-card-more">[Read more →](collectors.md)</span>
</div>

<div class="corpus-card" markdown>
<span class="corpus-card-n">04</span>

**[The Custodian](the-custodian.md)**

The autonomous agent runtime: ingest, lint, adapt, and eventually dream. How the corpus tends itself overnight.

<span class="corpus-card-more">[Read more →](the-custodian.md)</span>
</div>

<div class="corpus-card" markdown>
<span class="corpus-card-n">05</span>

**[Under the Hood](under-the-hood.md)**

Schema, frontmatter spec, domain rules, the op log, and the operating manual (CLAUDE.md) that governs it all.

<span class="corpus-card-more">[Read more →](under-the-hood.md)</span>
</div>

<div class="corpus-card corpus-card-cta" markdown>
**[Get started →](getting-started.md)**

Wire the collectors to your own accounts, run your first ingest, and install the nightly schedule.
</div>

</div>

---

<div class="corpus-ethos" markdown>
<div class="corpus-ethos-title" markdown>

## Why this exists

</div>
<div class="corpus-ethos-body" markdown>

Information that isn't cited can't be audited. Information that isn't cross-linked can't be found. And information that lives only in a chat history vanishes the moment the session ends.

Corpus treats every source as raw material. The agent's job is not to answer questions — it's to build a durable, searchable, linkable layer of derived knowledge that *can* answer questions, today and years from now. It's a compounding asset, not a conversation log.

!!! quote "Design principle"
    "Without provenance, the corpus becomes lossy compression you can't audit."

</div>
</div>

The whole system is governed by a single co-evolved operating manual that specifies path isolation, page types, ingest steps, lint checks, and anti-drift rules. The agent runs autonomously within those rules; the maintainer co-evolves the rules over time.

**Next:** [The Idea](the-idea.md) — the philosophy behind a self-organizing knowledge base.
