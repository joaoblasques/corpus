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
