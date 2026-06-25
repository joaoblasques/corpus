---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-clippings-lessons-from-building-claude-code-prompt-caching-is-everythi.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-prompt-caching.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-6cEQEba0i2A-give-me-10-mins-and-i-ll-save-you-millions-of-claude-tokens.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - prompt caching
  - prefix caching
  - cache hit rate
  - cache-safe forking
  - compaction buffer
  - defer_loading
  - cache TTL
  - session handoff skill
  - model switch cache break
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-17
updated: 2026-06-25
---

# Prompt Caching

**TL;DR.** Prompt caching reuses computation from previous API roundtrips by prefix-matching cached tokens against new requests, cutting cost and latency. The key constraint: caching is a prefix match — any change anywhere in the prefix invalidates everything after it. Claude Code's entire harness is built around maximising cache hit rates; low rates are treated as a production SEV [^src1].

## How prefix caching works

The API caches everything from the start of a request up to each `cache_control` breakpoint. For two requests to share a hit, their prefixes must match byte-for-byte from the first token [^src1]. Order therefore matters enormously: put static content first, dynamic content last.

Claude Code's canonical layering [^src1]:

| Layer | Caching scope |
|---|---|
| Static system prompt + Tool definitions | Global (all sessions) |
| CLAUDE.md | Per project |
| Session context | Per session |
| Conversation messages | Grows turn-by-turn |

Common ways teams accidentally break this ordering: inserting a timestamp in the static system prompt, shuffling tool definitions non-deterministically, changing which agents the Agent tool can call between requests [^src1].

## Use messages, not system-prompt edits, for updates

When data in the prompt becomes stale (e.g. the current time, a changed file), the instinct is to update the system prompt — but that invalidates the entire cache. The better approach: inject the update as a `<system-reminder>` tag in the next user message or tool result. "This helps preserve the cache" [^src1]. The system prompt stays frozen; only the conversational tail grows.

## Don't switch models or tools mid-session

**Model switching** — prompt caches are per-model. Switching from Opus to Haiku mid-conversation means rebuilding the cache from scratch for Haiku, which can cost more than having Opus answer a simpler question directly [^src1]. When a model switch is necessary, use a **handoff subagent**: ask Opus to prepare a concise handoff message for the next model on the task, then spawn the subagent fresh [^src1].

**Tool changes** — adding or removing tools invalidates the cached prefix for the entire conversation. The intuitive approach — narrow the tool set when not needed — is exactly wrong [^src1].

**Plan Mode design insight.** Claude Code keeps *all* tools in the request at all times. Plan Mode is implemented via `EnterPlanMode` and `ExitPlanMode` as tools the model calls itself, not by swapping tool sets. Bonus: because `EnterPlanMode` is a tool, the model can enter plan mode autonomously on a hard problem without any cache break [^src1].

**Tool search with `defer_loading`.** When dozens of MCP tools are loaded, Claude Code sends lightweight stubs (name only, `defer_loading: true`) for infrequently needed tools. Full schemas load only when the model selects them. The stubs are always present in the same order, keeping the cached prefix stable [^src1].

## Cache-safe compaction (forking)

When the context window fills, Claude Code must summarize (compact) the conversation. The naive approach — a separate API call with a different system prompt ("summarize this") and no tools — creates a fully uncached request: the prefix diverges at token one, and you pay full uncached input rates on the entire conversation at exactly the moment it's longest [^src1].

**The cache-safe fork**: use the *exact same* system prompt, user context, system context, and tool definitions as the parent conversation. Prepend the parent's messages, then append the compaction prompt as a new user message. From the API's perspective the request looks nearly identical to the parent's last request, so the cached prefix is reused. Only the compaction prompt itself is billed at uncached rates [^src1].

This requires a **compaction buffer** — enough reserved context window space to include the compaction instruction and its output tokens. Anthropic built this pattern directly into the API's `compaction` feature [^src1].

## Operational discipline: monitor like uptime

Claude Code's team runs alerts on cache hit rate and declares SEVs when it drops below threshold. "A few percentage points of cache miss rate can dramatically affect cost and latency" [^src1]. At scale, prompt caching is what makes long-running agentic subscriptions economically viable — it "allows us to reuse computation from previous roundtrips and significantly decrease latency and cost" [^src1].

## Summary: five design rules

1. **Prefix match is the core constraint.** Any change anywhere in the prefix invalidates everything after it. Design the full system around this.
2. **Use messages instead of system-prompt changes** for dynamic state (plan mode, date, file updates).
3. **Never change tools or models mid-conversation.** Model state as tool transitions. Defer tool loading instead of removing tools.
4. **Monitor cache hit rate like uptime.** Alert on cache breaks; treat SEVs seriously.
5. **Side-computation forks must share the parent's prefix.** Compaction, summarisation, skill execution — all need cache-safe parameters.

## Official API: automatic caching, TTL, and pricing

The Anthropic API supports two caching modes [^src2]:

**Automatic caching** — add a single top-level `cache_control: {"type": "ephemeral"}` field to the request; the system automatically applies a breakpoint to the last cacheable block and advances it as conversations grow. Best for multi-turn conversations; no per-block annotations needed [^src2].

**Explicit caching** — place `cache_control` on individual content blocks for fine-grained control over independently changing sections. Up to 4 breakpoints per request [^src2].

**Lookback window** — on a cache read, the system checks at most 20 block positions backward from the breakpoint. A common mistake: placing the breakpoint on a block that changes every request (e.g. a timestamp). Move it to the last stable block before the dynamic suffix [^src2].

**TTL options** [^src2]:
- 5-minute (default, `"ephemeral"`) — refreshed at no charge each time it's read
- 1-hour (`"ephemeral"` + `"ttl": "1h"`) — 2× base input token price; longer TTL must come before shorter ones in the same request

**Effective TTL by client context** [^src3]:
- **Claude subscription (Claude Code CLI/extension)**: 1-hour TTL automatically applied — sessions that go idle for ≥1 hour become fully un-cached on the next message
- **API direct requests**: 5-minute default; can be explicitly set to 1-hour at 2× cost
- **Sub-agents / nested model calls**: always 5-minute TTL regardless of subscription plan — every sub-agent call runs as an API call, so cache expires quickly between invocations
- **Overuse territory (subscription → API billing)**: when the weekly subscription limit is exceeded and usage shifts to per-token API billing, cache TTL drops from 1h to 5m — "very dangerous if you're managing multiple sessions" [^src3]

**Model switch = full cache invalidation** [^src3]: each model has its own cache. Switching with `/model` — or using the `plan_model` setting that swaps Opus (plan mode) for Sonnet (execution) — starts a fresh cache even when the conversation content is identical. "The Opus plan model setting resolves to Opus during plan mode and Sonnet during execution. So each plan toggle is a model switch and starts a fresh cache" [^src3]. The trade-off: plan-mode model switching reduces session-limit cost over time, but it does break caching on each toggle.

**CLAUDE.md edits are safe mid-session** [^src3]: edits to CLAUDE.md during a session don't invalidate the cache until the session is restarted — the edit applies only on next session load.

**Session handoff as `/compact` alternative** [^src3]: rather than compacting (which is lossy and can be slow), practitioners use a session-handoff skill: the skill summarizes the session state, open decisions, and key files; the user copies the summary, runs `/clear`, and pastes it into a fresh session. "It feels like I haven't actually lost anything" while guaranteeing a fresh 1h cache window [^src3].

**Pricing multipliers** (vs base input token price) [^src2]:

| Event | Multiplier |
|---|---|
| Cache write (5m) | 1.25× |
| Cache write (1h) | 2× |
| Cache read | 0.1× |

**Minimum cacheable prefix**: 1,024 tokens for most models (higher for some on Bedrock). Shorter prompts silently skip caching — check `cache_creation_input_tokens` + `cache_read_input_tokens` in response usage to verify [^src2].

**Pre-warming** — send `max_tokens: 0` to load system-prompt content into cache before user traffic arrives (no output billed, cache write billed). Prevents first-request latency penalty in latency-sensitive apps [^src2].

**What invalidates the cache** — changing tool definitions invalidates the full cache (tools→system→messages hierarchy); toggling citations/web-search or changing speed setting invalidates system + message caches; adding/removing images or changing thinking parameters invalidates message cache only [^src2].

**Workspace isolation** (as of Feb 5 2026): caches are isolated per workspace within an org on the Claude API, AWS Platform, and Microsoft Foundry. Two different workspaces do not share cache even with identical prompts [^src2].

## See also

- [[ai-engineering/agent-cost-management|Agent Cost Management]] — cost economics of long-running agents; prompt caching as the primary lever
- [[ai-engineering/claude-code|Claude Code]] — plan mode, compaction, and the full harness built around prompt caching
- [[ai-engineering/context-window-management|Context Window Management]] — compaction strategy and what to keep/compress/drop
- [[ai-engineering/mcp|MCP]] — `defer_loading` via the tool search tool; keeping MCP tool stubs stable
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — cloud agent pricing; prompt caching reduces per-session-hour costs

---

[^src1]: [Lessons from building Claude Code: Prompt caching is everything](../../raw/notes/notes-clippings-lessons-from-building-claude-code-prompt-caching-is-everythi.md) — Thariq Shihipar, Anthropic
[^src2]: [Prompt caching — Anthropic API docs](../../raw/web/web-prompt-caching.md) — platform.claude.com
[^src3]: [Give Me 10 Mins and I'll Save You Millions of Claude Tokens](../../raw/youtube/youtube-6cEQEba0i2A-give-me-10-mins-and-i-ll-save-you-millions-of-claude-tokens.md) — Nate Herk, YouTube
