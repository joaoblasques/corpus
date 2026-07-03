import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import query  # noqa: E402


# ===== UNIT 0 — OKF conformance: path constants =====

def test_log_path_constant_is_log_md():
    """LOG_PATH must point to corpus/log.md (OKF conformant name, not _log.md)."""
    assert query.LOG_PATH.name == "log.md", (
        f"LOG_PATH filename should be 'log.md', got {query.LOG_PATH.name!r}"
    )


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


def test_dedup_finds_match_in_youtube_dir(tmp_path):
    # Behavior check: a source already living in the youtube dedup dir is found,
    # proving youtube participates in dedup (not asserting the literal constant).
    inbox = tmp_path / "_inbox"
    web = tmp_path / "web"
    youtube = tmp_path / "youtube"
    youtube.mkdir()
    (youtube / "transcript.md").write_text(
        f"source_url: {query.ce.yaml_scalar('https://youtu.be/abcdefghijk')}\n",
        encoding="utf-8",
    )
    assert query.already_queued(
        "https://youtu.be/abcdefghijk", [inbox, web, youtube]
    ) is True


def test_dedup_dirs_constant_includes_expected_dirs():
    names = {p.name for p in query.DEDUP_DIRS}
    assert {"_inbox", "web", "youtube"} <= names


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


def test_build_web_document_emits_youtube_channel():
    meta = {
        "channel": "youtube",
        "source_url": "https://a.com/x",
        "via_query": "q",
        "fetched_at": "2026-06-12",
    }
    out = query.build_web_document(meta, "body")
    assert "channel: youtube" in out
    assert "channel: web" not in out


def test_build_web_document_defaults_channel_web():
    meta = {
        "source_url": "https://a.com/x",
        "via_query": "q",
        "fetched_at": "2026-06-12",
    }
    out = query.build_web_document(meta, "body")
    assert "channel: web" in out


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
        "what is X", _article(), "https://a.com/x",
        inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
    assert res["status"] == "written"
    assert res["source_url"] == "https://a.com/x"
    p = Path(res["path"])
    assert p.exists()
    content = p.read_text(encoding="utf-8")
    assert "via_query: what is X" in content
    assert 'source_url: "https://a.com/x"' in content
    assert "channel: web" in content


def test_queue_source_writes_youtube_channel(tmp_path):
    inbox = tmp_path / "_inbox"
    yt = {
        "title": "YouTube abc",
        "text": "[00:00] hi",
        "channel": "youtube",
    }
    res = query.queue_source(
        "what is X", yt, "https://youtu.be/abcdefghijk",
        inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
    assert res["status"] == "written"
    content = Path(res["path"]).read_text(encoding="utf-8")
    assert "channel: youtube" in content


def test_queue_source_duplicate_writes_nothing(tmp_path):
    inbox = tmp_path / "_inbox"
    inbox.mkdir()
    (inbox / "existing.md").write_text(
        f"source_url: {query.ce.yaml_scalar('https://a.com/x')}\n", encoding="utf-8"
    )
    before = set(inbox.glob("*.md"))
    res = query.queue_source(
        "what is X", _article(), "https://a.com/x",
        inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
    assert res["status"] == "duplicate"
    assert res["source_url"] == "https://a.com/x"
    assert set(inbox.glob("*.md")) == before


def test_queue_source_collision_distinct_paths(tmp_path):
    inbox = tmp_path / "_inbox"
    a = _article()
    b = _article()
    r1 = query.queue_source(
        "q", a, "https://a.com/one", inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
    r2 = query.queue_source(
        "q", b, "https://a.com/two", inbox=inbox, dedup_dirs=[inbox], at="2026-06-12"
    )
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


# ===== UNIT 4 — origin provenance (vault-delegated queries) =====

def test_resolve_origin_explicit_wins(monkeypatch):
    monkeypatch.setenv("CORPUS_QUERY_ORIGIN", "fromenv")
    assert query.resolve_origin("claudesidian") == "claudesidian"


def test_resolve_origin_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("CORPUS_QUERY_ORIGIN", "claudesidian")
    assert query.resolve_origin() == "claudesidian"


def test_resolve_origin_native_when_unset(monkeypatch):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    assert query.resolve_origin() == ""


def test_build_web_document_emits_origin_when_present():
    meta = {
        "source_url": "https://a.com/x",
        "via_query": "q",
        "query_origin": "claudesidian",
        "fetched_at": "2026-06-17",
    }
    out = query.build_web_document(meta, "body")
    assert "query_origin: claudesidian" in out
    # ordering: origin sits between via_query and fetched_at
    assert out.index("via_query:") < out.index("query_origin:") < out.index("fetched_at:")


def test_build_web_document_omits_origin_when_absent():
    # Native queries keep the original frontmatter shape — no origin line.
    meta = {"source_url": "https://a.com/x", "via_query": "q", "fetched_at": "2026-06-17"}
    out = query.build_web_document(meta, "body")
    assert "query_origin" not in out


def test_queue_source_writes_origin_from_arg(tmp_path, monkeypatch):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    inbox = tmp_path / "_inbox"
    res = query.queue_source(
        "what is X", _article(), "https://a.com/x",
        inbox=inbox, dedup_dirs=[inbox], at="2026-06-17", origin="claudesidian",
    )
    content = Path(res["path"]).read_text(encoding="utf-8")
    assert "query_origin: claudesidian" in content


def test_queue_source_writes_origin_from_env(tmp_path, monkeypatch):
    monkeypatch.setenv("CORPUS_QUERY_ORIGIN", "claudesidian")
    inbox = tmp_path / "_inbox"
    res = query.queue_source(
        "what is X", _article(), "https://a.com/x",
        inbox=inbox, dedup_dirs=[inbox], at="2026-06-17",
    )
    content = Path(res["path"]).read_text(encoding="utf-8")
    assert "query_origin: claudesidian" in content


def test_queue_source_native_omits_origin(tmp_path, monkeypatch):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    inbox = tmp_path / "_inbox"
    res = query.queue_source(
        "what is X", _article(), "https://a.com/x",
        inbox=inbox, dedup_dirs=[inbox], at="2026-06-17",
    )
    content = Path(res["path"]).read_text(encoding="utf-8")
    assert "query_origin" not in content


def test_log_gap_tags_origin(tmp_path, monkeypatch):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    log = tmp_path / "_log.md"
    query.log_gap("q", "a gap", [], "2026-06-17 10:00", log_path=log, origin="claudesidian")
    text = log.read_text(encoding="utf-8")
    assert "## [2026-06-17 10:00] query (origin: claudesidian) | q" in text


def test_log_gap_native_has_no_origin_tag(tmp_path, monkeypatch):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    log = tmp_path / "_log.md"
    query.log_gap("q", "a gap", [], "2026-06-17 10:00", log_path=log)
    text = log.read_text(encoding="utf-8")
    assert "## [2026-06-17 10:00] query | q" in text
    assert "origin:" not in text


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


def test_cli_fetch_and_queue_threads_origin(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(
        query, "_fetch", lambda url: {"title": "Fetched", "text": "body", "channel": "web"}
    )
    monkeypatch.setattr(query, "DEDUP_DIRS", [inbox])
    rc = query.main(
        ["fetch-and-queue", "--question", "q", "--url", "https://a.com/x",
         "--inbox", str(inbox), "--origin", "claudesidian"]
    )
    out = _capture(capsys)
    assert rc == 0
    assert "query_origin: claudesidian" in Path(out["path"]).read_text(encoding="utf-8")


def test_cli_log_gap_threads_origin(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("CORPUS_QUERY_ORIGIN", raising=False)
    log = tmp_path / "_log.md"
    monkeypatch.setattr(query, "LOG_PATH", log)
    rc = query.main(
        ["log-gap", "--question", "q", "--note", "a gap",
         "--at", "2026-06-17 10:00", "--origin", "claudesidian"]
    )
    out = _capture(capsys)
    assert rc == 0
    assert "## [2026-06-17 10:00] query (origin: claudesidian) | q" in log.read_text(encoding="utf-8")
