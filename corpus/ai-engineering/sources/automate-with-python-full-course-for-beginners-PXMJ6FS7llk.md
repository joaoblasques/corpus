---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md
    channel: youtube
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - youtube-quick-intake
created: 2026-07-02
updated: 2026-07-19
provisional: false
youtube_video_id: PXMJ6FS7llk
url: https://youtu.be/PXMJ6FS7llk
channel_name: freeCodeCamp.org
playlist: Python
published: 2022-06-20
transcript_status: ok
---

# Automate with Python – Full Course for Beginners

> **Quick intake** (YouTube · freeCodeCamp.org · playlist _Python_). [watch on YouTube](https://youtu.be/PXMJ6FS7llk) · [transcript](../../../raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md)

**TL;DR:** A beginner-focused freeCodeCamp course by Frank Andrade (data scientist) covering Python automation across a series of projects — table extraction, CSV scraping from URLs, Excel report generation, SMS sending, and website interaction.[^1]

---

## Course structure

The course is project-based, teaching Python automation through concrete tasks rather than abstract instruction.[^1] Instructor Frank Andrade provides accompanying code and an automation cheat sheet linked in the video description.[^1]

Automation tasks demonstrated include:

- Creating Excel reports
- Sending text messages
- Extracting tables from websites
- Interacting with websites
- Downloading CSV files from URLs[^1]

---

## Table extraction with pandas

The primary technique introduced is `pd.read_html(url)`, which returns a list of all HTML tables found at a given URL.[^2]

> "we only need to use the pandas library" to extract all tables from a Wikipedia page.[^2]

Workflow:

1. Install: `pip install pandas`
2. Import: `import pandas as pd`
3. Call `pd.read_html("<url>")` → returns a list of DataFrames, one per table
4. Index into the list (e.g., `simpsons[1]`) to access a specific table[^3]

Applied to a Simpsons episode list on Wikipedia, the call returned 23 tables; indexing to position 1 retrieved Season 1 episode data.[^3]

---

## CSV extraction from URLs

`pd.read_csv()` accepts a remote URL in place of a local file path, enabling direct download of CSV files from the web without manual browser interaction.[^4]

> "instead of writing the path of the file in your computer, in this case, we're going to write that link of the file"[^4]

Combined with a `for` loop, this pattern can batch-download all CSV files listed on a page — demonstrated against a football-match results website containing Premier League and other league data.[^5]

---

## Key patterns

| Pattern | Tool | Use case |
|---|---|---|
| HTML table extraction | `pd.read_html(url)` | Wikipedia tables, structured HTML pages |
| Remote CSV download | `pd.read_csv(url)` | Direct-link CSV files from data sites |
| Batch download | `for` loop + `pd.read_csv` | Bulk automation across many files |

---

[^1]: [transcript](../../../raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md) — [00:00](https://youtu.be/PXMJ6FS7llk?t=0)
[^2]: [transcript](../../../raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md) — [00:29](https://youtu.be/PXMJ6FS7llk?t=29)
[^3]: [transcript](../../../raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md) — [01:52](https://youtu.be/PXMJ6FS7llk?t=112)
[^4]: [transcript](../../../raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md) — [04:37](https://youtu.be/PXMJ6FS7llk?t=277)
[^5]: [transcript](../../../raw/youtube/youtube-PXMJ6FS7llk-automate-with-python-full-course-for-beginners.md) — [04:07](https://youtu.be/PXMJ6FS7llk?t=247)
