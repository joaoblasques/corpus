---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/email/email-2025-06-01-15-productivity-hacks-every-engineer-manager-should-know.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/youtube/youtube-BYjIIRpos0I-your-mac-can-work-like-a-personal-assistant-most-people-neve.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - time management
  - focus management
  - deep work
  - time blocking
  - productivity hacks
  - maker vs manager time
  - Mac personal assistant
  - Shortcuts app
  - Focus modes
tags:
  - corpus/productivity
  - concept
created: 2026-06-19
updated: 2026-06-25
---

# Time & Focus Management

**TL;DR** — Being busy is not the same as being productive [^src1]. The leverage in knowledge work comes from protecting uninterrupted focus and spending it on high-impact work, not from doing more tasks. The practices below — drawn from a 15-tip guide for engineers and managers — cluster into four moves: **plan in systems**, **protect focus** (time blocking, killing context-switches and notifications), **start and break down** the hard work, and **sustain the body** that does it.

## Plan in systems, not just to-do lists

Without structured planning you drown in reactive tasks; planning across horizons shows what matters now vs. next [^src1]:

- **Daily** — list the top 3 tasks; set clear intentions for focused work.
- **Weekly** — key deliverables, team syncs, buffer time for problem-solving.
- **Monthly / quarterly** — review milestones, tech debt, growth areas.

> "You do not rise to the level of your goals. You fall to the level of your systems." — James Clear [^src1]

This systems-over-goals framing connects to the broader [Mental Models](/productivity/mental-models.md) toolkit.

## Protect focus

The single most-repeated idea: deep, uninterrupted focus is where real progress happens, and almost everything else in the list exists to defend it [^src1].

- **Time blocking** — own your calendar or someone else will. Create themed blocks (deep work, meetings, admin, learning, breaks) and treat them as seriously as client meetings; reschedule rather than delete. Color-code to see balance at a glance [^src1].
- **Minimize context-switching** — it takes over 20 minutes to get back on track after an interruption; a few of those a day and your best hours are gone. Batch similar tasks, theme whole days ("focus day" / "meeting day"), and take 3–5 minutes to mentally reset when changing task types [^src1].
- **Avoid multitasking; practice monotasking** — the brain doesn't multitask, it toggles attention and loses depth each time. Work one task fully; use a task queue (Todoist, Trello, a checklist) and a Pomodoro-style timer (25–45 min) [^src1].
- **Limit notifications** — each ping breaks focus. Silence non-urgent visual/sound alerts, use Do-Not-Disturb / Focus modes, and check email and messages at set times (e.g. 11:30 and 15:30) rather than reacting instantly [^src1].
- **Separate maker time from manager time** — engineers ("makers") need long uninterrupted blocks; managers switch between planning/reviewing/communicating. When the two collide, productivity suffers. Reserve mornings for deep work and afternoons for meetings/admin; managers should still protect 2–3 hours of maker time a few times a week [^src1]. This echoes Paul Graham's maker-vs-manager schedule distinction.
- **Deep-work sessions** — block 60–90 minutes for one high-value task (the sweet spot before fatigue), in a quiet space with notifications off and the task pre-planned so no mental energy goes to deciding [^src1].

## Set priorities and act on the high-impact work

- **Don't confuse activity with progress** — prioritizing poorly makes you efficient at unimportant things. Use the **Eisenhower Matrix** (urgent vs. important) or the **ABC method**; start each day by identifying 1–3 high-impact tasks and protecting time for them. Teach the team to prioritize so they decide autonomously [^src1].
- **Focus on high-impact work** — value is in solving the *right* problems, not doing more. Prioritize outcomes over output, automate repetitive tasks, improve the process rather than just following it [^src1].

## Start, and break it down

- **Stop procrastinating; start before you feel ready** — procrastination is a silent performance killer that can stall whole teams. Start ugly (rough draft / skeleton / mind map), use the **5-minute rule** (commit to just 5 minutes and momentum usually carries you), and be honest about whether you're "too busy" or avoiding discomfort [^src1].
- **Two-minute rule** — from David Allen's *Getting Things Done*: if a task takes under 2 minutes, do it immediately so micro-tasks don't pile into a draining mental backlog [^src1].
- **Break big tasks into smaller ones** — big tasks feel overwhelming because they're *vague*; ambiguity causes procrastination. Zoom in until each step feels actionable: "if you're stuck, the task is probably too big" [^src1].

## Sustain the body that does the work

- **Take regular breaks** — breaks aren't a luxury; skipping them leads to decision fatigue and burnout. Plan recovery blocks: a screen-free lunch, walking breaks, creative breaks, short social breaks, active stretching [^src1].
- **Alternate sitting and standing** — physical stagnation leads to mental stagnation; try ~45–60 min sitting then 15–20 min standing, using standing time for lower-focus tasks like reading docs or replying to messages [^src1].
- **Improve typing speed** — a core, underrated skill for tech professionals; learn touch typing and prioritize accuracy before speed, since typing friction compounds across everything you do [^src1].

## Mac as a personal assistant

macOS includes underutilized automation layers that address time and attention management natively — without additional software [^src2].

**Shortcuts app (automation triggers)** [^src2]:
- Build "morning routine" and "evening routine" Shortcuts that chain actions: open specific apps (or close them), play music, check weather, set reminder → triggered by a tap on the Home Screen or a scheduled time.
- Shortcuts can run based on triggers: time of day, geofence arrival/departure, or automation from a widget. This means context-switch preparation (notifications off, apps open) can happen without manual intervention.
- "Most people have no idea that the Shortcuts app on their Mac can automate their entire morning before they even sit down" [^src2].

**Focus modes** [^src2]:
- macOS Focus modes (`System Settings → Focus`) define which apps, people, and notification sources can interrupt you. Work Focus: only Slack from direct reports, no social media. Deep Work Focus: nothing. Personal Focus: apps for family but not work.
- Schedules: Focus modes can auto-activate by time, location, or app launch (e.g., when you open Xcode, automatically enable Deep Work mode).
- Home Screen customisation per Focus mode: reduce friction by surfacing only task-relevant apps and hiding everything else during deep work blocks [^src2].

**Text replacement (typed abbreviations)** [^src2]:
- System Settings → Keyboard → Text Replacements: define shorthand for frequently typed content (email signature, boilerplate text, address, repeated code snippets). Reduces repetitive typing compound across the day.
- Works system-wide; more reliable than clipboard managers for static expansions.

**Dictation + Apple Intelligence** [^src2]:
- macOS native dictation (microphone icon in system tray or function key) transcribes continuously without a third-party app.
- Apple Intelligence (macOS 15+) extends this with writing tools integrated into every text field — rewrite, proofread, summarize — via right-click or keyboard shortcut.
- The Crazy Errors presenter's workflow: dictate rough text → Apple Intelligence rewrites/cleans → paste into destination. Replaces drafting time with directed editing [^src2].

**Mail rules** [^src2]:
- Mail.app rules (`Mail → Settings → Rules`) auto-file, auto-tag, or auto-forward email by sender, subject, or list header. Practical patterns: newsletters auto-moved to "Read Later" folder; GitHub notifications auto-archived; direct manager emails flagged.
- Prevents inbox as interrupt queue. Combine with designated "email time" blocks (not continuous monitoring) from the engineering guide above [^src1].

**Complementarity with AI dictation (SuperWhisper)**: the native dictation + Apple Intelligence setup handles light transcription and rewriting; SuperWhisper (see [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) §10) handles heavier AI-processing modes with full context awareness. They coexist on the same machine with different use cases [^src2].

## Context

This is the productivity domain's time-and-focus reference; it complements [Shipping and Scope](/productivity/shipping-and-scope.md) (deciding when work is *done*), [Working with Stakeholders](/productivity/working-with-stakeholders.md) (protecting time against external demands), and [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) (offloading low-value work). The source is a guest-authored guide (Aleš Žehelj, via Gregor Ojstersek's Engineering Leadership newsletter) aimed at both engineers and managers.

[^src1]: [15 Productivity Hacks Every Engineer & Manager Should Know (Engineering Leadership)](../../raw/email/email-2025-06-01-15-productivity-hacks-every-engineer-manager-should-know.md)
[^src2]: [Your Mac Can Work Like a Personal Assistant](../../raw/youtube/youtube-BYjIIRpos0I-your-mac-can-work-like-a-personal-assistant-most-people-neve.md) — Crazy Errors
