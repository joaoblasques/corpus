---
channel: email
source: gmail
gmail_message_id: 19eb6c62cc211ec1
from: The Code <superhumancode@news.codenewsletter.ai>
subject: 👀 Devs love and hate Fable 5
date_received: 2026-06-11
pointer: false
collected_at: 2026-06-11
links:
  - {url: https://huggingface.co/google/diffusiongemma-26B-A4B-it, fetched: true, score: 8, file: raw/web/google-diffusiongemma-26b-a4b-it-hugging-face.md}
  - {url: https://github.com/Q00/ouroboros, fetched: true, score: 8, file: raw/web/github-q00-ouroboros-agent-os-stop-prompting-start-specifyin.md}
  - {url: https://arxiv.org/abs/2605.30621, fetched: true, score: 8, file: raw/web/harness-updating-is-not-harness-benefit-disentangling-evolut.md}
  - {url: https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/, fetched: false, score: 7, reason: over-cap}
  - {url: https://developers.openai.com/codex/cli/features#:~:text=Review%20uncommitted%20changes, fetched: false, score: 7, reason: over-cap}
  - {url: https://surrealdb.com/, fetched: false, score: 7, reason: over-cap}
  - {url: https://cursor.com/insights, fetched: false, score: 6, reason: over-cap}
  - {url: https://newsletter.pragmaticengineer.com/p/ideas-slow-down-to-speed-up-when, fetched: false, score: 6, reason: over-cap}
  - {url: https://silviasapora.github.io/blog/ml-interviews.html, fetched: false, score: 6, reason: over-cap}
  - {url: https://hackbook-chi.vercel.app/, fetched: false, score: 6, reason: over-cap}
  - {url: https://dora.dev/dora-report-2025/, fetched: false, score: 5, reason: over-cap}
  - {url: https://codenewsletter.ai/p/google-drops-diffusiongemma-supermemory-now-runs-locally, fetched: false, score: 3, reason: low-utility}
  - {url: https://tweethunter.io/?utm_medium=email&utm_source=newsletter&utm_campaign=nl_thecode_0426_040326, fetched: false, score: 2, reason: low-utility}
  - {url: https://www.youtube.com/watch?v=hfba9dAT6xE, fetched: false, score: 0, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/ai-engineering/anthropic.md
---

View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/4465669c-c6c8-4a48-af73-16fa2a571a33/Group_Tweethunter.jpg?t=1781131537)
Follow image link: (https://tweethunter.io/?utm_medium=email&utm_source=newsletter&utm_campaign=nl_thecode_0426_040326)
Caption: 

----------
**Welcome back.** Anthropic's Fable 5 launch is causing a ton of controversy. The company reportedly apologized for secretly rerouting some requests to an older model, admitting it made the "wrong trade-off."

Meanwhile, developers are shipping all kinds of wild projects. One dev used Fable to [reverse-engineer](https://x.com/the2ndfloorguy/status/2064704204166635930) his Whoop heart rate data to figure out which coworker was stressing him out the most.

**Also:** Watch how Claude Fable 5 edited its launch video entirely through code, an ML researcher's playbook for landing frontier lab offers, and a new market for devs to build on.


--------------------
### **Today’s Insights**

* Powerful new updates and hacks for devs

* Why is company speed lagging despite AI coding gains

* How to catch bugs before you commit

* Trending social posts, top repos, and more


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **TODAY IN PROGRAMMING**




--------------------
View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/f76507cd-b67e-4617-95fa-18889bbd4384/Thumbnail__4_.jpg?t=1781158160)
Follow image link: (https://x.com/googlegemma/status/2064741002204545467)
Caption: Click here to see how Google's DiffusionGemma works.


--------------------
**Google unveils an experimental model that generates text 4x faster:** The search giant just dropped [**DiffusionGemma**](https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/), an experimental open model that drafts 256 tokens at once instead of generating word by word. Google says it hits 1,000+ tokens per second on a single H100. The speed comes with a trade-off. Output quality trails standard Gemma 4, so it's best for local work like code infilling and in-line edits. [**Download the weights.**](https://huggingface.co/google/diffusiongemma-26B-A4B-it)

**Supermemory ships a local-first memory engine:** The AI memory startup just announced [**Supermemory Local**](https://x.com/DhravyaShah/status/2064749237498519923), a self-contained build that packs its graph engine and embedding model into a single download. It works with Claude, OpenClaw, Hermes, and other agents on any machine. SDKs make it easy to give an agent long-term memory or set up a company brain. Plus, if you pair it with a local model, nothing ever leaves your machine.

**Anthropic brings Claude to Apple's AI framework:** The AI lab just rolled out a [**Swift package**](https://x.com/ClaudeDevs/status/2064756984617021807) that integrates Claude into Apple's Foundation Models framework as a server-side model. Developers can use it with the same API as Apple's on-device model, so streaming, tool calling, and structured output all work the same way. Requests go straight to the Claude API and never touch Apple's servers. It's in beta alongside the OS 27 releases. 


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **PRESENTED BY TWEETHUNTER**

## [The founders winning on X aren’t smarter. They’re just consistent.](https://tweethunter.io/?utm_medium=email&utm_source=newsletter&utm_campaign=nl_thecode_0426_040326)


--------------------
View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/dbf65d53-77e9-44ab-9204-1f255a7af378/tweethunter.jpg?t=1781131785)
Follow image link: (https://tweethunter.io/?utm_medium=email&utm_source=newsletter&utm_campaign=nl_thecode_0426_040326)
Caption: 


--------------------
[**Tweet Hunter**](https://tweethunter.io/?utm_medium=email&utm_source=newsletter&utm_campaign=nl_thecode_0426_040326) helps 5,600+ founders stay consistent on X.

In one session, you get:

* A full week of content queued

* Automations running in the background

* Stay visible without being online all day

All built on the official X API, so your account stays safe.

[**Start your free trial for 7 days**](https://tweethunter.io/?utm_medium=email&utm_source=newsletter&utm_campaign=nl_thecode_0426_040326)


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **INSIGHT**

## **Devs doubled their code output but their companies didn't get faster**


--------------------
View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/da7419bd-5e04-49b0-94d6-5012b026e7ba/superhumanteam_a_software_engineering_team_working_on_a_huge__f6ac6ca2-2c9e-4007-9da8-2c8cad57327e_3.jpg?t=1781168182)
Caption: Source: The Code, Superhuman


--------------------
**The flood of code is here.** Engineers are writing twice as much code as they did just six months ago. Cursor says PR sizes [tripled](https://cursor.com/insights) since January for top users, and Jellyfish found heavy AI adopters push twice as many PRs, with 72% of their code AI-assisted. Pragmatic Engineer's Gergely Orosz then [points out](https://newsletter.pragmaticengineer.com/p/ideas-slow-down-to-speed-up-when) in his breakdown that AI coding reached every industry, including automotive, in under a year.

**Technical debt is piling up.** Reviewers can't keep up, so most hit "LGTM" (looks good to me) without reading, while the few who still review are burning out. OpenCode's Dax Raad says AI mutes the guilt of shipping a hack, so the instinct to clean up debt never fires. The fallout: Amazon mandated senior sign-offs after AI-assisted changes caused outages, Windows 11 updates bricked devices, and third-party trackers put GitHub's uptime below one nine as agent traffic overwhelmed its infrastructure.

**The fix is boring.** The 2025 DORA report [found](https://dora.dev/dora-report-2025/) AI amplifies whatever system you already have: some companies doubled their incidents, others cut them in half. The winners run the old playbook:

* OpenCode CEO brought back heavy domain-driven design because agents need guardrails.

* ==Veteran engineer ==Kent Beck uses tests to stop agents from shipping regressions.

* Amazon put a human checkpoint before production.

**Few are buying it.** HashiCorp co-founder Mitchell Hashimoto says entire companies now ship bugs, betting agents will fix them before users notice. Meta reportedly gutted Instagram's Trust and Safety team days before hackers hijacked accounts through its own AI assistant. Kent Beck saw this with GUIs in the late 80s: everyone who could build one did, and the worst software came first. The teams fixing their quality checks now will make it out first. Read Pragmatic Engineer's full piece [here](https://newsletter.pragmaticengineer.com/p/ideas-slow-down-to-speed-up-when).


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **IN THE KNOW**

## **What’s trending on socials and headlines**


--------------------
View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/60e792b4-57eb-474d-997e-51bb2341088c/CleanShot_2026-06-11_at_11.31.29_2x.jpg?t=1781157748)
Caption: Meme of the day.


--------------------
* **Senior Brain:** This [**6-step setup**](https://x.com/mattpocockuk/status/2064663221718425660) trains you to think like a senior programmer, with a coding agent acting as your teacher (5.1K bookmarks).

* **No Editor Needed:** An Anthropic engineer shared how Claude Fable edited its [**launch video**](https://x.com/trq212/status/2064826394589442448) entirely through code. He didn't open a video editor once (520K views).

* **Smart Split:** Shadcn, creator of the shadcn/ui library, dropped a skill that puts Claude Fable on auditing your [**codebase**](https://x.com/shadcn/status/2064671802509410806) and writing plans, then hands execution to cheaper models (7K bookmarks).

* **Star Trek Logic:** Cohere's co-founder used a Star Trek analogy to [**explain**](https://x.com/MTSlive/status/2064768885166121277) why better LLMs aren't getting us closer to AGI.

* **Blue Bubble AI:** An a16z partner mapped every AI assistant you can text on iMessage like a contact. Apple just approved its first agent, and that opens a [**new market**](https://x.com/venturetwins/status/2064740052668944453) for devs to build on.

* **Loop Logic:** This skill rewrites and [scores your plans](https://x.com/seangeng/status/2064513457584541849) on a loop until they can't get any better. Pairs well with Fable 5 (1.4K bookmarks).

* **Interview Playbook:** A researcher who landed offers from DeepMind, Meta, and Cohere wrote up everything she learned. **[Here's the guide](https://silviasapora.github.io/blog/ml-interviews.html)** (2.4K likes).


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **AI CODING HACK**


--------------------
## **How to catch bugs before you commit**

Agent sessions often leave you with a mess of uncommitted changes that nobody actually reviews before they're committed. Codex has a [built-in fix](https://developers.openai.com/codex/cli/features#:~:text=Review%20uncommitted%20changes) for this. OpenAI documented a standalone review command that scans everything in your repo (staged, unstaged, and untracked) and flags issues with specific file references. 

Just run this from your repo root:

```
codex review --uncommitted

# Or point the reviewer at what worries you
codex review --uncommitted "Focus on error handling and edge cases"
```
Every review shows up as a separate round. Just address the issues and keep rerunning the command until the diff is clean. Once it is, you're good to commit.

P.S. Get 50+ AI coding hacks for Claude Code, Cursor, and Codex [here](https://hackbook-chi.vercel.app/).


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **TOP & TRENDING RESOURCES**




--------------------
View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/2453d5f0-8ad7-4b13-9606-264e065fa8b2/Thumbnail__5_.jpg?t=1781158660)
Follow image link: (https://www.youtube.com/watch?v=hfba9dAT6xE)
Caption: Click here to watch the tutorial.


--------------------
### **Top Tutorial**

[**How to build the best local agentic coding workflow:**](https://www.youtube.com/watch?v=hfba9dAT6xE) You’ll learn how to set up a local AI coding assistant using LM Studio and VS Code. The tutorial dives deep on how to select the best open-source models for your hardware, configure chat-driven code generation, and enable offline autocomplete entirely on your own machine.

———————————————————————————

### **Top Tool**

[SurrealDB:](https://surrealdb.com/) A multi-model database that makes building modern apps easy. It combines relational, document, and graph databases into one platform. You can build real-time apps and handle complex data without needing multiple systems.

———————————————————————————

### **Top Repo**

[**Ouroboros**](https://github.com/Q00/ouroboros)** (4.5K ⭐):** An agent OS for AI coding. It turns unpredictable tasks into reliable workflows using structured contracts. Instead of messy prompting, it follows a clear process to interview, build, and evolve your code.

———————————————————————————

### **Trending Paper**

[**Disentangling agent self-evolution:**](https://arxiv.org/abs/2605.30621) This paper looks at whether an AI's skill level affects how well it can improve itself using tools and prompts. It shows that while most models can create good updates, weaker ones struggle to actually use them correctly.


----------View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/18efc0eb-c3c4-483f-a001-0fe0dcca16c3/Group_from_Figma__2_.png?t=1758120539)
Caption: 

----------
##### **IN CASE YOU MISSED IT**


--------------------
### ==**Our most-clicked story from yesterday**==

Check out how Claude Fable 5 [changed](https://x.com/ClaudeDevs/status/2064399512664526853) the Claude Code team's workflow. They've shared three big shifts they've seen firsthand.


--------------------
==**Grow customers & revenue:**== Join companies like Google, IBM, and Datadog. Showcase your product to our 300K+ engineers and 150K+ followers on socials. [Get in touch.](https://www.passionfroot.me/the-code)

———————————————————————————

You can also reply directly to this email if you have suggestions, feedback, or questions.

Until next time — The Code team


----------
———

You are reading a plain text version of this post. For the best experience, copy and paste this link in your browser to view the post online:
https://codenewsletter.ai/p/google-drops-diffusiongemma-supermemory-now-runs-locally
