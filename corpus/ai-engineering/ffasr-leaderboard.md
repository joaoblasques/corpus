---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-introducing-the-ffasr-leaderboard-benchmarking-asr-in-the-re-c8f31042.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - Far-Field ASR Leaderboard
  - FFASR
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-03
updated: 2026-07-03
---

# FFASR Leaderboard

**TL;DR.** The FFASR (Far-Field ASR) Leaderboard is an open, community-driven benchmark from Treble Technologies and Hugging Face that scores automatic speech recognition (ASR) models under realistic far-field acoustic conditions — reverberation, background noise, microphone distance — rather than the clean, close-microphone conditions standard ASR benchmarks (LibriSpeech and similar) use [^src1]. Across all submitted models, far-field word error rate (WER) at low signal-to-noise ratio (SNR) is consistently several times higher than near-field WER on the same speech content [^src1].

## Why this benchmark exists

Voice interfaces have expanded past headsets and smartphones into AI voice agents, conference-room transcription, in-car assistants, humanoid robots, and smart glasses — environments with a microphone anywhere from one to several meters from the speaker. Models that score well on clean, close-mic benchmarks do not reliably predict far-field performance; prior efforts (CHiME, URGENT, NOIZEUS) addressed pieces of this but the field lacked a standardized, continuously updated, open leaderboard for it [^src1].

## Data and methodology

- **Simulation-based, not purely measured**: physical far-field recordings across a representative range of rooms/distances/noise conditions are prohibitively expensive to collect at scale, so acoustic data is generated with Treble's **hybrid wave-based simulation engine** (wave-based solver at low/mid frequencies + geometrical-acoustics modeling at higher frequencies), which captures diffraction, scattering, interference, and modal behavior that simpler simulators miss [^src1].
- **Sim-to-real validation**: two leaderboard columns, "Lab Measured" and "Lab Simulated," run the same evaluation on both measured and simulated audio to directly confirm the simulation matches reality [^src1].
- **Coverage**: 14 fully furnished rooms (20–470 m³: bathrooms, living rooms with hallways, offices, classrooms, restaurant spaces); each scene has one target speaker (recorded anechoic to avoid recording-environment reverb artifacts) and up to three noise sources — always including one transient source (e.g. coughing) and one continuous source (e.g. HVAC) — at three SNR levels [^src1].
- **Moving-source splits** (beta): evaluates models against audio where the speaker is in motion, relevant to humanoid robots, in-car speech, and mobile assistants where speaker-microphone geometry changes continuously [^src1].
- **Held-out test set**: 2,000 anechoic speech samples across the 14 rooms at three SNR tiers (~8 hours of audio per condition), Whisper-style text normalization applied consistently; audio is not exposed to submitters to avoid test-set contamination [^src1].

## Ranking axes

- **Primary ranking score**: nine evaluated conditions, four of which determine the primary score (as of 2026-06-22) [^src1].
- **RTFx** (audio seconds per inference second) is reported alongside WER for every submission, measured on an NVIDIA L4 GPU under identical conditions — the leaderboard's Analysis tab plots average WER against RTFx as a Pareto front so accuracy/speed tradeoffs are directly comparable for a given deployment target [^src1].
- **Near-field vs. far-field WER reported side by side**: this separation distinguishes a model that is genuinely accurate from one that is accurate but brittle to acoustic conditions — informing whether to invest in far-field fine-tuning, speech-enhancement preprocessing, or a different architecture [^src1].

## Submission pipeline

Paste a Hugging Face model ID into the Submit tab; evaluation runs server-side against the held-out set. Out-of-the-box support covers Whisper variants, IBM Granite Speech, Cohere Transcribe, Wav2Vec2/HuBERT CTC heads, SpeechBrain ASR, and most other Hub ASR architectures with no custom configuration. For more complex inference stacks (e.g. combining speech enhancement with ASR), a custom `evaluate()` function is supported via a custom-evaluator option, which runs on Hub Jobs after moderator review [^src1].

## Roadmap

Actively explored future tracks: multi-talker scenarios (more than one active speaker), microphone-array evaluation (beamforming, spatial filtering), and echo cancellation (relevant to any device that plays audio while listening) [^src1].

## Related

- [Hugging Face](/ai-engineering/hugging-face.md) — leaderboard co-launched and hosted on the Hub
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — benchmark/leaderboard design patterns generally
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Introducing the FFASR Leaderboard: Benchmarking ASR in the Real World](../../raw/web/web-introducing-the-ffasr-leaderboard-benchmarking-asr-in-the-re-c8f31042.md) — Hugging Face blog (Treble Technologies × Hugging Face), 2026-06-28
