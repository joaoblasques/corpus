import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_pdf as cp  # noqa: E402


def test_discover_finds_top_level_pdfs_only(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4 a")
    (tmp_path / "b.PDF").write_bytes(b"%PDF-1.4 b")
    (tmp_path / "notes.md").write_text("x")
    (tmp_path / ".hidden.pdf").write_bytes(b"%PDF x")
    (tmp_path / "~$tmp.pdf").write_bytes(b"%PDF x")
    proc = tmp_path / "_processed"; proc.mkdir()
    (proc / "old.pdf").write_bytes(b"%PDF x")
    names = sorted(d["filename"] for d in cp.discover(tmp_path))
    assert names == ["a.pdf", "b.PDF"]


def test_content_sha_stable(tmp_path):
    f = tmp_path / "x.pdf"; f.write_bytes(b"hello pdf bytes")
    assert cp.content_sha(str(f)) == cp.content_sha(str(f))
    assert len(cp.content_sha(str(f))) == 64


def test_pdf_filename(tmp_path):
    p = cp.pdf_filename("Deep Learning Book!.pdf", tmp_path)
    assert p.name == "pdf-deep-learning-book.md"


def test_build_pdf_source_has_frontmatter():
    doc = cp.build_pdf_source(
        {"pdf_origin": "paper.pdf", "source_path": "/d/paper.pdf", "title": "A Paper",
         "author": "Jo", "pages": 12, "content_sha": "abc123", "collected_at": "2026-06-18"},
        "body text here")
    assert "channel: pdf" in doc
    assert "pdf_origin: paper.pdf" in doc
    assert "content_sha: abc123" in doc
    assert "pages: 12" in doc
    assert doc.rstrip().endswith("body text here")


def test_already_collected_detects_prior_sha(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-x.md").write_text("---\nchannel: pdf\ncontent_sha: deadbeef\n---\nbody", encoding="utf-8")
    assert cp.already_collected("deadbeef", dirs=[raw]) is True
    assert cp.already_collected("0000", dirs=[raw]) is False
