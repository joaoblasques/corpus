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


def test_reapable_returns_all_collected_repo_fullnames(tmp_path):
    d = tmp_path / "github"; d.mkdir()
    (d / "ingested.md").write_text(
        "---\nchannel: github\nrepo: owner/done\ncorpus_ingested: true\n---\nbody", encoding="utf-8")
    (d / "pending.md").write_text(
        "---\nchannel: github\nrepo: owner/todo\n---\nbody", encoding="utf-8")
    # keys on COLLECTION, not ingestion: both captured digests are reapable regardless of ingest state
    assert set(cg.reapable(dirs=[d])) == {"owner/done", "owner/todo"}


def test_reapable_dedups_across_dirs(tmp_path):
    a = tmp_path / "_inbox"; a.mkdir()
    b = tmp_path / "github"; b.mkdir()
    fm = "---\nchannel: github\nrepo: owner/dup\ncorpus_ingested: true\n---\nbody"
    (a / "one.md").write_text(fm, encoding="utf-8")
    (b / "two.md").write_text(fm, encoding="utf-8")
    assert cg.reapable(dirs=[a, b]) == ["owner/dup"]   # same repo once, not twice


def test_reapable_empty_when_no_github_digests(tmp_path):
    d = tmp_path / "github"; d.mkdir()
    # a non-github file with no `repo:` field is never reapable (nothing collected here)
    (d / "note.md").write_text("---\nchannel: web\ntitle: something\n---\nbody", encoding="utf-8")
    assert cg.reapable(dirs=[d]) == []


def test_discover_topics_flat_sorted_deduped():
    tm = {"a": ["llm", "rag"], "b": ["rag", "mlops"]}
    assert cg.discover_topics(tm) == ["llm", "mlops", "rag"]   # deduped + sorted


def test_discover_topics_defaults_to_domain_map():
    out = cg.discover_topics()
    assert "llm" in out and out == sorted(set(out))   # uses DOMAIN_TOPICS, sorted/deduped


def test_rank_candidates_sorts_by_stars_desc():
    cands = {"o/a": 100, "o/b": 900, "o/c": 500}
    out = cg.rank_candidates(cands, starred=set(), already=lambda fn: False)
    assert out == [("o/b", 900), ("o/c", 500), ("o/a", 100)]


def test_rank_candidates_drops_starred_and_already_collected():
    cands = {"o/a": 100, "o/b": 900, "o/c": 500}
    out = cg.rank_candidates(cands, starred={"o/b"}, already=lambda fn: fn == "o/a")
    assert out == [("o/c", 500)]   # o/b starred, o/a already in corpus
