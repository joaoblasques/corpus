import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
mig = importlib.import_module("okf_migrate")


def test_piped_wikilink():
    out, un = mig.rewrite_wikilinks("see [[ai-engineering/claude-code|Claude Code]] now")
    assert out == "see [Claude Code](/ai-engineering/claude-code.md) now"
    assert un == []


def test_unpiped_wikilink_titlecases_last_segment():
    out, _ = mig.rewrite_wikilinks("[[ai-engineering/context-window-management]]")
    assert out == "[Context Window Management](/ai-engineering/context-window-management.md)"


def test_bare_target_resolved_via_callback():
    out, un = mig.rewrite_wikilinks("[[anthropic|Anthropic]]",
                                    resolve=lambda t: "ai-engineering/anthropic")
    assert out == "[Anthropic](/ai-engineering/anthropic.md)"
    assert un == []


def test_bare_target_unresolved_becomes_plain_text():
    out, un = mig.rewrite_wikilinks("[[mystery|Mystery]]", resolve=lambda t: None)
    assert out == "Mystery"
    assert un == ["mystery"]


def test_code_fences_are_skipped():
    src = "real [[a/b|B]]\n```\ncode [[c/d|D]] literal\n```\nmore [[e/f|F]]"
    out, _ = mig.rewrite_wikilinks(src)
    assert "[B](/a/b.md)" in out and "[F](/e/f.md)" in out
    assert "[[c/d|D]]" in out            # untouched inside the fence


def test_idempotent_on_plain_markdown_links():
    src = "already [markdown](/a/b.md) link"
    out, _ = mig.rewrite_wikilinks(src)
    assert out == src
