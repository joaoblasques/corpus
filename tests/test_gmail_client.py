import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gmail_client as gc  # noqa: E402


def _b64url(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")


def test_header_case_insensitive():
    headers = [{"name": "From", "value": "a@b.com"}, {"name": "Subject", "value": "Hi"}]
    assert gc.header(headers, "from") == "a@b.com"
    assert gc.header(headers, "SUBJECT") == "Hi"
    assert gc.header(headers, "missing") == ""


def test_extract_body_prefers_plain():
    payload = {
        "mimeType": "multipart/alternative",
        "parts": [
            {"mimeType": "text/plain", "body": {"data": _b64url("plain wins")}},
            {"mimeType": "text/html", "body": {"data": _b64url("<p>html loses</p>")}},
        ],
    }
    assert gc.extract_body(payload) == "plain wins"


def test_extract_body_falls_back_to_html():
    payload = {
        "mimeType": "text/html",
        "body": {"data": _b64url("<p>Hello</p><p>World</p>")},
    }
    out = gc.extract_body(payload)
    assert "Hello" in out and "World" in out
    assert "<p>" not in out


def test_extract_body_nested_multipart():
    payload = {
        "mimeType": "multipart/mixed",
        "parts": [
            {"mimeType": "multipart/alternative", "parts": [
                {"mimeType": "text/plain", "body": {"data": _b64url("deep body")}},
            ]},
            {"mimeType": "application/pdf", "body": {"attachmentId": "x"}},
        ],
    }
    assert gc.extract_body(payload) == "deep body"


def test_extract_body_empty_when_no_text():
    assert gc.extract_body({"mimeType": "image/png", "body": {}}) == ""


def test_html_to_text_strips_and_unescapes():
    assert gc.html_to_text("<p>Tom &amp; Jerry<br>line2</p>") == "Tom & Jerry\nline2"


def test_message_date_from_header():
    msg = {"payload": {"headers": [{"name": "Date", "value": "Mon, 09 Jun 2026 14:30:00 +0000"}]}}
    assert gc.message_date(msg) == "2026-06-09"


def test_message_date_falls_back_to_internaldate():
    # 2026-06-09T00:00:00Z in ms
    ms = int(1781000000)  # arbitrary epoch seconds
    msg = {"payload": {"headers": []}, "internalDate": str(ms * 1000)}
    assert gc.message_date(msg).count("-") == 2  # well-formed YYYY-MM-DD


def test_parse_message_full():
    msg = {
        "id": "MSG123",
        "internalDate": "1717939800000",
        "payload": {
            "headers": [
                {"name": "From", "value": "Jane <jane@example.com>"},
                {"name": "Subject", "value": "Weekly digest"},
                {"name": "Date", "value": "Mon, 09 Jun 2026 14:30:00 +0000"},
            ],
            "mimeType": "text/plain",
            "body": {"data": _b64url("The newsletter body.")},
        },
    }
    info = gc.parse_message(msg)
    assert info["message_id"] == "MSG123"
    assert info["from"] == "Jane <jane@example.com>"
    assert info["subject"] == "Weekly digest"
    assert info["date_received"] == "2026-06-09"
    assert info["body"] == "The newsletter body."


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
