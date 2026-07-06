#!/usr/bin/env python3
"""Tests for the EPUB book pipeline — stdlib extraction, chapter stubs, sha dedup, reaper."""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import book_client as bc  # noqa: E402
import collect_books as cb  # noqa: E402

CONTAINER = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

OPF = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Designing Data Systems</dc:title>
    <dc:creator>Jane Author</dc:creator>
  </metadata>
  <manifest>
    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>
    <item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>
    <item id="ch2" href="ch2.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine><itemref idref="cover"/><itemref idref="ch1"/><itemref idref="ch2"/></spine>
</package>"""

COVER = "<html><body><h1>Designing Data Systems</h1><p>by Jane Author</p></body></html>"


def _chapter_html(title: str) -> str:
    body = " ".join(["Reliable systems tolerate faults gracefully."] * 30)
    return f"<html><body><h1>{title}</h1><p>{body}</p><ul><li>point one</li></ul></body></html>"


def make_epub(path: Path) -> Path:
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr("META-INF/container.xml", CONTAINER)
        z.writestr("OEBPS/content.opf", OPF)
        z.writestr("OEBPS/cover.xhtml", COVER)
        z.writestr("OEBPS/ch1.xhtml", _chapter_html("Reliability"))
        z.writestr("OEBPS/ch2.xhtml", _chapter_html("Scalability"))
    return path


def test_extract_book_chapters_and_metadata(tmp_path):
    book = cb.extract_book(make_epub(tmp_path / "b.epub"))
    assert book["title"] == "Designing Data Systems"
    assert book["author"] == "Jane Author"
    titles = [c["title"] for c in book["chapters"]]
    assert titles == ["Reliability", "Scalability"]        # tiny cover skipped
    assert "## Reliability" in book["chapters"][0]["text"]
    assert "- point one" in book["chapters"][0]["text"]


def test_collect_writes_chapter_stubs_and_dedups(tmp_path, monkeypatch, capsys):
    watch = tmp_path / "Books"; watch.mkdir()
    make_epub(watch / "b.epub")
    inbox = tmp_path / "inbox"
    monkeypatch.setattr(cb, "INBOX", inbox)
    monkeypatch.setattr(cb, "DEDUP_DIRS", [inbox])
    assert bc.cmd_collect(bc._args(["collect", "--dir", str(watch)])) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["books"] == 1 and out["chapters"] == 2
    stubs = sorted(p.name for p in inbox.glob("book-*.md"))
    assert stubs == ["book-designing-data-systems-01-reliability.md",
                     "book-designing-data-systems-02-scalability.md"]
    text = (inbox / stubs[0]).read_text()
    assert "channel: book" in text and "chapter_title: Reliability" in text
    # second collect: sha dedup skips
    bc.cmd_collect(bc._args(["collect", "--dir", str(watch)]))
    out2 = json.loads(capsys.readouterr().out)
    assert out2["skipped"] == 1 and out2["books"] == 0


def test_file_moves_only_fully_ingested(tmp_path, monkeypatch, capsys):
    watch = tmp_path / "Books"; watch.mkdir()
    epub = make_epub(watch / "b.epub")
    inbox = tmp_path / "inbox"
    monkeypatch.setattr(cb, "INBOX", inbox)
    monkeypatch.setattr(cb, "DEDUP_DIRS", [inbox])
    bc.cmd_collect(bc._args(["collect", "--dir", str(watch)])); capsys.readouterr()
    stubs = sorted(inbox.glob("book-*.md"))

    # only one chapter ingested -> NOT moved
    s0 = stubs[0]; s0.write_text(s0.read_text().replace("---\n\n", "corpus_ingested: true\n---\n\n", 1))
    bc.cmd_file(bc._args(["file", "--dir", str(watch)]))
    assert json.loads(capsys.readouterr().out)["moved"] == 0
    assert epub.exists()

    # all chapters ingested -> moved to _processed/
    s1 = stubs[1]; s1.write_text(s1.read_text().replace("---\n\n", "corpus_ingested: true\n---\n\n", 1))
    bc.cmd_file(bc._args(["file", "--dir", str(watch)]))
    assert json.loads(capsys.readouterr().out)["moved"] == 1
    assert not epub.exists()
    assert (watch / "_processed" / "b.epub").exists()


def test_discover_skips_processed(tmp_path):
    watch = tmp_path / "Books"; (watch / "_processed").mkdir(parents=True)
    make_epub(watch / "new.epub")
    make_epub(watch / "_processed" / "old.epub")
    found = cb.discover(watch)
    assert [p.name for p in found] == ["new.epub"]
