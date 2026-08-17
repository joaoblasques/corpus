---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-Tj3018n5MVg-stanford-s-method-turns-claude-into-a-phd-level-research-tea.md
    channel: youtube
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - youtube-quick-intake
  - multi-agent
  - research
  - storm
created: 2026-07-02
updated: 2026-08-17
provisional: false
youtube_video_id: Tj3018n5MVg
url: https://youtu.be/Tj3018n5MVg
channel_name: Nate Herk | AI Automation
playlist: Corpus_queue
published: 2026-06-29
transcript_status: ok
---

# Stanford's Method Turns Claude Into a PHD Level Research Team

> **Source** (YouTube · Nate Herk | AI Automation · 2026-06-29). [watch on YouTube](https://youtu.be/Tj3018n5MVg) · [transcript](../../../raw/youtube/youtube-Tj3018n5MVg-stanford-s-method-turns-claude-into-a-phd-level-research-tea.md)

**TL;DR:** Stanford's Storm research method — ported into a Claude Code skill — runs five specialized agent personas in parallel, then runs six verifier agents over the merged output. The result beats Claude's native deep-research workflow on evidence quality, source diversity, and thesis strength, according to a head-to-head evaluation in Codex.

---

## Storm: the method

Storm is a Stanford research method. Per the source, peer-reviewed testing showed it produces "articles 25% more organized than the next best method."[^t0] The core insight: a single-prompt research run has blind spots; multiple distinct perspectives each find holes the others miss.[^t28]

Storm uses five agent personas:[^t53]

| Persona | Role |
|---|---|
| Practitioner | Applied, real-world angle |
| Academic | Literature and theory |
| Skeptic | Challenge assumptions |
| Economist | Cost, ROI, incentives |
| Historian | Precedent and trajectory |

Each persona runs independently, then their outputs are converged and disagreements surfaced before verification.[^t141]

---

## Implementation as a Claude Code skill

The author encoded Storm's principles into a Claude Code skill (distributed free). The pipeline:[^t28]

1. Five perspective agents each produce a draft analysis.
2. Six verifier agents check every claim — confirming, correcting, or demoting each source.
3. Output is a structured HTML briefing.

The HTML report includes:[^t141]

- A 60-second summary of key findings.
- Each finding ranked by reliability (e.g., "reliability high 9/10"), with the personas that supported vs. challenged it noted inline.
- Explicit flagging of the assumptions the briefing rests on.
- Identification of the "missing sixth lens" — the perspective none of the five covered.

The missing-lens output is actionable: the user can instruct Claude to spin up that sixth lens and regenerate a V3 report.[^t166]

---

## Comparison: Storm vs. Claude's native deep research

Claude Code has a built-in deep-research command (launched with dynamic workflows) that spins up a dynamic workflow — the source notes one example ran 103 agents in the background.[^t83] However, the resulting report in the comparison was a markdown file with only two confirmed sources and several unconfirmed ones, plus open questions.[^t108]

The same prompt run through the Storm skill produced an HTML briefing that Codex (a separate AI model, used as evaluator) rated as superior: "better evidence quality… much stronger source diversity… much stronger thesis… more actionable."[^t222]

---

## Customization

Because Storm is a skill rather than a built-in command, it can be tailored. Users can embed context about their business or goals so every report is scoped to their situation — not a generic brain dump of statistics.[^t196]

---

## Connections

- Relates to the general pattern of [multi-agent roleplay personas](/ai-engineering/multi-agent-systems.md) for broadening research coverage.
- The verification pass (confirm/correct/demote per source) is an instance of the adversarial-verify quality pattern used in multi-agent workflows.
- Claude Code's dynamic workflow / deep-research feature is the baseline being compared against.

---

[^t0]: Transcript [00:00](https://youtu.be/Tj3018n5MVg?t=0) — "peer-reviewed testing to produce articles 25% more organized than the next best method."
[^t28]: Transcript [00:28](https://youtu.be/Tj3018n5MVg?t=28) — verification pass: sources "confirmed, corrected or demoted" on the second pass.
[^t53]: Transcript [00:53](https://youtu.be/Tj3018n5MVg?t=53) — five perspectives listed: practitioner, academic, skeptic, economist, historian.
[^t83]: Transcript [01:23](https://youtu.be/Tj3018n5MVg?t=83) — native deep research "will spin up a dynamic workflow which will kick off hundreds of agents… 103 different agents running."
[^t108]: Transcript [01:48](https://youtu.be/Tj3018n5MVg?t=108) — native deep research output: markdown, "only two [sources] up here… a few more unconfirmed."
[^t141]: Transcript [02:21](https://youtu.be/Tj3018n5MVg?t=141) — Storm pipeline: five agents → converge → six verifier agents → HTML report with reliability scores.
[^t166]: Transcript [02:46](https://youtu.be/Tj3018n5MVg?t=166) — report flags "the missing sixth lens" and assumption list; user can request a V3.
[^t196]: Transcript [03:16](https://youtu.be/Tj3018n5MVg?t=196) — skill can be tailored: "here's my business… make it tailored towards us."
[^t222]: Transcript [03:42](https://youtu.be/Tj3018n5MVg?t=222) — Codex evaluation: "HTML briefing is better… better evidence quality… much stronger thesis… more actionable."
