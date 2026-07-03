---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-claude-code-is-terrible-at-design.md
    channel: web
    ingested_at: 2026-06-27
aliases:
  - Claude Code is terrible at design
  - Charlie Hills website workflow
  - spec-driven website build
  - CONTEXT COPY DESIGN workflow
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-27
updated: 2026-06-27
---

# Claude Code website build — the CONTEXT/COPY/DESIGN workflow (Charlie Hills)

**TL;DR.** A nine-step workflow for building a personal/marketing website with Claude Code that avoids the generic "AI look" (purple gradient, Inter font, identical bento cards). The core move is **spec-driven, approval-gated building**: separate the *facts*, the *copy*, and the *design* into three markdown files (`CONTEXT.md`, `COPY.md`, `DESIGN.md`), approve each before any code is written, and treat third-party components as **structural donors** whose styling is overridden by your design tokens [^src1]. The author's framing: Claude Code is "brilliant at building things that work and terrible at making them look good" — left alone it ships the same site as everyone else [^src1].

## The nine steps

1. **`CONTEXT.md` — the facts file.** Built in Claude Chat (which already has months of context on the user), using a one-question-at-a-time interview before drafting, then confirming the fact list. Holds who/what, every number and proof point, story, frameworks, and voice rules [^src1].
2. **Interview → `COPY.md`.** Claude proposes the page list, confirms it, then interviews one page at a time about gaps (what each page must say, proof, the call-to-action, and what searches it should rank for), drafting all copy into `COPY.md` for review before any build [^src1].
3. **Approve every word before any code.** `COPY.md` carries headlines, sections, title tags, meta descriptions, and a per-page SEO map; the user edits via instructions until approved [^src1].
4. **`DESIGN.md` — merge your brand with sites you love.** Gather ~5 admired design systems (downloaded as `DESIGN.md` files from a style library) plus a brand kit; Claude merges them into one `DESIGN.md` with a **decision log**. Rule of precedence: the user's **brand wins on colours and fonts**, the references **win on layout and feel** [^src1].
5. **Build, then verify.** `DESIGN.md` becomes styling tokens; `COPY.md` becomes pages verbatim. Claude runs the site locally, **screenshots every page, and reviews its own screenshots against `DESIGN.md`**, fixing failures before the user ever loads it [^src1].
6. **Add components as structural donors.** Premium components (e.g. from 21st.dev) arrive "wearing their own clothes." A standing `CLAUDE.md` rule treats any pasted component as a **structural donor only**: replace demo copy with `COPY.md`, translate every hardcoded colour/border/shadow/font to `DESIGN.md` tokens, ignore stock-image instructions, and drop unneeded parts [^src1].
7. **Hero video via image→video models.** Generate a still (image model), animate it into a looping hero video (video model) with the frame held static; Claude compresses it with ffmpeg (the author's went 23 MB → 2.3 MB) to keep the page fast [^src1].
8. **Iterate — a lot.** [^src1]
9. **Ship.** [^src1]

## Why it works (the pattern)

The workflow is a concrete instance of **separating specification from generation and gating each artifact**: facts, copy, and design are each fixed and approved *before* code exists, so the model is never improvising substance and style simultaneously. The **structural-donor** rule is the key anti-"AI-slop" mechanism — it keeps the engineering of a borrowed component while forcing it to inherit the project's design tokens, so the site stays on-brand instead of inheriting each library's default look [^src1]. This mirrors the broader agentic-coding lesson that a strong upfront plan/spec avoids burning tokens course-correcting later (see [Claude Design](/ai-engineering/claude-design.md)'s plan-first phase and [Claude Code](/ai-engineering/claude-code.md)).

> Note: the source is a Substack newsletter (Charlie Hills) and includes a satirical aside about a model being "pulled" by a government order — treated here as the author's joke, not a factual claim. The load-bearing content is the workflow itself.

## See also

- [Claude Design](/ai-engineering/claude-design.md) — Anthropic's hosted design app; the design-system-first, plan-first counterpart to this files-in-the-repo approach
- [Claude Code](/ai-engineering/claude-code.md) — the agent executing this workflow; `CLAUDE.md` standing-rules convention
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Claude Code is terrible at design (Charlie Hills, Substack)](../../../raw/web/web-claude-code-is-terrible-at-design.md)
