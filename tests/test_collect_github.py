import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_github as cg  # noqa: E402

REPO = {"full_name": "anthropics/claude-code", "html_url": "https://github.com/anthropics/claude-code",
        "description": "Agentic coding: tasks & PRs", "language": "TypeScript", "stars": 1234,
        "topics": ["agents", "cli"], "latest_release": "v2.0.1",
        "readme": "# Claude Code\nDoes things.", "docs": [{"path": "docs/x.md", "text": "Doc body"}]}


def test_slugify():
    assert cg.slugify("anthropics/claude-code") == "github-anthropics-claude-code"
    assert cg.slugify("d4vinci/Scrapling") == "github-d4vinci-scrapling"


def test_build_document_has_frontmatter_and_sections():
    doc = cg.build_document(REPO, collected_at="2026-06-22")
    assert "channel: github" in doc and "repo: anthropics/claude-code" in doc
    assert "stars: 1234" in doc and "latest_release: v2.0.1" in doc
    assert "topics: [agents, cli]" in doc
    assert "## README" in doc and "Does things." in doc
    assert "## Docs" in doc and "### docs/x.md" in doc and "Doc body" in doc


def test_build_document_tolerates_missing_pieces():
    doc = cg.build_document({"full_name": "a/b"}, collected_at="2026-06-22")
    assert "repo: a/b" in doc and "## README" in doc and "stars: 0" in doc


def test_write_collected_writes_then_dedups(tmp_path):
    d = tmp_path / "_inbox"
    led = tmp_path / "github_digested.txt"  # isolated ledger — don't touch the real one
    r1 = cg.write_collected(REPO, collected_at="2026-06-22", inbox=d, dedup_dirs=[d], ledger_path=led)
    assert r1["status"] == "written" and Path(r1["path"]).name == "github-anthropics-claude-code.md"
    r2 = cg.write_collected(REPO, collected_at="2026-06-22", inbox=d, dedup_dirs=[d], ledger_path=led)
    assert r2["status"] == "duplicate"   # dedup by repo: full-name


def test_already_collected_matches_frontmatter_repo_line(tmp_path):
    d = tmp_path / "_inbox"; d.mkdir()
    led = tmp_path / "noop_ledger.txt"  # isolate from the real on-disk ledger
    (d / "x.md").write_text("---\nchannel: github\nrepo: owner/name\n---\nbody", encoding="utf-8")
    assert cg.already_collected("owner/name", dirs=[d], ledger_path=led) is True
    assert cg.already_collected("owner/other", dirs=[d], ledger_path=led) is False


def test_reapable_returns_only_ingested_repo_fullnames(tmp_path):
    d = tmp_path / "github"; d.mkdir()
    (d / "ingested.md").write_text(
        "---\nchannel: github\nrepo: owner/done\ncorpus_ingested: true\n---\nbody", encoding="utf-8")
    (d / "pending.md").write_text(
        "---\nchannel: github\nrepo: owner/todo\n---\nbody", encoding="utf-8")
    assert cg.reapable(dirs=[d]) == ["owner/done"]   # only the corpus_ingested digest


def test_reapable_dedups_across_dirs(tmp_path):
    a = tmp_path / "_inbox"; a.mkdir()
    b = tmp_path / "github"; b.mkdir()
    fm = "---\nchannel: github\nrepo: owner/dup\ncorpus_ingested: true\n---\nbody"
    (a / "one.md").write_text(fm, encoding="utf-8")
    (b / "two.md").write_text(fm, encoding="utf-8")
    assert cg.reapable(dirs=[a, b]) == ["owner/dup"]   # same repo once, not twice


def test_reapable_empty_when_nothing_ingested(tmp_path):
    d = tmp_path / "github"; d.mkdir()
    (d / "p.md").write_text("---\nchannel: github\nrepo: owner/todo\n---\nbody", encoding="utf-8")
    assert cg.reapable(dirs=[d]) == []
