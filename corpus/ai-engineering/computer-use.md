---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-clippings-best-practices-for-computer-and-browser-use-with-claude.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-introducing-sonnet-4-6.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/web/web-mitigating-the-risk-of-prompt-injections-in-browser-use.md
    channel: web
    ingested_at: 2026-06-21
aliases:
  - computer use
  - browser use
  - computer use API
  - computer_20251124
  - CU
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-17
updated: 2026-06-21
---

# Computer Use (Claude)

**TL;DR**: Computer use lets Claude perceive a screen via screenshots and act on it via clicks, keyboard input, and scroll — enabling agentic automation of any desktop or browser workflow. The single highest-impact optimization is pre-downscaling screenshots to fit API resolution limits before sending them. After that, model selection, thinking-effort tuning, context management, and prompt-injection defense determine production reliability [^src1].

## Resolution and coordinate scaling

Click accuracy is the foundation. The root cause of most click inaccuracy is a mismatch between the coordinate space Claude thinks it is operating in and the actual image the API processed [^src1].

**API resolution limits** (images exceeding either limit are silently downscaled, causing coordinate drift) [^src1]:

| Model family | Max long edge | Max total pixels |
|---|---|---|
| Claude 4.6 (Opus/Sonnet/Haiku) | 1568 px | 1.15 MP |
| Claude Opus 4.7 | 2576 px | 3.75 MP |

**Recommended starting resolutions** [^src1]:
- **Claude 4.6 family**: 1280×720 (uses ~80% of pixel budget, stays within both limits, standard training resolution).
- **Claude Opus 4.7**: start at 1080p — meaningful quality lift over 720p with budget to spare.
- **Never send native resolution** without checking limits; 1920×1080+ exceeds the 4.6 family budget and will be silently downscaled.
- **Avoid below 960×540**: too much UI detail is lost for small target identification.
- **MacOS caveat**: screenshots often capture at 2× device pixel ratio; resize explicitly before sending.

**Max-API-fit approach** (advanced): compute the optimal resolution per image using the aspect ratio and the model's limits, to maximize visual fidelity without exceeding the pixel budget [^src1]. Code pattern:

```python
def compute_max_api_fit(native_w, native_h, MAX_LONG_EDGE=1568, MAX_PIXELS=1_150_000):
    aspect = native_w / native_h
    h_from_pixels = math.sqrt(MAX_PIXELS / aspect)
    w_from_pixels = h_from_pixels * aspect
    if native_w >= native_h:
        w = min(w_from_pixels, MAX_LONG_EDGE)
        h = w / aspect
    else:
        h = min(h_from_pixels, MAX_LONG_EDGE)
        w = h * aspect
    return int(min(w, native_w)), int(min(h, native_h))
```

**Coordinate scaling after resize**: when you resize a screenshot before sending, the model returns coordinates in the *display* space you specified. Scale back to native screen space before executing [^src1]:
```python
screen_x = int(api_x * (screen_w / display_w))
screen_y = int(api_y * (screen_h / display_h))
```

**Content ordering**: place the text instruction *before* the image in the API messages array. The model knows what to look for as it processes the screenshot, which improves click accuracy [^src1].

## Model selection for clicking

- **Sonnet 4.6**: most mechanically precise at clicking (best spatial accuracy, fewest near-misses); more robust when source images require heavy downscaling. Best balance of accuracy, reasoning, and cost for most tasks [^src1]. The Sonnet 4.6 launch cited "significant OSWorld improvements" and is described as having "major improvement compared to Sonnet 4.5" on prompt-injection robustness [^src2][^src3].
- **Opus 4.6**: stronger reasoning but slightly less clicking precision; use when reasoning matters more than click accuracy.
- **Opus 4.7**: closes the precision gap with Sonnet 4.6, plus has the higher resolution budget (3.75 MP), making it the strong choice for hard tasks where both reasoning and accuracy matter.
- **Haiku 4.5**: best when latency is the priority.
- **Orchestrator + sub-agent pattern**: advanced workflows use a reasoning model to handle planning while Sonnet or Haiku executes the mechanical clicking steps [^src1].

## Thinking effort tuning

Claude 4.6 and 4.7 support adaptive thinking (`thinking: {"type": "adaptive"}`) with effort levels `low`, `medium`, `high`, `xhigh` (4.7 only), `max` [^src1].

**Claude 4.6 family** [^src1]:
| Scenario | Effort | Rationale |
|---|---|---|
| Default | `medium` | Best accuracy-to-cost ratio; matches `high` with retries at half the tokens |
| High-throughput / cost-sensitive | `low` | More accurate than no thinking (fewer errors, fewer retries) at lower token cost |
| Simple, predictable workflows | disabled | Lowest latency for well-known UIs |
| Complex one-shot tasks | `high` | Needed when you can't retry and must get it right |

`max` is not recommended for 4.6 computer use — provides no accuracy benefit over `high` while increasing tokens. UI tasks are primarily perceptual, not deeply logical [^src1].

**Claude Opus 4.7** [^src1]:
| Scenario | Effort | Rationale |
|---|---|---|
| Default | `high` | Strong reasoning with reasonable token usage; close to max accuracy |
| High-throughput / cost-sensitive | `low` | Scores similarly to Sonnet 4.6 on max, with ~1/10th the tokens |
| Simple, well-defined workflows | try Sonnet 4.6 | Lowest latency |
| Complex one-shot tasks | `max` | When you must get it right on the first attempt |

## Handling small targets

Click accuracy degrades as targets shrink. Large buttons and inputs are reliable; checkboxes, system tray icons, and tiny toggles require extra strategies [^src1]:

- **Enable zoom**: `enable_zoom: True` in the tool configuration lets the model inspect screen regions at higher resolution before clicking.
- **Make targets larger**: if you control the UI, increasing target size (lower DPI, browser zoom) has outsized impact.
- **Keyboard alternatives**: for very small elements, tab navigation or keyboard shortcuts can be more reliable than clicking.
- **High-DPI sources**: a 16px checkbox at 3840×2160 becomes ~5px at 1280×720; consider Opus 4.7's higher resolution budget, or crop the screenshot to the relevant area before downscaling.

## Approaches that did NOT help (internal testing)

- Splitting the image into tiles/quadrants and sending separately: no improvement.
- Overlaying a coordinate grid: no reliable gains.
- Choice of resize algorithm (LANCZOS vs sips vs others): identical results — use whatever is convenient [^src1].

## Prompt injection defense

Computer use agents interact with untrusted content by design — every screenshot, webpage, or application UI could contain adversarial instructions [^src1]. The attack surface is fundamentally different from a controlled API integration.

**Anthropic's three-layer defense** [^src1]:
1. **Training-time robustness**: RL exposure to injected content during training; Claude is rewarded for correctly refusing malicious instructions.
2. **Real-time classifiers**: probes scan content entering the context window and flag potential prompt injection across text, images, and deceptive UI elements.
3. **Continuous red teaming**: internal and external adversarial evaluations.

**Classifier availability**: classifiers run automatically (zero additional latency, no extra cost) when using the official `computer_20251124` tool type. Custom tool implementations (`screenshot` + `click` as custom tools) do not currently receive classifier protection [^src1].

**Best practices regardless of classifier** [^src1]:
- **Human-in-the-loop for high-stakes actions**: pause and require user confirmation before submitting forms, making purchases, sending messages, or modifying data — the single most effective mitigation.
- **Scope permissions**: if the workflow doesn't need downloads, don't grant download access; reduce blast radius.
- **Log all agent actions with screenshots** per step for auditing and failure analysis.
- **Treat all web content as untrusted**: the system prompt should clearly separate user instructions from content encountered during task execution.

## Context management for long-running computer use

Screenshots accumulate at ~1,000–1,800 tokens each (depending on resolution). A 200k context window can fill in well under 100 screenshots [^src1]. Effective context management has more impact on cost and latency than almost any other optimization.

**Three composable layers** [^src1]:

**1. Cache breakpoints**: the API supports 4 breakpoints. Use one on the stable system-prompt prefix; use the other three on the most recent tool results, advancing them each turn. This keeps cache hit rate high while gracefully degrading if a breakpoint is invalidated.

**2. Rolling buffer (cache-aware)**: keep only the N most recent screenshots; prune older ones in batches (not one at a time — batch pruning keeps the message prefix stable between prune events, maintaining cache hits). Default: `keep_n=3`, `interval=25`.

**3. LLM-based compaction**: when pruning alone isn't enough, summarize the full conversation before discarding older history. Preserve verbatim user instructions, task template, constraints, actions taken, errors and fixes, progress tracking, current state, and next step [^src1]. Use server-side compaction (beta) via `context_management: {"edits": [{"type": "compact_20260112"}]}` and client-side truncation to keep the two views aligned.

> "We consistently observe significant accuracy degradation when images exceed [API] limits, and this single change [pre-downscaling] is worth more than almost any other optimization." [^src1]

## Teach mode (show, don't tell)

Instead of iterating on text prompts, record a demonstration — screenshots + action sequence — and replay it as context when Claude executes the same workflow. Used internally as "Teach Mode" in Claude in Chrome [^src1].

**Core concept**: playback isn't strict replay — Claude uses the demonstration as a guide and adapts to UI changes in the live environment (moved buttons, reorganized menus) [^src1].

**Data model**: each `WorkflowStep` bundles action type, human-readable description, timestamp, CSS selector, click coordinates, URL, viewport dimensions, and optionally a voice narration transcript [^src1]. Capture both selectors and coordinates: selectors are more robust to layout changes; coordinates provide a visual fallback.

**Playback modes** [^src1]:
- **Strict**: follow exactly; stop if UI changed too much. For compliance-sensitive workflows.
- **Adaptive**: follow the demonstration but adapt to UI changes. Best default.
- **Goal-oriented**: treat recorded steps as hints; focus on the end result. For frequently-changing UIs — consider first summarizing the recorded workflow to reduce input token cost.

## Experimental patterns

**Batch tools** (`computer_batch` / `browser_batch`): execute multiple sub-actions in one tool call to reduce round trips and output tokens. Works well for self-contained sequential actions (fill multiple form fields, chain keyboard shortcuts). Risky when action 2 depends on visual state from action 1 — batch tools see no intermediate screenshots [^src1].

**Advisor tool (beta)**: pairs an executor model with a higher-intelligence advisor model (e.g., Sonnet 4.6 executing, Opus 4.7 advising). The executor calls the advisor mid-generation for planning and course-correction; advisor runs server-side within a single request. Most useful on long-horizon tasks with mostly mechanical clicking punctuated by decision-heavy moments [^src1].

**Periodic reminder nudges**: on long sessions (>20 turns), the executor model can forget which tools are available. Append a short reminder about `computer_batch` or the advisor tool availability after tool results to restore tool awareness [^src1].

## Debugging tools

- **Trajectory viewer** (`streamlit run viewer/app.py`): step through recorded turns with screenshots, thinking, tool calls, and per-step usage. For post-mortem analysis of failed runs.
- **Tool debug panel** (`uvicorn debug.server:app`): exercise each tool individually (screenshot, click, type, scroll, zoom) to confirm the capture pipeline.
- **Localization playground** (`uvicorn localize.server:app --port 8001`): upload an image, ask Claude to point at a target, see predicted coordinates overlaid at both display and native resolution. Fastest way to diagnose click misses in isolation [^src1].

## See also

- [[ai-engineering/claude-code|Claude Code]] — Claude Code's auto mode uses a similar classifier approach for permission decisions
- [[ai-engineering/agent-harness|Agent Harness]] — harness design principles underlying computer use integrations
- [[ai-engineering/context-window-management|Context Window Management]] — compaction and rolling-buffer patterns apply directly
- [[ai-engineering/agent-security|Agent Security]] — prompt injection as an attack surface
- [[ai-engineering/claude-models|Claude Model Lineup]] — Sonnet 4.6, Opus 4.6, Opus 4.7, Haiku 4.5 model selection

---

[^src1]: [Best practices for computer and browser use with Claude](../../raw/notes/notes-clippings-best-practices-for-computer-and-browser-use-with-claude.md) — Lucas Gonzalez & Luca Weihs, Anthropic
[^src2]: [Introducing Claude Sonnet 4.6](../../raw/web/web-introducing-sonnet-4-6.md) — Anthropic official blog (OSWorld + prompt injection robustness)
[^src3]: [Mitigating the Risk of Prompt Injections in Browser Use](../../raw/web/web-mitigating-the-risk-of-prompt-injections-in-browser-use.md) — Anthropic (1% attack rate; Claude for Chrome beta)
