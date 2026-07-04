---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-pp-ocrv6-on-hugging-face-50-language-ocr-from-1-5m-to-34-5m-493a508e.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - PP-OCRv6
  - PaddleOCR
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-03
updated: 2026-07-03
---

# PP-OCRv6

**TL;DR.** PP-OCRv6 is the latest generation of PaddleOCR's (PaddlePaddle's OCR toolkit) universal OCR model family — three size tiers (1.5M/7.7M/34.5M parameters) covering 50 languages, targeting document, screenshot, multilingual, digital-display, industrial-label, and scene-text recognition [^src1]. It is a specialized (non-VLM) OCR model, positioned as a small, deployment-flexible alternative in an era where general-purpose vision-language models are increasingly used for text extraction [^src1].

## Model tiers

| Model | Params | Detection Hmean | Recognition accuracy | Typical use |
|---|---|---|---|---|
| PP-OCRv6_tiny | 1.5M | 80.6% | 73.5% | Edge devices, lightweight local OCR, latency-sensitive demos |
| PP-OCRv6_small | 7.7M | 84.1% | 81.3% | Mobile, desktop, balanced OCR services, multilingual at lower compute cost |
| PP-OCRv6_medium | 34.5M | 86.2% | 83.2% | Accuracy-oriented, server-side pipelines, industrial OCR, document ingestion |

All three tiers share **PPLCNetV4** as a unified backbone for both detection and recognition — they are variants of one architectural family, not unrelated models [^src1]. The medium and small tiers support 50 languages (Simplified Chinese, Traditional Chinese, English, Japanese, 46 Latin-script languages), reducing the need for separate per-language OCR models [^src1].

On PaddleOCR's in-house multi-scenario benchmark, PP-OCRv6_medium improves on PP-OCRv5_server by +4.6pp detection Hmean and +5.1pp recognition accuracy [^src1].

## Architecture changes from PP-OCRv5

- **Detection**: **RepLKFPN**, a lightweight large-kernel feature pyramid network for multi-scale text detection, targeting small/dense/rotated/low-resolution text or text embedded in complex backgrounds — detection quality directly bounds recognition quality since poor crops feed the recognizer [^src1].
- **Recognition**: **EncoderWithLightSVTR**, combining local context modeling with global attention — aimed at multilingual text, screen text, industrial characters, special symbols, dense text, and noisy image regions [^src1].

## Usage

```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
result = ocr.predict("path/or/url/to/image.png")
for res in result:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")
```

Output is available as visualization images and structured JSON, feeding downstream document parsing, search, extraction, RAG, analytics, or agent workflows [^src1].

## Inference backends

PaddleOCR 3.7 exposes a unified inference-engine interface (`engine=` parameter) across three backends: **Transformers** (Hugging Face/PyTorch-oriented, for Hub users), **ONNX Runtime** (portable, for ONNX-based deployments), and **Paddle Inference** (native format, default) [^src1]. All three run the same PP-OCRv6 model family, so the runtime choice doesn't fragment which model version is available [^src1].

## Related

- [Hugging Face](/ai-engineering/hugging-face.md) — hosts the PP-OCRv6 model collection and Space demo
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [PP-OCRv6 on Hugging Face: 50-Language OCR from 1.5M to 34.5M Parameters](../../raw/web/web-pp-ocrv6-on-hugging-face-50-language-ocr-from-1-5m-to-34-5m-493a508e.md) — Hugging Face blog (PaddlePaddle), 2026-06-28
