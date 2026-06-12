---
channel: email
source: gmail
gmail_message_id: 19de8de645abb1c9
from: Jeff Su <hello@jeffsu.org>
subject: "📬 Day 3: Build your first Cowork workstation"
date_received: 2026-05-02
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/6qhehouleled04u9/aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2RyaXZlL2ZvbGRlcnMvMVJld3E0UEs1c096clUyanRlaXViV09oS1F0Y2kwdTN6P3VzcD1kcml2ZV9saW5r", fetched: false, score: 0, reason: low-utility}
  - {url: "https://drive.google.com/drive/folders/1Rewq4PK5sOzrU2jteiubWOhKQtci0u3z?usp=drive_link", fetched: false, score: 0, reason: low-utility}
  - {url: "https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/kkhmh2unvnv347sk/bWFpbHRvOnNhcmFoQGNvbXBhbnkuY29t", fetched: false, score: 0, reason: low-utility}
  - {url: "https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/58hvh8ug2g2z3pc7/aHR0cDovL01FTU9SWS5tZA==", fetched: false, score: 0, reason: low-utility}
  - {url: "https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/25h2h9u3w3welva8/aHR0cDovL2plZmZzdS50eXBlZm9ybS5jb20vdG8vWm5aQ290Rm4jZW1haWw9dGlsYWthcGFzaEBnbWFpbC5jb20=", fetched: false, score: 0, reason: low-utility}
  - {url: "https://preferences.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z", fetched: false, score: 0, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/ai-engineering/claude-cowork.md
---

Hi Joao,

Yesterday you taught Cowork your voice. Today you connect it to
Gmail and build your first workstation.

By the end of this email: You'll have a personalized "Email HQ"
workstation with editorial rules from your own sent emails, a
contacts CRM built from the people you actually email, and Gmail
connected so Cowork can actually work with your inbox.

What Workstations Are
---------------------

Workstations are folders inside your workspace, one per “domain”
of work. Each gets its own CLAUDE.md with rules for that domain
and MEMORY.md with context for that domain.

"Root rules" cascade down automatically, so your voice principles
and preferences flow into every workstation without repeating
anything.

There are 2 types of workstations:

* Universal workstations: These handle work that cuts across
everything (e.g. email, brand identity).
* Dedicated workstations: These own one specific area (e.g.
personal finances, health).

Today we build a universal one. Tomorrow, a dedicated one.

Your root CLAUDE.md already has workstation-creation
instructions, so this is as simple as telling Cowork: "Create a
workstation called Email HQ for managing my email."

Connect Gmail
-------------

Before we build, let's give Cowork access to your email. Go to
Settings > Connectors and connect your Gmail account.

Cowork can now search your inbox, read threads, and understand
your email history. But don’t worry, even though the connector
can read your email. It doesn't send on your behalf. You always
review and hit send yourself.

This is the first time Cowork goes from reading files to working
with an external tool.

-------------------
The Populate Prompt
-------------------

Day 1 and Day 2 gave you pre-filled templates. Today's different
since Email HQ's value comes from being personalized to YOUR
email patterns. Instead of a generic template, you get a prompt
that creates the workstation AND fills it from your actual sent
emails.

-->Download the Email HQ Prompt (
https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/6qhehouleled04u9/aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2RyaXZlL2ZvbGRlcnMvMVJld3E0UEs1c096clUyanRlaXViV09oS1F0Y2kwdTN6P3VzcD1kcml2ZV9saW5r
)
Download the Email HQ Prompt (
https://drive.google.com/drive/folders/1Rewq4PK5sOzrU2jteiubWOhKQtci0u3z?usp=drive_link
)

What the prompt does:
---------------------

* Creates the Email HQ folder with CLAUDE.md, MEMORY.md, and an
Email HQ Resources subfolder, using the workstation-creation
instructions in your root CLAUDE.md.
* Scans your last 4 weeks of sent emails via the Gmail connector
you just set up.
* Extracts email-specific editorial rules: your default greeting,
sign-off, formality shifts by recipient type, and any conventions
not already in your voice principles file.
* Builds a contacts CRM of your 10 most frequent recipients, with
relationship context and tone notes for each.
* Adds a routing entry to your root CLAUDE.md so Cowork knows to
load Email HQ when you're working on email.
* Shows you everything before writing. You review and confirm
before Cowork saves anything.

Paste the prompt into Cowork and let it run. Takes about 2-3
minutes.

Reviewing What Cowork Extracted
-------------------------------

The prompt does a solid job, but the first pass almost always
needs corrections in two areas.

1. Editorial rules

Cowork might extract: "Uses bullet points in all emails."
Probably not quite right. You likely use bullets with your team
(because they skim) and full paragraphs with clients because
bullets feel too informal.

Tell Cowork to split the rule by recipient type and it’ll update
the Editorial Rules section with that distinction.

Why you'll hit this one: Cowork sees patterns in the aggregate,
but your email style shifts by audience. The first extraction
almost always flattens that nuance.

2. Contacts CRM

Each entry includes name, email, role/relationship, tone notes,
and common topics. The raw entries work, but they're usually too
vague:

❌ "Sarah (sarah@company.com (
https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/kkhmh2unvnv347sk/bWFpbHRvOnNhcmFoQGNvbXBhbnkuY29t
)) - Colleague. Professional tone."
✅ "Sarah Chen (sarah@company.com (
https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/kkhmh2unvnv347sk/bWFpbHRvOnNhcmFoQGNvbXBhbnkuY29t
)) - Project manager, Q3 website redesign. Direct and to the
point. Usually emails about timeline updates and vendor
approvals."

Spend 2 minutes reviewing the 10 entries. Each correction gets
saved to Email HQ's MEMORY.md (
https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/58hvh8ug2g2z3pc7/aHR0cDovL01FTU9SWS5tZA==
), so future drafts reference the right relationship context.

Why you'll hit this one: Cowork gets names and frequency right,
but it guesses at relationship context. You know things about
these people that don't show up in email headers.

​

Progress Check
--------------

Celebrating the small things can lead to significant strides over
time, so click here (
https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/25h2h9u3w3welva8/aHR0cDovL2plZmZzdS50eXBlZm9ybS5jb20vdG8vWm5aQ290Rm4jZW1haWw9dGlsYWthcGFzaEBnbWFpbC5jb20=
) to mark your progress!

Before Tomorrow
---------------

Email HQ is a universal workstation: it fires for all your email,
regardless of topic. But some domains need their own dedicated
space.

Tomorrow, you'll build a dedicated workstation for personal
finances, run a populate prompt that turns your credit card
statements into a categorized spending tracker, and add a routing
table so Cowork knows which workstation to load based on what
you're working on.

Talk soon,
Jeff

​Unsubscribe from Jeff's Cowork Toolkit (
https://44766ebe.click.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z/e0h6dkodi0u7o7o2mec7/aHR0cHM6Ly9jb3dvcmthY2FkZW15LmFpL3Rvb2xraXQvdW5zdWJzY3JpYmU=
) | Unsubscribe from everything (including workshops) (
https://44766ebe.unsubscribe.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z
)​

​Update my profile (
https://preferences.kit-mail3.com/5quz8vrl2kh8uvzg29ph6h9xl22dnsnhool6z
)​

Sushie Labs, 29 Austin Road, Tsim Sha Tsui, Kowloon, Hong Kong,
Hong Kong 00000
