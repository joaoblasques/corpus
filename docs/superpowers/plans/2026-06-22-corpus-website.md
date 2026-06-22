# Corpus Documentation Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (content pages parallelize well). Steps use `- [ ]`.

**Goal:** Build & deploy an external-facing MkDocs-Material site ("Knowledge Garden" look) that showcases, explains, and teaches the Corpus project — live on a public URL.

**Architecture:** A self-contained `website/` dir (Material for MkDocs) at repo root; a build-time hook injects real `corpus/_index.md` stats; 8 content pages written from the real project; a strict build + a privacy grep gate; the built site is published to a public GitHub Pages target (source repo is private).

**Tech Stack:** Python 3.12, MkDocs, `mkdocs-material`, `mkdocs-macros-plugin`, GitHub Actions/Pages. Tests via pytest + `mkdocs build --strict`.

## Global Constraints

- Everything lives under `website/` (+ `.github/workflows/docs.yml`). Never under `corpus/`/`raw/`.
- **Privacy (hard):** published `website/docs/**` must contain NO `/Users/...` paths, NO the user's email (`tilakapash@gmail.com` / git email), NO secrets/tokens, NO actual corpus knowledge-page content. Only aggregate stats + system descriptions.
- Visual: sage-green primary, amber accent, warm paper bg, serif headings (Lora) + sans body (Inter), light+dark. Via `website/docs/stylesheets/extra.css`.
- `mkdocs build --strict` MUST pass (no broken links / missing nav) as the build gate.
- Content is accurate to the real project (CLAUDE.md, `docs/superpowers/specs/*`, `bin/*`, memory) — never invented.

---

### Task 1: Scaffold + Knowledge-Garden theme

**Files:** Create `website/mkdocs.yml`, `website/requirements.txt`, `website/docs/stylesheets/extra.css`, and skeleton `website/docs/*.md` (one stub per nav entry).

- [ ] **Step 1:** Create `website/requirements.txt`:
```
mkdocs-material==9.5.44
mkdocs-macros-plugin==1.3.7
```

- [ ] **Step 2:** Create `website/mkdocs.yml`:
```yaml
site_name: Corpus
site_description: A personal knowledge base that tends itself — sources in, cited pages out.
site_url: https://joaoblasques.github.io/corpus-docs/
repo_url: https://github.com/joaoblasques/corpus
repo_name: corpus

theme:
  name: material
  custom_dir: docs/overrides
  palette:
    - scheme: default
      toggle: { icon: material/weather-night, name: Dark mode }
    - scheme: slate
      toggle: { icon: material/weather-sunny, name: Light mode }
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant
    - navigation.sections
    - navigation.top
    - content.code.copy
    - search.suggest
    - toc.follow
  icon:
    logo: material/sprout

nav:
  - Home: index.md
  - The Idea: the-idea.md
  - How It Works: how-it-works.md
  - Collectors: collectors.md
  - The Custodian: the-custodian.md
  - Under the Hood: under-the-hood.md
  - Getting Started: getting-started.md
  - Roadmap: roadmap.md

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - pymdownx.highlight
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed: { alternate_style: true }
  - toc: { permalink: true }

plugins:
  - search
  - macros:
      module_name: hooks/site_stats

extra_css:
  - stylesheets/extra.css
```

- [ ] **Step 3:** Create `website/docs/stylesheets/extra.css` (Knowledge-Garden palette + serif headings):
```css
:root {
  --md-primary-fg-color: #5a7a5a;        /* sage */
  --md-primary-fg-color--light: #6f8e6f;
  --md-primary-fg-color--dark: #46603f;
  --md-accent-fg-color: #c8862a;          /* amber */
}
[data-md-color-scheme="default"] {
  --md-default-bg-color: #faf8f2;          /* warm paper */
  --md-typeset-a-color: #4f6f4f;
}
[data-md-color-scheme="slate"] {
  --md-default-bg-color: #1c1b18;          /* warm charcoal */
  --md-primary-fg-color: #8fae8a;
  --md-accent-fg-color: #e0a747;
}
/* Serif headings via Google Fonts (loaded in overrides/main.html) */
.md-typeset h1, .md-typeset h2, .md-typeset h3 {
  font-family: "Lora", Georgia, serif;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.md-typeset h1 { color: var(--md-primary-fg-color--dark); }
/* Soft feature cards on the home grid */
.grid.cards > :is(ul,ol) > li, .grid > .card {
  border-radius: 12px;
}
```

- [ ] **Step 4:** Create `website/docs/overrides/main.html` to load the Lora serif font:
```html
{% extends "base.html" %}
{% block extrahead %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&display=swap" rel="stylesheet">
{% endblock %}
```

- [ ] **Step 5:** Create one stub per nav page so the build resolves. Each `website/docs/<name>.md` starts with `# <Title>` + a one-line placeholder. Files: `index.md, the-idea.md, how-it-works.md, collectors.md, the-custodian.md, under-the-hood.md, getting-started.md, roadmap.md`.

- [ ] **Step 6:** Create `website/docs/hooks/site_stats.py` as a minimal stub so the macros plugin loads (real logic in Task 2):
```python
def define_env(env):
    @env.macro
    def corpus_stats():
        return {"pages": 213, "sources": 568, "domains": 7}
```

- [ ] **Step 7:** Verify the build:
```bash
cd website && python3 -m pip install -r requirements.txt -q && python3 -m mkdocs build --strict
```
Expected: `Documentation built` with no warnings/errors.

- [ ] **Step 8:** Commit:
```bash
git add website && git commit -m "feat(website): scaffold MkDocs Material + Knowledge-Garden theme"
```

---

### Task 2: Live-stats hook (the one unit-tested piece)

**Files:** Modify `website/docs/hooks/site_stats.py`; Create `tests/test_site_stats.py`.

**Interfaces:** Produces `read_corpus_stats(index_path=None) -> dict` with keys `pages, sources, domains` (ints), and the `corpus_stats` macro wrapping it. Fallback constants `{213, 568, 7}` on any read/parse failure.

- [ ] **Step 1:** Write `tests/test_site_stats.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "website" / "docs" / "hooks"))
import site_stats as st  # noqa: E402


def test_reads_header_counts(tmp_path):
    idx = tmp_path / "_index.md"
    idx.write_text("# Corpus Index\n> Last updated: 2026-06-21 02:00 | Total pages: 213 | Total sources: 568\n",
                   encoding="utf-8")
    (tmp_path / "ai-engineering").mkdir(); (tmp_path / "data-engineering").mkdir()
    s = st.read_corpus_stats(index_path=idx)
    assert s["pages"] == 213 and s["sources"] == 568 and s["domains"] == 2


def test_missing_file_falls_back(tmp_path):
    s = st.read_corpus_stats(index_path=tmp_path / "nope.md")
    assert s["pages"] >= 1 and s["sources"] >= 1 and s["domains"] >= 1   # fallback constants, no raise


def test_garbled_header_falls_back(tmp_path):
    idx = tmp_path / "_index.md"; idx.write_text("no counts here", encoding="utf-8")
    s = st.read_corpus_stats(index_path=idx)
    assert set(s) == {"pages", "sources", "domains"}
```

- [ ] **Step 2:** Run → FAIL (`read_corpus_stats` undefined): `python3 -m pytest tests/test_site_stats.py -q`

- [ ] **Step 3:** Implement `website/docs/hooks/site_stats.py`:
```python
"""MkDocs-macros hook: inject real corpus stats (aggregate integers only) at build time."""
import re
from pathlib import Path

FALLBACK = {"pages": 213, "sources": 568, "domains": 7}
_HEADER = re.compile(r"Total pages:\s*(\d+)\s*\|\s*Total sources:\s*(\d+)")


def read_corpus_stats(index_path=None) -> dict:
    idx = Path(index_path) if index_path else Path(__file__).resolve().parents[3] / "corpus" / "_index.md"
    try:
        text = idx.read_text(encoding="utf-8", errors="ignore")
        m = _HEADER.search(text)
        if not m:
            return dict(FALLBACK)
        domains = sum(1 for p in idx.parent.iterdir() if p.is_dir() and not p.name.startswith("_"))
        return {"pages": int(m.group(1)), "sources": int(m.group(2)), "domains": domains or FALLBACK["domains"]}
    except OSError:
        return dict(FALLBACK)


def define_env(env):
    @env.macro
    def corpus_stats():
        return read_corpus_stats()
```

- [ ] **Step 4:** Run → PASS: `python3 -m pytest tests/test_site_stats.py -q`

- [ ] **Step 5:** Commit: `git add website/docs/hooks/site_stats.py tests/test_site_stats.py && git commit -m "feat(website): build-time corpus stats hook (aggregate-only, fallback-safe)"`

---

### Task 3–5: Content pages (parallelizable — each page independent)

Each page is written FROM the real project. Source map: `CLAUDE.md` (schema/§7/domains), `docs/superpowers/specs/2026-06-*` (Custodian, Gardener, gmail, github), `bin/*` (collectors, scheduled_run, custodian, gardener), the memory index. **Honor the privacy constraints** — describe the system; never paste `/Users/` paths, the user's email, secrets, or real corpus page content. Use admonitions, tables, and Mermaid diagrams. Each page ends links to 1–2 sibling pages.

- [ ] **Task 3 — Home + The Idea + How It Works**
  - `index.md`: Material **hero** + `.grid.cards`. Headline "A knowledge base that tends itself." Subhead (sources in, cited pages out). A stats row using the macro: `**{{ corpus_stats().pages }}** pages · **{{ corpus_stats().sources }}** sources · **{{ corpus_stats().domains }}** domains`. A one-glance Mermaid flow (sources → inbox → ingest → cited pages). 4–6 feature cards linking to deeper pages.
  - `the-idea.md`: the LLM-wiki pattern (Karpathy-inspired, personal); why self-organizing; the **provenance** rule (every claim cited — §7); claim lifecycle (confidence/supersession). ~500–800 words.
  - `how-it-works.md`: the pipeline collect → `raw/_inbox` → cluster ingest → `corpus/<domain>/` → indexes; the immutable-raw / derived-corpus layering; a Mermaid sequence/flow. ~500–800 words.
  - Build `mkdocs build --strict` passes; commit `feat(website): home, the-idea, how-it-works`.

- [ ] **Task 4 — Collectors + The Custodian**
  - `collectors.md`: intro + one subsection each for **email** (starred + 9 topic labels, un-label/archive), **YouTube** (76 playlists), **PDFs** (Drive folder, recursive incl. subfolders), **Obsidian** (vault folders, reaped after ingest), **GitHub** (starred repos, repo digest, never un-stars). Each: trigger · what's captured · dedup. A small table summarizing the 5 channels.
  - `the-custodian.md` (the centerpiece): the autonomous runtime — the **Gardener** (fills `stub` pages into cited drafts; **Opus writer + fail-closed Sonnet critic**; 6/8 filled in the first real run); the **safety harness** (caps, fingerprint stop, verifier-gate, main-only commits, the $47k-runaway lesson); **governance** (verify-pass+reversible → auto-commit, else → review queue); the **loop / adapt / dream** vision (Gardener → Adaptive Ingest → Dreamer). Mermaid of the govern decision. ~700–1000 words.
  - Build strict passes; commit `feat(website): collectors + the-custodian`.

- [ ] **Task 5 — Under the Hood + Getting Started + Roadmap**
  - `under-the-hood.md`: the CLAUDE.md schema (page types, frontmatter, kebab naming, wikilinks); domains (the 7, emergent-structure rules); the **2 AM nightly** schedule + **weekly Opus synthesis**; the **Sonnet (bulk) / Opus (deep) split** + subscription-auth pattern (no metered API). ~600–900 words.
  - `getting-started.md`: honest how-to — prerequisites (Python, `gh`, a vault), install, configure each collector (generic, no personal paths), run the schedule (launchd daily). Note it's shaped around a personal vault. ~500–700 words.
  - `roadmap.md`: shipped (collectors, cluster ingest, Custodian harness, Gardener, the site) + next (Adaptive Ingest, the Dreamer: idle consolidation + gated self-improvement). A checklist/timeline. ~300–500 words.
  - Build strict passes; commit `feat(website): under-the-hood, getting-started, roadmap`.

---

### Task 6: Privacy gate + strict build

**Files:** Create `tests/test_website_privacy.py`.

- [ ] **Step 1:** Write the test:
```python
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "website" / "docs"
FORBIDDEN = ["/Users/", "tilakapash@gmail.com", "ANTHROPIC_API_KEY", "Bearer ", "ghp_", "sk-ant"]


def test_no_private_data_in_published_docs():
    offenders = []
    for md in DOCS.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for needle in FORBIDDEN:
            if needle in text:
                offenders.append(f"{md.relative_to(DOCS)}: {needle}")
    assert not offenders, offenders
```

- [ ] **Step 2:** Run → PASS (fix any offender by rewording the content): `python3 -m pytest tests/test_website_privacy.py -q`

- [ ] **Step 3:** Full gate: `python3 -m pytest tests/test_site_stats.py tests/test_website_privacy.py -q` and `cd website && python3 -m mkdocs build --strict`.

- [ ] **Step 4:** Commit: `git add tests/test_website_privacy.py && git commit -m "test(website): privacy gate — no paths/emails/secrets in published docs"`

---

### Task 7: Deploy to a public URL

**Files:** Create `.github/workflows/docs.yml`.

Because `joaoblasques/corpus` is **private**, publish the built site to a dedicated **public** repo's Pages so the URL is free + public. Two-part: (a) one-time public repo + first deploy (controller does this live with `gh`), (b) the CI workflow for subsequent pushes.

- [ ] **Step 1 (one-time, controller):** create the public docs repo + first deploy:
```bash
gh repo create joaoblasques/corpus-docs --public -d "Corpus — documentation site" 2>/dev/null || true
cd website && python3 -m mkdocs build --strict
cd site && git init -q && git add -A && git commit -q -m "deploy: corpus docs site" \
  && git branch -M gh-pages \
  && git remote add origin https://github.com/joaoblasques/corpus-docs.git \
  && git push -fq origin gh-pages
gh api -X POST repos/joaoblasques/corpus-docs/pages -f source[branch]=gh-pages -f source[path]=/ 2>/dev/null || \
  gh api -X PUT repos/joaoblasques/corpus-docs/pages -f source[branch]=gh-pages 2>/dev/null || true
```
Live URL: `https://joaoblasques.github.io/corpus-docs/`. Report it to the user.

- [ ] **Step 2:** Create `.github/workflows/docs.yml` for ongoing deploys (runs in the private repo; pushes built site to the public docs repo via a PAT secret `DOCS_DEPLOY_TOKEN`):
```yaml
name: Deploy docs
on:
  push:
    branches: [main]
    paths: ["website/**", ".github/workflows/docs.yml"]
permissions:
  contents: read
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r website/requirements.txt
      - run: cd website && mkdocs build --strict
      - name: Publish to public Pages repo
        run: |
          cd website/site
          git init -q && git add -A
          git -c user.email=ci@corpus -c user.name=corpus-ci commit -q -m "deploy: ${GITHUB_SHA::7}"
          git push -fq "https://x-access-token:${{ secrets.DOCS_DEPLOY_TOKEN }}@github.com/joaoblasques/corpus-docs.git" HEAD:gh-pages
```

- [ ] **Step 3:** Note for the user: the workflow needs a repo secret `DOCS_DEPLOY_TOKEN` (a fine-scoped PAT with `contents:write` on `corpus-docs`). The first deploy in Step 1 doesn't need it (uses local `gh` auth). Commit the workflow: `git add .github/workflows/docs.yml && git commit -m "ci(website): deploy docs to public Pages on push"`.

---

## Notes for the executor
- Content tasks 3–5 parallelize (independent pages); build `--strict` after assembling each batch.
- The privacy test (Task 6) is the safety net — run it before any deploy.
- If `corpus-docs` Pages isn't live immediately, GitHub Pages can take 1–2 min to provision; the URL is `https://joaoblasques.github.io/corpus-docs/`.
- Keep the corpus repo's own test suite green; these website tests live alongside it under `tests/`.
