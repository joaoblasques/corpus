import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "website" / "hooks"))
import site_stats as st  # noqa: E402


def test_reads_header_counts(tmp_path):
    idx = tmp_path / "_index.md"
    idx.write_text(
        "# Corpus Index\n> Last updated: 2026-06-21 02:00 | Total pages: 213 | Total sources: 568\n",
        encoding="utf-8",
    )
    (tmp_path / "ai-engineering").mkdir()
    (tmp_path / "data-engineering").mkdir()
    (tmp_path / "_meta").mkdir()  # underscore dirs are not domains
    s = st.read_corpus_stats(index_path=idx)
    assert s["pages"] == 213 and s["sources"] == 568 and s["domains"] == 2


def test_missing_file_falls_back(tmp_path):
    s = st.read_corpus_stats(index_path=tmp_path / "nope.md")
    assert s["pages"] >= 1 and s["sources"] >= 1 and s["domains"] >= 1  # fallback, no raise


def test_garbled_header_falls_back(tmp_path):
    idx = tmp_path / "_index.md"
    idx.write_text("no counts here", encoding="utf-8")
    s = st.read_corpus_stats(index_path=idx)
    assert set(s) == {"pages", "sources", "domains"}
