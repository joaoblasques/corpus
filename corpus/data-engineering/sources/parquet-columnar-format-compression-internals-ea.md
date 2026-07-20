---
type: source
domain: data-engineering
status: stub
sources:
  - path: raw/notes/notes-03-resources-articles-parquet-columnar-format-compression-internals.md
    channel: notes
    ingested_at: 2026-07-20
aliases: []
tags:
  - corpus/data-engineering
  - source
  - doc-quick-intake
created: 2026-07-20
updated: 2026-07-20
provisional: false
url: 
origin: obsidian
---

# Parquet Columnar Format & Compression Internals

> **Quick intake** (obsidian). raw stub: `notes-03-resources-articles-parquet-columnar-format-compression-internals.md`

This document explains the Parquet columnar file format, its encoding techniques (Run-Length Encoding and Dictionary Encoding), and optional compression codec (zstd) for efficient data storage and querying. Parquet's columnar layout and encoding strategies can shrink data 8x or more compared to CSV. Understanding these internals is essential for designing efficient pipelines.

**Key topics**
- Parquet columnar file format
- Run-Length Encoding (RLE)
- Dictionary Encoding
- zstd compression codec
- data compression
- columnar storage
