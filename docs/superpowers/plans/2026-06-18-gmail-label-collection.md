# Gmail Label Collection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collect Gmail mail filed under 9 configured topic labels (alongside the existing starred flow), then after corpus ingest remove the matched label(s) and archive the message.

**Architecture:** Extend `bin/collect_email.py` (record `gmail_corpus_labels` on the source + a deterministic post-ingest scanner) and `bin/gmail_client.py` (label config, a labeled collection pass in `cmd_run`, and a `reap-labels` post-ingest subcommand), then wire `reap-labels` into `bin/scheduled_run.py` after the ingest phase. Mirrors the PDF/obsidian collect→ingest→reap split.

**Tech Stack:** Python 3.12, pytest, Gmail API (`gmail.modify` scope, already granted). Tests under `tests/`, run with `python3 -m pytest`. The Gmail service is passed in and mocked in tests.

## Global Constraints

- 9 corpus labels (exact Gmail names): `Data Engineering`, `Data Engineering/databricks`, `Data Engineering/dbt`, `Data Engineering/spark`, `Ml`, `ML Engineering`, `MLOps`, `Productivity`, `Prompting`.
- After ingest: remove only the **matched** corpus label(s) on a message, plus `INBOX` (archive). Never touch other labels.
- The starred flow is **unchanged** (still de-stars + archives immediately on collection).
- Labeled emails are **not** archived on collection — only post-ingest, gated on `corpus_ingested: true`.
- Source frontmatter marker: `gmail_corpus_labels:` (a YAML block list of matched label names). Present only for labeled emails.
- Dedup by `gmail_message_id` (existing `collect_email.already_collected`).
- Query Gmail by **label ID** (`messages().list(labelIds=[id])`), not `q="label:..."` search.
- `reap-labels` is idempotent and `--dry-run`-safe; gated on `corpus_ingested`.
- Channel stays `email` → `raw/email/`.
- Tests prepend `bin/` to `sys.path` (see `tests/test_gmail_client.py`).

---

### Task 1: `collect_email` — record `gmail_corpus_labels` + post-ingest scanner

**Files:**
- Modify: `bin/collect_email.py` (`build_document`; add `labeled_reapable`)
- Test: `tests/test_collect_email.py`

**Interfaces:**
- Consumes: nothing new.
- Produces:
  - `build_document(meta, body)` now emits a `gmail_corpus_labels:` YAML block list when `meta["gmail_corpus_labels"]` is a non-empty list; omits it otherwise.
  - `labeled_reapable(dirs=None) -> list[dict]` — each `{"gmail_message_id": str, "gmail_corpus_labels": [str, ...]}` for raw sources that have BOTH `corpus_ingested: true` and a non-empty `gmail_corpus_labels`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_collect_email.py`:

```python
def test_build_document_emits_corpus_labels():
    doc = ce.build_document(
        {"gmail_message_id": "abc", "from": "a@b.c", "subject": "S",
         "date_received": "2026-06-18", "collected_at": "2026-06-18",
         "gmail_corpus_labels": ["Data Engineering", "MLOps"]},
        "body")
    assert "gmail_corpus_labels:\n  - Data Engineering\n  - MLOps" in doc


def test_build_document_omits_corpus_labels_when_absent():
    doc = ce.build_document(
        {"gmail_message_id": "abc", "from": "a@b.c", "subject": "S",
         "date_received": "2026-06-18", "collected_at": "2026-06-18"}, "body")
    assert "gmail_corpus_labels" not in doc


def test_labeled_reapable_selects_ingested_labeled(tmp_path):
    d = tmp_path / "raw"; d.mkdir()
    (d / "email-ingested.md").write_text(
        "---\nchannel: email\ngmail_message_id: m1\n"
        "gmail_corpus_labels:\n  - MLOps\n  - Ml\ncorpus_ingested: true\n---\nbody",
        encoding="utf-8")
    (d / "email-not-ingested.md").write_text(  # has labels but not ingested
        "---\ngmail_message_id: m2\ngmail_corpus_labels:\n  - MLOps\n---\nx", encoding="utf-8")
    (d / "email-starred.md").write_text(  # ingested but no corpus labels (starred)
        "---\ngmail_message_id: m3\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    out = ce.labeled_reapable(dirs=[d])
    assert out == [{"gmail_message_id": "m1", "gmail_corpus_labels": ["MLOps", "Ml"]}]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_collect_email.py -k "corpus_labels or labeled_reapable" -v`
Expected: FAIL (`gmail_corpus_labels` not emitted; `labeled_reapable` not defined).

- [ ] **Step 3: Emit the field in `build_document`**

In `bin/collect_email.py` `build_document`, after the `pointer:` line and before the `collected_at:` line, insert:

```python
    labels = meta.get("gmail_corpus_labels") or []
    if labels:
        lines.append("gmail_corpus_labels:")
        lines += [f"  - {label}" for label in labels]
```

(For reference, the surrounding lines are:
```python
    lines.append(f"pointer: {'true' if meta.get('pointer') else 'false'}")
    # <-- insert the labels block here -->
    lines.append(f"collected_at: {meta['collected_at']}")
```
)

- [ ] **Step 4: Add `labeled_reapable`**

Add to `bin/collect_email.py` (near `already_collected`):

```python
def labeled_reapable(dirs: list[Path] | None = None) -> list[dict]:
    """Raw email sources ready for post-ingest un-label/archive: those with BOTH
    `corpus_ingested: true` and a non-empty `gmail_corpus_labels` block. Pure I/O —
    no network. Each item: {gmail_message_id, gmail_corpus_labels}."""
    out: list[dict] = []
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue
            if "corpus_ingested: true" not in text or not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            fm = text[3:end] if end != -1 else text
            mid = re.search(r"^gmail_message_id:\s*(.+)$", fm, re.M)
            lm = re.search(r"^gmail_corpus_labels:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
            if not mid or not lm:
                continue
            labels = [re.sub(r"^\s*-\s*", "", ln).strip()
                      for ln in lm.group(1).splitlines() if ln.strip()]
            if labels:
                out.append({"gmail_message_id": mid.group(1).strip(),
                            "gmail_corpus_labels": labels})
    return out
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_email.py -q`
Expected: PASS (new tests + existing).

- [ ] **Step 6: Commit**

```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): record gmail_corpus_labels + labeled_reapable scanner"
```

---

### Task 2: `gmail_client` — label config + resolve/match/list helpers

**Files:**
- Modify: `bin/gmail_client.py` (add `CORPUS_LABELS`, `resolve_label_ids`, `matched_corpus_labels`, `list_labeled_messages`)
- Test: `tests/test_gmail_client.py`

**Interfaces:**
- Consumes: a Gmail `service` (mocked in tests).
- Produces:
  - `CORPUS_LABELS: list[str]` (the 9 names).
  - `resolve_label_ids(service, names=None) -> tuple[dict[str,str], list[str]]` → (name→id for found labels, list of missing names). Defaults to `CORPUS_LABELS`.
  - `matched_corpus_labels(message_label_ids, name_to_id) -> list[str]` — pure: corpus label names whose id is in the message's label ids.
  - `list_labeled_messages(service, label_ids, max_results=None) -> list[dict]` — full messages across the label ids, deduped by message id.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_gmail_client.py` (the file already has `import gmail_client as gc` and the `sys.path` insert at the top — do NOT re-add them):

```python
class _Labels:
    def __init__(self, labels): self._labels = labels
    def list(self, **k): return self
    def execute(self): return {"labels": self._labels}


class _Messages:
    def __init__(self, by_label, full):
        self._by_label, self._full = by_label, full
    def list(self, userId=None, labelIds=None, maxResults=None):
        self._cur = self._by_label.get(labelIds[0], [])
        return self
    def list_next(self, req, resp): return None
    def get(self, userId=None, id=None, format=None):
        self._gid = id
        return self
    def execute(self):
        if hasattr(self, "_gid"):
            g = self._full[self._gid]; del self._gid; return g
        return {"messages": self._cur}


class _Svc:
    def __init__(self, labels=None, by_label=None, full=None):
        self._labels = labels or []
        self._by_label = by_label or {}
        self._full = full or {}
    def users(self): return self
    def labels(self): return _Labels(self._labels)
    def messages(self): return _Messages(self._by_label, self._full)


def test_resolve_label_ids_maps_and_reports_missing():
    svc = _Svc(labels=[{"name": "MLOps", "id": "L1"}, {"name": "Ml", "id": "L2"}])
    name_to_id, missing = gc.resolve_label_ids(svc, ["MLOps", "Ml", "Ghost"])
    assert name_to_id == {"MLOps": "L1", "Ml": "L2"}
    assert missing == ["Ghost"]


def test_matched_corpus_labels_intersects():
    name_to_id = {"MLOps": "L1", "Ml": "L2", "Prompting": "L3"}
    assert gc.matched_corpus_labels(["L2", "L9", "L1"], name_to_id) == ["Ml", "MLOps"] \
        or gc.matched_corpus_labels(["L2", "L9", "L1"], name_to_id) == ["MLOps", "Ml"]


def test_list_labeled_messages_dedups_across_labels():
    by_label = {"L1": [{"id": "m1"}, {"id": "m2"}], "L2": [{"id": "m2"}, {"id": "m3"}]}
    full = {k: {"id": k, "labelIds": []} for k in ("m1", "m2", "m3")}
    svc = _Svc(by_label=by_label, full=full)
    out = gc.list_labeled_messages(svc, ["L1", "L2"])
    assert sorted(m["id"] for m in out) == ["m1", "m2", "m3"]   # m2 deduped
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_gmail_client.py -k "resolve_label_ids or matched_corpus or list_labeled" -v`
Expected: FAIL (functions not defined).

- [ ] **Step 3: Implement the helpers**

In `bin/gmail_client.py`, near the top-level functions (e.g. after `list_starred_messages`), add:

```python
# Topic labels collected into the corpus (exact Gmail names). Edit to add/remove
# labels; documented in corpus/_config.md.
CORPUS_LABELS = [
    "Data Engineering", "Data Engineering/databricks", "Data Engineering/dbt",
    "Data Engineering/spark", "Ml", "ML Engineering", "MLOps",
    "Productivity", "Prompting",
]


def resolve_label_ids(service, names=None):
    """Map configured label names → Gmail label ids. Returns (name_to_id, missing)."""
    names = names if names is not None else CORPUS_LABELS
    resp = service.users().labels().list(userId="me").execute()
    by_name = {l["name"]: l["id"] for l in resp.get("labels", [])}
    name_to_id = {n: by_name[n] for n in names if n in by_name}
    missing = [n for n in names if n not in by_name]
    return name_to_id, missing


def matched_corpus_labels(message_label_ids, name_to_id) -> list:
    """Corpus label NAMES whose id is present on the message (pure)."""
    id_to_name = {v: k for k, v in name_to_id.items()}
    return [id_to_name[i] for i in message_label_ids if i in id_to_name]


def list_labeled_messages(service, label_ids, max_results=None) -> list:
    """Full messages across the given label ids, deduped by message id."""
    seen, out = set(), []
    for lid in label_ids:
        req = service.users().messages().list(userId="me", labelIds=[lid], maxResults=100)
        while req is not None:
            resp = req.execute()
            for m in resp.get("messages", []):
                mid = m["id"]
                if mid in seen:
                    continue
                seen.add(mid)
                full = service.users().messages().get(userId="me", id=mid, format="full").execute()
                out.append(full)
                if max_results and len(out) >= max_results:
                    return out
            req = service.users().messages().list_next(req, resp)
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_gmail_client.py -k "resolve_label_ids or matched_corpus or list_labeled" -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/gmail_client.py tests/test_gmail_client.py
git commit -m "feat(gmail): CORPUS_LABELS + resolve/match/list label helpers"
```

---

### Task 3: `gmail_client` — labeled collection pass in `cmd_run`

**Files:**
- Modify: `bin/gmail_client.py` (`cmd_run` — append a labeled pass after the starred pass)
- Test: `tests/test_gmail_client.py`

**Interfaces:**
- Consumes: `resolve_label_ids`, `list_labeled_messages`, `matched_corpus_labels`, `parse_message`, `ce.write_collected`, `enrich_email`.
- Produces: `cmd_run`'s JSON summary gains `labeled_written`, `labeled_duplicate`, `labeled_failed`, `missing_labels`. Labeled emails are written with `gmail_corpus_labels` and are NOT archived.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_gmail_client.py` (stubs the network + write so it tests the labeled-pass wiring):

```python
def test_cmd_run_labeled_pass_records_labels_and_does_not_archive(tmp_path, monkeypatch):
    import types
    written = []
    monkeypatch.setattr(gc, "get_service", lambda: object())
    monkeypatch.setattr(gc, "list_starred_messages", lambda svc, mx=None: [])  # no starred
    monkeypatch.setattr(gc, "resolve_label_ids", lambda svc, names=None: ({"MLOps": "L1"}, []))
    monkeypatch.setattr(gc, "list_labeled_messages",
                        lambda svc, ids, mx=None: [{"id": "m1", "labelIds": ["L1"]}])
    monkeypatch.setattr(gc, "parse_message", lambda full: {
        "message_id": "m1", "from": "a@b.c", "subject": "S", "date_received": "2026-06-18", "body": "b"})
    archived = []
    monkeypatch.setattr(gc, "archive_message", lambda svc, mid: archived.append(mid))
    monkeypatch.setattr(gc, "enrich_email", lambda *a, **k: {"captured": 0, "skipped": 0})

    def fake_write(meta, body):
        written.append(meta)
        return {"status": "written", "path": str(tmp_path / "x.md")}
    monkeypatch.setattr(gc.ce, "write_collected", fake_write)

    rc = gc.cmd_run(gc._args(["run"]))
    assert rc == 0
    assert written and written[0]["gmail_corpus_labels"] == ["MLOps"]   # labels recorded
    assert archived == []                                              # NOT archived
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_gmail_client.py -k labeled_pass -v`
Expected: FAIL (no labeled pass yet — `written` empty / no `gmail_corpus_labels`).

- [ ] **Step 3: Append the labeled pass to `cmd_run`**

In `bin/gmail_client.py` `cmd_run`, immediately BEFORE the final `print(json.dumps({...}))`, insert the labeled pass and extend the printed summary. Replace the existing final print block:

```python
    print(json.dumps({
        "found": found, "written": written, "duplicate": dup,
        "failed": failed, "archived": archived,
        "links_captured": links_captured, "links_skipped": links_skipped,
        "dry_run": bool(args.dry_run), "paths": paths,
    }, indent=2))
    return 0
```

with:

```python
    # --- Labeled pass: collect configured corpus labels. NO archive here — the
    # un-label/archive is deferred to `reap-labels`, gated on corpus_ingested. ---
    name_to_id, missing_labels = resolve_label_ids(service)
    labeled_written = labeled_dup = labeled_failed = 0
    for full in list_labeled_messages(service, list(name_to_id.values()), args.max):
        info = parse_message(full)
        labels = matched_corpus_labels(full.get("labelIds", []), name_to_id)
        try:
            res = ce.write_collected(
                {"gmail_message_id": info["message_id"], "from": info["from"],
                 "subject": info["subject"], "date_received": info["date_received"],
                 "collected_at": collected_at, "gmail_corpus_labels": labels},
                info["body"])
        except Exception:
            labeled_failed += 1
            continue
        status = res.get("status")
        if status == "written":
            labeled_written += 1
            paths.append(res["path"])
        elif status == "duplicate":
            labeled_dup += 1
        else:
            labeled_failed += 1
            continue
        if not args.no_links and status == "written":
            e = enrich_email(res["path"], info["message_id"], info["body"],
                             collected_at, args.max_links)
            links_captured += e["captured"]
            links_skipped += e["skipped"]

    print(json.dumps({
        "found": found, "written": written, "duplicate": dup,
        "failed": failed, "archived": archived,
        "labeled_written": labeled_written, "labeled_duplicate": labeled_dup,
        "labeled_failed": labeled_failed, "missing_labels": missing_labels,
        "links_captured": links_captured, "links_skipped": links_skipped,
        "dry_run": bool(args.dry_run), "paths": paths,
    }, indent=2))
    return 0
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_gmail_client.py -q`
Expected: PASS (labeled-pass test + existing).

- [ ] **Step 5: Commit**

```bash
git add bin/gmail_client.py tests/test_gmail_client.py
git commit -m "feat(gmail): cmd_run labeled pass — collect corpus labels, defer archive"
```

---

### Task 4: `gmail_client` — `reap-labels` post-ingest subcommand

**Files:**
- Modify: `bin/gmail_client.py` (add `cmd_reap_labels`; register the `reap-labels` subparser in `main`)
- Test: `tests/test_gmail_client.py`

**Interfaces:**
- Consumes: `ce.labeled_reapable`, `resolve_label_ids`, a Gmail `service` (mocked).
- Produces: `cmd_reap_labels(args) -> int`; the `reap-labels` subcommand. For each ingested labeled source, calls `messages().modify(removeLabelIds=[matched ids + "INBOX"])`. JSON: `{relabeled, archived, dry_run, errors}`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_gmail_client.py`:

```python
class _ModMessages:
    def __init__(self, calls): self._calls = calls
    def modify(self, userId=None, id=None, body=None):
        self._calls.append({"id": id, "removeLabelIds": body["removeLabelIds"]}); return self
    def execute(self): return {}


class _ModSvc:
    def __init__(self, labels, calls):
        self._labels = labels; self._calls = calls
    def users(self): return self
    def labels(self): return _Labels(self._labels)
    def messages(self): return _ModMessages(self._calls)


def test_reap_labels_removes_matched_labels_and_inbox(monkeypatch):
    monkeypatch.setattr(gc.ce, "labeled_reapable",
                        lambda: [{"gmail_message_id": "m1", "gmail_corpus_labels": ["MLOps", "Ml"]}])
    calls = []
    monkeypatch.setattr(gc, "get_service",
                        lambda: _ModSvc([{"name": "MLOps", "id": "L1"}, {"name": "Ml", "id": "L2"}], calls))
    rc = gc.cmd_reap_labels(gc._args(["reap-labels"]))
    assert rc == 0
    assert calls == [{"id": "m1", "removeLabelIds": ["L1", "L2", "INBOX"]}]


def test_reap_labels_dry_run_calls_no_modify(monkeypatch):
    monkeypatch.setattr(gc.ce, "labeled_reapable",
                        lambda: [{"gmail_message_id": "m1", "gmail_corpus_labels": ["MLOps"]}])
    calls = []
    monkeypatch.setattr(gc, "get_service", lambda: _ModSvc([{"name": "MLOps", "id": "L1"}], calls))
    rc = gc.cmd_reap_labels(gc._args(["reap-labels", "--dry-run"]))
    assert rc == 0
    assert calls == []   # dry-run never mutates Gmail
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_gmail_client.py -k reap_labels -v`
Expected: FAIL (`cmd_reap_labels` / `reap-labels` not defined).

- [ ] **Step 3: Implement `cmd_reap_labels` and register the subcommand**

Add the function to `bin/gmail_client.py`:

```python
def cmd_reap_labels(args) -> int:
    """Post-ingest: for each corpus-labeled email already in the corpus, remove the
    matched corpus label(s) + INBOX (archive). Gated on corpus_ingested; idempotent."""
    items = ce.labeled_reapable()
    if not items:
        print(json.dumps({"relabeled": 0, "archived": 0,
                          "dry_run": bool(args.dry_run), "note": "nothing-to-reap"}))
        return 0
    service = get_service()
    name_to_id, _ = resolve_label_ids(service)
    relabeled = errors = 0
    for it in items:
        ids = [name_to_id[n] for n in it["gmail_corpus_labels"] if n in name_to_id]
        if not ids:
            continue
        if args.dry_run:
            relabeled += 1
            continue
        try:
            service.users().messages().modify(
                userId="me", id=it["gmail_message_id"],
                body={"removeLabelIds": ids + ["INBOX"]}).execute()
            relabeled += 1
        except Exception:  # noqa: BLE001 — one bad message must not abort the batch
            errors += 1
    print(json.dumps({"relabeled": relabeled, "archived": relabeled,
                      "dry_run": bool(args.dry_run), "errors": errors}))
    return 0
```

Register the subparser in `main` (alongside the other `sub.add_parser(...)` calls):

```python
    prl = sub.add_parser("reap-labels",
                         help="Post-ingest: un-label + archive corpus-labeled emails.")
    prl.add_argument("--dry-run", action="store_true", help="Report only; no Gmail mutation.")
    prl.set_defaults(func=cmd_reap_labels)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_gmail_client.py -q`
Expected: PASS (reap-labels tests + existing).

- [ ] **Step 5: Commit**

```bash
git add bin/gmail_client.py tests/test_gmail_client.py
git commit -m "feat(gmail): reap-labels — post-ingest un-label + archive (gated, idempotent)"
```

---

### Task 5: Wire `reap-labels` into the scheduled run (post-ingest)

**Files:**
- Modify: `bin/scheduled_run.py` (add `run_email_relabel`; call it after `move_processed_inbox`)
- Test: `tests/test_scheduled_run.py`

**Interfaces:**
- Consumes: `gmail_client.py reap-labels` via subprocess (the `_subprocess_run` seam).
- Produces: `run_email_relabel(*, _subprocess_run=None) -> dict`; `tallies["email_relabel"]` in the run.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_scheduled_run.py`:

```python
class TestEmailRelabel:
    def test_run_email_relabel_invokes_reap_labels(self):
        called = []

        def fake_run(cmd, **kwargs):
            called.append(" ".join(cmd))
            import types
            return types.SimpleNamespace(returncode=0, stdout='{"relabeled": 0}', stderr="")

        result = scheduled_run.run_email_relabel(_subprocess_run=fake_run)
        assert any("gmail_client.py" in s and "reap-labels" in s for s in called), called
        assert result.get("relabeled") == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_scheduled_run.py -k run_email_relabel -v`
Expected: FAIL (`run_email_relabel` not defined).

- [ ] **Step 3: Add `run_email_relabel` and call it post-ingest**

In `bin/scheduled_run.py`, add the function (near `run_collectors`):

```python
def run_email_relabel(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `gmail_client.py reap-labels` to un-label + archive
    corpus-labeled emails now in the corpus. Gated on corpus_ingested inside the
    subcommand. Failure is recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "gmail_client.py"), "reap-labels"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}
```

In `main`, inside the non-dry-run `else:` branch, immediately AFTER the `move_processed_inbox` try/except block (the `tallies["inbox_move"] = ...` block around line 808-812), insert:

```python
                # Post-ingest: un-label + archive corpus-labeled emails now in the
                # corpus (gated on corpus_ingested). Failure must NOT abort the run.
                try:
                    tallies["email_relabel"] = run_email_relabel()
                except Exception as exc:  # noqa: BLE001
                    tallies["email_relabel"] = {"status": "failed", "error": str(exc)}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_scheduled_run.py -q`
Expected: PASS (new test + existing).

- [ ] **Step 5: Commit**

```bash
git add bin/scheduled_run.py tests/test_scheduled_run.py
git commit -m "feat(scheduled-run): run gmail reap-labels after the ingest phase"
```

---

### Task 6: Docs + full-suite gate

**Files:**
- Modify: `corpus/_config.md` (document the email-label collection + lifecycle)
- Modify: `corpus/_log.md` (append a `config` entry)

**Interfaces:** none (docs).

- [ ] **Step 1: Document in `corpus/_config.md`**

In the email section (near the `**Email collection**` note), add:

```markdown
**Label collection (corpus labels):** alongside starred mail, the `/collect-email`
run also collects messages under these Gmail labels (exact names; edit the
`CORPUS_LABELS` list in `bin/gmail_client.py`):
`Data Engineering`, `Data Engineering/databricks`, `Data Engineering/dbt`,
`Data Engineering/spark`, `Ml`, `ML Engineering`, `MLOps`, `Productivity`, `Prompting`.
Labeled emails record a `gmail_corpus_labels` frontmatter field and are NOT archived on
collection. After they are ingested (`corpus_ingested: true`), `bin/gmail_client.py
reap-labels` removes the matched corpus label(s) + `INBOX` (archive) — run post-ingest by
the scheduled job. The starred flow is unchanged (de-star + archive on collection).
```

- [ ] **Step 2: Append a `config` entry to `corpus/_log.md`**

```markdown

## [2026-06-18 HH:MM] config | Gmail label collection + post-ingest un-label/archive
- /collect-email now also collects 9 corpus labels (CORPUS_LABELS in bin/gmail_client.py);
  labeled emails carry gmail_corpus_labels and are NOT archived on collect
- new `gmail_client.py reap-labels` removes matched label(s) + INBOX after corpus_ingested;
  wired into scheduled_run after the ingest phase. Starred flow unchanged.
- spec: docs/superpowers/specs/2026-06-18-gmail-label-collection-design.md
```

(Use the real current time for `HH:MM`.)

- [ ] **Step 3: Run the full suite as the gate**

Run: `python3 -m pytest tests/ -q`
Expected: PASS (all tests, incl. the new collect_email / gmail_client / scheduled_run ones).

- [ ] **Step 4: Commit**

```bash
git add corpus/_config.md corpus/_log.md
git commit -m "docs(gmail): document corpus-label email collection + reap-labels lifecycle"
```

---

## Notes for the executor

- **Smoke test after merge (optional, real Gmail):** `python3 bin/gmail_client.py reap-labels --dry-run` reports how many ingested labeled emails *would* be un-labeled/archived (no mutation). A full `python3 bin/gmail_client.py run --dry-run` collects starred + labeled without mutating Gmail.
- **reap-labels runs AFTER ingest only** — it is gated on `corpus_ingested`, so running it early is a no-op. Keep it out of the collection phase.
- **OAuth:** the `gmail.modify` scope is already granted (used for de-star/archive); `removeLabelIds` needs nothing more.
```
