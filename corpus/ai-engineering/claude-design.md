---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-gAoZ95kqG7w-claude-design-just-became-unstoppable.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/youtube/youtube-TcFeSjwTo7g-claude-design-builds-beautiful-3d-websites-instantly-full-tu.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/youtube/youtube-ovabeVoWrA0-claude-design-2-hour-course-beginner-to-pro.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Claude Design
  - Claude Designs
  - Anthropic Labs Design
  - Claude Design app
  - design system (Claude)
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-26
updated: 2026-06-26
confidence: 0.75
last_confirmed: 2026-06-26
---

# Claude Design

**TL;DR**: Claude Design is an Anthropic Labs product (launched **April 17, 2026**, the day after Claude Opus 4.7) that lets you "collaborate with Claude to create polished visual work like designs, prototypes, slides, one-pagers, and more" — and even animations and videos — using natural language [^src3]. It is a **separate app** in the Anthropic ecosystem alongside Claude Chat, Claude Cowork, and Claude Code, with a Lovable/Bolt-style interface that lowers the barrier to entry versus building designs inside Claude Code [^src1]. It is powered by Anthropic's "most capable vision model," **Opus 4.7** [^src1][^src3], available in research preview to paid subscribers only, with its **own usage limit** separate from regular Claude/Claude Code usage [^src3].

## What it is

Claude Design moves the design/prototype workflow out of raw Claude Code folders-and-files and onto a hosted, "lovable style interface" with a left-hand task list and a right-hand live preview [^src1]. Nate Herk frames it as "another iteration of Cowork, but this is for design" — the same surprise-free, iterate-all-the-way-through pattern, applied to visual work instead of code [^src1].

The launch sat directly on the Opus 4.7 release: the announcement called out a jump in **visual reasoning** benchmarks — "82% and 91% compared to Opus 4.6's 69% and 84.7%" — which is exactly the capability the product leans on [^src1]. Claude Design "uses its eyes to see what's going on on the page" to validate its own output and catch mistakes [^src3].

> [unsourced — exact benchmark names not given in source] The two visual-reasoning percentages are quoted from the video's reading of the announcement; the specific benchmark suites were not named.

## Capabilities

- **Prototypes** — wireframe or high-fidelity; start from a prompt or a hand-drawn **sketch** on the canvas to "visually get on the same page as Claude" [^src2].
- **Slide decks**, **one-pagers**, **templates**, plus **animations and videos** [^src3].
- **Import existing brand** — logos, brand assets, current websites/apps, or a GitHub repo, so output is consistent with an existing brand [^src1][^src3].
- **Organization-scoped sharing** — keep a design private or share it across a team [^src1].
- **Export** to Canva, PDF, PowerPoint, HTML, or Zip files [^src1][^src3].
- **Hand off to Claude Code** — "when a design is ready, Claude can package everything and you can pass it off to Claude Code to do the actual building and syncing to GitHub" [^src1].

## Design systems

The first recommended step is to **set up a design system** so "anyone can create good looking designs and assets" that stay on-brand by default [^src1]. The setup form takes a company name, a blurb, examples of existing design systems/products (a GitHub repo and brand-guidelines doc can be linked), the logo, and freeform notes on the desired feel [^src1].

Generation "takes about 15 minutes" — you can step away but must keep the tab open [^src1]. Claude imports from the linked GitHub repo, builds preview cards and styles, and surfaces **colors, accents/gradients, neutrals, typography, spacing, buttons, badges, and cards** for human approval ("looks good") before locking them in [^src1]. The output includes a `README` and a **`skill.md`** — "a machine-readable manifest for Claude Code" — plus (effectively) a design-system spec analogous to a `design.md` the agent reads to follow brand guidelines [^src1]. Once built, "your team's new projects will use this design system by default" [^src1]. Building a design system is acknowledged as **token-intensive** [^src3].

## Usage limits and model strategy

Claude Design is a **paid-only research preview** — available to Pro, Max, Team, and Enterprise subscribers; free-plan users must upgrade [^src3]. It has a **separate usage limit** from regular Claude and Claude Code ("Claude Design specific limit"), which "is pretty much a weekly reset"; hitting it means waiting for reset or buying extra usage out of balance [^src3]. The cost is real — one creator "spent over $200 in extra usage just playing around" [^src2].

Because Opus 4.7 "goes through tokens quicker" and is more expensive than Sonnet or Haiku, you can **switch which model** Claude Design uses to conserve the limit, trading visual quality for runtime [^src3]. The broader cost lesson mirrors agentic coding: a stronger **planning phase up front** (e.g. building the design system first, iterating in-interface) means "you are spending less because you're not chasing it down the wrong path and trying to course correct" [^src1].

## Building 3D / interactive websites

A representative workflow transforms a static site into an interactive, scroll-driven **3D** experience — cards that pop up, scenes that progress as you scroll — while preserving the original brand, colors, and copy [^src2]. The end-to-end flow: brainstorm the brand/spec in Claude Chat, generate a hero **background image** (e.g. via an image model — "nano banana two" — at 16:9) and animate it into a looping **hero video** (via a video model — "Seedance/CDance 2.0" — using the still as first and last frame so the camera doesn't move), then assemble in Claude Design starting from a high-fidelity prototype and a canvas sketch, dragging in the MP4 as the hero background, and finally deploy [^src2].

## Market context

- **Krieger (ex-Figma, Instagram co-founder) "left Figma pretty much right before the announcement of Claude Design" and is now Anthropic's CPO** — fuel for the "where are these tools headed" framing [^src3].
- Widely dubbed a **"Figma killer"** at release [^src3], though Anthropic and **Canva** publicly framed the relationship as collaborative, not competitive ("we've loved collaborating with Anthropic over the past couple of years") [^src1].

## See also

- [[ai-engineering/ai-presentation-tools|AI Presentation Tools]] — Claude Design is approach #1 in the slide/deck landscape
- [[ai-engineering/claude-code|Claude Code]] — the build/sync target Claude Design hands off to; `skill.md`/`design.md` conventions
- [[ai-engineering/claude-cowork|Claude Cowork]] — the sibling Labs product; Claude Design is "another iteration of Cowork, but for design"
- [[ai-engineering/claude-models|Claude Model Lineup]] — Opus 4.7 (vision) powers Claude Design; model-switching to conserve the limit
- [[ai-engineering/agent-cost-management|Agent Cost Management]] — plan-first to avoid burning the (separate, weekly) Design limit
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Claude Design Just Became Unstoppable (Nate Herk | AI Automation)](../../raw/youtube/youtube-gAoZ95kqG7w-claude-design-just-became-unstoppable.md)
[^src2]: [Claude Design Builds Beautiful 3D Websites Instantly — full tutorial (Nate Herk | AI Automation)](../../raw/youtube/youtube-TcFeSjwTo7g-claude-design-builds-beautiful-3d-websites-instantly-full-tu.md)
[^src3]: [Claude Design 2 HOUR COURSE — Beginner to Pro (Nate Herk | AI Automation)](../../raw/youtube/youtube-ovabeVoWrA0-claude-design-2-hour-course-beginner-to-pro.md)
