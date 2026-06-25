---
type: entity
domain: productivity
status: stub
sources:
  - path: raw/github/github-jackyzha0-quartz.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Quartz
  - Quartz v5
  - quartz SSG
  - digital garden SSG
  - Obsidian publishing
  - jackyzha0/quartz
tags:
  - corpus/productivity
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Quartz SSG

**TL;DR** — Quartz is an open-source TypeScript static-site generator that turns Obsidian vaults (or any folder of Markdown) into navigable websites with backlinks, graph view, and networked-thought structure intact. The de facto tool for publishing a digital garden [^src1].

## What it is

- **Repository**: `jackyzha0/quartz` on GitHub — 12,577+ stars (as of ingest date) [^src1].
- **Language**: TypeScript.
- **GitHub topics**: `digital-garden`, `networked-thought`, `obsidian`, `publishing`, `static-site-generator` [^src1].
- **Version**: Quartz v5 is the current major version; prior versions (v4, v3) are legacy but still documented.

## Core function

Quartz reads a directory of Markdown files and emits a static website [^src1]. Key features:

- Converts `[[WikiLink]]` syntax to resolved HTML links (critical for Obsidian vaults where all internal links are WikiLinks).
- Renders the **backlinks graph** as an interactive, explorable visualization.
- Generates a **graph view** per page and a global graph for the whole vault.
- Produces a search index (full-text search in-browser, no backend).
- Supports tags, folders, custom layouts, and RSS/Atom feeds.

## Integration with Obsidian

Quartz is purpose-built for Obsidian vaults but is not officially affiliated with Obsidian. Workflow:

1. Keep the vault as the source of truth (local Markdown files).
2. Point Quartz at the vault directory; it handles WikiLink resolution, frontmatter parsing, and asset bundling.
3. Deploy the built static site to GitHub Pages, Netlify, Cloudflare Pages, or any static host.

This is a non-destructive publishing pipeline: source files are untouched; Quartz only reads them.

## Why it matters in the productivity domain

Publishing a second brain / digital garden externally turns a private knowledge system into a shareable reference — the "learn in public" and "digital garden" patterns favoured by PKM communities. Quartz is the standard implementation path for Obsidian users who want an external-facing garden without a CMS or database.

See [[productivity/obsidian-pkm|Obsidian & PKM]] for vault architecture and [[productivity/ai-augmented-knowledge-work|AI-Augmented Knowledge Work]] for the relationship between the vault and AI context layers.

---

[^src1]: [jackyzha0/quartz (GitHub)](../../raw/github/github-jackyzha0-quartz.md)
