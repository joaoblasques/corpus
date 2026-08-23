---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-count-the-number-of-safari-tabs-35a54d60.md
    channel: web
    ingested_at: 2026-08-23
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - simon-willison
  - til
  - applescript
created: 2026-08-23
updated: 2026-08-23
---

# TIL: Count Safari Tabs via AppleScript (Simon Willison, June 2026)

**TL;DR**: A Simon Willison TIL post showing a one-liner AppleScript command to count Safari tabs across all windows.

Command:

```
osascript -e 'tell application "Safari" to count tabs of every window'
```

Returns a list of per-window tab counts. Posted June 29, 2026 on simonwillison.net/til/.

## See also

- [Simon Willison](/ai-engineering/simon-willison.md) — author
