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
tags:
  - corpus/productivity
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Obsidian & Personal Knowledge Management

**TL;DR** — Obsidian is a local-first note app: a **vault is just a folder of plain-text Markdown files** on your machine, so your notes outlive the app and open in any editor [^src1][^src2]. The core value is **linking ideas, not filing them** — capture with near-zero friction, connect notes with backlinks, and let structure *emerge* over time rather than imposing folder hierarchies up front [^src1][^src2]. Both sources converge on the same discipline: start simple, link first, earn structure later.

## What Obsidian is

- A **vault** is a folder of files on your computer; notes are plain-text Markdown, "not stuck in some database in a cloud server somewhere" — if Obsidian disappears, the notes remain openable in any Markdown-capable app [^src2]. The same note opens identically in VS Code, TextEdit, iA Writer, etc. [^src1].
- **You own your data.** Sync is optional via any cloud service (Dropbox) or paid Obsidian Sync (end-to-end encrypted, version history) [^src1].
- Highly extensible via core and community **plugins** and **themes**; "with great flexibility comes great complexity" [^src2].

## Markdown & capture mechanics

Both videos teach the same Markdown surface: `#` headings (more hashes = smaller), `**bold**` / `*italic*`, `-` bullets and numbered lists, `==highlight==`, `~~strikethrough~~`, `- [ ]` checkboxes, `>` quote/callout blocks, `` ` `` inline and ``` ``` ``` code, `---` divider [^src1][^src2]. Links are the heart of it: `[[double brackets]]` for internal links, `[text](url)` for external [^src1][^src2].

A defining feature: **you can link to a note that does not exist yet**, then create it later by clicking the link — "create that backlink and come back to it later" [^src2]. This lets capture and connection happen in the same motion [^src1].

> Recommended early setting: **Files & Links → automatically update internal links**, so renaming a note doesn't break the links pointing at it [^src1].

## Linking over filing (the central idea)

The corpus-relevant thesis is that **connection beats categorization**:

- **Backlinks** relate notes to each other; *linked mentions* (an explicit `[[link]]`) and *unlinked mentions* (the note's title appears as plain text, convertible to a real link with one click) both surface in a note's footer/side panel [^src2].
- **Structure must be earned.** "Don't overfolder your ideas… categories get so fuzzy and ambiguous that standard hierarchies become brittle. Keep things in big buckets until patterns naturally show up" [^src1]. Folders create "cognitive friction" — deciding which folder a cross-cutting note belongs to wastes time and suppresses note-making [^src2].
- A pragmatic minimal folder scheme: three big buckets — **Atlas** (timeless ideas/knowledge), **Calendar** (time-based notes, e.g. daily notes), **Efforts** (time-bound projects/tasks) — then subfolder only as deserved [^src1]. The alternative simple scheme from the other source: one folder per year plus an `_utilities` folder (underscore sorts it to the top) [^src2].
- Prefer **Maps of Content (MOCs)** — index notes that link related notes by topic/theme — over tags for building "strong connective hubs" in the graph [^src1].

This *emergent structure* discipline is the same anti-drift principle the corpus itself follows: route into existing buckets, let new structure appear only when it earns its place. See [[productivity/README|Productivity]].

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

Obsidian ships **no built-in AI**; you decide how much to integrate based on your privacy needs [^src1]. One source pairs Obsidian with **Claude** to "ask questions… talk to my notes, do deep research, and instantly populate properties," while keeping a deliberate separation between original thinking ("idea verse") and AI-generated notes so the vault "stays a sacred space" — and backing up before any AI experiment [^src1]. The Claude/LLM side of this lives in the ai-engineering domain; see [[ai-engineering/claude-cowork|Claude Cowork]] for AI-over-local-files workflows. This complements [[productivity/ai-augmented-knowledge-work|AI-Augmented Knowledge Work]], which covers standing-context files and voice/about-me files.

## Related

- [[productivity/learning-to-learn|Learning to Learn]] — writing-to-process; PKM is the tooling layer for that habit.
- [[productivity/ai-augmented-knowledge-work|AI-Augmented Knowledge Work]] — about-me/voice files are themselves curated Markdown, the same substrate.

[^src1]: [Give Me 15 Minutes. I'll Teach You 80% of Obsidian](../../raw/youtube/youtube-z4AbijUCoKU-give-me-15-minutes-i-ll-teach-you-80-of-obsidian.md) (Linking Your Thinking / Nick Milo)
[^src2]: [The Ultimate Obsidian for Beginner's Guide 2025](../../raw/youtube/youtube-gafuqdKwD_U-the-ultimate-obsidian-for-beginner-s-guide-2025.md) (CreaDev Labs)
