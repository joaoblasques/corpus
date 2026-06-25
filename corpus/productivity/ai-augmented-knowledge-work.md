---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/email/email-2026-05-25-reclaim-6-hours-of-your-week-in-10-mins.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-03-you-re-just-a-text-file.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-08-loop-engineering.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/youtube/youtube-yjO9UHIunSE-jfdi-system-my-ai-executive-assistant-full-life-command-cent.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-CvLkhGWZlvE-how-i-turned-claude-into-my-personal-assistant-full-guide.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-1dYp9ymqy_g-it-s-cognitive-uploading-how-google-notebooklm-s-steven-john.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-47oi3Q9apK0-the-definitive-guide-to-setting-up-your-ai-second-brain.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-4l8MXYUqGaA-how-to-build-the-ultimate-ai-second-brain-obsidian-claude-co.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-5H-s-TIO0QE-build-this-once-any-ai-you-use-will-get-smarter-forever.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-py3szwKAZYU-pro-ai-dictation-tips-for-superwhisper-mastering-context-awa.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - AI workflow
  - voice file
  - about-me file
  - loop engineering
  - reclaim hours
  - cognitive uploading
  - information hierarchy
  - three brains
  - second brain
  - NotebookLM
  - SuperWhisper
  - AI dictation
tags:
  - corpus/productivity
  - concept
created: 2026-06-12
updated: 2026-06-25
---

# AI-Augmented Knowledge Work

**TL;DR** — Set up reusable AI scaffolding once so each task costs seconds, not a cold re-explanation. Three escalating moves: (1) **standing instructions and projects** so the model already knows who you are; (2) **a compressed "about-me" file** that captures your voice and taste for any model; (3) **loop engineering** — designing systems that prompt agents instead of you prompting them. Across all three, *judgment and verification stay human* [^src1][^src2][^src3].

## 1. Standing context (the weekly setup ritual)

The anti-pattern: opening a blank chat every morning and re-explaining yourself — "like onboarding a new employee daily and firing them at 5pm" [^src1]. Spend ~15 minutes once; every later check-in takes 30 seconds [^src1].

- **Profile preferences**: tell the model exactly how to behave (skip preamble, lead with the answer, give a real recommendation not a neutral list, push back on bad ideas) [^src1].
- **Projects as memory**: a workspace where instructions and files ride into every chat; train 2–3 on your real samples [^src1].
- **Make it interrogate you first**: have the model attack then steel-man your plan before giving an opinion — "two minutes answering > twenty minutes correcting" [^src1].
- **Prompting mechanics** (attributed to Anthropic's guidance): say what *to* do not what to avoid; explain the *why*; 3–5 examples is the sweet spot for steering tone; **query-last ordering** (long doc on top, question at the bottom) can improve answers up to 30% on big inputs [^src1]. See [[ai-engineering/prompt-engineering|Prompt Engineering]] if present.

## 2. The about-me / voice file

"Give me 2 hours. One file. And any AI becomes you" [^src2]. The claim: your voice and taste are patterns, and patterns fit in a portable text file usable across Claude, ChatGPT, Gemini, etc. [^src2].

- **Two-step extraction**: a "Taste Interviewer" prompt runs ~100 questions across beliefs, writing mechanics, aesthetic crimes, voice, structure, hard nos, red flags — then a "Voice Compiler" prompt compresses the 20k-word dump to a 2–4k-token, XML-structured file (hard ceiling 5k) [^src2].
- **Compression test**: keep a line only if removing it would change how the AI writes, edits, judges, refuses, or decides — "maximum behavioral fidelity per token" [^src2].
- **Why compress**: the raw dump "eats too much of your context window" and re-costs tokens every turn [^src2].
- **Payoff**: you become *portable* (hand the file to a teammate or ghostwriter) and *consistent* — "a resource instead of a bottleneck." Edit the file often, because taste changes [^src2].
- **Caveat surfaced by the source**: consistency makes you predictable; the file is a tool to free time for thinking and choosing the right task, not just to go faster [^src2].

## 3. Loop engineering

"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents" (Steinberger); "My job is to write loops" (Boris Cherny, Claude Code lead) [^src3]. A loop is a recursive goal: define a purpose, the AI iterates until complete [^src3].

- **Five building blocks plus memory**, present in both Claude Code and Codex [^src3]:
  1. **Automations** — scheduled discovery/triage (the "heartbeat"); Claude Code via `/loop`, cron, hooks, or GitHub Actions.
  2. **Worktrees** — isolated checkouts so parallel agents don't collide.
  3. **Skills** — project knowledge written once (a `SKILL.md`) so the loop stops re-deriving intent every cycle.
  4. **Plugins / connectors** (MCP) — let the loop act in real tools (issue tracker, DB, Slack).
  5. **Sub-agents** — separate the maker from the checker; the model that wrote code grades its own homework too kindly. (`/goal` runs until a verifiable condition holds, with a fresh model judging "done.")
  - **Memory** — a markdown file or board outside the conversation: "The agent forgets, the repo doesn't" [^src3].
- **What the loop does NOT remove** [^src3]: verification is still yours ("done" is a claim, not a proof); **comprehension debt** grows faster as the loop ships code you didn't write; and the comfortable posture — "cognitive surrender" — is the dangerous one. "Build the loop. Stay the engineer."

> Two people can build the same loop and get opposite results — one to move faster on work they understand, the other to avoid understanding it. "The loop doesn't know the difference. You do" [^src3].

This is the productivity face of agent orchestration; see [[ai-engineering/agentic-coding|Agentic Coding]] / loop and harness pages in the ai-engineering domain for the engineering depth, and [[productivity/shipping-and-scope|Shipping and Scope]] for why verification of outcomes is the durable skill.

## 6. The three-brain model (human / AI / shared second brain)

A framework for keeping thinking and doing cleanly separated [^src7]:

- **Human brain → thinking**: deep, effortful, friction-full thinking; powered by experience, curiosity, taste, judgment. Output: critical thinking, mental models, creativity. "We are too eager to make thinking frictionless… when it comes to building our capacity to think it is the wrong choice" [^src7].
- **AI brain → doing**: following workflows, coding, knowledge work tasks. Great at step-by-step execution; poor at genuine thinking ("it hallucinates, can't really get to the real point if you know what's going on") [^src7].
- **Shared second brain → context**: the repository that feeds both. Separating human thinking notes (bottom-up, emergent, zettelkasten-style) from AI context folders (top-down, hierarchical, five file types) prevents both pollution of your thinking garden and cognitive overhead while doing [^src7].

**Golden rules** [^src7]:
1. Do not mix human and AI output — you need to know which ideas are yours and which are AI-generated.
2. Do not distract thinking with doing — task lists and project management should live in a separate space from your thinking notes.

**Five types of AI context files** (the "doing" folder) [^src7]:
- **About-me**: who you are, preferences, standards, what you dislike, your goals. The primary personalization layer.
- **Frameworks**: your SOPs, personal matrices, decision heuristics. Prevents the AI from defaulting to "average" internet patterns. "If you can't articulate what good means, you can't complain the AI is giving you crap."
- **Examples**: both good and bad examples of outputs; show AI what good means concretely, not just describe it.
- **Knowledge base**: everything the AI needs as source of truth for this domain.
- **Knowledge map**: an index that describes the hierarchy so the AI knows where to look.

The output loop: AI creates something → you evaluate → feed it back into the knowledge base as a good or bad example, which grows the context over time [^src7]. This mirrors Karpathy's LLM-wiki pattern but distinguishes the thinking (human-owned) layer from the doing (AI-fed) layer.

## 7. The information hierarchy (AI-portable context)

"You don't build agents, you build the information that they read. The agent is just whatever AI you point at your information hierarchy" [^src8].

**The friction tax** solved by this structure [^src8]:
- Re-explaining yourself every new chat ("like onboarding a new employee daily and firing them at 5pm") [^src1].
- Memory locked to one tool — switch tools, lose everything.
- Subscription roulette: five tools, unclear which you actually use.

**Two-tier structure** [^src8]:
- **Top tier — business folder** (changes rarely): `about-me.md`, `about-my-business.md`, `about-my-voice.md` (highest-leverage: writing style, tone, phrases to use/avoid), `my-offers.md`.
- **Bottom tier — project folders** (one per project/client): five subfolders each: `instructions/` (the Claude.md), `voice/` (project-specific), `references/` (research, SOPs — fastest SOP creation: record yourself with Loom, it auto-generates SOP), `examples/` (3–5 best past outputs), `notes/` (ongoing updates — "this week's newsletter had 42% open rate; story approach worked" — this is how the AI gets smarter over time).

**The key insight**: "The AI is the disposable part. The hierarchy is the part that lasts." Point Claude at it today; point Gemini at it tomorrow — same files, same results. Three years from now, half of today's AI tools will be gone; the hierarchy persists and keeps improving [^src8].

## 8. The two-layer second brain (meta + project)

A practitioner setup for Obsidian + Claude Code that combines strategic thinking with tactical execution [^src9]:

- **Layer 1 (meta / strategy)**: Claude as thinking partner, acting as "general of an army." Has access to notes (books, courses, videos), journals, goals, reviews, and the project layer. Answers strategic questions: "What should I do?" Two skills: `new project` (interviews you to create a new layer-2 project) and `weekly update` (refreshes all context).
- **Layer 2 (project / execution)**: Claude as a "soldier" with a very specific task. Each project folder has its own Claude.md (role, project scope, skills), input/process/output folders, and skills specific to that project. Claude in this context only cares about its project role — "the narrowness is the power."

**Mobile access**: use Claude's dispatch/remote feature to control the desktop brain from your phone. "Leave your computer on. You have full access to your second brain entirely from anywhere in the world" [^src9].

**Team sync**: Obsidian Sync ($4/month) replicates the vault across team members — every collaborator gets the same project structure, same Claude context, same skills [^src9].

**Key principle**: "AI is to help us achieve what God has already put on our hearts. Don't let the robot decide your fate" — personalize the structure to your actual goals, not someone else's template. Copy the structure; never copy the content [^src9].

## 9. Cognitive uploading vs cognitive offloading

Steven Johnson (co-founder, Google NotebookLM) distinguishes two modes of AI use [^src6]:

- **Cognitive offloading** (the risk): relying on AI to think for you. Students passing classes without understanding; professionals using AI to reply to emails without reading them. "Eventually you'll hit a wall where someone will be like, you don't understand anything that's going on here" [^src6].
- **Cognitive uploading** (the opportunity): using AI as an extension of memory. Decades of highlights, quotes, research notes stored in a notebook, then dynamically surfaced based on what you're working on *right now*. "I've got this offline collection of things that influenced me… now I think of a tool like NotebookLM as basically cognitive uploading… it can figure out the most relevant bits from my whole history of ideas and put that into my brain" [^src6].

**The serendipity gain**: the fear that AI kills serendipitous connections is backwards. With a rich notebook, you can follow any impulse of curiosity with "much less resistance." Johnson's book research on the Gold Rush: 13–14 minutes to assemble comprehensive knowledge on a highly obscure wagon-train topic that previously would have taken four weeks [^src6].

**Inverted search**: beyond finding things you specified, these tools excel at finding *what you didn't specify* — "go through all your sources and be like, 'Oh, the thing you didn't mention is this one crazy thing'" [^src6]. Searching for the negative space: "take a look at this literature and give me a list of unasked questions that would be relevant." This is barely exploited yet [^src6].

**AI as ghostwriter, not author**: paragraph-by-paragraph directed writing — you know what you want to say (outlines, wrestling with ideas); AI generates first drafts of each paragraph guided by your instructions and your knowledge base. "The argument and the structure and the narrative and the ideas were generated by a human; the first draft of each paragraph was generated by AI based on the guidance and instructions of the human" [^src6]. Compare: one-shot "write me a five-page paper" produces slop; guided step-by-step with your knowledge base produces something with your voice.

## 10. SuperWhisper: context-aware AI dictation

SuperWhisper is a voice-to-text tool whose context awareness transforms it from transcription into a full AI-processing layer for dictation [^src10].

**Three types of context** (only active when explicitly toggled) [^src10]:
1. **Application context**: reads the active window via Accessibility API — app name, vocabulary, names, and all text in the active input field. Captured *after* transcription completes (timing matters: don't switch windows during long transcriptions).
2. **Clipboard context**: captures the last copied content within ~3 seconds before dictation start or during dictation. Captured when you stop recording.
3. **Selected text context**: captures selected text at the moment you press start. Not available in custom modes by default — must be enabled by editing the mode's JSON config file (change `contextFromSelection` from `false` to `true`, restart app).

**Design principle**: "use these toggles intentionally." Application context active on a translation-only mode sends unnecessary context and confuses the AI; the toggle should only be on when the task genuinely needs window content [^src10].

**Power pattern**: combine all three — select a markdown table (selected text), copy source content from a website mid-dictation (clipboard), and speak a combining instruction, all while staying in the destination window (application context). One dictation, three sources of context, one combined output [^src10].

**Custom modes**: each mode has its own AI prompt and context settings. The default built-in modes are mostly transcription-only; real power requires custom modes. Most useful for generating content, reformatting, summarizing, or coding — not just converting speech to text [^src10].

**Reprocessing trick** (undocumented): if a dictation fails, the recording is preserved in History. To reprocess *with context*, don't use the built-in Reprocess button — instead, run a script that opens the most recent recording file with SuperWhisper, while in the window you want for application context, with selected text pre-captured from a prior session stored in an invisible buffer. This lets you recover full context-aware processing from a failed session [^src10].

## 4. The JFDI system (AI executive assistant)

A practitioner-built "JFDI system" (Just Freaking Do It) demonstrates a fully automated personal operating system powered by AI agents [^src4]. Core automation flows:

**8:30 AM auto-dashboard** [^src4]: at startup, the system automatically:
1. Checks calendar for today's meetings (loads agenda, attendee info, relevant notes).
2. Reviews open tasks and projects; surfaces what's at risk.
3. Pulls email threads that need decisions.
4. Generates a single "today's focus" brief — no manual morning review.

**Goal alignment** [^src4]: every task is scored against a proportional-allocation model — what % of this week should go to each goal area? The system flags when actual time allocation drifts more than 20% from the target, surfacing "you're spending 60% of this week on reactive email but your Q3 goal is product strategy."

**CRM automation** [^src4]: after every meeting or call, the system:
- Extracts action items and commitments from meeting notes.
- Logs contact updates (new role, project, mention).
- Reminds you to follow up with anyone you haven't spoken to in N days.

**Knowledge auto-routing** [^src4]: documents, links, and notes dropped into a designated inbox are automatically classified (project vs. reference vs. archive), tagged, and routed — no manual filing. 

**Spark file** [^src4]: a dedicated inbox for half-formed ideas, quotes, and observations. The system surfaces spark-file items weekly, clusters related ones, and asks "is this worth developing?"

## 5. The personal AI OS (Claude + Supabase + Telegram)

A second practitioner documents a "personal AI OS" built from three layers [^src5]:

**Design layer (Claude Designs → Claude Code)** [^src5]: wireframes and specs go through Claude Designs first; the result feeds Claude Code for implementation. This creates an iterative design-code loop where visual prototypes are cheap and code is generated against a spec, not guessed from a vague prompt.

**Backend layer (Supabase)** [^src5]: all persistent data (contacts, habits, finances, journal entries) lives in Supabase — an open-source Firebase alternative with a Postgres backend and REST/GraphQL API. Supabase handles auth, real-time subscriptions, and row-level security, so the AI agents have a consistent, structured store to read/write.

**Input layer (Telegram bot + Whisper)** [^src5]: a Telegram bot acts as the single input channel — text or voice messages. Voice goes through Whisper (OpenAI speech-to-text) for transcription. The bot routes the transcribed message to the right agent module:
- Finance tracking (categorizes and logs expenses).
- Habit tracking (logs completions, computes streaks).
- Journal (records entries with tags and mood).
- CRM (logs contact interactions, follow-up reminders).

The result: everything happens through one messaging interface. No app-switching; no manual category selection; the AI infers intent from context [^src5].

---

[^src1]: [Reclaim 6 Hours of your Week in 10 mins](../../raw/email/email-2026-05-25-reclaim-6-hours-of-your-week-in-10-mins.md)
[^src2]: [You're just a text file.](../../raw/email/email-2026-05-03-you-re-just-a-text-file.md)
[^src3]: [Loop Engineering](../../raw/email/email-2026-06-08-loop-engineering.md)
[^src4]: [JFDI System — My AI Executive Assistant (Full Life Command Center)](../../raw/youtube/youtube-yjO9UHIunSE-jfdi-system-my-ai-executive-assistant-full-life-command-cent.md)
[^src5]: [How I Turned Claude into My Personal Assistant — Full Guide](../../raw/youtube/youtube-CvLkhGWZlvE-how-i-turned-claude-into-my-personal-assistant-full-guide.md)
[^src6]: [It's Cognitive Uploading — How Google NotebookLM's Steven Johnson Uses AI](../../raw/youtube/youtube-1dYp9ymqy_g-it-s-cognitive-uploading-how-google-notebooklm-s-steven-john.md) — Dan Blumberg interview with Steven Johnson
[^src7]: [The Definitive Guide to Setting Up Your AI Second Brain](../../raw/youtube/youtube-47oi3Q9apK0-the-definitive-guide-to-setting-up-your-ai-second-brain.md) — Vicky Zhao (BASB / three-brain model / Zettelkasten)
[^src8]: [Build This Once. Any AI You Use Will Get Smarter Forever](../../raw/youtube/youtube-5H-s-TIO0QE-build-this-once-any-ai-you-use-will-get-smarter-forever.md) — Rick Mulready (information hierarchy)
[^src9]: [How to Build the Ultimate AI Second Brain (Obsidian + Claude Code)](../../raw/youtube/youtube-4l8MXYUqGaA-how-to-build-the-ultimate-ai-second-brain-obsidian-claude-co.md) — KJ Rainey (two-layer brain)
[^src10]: [Pro AI Dictation Tips for SuperWhisper — Mastering Context Awareness](../../raw/youtube/youtube-py3szwKAZYU-pro-ai-dictation-tips-for-superwhisper-mastering-context-awa.md) — A Fading Thought
