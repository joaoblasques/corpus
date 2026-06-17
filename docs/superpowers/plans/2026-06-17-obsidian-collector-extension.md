# Obsidian Collector Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing `collect-obsidian` collector to cover two more vault folders, keep Articles/Study Notes PARA-native, and fetch inline external links from note bodies.

**Architecture:** Edit the policy module `bin/collect_obsidian.py` (include set, link extraction, filename, provenance) and its thin driver `bin/obsidian_client.py` (note-branch link fetch), then update config + skill docs. TDD throughout, mirroring the existing collector tests. No schema change to `CLAUDE.md`, no change to the launchd scheduled job.

**Tech Stack:** Python 3.12, pytest. Tests under `tests/`, run with `python3 -m pytest`. The collector reuses `fetch_link.py` for network fetches and `collect_email.slugify/yaml_scalar/URL_RE`.

## Global Constraints

- Collector writes only into `raw/_inbox/`; never into `corpus/` or the vault (except the reaper's gated `git rm`, unchanged here).
- Reap stays gated on `corpus_ingested` of the raw copy; never auto-commits the vault.
- Channel labels: note bodies → `notes`; fetched links → `web`.
- Inline-link fetch provenance key: `via_vault_note` (URL-list links keep `via_vault_list`). Exactly one provenance key per web source.
- `MAX_LINKS_PER_NOTE = 10`.
- Auth-walled domains skipped without a network call: `linkedin.com`, `x.com`, `twitter.com`.
- Dry run makes **no** network calls.
- All tests prepend `bin/` to `sys.path` and `import collect_obsidian as co` (see existing `tests/test_collect_obsidian.py`).

---

### Task 1: Folder policy — new include set

**Files:**
- Modify: `bin/collect_obsidian.py:20-23` (`INCLUDE_DIRS`)
- Test: `tests/test_collect_obsidian.py` (`test_is_included_resources`, `test_is_included_excludes`)

**Interfaces:**
- Consumes: nothing new.
- Produces: `co.is_included(rel_path) -> bool` with the new policy. No signature change.

- [ ] **Step 1: Update the inclusion tests to the new policy (make them fail first)**

In `tests/test_collect_obsidian.py`, replace the body of `test_is_included_resources` and `test_is_included_excludes` with:

```python
def test_is_included_resources():
    # PARA-native folders are now EXCLUDED from collect->delete (kept in place)
    assert co.is_included("03_Resources/Articles/Clean Code.md") is False
    assert co.is_included("03_Resources/Study Notes/CAP.md") is False
    # Newly collected folders
    assert co.is_included("Clippings/Introducing routines in Claude Code.md") is True
    assert co.is_included("06_Metadata/Reference/note_taking_protocol.md") is True
    # Still-collected folders
    assert co.is_included("00_Inbox/Clippings/scrape/merkle-trees-scrape.md") is True
    assert co.is_included("03_Resources/Books/cheatsheet.md") is True
    assert co.is_included("03_Resources/Snippets/Enrich Notes Script.md") is True


def test_is_included_excludes():
    assert co.is_included("03_Resources/llm-wiki-system/CLAUDE.md") is False
    assert co.is_included("01_Projects/foo.md") is False
    assert co.is_included("00_Inbox/Clippings/articles_processed.md") is False
    assert co.is_included("06_Metadata/Templates/Daily-Note-Template.md") is False
    assert co.is_included("06_Metadata/SETUP_COMPLETE.md") is False
    assert co.is_included("06_Metadata/Reference/README.md") is False
    assert co.is_included("03_Resources/Books/cheatsheet.pdf") is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py::test_is_included_resources tests/test_collect_obsidian.py::test_is_included_excludes -v`
Expected: FAIL (Articles/Study Notes still return True; `Clippings`/`06_Metadata/Reference` return False).

- [ ] **Step 3: Update `INCLUDE_DIRS`**

In `bin/collect_obsidian.py` replace the `INCLUDE_DIRS` list:

```python
INCLUDE_DIRS = [
    "Clippings",                       # top-level web clippings
    "00_Inbox/Clippings",
    "03_Resources/Books",
    "03_Resources/Snippets",
    "03_Resources/Prompt Templates",
    "06_Metadata/Reference",           # reference prompt notes only
]
```

(`EXCLUDE_DIRS`, `EXCLUDE_FILE_RE`, and `is_included` are unchanged. The `README.md` rule already excludes `06_Metadata/Reference/README.md`; `Templates/` and `SETUP_COMPLETE.md` fall outside the include set.)

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py::test_is_included_resources tests/test_collect_obsidian.py::test_is_included_excludes -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): add Clippings + 06_Metadata/Reference, drop Articles/Study Notes to PARA-native"
```

---

### Task 2: `read_note` surfaces the note's `source:` URL

**Files:**
- Modify: `bin/collect_obsidian.py:57-73` (`read_note`)
- Modify: `bin/obsidian_client.py:41` (unpack the new return value)
- Test: `tests/test_collect_obsidian.py` (`test_read_note_extracts_title_tags_body`, `test_read_note_no_frontmatter_uses_stem`)

**Interfaces:**
- Consumes: nothing new.
- Produces: `co.read_note(abs_path) -> (title: str, tags: list[str], source_url: str, body: str)`. The new 3rd element is the `source:` frontmatter value (empty string when absent). Task 6 consumes `source_url`.

- [ ] **Step 1: Update the read_note tests to expect the 4-tuple (fail first)**

Replace these two tests in `tests/test_collect_obsidian.py`:

```python
def test_read_note_extracts_title_tags_body(tmp_path):
    f = tmp_path / "n.md"
    f.write_text('---\ntitle: "Hello"\nsource: "https://ex.com/a"\ntags:\n  - x\n  - y\n---\nBody here\n')
    title, tags, source_url, body = co.read_note(str(f))
    assert title == "Hello"
    assert tags == ["x", "y"]
    assert source_url == "https://ex.com/a"
    assert body.strip() == "Body here"


def test_read_note_no_frontmatter_uses_stem(tmp_path):
    f = tmp_path / "My Note.md"
    f.write_text("Just text, no frontmatter")
    title, tags, source_url, body = co.read_note(str(f))
    assert title == "My Note"
    assert tags == []
    assert source_url == ""
    assert body.strip() == "Just text, no frontmatter"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k read_note -v`
Expected: FAIL (`ValueError: not enough values to unpack`).

- [ ] **Step 3: Implement the 4-tuple in `read_note`**

In `bin/collect_obsidian.py`, change `read_note` to parse `source:` and return it. Full replacement:

```python
def read_note(abs_path: str):
    """Return (title, tags, source_url, body) — splits the note's frontmatter off the body."""
    t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    title, tags, source_url, body = "", [], "", t
    if t.startswith("---"):
        end = t.find("\n---", 3)
        if end != -1:
            fm, body = t[3:end], t[end + 4:].lstrip("\n")
            tm = re.search(r"^title:\s*(.+)$", fm, re.M)
            if tm:
                title = tm.group(1).strip().strip('"')
            sm = re.search(r"^source:\s*(.+)$", fm, re.M)
            if sm:
                source_url = sm.group(1).strip().strip('"')
            tg = re.search(r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
            if tg:
                tags = [re.sub(r"^\s*-\s*", "", ln).strip() for ln in tg.group(1).splitlines() if ln.strip()]
    if not title:
        title = Path(abs_path).stem
    return title, tags, source_url, body
```

- [ ] **Step 4: Keep the driver call site consistent**

In `bin/obsidian_client.py:41` change the unpack to the 4-tuple (link-fetch wiring comes in Task 6):

```python
                title, tags, source_url, body = co.read_note(d["abs_path"])
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k read_note -v && python3 -m pytest tests/test_obsidian_client.py -v`
Expected: PASS (driver still works; it ignores `source_url` for now).

- [ ] **Step 6: Commit**

```bash
git add bin/collect_obsidian.py bin/obsidian_client.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): read_note returns the note source URL"
```

---

### Task 3: `extract_inline_links` helper

**Files:**
- Modify: `bin/collect_obsidian.py` (add constants near line 26; add function after `parse_url_list`)
- Test: `tests/test_collect_obsidian.py` (new tests)

**Interfaces:**
- Consumes: `URL_RE` (already imported from `collect_email`).
- Produces: `co.extract_inline_links(body: str, source_url: str = "") -> dict` returning
  `{"links": list[str], "auth_skipped": int, "dropped": int}` —
  `links` = deduped external http(s) URLs from the body, minus `source_url`, asset links, and auth-walled domains, capped at `MAX_LINKS_PER_NOTE`;
  `auth_skipped` = count of distinct auth-walled URLs dropped;
  `dropped` = count of eligible links beyond the cap (0 if none).
- Also produces module constants `MAX_LINKS_PER_NOTE = 10` and `AUTH_WALLED_RE`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_collect_obsidian.py`:

```python
def test_extract_inline_links_basic_dedup():
    body = "See https://a.com/x and again https://a.com/x and https://b.com/y."
    r = co.extract_inline_links(body)
    assert r["links"] == ["https://a.com/x", "https://b.com/y"]
    assert r["auth_skipped"] == 0
    assert r["dropped"] == 0


def test_extract_inline_links_skips_source_assets_auth():
    body = ("source repeated https://src.com/post "
            "image ![alt](https://c.com/pic.png) "
            "doc https://c.com/file.pdf "
            "social https://www.linkedin.com/in/x "
            "good https://good.com/article")
    r = co.extract_inline_links(body, source_url="https://src.com/post")
    assert r["links"] == ["https://good.com/article"]
    assert r["auth_skipped"] == 1  # linkedin


def test_extract_inline_links_respects_cap():
    body = " ".join(f"https://s{i}.com/a" for i in range(15))
    r = co.extract_inline_links(body)
    assert len(r["links"]) == co.MAX_LINKS_PER_NOTE
    assert r["dropped"] == 5
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k extract_inline_links -v`
Expected: FAIL (`AttributeError: module 'collect_obsidian' has no attribute 'extract_inline_links'`).

- [ ] **Step 3: Implement constants + function**

In `bin/collect_obsidian.py`, after the `URL_LIST_NAMES` line (≈26) add:

```python
MAX_LINKS_PER_NOTE = 10
AUTH_WALLED_RE = re.compile(r"(?i)://(?:[^/]*\.)?(?:linkedin\.com|x\.com|twitter\.com)(?:/|$)")
ASSET_EXT_RE = re.compile(r"(?i)\.(?:png|jpe?g|gif|svg|webp|pdf|mp4|mov|zip)$")
```

After `parse_url_list` add:

```python
def extract_inline_links(body: str, source_url: str = "") -> dict:
    """External http(s) links in a note body: deduped, minus the source URL, asset
    links, and auth-walled domains; capped at MAX_LINKS_PER_NOTE."""
    seen, links, auth = set(), [], 0
    for m in URL_RE.finditer(body or ""):
        u = m.group(0).rstrip(".,)")
        if u in seen:
            continue
        seen.add(u)
        if source_url and u == source_url.rstrip(".,)"):
            continue
        if ASSET_EXT_RE.search(u.split("?", 1)[0]):
            continue
        if AUTH_WALLED_RE.search(u):
            auth += 1
            continue
        links.append(u)
    dropped = max(0, len(links) - MAX_LINKS_PER_NOTE)
    return {"links": links[:MAX_LINKS_PER_NOTE], "auth_skipped": auth, "dropped": dropped}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k extract_inline_links -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): extract_inline_links with dedup, asset/auth filters, cap"
```

---

### Task 4: `note_filename` collision disambiguation

**Files:**
- Modify: `bin/collect_obsidian.py:76-81` (`note_filename`)
- Test: `tests/test_collect_obsidian.py` (`test_note_filename`)

**Interfaces:**
- Consumes: `slugify` (already imported).
- Produces: `co.note_filename(rel_path, base=None) -> Path` whose filename is `notes-<parent-slug>-<stem-slug>.md`, where `<parent-slug>` is the slugified immediate parent folder of the note. Same signature.

- [ ] **Step 1: Update the filename test (fail first)**

Replace `test_note_filename` in `tests/test_collect_obsidian.py` with exactly:

```python
def test_note_filename(tmp_path):
    p = co.note_filename("03_Resources/Books/Clean Code!.md", tmp_path)
    assert p.name == "notes-03-resources-books-clean-code.md"
    # same title, different folder -> different raw filename (collision fixed)
    a = co.note_filename("Clippings/Routines.md", tmp_path)
    b = co.note_filename("00_Inbox/Clippings/Routines.md", tmp_path)
    assert a.name == "notes-clippings-routines.md"
    assert b.name == "notes-00-inbox-clippings-routines.md"
    assert a.name != b.name
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_obsidian.py::test_note_filename -v`
Expected: FAIL (current name is `notes-clean-code.md`).

- [ ] **Step 3: Implement parent-token disambiguation**

Replace `note_filename` in `bin/collect_obsidian.py`:

```python
def note_filename(rel_path: str, base=None) -> Path:
    base = base if base is not None else INBOX
    parts = rel_path.replace("\\", "/").split("/")
    stem = parts[-1]
    if stem.endswith(".md"):
        stem = stem[:-3]
    # full parent path slug so same-titled notes in different trees never collide
    parent_slug = slugify("-".join(parts[:-1])) if len(parts) >= 2 else ""
    name = f"notes-{parent_slug}-{slugify(stem)}.md" if parent_slug else f"notes-{slugify(stem)}.md"
    return base / name
```

> The **full** parent path is slugified, so `03_Resources/Books/Clean Code!.md -> notes-03-resources-books-clean-code.md`, `Clippings/Routines.md -> notes-clippings-routines.md`, and `00_Inbox/Clippings/Routines.md -> notes-00-inbox-clippings-routines.md`. Immediate-parent-only would NOT work — both Clippings folders share the parent name `Clippings`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_collect_obsidian.py::test_note_filename -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "fix(collect-obsidian): disambiguate raw note filename by parent folder"
```

---

### Task 5: `build_url_source` supports `via_vault_note`

**Files:**
- Modify: `bin/collect_obsidian.py:103-112` (`build_url_source`)
- Test: `tests/test_collect_obsidian.py` (`test_build_url_source` + new variant)

**Interfaces:**
- Consumes: `yaml_scalar` (already imported).
- Produces: `co.build_url_source(meta, body) -> str`. `meta` carries exactly one of `via_vault_list` or `via_vault_note`; the emitted frontmatter includes whichever is present. Unchanged signature.

- [ ] **Step 1: Add the new-variant test (fail first)**

In `tests/test_collect_obsidian.py`, keep the existing `test_build_url_source` and add:

```python
def test_build_url_source_via_vault_note():
    doc = co.build_url_source(
        {"source_url": "https://a.com/x", "via_vault_note": "Clippings/Routines.md",
         "title": "X", "collected_at": "2026-06-17"}, "body text")
    assert "channel: web" in doc
    assert "via_vault_note: Clippings/Routines.md" in doc
    assert "via_vault_list:" not in doc
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k build_url_source -v`
Expected: FAIL (`KeyError: 'via_vault_list'`).

- [ ] **Step 3: Implement conditional provenance**

Replace `build_url_source` in `bin/collect_obsidian.py`:

```python
def build_url_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: web", "source: obsidian-list",
        f"source_url: {meta['source_url']}",
    ]
    if meta.get("via_vault_note"):
        lines.append(f"via_vault_note: {meta['via_vault_note']}")
    else:
        lines.append(f"via_vault_list: {meta['via_vault_list']}")
    lines += [
        f"title: {yaml_scalar(meta.get('title', ''))}",
        f"collected_at: {meta['collected_at']}", "---", "", body.strip(), "",
    ]
    return "\n".join(lines)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k build_url_source -v`
Expected: PASS (both the existing url-list test and the new note variant).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): build_url_source supports via_vault_note provenance"
```

---

### Task 6: Driver — fetch inline links in the note branch

**Files:**
- Modify: `bin/obsidian_client.py` — `cmd_collect` (counter dict + the `if d["kind"] == "note":` branch)
- Test: `tests/test_obsidian_client.py` (new test)

**Interfaces:**
- Consumes: `co.extract_inline_links`, `co.build_url_source` (via_vault_note), `co.url_filename`, `co.url_already_collected`, and the `fetch_url` seam (stubbable). The driver invokes via `oc.cmd_collect(oc._args([...]))`; dedup uses `co.DEDUP_DIRS`.
- Produces: the JSON summary gains integer keys `inline_urls`, `inline_failed`, `inline_skipped_auth`, `inline_dropped`.

- [ ] **Step 1: Write the failing driver test**

Follow the existing pattern in `tests/test_obsidian_client.py` — a real tmp vault passed via `--vault`, `fetch_url` stubbed, `co.INBOX`/`co.DEDUP_DIRS` pointed at the tmp inbox, invoked through `oc.cmd_collect(oc._args([...]))`. Add:

```python
def test_collect_fetches_inline_note_links(tmp_path, monkeypatch):
    import obsidian_client as oc
    inbox = tmp_path / "inbox"; inbox.mkdir()
    vault = tmp_path / "vault"; (vault / "Clippings").mkdir(parents=True)
    (vault / "Clippings" / "N.md").write_text(
        '---\ntitle: "N"\nsource: "https://src.com/p"\n---\n'
        'read https://good.com/a and https://src.com/p again\n')
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(oc, "fetch_url", lambda url: {"title": "A", "text": "fetched body"})
    rc = oc.cmd_collect(oc._args(["collect", "--vault", str(vault)]))
    assert rc == 0
    webs = list(inbox.glob("web-*.md"))
    assert len(webs) == 1                       # good.com fetched; src.com skipped as source URL
    text = webs[0].read_text()
    assert "via_vault_note: Clippings/N.md" in text
    assert "source_url: https://good.com/a" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_obsidian_client.py -k inline -v`
Expected: FAIL (no `web-*.md` produced — note branch doesn't fetch links yet).

- [ ] **Step 3: Add counters**

In `bin/obsidian_client.py`, inside `cmd_collect`, extend the counter dict:

```python
    t = {"notes": 0, "urls": 0, "url_failed": 0, "skipped": 0,
         "inline_urls": 0, "inline_failed": 0, "inline_skipped_auth": 0, "inline_dropped": 0}
```

- [ ] **Step 4: Fetch inline links after writing the note**

In the `if d["kind"] == "note":` block, after `t["notes"] += 1`, append:

```python
                il = co.extract_inline_links(body, source_url)
                t["inline_skipped_auth"] += il["auth_skipped"]
                t["inline_dropped"] += il["dropped"]
                for url in il["links"]:
                    if co.url_already_collected(url):
                        t["skipped"] += 1
                        continue
                    if args.dry_run:
                        t["inline_urls"] += 1
                        continue
                    content = fetch_url(url)
                    if not content or not content.get("text"):
                        t["inline_failed"] += 1
                        continue
                    p2 = co.url_filename(url, content.get("title", ""))
                    p2.parent.mkdir(parents=True, exist_ok=True)
                    p2.write_text(co.build_url_source(
                        {"source_url": url, "via_vault_note": d["rel_path"],
                         "title": content.get("title", ""), "collected_at": collected_at},
                        content["text"]), encoding="utf-8")
                    t["inline_urls"] += 1
```

> `source_url` is available because Task 2 makes the note-branch unpack `title, tags, source_url, body`. The `args.dry_run` guard ensures no network call on dry runs.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_obsidian_client.py -v`
Expected: PASS (new test + existing driver tests).

- [ ] **Step 6: Commit**

```bash
git add bin/obsidian_client.py tests/test_obsidian_client.py
git commit -m "feat(collect-obsidian): fetch inline note links as channel web (via_vault_note)"
```

---

### Task 7: Docs, config, and full-suite gate

**Files:**
- Modify: `corpus/_config.md` (collect-obsidian section)
- Modify: `corpus/_log.md` (append a `config` entry)
- Modify: `.claude/skills/collect-obsidian/SKILL.md` (include/exclude + inline-link note)

**Interfaces:** none (docs only).

- [ ] **Step 1: Update `corpus/_config.md`**

In the `## Obsidian vault collection (collect-obsidian)` section, replace the Include/Exclude bullets with:

```markdown
- **Include (collect → reap):** `Clippings/` (top-level), `00_Inbox/Clippings/`,
  `03_Resources/{Books, Snippets, Prompt Templates}`, `06_Metadata/Reference/`.
- **PARA-native (ingested in place, never reaped):** `03_Resources/Articles/`,
  `03_Resources/Study Notes/` — these keep their in-vault citations.
- **Exclude:** `03_Resources/llm-wiki-system` (corpus mirror), `01_Projects`, `02_Areas`,
  `04_Archive`, `06_Metadata/{Templates, SETUP_COMPLETE.md, README.md}`, rest of `00_Inbox`,
  `*_processed.md`, `README.md`, binaries.
- Inline external links in note bodies are fetched (channel `web`, provenance
  `via_vault_note`, deduped, asset/auth-walled links skipped, capped at 10/note), in addition
  to dedicated URL-list files (`articles to process.md`, `TO SCRAPE.md`).
```

- [ ] **Step 2: Append a `config` log entry to `corpus/_log.md`**

```markdown

## [2026-06-17 HH:MM] config | collect-obsidian include set + inline-link following
- include: +Clippings (top-level), +06_Metadata/Reference; -03_Resources/Articles, -03_Resources/Study Notes (kept PARA-native, never reaped)
- links: note-body inline links now fetched (channel web, via_vault_note; asset/auth filters; cap 10/note)
- raw note filenames disambiguated by parent folder (collision fix)
- spec: docs/superpowers/specs/2026-06-17-obsidian-collector-extension-design.md
```

(Use the real current time for `HH:MM`.)

- [ ] **Step 3: Update `.claude/skills/collect-obsidian/SKILL.md`**

Update the include/exclude description to match `_config.md` above and add one line under Notes:

```markdown
- Inline external links inside note bodies are fetched as channel `web` (provenance
  `via_vault_note`), deduped, asset/auth-walled links skipped, capped at 10 per note.
```

- [ ] **Step 4: Run the full collector suite as the gate**

Run: `python3 -m pytest tests/test_collect_obsidian.py tests/test_obsidian_client.py -v`
Expected: PASS (all tests).

- [ ] **Step 5: Commit**

```bash
git add corpus/_config.md corpus/_log.md .claude/skills/collect-obsidian/SKILL.md
git commit -m "docs(collect-obsidian): document new include set + inline-link following"
```

---

## Notes for the executor

- **Transition wrinkle (filename change):** existing in-flight `raw/_inbox/notes-<slug>.md`
  files written under the old scheme keep their old names; newly collected notes use the
  parent-token names. Any note still in the vault and not yet ingested may be re-collected
  under the new name (a one-time transient duplicate), which the next ingest + reap resolves.
  No action needed; just don't be surprised by it.
- **No scheduled-job change:** `bin/scheduled_run.py` and the launchd plist are untouched. The
  daily 08:00 run picks up the new behavior automatically because it already invokes the
  obsidian collector. Optionally verify after merge with a dry run:
  `python3 bin/obsidian_client.py collect --dry-run`.
- **Verification of real coverage** (post-merge, optional): the dry run should now report
  notes discovered under `Clippings/` and `06_Metadata/Reference/`, and zero under
  `03_Resources/Articles`/`Study Notes`.
```
