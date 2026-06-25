---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/email/email-2026-06-21-claude-linkedin.md
    channel: email
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-5-claude-ai-skill-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - ghost voice
  - voice training Claude
  - Claude LinkedIn
  - LinkedIn AI posts
  - AI writing in your voice
  - personal brand AI
  - stylometry AI
  - Spiral writing
tags:
  - corpus/ai-business
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# AI Content With Your Voice

**TL;DR.** The common failure mode of AI-assisted content is generic output ("write me a video about money"). The durable play — called "ghost voice" or stylometry-based voice training — is feeding the model your own corpus (transcripts, voice memos, past posts, testimonials) so it drafts *with* you rather than *for* you, "in your voice, on your topics, using the exact phrases" [^src2]. Two concrete applications: Claude trained on LinkedIn posts for social content, and Spiral as a dedicated stylometry tool for brand voice. Both frame the model as a mirror, not a ghostwriter.

## The ghost voice skill

"It is not supposed to write content for you. It's supposed to write content with you in your voice, on your topics, using the exact phrases. And the garbage AI content that you see everywhere on YouTube and TikTok, that is people typing 'write me a video about money' into a chat bot and posting whatever comes out" [^src2].

The ghost voice setup [^src2]:
1. Create a Claude project.
2. Upload everything you have: past blog posts, video transcripts, voice memos, quirks, slang, life story, testimonials from clients, sales calls, comments/interactions.
3. Give it instructions: "Write in my voice, use these phrases, avoid those phrases."
4. Ask for hooks, scripts, captions, emails. Tell it the outcome you want and let it interview you until it has enough context.
5. First 10 outputs need editing; edit the prompt until the voice is right.

"Claude becomes a mirror. It writes the script that you would have written if you had 40 more hours in your week… You just show up and be the person on camera" [^src2].

Client example: Antoine (Black Heights channel) was spending hours per script; with Claude doing heavy lifting, his production time was cut in half and the channel reached five figures/month [^src2].

## Claude trained on LinkedIn posts

A step-by-step workflow for turning your LinkedIn post history into a reusable Claude skill [^src1]:

**Step 1 — Extract your posts.** Use Apify (not free but ~$5 in credits covers 2,000 posts) to safely and legally scrape your public LinkedIn posts as a CSV/XLSX. The key is not doing it from your account (automation violates LinkedIn ToS); public posts are openly on the web [^src1].

**Step 2 — Train Claude on the data.** Upload the spreadsheet to Claude and run a detailed analytics prompt that handles LinkedIn export quirks:
- The `type` column says "post" for every row — ignore it; derive format from media columns (document = carousel, postVideo = video, article = link, postImages = image, else text-only)
- Engagement = likes + comments + shares; reaction mix signals emotional register
- Timestamp derived from activity ID: `id >> 22` → Unix milliseconds

The prompt generates a report with: bottom-line summary, format performance (avg/median engagement by type), winning angles/hooks ranked by engagement, biggest outliers analyzed, and a Stop/Continue/Start recommendation [^src1].

**Step 3 — Create a reusable skill.** Use `/skill-creator` to build a personal skill that captures your voice report and SOP. When invoked, the skill uses `AskUserQuestion` to get input before generating hooks/angles/captions. The skill then helps assemble a post collaboratively [^src1].

**Step 4 — Capture a viral post recipe.** Take a screenshot of your best-performing post and have Claude build a separate skill capturing its recipe: format, hook (first two visible lines), caption structure, tone, line breaks. This skill can recreate the pattern for any new topic [^src1].

**Promo framing (from Ruben Hassid, 700K+ readers)**: the newsletter is building toward a ghostwriting agency pitch. The core workflow is solid but the funnel is toward a paid circle ($200/yr, 3,700 members) [^src1].

**Limitations acknowledged** [^src1]:
- "AI isn't creative. It's really good at following instructions."
- Not faster per post — but you spend time more efficiently.
- Claude at $100/month is expensive relative to casual use.
- Only worth it if posting at least once/week with enough past posts.
- Training on bad content won't make good posts; quality-gate your input.
- "Ultra-viral is often novelty" — the skill helps with repetition, not breakthrough originality.

## Spiral — dedicated stylometry tool

Spiral (writewithspiral.com) is built explicitly on stylometry — "the nearly 200-year-old science of analyzing linguistic patterns to determine authorship" — applied to AI content [^src3]:

- Analyzes sentence length distributions, punctuation frequency, word choice ratios, and syntactic structures across your writing corpus.
- "These patterns hold remarkably stable across a writer's body of work" (the same property that resolved disputed authorship of the Federalist Papers).
- Maps your voice across every channel, then builds custom styles your whole team can use.
- Key differentiator: "ChatGPT and Claude don't have custom stylometrics built in. Spiral does."

Spiral positions itself as an "opinionated writing partner with taste, built on Every's editorial standards" — pre-configured to push back, ask clarifying questions, and present multiple drafts [^src3].

Pricing: $15/month personal, $25/user/month team, $30/month for the Every bundle (includes Cora, Monologue, Sparkle, Proof). MCP + API access included at all tiers [^src3].

Use case: "handles the drafts you don't want to write, sharpens the ones you do, and keeps your voice consistent whether you're writing a tweet or a 3,000-word essay" [^src3].

## Conversion engineering — words as the product

A related skill: **conversion engineering** — using your offer + the customer's exact language as inputs to generate sales copy. "Words make money, and the right words make a lot of money" [^src2].

Process [^src2]:
1. Pick one thing you sell or want to sell.
2. Open Claude, paste your offer description.
3. Paste 10–20 real audience quotes (comments on videos, email replies, actual words people have said).
4. Ask Claude for: a hook for the top of the sales page, three email subject lines, one CTA in the customer's exact language.
5. Test and pick the winner.

"Hiring a top copywriter used to cost five to fifty thousand dollars for a single sales page… the conversion engineer skill flips that: you + Claude + the right inputs (your offer + your customer's exact language) = sales copy that outperforms most agency work" [^src2].

Example: Carla (1,500 YouTube subscribers, 100–200 views/video) closed a six-figure contract using Claude-written copy focused on exact client language rather than vanity metrics [^src2].

## Relationship to other pages

- **[[ai-business/monetizing-code|Monetizing Code]]** — the positioning one-pager (seven-question self-interview) + "clarity test" prompt maps to conversion engineering here; both are about selling outcomes in the buyer's language.
- **[[ai-business/ai-consulting-playbook|AI Consulting Playbook]]** — the "ghost voice" skill is the same mechanism as the client-specific Claude skills described there; this page provides the *content creation* use case.
- **[[ai-business/boring-expert-businesses|Boring Expert Businesses]]** — a compliance or fractional executive business can use ghost voice / conversion engineering to scale outreach messaging.

[^src1]: [Claude + LinkedIn (Ruben Hassid newsletter)](../../raw/email/email-2026-06-21-claude-linkedin.md)
[^src2]: [5 Claude AI Skills That Pay More Than a College Degree](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-5-claude-ai-skill-report.md) — lead-gen video funneling to coaching program; income screenshots used as social proof; video report from Obsidian vault
[^src3]: [Spiral — The writing partner for you and your agent](../../raw/web/web-spiral-the-writing-partner-for-you-and-your-agent.md)
