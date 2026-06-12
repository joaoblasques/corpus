---
channel: email
source: gmail
gmail_message_id: 19dde43344b89d85
from: Jeff Su <hello@jeffsu.org>
subject: "👋 Day 1: Welcome to the Cowork Toolkit, let’s dive in!"
date_received: 2026-04-30
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://drive.google.com/drive/folders/1mKMGnqp12hH8Q3V4gp9i1yzaQaI8CcgQ?usp=sharing", fetched: true, score: 8, file: raw/web/shared-cowork-toolkit-templates-d1.md}
  - {url: "https://44766ebe.click.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve/dphehmuen0mrv4bl/aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2RyaXZlL2ZvbGRlcnMvMW1LTUducXAxMmhIOFEzVjRncDlpMXl6YVFhSThDY2dRP3VzcD1zaGFyaW5n", fetched: false, score: 0, reason: low-utility}
  - {url: "https://44766ebe.click.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve/e0hph0u7o0256lh7/aHR0cHM6Ly9qZWZmc3UudHlwZWZvcm0uY29tL3RvL1BHZGtDdjE3I2VtYWlsPUpvYW8=", fetched: false, score: 0, reason: low-utility}
  - {url: "https://preferences.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve", fetched: false, score: 0, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/ai-engineering/claude-cowork.md
---

Hi Joao,

Welcome to my Cowork Toolkit! Over the next few days, you'll
build a Cowork workspace that's tailored to you: it'll remember
how you work, write in your voice, and handle real tasks without
you having to re-explain context every session.

Each email is short and actionable, but I go deeper on the
nuances I can't cover in a 15-minute video. So even if you've
watched everything on my channel, you'll get new material.

Let's get started! 😁

------------------------
Chat vs. Cowork vs. Code
------------------------

At the risk of massively oversimplifying, there are three ways to
use Claude:

* Claude Chat: Similar to Gemini and ChatGPT: you ask, it
answers. But it won't proactively verify its own work, read files
on your computer, or take actions you didn't explicitly request.
* Claude Code: This is for developers. Skip this if you (like me)
don’t have a coding background.
* Claude Cowork: This is the non-developer version of Claude
Code. Although it’s technically less capable, this is actually a
feature and NOT a bug. Anthropic puts all new capabilities into
Code first, and the best ones trickle down into Cowork over time.

If you signed up for this toolkit, Cowork is the right tool for
you. Everything I teach from here on applies to Cowork.

----------------------------
Where Your Instructions Live
----------------------------

Claude has three layers of customization, from broadest to most
specific:

Personal preferences apply to Chat, Cowork, and Code. Your name,
tone preferences, basic settings. Think of it as "how Claude
talks to you everywhere.

​
Cowork-specific instructions only apply inside Cowork. Still just
a settings field.

​
CLAUDE.md and MEMORY.md files live in your Cowork workspace
folder, and this is where the real power is.

​
The first two are settings you can fill out in 5 minutes. The
third layer is what this entire Toolkit is about, because this is
where Cowork goes from "slightly better chatbot" to "assistant
that actually knows you."

-------------------------------------
CLAUDE.md: Your Standing Instructions
-------------------------------------

Two things to know about this weirdly-named file:

* There MUST be a CLAUDE.md file in your root Cowork folder,
named EXACTLY CLAUDE.md (case-sensitive), or Cowork won't
recognize it. Not "claude.md," not "Claude.md," not
"instructions.md."
* It's a plain-text markdown file. Just text with some headers
and bullet points, that's it.

​
Think of it as the brief you'd hand a new assistant on their
first day. "Here's how I like things done, here's what I care
about, here are the rules." Cowork reads this file at the start
of every session, so anything you put in here becomes persistent
behavior.

You only want to add rules and instructions to your CLAUDE.md
files. Things like:

* "Always do X."
* "Never do Y.
* "When I ask about Z, do it this way."

Specifically, your first few rules within CLAUDE.md might look
something like this:

* Never update my files without asking me first
* If new information conflicts with something you already know,
flag it before overwriting
* Before writing any content, read voice-principles.md

In plain English:CLAUDE.md tells Cowork what to DO.

-----------------------------------
MEMORY.md: Your Accumulated Context
-----------------------------------

MEMORY.md is similar to CLAUDE.md in that it’s also a plain-text
markdown file, but it serves a completely different purpose.

MEMORY.md stores what Cowork has learned about you over time:
your active projects, key decisions, important contacts,
preferences, things you've told it to remember.

* CLAUDE.md might say “always add an end date to projects”
* MEMORY.md would say “Phase 2 for website revamp project just
started, expected completion in November”

​
The key difference:

* CLAUDE.md is prescriptive (what to do). MEMORY.md is
descriptive (what to know).
* Rules go in CLAUDE.md. Facts go in MEMORY.md.

Every session, Cowork can learn something new about you and add
it to MEMORY.md. Over time, this is what makes a 3-month-old
workspace feel fundamentally different from a 3-day-old one.
(More on this in a few days.)

In plain English:MEMORY.md tells Cowork what to KNOW.

----------------------
Your Starter Templates
----------------------

Because I’m an angel (😇), I've put together pre-filled versions
of both CLAUDE.md and MEMORY.md files based on my actual
workspace (simplified, no sensitive info) so they work the moment
you drop them in.

Step 1: Create a new folder in your documents folder called
"Cowork OS" (or whatever you'd like, this name doesn’t matter).

​
Step 2: Download the templates:

-->Download CLAUDE.md and MEMORY.md (
https://44766ebe.click.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve/dphehmuen0mrv4bl/aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2RyaXZlL2ZvbGRlcnMvMW1LTUducXAxMmhIOFEzVjRncDlpMXl6YVFhSThDY2dRP3VzcD1zaGFyaW5n
)
Download CLAUDE.md and MEMORY.md (
https://drive.google.com/drive/folders/1mKMGnqp12hH8Q3V4gp9i1yzaQaI8CcgQ?usp=sharing
)(make sure you download them as .md files, NOT .docx)

Step 3: Move both files into your Cowork OS folder.

Step 4: Open Cowork and select that folder as your workspace
folder.

That's it. Cowork will now read your CLAUDE.md at the start of
every session. No edits needed; the templates work out of the
box.

​
What's inside the CLAUDE.md template:

* A memory system so Cowork knows how to update MEMORY.md from
day one
* Preferences that work for most professionals (tone, length,
formatting defaults)
* Practical rules like "ask clarifying questions before starting
a complex task"
* A routing map and workstation template you'll use starting in
Day 3

What's inside the MEMORY.md template:

* An active projects tracker (pre-filled with your Toolkit
progress)
* Three starter memories showing the format (swap these with your
own over time)

You'll customize both files naturally over the next few days. For
now, just drop them in and move on.

--------------
Progress Check
--------------

Celebrating the small things can lead to significant strides over
time, so click here (
https://44766ebe.click.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve/e0hph0u7o0256lh7/aHR0cHM6Ly9qZWZmc3UudHlwZWZvcm0uY29tL3RvL1BHZGtDdjE3I2VtYWlsPUpvYW8=
) to mark your progress!

---------------
Before Tomorrow
---------------

One quick setup for Day 2: create a folder called 00_Resources
inside your workspace folder, so your root folder looks something
like this:

​
Right now your CLAUDE.md has everything in one file: your rules,
preferences, context. Tomorrow, you'll teach Cowork your actual
writing voice, and in the process, learn a technique that keeps
your CLAUDE.md clean and modular as it grows.

Talk soon,
Jeff

​Unsubscribe from Jeff's Cowork Toolkit (
https://44766ebe.click.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve/7qhdgkpgu2u95oml65t9/aHR0cHM6Ly9jb3dvcmthY2FkZW15LmFpL3Rvb2xraXQvdW5zdWJzY3JpYmU=
) | Unsubscribe from everything (including workshops) (
https://44766ebe.unsubscribe.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve
)​

​Update my profile (
https://preferences.kit-mail3.com/v8uqr3w8dvsmuxdko7xaghvk3gvnph9h224ve
)​

Sushie Labs, 29 Austin Road, Tsim Sha Tsui, Kowloon, Hong Kong,
Hong Kong 00000
