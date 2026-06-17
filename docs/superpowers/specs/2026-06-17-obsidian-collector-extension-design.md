# Obsidian Collector Extension — Design

> Date: 2026-06-17
> Status: approved (design); pending implementation plan
> Supersedes nothing; extends `2026-06-12-obsidian-collector-design.md` and mirrors the
> inline-link pattern from `2026-06-11-email-link-following-design.md`.

## Problem

The user wants vault notes from four folders pulled into the corpus and then deleted from
the Obsidian vault, with links inside notes also fetched and collected, on a periodic
schedule. Investigation showed **most of this already exists**: the `collect-obsidian`
skill + `bin/collect_obsidian.py` + `bin/obsidian_client.py` already collect reference-layer
notes into `raw/_inbox/`, reap vault originals after `corpus_ingested`, and run daily via the
`com.corpus.daily` launchd job. The gaps are narrow:

1. Two of the four requested folders are **not** collected: top-level `Clippings/` and
   `06_Metadata/`.
2. Link-following only covers dedicated **URL-list files** (`articles to process.md`,
   `TO SCRAPE.md`); inline links in ordinary note bodies are not fetched.

This is therefore a **targeted extension of existing code**, not a new collector.

## Decisions (from brainstorming)

- **06_Metadata** → collect `06_Metadata/Reference/` only (3 prompt notes). Skip Templates,
  `README.md`, `SETUP_COMPLETE.md` — vault scaffolding, not knowledge (§9 anti-bloat).
- **03_Resources/Articles + Study Notes** → keep **PARA-native**: ingested in place, never
  reaped. 21 notes are already ingested and cited at their vault paths
  (`[[03_Resources/Articles/foo]]`); reaping would break provenance. These two dirs are
  **removed** from the collect→delete include set.
- **Links** → follow inline external links in note bodies, in addition to the existing
  URL-list files. Do **not** re-fetch a clipping's own `source:` URL (content already inline).
- **Top-level `Clippings/`** → add to the collect→delete include set (high-value Anthropic/
  Claude blog clips with clean frontmatter).
- **Schedule** → no change; the daily job already runs the obsidian collector.

## Scope

In: `bin/collect_obsidian.py`, `bin/obsidian_client.py`, `corpus/_config.md`,
`corpus/_log.md` (config entry), `.claude/skills/collect-obsidian/SKILL.md`, tests.
Out: `CLAUDE.md` schema (no change), the launchd plist/scheduled_run (no change), the
PARA-native Branch-B ingest flow (unchanged).

## Design

### 1. Folder policy — `bin/collect_obsidian.py`

`INCLUDE_DIRS` becomes:

```python
INCLUDE_DIRS = [
    "Clippings",                       # NEW — top-level web clippings
    "00_Inbox/Clippings",
    "03_Resources/Books",
    "03_Resources/Snippets",
    "03_Resources/Prompt Templates",
    "06_Metadata/Reference",           # NEW — reference prompt notes only
]
```

Removed vs. today: `03_Resources/Articles`, `03_Resources/Study Notes` (→ stay PARA-native).

`EXCLUDE_DIRS` / `EXCLUDE_FILE_RE` unchanged. The existing `README.md` rule already excludes
`06_Metadata/Reference/README` if present; `SETUP_COMPLETE.md` and `Templates/` fall outside
the include set so need no explicit exclude. `is_included()` logic is unchanged (prefix match
on the new dirs). Top-level `Clippings` and `00_Inbox/Clippings` are distinct rel-path
prefixes, so no collision in classification.

### 2. Inline link extraction — `bin/collect_obsidian.py` (new helper)

```python
MAX_LINKS_PER_NOTE = 10
AUTH_WALLED_RE = re.compile(r"(?i)://([^/]*\.)?(linkedin\.com|x\.com|twitter\.com)/")

def extract_inline_links(body: str, source_url: str = "") -> list:
    """External http(s) links in a note body, deduped, minus the note's own source URL,
    asset/image links, and Obsidian wikilinks. Capped at MAX_LINKS_PER_NOTE."""
```

Rules:
- Use the shared `URL_RE` to find `http(s)` URLs in the **body** only.
- Drop: the note's own `source:` frontmatter URL; image/asset extensions
  (`.png/.jpg/.jpeg/.gif/.svg/.webp/.pdf/.mp4/.mov/.zip`); anything inside an Obsidian
  wikilink `[[...]]`.
- Auth-walled domains (`AUTH_WALLED_RE`) are returned separately as `skipped_auth` so the
  driver can count them without a doomed network call (mirrors the existing LinkedIn/x.com
  behavior for URL-lists).
- Dedup within the note; global dedup happens at fetch time via `url_already_collected` +
  ledger. Cap the returned list at `MAX_LINKS_PER_NOTE`; if truncated, the count of dropped
  links is reported (no silent truncation).

### 3. Driver — `bin/obsidian_client.py` note branch

After writing the note source (non-dry-run), extract inline links from the note body and
fetch each through the existing `fetch_url` path — identical to the URL-list branch but with
provenance `via_vault_note: <rel_path>`:

```python
for url in co.extract_inline_links(body, source_url):
    if co.url_already_collected(url):          # global raw-dir dedup; no per-note ledger
        t["skipped"] += 1; continue
    if args.dry_run: t["inline_urls"] += 1; continue
    content = fetch_url(url)
    if not content or not content.get("text"): t["inline_failed"] += 1; continue
    path = co.url_filename(url, content.get("title", ""))
    path.write_text(co.build_url_source(
        {"source_url": url, "via_vault_note": d["rel_path"],
         "title": content.get("title", ""), "collected_at": collected_at},
        content["text"]), encoding="utf-8")
    t["inline_urls"] += 1
```

New counters in the JSON summary: `inline_urls`, `inline_failed`, `inline_skipped_auth`.
On a dry run, links are counted as discovered but no network call is made (consistent with the
existing URL-list dry-run behavior).

### 4. Provenance — `build_url_source`

Accept an optional `via_vault_note` key alongside the existing `via_vault_list`. Exactly one
of the two is present per fetched web source, recording whether the URL came from a URL-list
file or from a note body. Channel is `web` for both.

### 5. Reap

Unchanged. A note is reaped (vault original `git rm`, not committed) only once its raw copy is
`corpus_ingested`. Inline-link web sources are independent `raw/web/` items with their own
lifecycle; they are **not** struck from the note (the whole note is deleted on reap). The
PARA-native Articles/Study Notes are untouched by reap because they are no longer in the
include set.

### 6. Filename collision

A top-level `Clippings/X.md` and `00_Inbox/Clippings/X.md` both currently map to
`notes-<slug(X)>.md`. Disambiguate `note_filename()` deterministically by prepending a
slugified token of the note's **parent folder** to the filename — e.g.
`notes-clippings-<slug>.md` vs `notes-00-inbox-clippings-<slug>.md` — so two same-titled
notes from different folders cannot overwrite each other in `raw/_inbox/`. (This changes the
raw filename only; `vault_origin` frontmatter still records the full rel-path.)

## Data flow

```
vault note (included dir, unstamped)
  → collect → raw/_inbox/notes-<slug>.md            (channel notes, via vault_origin)
  → each inline link → fetch_link → raw/_inbox/web-<slug>.md  (channel web, via_vault_note)
  → daily /ingest-auto → corpus pages + stamp raw copies (corpus_ingested)
  → reap → git rm vault note (gated on corpus_ingested; web sources persist in raw/web)
```

## Testing

Extend the existing collector tests:
- **Inclusion:** a file under top-level `Clippings/` and under `06_Metadata/Reference/` is
  included; a file under `06_Metadata/Templates/` and `SETUP_COMPLETE.md` is excluded.
- **PARA-native exclusion:** files under `03_Resources/Articles/` and `Study Notes/` are
  **not** included (regression guard for the policy change).
- **Inline links:** `extract_inline_links` dedups; drops the `source:` URL, wikilinks, and
  asset links; flags auth-walled domains; respects `MAX_LINKS_PER_NOTE`.
- **Driver:** note-branch inline fetch queues a channel-`web` source with `via_vault_note`,
  honors `url_already_collected`/ledger dedup, and the dry-run path makes no network call
  (stub `fetch_url`).

## Risks / mitigations

- **Fetch noise** (notes linking to nav/social/junk) → `MAX_LINKS_PER_NOTE` cap, auth-walled
  skiplist, and the downstream §7 citation gate at ingest (a low-signal fetched page simply
  produces no corpus claim).
- **Re-collection loops** → existing `url_already_collected` + ledger dedup covers inline
  links the same way it covers URL-list links.
- **Accidental reap of cited notes** → Articles/Study Notes removed from the include set;
  reap remains gated on `corpus_ingested` of the raw copy.

## Docs to update

- `corpus/_config.md` — collect-obsidian section: new include set, the Articles/Study-Notes
  PARA-native carve-out, and inline-link behavior; append a `config` log entry to
  `corpus/_log.md`.
- `.claude/skills/collect-obsidian/SKILL.md` — include/exclude list + inline-link note.
