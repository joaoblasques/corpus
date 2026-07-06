# Free & legal source catalog for Corpus (2026-07-06)

> Verified via web search + prior-known licensing. HARD-EXCLUDED: pirate/shadow mirrors
> (z-lib, libgen, sci-hub, pdfcoffee, scribd/dokumen re-uploads) and DRM store copies.
> Legend: ✅ direct download · 📝 free but form-gated (you fill a form) · 🔁 wire-as-feed
> (recurring collector, not a manual drop) · 🐙 GitHub-hosted markdown/AsciiDoc (ingest cleanest).

## Bucket A — Grab-now (download once → CorpusInbox/Books or /PDFs)

### AI / LLM engineering + ML foundations
| Book | Domain | License / why legal | Format | URL |
|---|---|---|---|---|
| **Dive into Deep Learning** (Zhang, Lipton, Li, Smola) | ai-engineering | CC BY-SA 4.0 | ✅ PDF | https://d2l.ai/d2l-en.pdf — **downloaded** |
| **Mathematics for Machine Learning** (Deisenroth, Faisal, Ong) | ai-engineering | author-hosted free (Cambridge permits) | ✅ PDF | https://mml-book.github.io/book/mml-book.pdf — **downloaded** |
| **Elements of Statistical Learning** (Hastie, Tibshirani, Friedman) | ai-engineering | author-hosted free (Stanford) | ✅ PDF | https://hastie.su.domains/ElemStatLearn/ |
| **An Introduction to Statistical Learning** (ISLR/ISLP) | ai-engineering | author-hosted free | ✅ PDF | https://www.statlearning.com/ |

### Data engineering / warehousing
| Book | Domain | License | Format | URL |
|---|---|---|---|---|
| **Data-Driven Science and Engineering** v2 (Brunton, Kutz) | data-engineering / mlops | author-hosted free (databookuw) | ✅ PDF | https://databookuw.com/ — **downloaded** |
| **Spark: The Definitive Guide** (Chambers, Zaharia) | data-engineering | Databricks giveaway | 📝 PDF | https://pages.databricks.com/definitive-guide-spark.html |
| **Big Book of Data Engineering** (4th ed) | data-engineering | Databricks giveaway | 📝 PDF | https://www.databricks.com/resources/ebook/big-book-of-data-engineering |
| **Big Book of Data Warehousing & BI** | data-engineering | Databricks giveaway | 📝 PDF | https://www.databricks.com/resources/ebook/big-book-data-warehousing-and-bi |
| **Rebuilding Reliable Data Pipelines** (Malaska) | data-engineering | O'Reilly free report | 📝 PDF | https://www.oreilly.com/library/view/rebuilding-reliable-data/9781492058175/ |

### Software engineering / systems / MLOps
| Book | Domain | License | Format | URL |
|---|---|---|---|---|
| **Operating Systems: Three Easy Pieces** (OSTEP) | software-engineering | free, author-hosted (per-chapter PDFs) | ✅ PDF | https://pages.cs.wisc.edu/~remzi/OSTEP/ |
| **The Architecture of Open Source Applications** v1+v2 | software-engineering | CC BY 3.0 | 🐙 HTML/PDF | https://aosabook.org/en/ |
| **Designing Distributed Systems** (Burns) | software-engineering / mlops | Microsoft giveaway | ✅ PDF | (Microsoft) — **downloaded** |
| **Google SRE** — *Site Reliability Engineering*, *SRE Workbook*, *Building Secure & Reliable Systems* | mlops | free online (Google) | 🔁 HTML | https://sre.google/books/ |

### Blockchain (GitHub markdown — cleanest possible ingest)
| Book | Domain | License | Format | URL |
|---|---|---|---|---|
| **Mastering Bitcoin** 3rd ed (Antonopoulos, Harding) | blockchain | CC BY-SA 4.0 | 🐙 AsciiDoc | https://github.com/bitcoinbook/bitcoinbook |
| **Mastering Ethereum** (Antonopoulos, Wood) | blockchain | CC BY-SA (non-commercial) | 🐙 AsciiDoc | https://github.com/ethereumbook/ethereumbook |

## Bucket B — Wire-as-feed (recurring collector; I build, you don't fetch)

| Source | Domain(s) | Why legal | Collector idea |
|---|---|---|---|
| **arXiv** (cs.AI, cs.LG, cs.DC, cs.SE, q-fin) | ai-engineering, software-engineering, trading | open-access, redistributable metadata + PDFs | standing topic queries → abstract stubs → LLM triage promotes high-relevance to full ingest (roadmap Phase 3) |
| **National Academies Press** (nap.edu) | data-engineering, mlops | free PDFs, US gov-adjacent | subject-filtered new-release fetch |
| **MIT OpenCourseWare** | all technical | CC BY-NC-SA | course lecture-notes fetch for named courses |
| **Open Textbook Library** (open.umn.edu/opentextbooks) | all | CC (300+ books) | subject-filtered catalog pull |
| **QuantEcon** (quantecon.org) | trading | open, BSD/CC | lecture-series fetch (Python quant/econ, time series) |
| **Official docs & changelogs** (Claude Code, Spark, dbt, DuckDB…) | all | vendor docs, freely readable | roadmap Phase 2 RSS/release-notes collector |

## Honest gaps
- **Trading/quant**: very thin on free *books* (the canonical ones — López de Prado, Chan — are commercial). Best legal path is the **arXiv q-fin feed + QuantEcon**, not book downloads.
- **AI-business / productivity**: almost no free legal *books* (this genre is Kindle/commercial or blog-native). Best served by the **Phase-2 blog RSS feed**, not the book channel.

## Recommended order of operations
1. **Now**: 4 books already downloaded + chunked (d2l, mml, Brunton-Kutz, Burns). Ingesting nightly.
2. **You (5 min each, form-gated)**: grab Spark Definitive Guide + Big Book of Data Engineering → drop in `CorpusInbox/PDFs/`.
3. **Me (build)**: a `github-book` ingest path for the CC AsciiDoc books (Mastering Bitcoin/Ethereum, AOSA) — markdown ingest, no PDF extraction, highest fidelity.
4. **Me (Phase 3)**: arXiv + OA-repository feed collectors for the recurring high-signal stream.

---

## Execution status (2026-07-06)
- **Downloaded & queued** (CorpusInbox): d2l, mml-book, Intro to Statistical Learning, Brunton-Kutz,
  Burns, + 68 OSTEP chapter PDFs. (ESL landing page is a JS redirect stub — left as a manual grab.)
- **GitHub-book pipeline BUILT & RUN** (bin/collect_github_book.py + github_book_client.py +
  github_books.yaml): Mastering Bitcoin (14 ch) + Mastering Ethereum (17 ch) collected as chapter
  stubs. On-demand: `python3 bin/github_book_client.py collect`. AsciiDoc/Markdown → clean prose,
  no PDF extraction. AOSA can be added to the config once its glob is verified.
- **Ingest prioritization**: book/pdf channels now sort ahead of the general web/youtube backlog
  (behind labeled email), so books drain first — they were landing at the back of the oldest-first
  queue (position ~1067/1098). Now top of the queue.

## Phase 3 SHIPPED (2026-07-06, commit 09ffdc8)
- **arXiv feed collector LIVE** (bin/arxiv_client.py collect + collect_arxiv.py + arxiv_feeds.yaml):
  standing per-domain queries → `arxiv`-channel abstract stubs → normal ingest → queryable source
  pages pointing back to the papers. Wired into the nightly (--max 24). Stdlib-only, id-deduped,
  polite. 6 domain feeds (llm-agents, rag-and-context, llm-systems-eval, data-systems,
  distributed-systems, quant-trading). Add/edit feeds in arxiv_feeds.yaml.
- **Still open** (other Bucket-B feeds, lower priority): National Academies Press, MIT OCW,
  Open Textbook Library, QuantEcon — heterogeneous, no uniform API; build per-source if/when wanted.

## Book auto-acquisition SHIPPED (2026-07-06)
Manual Drive drops are now optional. Three layers, all allowlist-safe:
- **book_fetch** (commit 5757c01): manifest `bin/book_sources.yaml` of KNOWN-LEGAL direct URLs →
  nightly download into CorpusInbox/PDFs/_auto (allowlist-gated: arXiv/.edu/CC-GitHub/author/
  publisher-giveaway hosts only). Adding a book = one manifest line.
- **book_discover** (commit dd387b0): scans ONE curated legal index (free-programming-books, CC BY)
  → proposes corpus-relevant PDF books into `raw/_book_review.md`. Trusted-host finds pre-checked
  [x] (auto-download); untrusted-host finds [ ] await a human tick. Never crawls the open web.
- **review promotion**: book_fetch downloads every [x] review entry (approval = trusted pre-check
  OR human tick, bypassing the allowlist for those vouched URLs only).
To approve a reviewed book: tick [x] in raw/_book_review.md — the next nightly fetches it.
