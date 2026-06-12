import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_obsidian as co  # noqa: E402


def test_is_included_resources():
    assert co.is_included("03_Resources/Articles/Clean Code.md") is True
    assert co.is_included("03_Resources/Study Notes/CAP.md") is True
    assert co.is_included("00_Inbox/Clippings/scrape/merkle-trees-scrape.md") is True


def test_is_included_excludes():
    assert co.is_included("03_Resources/llm-wiki-system/CLAUDE.md") is False  # corpus mirror
    assert co.is_included("01_Projects/foo.md") is False                      # not a knowledge dir
    assert co.is_included("00_Inbox/Clippings/articles_processed.md") is False # ledger
    assert co.is_included("03_Resources/Articles/README.md") is False         # readme
    assert co.is_included("03_Resources/Books/cheatsheet.pdf") is False        # binary


def test_classify():
    assert co.classify("00_Inbox/Clippings/articles to process.md") == "url-list"
    assert co.classify("00_Inbox/Clippings/TO SCRAPE.md") == "url-list"
    assert co.classify("03_Resources/Articles/Clean Code.md") == "note"


def test_parse_url_list():
    text = "\nhttps://a.com/x\n\nsome prose\nhttps://b.com/y?z=1\nhttps://a.com/x\n"
    assert co.parse_url_list(text) == ["https://a.com/x", "https://b.com/y?z=1"]


def test_read_note_extracts_title_tags_body(tmp_path):
    f = tmp_path / "n.md"
    f.write_text("---\ntitle: \"Clean Code\"\ntags:\n  - python\n  - clean-code\n---\n\nBody line.\n",
                 encoding="utf-8")
    title, tags, body = co.read_note(str(f))
    assert title == "Clean Code"
    assert tags == ["python", "clean-code"]
    assert body.strip() == "Body line."


def test_read_note_no_frontmatter_uses_stem(tmp_path):
    f = tmp_path / "Just A Note.md"
    f.write_text("plain body", encoding="utf-8")
    title, tags, body = co.read_note(str(f))
    assert title == "Just A Note" and tags == [] and body.strip() == "plain body"


def test_note_filename(tmp_path):
    p = co.note_filename("03_Resources/Articles/Clean Code!.md", tmp_path)
    assert p.name == "notes-clean-code.md"


def test_build_note_source():
    doc = co.build_note_source(
        {"vault_origin": "03_Resources/Articles/Clean Code.md", "title": "Clean: Code",
         "tags": ["python"], "collected_at": "2026-06-12"}, "Body text.")
    assert "channel: notes" in doc
    assert "source: obsidian" in doc
    assert "vault_origin: 03_Resources/Articles/Clean Code.md" in doc
    assert 'title: "Clean: Code"' in doc
    assert "  - python" in doc
    assert doc.rstrip().endswith("Body text.")


def test_build_url_source():
    doc = co.build_url_source(
        {"source_url": "https://a.com/x", "via_vault_list": "00_Inbox/Clippings/articles to process.md",
         "title": "A", "collected_at": "2026-06-12"}, "Article body")
    assert "channel: web" in doc
    assert "source_url: https://a.com/x" in doc
    assert "via_vault_list: 00_Inbox/Clippings/articles to process.md" in doc
    assert doc.rstrip().endswith("Article body")


def test_fm_field():
    assert co.fm_field("---\nvault_origin: a/b.md\n---\n", "vault_origin") == "a/b.md"
    assert co.fm_field("no fm", "vault_origin") is None


def test_is_vault_note_ingested(tmp_path):
    a = tmp_path / "a.md"; a.write_text("---\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    b = tmp_path / "b.md"; b.write_text("---\ntitle: x\n---\ny", encoding="utf-8")
    assert co.is_vault_note_ingested(str(a)) is True
    assert co.is_vault_note_ingested(str(b)) is False


def test_already_collected_vault(tmp_path):
    d = tmp_path / "inbox"; d.mkdir()
    (d / "notes-x.md").write_text("---\nvault_origin: 03_Resources/Articles/X.md\n---\n", encoding="utf-8")
    assert co.already_collected_vault("03_Resources/Articles/X.md", [d]) is True
    assert co.already_collected_vault("03_Resources/Articles/Y.md", [d]) is False


def test_url_already_collected(tmp_path):
    d = tmp_path / "web"; d.mkdir()
    (d / "web-x.md").write_text("---\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    assert co.url_already_collected("https://a.com/x", [d]) is True
    assert co.url_already_collected("https://a.com/z", [d]) is False
