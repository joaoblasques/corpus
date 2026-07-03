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


def test_reformat_log_newest_first_iso_groups():
    src = ("# Corpus Log\n\n"
           "## [2026-05-07] schema | bootstrap\n- did x\n\n"
           "## [2026-07-02] ingest | Foo\n- did y\n")
    out = mig.reformat_log(src)
    # newest date first, ISO group headings, no bracket/op-in-heading
    assert out.index("## 2026-07-02") < out.index("## 2026-05-07")
    assert "## [2026-" not in out
    assert "bootstrap" in out and "Foo" in out           # no entry lost


def test_stamp_index_adds_okf_version_once():
    once = mig.stamp_index("# Corpus Index\n\n## Domains\n")
    assert once.startswith('---\nokf_version: "0.1"\n---\n')
    assert mig.stamp_index(once) == once                 # idempotent


def test_ensure_type_adds_or_inserts():
    assert mig.ensure_type("# Domains\n", "domain-registry").startswith(
        "---\ntype: domain-registry\n---\n")
    got = mig.ensure_type("---\nfoo: 1\n---\nbody", "domain-registry")
    assert "type: domain-registry" in got and "foo: 1" in got


def test_migrate_bundle_end_to_end(tmp_path):
    b = tmp_path / "corpus"; (b / "ai-engineering").mkdir(parents=True)
    (b / "_index.md").write_text("# Corpus Index\n\n### ai-engineering\n- [[ai-engineering/x|X]]\n")
    (b / "_log.md").write_text("# Corpus Log\n\n## [2026-05-07] schema | boot\n- a\n")
    (b / "_domains.md").write_text("# Domains\n")
    (b / "ai-engineering" / "x.md").write_text("---\ntype: entity\n---\nsee [[ai-engineering/y|Y]]\n")
    r = mig.migrate_bundle(b, dry_run=False)
    assert (b / "index.md").exists() and not (b / "_index.md").exists()
    assert (b / "log.md").exists() and not (b / "_log.md").exists()
    assert (b / "index.md").read_text().startswith('---\nokf_version: "0.1"\n---')
    assert "[Y](/ai-engineering/y.md)" in (b / "ai-engineering" / "x.md").read_text()
    assert "type: domain-registry" in (b / "_domains.md").read_text()
    assert r["links"] >= 2
