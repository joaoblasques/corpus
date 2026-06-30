# Source-channel specifics

## 10.1 Matter exports

Matter exports look like:
```yaml
---
title: ...
url: ...
author: ...
tags: [...]
date_published: ...
date_saved: ...
---
```
Plus highlights in the body marked with quote blocks.

**Rules**:
- Treat the user's **highlights** as higher signal than full body text. They've already done the curation.
- Existing Matter `tags` are **routing hints, not authoritative**. You may override with better domain placement, but log the override.
- Always preserve `url` in the source-summary page.

## 10.2 YouTube transcripts

Transcripts have channel + video metadata (in filename or YAML) and timestamps `[MM:SS]`.

**Rules**:
- Cite specific claims with timestamps: `[12:34](../../raw/youtube/<file>.md#t=12:34)`.
- The video's playlist (if present in metadata) is a strong domain hint.
- Skip routine intros, outros, and sponsor reads.

## 10.3 Web clips

- Use the URL as canonical identity (in source-summary page).
- If clipped via Obsidian Web Clipper, frontmatter is usually clean; trust it.

## 10.4 Personal notes (first-party vault content)

First-party notes the user authored or annotated — articles, study notes, book notes, course summaries. Higher trust signal than web clippings: the user already curated and processed these. Treat tags and structure as authoritative routing hints.

**Two sub-cases — check source location first (§8.1 Step 0):**

- **PARA-native** (files under a path listed in `corpus/_config.md` — currently `03_Resources/Articles/` and `03_Resources/Study Notes/`): ingest **in place** under Branch B. Do not copy to `raw/`. Stamp the file in place after ingest.
- **`raw/notes/`** (no PARA home): first-party notes that arrived via inbox or have no canonical PARA location. Treat as immutable like any other raw-channel file. Ingest under Branch C.

When in doubt whether a file has a PARA home, check `corpus/_config.md` before deciding which sub-case applies.
