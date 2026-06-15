---
name: ingest-auto
description: Unattended safe-subset ingest of raw/_inbox/ up to a --max bound. Routes sources to existing domains only, defers any gated judgment to raw/_inbox/_REVIEW.md. Invoked headless by bin/scheduled_run.py; also runnable interactively for a manual safe pass.
---

# Ingest Auto (safe-subset)

Run the v0.6 Branch-A batch ingest over `raw/_inbox/` **unattended**, processing at most
`--max N` sources, deferring every judgment-call to the review queue instead of writing.
This is the corpus's pre-push guardrail: the scope of what it may do is narrow and fixed.

## Safety rules (non-negotiable)

1. **Writes are confined to two locations only:**
   - `corpus/` — ungated corpus pages, plus `_index.md` and `_log.md` per the normal
     ingest (CLAUDE.md §8.1). No other path inside `corpus/` is off-limits, but no path
     outside `corpus/` may be written.
   - `raw/_inbox/_REVIEW.md` — the deferral queue, append-only. This is the only write
     permitted outside `corpus/`.
2. **No new domains, ever.** This skill cannot create a new domain or mark one provisional.
   Any source that fits no existing domain is deferred, not routed.
3. **Bias to defer.** When routing or coverage is uncertain, DEFER. A false defer is always
   safer than a false write. The review queue exists precisely to hold these cases.
4. **Respect the `--max` bound.** Process at most N sources per run. Overflow is not a
   failure — the next scheduled run picks up where this one left off. Do not exceed the
   bound to avoid leaving a source partially processed.
5. **No PARA-native sources.** Branch A covers `raw/_inbox/` only. If a source in the inbox
   looks like a PARA-native file that has been copied there, defer it (trigger: collision).

## What is ungated (may write without deferral)

- Routing a source to an **existing** domain listed in `corpus/_domains.md`.
- Creating or updating **entity and concept pages** within that domain.
- Deduplicating via the global entity registry built in Phase 2.
- Cross-linking pages (intra-cluster, then to existing corpus pages) and linking new pages
  from their domain hub (`README.md`) so no orphans are created.
- Running Phase-5 lint checks on touched domains and applying safe fixes (orphan linking,
  alias merges where unambiguous).
- Stamping processed source files (`corpus_ingested`, `corpus_ingested_at`, `corpus_pages`)
  and moving them from `raw/_inbox/` to the appropriate `raw/<channel>/` subfolder.
- Appending to `corpus/_index.md`, `corpus/_log.md`, and `raw/_inbox/_REVIEW.md`.

## What is gated (always defer, never write)

Defer a source immediately — before reading its body in full — if it triggers **any** of
these four conditions. Do not attempt partial ingest; defer the entire source.

| # | Trigger | Detection |
|---|---|---|
| G1 | **New or provisional domain needed** | Source fits no existing domain in `corpus/_domains.md` after good-faith matching (CLAUDE.md §9) |
| G2 | **20+ page cascade** | Phase-2 entity extraction projects ≥20 pages touched for this source (CLAUDE.md §13) |
| G3 | **Contradiction-synthesis judgment** | A claim in the source conflicts with an existing corpus page (CLAUDE.md §7.1) |
| G4 | **PARA-native collision** | Source frontmatter carries `corpus_ingested: true` (CLAUDE.md §9, collision rule) |

Plus the standing bias-to-defer clause: **if routing or coverage is uncertain for any reason
not listed above, defer rather than write.**

## Deferral queue format

When a source is deferred, append exactly one line to `raw/_inbox/_REVIEW.md`:

```
- DEFER <trigger>: <source-filename> — <one-line reason>
```

Where `<trigger>` is one of `G1`, `G2`, `G3`, `G4`, or `UNCERTAIN`.
The source file is left in place in `raw/_inbox/`; it is NOT stamped; it is NOT moved.

Examples:
```
- DEFER G1: email-2026-06-11-who-s-actually-in-charge-of-ai.md — fits no existing domain (closest: ai-engineering, but content is governance/policy, distinct)
- DEFER G2: youtube-karpathy-llm-deepdive.md — entity extraction projects 31 pages; exceeds 20-page bound
- DEFER G3: raw-matter-attention-mechanisms.md — claim "transformers do not use positional encoding" contradicts corpus/ai-engineering/transformer-architecture.md
- DEFER G4: raw-matter-context-engineering.md — corpus_ingested: true already present; re-ingest requires user decision
- DEFER UNCERTAIN: email-2026-05-21-ais-uneasy-promise.md — topic spans policy, engineering, and business; routing ambiguous across 3 domains
```

`_REVIEW.md` is append-only per run. If the file does not exist, create it with a header:

```markdown
# Ingest-Auto Deferral Queue

Sources listed here were deferred by `/ingest-auto` and require a manual review pass.
Each line: `- DEFER <trigger>: <filename> — <reason>`

<!-- entries below, newest last -->
```

## Procedure

### Step 1 — Read the constraint set
Read `CLAUDE.md` §8.1 (batch ingest pipeline), `corpus/_index.md`, `corpus/_domains.md`.
These three files define the allowed write space and the existing domain routing targets.
Do not proceed without them.

### Step 2 — Pre-flight (Phase 0)
List all files in `raw/_inbox/` excluding `_REVIEW.md` itself. Count them.
- If count = 0: report "inbox empty, nothing to do" and stop.
- If count > `--max`: note the overflow; you will process the first N by modification time
  (oldest first) and leave the rest for the next run.

For every candidate source (up to N), check its frontmatter for `corpus_ingested: true`.
Any hit → mark as G4 deferred immediately; do not read further.

### Step 3 — Survey & cluster (Phase 1)
For each non-deferred candidate, read only the title, tags/playlist field, and first
paragraph (do NOT read full bodies yet). Cluster thematically. Attempt to route each cluster
to an existing domain in `corpus/_domains.md`.
- Clear fit → queue for ingest.
- No fit after good-faith matching → mark every source in that cluster as G1 deferred.
- Uncertain fit → mark each uncertain source as UNCERTAIN deferred.

### Step 4 — Global entity registry (Phase 2)
For queued sources only, extract 3–10 candidate entities/concepts per source (condensed read).
Dedup against `corpus/_index.md` and across clusters by name + alias similarity. Build the
registry `{canonical-slug → aliases, domain, page-path}`.

If entity extraction for a source projects ≥20 pages to touch → mark that source G2
deferred; remove it from the queue; do not include its entities in the registry.

### Step 5 — Per-cluster ingest (Phase 3)
For each queued cluster:
1. Read full source bodies (honor Matter highlights per CLAUDE.md §10.1, YouTube timestamps
   per §10.2).
2. Create or update entity/concept pages using the registry. Every non-trivial claim must
   cite the source (CLAUDE.md §7 — if a claim cannot be cited, omit it or mark
   `[unsourced]`).
3. During write, check every claim against existing corpus pages for contradictions
   (CLAUDE.md §7.1). Any contradiction found → **stop writing that source**, mark it G3
   deferred, discard all partial writes for that source, and continue with the next source.
4. Cross-link pages. Link every new page from its domain hub (`README.md`) — no orphans.
5. Write source-summary pages (`type: source`) when the source warrants standalone treatment;
   this is low-bar unattended (write if it keeps the index queryable).

Workers own disjoint domains. Shared files (`_index.md`, `_log.md`, `_domains.md`,
`_config.md`) are written only in Phase 4 (Coordinator-owns-shared-files rule,
CLAUDE.md §8.1).

### Step 6 — Integrate (Phase 4)
For each successfully ingested source (serialized, Coordinator):
- Stamp the source file: `corpus_ingested: true`, `corpus_ingested_at: <today>`,
  `corpus_pages: [list]`.
- Move the file from `raw/_inbox/` to the appropriate `raw/<channel>/` subfolder
  (matter → `raw/matter/`, youtube → `raw/youtube/`, web/email/notes → `raw/web/` or
  `raw/notes/` per the channel frontmatter field; if ambiguous, use `raw/web/`).
- Update `corpus/_index.md` once from all worker deltas.
- Append an `ingest` entry to `corpus/_log.md` (CLAUDE.md §12):
  ```
  ## [YYYY-MM-DD HH:MM] ingest | <source title>
  - source: raw/<channel>/<filename>
  - channel: <channel>
  - domain: <domain>
  - pages touched: [list]
  - new pages: [list]
  - notes: ingest-auto run; N processed, M deferred
  ```

### Step 7 — Verify (Phase 5)
Run lint checks scoped to touched domains only (CLAUDE.md §8.3):
- Orphans (no inbound hub link → link from hub).
- Duplicate entities (alias overlap → merge if unambiguous; defer if judgment needed).
- Stubs older than 14 days → flag in the run report, do not auto-archive.
- Provisional domains → flag if >30 days and <3 sources; do not auto-merge.

Apply only unambiguous safe fixes. Surface anything requiring judgment in the run report.

### Step 8 — Finalize the review queue
Write (or append to) `raw/_inbox/_REVIEW.md` with all deferred sources from this run.
If there are no deferred sources, append a note:
```
<!-- [YYYY-MM-DD] run: N processed, 0 deferred -->
```
so the file records a clean run.

### Step 9 — Report
Output a run summary to stdout (captured by `bin/scheduled_run.py`):

```
ingest-auto complete
  processed: N / M candidates (--max bound: N)
  ingested:  K sources
  deferred:  D sources (see raw/_inbox/_REVIEW.md)
  pages new: X | pages updated: Y
  domains touched: [list]
  deferred breakdown: G1=n G2=n G3=n G4=n UNCERTAIN=n
```

## Notes

- This skill is invoked headless by `bin/scheduled_run.py` (which then auto-commits and
  pushes `corpus/`). It is also safe to run interactively for a manual safe pass; behavior
  is identical.
- Overflow (more inbox files than `--max`) is intentional. Do not work around it. The next
  run continues from where this one left off (oldest-first ordering).
- `_REVIEW.md` entries are consumed by the user (or a separate review helper) in an
  interactive session; do not attempt to resolve gated items here.
- Source-by-source ingestion (N ≤ 10) follows the same four gated-defer checks; the
  cluster-based Phase 1–3 is most valuable for larger batches but applies at any size.
