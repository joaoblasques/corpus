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
     ingest (CLAUDE.md §8.1). **`corpus/_domains.md` is NEVER written in an unattended
     run** — domain records are Coordinator-owned and may not be modified without the user
     present (CLAUDE.md §8.1 Coordinator-owns-shared-files rule). (`corpus/_index.md` and
     `corpus/_log.md` ARE written as part of normal ingest integration — those remain
     allowed.) No path outside `corpus/` may be written.
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
- Running Phase-5 lint checks on touched domains and applying the two enumerated safe fixes
  (orphan linking from hub, exact-duplicate wikilink removal). All other lint actions are
  flagged for review only — never auto-applied unattended.
- Stamping processed source files (`corpus_ingested`, `corpus_ingested_at`, `corpus_pages`)
  and moving them from `raw/_inbox/` to the appropriate `raw/<channel>/` subfolder.
- Appending to `corpus/_index.md`, `corpus/_log.md`, and `raw/_inbox/_REVIEW.md`.

## What is gated (always defer, never write)

Defer a source immediately — before reading its body in full — if it triggers **any** of
these four conditions. Do not attempt partial ingest; defer the entire source.

| # | Trigger | Detection |
|---|---|---|
| G1 | **No plausible existing domain** | Source cannot fit ANY existing domain in `corpus/_domains.md` — even imperfectly (CLAUDE.md §9 bias: route if any fit is plausible, defer ONLY when no existing domain is plausible at all) |
| G2 | **20+ page cascade** | The count of unique pages (new + existing) that would be created or updated for this source in the Phase-2 registry reaches or exceeds 20 (CLAUDE.md §13) |
| G3 | **Contradiction with existing page** | A claim in the source conflicts with an existing corpus page; resolving it requires a synthesis judgment (CLAUDE.md §7.1) |
| G4 | **PARA-native collision** | Source frontmatter carries `corpus_ingested: true` (CLAUDE.md §9, collision rule) |

Plus the standing bias-to-defer clause: **if routing or coverage is uncertain for any reason
not listed above, defer rather than write.**

## Pointer sources (resolve to the fetched companion)

Some inbox emails are **pointers**: frontmatter `pointer: true`, a body that is only a URL,
and a `links:` list. The real content is NOT in the email — the collector fetched it to a
companion file named in a `links:` entry with `fetched: true` and `file: raw/web/<name>.md`.
A pointer email is therefore *not* an empty stub: it must be resolved to its companion, never
skipped as content-less and never extracted from the bare URL/title.

For any candidate with `pointer: true`:

1. **Find the companion.** In `links:`, take the entries with `fetched: true` and a
   `file: raw/web/<name>.md`.
2. **Exactly one substantive fetched companion → resolve and extract from IT.** Read
   `raw/web/<name>.md` and extract entities/claims from the **companion body**, not the email.
   Route using the companion's content. Cite the **companion** as the source in `sources:` and
   footnotes (`channel: web`, `path: raw/web/<name>.md`) — it holds the actual article. Stamp
   BOTH the pointer email and the companion file with `corpus_ingested`, `corpus_ingested_at`,
   and the same `corpus_pages` list.
3. **No fetched companion (none present, or the named file is missing/empty) → DEFER**
   (trigger `UNCERTAIN`, reason "pointer with no fetched companion — nothing to extract").
   **Never fabricate from the bare URL or subject line.** Inventing content a source does not
   contain — e.g. a speculative "topics likely include…" section — is the corpus's worst
   failure mode (CLAUDE.md §7, §13). When in doubt here, defer.
4. **Multiple fetched companions spanning different topics (a digest/newsletter) → DEFER**
   (`G1`/`UNCERTAIN`): a digest is not a single-article pointer, and routing its many articles
   is a judgment call. Its companions are separate `raw/web/` sources in their own right.

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
Read `CLAUDE.md` §8.1 (batch ingest pipeline), `corpus/_index.md`, `corpus/_domains.md`,
and `corpus/_config.md`. These four files define the allowed write space, the existing domain
routing targets, and the PARA-native path list needed to detect G4 collisions and
Safety-Rule-5 "looks-like-PARA-native" cases (CLAUDE.md §8.1 Phase 0). Do not proceed
without all four.

### Step 2 — Pre-flight (Phase 0)
**If the invocation names an explicit list of files to process** (the scheduled
orchestrator pre-filters to substantive, un-ingested sources and passes them in),
process EXACTLY those — do NOT survey or touch any other inbox file. Otherwise:
list all files in `raw/_inbox/` excluding `_REVIEW.md` itself. Count them.
- If count = 0: report "inbox empty, nothing to do" and stop.
- If count > `--max`: note the overflow; you will process the first N by modification time
  (oldest first) and leave the rest for the next run.

Either way, skip files that have no substantive body (e.g. YouTube stubs with
`transcript_status: blocked`/`disabled` and a `_No transcript available._` body)
and any already stamped `corpus_ingested: true`. **A `pointer: true` email is NOT a
content-less stub** — its body is just a URL, but its content lives in a fetched
`raw/web/` companion; resolve it per **Pointer sources**, do not skip it.

For every candidate source (up to N), check its frontmatter for `corpus_ingested: true`.
Any hit → mark as G4 deferred immediately; do not read further.

### Step 3 — Survey & cluster (Phase 1)
For each non-deferred candidate, read only the title, tags/playlist field, and first
paragraph (do NOT read full bodies yet). **For a `pointer: true` candidate the email body is
empty — survey its fetched companion's (`raw/web/<name>.md`) title and first paragraph
instead** (see **Pointer sources**). Cluster thematically. Attempt to route each cluster
to an existing domain in `corpus/_domains.md`.
- Clear fit → queue for ingest.
- Imperfect but plausible fit → queue for ingest (route there; §9 default is to route, not
  defer-to-new-domain).
- No existing domain is plausible at all → mark every source in that cluster as G1 deferred.
- Genuinely uncertain across multiple domains → mark each uncertain source as UNCERTAIN
  deferred.

### Step 4 — Global entity registry (Phase 2)
For queued sources only, extract 3–10 candidate entities/concepts per source (condensed read).
Dedup against `corpus/_index.md` and across clusters by name + alias similarity. Build the
registry `{canonical-slug → aliases, domain, page-path}`.

If the count of unique pages (new + existing) that would be created or updated for a source
reaches or exceeds 20 → mark that source G2 deferred; remove it from the queue; do not
include its entities in the registry.

### Step 5 — Per-cluster ingest (Phase 3)
For each queued cluster:
1. Read full source bodies (honor Matter highlights per CLAUDE.md §10.1, YouTube timestamps
   per §10.2). **For `pointer: true` sources, read and extract from the resolved
   `raw/web/` companion body, not the email** (see **Pointer sources**); if no fetched
   companion exists, that source was already deferred in Step 3 — do not fabricate.
2. Create or update entity/concept pages using the registry. Every non-trivial claim must
   cite the source (CLAUDE.md §7 — if a claim cannot be cited, omit it or mark
   `[unsourced]`).
3. During write, check every claim against existing corpus pages for contradictions
   (CLAUDE.md §7.1). Any contradiction found → **do not write the contradiction-synthesis
   and do not overwrite or modify the conflicting existing page**; any ungated factual pages
   already written for this source remain as-is (they cannot be un-written mid-run); defer
   the source to `_REVIEW.md` with a G3 note that names the conflicting source file and the
   existing corpus page; then continue with the next source. What is deferred is the
   *contradiction resolution*, not necessarily every page from the source.
4. Cross-link pages. Link every new page from its domain hub (`README.md`) — no orphans.
5. Write source-summary pages (`type: source`) when the source warrants standalone treatment;
   this is low-bar unattended (write if it keeps the index queryable).

Workers own disjoint domains. Shared files (`_index.md` and `_log.md`) are written only in
Phase 4 (Coordinator-owns-shared-files rule, CLAUDE.md §8.1). `_domains.md` and `_config.md`
are NEVER written by this skill (Safety Rule 1).

### Step 6 — Integrate (Phase 4)
For each successfully ingested source (serialized, Coordinator):
- Stamp the source file: `corpus_ingested: true`, `corpus_ingested_at: <today>`,
  `corpus_pages: [list]`. **For a resolved pointer, stamp BOTH the pointer email and its
  `raw/web/` companion** with the same three fields (see **Pointer sources**).
- **File relocation (headless vs interactive):**
  - **Headless mode** (invoked by `bin/scheduled_run.py`): do **not** move files.
    Leave the stamped file in `raw/_inbox/`. The orchestrator
    (`bin/scheduled_run.py::move_processed_inbox`) reads the stamp and the `channel:`
    frontmatter field after the skill exits, then relocates files deterministically.
    The stamp itself is the re-ingest guard (CLAUDE.md §9).
  - **Interactive mode** (manual run): you may move the file from `raw/_inbox/` to the
    appropriate `raw/<channel>/` subfolder (matter → `raw/matter/`, youtube →
    `raw/youtube/`, web/email/notes → `raw/web/` or `raw/notes/` per the channel
    frontmatter field; if ambiguous, use `raw/web/`), following CLAUDE.md §8.1 step 10A.
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
Run lint checks scoped to touched domains only (CLAUDE.md §8.3). In unattended mode the
ONLY auto-applied fixes are:

- **(a) Orphan linking** — if a new page has no inbound link from its domain hub `README.md`,
  add the link. This is safe: it only adds a wikilink to an already-written page.
- **(b) Exact-duplicate wikilink removal** — if the same wikilink appears more than once in a
  hub page, remove the duplicates. This is safe: no semantic change.

Everything else is recorded in the run report and left for human review — NEVER applied
unattended:

- Alias merges (even when seemingly unambiguous).
- Page splits or consolidations.
- Archive proposals for old stubs.
- Domain-health or provisional-domain changes.
- Any contradiction or synthesis resolution.

Specific flags to surface in the run report (do not auto-fix):

- Stubs older than 14 days → flag, do not archive.
- Provisional domains >30 days and <3 sources → flag, do not merge.

### Step 8 — Finalize the review queue
Write (or append to) `raw/_inbox/_REVIEW.md` with all deferred sources from this run.
If there are no deferred sources, append a note:
```
<!-- [YYYY-MM-DD] run: N processed, 0 deferred -->
```
so the file records a clean run.

### Step 9 — Report
Your **final message MUST be exactly one flat JSON object and nothing else** (no
prose before or after it) so `bin/scheduled_run.py` can parse the run result:

```json
{"ingested": K, "deferred": D, "pages_created": X, "pages_updated": Y}
```

- `ingested` — sources fully ingested this run.
- `deferred` — sources written to `raw/_inbox/_REVIEW.md` this run.
- `pages_created` / `pages_updated` — corpus page counts.

Do not wrap it in markdown fences, and do not add a human-readable summary in the
final message — the JSON object is the entire final output. (When run interactively
you may still narrate progress in earlier turns; only the LAST message must be the
bare JSON object.)

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
