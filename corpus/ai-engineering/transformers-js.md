---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-experimenting-with-the-proposed-cross-origin-storage-api-in-dba1e8f0.md
    channel: web
    ingested_at: 2026-07-03
aliases:
  - Transformers.js
  - transformers.js
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-03
updated: 2026-07-03
---

# Transformers.js

**TL;DR.** Transformers.js is Hugging Face's JavaScript library for running transformer models directly in the browser via task-specific `pipeline()` calls (e.g. automatic speech recognition, sentiment analysis), built on top of ONNX Runtime Web [^src1]. Its main scaling problem — every site re-downloading the same model/runtime bytes because browser caches are partitioned per-origin — is what the proposed **Cross-Origin Storage (COS) API** is designed to fix, and Transformers.js is one of the libraries piloting it [^src1].

## Usage pattern

```js
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@4.2.0';
const asr = await pipeline(
  'automatic-speech-recognition',
  'Xenova/whisper-tiny.en',
  { device: 'webgpu' },
);
const result = await asr('jfk.wav');
```

Transformers.js has default-model resolution per task (e.g. `Xenova/whisper-tiny.en` for ASR, `Xenova/distilbert-base-uncased-finetuned-sst-2-english` for sentiment analysis) and automatically downloads/caches model resources and the underlying Wasm runtime files via the browser's Cache API [^src1].

## The cache-partitioning problem

Browsers key cached resources by a **Network Isolation Key** (top-level site + current-frame site) in addition to the resource URL, specifically to prevent cache-timing side-channel attacks that could otherwise leak browsing history across origins [^src1]. Consequence: two unrelated sites using the exact same model or the exact same shared ONNX Runtime Wasm file (`ort-wasm-simd-threaded.asyncify.wasm`, ~4.7 MB, shared by every Transformers.js app regardless of model) each pay the full download and storage cost independently — measured at 177 MB of duplicate download/storage for one popular model (`Xenova/whisper-tiny.en`) alone in a two-origin toy example [^src1].

## Cross-Origin Storage (COS) API

An early-stage, not-yet-standardized browser proposal (not natively implemented in any browser; testable via a Chrome extension polyfill) that lets web apps store/retrieve large files across origin boundaries, identified by a **cryptographic hash** (e.g. SHA-256) rather than by URL or origin [^src1]:

```js
const hash = { algorithm: 'SHA-256', value: '8f43...' };
try {
  const handle = await navigator.crossOriginStorage.requestFileHandle(hash);
  const fileBlob = await handle.getFile();          // cache hit
} catch {
  const fileBlob = await fetch(url).then(r => r.blob());   // cache miss
  const handle = await navigator.crossOriginStorage.requestFileHandle(hash, { create: true, origins: '*' });
  const writableStream = await handle.createWritable();
  await writableStream.write(fileBlob);
  await writableStream.close();
}
```

- **API shape**: modeled after the File System Standard's OPFS `getFileHandle()` — `hash` plays the role of `name`; `options.create` toggles read-only vs. write access [^src1].
- **Visibility control** via the `origins` option: `'*'` makes a file globally discoverable by hash (right for shared AI model/runtime resources); a specific origin list restricts access (e.g. proprietary resources shared within one company's properties); omitting `origins` defaults to same-site-only [^src1].
- **Visibility can only be upgraded, never downgraded** — a file already stored `'*'` cannot later be re-stored with a narrower list (prevents a malicious actor from narrowing a public resource's availability). Any site can widen a restricted file's visibility later by re-storing it under the same hash with a broader `origins` value and `create: true`, but must re-write the full file content (prevents using the upgrade path as a side-channel to detect whether a file was already present) [^src1].
- **Integrity by construction**: the browser verifies the hash matches the written bytes on write, so a file read from COS is guaranteed to be exactly the expected bytes — closing a gap where apps today have no practical way to verify a CDN served the correct model weights [^src1].
- **Privacy mitigation for the hash-based cross-site probing risk**: (1) developer-side — don't store non-shareable resources with `origins: '*'`; (2) browser-side — **availability gating**, where the browser may suppress confirmation of a file's presence if it hasn't been encountered across a sufficient number of distinct origins, even if the file is physically on disk. Apps should treat "not found" as ambiguous (either genuinely absent, or present-but-withheld) and always fall back to network fetch on error [^src1].

## Transformers.js's COS integration

Piloted at the library level (PR #1549) behind an opt-in experimental flag [^src1]:

```js
env.experimental_useCrossOriginStorage = true;
```

With the flag set, Transformers.js resolves the SHA-256 hash for each Xet-tracked model file by fetching the raw Xet pointer and reading its `oid sha256:` field, then uses that hash as the COS lookup key — falling back to a normal network download (and storing the result in COS for the next caller) when the resource isn't already present [^src1]. `ModelRegistry.is_pipeline_cached()` integrates with COS (alongside the Cache API) so an app can probe which of several acceptable model variants (e.g. Whisper tiny/medium/large-v3) the user already has cached before choosing which to load [^src1]. **WebLLM** (opt-in) and **wllama** (automatic) are also experimenting with COS [^src1].

## Related

- [Hugging Face](/ai-engineering/hugging-face.md) — publisher of Transformers.js and the models it serves
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Experimenting with the proposed Cross-Origin Storage API in Transformers.js](../../raw/web/web-experimenting-with-the-proposed-cross-origin-storage-api-in-dba1e8f0.md) — Hugging Face blog / Chrome team, 2026-06-28
