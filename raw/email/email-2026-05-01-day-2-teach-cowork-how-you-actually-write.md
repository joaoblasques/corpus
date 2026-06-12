---
channel: email
source: gmail
gmail_message_id: 19de3b8df052e9e7
from: Jeff Su <hello@jeffsu.org>
subject: "✍️ Day 2: Teach Cowork how you actually write"
date_received: 2026-05-01
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://drive.google.com/drive/folders/13VFIng3P98c5Qy5ueGngH194wrRQekQ-?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto", fetched: true, score: 6, file: raw/web/shared-cowork-toolkit-templates-d2.md}
  - {url: "https://44766ebe.click.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23/58hvh8ug2gn53os7/aHR0cHM6Ly9qZWZmc3UudHlwZWZvcm0uY29tL3RvL09yT3F0RjlnI2VtYWlsPXRpbGFrYXBhc2hAZ21haWwuY29t", fetched: false, score: 1, reason: low-utility}
  - {url: "https://44766ebe.click.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23/kkhmh2unvn58zeik/aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2RyaXZlL2ZvbGRlcnMvMTNWRkluZzNQOThjNVF5NXVlR25nSDE5NHdyUlFla1EtP2Rtcj0xJmVjPXdnYy1kcml2ZS0lNUJtb2R1bGUlNUQtZ290bw==", fetched: false, score: 0, reason: low-utility}
  - {url: "https://preferences.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23", fetched: false, score: 0, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/ai-engineering/claude-cowork.md
---

Hi Joao,

Yesterday we gave your Cowork a brain (it knows who you are and
what you do). Today let’s teach Cowork your voice (so it doesn’t
sound like…AI).

And you'll also learn a technique that keeps your CLAUDE.md clean
and modular as it grows.

--------------------------
Your Voice Principles File
--------------------------

Put simply, you need to create a dedicated file that captures
your writing patterns: sentence length, tone, word choice,
formatting habits, phrases you use and phrases you avoid.

We do this in two steps:

* Tell Cowork to create a file called voice-principles.md in your
00_Resources folder.
* Tell Cowork to add a line to your CLAUDE.md that says: "Before
producing any written content, read voice-principles.md in the
Resources folder."

That's it! Cowork now checks your voice file before writing
anything.

-------------------------------------------
Your Starter Voice File + Extraction Prompt
-------------------------------------------

Like yesterday, I've put together a pre-filled
voice-principles.md based on the one I actually use (simplified,
no sensitive info) so it works the moment you drop it in.

What's inside:
--------------

* Tone: "Write like a clear, thoughtful colleague talking to a
smart friend." Professional but not stiff.
* Sentence style: Vary sentence length, cap paragraphs at 1-3
sentences, use connectors like "so," "because," "for example"
instead of stacking fragments.
* Words and phrases to avoid: The usual AI giveaways ("dive
into," "game-changing," "straightforward," "leverage") plus a
section to add your own.

-->Download Templates (
https://44766ebe.click.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23/kkhmh2unvn58zeik/aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2RyaXZlL2ZvbGRlcnMvMTNWRkluZzNQOThjNVF5NXVlR25nSDE5NHdyUlFla1EtP2Rtcj0xJmVjPXdnYy1kcml2ZS0lNUJtb2R1bGUlNUQtZ290bw==
)
Download Templates (
https://drive.google.com/drive/folders/13VFIng3P98c5Qy5ueGngH194wrRQekQ-?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto
)(make sure you download voice-principles as an .md file, NOT
.docx)

Drop voice-principles.md into your 00_Resources folder. Cowork
will read it before writing anything because your CLAUDE.md
already has the pointer.

​

Making it yours
---------------

The template works as-is, but it sounds generic until you
personalize it. So I've included a Voice Extraction Prompt (same
link as above) that has Cowork analyze YOUR actual writing and
update the file with YOUR patterns.

* If you've already connected Gmail to Cowork (from the video or
on your own): paste the extraction prompt and Cowork scans your
last 30 sent emails, pulls out your writing patterns, and updates
voice-principles.md automatically.
* If you haven't connected Gmail yet: paste 5 emails or documents
you've written into Cowork, then paste the extraction prompt
below them. Cowork does the same analysis on whatever you give
it.

After running it, Cowork shows you exactly what changed. Review
the updates, correct anything that feels off, and save. The whole
thing takes about five minutes (most of that is picking which
emails to paste, if you're going the manual route).

The one thing to do right now: run the extraction prompt with
your own writing. Everything else in the template works as-is.
You'll customize it naturally over time.

----------------------------------------
The Pattern Behind This: Reference Files
----------------------------------------

What you just did, creating a separate file and pointing
CLAUDE.md to it, is a pattern you'll use a lot. It's called a
"reference file."

There are 3 reasons why we would create separate files INSTEAD of
putting everything in CLAUDE.md:

* Size: CLAUDE.md should stay under ~300 lines. Voice principles
alone could be 50+ lines. Multiply that by every domain you work
in and CLAUDE.md becomes unreadable.
* Modularity: Different parts of your workspace can load
different reference files. Your voice file gets loaded
everywhere. A specific framework or set of notes might only load
in one context.
* Maintainability: When you update your voice, you edit one file.
Everything that references it gets the update automatically.

Your 00_Resources folder is where reference files live. Right now
it has one file. By the end of this sequence, it'll have several.

Rule of thumb: if your CLAUDE.md is getting long, that's a signal
to pull content out into a reference file and replace it with a
pointer.

---------------------------------------
Three Ways You'll Refine This Over Time
---------------------------------------

The extraction prompt is the starting point, so here are three
scenarios where you'll naturally improve your voice principles
through normal use.

1. The punctuation tic
----------------------

You ask Cowork to draft a message to your manager. The draft
looks fine, but something feels off. Then you spot it: em dashes
everywhere. You never use em dashes. You use commas and periods.

Tell Cowork: "I don't use em dashes. Add that to my voice
principles file." Cowork opens voice-principles.md, adds the rule
to the Formatting Defaults section, and every future draft
follows it.

Why you'll hit this one: most people can't articulate their
punctuation preferences until they see the wrong one. Em dashes
are the single most common AI writing tic.

2. AI-giveaway phrases
----------------------

A week in, you ask Cowork to summarize a meeting. It opens with
"Let's dive into the key takeaways" and you’re like “Ew, I would
never say that.”

Tell Cowork: "Never use the phrase 'dive into.' Add it to my
avoid list." Cowork opens voice-principles.md, adds it to Words
and Phrases to Avoid, and that phrase rarely appears again.

Over the next month, you'll catch 3-4 more: "game-changing,"
"straightforward," "leverage." Each one is a 10-second
correction. The blacklist grows, and the AI-speak (slowly)
disappears.

Why you'll hit this one: every AI model defaults to the same
filler phrases. You'll recognize them the moment you see them in
your own draft.

3. The paragraph density preference
-----------------------------------

You ask Cowork to draft an email to a client. The content is
right, but it's a wall of text: one long 5-sentence paragraph
where you'd normally break it into two or three.

Tell Cowork: "I cap paragraphs at 2-3 sentences in emails. Update
my voice principles." Cowork adds the rule to the Sentence Style
section.

Why you'll hit this one: AI models default to dense paragraphs.
The mismatch is invisible until you compare a Cowork draft to
something you actually wrote.

Each correction takes 10 seconds. After a month, your voice file
will have a dozen rules you never wrote by hand, and Cowork's
first drafts will feel like yours.

--------------
Progress Check
--------------

Celebrating the small things can lead to significant strides over
time, so click here (
https://44766ebe.click.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23/58hvh8ug2gn53os7/aHR0cHM6Ly9qZWZmc3UudHlwZWZvcm0uY29tL3RvL09yT3F0RjlnI2VtYWlsPXRpbGFrYXBhc2hAZ21haWwuY29t
) to mark your progress!

---------------
Before Tomorrow
---------------

You now have both CLAUDE.md and MEMORY.md files, a resources
folder, and a voice profile. That's already more persistence than
most Cowork users.

But everything still lives in one flat folder, and Cowork can
only read files.

Tomorrow, I'll show you "workstations": domain-specific folders
that give Cowork specialized modes for different areas of your
work.

See you tomorrow,
Jeff

​Unsubscribe from Jeff's Cowork Toolkit (
https://44766ebe.click.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23/m2h04z24a6u3z3qo27il/aHR0cHM6Ly9jb3dvcmthY2FkZW15LmFpL3Rvb2xraXQvdW5zdWJzY3JpYmU=
) | Unsubscribe from everything (including workshops) (
https://44766ebe.unsubscribe.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23
)​

​Update my profile (
https://preferences.kit-mail3.com/0vuekw7ld6sguok2rk4alhv7z95llcnhddg23
)​

Sushie Labs, 29 Austin Road, Tsim Sha Tsui, Kowloon, Hong Kong,
Hong Kong 00000
