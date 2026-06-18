import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import pdf_client as pc  # noqa: E402


def test_collect_writes_pdf_source(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF-1.4 hello")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(pc, "extract", lambda p: {
        "markdown": "real body " * 40, "title": "A", "author": "Jo", "pages": 3, "words": 80})
    rc = pc.cmd_collect(pc._args(["collect", "--dir", str(watch)]))
    assert rc == 0
    files = list(inbox.glob("pdf-*.md"))
    assert len(files) == 1
    text = files[0].read_text()
    assert "channel: pdf" in text and "pdf_origin: a.pdf" in text


def test_collect_low_text_guard_skips(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "scan.pdf").write_bytes(b"%PDF-1.4 img")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(pc, "extract", lambda p: {
        "markdown": "two words", "title": "scan", "author": "", "pages": 5, "words": 2})
    pc.cmd_collect(pc._args(["collect", "--dir", str(watch)]))
    assert list(inbox.glob("pdf-*.md")) == []          # nothing written
    assert (watch / "scan.pdf").exists()                # left in place


def test_collect_dedup_skips_already_collected(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF-1.4 hello")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    sha = pc.cp.content_sha(str(watch / "a.pdf"))
    (inbox / "pdf-a.md").write_text(f"---\nchannel: pdf\ncontent_sha: {sha}\n---\nx", encoding="utf-8")
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    calls = []
    monkeypatch.setattr(pc, "extract", lambda p: calls.append(p) or {
        "markdown": "x " * 60, "title": "A", "author": "", "pages": 1, "words": 60})
    pc.cmd_collect(pc._args(["collect", "--dir", str(watch)]))
    assert calls == []                                  # extract never called (deduped)


def test_collect_dry_run_writes_nothing(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF-1.4 hello")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(pc, "extract", lambda p: {
        "markdown": "x " * 60, "title": "A", "author": "", "pages": 1, "words": 60})
    pc.cmd_collect(pc._args(["collect", "--dir", str(watch), "--dry-run"]))
    assert list(inbox.glob("pdf-*.md")) == []


def test_file_moves_only_ingested_pdf(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF a")
    (watch / "b.pdf").write_bytes(b"%PDF b")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-a.md").write_text(
        "---\nchannel: pdf\npdf_origin: a.pdf\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    (raw / "pdf-b.md").write_text(
        "---\nchannel: pdf\npdf_origin: b.pdf\n---\nx", encoding="utf-8")
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [raw])
    rc = pc.cmd_file(pc._args(["file", "--dir", str(watch)]))
    assert rc == 0
    assert not (watch / "a.pdf").exists()                       # moved
    assert (watch / "_processed" / "a.pdf").exists()
    assert (watch / "b.pdf").exists()                            # not ingested -> stays


def test_file_rejects_path_traversal(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    outside = tmp_path / "etc"; outside.mkdir()
    (outside / "x.pdf").write_bytes(b"secret")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-evil.md").write_text(
        "---\nchannel: pdf\npdf_origin: ../etc/x.pdf\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [raw])
    pc.cmd_file(pc._args(["file", "--dir", str(watch)]))
    assert (outside / "x.pdf").exists()                          # never touched
