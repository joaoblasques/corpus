# Corpus Documentation Website — Design Spec

> Date: 2026-06-22
> Status: **design approved**; ready for implementation plan
> An external-facing docs site that showcases, explains, and teaches the Corpus project.

## 1. Problem & goal

The Corpus project has grown fast (collectors, the cluster ingest pipeline, the Custodian
runtime, scheduled automation). It deserves an external-facing **documentation website** that
does three jobs at once: **showcase** it (polished, impressive), **explain** the idea (the
self-organizing LLM-wiki personal KB + its architecture), and **guide** a reader who wants to
understand or stand up something similar. Reference: the user's own
[Nora Bennett docs](https://docs.nora-bennett.com/) (Material for MkDocs). Visual direction is
its own: **"Knowledge Garden."**

## 2. Decisions (confirmed)

- **Tech:** MkDocs + **Material for MkDocs** (Python; matches the project + the Nora reference).
- **Purpose:** all three — showcase + concept explainer + how-to.
- **Visual:** "Knowledge Garden" — warm paper background, **sage-green** primary, **amber**
  accent, **serif headings** + clean sans body, soft/organic; light **and** dark mode.
- **Location:** a new top-level **`website/`** dir (alongside `bin/`, `docs/`). NOT under
  `corpus/` or `raw/` — it is project tooling, not corpus data (preserves path isolation).
- **Deploy:** GitHub Pages. The corpus repo is **private**, so the **built site** is published
  to a dedicated **public** Pages target → public live URL. Source lives in the private repo.
- **Live numbers:** a build-time macro injects real `corpus/_index.md` counts (pages/sources/
  domains) into the Home page.
- **Content:** written from the real project (CLAUDE.md, specs, code, logs); accurate, linked.

## 3. Privacy constraints (hard)

The published site MUST NOT contain: corpus knowledge content (the actual pages), the user's
email or name-as-identifier, local filesystem paths (`/Users/...`), API/auth secrets, or
private repo internals beyond what's needed to explain the architecture. Only **aggregate**
stats (page/source/domain counts) and **system descriptions** are published.

## 4. Architecture

```
website/
  mkdocs.yml                 # Material theme, palette, nav, plugins, extensions
  docs/
    index.md                 # Home (showcase landing)
    the-idea.md              # concept / LLM-wiki pattern / provenance
    how-it-works.md          # pipeline end-to-end + Mermaid diagram
    collectors.md            # the 5 intake channels
    the-custodian.md         # autonomous runtime (Gardener, harness, vision)
    under-the-hood.md        # schema, domains, schedule, Sonnet/Opus split
    getting-started.md       # install + configure + run
    roadmap.md               # what's next
    assets/                  # logo/favicon, custom CSS
    stylesheets/extra.css    # Knowledge-Garden palette + serif headings
  hooks/site_stats.py        # build-time stats provider (see §6)
.github/workflows/docs.yml   # build + publish to public Pages target
website/requirements.txt     # mkdocs-material, mkdocs-macros-plugin
```

### 4.1 `mkdocs.yml`
- `theme.name: material`; palette: two schemes (default + slate), `primary`/`accent` set via
  custom CSS variables (Material's named palette lacks sage/amber → override in `extra.css`).
- `theme.font`: heading serif (e.g. **Lora**), body sans (e.g. **Inter**) via Google Fonts.
- Features: `navigation.instant`, `navigation.sections`, `navigation.top`, `content.code.copy`,
  `search.suggest`, `toc.integrate` off.
- Extensions: `admonition`, `pymdownx.highlight`, `pymdownx.superfences` (+ mermaid fence),
  `pymdownx.tabbed`, `tables`, `toc` (permalink), `attr_list`, `md_in_html`.
- Plugins: `search`, `macros` (mkdocs-macros-plugin).
- `extra_css: [stylesheets/extra.css]`.

### 4.2 Visual identity (`stylesheets/extra.css`)
- `--md-primary-fg-color`: sage green (~`#5a7a5a` light / adjusted for dark).
- `--md-accent-fg-color`: amber (~`#c8862a`).
- Light scheme: warm paper bg (~`#faf8f2`); Dark scheme: warm-charcoal bg.
- Headings: serif (Lora); body: Inter. Rounded cards, soft section dividers.
- A small leaf/growth motif as the logo/favicon (simple inline SVG).

## 5. Pages (content responsibilities)

| Page | Covers |
|---|---|
| **Home** (`index.md`) | Hero ("A knowledge base that tends itself"), 3-line what-it-is, **live numbers** (pages/sources/domains), one-glance flow (sources → ingest → cited pages), feature cards, links into the deeper pages. |
| **The Idea** | The LLM-wiki pattern (Karpathy-inspired); why a *personal, self-organizing* KB; the non-negotiable **provenance** rule (every claim cited, §7); claim lifecycle (confidence, supersession). |
| **How It Works** | The pipeline: collect → `raw/_inbox` → cluster ingest → `corpus/` pages → indexes; the raw/corpus layering; a Mermaid flow diagram. |
| **Collectors** | The five intake channels — **email** (starred + labels), **YouTube** (playlists), **PDFs** (Drive folder, recursive), **Obsidian** (vault folders), **GitHub** (starred repos). One short section each: trigger, what's captured, dedup. |
| **The Custodian** | The showcase centerpiece: the autonomous runtime — the **Gardener** (fills thin pages, Opus writer + fail-closed Sonnet critic), the **safety harness** (caps, verifier-gate, main-only commits), governance (auto-commit vs review queue), and the **loop / adapt / dream** vision. |
| **Under the Hood** | The CLAUDE.md schema (page types, frontmatter, naming); domains; the nightly 2 AM schedule + weekly Opus synthesis; the **Sonnet/Opus split**; subscription-auth pattern. |
| **Getting Started** | Honest how-to: prerequisites, install, configure each collector, run the schedule; note it is shaped around a personal vault. |
| **Roadmap** | What's next: Adaptive Ingest, the Dreamer (idle consolidation + gated self-improvement). |

## 6. Live numbers (build-time)

`hooks/site_stats.py` is an MkDocs hook exposing a macro `corpus_stats()` that reads
`../corpus/_index.md`'s header line (`Total pages: N | Total sources: M`) and counts `corpus/*/`
domains, returning `{pages, sources, domains}`. The Home page uses `{{ corpus_stats().pages }}`
etc. If `_index.md` is unreadable (e.g. CI without the corpus), it falls back to last-known
constants so the build never breaks. **Only aggregate integers are emitted.**

## 7. Deploy

`.github/workflows/docs.yml`: on push to `main` touching `website/**`, set up Python, install
`website/requirements.txt`, `mkdocs build --strict` (fails on broken links/nav), then publish
the built `site/` to the public Pages target. Because the source repo is private, the workflow
pushes the built site to a dedicated **public** repo's Pages (or GitHub Pages if the plan
permits private Pages) — resolved at deploy time. A manual `mkdocs gh-deploy`-style path is the
fallback for the first live URL. Final URL reported to the user.

## 8. Testing

- `site_stats.py`: parses a sample `_index.md` header → correct `{pages, sources, domains}`;
  missing/garbled file → fallback constants (no exception). Unit-tested.
- `mkdocs build --strict` succeeds (no broken internal links, nav resolves) — CI gate.
- Privacy check: a test/grep asserts no `/Users/`, no the-user-email, no secret patterns in
  `website/docs/**` published content.

## 9. Scope

In: the 8-page site, Knowledge-Garden theme, live-stats hook, strict build, public deploy.
Out: publishing actual corpus knowledge pages; a custom domain (default Pages URL unless the
user supplies one); search beyond Material's built-in; i18n; comments/analytics.

## 10. Decisions locked
1. MkDocs Material; `website/` at repo root; public Pages deploy of the built site only.
2. "Knowledge Garden" visual (sage/amber/serif, light+dark) via `extra.css`.
3. 8 pages covering showcase + explain + how-to; content from the real project.
4. Build-time live stats (aggregate only); strict build; hard privacy constraints (§3).
