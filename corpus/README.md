---
type: bundle-readme
title: Corpus — OKF v0.1 knowledge bundle
---

# Corpus — OKF v0.1 Knowledge Bundle

This directory is a **Google Open Knowledge Format (OKF) v0.1** bundle.

## What is OKF?

OKF is a portable, self-contained knowledge representation format. See the [Google OKF specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) for full details.

## Bundle contents

This `corpus/` directory is a standalone OKF v0.1 bundle, conforming to the specification:

- **Version declaration**: OKF version is declared as `okf_version: "0.1"` in `index.md`.
- **Concept documents**: Every markdown file in this directory is a concept document. Each document MUST begin with YAML frontmatter containing a non-empty `type` field. Other fields (title, domain, status, etc.) are optional and used by this corpus's schema, but `type` is required for OKF conformance.
- **Cross-links**: Markdown links are root-relative (e.g., ``[Text](/<domain>/<page>.md)``) with no Obsidian wikilinks. Links are untyped; broken links are tolerated per the OKF spec.
- **Reserved files**:
  - `index.md` — directory catalog (no frontmatter, progressive-disclosure format).
  - `log.md` — append-only change history (newest-first, `## YYYY-MM-DD` format).

## Validation

Validate OKF conformance by running:

```bash
python3 bin/okf_lint.py
```

This checker enforces three core rules:
1. Every concept document has YAML frontmatter.
2. Every frontmatter block contains a non-empty `type` field.
3. Reserved files (`index.md`, `log.md`) conform to their prescribed format.

A conformant bundle reports `"violations": 0`.

## Portability

A copy of the `corpus/` directory (and only this directory, not the surrounding repo) is a complete, portable OKF v0.1 bundle. It can be ingested, queried, and migrated independently of its source repository.
