import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_pdf as cp  # noqa: E402


def _make_pdf(path, text, title="", author=""):
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_textbox(fitz.Rect(50, 50, 550, 750), text, fontsize=12)
    if title or author:
        doc.set_metadata({"title": title, "author": author})
    doc.save(str(path)); doc.close()


def test_extract_reads_text_and_metadata(tmp_path):
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf, "Hello world this is a real test pdf body. " * 20,
              title="My Test PDF", author="Tester")
    r = cp.extract(str(pdf))
    assert "Hello world" in r["markdown"]
    assert r["title"] == "My Test PDF"
    assert r["author"] == "Tester"
    assert r["pages"] == 1
    assert r["words"] >= 50


def test_extract_does_not_pollute_stdout(tmp_path, capfd):
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf, "Hello world body text here. " * 30)
    cp.extract(str(pdf))
    out = capfd.readouterr().out
    assert "Tesseract" not in out and "Document parser" not in out


def test_extract_disables_ocr(tmp_path, monkeypatch):
    """pymupdf4llm 1.27 OCRs every image page by default — one image-heavy PDF then wedges
    the whole batch for tens of minutes. extract() must pass use_ocr=False to skip it."""
    import pymupdf4llm
    captured = {}

    def fake_to_markdown(path, **kw):
        captured.update(kw)
        return "# Title\n" + ("body text " * 20)

    monkeypatch.setattr(pymupdf4llm, "to_markdown", fake_to_markdown)
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf, "hello world " * 40)
    r = cp.extract(str(pdf))
    assert captured.get("use_ocr") is False
    assert "body text" in r["markdown"]


def test_extract_falls_back_when_use_ocr_unsupported(tmp_path, monkeypatch):
    """Older pymupdf4llm has no use_ocr kwarg (and no OCR-by-default) — extract must still work."""
    import pymupdf4llm
    calls = []

    def fake_to_markdown(path, **kw):
        calls.append(kw)
        if "use_ocr" in kw:                       # simulate the old signature rejecting it
            raise TypeError("unexpected keyword argument 'use_ocr'")
        return "# Title\n" + ("legacy body " * 20)

    monkeypatch.setattr(pymupdf4llm, "to_markdown", fake_to_markdown)
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf, "hello " * 40)
    r = cp.extract(str(pdf))
    assert len(calls) == 2                         # tried with kwarg, then fell back without
    assert "legacy body" in r["markdown"]


def test_extract_title_falls_back_to_stem(tmp_path):
    pdf = tmp_path / "Untitled Paper.pdf"
    _make_pdf(pdf, "some text " * 30)
    r = cp.extract(str(pdf))
    assert r["title"] == "Untitled Paper"


def test_discover_recurses_but_skips_processed(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4 a")
    (tmp_path / "b.PDF").write_bytes(b"%PDF-1.4 b")
    (tmp_path / "notes.md").write_text("x")
    (tmp_path / ".hidden.pdf").write_bytes(b"%PDF x")
    (tmp_path / "~$tmp.pdf").write_bytes(b"%PDF x")
    sub = tmp_path / "Invoices"; sub.mkdir()
    (sub / "inv.pdf").write_bytes(b"%PDF inv")          # real subfolder → COLLECTED
    proc = tmp_path / "_processed"; proc.mkdir()
    (proc / "old.pdf").write_bytes(b"%PDF x")           # already filed → skipped
    names = sorted(d["filename"] for d in cp.discover(tmp_path))
    assert names == ["a.pdf", "b.PDF", "inv.pdf"]       # subfolder in; _processed/hidden/temp out


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


def test_processable_selects_only_ingested(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-a.md").write_text(
        "---\nchannel: pdf\npdf_origin: a.pdf\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    (raw / "pdf-b.md").write_text(
        "---\nchannel: pdf\npdf_origin: b.pdf\n---\nx", encoding="utf-8")  # not ingested
    # processable() returns (source_path, pdf_origin) tuples; source_path is None when the
    # stub predates the subfolder-aware collector (only pdf_origin recorded).
    assert cp.processable(dirs=[raw]) == [(None, "a.pdf")]


def test_discover_recurses_into_subfolders(tmp_path):
    (tmp_path / "top.pdf").write_bytes(b"%PDF-1.4 top")
    sub = tmp_path / "Invoices"; sub.mkdir()
    (sub / "nested.pdf").write_bytes(b"%PDF-1.4 nested")
    deep = sub / "2026"; deep.mkdir()
    (deep / "deep.PDF").write_bytes(b"%PDF-1.4 deep")          # uppercase ext too
    (sub / "notes.txt").write_text("not a pdf", encoding="utf-8")
    names = sorted(d["filename"] for d in cp.discover(watch_dir=tmp_path))
    assert names == ["deep.PDF", "nested.pdf", "top.pdf"]      # subfolders + nested, .txt ignored
