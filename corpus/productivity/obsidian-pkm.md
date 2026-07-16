---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/youtube/youtube-z4AbijUCoKU-give-me-15-minutes-i-ll-teach-you-80-of-obsidian.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-gafuqdKwD_U-the-ultimate-obsidian-for-beginner-s-guide-2025.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/web/web-stop-writing-markdown-in-obsidian-do-this-instead.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/youtube/youtube-1RIXGL5Vgag-don-t-use-obsidian-with-claude-use-vs-code.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-40GPEEj3ijg-stop-learning-obsidian.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-47oi3Q9apK0-the-definitive-guide-to-setting-up-your-ai-second-brain.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-4l8MXYUqGaA-how-to-build-the-ultimate-ai-second-brain-obsidian-claude-co.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-jackyzha0-quartz.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Obsidian
  - personal knowledge management
  - PKM
  - second brain
  - note-taking
  - backlinks
  - maps of content
  - MOC
  - zettelkasten
  - context engineering
  - Claude Code Obsidian
  - Kepano skills
  - knowledge architect
tags:
  - corpus/productivity
  - concept
created: 2026-06-15
updated: 2026-06-25
---

# Obsidian & Personal Knowledge Management

**TL;DR** — Obsidian is a local-first note app: a **vault is just a folder of plain-text Markdown files** on your machine, so your notes outlive the app and open in any editor [^src1][^src2]. The core value is **linking ideas, not filing them** — capture with near-zero friction, connect notes with backlinks, and let structure *emerge* over time rather than imposing folder hierarchies up front [^src1][^src2]. Both sources converge on the same discipline: start simple, link first, earn structure later.

## What Obsidian is

- A **vault** is a folder of files on your computer; notes are plain-text Markdown, "not stuck in some database in a cloud server somewhere" — if Obsidian disappears, the notes remain openable in any Markdown-capable app [^src2]. The same note opens identically in VS Code, TextEdit, iA Writer, etc. [^src1].
- **You own your data.** Sync is optional via any cloud service (Dropbox) or paid Obsidian Sync (end-to-end encrypted, version history) [^src1].
- Highly extensible via core and community **plugins** and **themes**; "with great flexibility comes great complexity" [^src2].

## Markdown & capture mechanics

Both videos teach the same Markdown surface: `#` headings (more hashes = smaller), `**bold**` / `*italic*`, `-` bullets and numbered lists, `==highlight==`, `~~strikethrough~~`, `- [ ]` checkboxes, `>` quote/callout blocks, `` ` `` inline and ``` ``` ``` code, `---` divider [^src1][^src2]. Links are the heart of it: `Double Brackets` for internal links, `[text](url)` for external [^src1][^src2].

A defining feature: **you can link to a note that does not exist yet**, then create it later by clicking the link — "create that backlink and come back to it later" [^src2]. This lets capture and connection happen in the same motion [^src1].

> Recommended early setting: **Files & Links → automatically update internal links**, so renaming a note doesn't break the links pointing at it [^src1].

## Linking over filing (the central idea)

The corpus-relevant thesis is that **connection beats categorization**:

- **Backlinks** relate notes to each other; *linked mentions* (an explicit `Link`) and *unlinked mentions* (the note's title appears as plain text, convertible to a real link with one click) both surface in a note's footer/side panel [^src2].
- **Structure must be earned.** "Don't overfolder your ideas… categories get so fuzzy and ambiguous that standard hierarchies become brittle. Keep things in big buckets until patterns naturally show up" [^src1]. Folders create "cognitive friction" — deciding which folder a cross-cutting note belongs to wastes time and suppresses note-making [^src2].
- A pragmatic minimal folder scheme: three big buckets — **Atlas** (timeless ideas/knowledge), **Calendar** (time-based notes, e.g. daily notes), **Efforts** (time-bound projects/tasks) — then subfolder only as deserved [^src1]. The alternative simple scheme from the other source: one folder per year plus an `_utilities` folder (underscore sorts it to the top) [^src2].
- Prefer **Maps of Content (MOCs)** — index notes that link related notes by topic/theme — over tags for building "strong connective hubs" in the graph [^src1].

This *emergent structure* discipline is the same anti-drift principle the corpus itself follows: route into existing buckets, let new structure appear only when it earns its place. See [Productivity](/productivity/README.md).

## Organization methods (pick by temperament)

Obsidian offers several overlapping ways to resurface notes; the beginner guide frames them as a choose-your-style menu [^src2]:

| Method | Use when you… |
|---|---|
| **Folders** | like strict hierarchy |
| **Tags** (nestable with `/`) | want to categorize one note many ways |
| **Backlinks** | want to see connections between ideas |
| **Bookmarks** (incl. saved searches) | want an index / table of contents |
| **Properties** (YAML frontmatter) | want sortable/filterable metadata |
| **Search** | everything else — the always-available fallback |

**Properties** are YAML frontmatter (`---` at the top) holding typed metadata — text, list, number, checkbox, date — and are the recommended home for tags [^src1][^src2]. **Templates** (core plugin) inject reusable note skeletons — e.g. a book-notes or YouTube-video template with preset properties and a collapsed callout of reminders — via a hotkey [^src2].

## Graph view & Canvas

- **Graph view** visualizes all notes and their links; honestly assessed as more motivational than essential — the beginner guide's main practical use is **finding orphan notes** (no connections), a prompt to either link or delete them: "if there's nothing that note connects to… is it really worth keeping" [^src2]. It can be filtered/grouped/colored by tag or search query [^src2].
- **Canvas** is an infinite whiteboard: cards (local to the canvas), embedded vault notes, media, and web pages, with labeled directional connections and groups — useful for mind-mapping and, combined with the DataView community plugin, lightweight dashboards [^src2].

## Gotchas (common beginner mistakes)

From the 15-minute guide [^src1]:

- **Don't import everything** from an old notes app — dumping thousands of legacy notes makes the vault unsearchable. Start fresh, link your own thoughts.
- **Don't chase plugins on day one** (advanced tables, kanban, DataView) — focus on linking first.
- **Don't overfolder** (see above).
- **Don't put off learning hotkeys** — speed makes the tool enjoyable (`Cmd/Ctrl+O` quick switcher, `Cmd+P` command palette, `Cmd+B`/`Cmd+I`, etc.) [^src1].

## AI and Obsidian

Obsidian ships **no built-in AI**; you decide how much to integrate based on your privacy needs [^src1]. One source pairs Obsidian with **Claude** to "ask questions… talk to my notes, do deep research, and instantly populate properties," while keeping a deliberate separation between original thinking ("idea verse") and AI-generated notes so the vault "stays a sacred space" — and backing up before any AI experiment [^src1]. The Claude/LLM side of this lives in the ai-engineering domain; see [Claude Cowork](/ai-engineering/claude-cowork.md) for AI-over-local-files workflows. This complements [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md), which covers standing-context files and voice/about-me files.

## Markdown 2.0: notes as software (HTML-in-Obsidian)

One emerging pattern pushes beyond plain Markdown: embedding **HTML + JavaScript** inside vault notes to make them interactive software [^src3]. The motivating argument is **information density** — "rather than just walls of text, you can have tables, illustrations, code snippets, plots, diagrams, all within a single contained file" [^src3].

### What this unlocks

- **Slides from any outline.** An HTML artifact rendered inside Obsidian can advance bullet points interactively, replacing external slide tools [^src3].
- **Kanban/triage boards.** Drag-and-drop task views built as micro-software living directly in the vault [^src3].
- **Live dashboards from daily notes.** Via the **Dataview** community plugin (enable *inline queries* + *JavaScript queries* in settings), arbitrary code executes against vault data at render time. A sleep/energy dashboard that pulls from frontmatter properties and redraws in real time exemplifies this [^src3].

### Dynamic memory for Claude

The most striking claim: these dashboards function as **"dynamic memory"** for an AI agent — a shared "Command Center" that both the user and Claude read each morning [^src3]. Goals, metrics, and current context live in vault notes; Claude reads the same view the user sees. "You don't need to explain your goals every session" [^src3]. This connects the Obsidian substrate directly to the standing-context pattern in [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) (about-me/voice files), but makes the context *dynamic and self-updating* rather than manually curated.

### Tradeoffs vs plain Markdown

| Dimension | Plain Markdown | HTML-in-Obsidian |
|---|---|---|
| **Readability** | Human-readable anywhere | HTML tags opaque in raw view |
| **AI generation time** | Fast | ~2–4× slower; more tokens [^src3] |
| **Git diffs** | Clean line diffs | Hard to review HTML tag noise [^src3] |
| **Interactivity** | None | Full (JS, Dataview queries) |
| **Portability** | Any editor | Requires Obsidian + Dataview for live features |

### Relationship to prior Obsidian principles

This is an *extension*, not a contradiction, of the linking-over-filing thesis: the Markdown vault is still the substrate; HTML layers interactivity on top without abandoning plain-text ownership. The same files still live in folders, open in any text editor, and use YAML frontmatter — Dataview queries read those properties. The plain-Markdown gotchas (don't overfolder, don't chase plugins on day one) still apply; HTML/Dataview is an advanced layer, not a starting point.

## Context engineering as the real Obsidian skill

"Stop learning Obsidian features. Start engineering context" — the core thesis of the most useful practitioner take [^src4].

- **Kepano (Obsidian CEO) open-sourced his `obsidian-skills` repo** — a collection of slash-command skills specifically designed for Claude Code operating inside an Obsidian vault. The repo ships modular skills for different vault tasks; Claude generates syntactically correct WikiLinks, canvas JSON, and frontmatter without being told the format each session [^src4].
- **The architect/builder/material framing**: "You are the architect, Claude is the builder, Obsidian is the material." The architect *must* understand the material's constraints; but the architect doesn't swing hammers — that's the builder's job. "People keep learning more Obsidian features when what they should be learning is how to better describe what they want" [^src4].
- **Context engineering vs. memorizing tool features**: "The real skill isn't mastering Obsidian features. It's engineering the right context so Claude understands your vault's logic." Once the context is right, Claude generates correct WikiLinks, canvas JSON, and frontmatter without being told how each session. The skills repo is a context-engineering starter kit [^src4].
- **`/loop` command pattern**: Kepano's skills include a `/loop` command that runs a continuous improvement cycle inside the vault — read → propose → write → verify — without manual prompting per step. Matches the ai-engineering domain's agent-loop pattern [^src4].

## Zettelkasten + AI: thinking vs doing

Traditional Zettelkasten (atomic notes, connected notes, processing → not documenting) lives in the *thinking* brain, not the AI context layer [^src5].

- The Zettelkasten core disciplines: **atomic notes** (one idea per note), **connected notes** (each new note links to existing knowledge), **processing over capturing** ("don't just document, process what it means to you"). Quantity of notes is irrelevant without connections [^src5].
- The critical distinction: "Your Zettelkasten is your second brain. Your AI context folder is your AI brain's information diet." They should not be the same folder.
- The AI context folder has its own structure (see [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) §6) and is optimized for *feeding AI context*; the Zettelkasten is optimized for *human thinking*. Mixing the two degrades both [^src5].
- **Karpathy reference**: the LLM-wiki pattern (separate from personal note-taking) is the "doing" layer of the three-brain model; the thinking layer is emergent Zettelkasten [^src5].

## VS Code as a PKA alternative

A contrarian take: VS Code + Claude may be functionally superior to Obsidian for AI-augmented knowledge work [^src6].

- **Arguments against Obsidian for AI workflows**: (1) Obsidian's plugin-heavy workflow fragments and locks you into Obsidian-specific structures; (2) VS Code is free, local, file-based, portable, widely supported — same Markdown files, no vendor lock; (3) Claude Code was built for VS Code workflows, and the ICOR/loop workflow maps directly onto it [^src6].
- **The ICOR/Tom setup**: a local folder of Markdown files opened in VS Code, with multiple parallel Claude terminals in separate panes. `CLAUDE.md` file in the folder root gives Claude persistent instructions. Skills per project, each in its own Claude context. "You can have your whole knowledge base open in one terminal and your current project in another" [^src6].
- **Counter-position**: Obsidian's graph, backlinks, and visual canvas still differentiate it for *non-AI* note navigation; VS Code's advantage is primarily for users whose primary workflow is Claude Code interaction. The two can coexist — Obsidian for graph browsing, VS Code + Claude for active knowledge work — since both read the same Markdown files [^src6].

## Publishing: Quartz SSG

[Quartz v5](/productivity/quartz-ssg.md) is the leading static-site generator for Obsidian vaults as digital gardens [^src7]. It converts the vault's Markdown files (including WikiLinks, backlinks, and graph) into a navigable website — the same rendering pipeline that powers community "digital garden" sites. See [Quartz](/productivity/quartz-ssg.md) for full entity page.

## Related

- [Learning to Learn](/productivity/learning-to-learn.md) — writing-to-process; PKM is the tooling layer for that habit.
- [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) — about-me/voice files are themselves curated Markdown, the same substrate; HTML dashboards extend this to dynamic/auto-updating context.
- [Quartz SSG](/productivity/quartz-ssg.md) — publish an Obsidian vault as a digital garden.
- [Decision Making](/productivity/decision-making.md) — the Zettelkasten principle of atomic notes connects to how [decision frameworks](/productivity/decision-making.md) are best stored: one concept per note, not bundled.

[^src1]: [Give Me 15 Minutes. I'll Teach You 80% of Obsidian](../../raw/youtube/youtube-z4AbijUCoKU-give-me-15-minutes-i-ll-teach-you-80-of-obsidian.md) (Linking Your Thinking / Nick Milo)
[^src2]: [The Ultimate Obsidian for Beginner's Guide 2025](../../raw/youtube/youtube-gafuqdKwD_U-the-ultimate-obsidian-for-beginner-s-guide-2025.md) (CreaDev Labs)
[^src3]: [Stop Writing Markdown in Obsidian. Do This Instead](../../raw/web/web-stop-writing-markdown-in-obsidian-do-this-instead.md) (Artem / ArtemXTech Substack, "Markdown 2.0: Notes Are Software Now")
[^src4]: [Stop Learning Obsidian. Start Engineering Context](../../raw/youtube/youtube-40GPEEj3ijg-stop-learning-obsidian.md) — JB Russell
[^src5]: [The Definitive Guide to Setting Up Your AI Second Brain](../../raw/youtube/youtube-47oi3Q9apK0-the-definitive-guide-to-setting-up-your-ai-second-brain.md) — Vicky Zhao
[^src6]: [Don't Use Obsidian With Claude — Use VS Code](../../raw/youtube/youtube-1RIXGL5Vgag-don-t-use-obsidian-with-claude-use-vs-code.md) — ICOR with Tom
[^src7]: [jackyzha0/quartz (GitHub)](../../raw/github/github-jackyzha0-quartz.md)

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Personal Knowledge Corpus Pipeline](/ai-engineering/personal-knowledge-corpus-pipeline.md) · _ai-engineering_
- [Semantic Layer](/data-engineering/semantic-layer.md) · _data-engineering_
- [Context Engineering](/ai-engineering/context-engineering.md) · _ai-engineering_
- [Navigating a Technical Career](/ai-business/technical-career.md) · _ai-business_

<!-- RELATED:END -->
