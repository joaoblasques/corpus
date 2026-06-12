import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import query  # noqa: E402


# ===== UNIT 1 — already_queued =====

def test_already_queued_true_when_needle_present(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "a.md").write_text(
        query.build_web_document(
            {"source_url": "https://a.com/x", "via_query": "q", "fetched_at": "2026-06-12"},
            "body",
        ),
        encoding="utf-8",
    )
    assert query.already_queued("https://a.com/x", [d]) is True


def test_already_queued_false_when_absent(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "a.md").write_text(
        query.build_web_document(
            {"source_url": "https://a.com/x", "via_query": "q", "fetched_at": "2026-06-12"},
            "body",
        ),
        encoding="utf-8",
    )
    assert query.already_queued("https://b.com/y", [d]) is False


def test_already_queued_partial_url_does_not_match(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "a.md").write_text(
        query.build_web_document(
            {"source_url": "https://a.com/x", "via_query": "q", "fetched_at": "2026-06-12"},
            "body",
        ),
        encoding="utf-8",
    )
    # The serialized line ends at the full URL; a query for the prefix must not match
    # (needle is line-anchored with a trailing newline).
    assert query.already_queued("https://a.com/", [d]) is False


def test_already_queued_skips_unreadable_files(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    needle_line = f"source_url: {query.ce.yaml_scalar('https://a.com/x')}\n"
    # Binary / undecodable content must be swallowed, not raise.
    (d / "bin.md").write_bytes(b"\xff\xfe\x00\x01" + needle_line.encode("utf-8"))
    (d / "ok.md").write_text(needle_line, encoding="utf-8")
    assert query.already_queued("https://a.com/x", [d]) is True


def test_already_queued_missing_dir_skipped(tmp_path):
    missing = tmp_path / "nope"
    assert query.already_queued("https://a.com/x", [missing]) is False


def test_dedup_dirs_constant_defaults():
    names = [p.name for p in query.DEDUP_DIRS]
    assert names == ["_inbox", "web", "youtube"]


# ===== UNIT 2 — build_web_document =====

def test_build_web_document_structure():
    meta = {
        "source_url": "https://a.com/x",
        "via_query": "what is X",
        "fetched_at": "2026-06-12",
    }
    out = query.build_web_document(meta, "  the body  ")
    assert out.startswith("---\n")
    assert "channel: web" in out
    # URL contains a colon, so yaml_scalar quotes it.
    assert 'source_url: "https://a.com/x"' in out
    assert "via_query: what is X" in out
    assert "fetched_at: 2026-06-12" in out
    # frontmatter closes then stripped body
    assert "---\n\nthe body\n" in out
    assert out.endswith("\n")


def test_build_web_document_quotes_question_with_colon():
    question = 'Why: "edge" cases, really?'
    meta = {
        "source_url": "https://a.com/x",
        "via_query": question,
        "fetched_at": "2026-06-12",
    }
    out = query.build_web_document(meta, "body")
    fm = out.split("---")[1]
    parsed = yaml.safe_load(fm)
    assert parsed["via_query"] == question
    assert parsed["source_url"] == "https://a.com/x"


def test_build_web_document_strips_body_and_trailing_newline():
    meta = {"source_url": "u", "via_query": "q", "fetched_at": "2026-06-12"}
    out = query.build_web_document(meta, "\n\n  hello world  \n\n")
    assert out.endswith("hello world\n")
    assert "\n\nhello world\n" in out


# ===== UNIT 3 — queue_source =====

def _article(title="My Article"):
    return {
        "title": title,
        "text": "Some article body.",
        "channel": "web",
        "source_url": "https://a.com/x",
    }


def test_queue_source_writes_file(tmp_path):
    inbox = tmp_path / "_inbox"
    res = query.queue_source(
        "what is X", _article(), inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
    assert res["status"] == "written"
    assert res["source_url"] == "https://a.com/x"
    p = Path(res["path"])
    assert p.exists()
    content = p.read_text(encoding="utf-8")
    assert "via_query: what is X" in content
    assert 'source_url: "https://a.com/x"' in content


def test_queue_source_duplicate_writes_nothing(tmp_path):
    inbox = tmp_path / "_inbox"
    inbox.mkdir()
    (inbox / "existing.md").write_text(
        f"source_url: {query.ce.yaml_scalar('https://a.com/x')}\n", encoding="utf-8"
    )
    before = set(inbox.glob("*.md"))
    res = query.queue_source(
        "what is X", _article(), inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
    assert res["status"] == "duplicate"
    assert res["source_url"] == "https://a.com/x"
    assert set(inbox.glob("*.md")) == before


def test_queue_source_collision_distinct_paths(tmp_path):
    inbox = tmp_path / "_inbox"
    a = dict(_article(), source_url="https://a.com/one")
    b = dict(_article(), source_url="https://a.com/two")
    r1 = query.queue_source("q", a, inbox=inbox, dedup_dirs=[inbox], at="2026-06-12")
    r2 = query.queue_source("q", b, inbox=inbox, dedup_dirs=[inbox], at="2026-06-12")
    assert r1["status"] == "written"
    assert r2["status"] == "written"
    assert r1["path"] != r2["path"]


# ===== UNIT 3 — log_gap =====

def test_log_gap_appends_well_formed_block(tmp_path):
    log = tmp_path / "_log.md"
    query.log_gap(
        "what is X",
        "no coverage of X",
        ["raw/_inbox/a.md", "raw/_inbox/b.md"],
        "2026-06-12 10:30",
        log_path=log,
    )
    text = log.read_text(encoding="utf-8")
    assert "## [2026-06-12 10:30] query | what is X" in text
    assert "- gap: no coverage of X" in text
    assert "- queued: raw/_inbox/a.md, raw/_inbox/b.md" in text


def test_log_gap_second_call_preserves_first(tmp_path):
    log = tmp_path / "_log.md"
    query.log_gap("first q", "gap one", [], "2026-06-12 10:00", log_path=log)
    query.log_gap("second q", "gap two", [], "2026-06-12 11:00", log_path=log)
    text = log.read_text(encoding="utf-8")
    assert "## [2026-06-12 10:00] query | first q" in text
    assert "## [2026-06-12 11:00] query | second q" in text
    assert text.index("first q") < text.index("second q")


def test_log_gap_empty_queued_writes_none(tmp_path):
    log = tmp_path / "_log.md"
    query.log_gap("q", "a gap", [], "2026-06-12 10:00", log_path=log)
    assert "- queued: none" in log.read_text(encoding="utf-8")


# ===== UNIT 3 — CLI =====

def _capture(capsys):
    return json.loads(capsys.readouterr().out.strip())


def test_cli_fetch_and_queue_success(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(
        query, "_fetch", lambda url: {"title": "Fetched", "text": "body", "channel": "web"}
    )
    # dedup against the inbox only so we don't touch the real raw/ dirs
    monkeypatch.setattr(query, "DEDUP_DIRS", [inbox])
    rc = query.main(
        ["fetch-and-queue", "--question", "what is X",
         "--url", "https://a.com/x", "--inbox", str(inbox)]
    )
    out = _capture(capsys)
    assert rc == 0
    assert out["status"] == "written"
    assert Path(out["path"]).exists()


def test_cli_fetch_and_queue_failure(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"

    def boom(url):
        raise ValueError(f"unsupported url: {url}")

    monkeypatch.setattr(query, "_fetch", boom)
    monkeypatch.setattr(query, "DEDUP_DIRS", [inbox])
    rc = query.main(
        ["fetch-and-queue", "--question", "q",
         "--url", "https://a.com/bad.pdf", "--inbox", str(inbox)]
    )
    out = _capture(capsys)
    assert rc == 1
    assert out["status"] == "error"
    assert "unsupported" in out["error"]
    assert out["url"] == "https://a.com/bad.pdf"
    assert not inbox.exists() or not list(inbox.glob("*.md"))


def test_cli_fetch_and_queue_duplicate(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    inbox.mkdir()
    (inbox / "existing.md").write_text(
        f"source_url: {query.ce.yaml_scalar('https://a.com/x')}\n", encoding="utf-8"
    )
    monkeypatch.setattr(
        query, "_fetch", lambda url: {"title": "Fetched", "text": "body", "channel": "web"}
    )
    monkeypatch.setattr(query, "DEDUP_DIRS", [inbox])
    before = set(inbox.glob("*.md"))
    rc = query.main(
        ["fetch-and-queue", "--question", "q",
         "--url", "https://a.com/x", "--inbox", str(inbox)]
    )
    out = _capture(capsys)
    assert rc == 0
    assert out["status"] == "duplicate"
    assert set(inbox.glob("*.md")) == before


def test_cli_log_gap(tmp_path, monkeypatch, capsys):
    log = tmp_path / "_log.md"
    monkeypatch.setattr(query, "LOG_PATH", log)
    rc = query.main(
        ["log-gap", "--question", "q", "--note", "a gap",
         "--at", "2026-06-12 10:00", "--queued", "raw/_inbox/a.md,raw/_inbox/b.md"]
    )
    out = _capture(capsys)
    assert rc == 0
    assert out["status"] == "logged"
    text = log.read_text(encoding="utf-8")
    assert "## [2026-06-12 10:00] query | q" in text
    assert "- queued: raw/_inbox/a.md, raw/_inbox/b.md" in text
