---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-http-simonwillison-net-atom-everything-dcb07bd8.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-datasette-apps-host-custom-html-applications-inside-datasett-5f725425.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-sqlite-utils-4-0rc1-adds-migrations-and-nested-transactions-5199a144.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-porting-the-moebius-0-2b-image-inpainting-model-to-run-in-th-71cb4d77.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-temporary-cloudflare-accounts-for-ai-agents-9feea510.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-prompt-injection-as-role-confusion-f81ed04e.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-glm-5-2-is-probably-the-most-powerful-text-only-open-weights-42e4b84f.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-what-happened-after-2-000-people-tried-to-hack-my-ai-assista-20e22694.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-incident-report-cve-2026-lgtm-61a73fa6.md
    channel: web
    ingested_at: 2026-07-05
aliases:
  - Simon Willison
  - simonwillison.net
  - simonw
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-05
updated: 2026-07-05
---

# Simon Willison

**TL;DR**: Simon Willison is a British software developer and open-source author best known for creating [Datasette](/ai-engineering/datasette.md) and `sqlite-utils`, co-creating Django, and running a highly influential engineering blog at simonwillison.net [^src1]. His blog tracks practical AI engineering, tool releases, security research, and open-source development.

## Projects

- **[Datasette](/ai-engineering/datasette.md)** — tool for publishing and exploring SQLite databases as web apps; active development in 2026
- **sqlite-utils** — Python CLI/library for manipulating SQLite databases; 4.0 RC1 added migrations and nested transactions [^src3]
- **Datasette Lite** — Datasette running in the browser via Pyodide + WebAssembly
- **simonw/browser-compat-db** — MDN browser compatibility data converted to a ~66MB SQLite database, explorable via Datasette Lite [^src2]

## AI-assisted development practice

Willison is an active practitioner of AI-assisted programming and documents his workflow publicly:
- Uses Claude Code (Opus 4.8), GPT-5.5 xhigh (Codex Desktop), and Claude Fable 5 for security review as primary tools in 2026 [^src4]
- Ported the Moebius 0.2B image inpainting model from PyTorch/CUDA to run in-browser via ONNX + WebGPU using Claude Code [^src5]
- Characterizes AI coding as "vibe coding" and documents both its capabilities and failure modes

## Notable observations and curated commentary

Willison's blog functions as a highly-curated link blog on AI engineering. Notable curated observations from mid-2026 [^src1]:

**On prompt injection:** Research by Charles Ye, Jasmine Cui, and Dylan Hadfield-Menell showing LLMs weight *writing style* more heavily than role tag content — "destyling" an attack drops success from 61% to 10%; underlying mechanism is "role confusion" [^src6]. Willison endorses the paper and calls the blog-style writeup model best practice.

**On frontier model injection resistance:** Fernando Irarrázaval's public challenge (hackmyclaw.com) — 6,000 attempts, $500 token spend, no successful prompt injection against an Opus 4.6 instance with anti-injection rules. Willison's reading: "the effort the labs have been putting in to training their frontier models not to fall for injection attacks do appear effective in making these attacks much harder to pull off" — but 6,000 failed attempts provides no guarantees, and he does not recommend deploying systems where injection could cause irreversible damage [^src7].

**On AI agent cost runaway:** Andrew Nesbitt's satirical incident report CVE-2026-LGTM: two AI review agents in a disagreement loop, 340 comments, $41,255 inference spend before API keys are revoked [^src8]. Illustrates the real risk of unmonitored multi-agent workflows.

**On MCP auth:** Curated Sean Lynch HN comment: "The real valuable capability MCP offers over skills/CLI is isolating the auth flow outside of the agent's context window" — the idealized form of MCP may be "just an auth gateway for the API and nothing else" [^src9].

**On engineering discipline:** Charity Majors' observation that 2025 inverted code economics — "Lines of code went from being treasured… to being disposable and regenerable, practically overnight" — therefore AI demands *more* engineering discipline, not less [^src1].

## See also

- [Datasette](/ai-engineering/datasette.md) — primary project
- [Agent Security](/ai-engineering/agent-security.md) — prompt injection research curation; role confusion mechanism
- [MCP](/ai-engineering/mcp.md) — auth-gateway framing (Sean Lynch observation)
- [Vibe Coding](/ai-engineering/vibe-coding.md) — Willison documents AI-assisted development extensively

---

[^src1]: [Simon Willison's blog — Atom feed, June 2026](../../raw/web/web-http-simonwillison-net-atom-everything-dcb07bd8.md) — simonwillison.net
[^src2]: [simonw/browser-compat-db](../../raw/web/web-simonw-browser-compat-db-ff39842e.md)
[^src3]: [sqlite-utils 4.0rc1 adds migrations and nested transactions](../../raw/web/web-sqlite-utils-4-0rc1-adds-migrations-and-nested-transactions-5199a144.md)
[^src4]: [Datasette Apps: Host custom HTML applications inside Datasette](../../raw/web/web-datasette-apps-host-custom-html-applications-inside-datasett-5f725425.md)
[^src5]: [Porting the Moebius 0.2B image inpainting model to run in the browser with Claude Code](../../raw/web/web-porting-the-moebius-0-2b-image-inpainting-model-to-run-in-th-71cb4d77.md)
[^src6]: [Prompt Injection as Role Confusion](../../raw/web/web-prompt-injection-as-role-confusion-f81ed04e.md)
[^src7]: [What happened after 2,000 people tried to hack my AI assistant](../../raw/web/web-what-happened-after-2-000-people-tried-to-hack-my-ai-assista-20e22694.md)
[^src8]: [Incident Report: CVE-2026-LGTM](../../raw/web/web-incident-report-cve-2026-lgtm-61a73fa6.md)
[^src9]: [A quote from Sean Lynch](../../raw/web/web-a-quote-from-sean-lynch-f248e4ad.md)
