import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gardener as g  # noqa: E402


def _stub(dirp, name, sources_rel, created="2026-01-01", body="x"):
    sb = "\n".join(f"  - path: {s}" for s in sources_rel)
    (dirp / name).write_text(
        f"---\ntype: concept\nstatus: stub\ncreated: {created}\nsources:\n{sb}\n---\n{body}\n",
        encoding="utf-8")


def test_find_stubs_only_stub_status(tmp_path):
    d = tmp_path / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "a.md", ["raw/x.md"])
    (d / "b.md").write_text("---\nstatus: draft\n---\nx", encoding="utf-8")
    (tmp_path / "corpus" / "_index.md").write_text("---\nstatus: stub\n---\nx", encoding="utf-8")
    out = [p.name for p in g.find_stubs(corpus_dir=tmp_path / "corpus")]
    assert out == ["a.md"]   # only status:stub, catalog _files skipped


def test_is_expandable_requires_existing_nonempty_source(tmp_path):
    root = tmp_path; (root / "raw").mkdir()
    (root / "raw" / "real.md").write_text("content", encoding="utf-8")
    (root / "raw" / "empty.md").write_text("", encoding="utf-8")
    d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "good.md", ["raw/real.md"]); _stub(d, "bad.md", ["raw/missing.md"])
    _stub(d, "emptysrc.md", ["raw/empty.md"])
    assert g.is_expandable(d / "good.md", root=root) is True
    assert g.is_expandable(d / "bad.md", root=root) is False
    assert g.is_expandable(d / "emptysrc.md", root=root) is False


def test_rank_by_inbound_then_created(tmp_path):
    c = tmp_path / "corpus"; d = c / "ai"; d.mkdir(parents=True)
    _stub(d, "pop.md", ["raw/x.md"], created="2026-02-01")
    _stub(d, "old.md", ["raw/x.md"], created="2026-01-01")
    # a draft page links to ai/pop twice → pop has higher inbound
    (d / "linker.md").write_text("see [[ai/pop|Pop]] and [[ai/pop]] vs [[ai/old]]", encoding="utf-8")
    ranked = [p.name for p in g.rank_stubs([d / "old.md", d / "pop.md"], corpus_dir=c)]
    assert ranked == ["pop.md", "old.md"]   # pop: 2 inbound > old: 1


def test_worklist_skips_unexpandable_and_queues_them(tmp_path):
    root = tmp_path; (root / "raw").mkdir()
    (root / "raw" / "real.md").write_text("content", encoding="utf-8")
    c = root / "corpus"; d = c / "ai"; d.mkdir(parents=True)
    _stub(d, "good.md", ["raw/real.md"]); _stub(d, "bad.md", ["raw/missing.md"])
    queued = []
    nxt = g.make_worklist(corpus_dir=c, root=root, _queue=lambda k, det: queued.append((k, det)))
    first = nxt(); second = nxt()
    assert first is not None and first.name == "good.md"
    assert second is None                       # bad.md filtered out → worklist exhausted
    assert queued and queued[0][0] == "stub-no-source"   # unexpandable queued once
