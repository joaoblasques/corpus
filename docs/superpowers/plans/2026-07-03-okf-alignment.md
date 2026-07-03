# OKF Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `corpus/` a conformant Google Open Knowledge Format (OKF) v0.1 bundle — reserved `index.md`/`log.md`, plain root-relative markdown links (no wikilinks), `type` required, `okf_version` stamp — with a validator so it stays conformant.

**Architecture:** Build a conformance validator first (so the migration is verifiable), then a migration script (wikilink rewriter + reserved-file conversion), run it as one reviewable commit, update the tooling that writes the corpus to emit OKF, wire the validator into lint + the nightly, and update the schema doc.

**Tech Stack:** Python 3 (`/usr/local/bin/python3`), pytest, regex. No new deps.

## Global Constraints

- OKF required frontmatter field: **`type`** (non-empty). All 745 concept docs already have it.
- Reserved filenames (exactly two): **`index.md`**, **`log.md`**. All other `.md` are concept docs.
- `index.md`: **no frontmatter except the bundle-root `index.md` which carries `okf_version: "0.1"`**; body = `# Section` headings + `* [Title](/path.md) - desc` bullets.
- `log.md`: **newest-first**, `## YYYY-MM-DD` date-group headings, prose entries.
- Cross-links: **plain markdown, root-relative absolute** — `[Text](/domain/page.md)`. **No `[[wikilinks]]`.** Broken links tolerated.
- Conformance (3 rules): every non-reserved `.md` has parseable YAML frontmatter; non-empty `type`; reserved files follow their format.
- `okf_version` value is the exact string `"0.1"`, only in root `corpus/index.md` frontmatter.
- Bundle boundary = `corpus/`. Never touch `raw/`, `bin/` output paths beyond what's specified, or the vault.
- Migration must be idempotent, support `--dry-run`, and never lose log entries.

---

### Task 1: OKF conformance validator (`bin/okf_lint.py`)

Build the checker first so every later step is verifiable.

**Files:**
- Create: `bin/okf_lint.py`
- Test: `tests/test_okf_lint.py`

**Interfaces:**
- Produces:
  - `parse_frontmatter(text: str) -> dict | None` — returns the parsed YAML frontmatter dict, `{}` if the block is empty, or `None` if there is no `---`-delimited block or it doesn't parse.
  - `check_concept(path: Path, text: str) -> list[str]` — violation strings for a non-reserved doc (missing/unparseable frontmatter; missing/empty `type`).
  - `check_index(path: Path, text: str, is_root: bool) -> list[str]` — root index.md may have only `okf_version`; non-root index.md must have no frontmatter.
  - `check_log(path: Path, text: str) -> list[str]` — date headings must match `^## \d{4}-\d{2}-\d{2}$`.
  - `lint_bundle(root: Path) -> dict` — `{"violations": [...], "checked": N, "concepts": N}` over the tree; reserved files routed to check_index/check_log, others to check_concept.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_okf_lint.py
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
ok = importlib.import_module("okf_lint")


def test_parse_frontmatter_variants():
    assert ok.parse_frontmatter("---\ntype: entity\n---\nbody") == {"type": "entity"}
    assert ok.parse_frontmatter("no frontmatter here") is None
    assert ok.parse_frontmatter("---\n---\nbody") == {}


def test_concept_needs_nonempty_type():
    assert ok.check_concept(Path("a.md"), "---\ntype: entity\n---\nx") == []
    assert ok.check_concept(Path("a.md"), "no fm") != []            # missing frontmatter
    assert ok.check_concept(Path("a.md"), "---\ntitle: x\n---\ny") != []  # no type
    assert ok.check_concept(Path("a.md"), "---\ntype: ''\n---\ny") != []  # empty type


def test_root_index_allows_only_okf_version():
    assert ok.check_index(Path("index.md"), '---\nokf_version: "0.1"\n---\n# D\n', True) == []
    assert ok.check_index(Path("index.md"), "# D\n* [a](/a.md)\n", True) == []   # no fm is fine
    assert ok.check_index(Path("d/index.md"), "---\nokf_version: \"0.1\"\n---\n", False) != []  # non-root fm forbidden


def test_log_date_headings_iso():
    assert ok.check_log(Path("log.md"), "# Log\n## 2026-07-03\n* x\n") == []
    assert ok.check_log(Path("log.md"), "# Log\n## [2026-07-03 10:00] ingest\n") != []  # bracketed = bad


def test_lint_bundle_tolerates_broken_links_and_unknown_keys(tmp_path):
    (tmp_path / "a.md").write_text("---\ntype: entity\nweird_key: 1\n---\n[x](/missing.md)\n")
    (tmp_path / "index.md").write_text('---\nokf_version: "0.1"\n---\n# S\n* [a](/a.md) - d\n')
    r = ok.lint_bundle(tmp_path)
    assert r["violations"] == []          # unknown keys + broken links are OKF-legal
    assert r["concepts"] == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_okf_lint.py -v -p no:cacheprovider`
Expected: FAIL — `ModuleNotFoundError: No module named 'okf_lint'`

- [ ] **Step 3: Write minimal implementation**

```python
# bin/okf_lint.py
#!/usr/bin/env python3
"""okf_lint.py — check that corpus/ is a conformant OKF v0.1 bundle.

Three rules (SPEC §9): every non-reserved .md has parseable YAML frontmatter; every
frontmatter has a non-empty `type`; reserved files (index.md/log.md) follow their format.
Consumers MUST tolerate broken links, unknown keys, unknown type values, missing optional
fields — so this reports ONLY the three structural rules, nothing else."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "corpus"
RESERVED = {"index.md", "log.md"}
_FM = re.compile(r"^---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str):
    m = _FM.match(text)
    if not m:
        return None
    import yaml
    try:
        data = yaml.safe_load(m.group(1))
    except Exception:  # noqa: BLE001
        return None
    return data if isinstance(data, dict) else ({} if data is None else None)


def check_concept(path: Path, text: str) -> list[str]:
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{path}: no parseable YAML frontmatter"]
    t = fm.get("type")
    if not (isinstance(t, str) and t.strip()):
        return [f"{path}: missing/empty required `type` field"]
    return []


def check_index(path: Path, text: str, is_root: bool) -> list[str]:
    fm = parse_frontmatter(text)
    if fm is None:
        return []  # index.md with no frontmatter is valid
    if not is_root:
        return [f"{path}: non-root index.md must not have frontmatter"]
    extra = set(fm) - {"okf_version"}
    return [f"{path}: root index.md frontmatter may only contain okf_version (found {extra})"] if extra else []


def check_log(path: Path, text: str) -> list[str]:
    out = []
    for ln in text.splitlines():
        if ln.startswith("## ") and not re.match(r"^## \d{4}-\d{2}-\d{2}$", ln):
            out.append(f"{path}: log heading not ISO date group: {ln!r}")
    return out


def lint_bundle(root: Path) -> dict:
    viol, checked, concepts = [], 0, 0
    for p in sorted(root.rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        checked += 1
        if p.name == "index.md":
            viol += check_index(p, text, is_root=(p.parent == root))
        elif p.name == "log.md":
            viol += check_log(p, text)
        else:
            concepts += 1
            viol += check_concept(p, text)
    return {"violations": viol, "checked": checked, "concepts": concepts}


def main(argv=None) -> int:
    import json
    r = lint_bundle(BUNDLE)
    print(json.dumps({"checked": r["checked"], "concepts": r["concepts"],
                      "violations": len(r["violations"]), "detail": r["violations"][:50]}, indent=2))
    return 1 if r["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_okf_lint.py -v -p no:cacheprovider`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add bin/okf_lint.py tests/test_okf_lint.py
git commit -m "feat(okf): conformance validator (bin/okf_lint.py) — the 3 rules, tolerant of broken links/unknown keys"
```

---

### Task 2: Wikilink → markdown-link rewriter (`bin/okf_migrate.py`)

The highest-risk piece (4,293 links). Pure function, fully TDD'd, before any file is touched.

**Files:**
- Create: `bin/okf_migrate.py`
- Test: `tests/test_okf_migrate.py`

**Interfaces:**
- Produces:
  - `rewrite_wikilinks(text: str, resolve=None) -> tuple[str, list[str]]` — replace every
    `[[target|display]]` / `[[target]]` with `[display](/target.md)`; returns `(new_text,
    unresolved)`. `target` already containing a `/` is used as-is (root-relative). A bare target
    (no `/`) is passed to `resolve(target)`; if that returns a path it's used, else the link
    becomes plain `display` text and `target` is appended to `unresolved`. **Fenced code blocks
    (``` ... ```) are skipped.** A `[[target]]` with no display uses the last path segment,
    title-cased-from-kebab, as display.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_okf_migrate.py
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
mig = importlib.import_module("okf_migrate")


def test_piped_wikilink():
    out, un = mig.rewrite_wikilinks("see [[ai-engineering/claude-code|Claude Code]] now")
    assert out == "see [Claude Code](/ai-engineering/claude-code.md) now"
    assert un == []


def test_unpiped_wikilink_titlecases_last_segment():
    out, _ = mig.rewrite_wikilinks("[[ai-engineering/context-window-management]]")
    assert out == "[Context Window Management](/ai-engineering/context-window-management.md)"


def test_bare_target_resolved_via_callback():
    out, un = mig.rewrite_wikilinks("[[anthropic|Anthropic]]",
                                    resolve=lambda t: "ai-engineering/anthropic")
    assert out == "[Anthropic](/ai-engineering/anthropic.md)"
    assert un == []


def test_bare_target_unresolved_becomes_plain_text():
    out, un = mig.rewrite_wikilinks("[[mystery|Mystery]]", resolve=lambda t: None)
    assert out == "Mystery"
    assert un == ["mystery"]


def test_code_fences_are_skipped():
    src = "real [[a/b|B]]\n```\ncode [[c/d|D]] literal\n```\nmore [[e/f|F]]"
    out, _ = mig.rewrite_wikilinks(src)
    assert "[B](/a/b.md)" in out and "[F](/e/f.md)" in out
    assert "[[c/d|D]]" in out            # untouched inside the fence


def test_idempotent_on_plain_markdown_links():
    src = "already [markdown](/a/b.md) link"
    out, _ = mig.rewrite_wikilinks(src)
    assert out == src
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_okf_migrate.py -v -p no:cacheprovider`
Expected: FAIL — `ModuleNotFoundError: No module named 'okf_migrate'`

- [ ] **Step 3: Write minimal implementation**

```python
# bin/okf_migrate.py
#!/usr/bin/env python3
"""okf_migrate.py — one-time migration of corpus/ to OKF v0.1.

Rewrites Obsidian [[wikilinks]] to root-relative markdown links, renames the reserved catalog/
log files, reformats the log newest-first, and stamps okf_version. Idempotent; --dry-run."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "corpus"

_WIKILINK = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
_FENCE = re.compile(r"```.*?```", re.S)


def _titlecase(seg: str) -> str:
    return " ".join(w.capitalize() for w in seg.replace("-", " ").split())


def rewrite_wikilinks(text: str, resolve=None):
    """[[target|display]] -> [display](/target.md); returns (new_text, unresolved). Skips fences."""
    unresolved: list[str] = []
    # protect fenced code blocks
    fences: list[str] = []

    def _stash(m):
        fences.append(m.group(0))
        return f"\x00FENCE{len(fences) - 1}\x00"

    protected = _FENCE.sub(_stash, text)

    def _sub(m):
        target = m.group(1).strip()
        display = (m.group(2) or "").strip()
        if "/" not in target:
            resolved = resolve(target) if resolve else None
            if not resolved:
                unresolved.append(target)
                return display or _titlecase(target)
            target = resolved
        if not display:
            display = _titlecase(target.rsplit("/", 1)[-1])
        return f"[{display}](/{target}.md)"

    out = _WIKILINK.sub(_sub, protected)
    for i, f in enumerate(fences):
        out = out.replace(f"\x00FENCE{i}\x00", f)
    return out, unresolved
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_okf_migrate.py -v -p no:cacheprovider`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add bin/okf_migrate.py tests/test_okf_migrate.py
git commit -m "feat(okf): wikilink->markdown rewriter (fence-safe, resolvable, idempotent)"
```

---

### Task 3: Reserved-file conversion helpers (`bin/okf_migrate.py`)

**Files:**
- Modify: `bin/okf_migrate.py`
- Test: `tests/test_okf_migrate.py`

**Interfaces:**
- Consumes: `rewrite_wikilinks` (Task 2).
- Produces:
  - `reformat_log(text: str) -> str` — parse `## [YYYY-MM-DD ...] op | subject` entries, group by
    date, emit newest-date-first under `## YYYY-MM-DD` headings with the original entry lines as
    `* ` bullets (lead word from op). Never drop an entry.
  - `stamp_index(text: str) -> str` — ensure the catalog begins with a `---\nokf_version: "0.1"\n---`
    frontmatter block (add if absent; leave if present).
  - `ensure_type(text: str, type_value: str) -> str` — if the doc has no frontmatter, prepend
    `---\ntype: <type_value>\n---\n`; if it has frontmatter without `type`, insert the `type` line.

- [ ] **Step 1: Write the failing test**

```python
def test_reformat_log_newest_first_iso_groups():
    src = ("# Corpus Log\n\n"
           "## [2026-05-07] schema | bootstrap\n- did x\n\n"
           "## [2026-07-02] ingest | Foo\n- did y\n")
    out = mig.reformat_log(src)
    # newest date first, ISO group headings, no bracket/op-in-heading
    assert out.index("## 2026-07-02") < out.index("## 2026-05-07")
    assert "## [2026-" not in out
    assert "bootstrap" in out and "Foo" in out           # no entry lost


def test_stamp_index_adds_okf_version_once():
    once = mig.stamp_index("# Corpus Index\n\n## Domains\n")
    assert once.startswith('---\nokf_version: "0.1"\n---\n')
    assert mig.stamp_index(once) == once                 # idempotent


def test_ensure_type_adds_or_inserts():
    assert mig.ensure_type("# Domains\n", "domain-registry").startswith(
        "---\ntype: domain-registry\n---\n")
    got = mig.ensure_type("---\nfoo: 1\n---\nbody", "domain-registry")
    assert "type: domain-registry" in got and "foo: 1" in got
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_okf_migrate.py -k "reformat_log or stamp_index or ensure_type" -v -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'okf_migrate' has no attribute 'reformat_log'`

- [ ] **Step 3: Write minimal implementation**

Append to `bin/okf_migrate.py`:

```python
_LOG_ENTRY = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})[^\]]*\]\s*(\w+)\s*\|\s*(.+)$")


def reformat_log(text: str) -> str:
    """Group log entries by date, newest first, under `## YYYY-MM-DD` headings. Lossless."""
    lines = text.splitlines()
    groups: dict[str, list[str]] = {}
    order: list[str] = []
    cur_date = None
    for ln in lines:
        m = _LOG_ENTRY.match(ln)
        if m:
            cur_date, op, subject = m.group(1), m.group(2), m.group(3)
            groups.setdefault(cur_date, [])
            if cur_date not in order:
                order.append(cur_date)
            groups[cur_date].append(f"* **{op.capitalize()}**: {subject.strip()}")
        elif cur_date is not None and ln.strip():
            # continuation lines of the current entry -> nested detail
            groups[cur_date].append(f"  {ln.strip()}")
    out = ["# Corpus Log", "", "> OKF v0.1 change log. Newest first, grouped by date.", ""]
    for d in sorted(order, reverse=True):
        out.append(f"## {d}")
        out.extend(groups[d])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def stamp_index(text: str) -> str:
    if text.startswith("---\n") and "okf_version:" in text.split("---\n", 2)[1]:
        return text
    return '---\nokf_version: "0.1"\n---\n' + text


def ensure_type(text: str, type_value: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return f"---\ntype: {type_value}\n---\n{text}"
    fm, body = m.group(1), m.group(2)
    if re.search(r"^type:", fm, re.M):
        return text
    return f"---\ntype: {type_value}\n{fm}\n---\n{body}"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_okf_migrate.py -v -p no:cacheprovider`
Expected: PASS (9 tests)

- [ ] **Step 5: Commit**

```bash
git add bin/okf_migrate.py tests/test_okf_migrate.py
git commit -m "feat(okf): log reformat (newest-first ISO groups) + index okf_version stamp + ensure_type"
```

---

### Task 4: Migration driver + run it on the real corpus

**Files:**
- Modify: `bin/okf_migrate.py` (add `migrate_bundle` + CLI)
- Test: `tests/test_okf_migrate.py`

**Interfaces:**
- Consumes: all Task 2/3 helpers; `okf_lint.lint_bundle` for the post-check.
- Produces: `migrate_bundle(bundle: Path, dry_run: bool) -> dict` — renames `_index.md`→`index.md`
  (stamp + link-rewrite), `_log.md`→`log.md` (reformat), `_domains.md` gets `type: domain-registry`
  (`_config.md` already has `type`), rewrites wikilinks in every concept `.md`, and returns
  `{"files": N, "links": N, "unresolved": [...], "renamed": [...]}`.

- [ ] **Step 1: Write the failing test**

```python
def test_migrate_bundle_end_to_end(tmp_path):
    b = tmp_path / "corpus"; (b / "ai-engineering").mkdir(parents=True)
    (b / "_index.md").write_text("# Corpus Index\n\n### ai-engineering\n- [[ai-engineering/x|X]]\n")
    (b / "_log.md").write_text("# Corpus Log\n\n## [2026-05-07] schema | boot\n- a\n")
    (b / "_domains.md").write_text("# Domains\n")
    (b / "ai-engineering" / "x.md").write_text("---\ntype: entity\n---\nsee [[ai-engineering/y|Y]]\n")
    r = mig.migrate_bundle(b, dry_run=False)
    assert (b / "index.md").exists() and not (b / "_index.md").exists()
    assert (b / "log.md").exists() and not (b / "_log.md").exists()
    assert (b / "index.md").read_text().startswith('---\nokf_version: "0.1"\n---')
    assert "[Y](/ai-engineering/y.md)" in (b / "ai-engineering" / "x.md").read_text()
    assert "type: domain-registry" in (b / "_domains.md").read_text()
    assert r["links"] >= 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_okf_migrate.py -k migrate_bundle -v -p no:cacheprovider`
Expected: FAIL — `AttributeError: ... 'migrate_bundle'`

- [ ] **Step 3: Write minimal implementation**

Append to `bin/okf_migrate.py`:

```python
def _resolver(bundle: Path):
    """Map a bare page slug -> 'domain/slug' by scanning the tree once."""
    index: dict[str, str] = {}
    for p in bundle.rglob("*.md"):
        if p.name in ("_index.md", "_log.md", "_config.md", "_domains.md", "index.md", "log.md"):
            continue
        rel = p.relative_to(bundle).with_suffix("").as_posix()
        index.setdefault(p.stem, rel)  # first wins; ambiguous slugs stay first-seen
    return lambda slug: index.get(slug)


def migrate_bundle(bundle: Path, dry_run: bool = False) -> dict:
    resolve = _resolver(bundle)
    files = links = 0
    unresolved: list[str] = []
    renamed: list[str] = []

    def _write(path: Path, text: str):
        if not dry_run:
            path.write_text(text, encoding="utf-8")

    # concept docs: rewrite wikilinks
    for p in sorted(bundle.rglob("*.md")):
        if p.name in ("_index.md", "_log.md", "index.md", "log.md"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if p.name == "_domains.md":
            text = ensure_type(text, "domain-registry")
        new, un = rewrite_wikilinks(text, resolve)
        links += text.count("[[")
        unresolved += un
        if new != text:
            files += 1
            _write(p, new)

    # reserved catalog
    idx = bundle / "_index.md"
    if idx.exists():
        text = stamp_index(idx.read_text(encoding="utf-8"))
        text, un = rewrite_wikilinks(text, resolve)
        unresolved += un
        if not dry_run:
            (bundle / "index.md").write_text(text, encoding="utf-8")
            idx.unlink()
        renamed.append("_index.md->index.md")

    # reserved log
    lg = bundle / "_log.md"
    if lg.exists():
        text = reformat_log(lg.read_text(encoding="utf-8"))
        if not dry_run:
            (bundle / "log.md").write_text(text, encoding="utf-8")
            lg.unlink()
        renamed.append("_log.md->log.md")

    return {"files": files, "links": links, "unresolved": sorted(set(unresolved)),
            "renamed": renamed}


def main(argv=None) -> int:
    import argparse
    import json
    ap = argparse.ArgumentParser(description="Migrate corpus/ to OKF v0.1.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    r = migrate_bundle(BUNDLE, dry_run=args.dry_run)
    r["unresolved_count"] = len(r["unresolved"])
    r["unresolved"] = r["unresolved"][:40]
    print(json.dumps({**r, "dry_run": args.dry_run}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests + dry-run + real run + verify**

```bash
python3 -m pytest tests/test_okf_migrate.py -v -p no:cacheprovider   # all pass
python3 bin/okf_migrate.py --dry-run                                  # inspect links/unresolved
python3 bin/okf_migrate.py                                            # real migration
python3 bin/okf_lint.py                                               # expect "violations": 0
grep -rn '\[\[' corpus/ --include='*.md' | grep -v '```' | wc -l      # expect 0 (outside fences)
```
Expected: tests PASS; lint reports `"violations": 0`; wikilink count 0.

- [ ] **Step 5: Commit (migration is a big diff — its own commit)**

```bash
git add bin/okf_migrate.py tests/test_okf_migrate.py corpus/
git commit -m "feat(okf): migrate corpus/ to OKF v0.1 — index.md/log.md, root-relative links, okf_version"
```

---

### Task 5: Tooling emits OKF (writers)

Update the 7 `bin/` files that read/write `_index.md`/`_log.md` or emit wikilinks so new output is born conformant.

**Files:**
- Modify: `bin/quick_ingest_youtube.py` (`INDEX = CORPUS/"_index.md"` → `"index.md"`; `_index_append` writes `- [Title](/domain/sources/slug.md) — …` instead of `[[...]]`)
- Modify: `bin/quick_ingest_docs.py` (uses `qy._index_append` — inherits the fix; verify)
- Modify: `bin/scheduled_run.py` (`LOG_PATH` → `corpus/log.md`; `write_run_report` emits `## YYYY-MM-DD` + `* **op**: …` newest-first — prepend under today's date group)
- Modify: `bin/corpus_lint.py`, `bin/query.py`, `bin/pending_review.py`, `bin/weekly_synthesis.py` (`_index.md`→`index.md`, `_log.md`→`log.md` path constants; wikilink emission → markdown links)
- Test: extend each file's existing test for the new output shape.

**Interfaces:**
- Consumes: the migrated `corpus/index.md` + `corpus/log.md`.
- Produces: writers whose new pages/links/log entries pass `okf_lint`.

- [ ] **Step 1: Write/adjust the failing test** — for `quick_ingest_youtube._index_append`, assert it writes a `- [Title](/domain/sources/slug.md) —` line (not `[[...]]`):

```python
# in tests/test_... (quick intake): after _index_append, the index line matches
assert re.search(r"- \[.*\]\(/ai-engineering/sources/slug\.md\)", INDEX.read_text())
assert "[[" not in INDEX.read_text()
```

- [ ] **Step 2: Run it, verify it fails** (current code writes `[[...]]`).

- [ ] **Step 3: Implement** — in `bin/quick_ingest_youtube.py` change `INDEX` to `CORPUS / "index.md"` and the `_index_append` bullet to:

```python
bullet = f"- [{title}](/{domain}/sources/{slug}.md) — source · stub · {one_line}"
```
Update path constants in the other 6 files (`_index.md`→`index.md`, `_log.md`→`log.md`). In `scheduled_run.write_run_report`, write the run summary as a `## <today ISO>` group with `* **Ingest**: …` bullets, prepended after the log header (newest-first).

- [ ] **Step 4: Run each touched file's tests + `okf_lint`** — all pass; a simulated ingest leaves `okf_lint` at 0 violations.

- [ ] **Step 5: Commit**

```bash
git add bin/ tests/
git commit -m "feat(okf): corpus writers emit OKF (index.md/log.md, root-relative links, ISO log groups)"
```

---

### Task 6: Wire the conformance guard into lint + the nightly

**Files:**
- Modify: `bin/corpus_lint.py` (call `okf_lint.lint_bundle`; include an `okf` count in its report)
- Modify: `bin/scheduled_run.py` (`write_run_report` surfaces an `okf: N violations` line)
- Test: `tests/test_corpus_lint.py` (a wikilink or a typeless doc raises the OKF count)

- [ ] **Step 1: Write the failing test** — a fixture bundle with one typeless `.md` yields `okf_violations >= 1` from `corpus_lint`.
- [ ] **Step 2: Run it, verify it fails.**
- [ ] **Step 3: Implement** — import `okf_lint` in `corpus_lint`, add `report["okf_violations"] = len(okf_lint.lint_bundle(BUNDLE)["violations"])`; in `scheduled_run.write_run_report` append `  - okf: {n} violations{' ⚠' if n else ''}`.
- [ ] **Step 4: Run `tests/test_corpus_lint.py` + `tests/test_scheduled_run.py -k report`** — pass.
- [ ] **Step 5: Commit**

```bash
git add bin/corpus_lint.py bin/scheduled_run.py tests/
git commit -m "feat(okf): wire okf_lint into corpus_lint + nightly run report (conformance guard)"
```

---

### Task 7: Schema doc (`CLAUDE.md` → v2.0, OKF-aligned)

**Files:**
- Modify: `CLAUDE.md` (§4 frontmatter, §5 naming, §6 linking, §11 index, §12 log, §15 version)
- Modify: `corpus/log.md` (append a `schema` entry under today's date)

- [ ] **Step 1** — Update §6 Linking: replace the Obsidian-wikilink rule with "Cross-links are plain markdown links using bundle-root-relative absolute paths: `[Display](/<domain>/<page>.md)`. No `[[wikilinks]]`. Links are untyped; express the relationship in prose (§7.1). Broken links are tolerated." Update §11/§12 to the OKF `index.md`/`log.md` formats. In §4, note `type` is the OKF-required field and list `title/description/resource/tags/timestamp` as recommended, with all existing fields as OKF-legal extensions. Add a short "OKF conformance" note pointing at `bin/okf_lint.py` and `okf_version: "0.1"`.
- [ ] **Step 2** — Bump the title/version line to **v2.0** and add a v2.0 bullet to `docs/changelog.md`: "v2.0 — corpus aligned to Google OKF v0.1: reserved index.md/log.md, root-relative markdown links (wikilinks retired), okf_version stamp, okf_lint conformance guard."
- [ ] **Step 3** — Append to `corpus/log.md` under today's `## YYYY-MM-DD`: `* **Schema**: OKF v0.1 alignment (v2.0) — see docs/superpowers/specs/2026-07-03-okf-alignment-design.md`.
- [ ] **Step 4** — Verify `python3 bin/okf_lint.py` still reports 0 violations (the schema doc lives in the repo root / `docs/`, not the `corpus/` bundle, so it doesn't affect conformance).
- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md docs/changelog.md corpus/log.md
git commit -m "docs(okf): CLAUDE.md v2.0 — OKF-aligned schema (reserved files, markdown links, conformance)"
```

---

### Task 8: Transferability proof (bundle manifest)

**Files:**
- Create: `corpus/README.md` (bundle-root, a concept doc with `type`)

- [ ] **Step 1** — Create `corpus/README.md` with frontmatter `type: bundle-readme` and a body stating: this directory is an **OKF v0.1 bundle** (`okf_version: "0.1"` in `index.md`), links are root-relative markdown, `type` is required, validate with `bin/okf_lint.py`, reference the Google OKF spec URL.
- [ ] **Step 2** — Run `python3 bin/okf_lint.py` → 0 violations (README has a `type`, so it's a valid concept doc).
- [ ] **Step 3** — Sanity: `git ls-files corpus | head` shows the bundle is a self-contained markdown tree; note in the commit that a `corpus/`-only copy is a portable OKF bundle.
- [ ] **Step 4: Commit + push**

```bash
git add corpus/README.md
git commit -m "docs(okf): bundle README declaring OKF v0.1 conformance (transferability)"
git push origin main
```

---

## Self-Review

**Spec coverage:**
- OKF rules (type required, reserved index.md/log.md, root-relative links, okf_version, conformance) → Tasks 1–4. ✓
- Reserved-file formats (index no-fm + root okf_version; log newest-first ISO) → Tasks 3–4. ✓
- 4,293 wikilink rewrite (fence-safe, resolvable) → Task 2 + Task 4 run. ✓
- `_config`/`_domains` type (config already tagged; domains via `ensure_type`) → Task 4. ✓
- Tooling emits OKF → Task 5. ✓
- Conformance guard in lint + nightly → Task 6. ✓
- Schema `CLAUDE.md` v2.0 + changelog + log entry → Task 7. ✓
- `resource:` backfill → deferred (best-effort, OKF-legal to omit; noted as optional in Task 5/7, not a blocker). Flagged so it isn't mistaken for a gap.
- Transferability proof → Task 8. ✓

**Placeholder scan:** every code step shows complete code; prose-only steps (Task 5/6/7 sub-steps) name exact files + exact string changes. No TBD/TODO.

**Type consistency:** `parse_frontmatter`/`check_concept`/`check_index`/`check_log`/`lint_bundle` (Task 1), `rewrite_wikilinks -> (str, list)` (Task 2), `reformat_log`/`stamp_index`/`ensure_type` (Task 3), `migrate_bundle -> dict` (Task 4) — used consistently across tasks. ✓
