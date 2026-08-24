---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-what-is-seed-audio-1-0-bytedance-s-audio-scene-generator-for-3af2ff8f.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - Seed Audio 1.0
  - ByteDance Seed Audio
  - audio scene generation
tags:
  - corpus/ai-engineering
  - source
  - ai-audio
  - bytedance
  - seedance
created: 2026-08-24
updated: 2026-08-24
---

# Seed Audio 1.0: ByteDance's Audio Scene Generator for AI Video Workflows

**TL;DR.** Seed Audio 1.0 is ByteDance's audio scene generation model — not a general-purpose TTS tool. It ingests a video clip, reads the visual content, and produces a unified audio track (dialogue + ambient + SFX) synchronized with the scene at $0.18/min. Designed as the audio leg of the [Seedance](/ai-engineering/sources/seedance-2-5-features-explained-992932d0.md) video generation pipeline. [^sa]

## What makes it "audio scene generation" (not TTS)

Standard TTS tools produce voice from text. Audio scene generation is contextually aware: Seed Audio 1.0 reads the visual content of a video — setting, motion, character behavior — and infers the audio environment from the visuals rather than requiring a complete text description [^sa].

Output is a unified mix of three layers [^sa]:

| Layer | What it generates |
|---|---|
| Speech / dialogue | Voices that fit detected characters or scene context |
| Ambient audio | Environmental sound matching the visual setting |
| Sound effects | Action-triggered sounds (footsteps, doors, impacts) |

All three are layered into a single synchronized audio track, not separate stems by default [^sa].

## Input formats

- A video clip (primary — analyzed for visual context)
- Optional text prompt for additional scene description
- Parameters for tone, environment, and audio intensity

"You don't have to write detailed prompts for every audio element. The model infers many of these from the video itself." [^sa]

## What it does NOT do

Seed Audio 1.0 is not a music composition tool. It generates *diegetic* sound — audio that exists within the world of the scene (dialogue, ambient noise, SFX). Background music/scores require a separate tool (Suno, Udio, etc.) [^sa].

## Pricing

$0.18 per minute of generated output (not per compute-minute) [^sa]:

| Volume | Cost |
|---|---|
| 30-second clip | ~$0.09 |
| 5-minute short | ~$0.90 |
| 100 minutes | $18.00 |

Positioned as cost-effective vs. running TTS + SFX + mixing separately, which "would cost more per minute in aggregate, and consume significantly more time" [^sa].

## Integration with Seedance

Designed as the audio leg of the Seedance workflow — but accessible via API for any video pipeline [^sa]:

1. Generate video using Seedance from text/image prompt
2. Pass video clip to Seed Audio 1.0
3. Receive synchronized audio matched to the generated video
4. Combine and export

For the reverse workflow (audio-first then video), see [Seed Audio → Seedance workflow](/ai-engineering/sources/seed-audio-seedance-workflow-53f11534.md).

## Use cases beyond Seedance

- Social media content production at scale
- Synthetic training data (audio-complete video for vision model training)
- Localization / dubbing workflows
- Game / simulation environment audio
- Automated news/report video [^sa]

## Related

- [Seedance 2.5 features](/ai-engineering/sources/seedance-2-5-features-explained-992932d0.md)
- [Seedance 2.5 Volcano Arc / IP licensing](/ai-engineering/sources/seedance-2-5-volcano-arc-ip-licensing-41a7a0cc.md)
- [Seed Audio → Seedance audio-first workflow](/ai-engineering/sources/seed-audio-seedance-workflow-53f11534.md)

---

[^sa]: MindStudio Blog, "What Is Seed Audio 1.0? ByteDance's Audio Scene Generator for AI Video Workflows," mindstudio.ai, 2026-07-01. `raw/_inbox/web-what-is-seed-audio-1-0-bytedance-s-audio-scene-generator-for-3af2ff8f.md`
