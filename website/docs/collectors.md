# Collectors

Corpus doesn't wait for you to paste things in. Five collectors run automatically on a nightly schedule, each watching a different channel where knowledge tends to accumulate. They pull raw material down, deduplicate it, and drop it into a shared inbox — a staging area that the ingest pipeline drains the same night. Nothing becomes a corpus page at collection time; that promotion happens later, under the ingest step's stricter rules.

!!! abstract "How collectors relate to the rest of the pipeline"
    Collection is intake only. Collectors write immutable raw source files — they never touch corpus pages, never modify what they previously collected, and never make editorial judgments. The [ingest pipeline](how-it-works.md) handles routing, extraction, and page creation.

## At a glance

| Channel | Trigger | What gets captured |
|---|---|---|
| **Email** | Starred messages + 9 topic labels | Message body, links, metadata; message is un-labelled and archived after ingest |
| **YouTube** | Videos in your watched playlists | Timestamped transcripts + video/channel metadata |
| **PDFs** | Files dropped in a watched Drive folder | Extracted text + document metadata |
| **Obsidian** | Notes in configured vault folders | Full note content; vault note can be reaped after ingest |
| **GitHub** | Repos you star | README + Markdown docs + repo metadata digest |

---

## Email

The email collector watches two distinct surfaces in your inbox:

1. **Starred messages** — any message you star is queued for collection on the next run.
2. **Topic labels** — a fixed set of nine thematic labels (data engineering, machine learning, ML engineering, MLOps, productivity, prompting, and a few others) acts as a lightweight triage system. Apply a label to any thread and the collector picks it up automatically.

After a message is successfully collected and ingested, the collector removes the label and archives the message. Your inbox stays clean; the knowledge lives in the corpus instead.

!!! tip "Zero-friction triage"
    Starring or labelling is the entire user action required. The rest happens overnight without further input.

Deduplication is by message ID — re-labelling a message you've already ingested won't create a duplicate raw file.

---

## YouTube

The YouTube collector scans your saved playlists and downloads timestamped transcripts for any video it hasn't seen before. Deduplication is by video ID; each video is collected exactly once regardless of how many playlists it appears in.

Timestamps are preserved in the raw transcript file, which means the ingest pipeline can later produce citations that link directly to a specific moment in a video — useful when a 45-minute talk makes one genuinely important point at the 31-minute mark.

!!! note "Rate limits and gradual recovery"
    YouTube's transcript API imposes rate limits. When a transcript can't be fetched on a given run, the collector marks it as pending rather than failing silently. Subsequent nightly runs retry pending videos until all transcripts are recovered — no manual intervention needed.

The collector processes dozens of playlists on each run, making it practical to maintain a broad watchlist without worrying about throughput.

---

## PDFs

Drop a PDF into a configured Google Drive folder — including any subfolder within it — and the collector picks it up on the next nightly run. It extracts the document text and preserves metadata (title, page count, file name) in the raw capture alongside the content.

This makes PDFs first-class citizens alongside web articles and transcripts. Research papers, slide decks exported as PDFs, and dense technical documents all flow through the same ingest pipeline as any other source.

Deduplication is by file identity: re-uploading the same file won't produce a second raw entry.

!!! warning "Scanned PDFs"
    The collector extracts text-layer content. Image-only scanned documents without an OCR layer will produce an empty or sparse raw file that won't yield useful corpus pages.

---

## Obsidian

The Obsidian collector reads notes from configured vault folders — web clippings saved via browser extension, book notes, reference summaries, anything you've already annotated by hand. Because these are first-party notes, they carry higher trust: the tags and structure you applied are treated as authoritative routing hints by the ingest pipeline.

After a note's content is safely collected **and** confirmed ingested into the corpus, the original vault note can be *reaped* — deleted from the vault. The reap is recoverable from the vault's own git history, so nothing is permanently lost. Notes are never reaped before their content is confirmed in the corpus.

!!! abstract "Vault folders stay tidy"
    The combination of collection → ingest → reap means your vault gradually sheds processed notes rather than accumulating them indefinitely. The knowledge migrates into the corpus; the vault retains only what's unprocessed or actively in use.

Two sub-cases apply: notes in designated PARA-native paths (such as Articles or Study Notes folders) are read and stamped in place without being copied elsewhere; notes that don't have a canonical PARA home arrive via the inbox path.

---

## GitHub

The GitHub collector watches your starred repositories. For each newly starred repo it hasn't seen before, it assembles a *repo digest*: the README, any Markdown documentation files found in the repo, a metadata block (description, topics, primary language, star count, latest release tag).

This is a read-only, additive operation: the collector **never un-stars** a repository. Your GitHub stars remain exactly as you left them, functioning as bookmarks independently of whether the corpus has ingested a given repo.

Deduplication is by repository name. Re-starring a repo you previously starred (or that has already been ingested) won't trigger a second collection pass.

!!! tip "Practical use"
    Star a repo when you want to remember why it matters. The collector turns that gesture into a structured raw file; the ingest pipeline turns that file into corpus pages that cite the actual README content rather than just a URL.

---

## Shared disciplines

All five collectors follow the same underlying contract:

- **Dedup before write.** Each channel has a stable identity key (message ID, video ID, file identity, repo name). Nothing is collected twice.
- **Immutable raw capture.** Collectors write and never edit. Once a raw file exists it is treated as a read-only record by everything downstream.
- **Collection ≠ ingestion.** Dropping something into the inbox does not create a corpus page. The ingest pipeline makes that decision — applying domain routing, provenance rules, and citation discipline.
- **Failures are visible.** Rate-limit hits, unreachable sources, and parse errors are logged rather than silently skipped.

---

**Next:** [How It Works](how-it-works.md) — how the ingest pipeline turns raw files into cited, cross-linked corpus pages.
