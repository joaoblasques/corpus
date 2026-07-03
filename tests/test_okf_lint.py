import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
ok = importlib.import_module("okf_lint")


def test_parse_frontmatter_variants():
    assert ok.parse_frontmatter("---\ntype: entity\n---\nbody") == {"type": "entity"}
    assert ok.parse_frontmatter("no frontmatter here") is None
    assert ok.parse_frontmatter("---\n---\nbody") == {}


def test_concept_needs_nonempty_type():
    assert ok.check_concept(Path("a.md"), "---\ntype: entity\n---\nx") == []
    assert ok.check_concept(Path("a.md"), "no fm") != []            # missing frontmatter
    assert ok.check_concept(Path("a.md"), "---\ntitle: x\n---\ny") != []  # no type
    assert ok.check_concept(Path("a.md"), "---\ntype: ''\n---\ny") != []  # empty type


def test_root_index_allows_only_okf_version():
    assert ok.check_index(Path("index.md"), '---\nokf_version: "0.1"\n---\n# D\n', True) == []
    assert ok.check_index(Path("index.md"), "# D\n* [a](/a.md)\n", True) == []   # no fm is fine
    assert ok.check_index(Path("d/index.md"), "---\nokf_version: \"0.1\"\n---\n", False) != []  # non-root fm forbidden


def test_log_date_headings_iso():
    assert ok.check_log(Path("log.md"), "# Log\n## 2026-07-03\n* x\n") == []
    assert ok.check_log(Path("log.md"), "# Log\n## [2026-07-03 10:00] ingest\n") != []  # bracketed = bad


def test_lint_bundle_tolerates_broken_links_and_unknown_keys(tmp_path):
    (tmp_path / "a.md").write_text("---\ntype: entity\nweird_key: 1\n---\n[x](/missing.md)\n")
    (tmp_path / "index.md").write_text('---\nokf_version: "0.1"\n---\n# S\n* [a](/a.md) - d\n')
    r = ok.lint_bundle(tmp_path)
    assert r["violations"] == []          # unknown keys + broken links are OKF-legal
    assert r["concepts"] == 1
