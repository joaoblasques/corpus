# Gmail Label Collection + Post-Ingest Un-label/Archive — Design

> Date: 2026-06-18
> Status: approved (design); pending implementation plan
> Extends the existing Gmail collector (`bin/gmail_client.py` + `bin/collect_email.py`);
> mirrors the post-ingest reaper pattern from the PDF (`pdf_client.py file`) and Obsidian
> (`obsidian_client.py reap`) collectors.

## Problem

The Gmail collector currently collects only **starred** mail (`q="is:starred"`), and de-stars +
archives each message *immediately on collection*. The user also files mail under topic
**labels** and wants those collected into the corpus too — and, because some of those emails are
just links, the content behind the links pulled in (already handled by the collector's
`enrich_email` link-following). After a labeled email is **ingested into the corpus**, its
collected label(s) should be removed and the email archived — but only *after* ingest, unlike the
immediate starred flow.

## Decisions (confirmed with user)

- **Label set (9, config-editable):** `Data Engineering`, `Data Engineering/databricks`,
  `Data Engineering/dbt`, `Data Engineering/spark`, `Ml`, `ML Engineering`, `MLOps`,
  `Productivity`, `Prompting`. (Exact Gmail names — note `Ml`, not `ML`.) Other user labels
  (`@shopping`, `Sax`, `Status/*`) are excluded.
- **After ingest:** remove only the **matched corpus label(s)** on that message, then **archive**
  (remove the `INBOX` label). Other labels (e.g. `Status/To Read`) are left intact.
- **Starred flow unchanged:** still de-stars + archives immediately on collection. Only the new
  labeled flow defers its un-label/archive to post-ingest.

## Scope

In: `bin/gmail_client.py` (label config, labeled collection pass, `reap-labels` subcommand),
`bin/collect_email.py` (record `gmail_corpus_labels` in the email source frontmatter),
`bin/scheduled_run.py` (run `reap-labels` after the ingest phase), `corpus/_config.md` (document
the label set + lifecycle), tests.
Out: changing the starred lifecycle; OCR/attachment handling; a per-label routing-to-domain
scheme (labels are collection filters, not corpus domains — routing stays with the normal ingest).

## Design

### 1. Label config — `bin/gmail_client.py`

```python
# Topic labels collected into the corpus (exact Gmail names). Edit this list to
# add/remove labels. Documented in corpus/_config.md.
CORPUS_LABELS = [
    "Data Engineering", "Data Engineering/databricks", "Data Engineering/dbt",
    "Data Engineering/spark", "Ml", "ML Engineering", "MLOps",
    "Productivity", "Prompting",
]
```

Same "editable list in the collector module, documented in `_config.md`" pattern as
`collect_obsidian.INCLUDE_DIRS`.

### 2. Labeled collection pass — `cmd_run` (extended)

`cmd_run` keeps its starred pass exactly as-is, then runs a **labeled pass**:

- `resolve_label_ids(service, CORPUS_LABELS) -> dict[name, id]` — one `labels.list` call; map each
  configured name to its Gmail label ID. A configured name with no matching Gmail label is
  reported (skipped), not fatal.
- `list_labeled_messages(service, label_ids) -> list[dict]` — for the union of the 9 label IDs,
  page `messages().list(userId="me", labelIds=[id])` per label, **dedup by message id**, fetch
  full messages. (Query by `labelIds`, not `q="label:..."` — exact, and avoids space/slash search
  quirks and the parent-doesn't-include-sublabels issue.)
- For each unique message: compute its **matched corpus labels** = (message's `labelIds` ∩ the 9
  corpus label IDs), mapped back to names. Collect via the existing `collect_email` path (channel
  `email`, `enrich_email` link-following), recording `gmail_message_id` (already done) **and**
  `gmail_corpus_labels: [<names>]` in the source frontmatter. **Do NOT archive.**
- Dedup by `gmail_message_id` against already-collected sources (existing behavior), so an email
  already collected (starred or labeled, this run or a prior one) is not re-collected.

`cmd_run`'s JSON summary gains labeled-pass counts (e.g. `labeled_written`, `labeled_dup`).

### 3. Email source frontmatter — `bin/collect_email.py`

The email-source builder gains an optional `gmail_corpus_labels` field (a YAML list). Absent for
starred-only emails; present (the matched corpus label names) for labeled emails. This is the
marker the post-ingest reaper keys on.

### 4. Post-ingest reaper — `gmail_client.py reap-labels` (new subcommand)

`reap-labels [--dry-run]`:
- Scan `raw/_inbox` + `raw/email` for sources with **`corpus_ingested: true`** AND a
  non-empty **`gmail_corpus_labels`** field (a deterministic, network-free pre-scan — like
  `collect_obsidian.reapable`).
- Resolve `CORPUS_LABELS` names → IDs once (`labels.list`).
- For each such source: `messages().modify(userId="me", id=<gmail_message_id>,
  body={"removeLabelIds": [<matched label IDs> + "INBOX"]})` — removes the matched corpus
  label(s) and archives. Idempotent (removing an absent label is a no-op, so a re-run after the
  message is already un-labeled/archived does nothing). `--dry-run` reports what it would do
  without calling `modify`.
- JSON summary: `{relabeled: n, archived: n, dry_run, errors: [...]}`.

This is the email analogue of `pdf_client.py file` and `obsidian_client.py reap`: a post-ingest
step gated on `corpus_ingested`.

### 5. Scheduled wiring — `bin/scheduled_run.py`

- Collection phase: unchanged call to `gmail_client.py run` now also collects labels (step 2).
- After the ingest phase (beside `move_processed_inbox`): run `gmail_client.py reap-labels`.
  Failure is recorded, never aborts the run (same isolation as the other post-ingest steps).
  Gated on `corpus_ingested`, so it can never un-label an email whose content isn't in the corpus.

## Data flow

```
labeled email (∈ 9 corpus labels)
  → gmail run (labeled pass): collect → raw/_inbox/email-*.md
       (channel email; gmail_message_id; gmail_corpus_labels=[matched]; link-following) — NOT archived
  → /ingest-auto → corpus pages + stamp source corpus_ingested → move to raw/email
  → gmail reap-labels: modify(removeLabelIds = matched corpus label IDs + INBOX) → un-labeled + archived
```

## Edge cases

- **Starred AND labeled:** the starred pass collects + archives it immediately; its corpus label
  remains (the reaper only processes sources carrying `gmail_corpus_labels`, which a starred-only
  source lacks). Rare; acceptable for v1 — noted, not handled specially.
- **Collected but not yet ingested:** the email keeps its label between collect and ingest;
  `gmail_message_id` dedup prevents re-collection. The reaper only acts once `corpus_ingested`.
- **Deferred/skipped at ingest:** if a labeled email is never ingested (deferred), it's never
  un-labeled — correct (the label/archive only happens once its content is truly in the corpus).
- **Configured label missing in Gmail:** reported and skipped, not fatal.
- **Message in multiple corpus labels:** collected once; all matched corpus labels recorded and
  all removed at reap.

## Testing

Mock the Gmail service (existing test pattern):
- `resolve_label_ids` maps names→IDs and reports a missing configured label.
- `list_labeled_messages` dedups a message that carries two corpus labels.
- the labeled collection records `gmail_corpus_labels` and does NOT archive; `gmail_message_id`
  dedup skips an already-collected message.
- `reap-labels`: only processes `corpus_ingested` sources with `gmail_corpus_labels`; calls
  `modify` with the matched label IDs + `INBOX`; is idempotent; `--dry-run` calls no `modify`.
- A `scheduled_run` test asserts `reap-labels` is invoked after the ingest phase.

## Risks / mitigations

- **Wrong label removed** → the reaper removes only IDs in `CORPUS_LABELS ∩ message labels`
  (computed from the recorded `gmail_corpus_labels`), never arbitrary labels; `--dry-run` lets the
  first run be previewed.
- **Un-labeling before ingest** → strictly gated on `corpus_ingested`; runs only in the
  post-ingest phase.
- **Label-list drift** (rename in Gmail) → names live in `CORPUS_LABELS` (one edit point) +
  documented in `_config.md`; a renamed/absent label is skipped with a report, not a crash.
- **OAuth scope:** `gmail.modify` is already granted (used for de-star/archive) — sufficient for
  `removeLabelIds`. No scope change.
