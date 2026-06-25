---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-RLt0Rfc-4Lg-the-fastest-way-to-create-polished-slides-with-ai-agents.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-X5h4J_JeZ8A-claude-just-destroyed-power-point-with-this-insane-update.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-wpVyP75UvjM-claude-just-changed-how-i-make-presentations.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-nAfbaZysFuk-i-replaced-powerpoint-with-claude-code.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-0V2yEaph7ac-how-to-build-pro-presentations-in-claude-cowork.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-4KC7Vn4txkA-how-to-create-slide-presentations-with-claude-2025-update.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-t2ELuj2prA0-claude-html-slides-the-new-powerpoint-killer-full-tutorial.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - AI presentation tools
  - Claude slides
  - presentation automation
  - Claude Designs
  - Claude PowerPoint
  - Gamma API
  - HTML slides
  - brand design system
  - component libraries
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-20
updated: 2026-06-25
---

# AI Presentation Tools

**TL;DR**: Multiple approaches exist for generating polished slide decks with AI — from built-in Claude capabilities (Claude Designs, PowerPoint add-in) to code-first workflows using Claude Code + Gamma API or bespoke HTML generation. The Claude Slides playlist (6 videos) maps the full landscape.

## Approaches

### 1. Claude Designs (Anthropic Labs)
An Anthropic-built feature in Claude.ai for generating visual slide decks and UI designs directly from a prompt. The feature was released as part of an update characterized as Claude "destroying PowerPoint" [^src2]. Can generate multi-slide decks with visual layout, not just bullet text.

### 2. Claude PowerPoint Add-in (Microsoft Marketplace)
A native add-in for PowerPoint available at `marketplace.microsoft.com`. Integrates Claude into the PowerPoint editing interface, enabling prompt-based slide generation and modification within the familiar Office environment [^src3].

### 3. Gamma API + Claude Code
Claude Code can call the Gamma API to auto-generate polished presentations as part of an agent workflow. Faster than starting from scratch and produces professional layouts without manual design work [^src1]. Suitable for teams wanting to automate the "slide deck from spec" step in a delivery pipeline.

### 4. Claude Code → HTML slides (full brand design system approach)
Replace PowerPoint entirely with Claude Code generating HTML-based presentations. The full-tutorial approach (2026) documents a systematic workflow using a complete brand design system [^src4][^src7]:

**Phase 1 — Brand design system**: define a `brand-system.md` with color palette (primary, secondary, neutrals), typography (font family, size scale, weights), spacing tokens, and shadow/border-radius conventions. Claude reads this first and applies it consistently across all slides [^src7].

**Phase 2 — Component libraries**: build reusable HTML/CSS components (title card, content card, data visualization card, quote card) before generating full decks. Each component is tested standalone before combining [^src7].

**Phase 3 — Animated charts**: charts built in pure HTML/CSS/JS rather than static images — bars animate on scroll-into-view using `IntersectionObserver`; numbers count up; line charts draw progressively [^src7].

**Photo integration**: Unsplash URLs (direct CDN links, no API key) for free, high-quality photography. Pattern: `https://source.unsplash.com/1600x900/?<keyword>` [^src7].

The result is version-controllable, diff-able, and deployable as a static page. "Free vs PowerPoint and Gamma" is the positioning: no subscription, no export limits, full programmatic control [^src7].

One practitioner also documented building slides using design tokens and 20 design principles — consistent typography scale, color tokens, spacing system, and component hierarchy [^src4].

### 5. Claude Cowork presentation skill
A custom skill in [[ai-engineering/claude-cowork|Claude Cowork]] that wraps a presentation-builder workflow — triggered by `/presentations` or similar, guiding the operator through structure, content, and output format [^src5]. Integrates with the Cowork folder system for persisting slide templates and brand assets.

### 6. Basic prompt-to-PowerPoint
The simplest workflow: paste an outline into Claude.ai and instruct it to produce a PowerPoint-compatible structure, then copy into slides. Lower quality than the above but zero setup [^src6]. Primarily useful as a first draft accelerator.

## Design principles for HTML slides (via Claude Code)

When generating HTML slides, twenty design principles improve output quality [^src4]:
- **Token-driven**: extract colors, spacing, and typography into CSS variables (design tokens) before writing component CSS.
- **Component hierarchy**: define slide shell → section dividers → content cards → typography scale.
- **Progressive enhancement**: ensure legibility without JavaScript; enhance with transitions only after.
- **Presenter view**: expose speaker notes as a `<aside>` element hidden in presentation mode.
- **Export path**: HTML → PDF via print-to-PDF or `puppeteer` ensures a shareable deliverable.

## Trade-offs

| Approach | Setup | Quality | Version control |
|---|---|---|---|
| Claude Designs | None | High (visual) | None |
| PowerPoint add-in | Low | High (PPT-native) | Via OneDrive |
| Gamma API | Medium | High (web design) | API contract |
| HTML via Claude Code | Medium | Fully custom | Git-native |
| Cowork skill | Medium | Workflow-defined | Skill file |
| Basic prompt | None | Low | None |

## See also

- [[ai-engineering/claude-cowork|Claude Cowork]] — skill system; `/presentations` workflow
- [[ai-engineering/claude-code|Claude Code]] — HTML generation, design.md conventions
- [[ai-engineering/agent-skills|Agent Skills]] — wrapping presentation workflows as skills
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [The Fastest Way to Create Polished Slides with AI Agents](../../raw/youtube/youtube-RLt0Rfc-4Lg-the-fastest-way-to-create-polished-slides-with-ai-agents.md) — YouTube playlist: Claude Slides
[^src2]: [Claude Just Destroyed PowerPoint with This Insane Update](../../raw/youtube/youtube-X5h4J_JeZ8A-claude-just-destroyed-power-point-with-this-insane-update.md) — YouTube playlist: Claude Slides
[^src3]: [Claude Just Changed How I Make Presentations](../../raw/youtube/youtube-wpVyP75UvjM-claude-just-changed-how-i-make-presentations.md) — YouTube playlist: Claude Slides
[^src4]: [I Replaced PowerPoint with Claude Code](../../raw/youtube/youtube-nAfbaZysFuk-i-replaced-powerpoint-with-claude-code.md) — YouTube playlist: Claude Slides
[^src5]: [How to Build Pro Presentations in Claude Cowork](../../raw/youtube/youtube-0V2yEaph7ac-how-to-build-pro-presentations-in-claude-cowork.md) — YouTube playlist: Claude Slides
[^src6]: [How to Create Slide Presentations with Claude — 2025 Update](../../raw/youtube/youtube-4KC7Vn4txkA-how-to-create-slide-presentations-with-claude-2025-update.md) — YouTube playlist: Claude Slides
[^src7]: [Claude HTML Slides: The New PowerPoint Killer (Full Tutorial)](../../raw/youtube/youtube-t2ELuj2prA0-claude-html-slides-the-new-powerpoint-killer-full-tutorial.md) — YouTube
