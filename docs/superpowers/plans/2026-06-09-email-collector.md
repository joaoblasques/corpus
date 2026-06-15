# Email Collector (collect-email skill) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/collect-email` Claude Code skill that captures starred Gmail messages into `raw/_inbox/` as normalized markdown, then de-stars and archives them — idempotently and safely.

**Architecture:** A thin skill (`.claude/skills/collect-email/SKILL.md`) drives Gmail via the claude.ai MCP connector and delegates all deterministic work — slugify, pointer detection, dedup, frontmatter, file writing — to a unit-tested Python module (`bin/collect_email.py`). The skill mutates Gmail (de-star/archive) only after the module confirms a durable write.

**Tech Stack:** Python 3.11 (stdlib only), pytest, the existing corpus `bin/` + `tests/` layout, and the `mcp__claude_ai_Gmail__*` tools.

---

## File Structure

- **Create** `bin/collect_email.py` — deterministic core + CLI. One responsibility: turn one fetched email into an idempotent, normalized file in `raw/_inbox/`.
- **Create** `tests/test_collect_email.py` — pytest unit tests for the core.
- **Create** `.claude/skills/collect-email/SKILL.md` — skill orchestration (Gmail MCP + delegation to the script).
- **Create** `raw/email/.gitkeep` — post-ingest channel directory.
- **Modify** `corpus/_config.md` — register the `email` channel.
- **Modify** `corpus/_log.md` — append a `config` log entry.

All Gmail access happens only in Task 8 (end-to-end test), with the user present.

---

### Task 1: Register the `email` channel

**Files:**
- Modify: `corpus/_config.md`
- Create: `raw/email/.gitkeep`
- Modify: `corpus/_log.md`

- [ ] **Step 1: Add the channel-labels row in `corpus/_config.md`**

In the "Channel labels (reference)" table, add a row under the existing ones:

```markdown
| `email` | `raw/email/` (collected via `/collect-email`) | — |
```

- [ ] **Step 2: Document the email-collection path**

In `corpus/_config.md`, immediately under that table, add:

```markdown
**Email collection**: starred Gmail messages are captured by the `/collect-email` skill into `raw/_inbox/` (channel `email`), then routed to `raw/email/` by the normal Branch A ingest flow. The skill writes a `gmail_message_id` frontmatter field used for dedup; it is not part of the §2 source-stamp spec.
```

- [ ] **Step 3: Create the channel directory**

Run:
```bash
mkdir -p raw/email && touch raw/email/.gitkeep
```

- [ ] **Step 4: Append a config log entry to `corpus/_log.md`**

Append at the end of the file:

```markdown

## [2026-06-09] config | add email channel

- Added `email` channel → `raw/email/` to corpus/_config.md (channel-labels table + email-collection note).
- Created raw/email/ (with .gitkeep).
- Supports the /collect-email collector (sub-project B): captures starred Gmail into raw/_inbox/ (channel email), routed to raw/email/ by Branch A ingest.
```

- [ ] **Step 5: Verify lint still passes**

Run: `./bin/lint`
Expected: `Lint: 0 errors` (warnings unchanged).

- [ ] **Step 6: Commit**

```bash
git add corpus/_config.md corpus/_log.md raw/email/.gitkeep
git commit -m "config: register email channel for collect-email collector"
```

---

### Task 2: Module scaffold + `slugify`

**Files:**
- Create: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_collect_email.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_email as ce  # noqa: E402


def test_slugify_basic():
    assert ce.slugify("Hello World") == "hello-world"


def test_slugify_strips_punctuation_and_collapses():
    assert ce.slugify("Re: [Newsletter] AI & You!!") == "re-newsletter-ai-you"


def test_slugify_truncates_without_trailing_hyphen():
    out = ce.slugify("a" * 80, max_len=10)
    assert out == "a" * 10


def test_slugify_empty_is_untitled():
    assert ce.slugify("!!!") == "untitled"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'collect_email'` (file doesn't exist yet).

- [ ] **Step 3: Write minimal implementation**

Create `bin/collect_email.py`:

```python
#!/usr/bin/env python3
"""collect_email.py — deterministic core for the collect-email skill.

The skill fetches starred Gmail messages via MCP and, for each one, invokes
this script to idempotently write a normalized markdown file into raw/_inbox/.
Gmail mutation (de-star/archive) is performed by the skill only after this
script reports a successful write.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "email"]

URL_RE = re.compile(r"https?://[^\s)>\]]+")
POINTER_MAX_PROSE = 200  # non-URL chars below which a body is "just a link"


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(text) > max_len:
        text = text[:max_len].rstrip("-")
    return text or "untitled"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): module scaffold + slugify"
```

---

### Task 3: `detect_pointer`

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_collect_email.py`:

```python
def test_detect_pointer_true_for_bare_link():
    ok, url = ce.detect_pointer("Check this out: https://example.com/article")
    assert ok is True
    assert url == "https://example.com/article"


def test_detect_pointer_false_for_prose_newsletter():
    body = "Welcome to the weekly digest. " * 20 + "More at https://example.com"
    ok, url = ce.detect_pointer(body)
    assert ok is False
    assert url is None


def test_detect_pointer_false_when_no_url():
    ok, url = ce.detect_pointer("Just some text, no links here.")
    assert ok is False
    assert url is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: FAIL — `AttributeError: module 'collect_email' has no attribute 'detect_pointer'`.

- [ ] **Step 3: Write minimal implementation**

Append to `bin/collect_email.py`:

```python
def detect_pointer(body: str) -> tuple[bool, str | None]:
    """A body is a 'pointer' if it is dominated by a link (little other prose)."""
    urls = URL_RE.findall(body or "")
    if not urls:
        return False, None
    prose = URL_RE.sub("", body).strip()
    if len(prose) <= POINTER_MAX_PROSE:
        return True, urls[0]
    return False, None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: PASS (7 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): pointer detection"
```

---

### Task 4: `already_collected` (dedup)

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_collect_email.py`:

```python
def test_already_collected_finds_existing(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "email-2026-06-09-x.md").write_text(
        "---\ngmail_message_id: ABC123\n---\nbody\n", encoding="utf-8"
    )
    assert ce.already_collected("ABC123", [d]) is True


def test_already_collected_absent(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    assert ce.already_collected("NOPE", [d]) is False


def test_already_collected_ignores_missing_dirs(tmp_path):
    assert ce.already_collected("X", [tmp_path / "does-not-exist"]) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: FAIL — `AttributeError: ... 'already_collected'`.

- [ ] **Step 3: Write minimal implementation**

Append to `bin/collect_email.py`:

```python
def already_collected(message_id: str, search_dirs: list[Path] | None = None) -> bool:
    dirs = search_dirs if search_dirs is not None else DEDUP_DIRS
    needle = f"gmail_message_id: {message_id}"
    for d in dirs:
        if not d.exists():
            continue
        for md in d.glob("*.md"):
            try:
                if needle in md.read_text(encoding="utf-8"):
                    return True
            except (OSError, UnicodeDecodeError):
                continue
    return False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: PASS (10 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): dedup by gmail_message_id"
```

---

### Task 5: `yaml_scalar`, `build_document`, `target_filename`

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_collect_email.py`:

```python
def _meta(**over):
    base = {
        "gmail_message_id": "ABC123",
        "from": "Jane Doe <jane@example.com>",
        "subject": "Hello: a test",
        "date_received": "2026-06-09",
        "collected_at": "2026-06-09",
        "pointer": False,
        "url": None,
    }
    base.update(over)
    return base


def test_yaml_scalar_quotes_colon():
    assert ce.yaml_scalar("Hello: world") == '"Hello: world"'


def test_yaml_scalar_plain_passthrough():
    assert ce.yaml_scalar("just text") == "just text"


def test_build_document_has_frontmatter_and_body():
    doc = ce.build_document(_meta(), "The body text.")
    assert doc.startswith("---\n")
    assert "channel: email" in doc
    assert "gmail_message_id: ABC123" in doc
    assert 'subject: "Hello: a test"' in doc
    assert "pointer: false" in doc
    assert doc.rstrip().endswith("The body text.")


def test_build_document_includes_url_when_pointer():
    doc = ce.build_document(_meta(pointer=True, url="https://x.com"), "https://x.com")
    assert "url: https://x.com" in doc
    assert "pointer: true" in doc


def test_target_filename_collision_appends_id(tmp_path):
    first = ce.target_filename("2026-06-09", "Hello: a test", "ABC123", tmp_path)
    first.write_text("x", encoding="utf-8")
    second = ce.target_filename("2026-06-09", "Hello: a test", "ZZZ999", tmp_path)
    assert first != second
    assert "email-2026-06-09-hello-a-test" in first.name
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: FAIL — `AttributeError: ... 'yaml_scalar'`.

- [ ] **Step 3: Write minimal implementation**

Append to `bin/collect_email.py`:

```python
def yaml_scalar(value: str) -> str:
    value = (value or "").replace("\n", " ").strip()
    needs_quote = (
        value == ""
        or value[:1] in "-?:#&*!|>%@`"
        or bool(re.search(r'[:#\[\]{}",]', value))
    )
    if needs_quote:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def build_document(meta: dict, body: str) -> str:
    lines = [
        "---",
        "channel: email",
        "source: gmail",
        f"gmail_message_id: {meta['gmail_message_id']}",
        f"from: {yaml_scalar(meta['from'])}",
        f"subject: {yaml_scalar(meta['subject'])}",
        f"date_received: {meta['date_received']}",
    ]
    if meta.get("url"):
        lines.append(f"url: {meta['url']}")
    lines.append(f"pointer: {'true' if meta.get('pointer') else 'false'}")
    lines.append(f"collected_at: {meta['collected_at']}")
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    return "\n".join(lines)


def target_filename(date_received: str, subject: str, message_id: str,
                    inbox: Path | None = None) -> Path:
    base = inbox if inbox is not None else INBOX
    slug = slugify(subject)
    candidate = base / f"email-{date_received}-{slug}.md"
    if candidate.exists():
        suffix = re.sub(r"[^a-z0-9]+", "", message_id.lower())[:8] or "x"
        candidate = base / f"email-{date_received}-{slug}-{suffix}.md"
    return candidate
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: PASS (15 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): document builder + filename"
```

---

### Task 6: `write_collected` orchestrator + CLI

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_collect_email.py`:

```python
def test_write_collected_writes_file(tmp_path):
    inbox = tmp_path / "_inbox"
    res = ce.write_collected(_meta(), "Newsletter body here.", inbox=inbox, dedup_dirs=[inbox])
    assert res["status"] == "written"
    p = Path(res["path"])
    assert p.exists()
    assert "gmail_message_id: ABC123" in p.read_text(encoding="utf-8")


def test_write_collected_dedup_skips(tmp_path):
    inbox = tmp_path / "_inbox"
    ce.write_collected(_meta(), "body", inbox=inbox, dedup_dirs=[inbox])
    res2 = ce.write_collected(_meta(), "body", inbox=inbox, dedup_dirs=[inbox])
    assert res2["status"] == "duplicate"
    assert len(list(inbox.glob("*.md"))) == 1


def test_write_collected_sets_pointer(tmp_path):
    inbox = tmp_path / "_inbox"
    res = ce.write_collected(
        _meta(gmail_message_id="PTR1"), "https://example.com/x", inbox=inbox, dedup_dirs=[inbox]
    )
    assert res["pointer"] is True
    assert res["url"] == "https://example.com/x"


def test_cli_writes_and_prints_json(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(ce, "INBOX", inbox)
    monkeypatch.setattr(ce, "DEDUP_DIRS", [inbox])
    body_file = tmp_path / "body.md"
    body_file.write_text("Hello body", encoding="utf-8")
    rc = ce.main([
        "--message-id", "CLI1", "--from", "a@b.com", "--subject", "Subj",
        "--date", "2026-06-09", "--collected-at", "2026-06-09",
        "--body-file", str(body_file),
    ])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "written"
    assert Path(out["path"]).exists()
```

Add `import json` at the top of the test file (below the existing imports):

```python
import json
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: FAIL — `AttributeError: ... 'write_collected'`.

- [ ] **Step 3: Write minimal implementation**

Append to `bin/collect_email.py`:

```python
def write_collected(meta: dict, body: str, inbox: Path | None = None,
                    dedup_dirs: list[Path] | None = None) -> dict:
    if already_collected(meta["gmail_message_id"], dedup_dirs):
        return {"status": "duplicate", "gmail_message_id": meta["gmail_message_id"]}
    pointer, url = detect_pointer(body)
    meta = {**meta, "pointer": pointer, "url": url}
    base = inbox if inbox is not None else INBOX
    base.mkdir(parents=True, exist_ok=True)
    path = target_filename(meta["date_received"], meta["subject"],
                           meta["gmail_message_id"], base)
    path.write_text(build_document(meta, body), encoding="utf-8")
    return {"status": "written", "path": str(path), "pointer": pointer, "url": url}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Write a starred Gmail message into raw/_inbox/ (idempotent)."
    )
    p.add_argument("--message-id", required=True)
    p.add_argument("--from", dest="sender", required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--date", dest="date_received", required=True)
    p.add_argument("--collected-at", required=True)
    p.add_argument("--body-file", required=True)
    args = p.parse_args(argv)
    body = Path(args.body_file).read_text(encoding="utf-8")
    meta = {
        "gmail_message_id": args.message_id,
        "from": args.sender,
        "subject": args.subject,
        "date_received": args.date_received,
        "collected_at": args.collected_at,
    }
    print(json.dumps(write_collected(meta, body)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the full test module to verify it passes**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: PASS (19 passed).

- [ ] **Step 5: Verify the whole suite + lint are green**

Run: `python3 -m pytest tests/ -q && ./bin/lint`
Expected: all tests pass; `Lint: 0 errors`.

- [ ] **Step 6: Commit**

```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): write orchestrator + CLI"
```

---

### Task 7: Author the `collect-email` skill

**Files:**
- Create: `.claude/skills/collect-email/SKILL.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/skills/collect-email/SKILL.md` with exactly this content:

````markdown
---
name: collect-email
description: Collect starred Gmail messages into the corpus raw/_inbox/ as markdown, then de-star and archive them. Run manually or via /loop. Use when the user wants to pull starred emails into the corpus pipeline.
---

# Collect Email

Capture every **starred** Gmail message into `raw/_inbox/` as a normalized markdown
file, then de-star and archive it. Collection only — never ingest into `corpus/`.

## Safety rules (non-negotiable)
- De-star/archive an email **only after** its markdown file is confirmed written.
- On any failure for one email: skip it, leave it starred, continue with the rest.
- Write only to `raw/_inbox/`. Never touch `corpus/` or the vault.

## Procedure

1. Find starred mail: call `mcp__claude_ai_Gmail__search_threads` with query `is:starred`.
   If none, report "0 starred" and stop.
2. For each thread, call `mcp__claude_ai_Gmail__get_thread` and identify the
   **starred message(s)** within it. Process each starred message:
   a. Extract: `message_id`, `from` (display + address), `subject`,
      `date_received` (YYYY-MM-DD), and the body as plain text/markdown.
   b. Write the body to a temp file, e.g. `/tmp/collect-email-body.md`.
   c. Run the deterministic writer (it handles dedup, pointer detection,
      frontmatter, filename, and the write):
      ```bash
      python3 bin/collect_email.py \
        --message-id "<message_id>" \
        --from "<from>" \
        --subject "<subject>" \
        --date "<date_received>" \
        --collected-at "$(date +%Y-%m-%d)" \
        --body-file /tmp/collect-email-body.md
      ```
   d. Parse the JSON it prints:
      - `{"status":"written", "path":...}` → confirm the file exists, then go to step 3.
      - `{"status":"duplicate"}` → already collected on a prior run; go straight to
        step 3 to finish archiving (idempotent retry).
      - anything else / error → record as failed, leave the email starred, skip step 3.
3. De-star and archive (only reached on written/duplicate):
   - `mcp__claude_ai_Gmail__unlabel_message` removing `STARRED`.
   - `mcp__claude_ai_Gmail__unlabel_message` removing `INBOX` (archive).
4. Report a one-line tally: `<N> starred found · <M> collected · <K> skipped (dup) · <F> failed (left starred)`, then list the created file paths.

## Notes
- This skill does NOT follow links inside emails (pointer emails are captured with
  their URL recorded in frontmatter; following is a future enhancement).
- Run via `/loop <interval> /collect-email` to probe on a cadence within an active
  Claude Code session (the Gmail connector is available there).
- After collection, run the normal corpus ingest on `raw/_inbox/` when you choose;
  ingest then routes files to `raw/email/`.
````

- [ ] **Step 2: Sanity-check the deterministic writer end-to-end (no Gmail)**

Run:
```bash
printf 'A short test body.\n' > /tmp/collect-email-body.md
python3 bin/collect_email.py --message-id "SMOKE1" --from "t@e.com" \
  --subject "Smoke test" --date 2026-06-09 --collected-at 2026-06-09 \
  --body-file /tmp/collect-email-body.md
ls raw/_inbox/
```
Expected: prints `{"status": "written", "path": "raw/_inbox/email-2026-06-09-smoke-test.md", ...}` and the file appears in `raw/_inbox/`.

- [ ] **Step 3: Remove the smoke-test artifact**

Run: `rm -f raw/_inbox/email-2026-06-09-smoke-test.md`
(Confirm only the smoke file is removed; leave any real inbox files untouched.)

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/collect-email/SKILL.md
git commit -m "feat(collect-email): skill orchestration"
```

---

### Task 8: End-to-end test with the user (manual)

**Files:** none (live verification)

> This is the only task that touches Gmail. Do it interactively with the user.

- [ ] **Step 1: Confirm the connector**

Verify `mcp__claude_ai_Gmail__search_threads`, `get_thread`, and `unlabel_message`
are available in the session. If not, stop and report (see Risks in the spec).

- [ ] **Step 2: Ask the user to seed test data**

Ask the user to star 2–3 real emails: at least one plain newsletter (body-is-content)
and one that is essentially a single link (pointer).

- [ ] **Step 3: Run the skill once**

Invoke `/collect-email`. Observe the run summary.

- [ ] **Step 4: Verify outputs**

- `raw/_inbox/` contains one markdown file per starred email, with correct
  frontmatter; `pointer`/`url` set correctly on the link email.
- The starred emails are now de-starred and archived in Gmail.
- The run summary tally is accurate.

- [ ] **Step 5: Verify idempotency**

Run `/collect-email` again immediately.
Expected: `0 collected` (all deduped), nothing new written, no Gmail changes.

- [ ] **Step 6: Report results to the user**

Summarize what worked, any extraction-fidelity issues on HTML-heavy emails, and
confirm readiness to (a) wire `/loop`, (b) start collector #2 (Obsidian), or
(c) build v1.1 link-following.

---

## Self-Review

**1. Spec coverage:**
- Trigger = starred → Task 7 step 1 (`is:starred`). ✅
- Write to `raw/_inbox/` as normalized markdown → Tasks 5–6 + format. ✅
- De-star + archive after durable write → Task 7 steps 2d→3; ordering enforced. ✅
- Idempotency via `gmail_message_id` → Task 4 + Task 6 dup test. ✅
- Per-email isolation + reporting → Task 7 steps 2/4. ✅
- Raw file format (all frontmatter fields) → Task 5 `build_document`. ✅
- Pointer detection v1 (record, don't follow) → Task 3; Task 7 Notes. ✅
- `email` channel config → Task 1. ✅
- Testing plan (seed, run, verify, re-run dedup) → Task 8. ✅
- Non-goals (link-following, Obsidian, headless, attachments) → not implemented, noted. ✅

**2. Placeholder scan:** No TBD/TODO; every code step shows complete code; every command has expected output. ✅

**3. Type consistency:** `slugify`, `detect_pointer`, `already_collected`, `yaml_scalar`, `build_document`, `target_filename`, `write_collected`, `main` — names and signatures are consistent across tasks and the CLI/skill invocation. The skill calls `bin/collect_email.py` with the exact flags `main()` defines. ✅

---
```
