---
name: query
description: Answer a factual-recall question from cited corpus pages; fill thin coverage with labeled web top-up (auto-queued for ingestion); offer to file valuable answers back as synthesis pages. Interactive.
---

# Query

Turn the corpus into a trustworthy factual-recall second brain. Answer the user's
question from **cited corpus pages**; where coverage is thin, top up with **labeled**
web sources (auto-queued into `raw/_inbox/` for later ingestion); log gaps; and offer
to file a valuable answer back as a `synthesis` page. Interactive session op — needs
corpus read + WebSearch + network. Not headless.

## Safety rules (non-negotiable)
- **Covered queries write NOTHING** — no inbox file, no log entry, no page. If the
  corpus fully answers the question, it is completely read-only.
- The `bin/query.py` helper writes only to `raw/_inbox/` (gap web sources) and
  append-only to `corpus/_log.md` (gaps). It NEVER writes corpus pages.
- Corpus pages are authored by YOU only after explicit user approval (the file-back
  offer). Follow §3 (page types), §4 (frontmatter), §7 (every claim cited).
- Web top-up is ALWAYS labeled `[fresh — not yet in corpus]`; corpus claims are
  ALWAYS cited to pages. Never blur the two. Never present the model's own general
  knowledge as a corpus claim.
- On web-fetch failure (paywall/blocked/unsupported, e.g. LinkedIn/x.com): state the
  gap, fabricate nothing, queue nothing for that source.

## Retrieval model
Retrieval is **your LLM selection over `corpus/_index.md`** — read the index (loaded
at session start), pick candidate pages by topic + `aliases:`, then read them. There
is no keyword tool; your judgment over the index is the retrieval. URL discovery on a
gap is the session **WebSearch** tool; `bin/query.py fetch-and-queue` (which wraps
`fetch_link`) is the extractor that fetches and queues each chosen URL.

## Procedure
1. **Read first:** `CLAUDE.md` §8.2, then `corpus/_index.md`.
2. **Retrieve:** select candidate pages from the index by topic + `aliases:`; read them.
3. **Coverage gate:** if the corpus fully covers the question → answer from those pages
   **only**. No WebSearch, no `fetch-and-queue`, no `log-gap`, no writes of any kind.
   Name which pages answered it. Stop here.
4. **Answer format:** every non-trivial corpus claim carries an inline citation to the
   page(s) it came from, using `[[domain/page|Title]]` wikilinks. Never present the
   model's general knowledge as a corpus claim.
5. **Gap branch (corpus thin or missing):** run **WebSearch** for up to 3 candidate URLs
   (soft cap — honor a larger ask). For each, run:
   ```bash
   python3 bin/query.py fetch-and-queue --question "<the question>" --url "<URL>"
   ```
   - On `written`/`duplicate`: READ the queued file and use it to answer — but mark
     every such claim **`[fresh — not yet in corpus]`**, visually distinct from cited
     corpus claims.
   - On `error`: state plainly that the gap couldn't be auto-filled for that source.
     Fabricate nothing; queue nothing.
6. **Log the gap:** after answering a gap question, run:
   ```bash
   python3 bin/query.py log-gap --question "<q>" --note "<what the corpus didn't cover>" \
     --at "YYYY-MM-DD HH:MM" --queued <comma-joined written paths, or omit>
   ```
7. **Offer file-back:** if the answer drew on **2+ corpus pages OR kept web top-up**,
   ASK whether to save it as a `synthesis` page (a single-page restatement is trivial —
   do not offer). Only on a **yes**: YOU author `corpus/<domain>/<topic>.md` per §3/§4
   (type `synthesis`; domain; status; sources; tags; created/updated) with inline
   citations and wikilinks, then update `corpus/_index.md` and append a `query`/file-back
   note to `corpus/_log.md`. On a **no**, persist nothing beyond the gap log.

## External / headless origin (e.g. claudesidian / Obsidian vault)
This op can be delegated from outside the corpus — claudesidian (the user's Obsidian
vault at `/Users/jonasblasques/Dev/second-brain`) calls it headless via
`cd /Users/jonasblasques/Dev/corpus && CORPUS_QUERY_ORIGIN=claudesidian claude -p "/query <q>"`.

When `$CORPUS_QUERY_ORIGIN` is set (a non-interactive, vault-delegated run):
- **Compounding still happens the safe way:** answer the question, and on a gap run
  `fetch-and-queue` + `log-gap` exactly as usual. `query.py` reads `$CORPUS_QUERY_ORIGIN`
  and stamps `query_origin:` on each queued source plus `(origin: <origin>)` on the gap
  log entry — so you can later see what the vault has been asking. (You may pass
  `--origin` explicitly; it overrides the env var.)
- **Do NOT author synthesis pages.** Skip step 7's file-back offer entirely — there is no
  interactive user to approve it, and authoring corpus pages is the most consequential
  write. Queued gap sources drain into the corpus on the next normal ingest; that is the
  compounding. Synthesis authoring stays an interactive, human-attended corpus session.
- Return the answer (with the same citation / `[fresh — not yet in corpus]` labeling) as
  your final output so claudesidian can surface it to the user.

Native (in-repo) interactive queries leave `$CORPUS_QUERY_ORIGIN` unset: no origin stamp,
and step 7's file-back offer applies as written.

## Notes
- Queued web sources drain into the corpus on the next normal ingest of `raw/_inbox/`
  (the v0.6 Branch-A pipeline) — `/query` is effectively a third intake channel; the
  `via_query` frontmatter marks sources that entered through a gap, and `query_origin`
  (when present) marks ones that entered through an external delegated query.
- Web-fetch soft cap is 3 per query; raise it on request.
