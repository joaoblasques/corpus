---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-02-d4vinci-scrapling-an-adaptive-web-scraping-framework-that-ha.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/web/github-d4vinci-scrapling-an-adaptive-web-scraping-framework.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - Scrapling
  - web scraping
  - adaptive scraping
  - scraping framework
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-07-13
---

# Scrapling (Adaptive Web Scraping)

**TL;DR**: Scrapling is an adaptive Python web-scraping framework that "handles everything from a single request to a full-scale crawl" [^src2]. Its AI-engineering relevance is a built-in **MCP server** that extracts targeted page content before passing it to an LLM (Claude/Cursor/etc.), thereby "speeding up operations and reducing costs by minimizing token usage" [^src2]. The parser survives site redesigns by relocating elements via similarity algorithms; fetchers bypass Cloudflare Turnstile out of the box [^src2].

## Why it matters for agents

The MCP server makes Scrapling a retrieval pre-processor for LLM agents: instead of receiving raw HTML (token-expensive and noisy), the model receives clean extracted content [^src2]. This is a [context-engineering](/ai-engineering/context-engineering.md) pattern applied at the retrieval edge — minimizing what enters the context window. Any MCP-compatible client (Claude Code, Cursor) can invoke scraping on demand through this interface [^src2].

The CLI extends this to zero-code extraction: `scrapling extract get '<url>' output.md` writes a Markdown representation of a page's body content without writing any Python [^src2]. Paired with CSS selectors or stealthy fetchers, it can feed cleaned pages directly into a corpus or RAG pipeline. Supported output formats are `.txt` (text content), `.md` (Markdown), and `.html` (raw HTML) [^src2].

An interactive IPython-based scraping shell (`scrapling shell`) is also available, with shortcuts, curl-to-Scrapling conversion, and in-browser result preview — aimed at rapid script development [^src2].

## Fetcher tiers

Three fetcher classes serve different threat levels [^src2]:

| Class | Mechanism | Use case |
|---|---|---|
| `Fetcher` / `AsyncFetcher` | Fast HTTP; TLS-fingerprint impersonation (`impersonate='chrome'`), HTTP/3, stealthy headers | Lightly-protected or open sites |
| `DynamicFetcher` / `DynamicSession` | Full browser automation via Playwright Chromium or Google Chrome | JavaScript-heavy, dynamic sites |
| `StealthyFetcher` / `StealthySession` | Advanced fingerprint spoofing; bypasses all types of Cloudflare Turnstile/Interstitial | Sites with aggressive anti-bot protection |

All fetcher classes support session variants (`FetcherSession`, `StealthySession`, `DynamicSession`) for cookie and state persistence across requests, as well as full async (`AsyncStealthySession`, `AsyncDynamicSession`) [^src2]. Domain and ad blocking (~3,500 known ad/tracker domains) is available in browser-based fetchers, along with optional DNS-over-HTTPS to prevent DNS leaks when using proxies [^src2].

## Adaptive element selection

The parser's standout feature is element relocation after site restructuring. Setting `auto_save=True` on first scrape records element fingerprints; on subsequent runs, passing `adaptive=True` uses "intelligent similarity algorithms" to find elements even when the page structure has changed [^src2]. Auto selector generation (CSS/XPath) for any element is also available [^src2].

Selection methods span CSS selectors, XPath, BeautifulSoup-style `find_all`, text-based search, regex search, and DOM traversal (parent, sibling, child, `below_elements()`, `find_similar()`) [^src2].

## Spider framework

The spider API mirrors Scrapy: define `start_urls`, an async `parse()` callback, and `Request`/`Response` objects [^src2]. Key operational features [^src2]:

- **Concurrent crawling** — configurable concurrency limits, per-domain throttling, download delays.
- **Multi-session routing** — HTTP and stealthy browser sessions unified in one spider, routed by session ID per request.
- **Pause & resume** — checkpoint-based persistence (`crawldir` arg); `Ctrl+C` saves state, restart resumes from last checkpoint.
- **Streaming** — `async for item in spider.stream()` emits items as they arrive with real-time stats.
- **Blocked request detection** — automatic retry with customizable logic.
- **Robots.txt compliance** — optional `robots_txt_obey` flag respecting `Disallow`, `Crawl-delay`, and `Request-rate` with per-domain caching.
- **Development mode** — cache responses on first run, replay on subsequent runs for parse-logic iteration without re-hitting servers.
- **Export** — built-in JSON/JSONL via `result.items.to_json()` / `result.items.to_jsonl()`.

## Performance

Parser benchmarks against other Python libraries (averages of 100+ runs) [^src2]:

| Library | Time (ms) | vs Scrapling |
|---|---|---|
| Scrapling | 2.02 | 1.0× |
| Parsel/Scrapy | 2.04 | 1.01× |
| Raw lxml | 2.54 | 1.26× |
| PyQuery | 24.17 | ~12× |
| BS4 with lxml | 1,584 | ~784× |
| BS4 with html5lib | 3,392 | ~1,679× |

Adaptive element finding: Scrapling at 2.39 ms vs. AutoScraper at 12.45 ms (~5.2× slower) [^src2].

The source also claims "10× faster than the standard library" JSON serialization and a minimal memory footprint via lazy loading [^src2].

## Installation

Requires Python 3.10+. Packages are split by feature surface [^src2]:

```
pip install scrapling                  # parser only (no fetchers or CLI)
pip install "scrapling[fetchers]"      # + fetchers; then: scrapling install  (downloads browsers)
pip install "scrapling[ai]"            # + MCP server
pip install "scrapling[shell]"         # + CLI extract + IPython shell
pip install "scrapling[all]"           # everything
```

A pre-built Docker image with all extras and browsers is available (`pyd4vinci/scrapling` on DockerHub; auto-built from `main` via GitHub Actions) [^src2].

## Provenance & license

Author: Karim Shoair. Initial release: 2024. 92% test coverage; full type hints with PyRight + MyPy on every change; BSD-3-Clause license [^src2]. The source cautions: "This library is provided for educational and research purposes only" — users must comply with local/international data scraping laws and respect `robots.txt` [^src2].

> Gotcha: the base `pip install scrapling` does **not** include fetchers or CLI; importing from `scrapling.fetchers` or `scrapling.spiders` raises `ModuleNotFoundError` without the extras install [^src2].

## See also

- [MCP](/ai-engineering/mcp.md) — the protocol Scrapling exposes for agent-driven scraping
- [Context Engineering](/ai-engineering/context-engineering.md) — extract-before-LLM as a token-minimizing pattern
- [RAG](/ai-engineering/rag.md) — scraped/cleaned pages as a retrieval source

---

[^src1]: [D4Vinci/Scrapling: an adaptive Web Scraping framework](../../raw/email/email-2026-05-02-d4vinci-scrapling-an-adaptive-web-scraping-framework-that-ha.md) — email pointer
[^src2]: [D4Vinci/Scrapling (README)](../../raw/web/github-d4vinci-scrapling-an-adaptive-web-scraping-framework.md) — GitHub
