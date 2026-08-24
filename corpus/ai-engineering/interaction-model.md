---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-inside-thinking-machines-interaction-models-cc471afb.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - interaction model
  - TML-Interaction-Small
  - Thinking Machines lab
  - micro-turns
  - time-aligned micro-turns
  - harness ceiling
  - two-model coordination
  - voice AI harness
  - interactivity inside model
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
confidence: 0.8
last_confirmed: 2026-08-24
---

# Interaction Model

**TL;DR**: An architectural approach where real-time interactivity — handling concurrent input/output streams, interruptions, and time-awareness — is built into the model itself rather than implemented as external scaffolding (a "harness"). Proposed by Thinking Machines lab; their first implementation is TML-Interaction-Small (276B MoE, 12B active), designed around 200ms micro-turns [^src1].

## The harness architecture and its ceiling

Most real-time voice AI is built as a harness: a turn-based language model surrounded by helper components that simulate conversation [^src1].

**Standard harness components** [^src1]:
- Voice Activity Detection (VAD) — detects pauses, decides when the user has stopped speaking
- Speech-to-Text (STT) — transcribes the audio
- Language model — generates a text response
- Text-to-Speech (TTS) — converts the response back to audio
- Dialog manager — orchestrates the pipeline to minimize perceived latency

The harness mostly works, but it has a structural ceiling: **the helpers are simpler than the model itself** [^src1]. VAD runs on raw audio signals using a much smaller model than the underlying LLM. This gap creates categories of behavior the harness cannot support:

- *Proactive interjections* ("interrupt me when I say something wrong") — the helper deciding when to speak operates purely on acoustic signals; correctness is the LLM's job [^src1].
- *Visual reactions* ("tell me when I've written a bug") — the audio helper has no access to screen content [^src1].
- *Mid-sentence corrections* — requires speaking while listening, which turn-based architecture handles as separate operations [^src1].

> "The helpers are simpler than the model itself. This limits whole categories of behavior." [^src1]

Thinking Machines applies Sutton's Bitter Lesson to this domain: methods that leverage general computation and learning consistently outperform human-designed heuristics. VAD, dialog management, and turn detection are heuristics; the path past the ceiling is to absorb them into the model [^src1].

## The interaction model architecture

Thinking Machines' answer is to redesign the model for real-time interactivity from scratch, not add voice on top of a text model [^src1].

### Design principle: start from continuous audio and video

Most multimodal systems start with text and add audio/video on top. Thinking Machines did the reverse — starting from continuous audio and video because live conversation operates under tight real-time constraints that text can avoid [^src1]. Designing around the hardest case first produces an architecture that handles concurrent input and output streams across every modality.

### Time-aligned micro-turns

Instead of conversation turns (user speaks → model speaks → user speaks), Thinking Machines slices time into **200-millisecond chunks** called micro-turns [^src1]. Every 200ms the model:
1. Takes in whatever arrived across audio, video, and text streams
2. Decides what to output across audio and text streams

Time becomes the fundamental unit, replacing the turn entirely. This unlocks behaviors that turn-based architectures cannot support regardless of speed [^src1]:
- Speaking while listening (live translation)
- Watching while speaking (live sports commentary)
- Jumping in mid-sentence based on visual events (counting pushups in real time)
- Correcting mispronunciation as it is heard (requires simultaneous speak and listen)

### Lightweight processing without pretrained encoders

TML-Interaction-Small skips heavy pretrained encoders (like Whisper for audio). Audio and video go through lightweight components trained from scratch alongside the core model, rather than being routed through standalone systems [^src1]. This avoids the encoder as a bottleneck for real-time constraints.

### Two-model coordination: fast + slow

Time-aligned micro-turns solve responsiveness but create a new problem: how does a 200ms model do deep reasoning? [^src1]

**The solution: two coordinated models** [^src1]:
- **Interaction model** — fast, present, handles real-time conversation micro-turn by micro-turn
- **Background model** — slower, handles sustained reasoning, tool use, browsing, chained reasoning

**Coordination flow** [^src1]:
1. When the interaction model hits something requiring deeper reasoning, it sends a rich context package (the full conversation, not a standalone query) to the background model
2. The background model runs asynchronously; results stream back as produced
3. The interaction model weaves results into the conversation at a natural moment, not as an abrupt context switch

From the user's perspective: one continuous conversation with one AI. Behind the scenes: two coordinated systems. This is the fast-path/slow-path pattern — common in operating systems and web browsers — applied to AI inference [^src1].

## First implementation: TML-Interaction-Small

**Architecture** [^src1]:
- 276 billion parameter Mixture-of-Experts (MoE) model
- 12 billion parameters active at any moment
- Named "Small" to indicate its position in a planned lineup (larger versions expected)
- Contributed a streaming session feature back to the open-source SGLang library enabling 200ms chunk processing at low latency

## Benchmarks

Existing voice AI benchmarks do not capture the qualitative shift; Thinking Machines built their own [^src1]:

| Benchmark | Task example |
|---|---|
| **TimeSpeak** | "Remind me to breathe in and out every 4 seconds until I ask you to stop" — tests whether the model initiates speech at user-specified times with correct content |
| **CueSpeak** | "Every time I codeswitch, give me the correct word in the original language" — tests whether the model speaks at the right moment while the user is still talking |
| **RepCount-A** | Streams video of pushup reps; instruction: "count out reps" — tests visual real-time tracking |
| **ProactiveVideoQA** | Streams video with questions whose answers depend on what is happening visually at specific moments |

Result: across these benchmarks, all existing models (turn-based architectures) either stay silent or give wrong answers. Thinking Machines presents this as evidence of a new capability class, not just lower latency [^src1].

## Limitations

**Long sessions**: continuous audio/video accumulates context very quickly. The streaming-session design handles short and medium interactions well; very long sessions require careful context management [^src1].

**Connectivity**: streaming audio and video at low latency demands a reliable internet connection; poor connectivity degrades significantly [^src1].

**Scaling model size**: TML-Interaction-Small is the size it is partly because Thinking Machines' larger pretrained models are too slow to serve within latency targets. Real-time constraints cap model size directly [^src1].

## The general principle

The Thinking Machines work illustrates a pattern that appears across computing: **adding a capability through external scaffolding creates a ceiling on how good that capability can get — the scaffolding becomes the bottleneck rather than the underlying system** [^src1].

Applied to AI:
- Hand-crafted computer vision features → deep learning
- Hand-crafted game heuristics → self-play
- Harness-based interactivity → interactivity inside the model

This is Sutton's Bitter Lesson applied to the interface layer [^src1].

## See also

- [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) — the two-model coordination scheme (fast interaction + slow background) mirrors the orchestrator-subagent pattern
- [Agent Harness](/ai-engineering/agent-harness.md) — harness architecture is what this approach replaces for real-time modalities
- [Claude Code](/ai-engineering/claude-code.md) — Claude Code uses a harness model; contrast with the interaction model approach

---

[^src1]: [Inside Thinking Machines' Interaction Models](../../raw/web/web-inside-thinking-machines-interaction-models-cc471afb.md) — ByteByteGo, collected 2026-07-01; harness ceiling, micro-turn architecture, TML-Interaction-Small, two-model coordination, benchmarks
