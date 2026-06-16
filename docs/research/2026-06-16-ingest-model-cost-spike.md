# Ingest-model cost spike — can we run the unattended ingest off paid Opus?

> 2026-06-16 · spike · outcome: **keep Opus as the ingest default; ship a reversible opt-in `--model` lever; do NOT route the agentic ingest through OpenRouter free-tier.**

## Question

The headless daily ingest (`bin/scheduled_run.py run` → `claude --print` over the
`/ingest-auto` skill) is the dominant per-run cost (a single 3-source ingest ran
~$2.6 notional / 16k output / 2M cache reads). Can we cut that by moving the
ingest off paid Opus — to OpenRouter free-tier, or to a cheaper Claude tier?

## Findings

### 1. OpenRouter free-tier does not fit the *agentic* ingest

The ingest is not a single LLM call routed through `bin/llm.py` — it is the full
Claude Code agentic loop (`claude --print`) driving the `/ingest-auto` skill with
Read/Write/Edit/Glob/Grep/LS tools, returning a JSON envelope. That loop is built
around Anthropic models and the Claude Code tool/skill system. Pointing it at
OpenRouter would mean an `ANTHROPIC_BASE_URL` swap that, in practice, breaks
tool-use reliability and the skill machinery. OpenRouter stays useful only for the
**mechanical** `bin/llm.py` path (link-ranking), which is already wired and
defaults off. So the realistic in-ecosystem lever is the Claude `--model` flag
(stay on the subscription, pick a cheaper tier), not a provider swap.

### 2. Haiku is NOT safe for the unattended ingest — it fabricates where Opus abstains

Live A/B data point. Ran one real ingest of a **pointer email**
(`email-2026-05-17-…andrej-karpathy-skills…`, `pointer: true`, body = bare URL;
real content fetched separately to `raw/web/github-multica-ai-…md`) with
`--model claude-haiku-4-5`. Result: `{"status":"ok","ingested":1}` in 96s — fast
and cheap. But the page it wrote was a **provenance violation**:

- It did **not follow the pointer** to the fetched web content.
- Having only the title/URL, it **invented** a "Key themes" section prefixed
  *"Topics likely include…"* — speculation, not extraction — with a single
  bare-URL citation. Directly violates CLAUDE.md §7 ("compress what sources say,
  not invent what they don't") and §13 ("filing a claim with no source").
- Set `confidence: 0.8` on what was mostly fabricated.

Contrast: Opus **deferred** this exact class of pointer/digest emails to
`raw/_inbox/_REVIEW.md` (the two entries resolved the same day) rather than
fabricate. The cheap model turns a correct *abstention* into corpus rot — the one
failure mode the whole architecture exists to prevent. The post-ingest lint gate
did not catch it (the invented wikilinks happened to resolve), which underscores
that model judgment, not just mechanical lint, is load-bearing here.

> The experiment was diagnostic: the generated page and the source stamp were
> reverted; the corpus is unchanged by this spike.

## Decision

- **Default stays Opus.** The cost delta is not worth silent corpus degradation on
  exactly the ambiguous sources (pointers, digests) that need the most judgment.
- **Ship the lever anyway, opt-in.** `run_ingest(model=…)` / env
  `SCHEDULED_RUN_INGEST_MODEL` adds the cheaper-tier override without flipping it
  (unset → no `--model` flag → session default). Lets us re-test on a *substantive,
  non-pointer* corpus as models improve, and run cheap throwaway experiments.
- **Real cost control is elsewhere and already shipped:** the `--max 6` per-run cap
  (PR #21) and the post-ingest lint gate (PR #20). Those bound spend and catch
  mechanical rot without touching model quality.

## Follow-ups (not done)

- Re-run the A/B on a *substantive* source (not a pointer) before any future
  reconsideration — the pointer case is the hardest, so this verdict is
  conservative-correct but a fuller picture needs a content-rich source too.
- Consider teaching `/ingest-auto` to resolve `pointer: true` emails to their
  fetched `raw/web/` companion before extraction, so pointer emails stop being a
  deferral/again-fabrication trap regardless of model.
