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


import json, types


def test_expand_prompt_includes_page_and_sources(tmp_path):
    root = tmp_path; (root / "raw").mkdir()
    (root / "raw" / "s.md").write_text("SOURCE BODY about X", encoding="utf-8")
    d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "openai.md", ["raw/s.md"], body="stub tldr")
    p = g.expand_prompt(d / "openai.md", root=root)
    assert "openai.md" in p or "stub tldr" in p
    assert "SOURCE BODY about X" in p          # the cited source text is embedded
    assert "stub" in p.lower() and "draft" in p.lower()   # the stub→draft instruction


def test_execute_success_returns_changed_path(tmp_path):
    root = tmp_path; (root / "raw").mkdir()
    (root / "raw" / "s.md").write_text("body", encoding="utf-8")
    d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "openai.md", ["raw/s.md"])
    def fake_run(cmd, **k):
        return types.SimpleNamespace(returncode=0,
            stdout=json.dumps({"result": "done", "usage": {"output_tokens": 120}}), stderr="")
    execute = g.make_execute(root=root, _run=fake_run)
    res = execute(d / "openai.md", "OBEY")
    assert res.changed_paths == [str(d / "openai.md")] and res.usage["output_tokens"] == 120


def test_execute_failure_returns_empty_changed_paths(tmp_path):
    root = tmp_path; (root / "raw").mkdir()
    (root / "raw" / "s.md").write_text("body", encoding="utf-8")
    d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "openai.md", ["raw/s.md"])
    def fake_run(cmd, **k):
        return types.SimpleNamespace(returncode=1, stdout="", stderr="boom")
    execute = g.make_execute(root=root, _run=fake_run)
    res = execute(d / "openai.md", "OBEY")
    assert res.changed_paths == [] and res.errors


def test_execute_never_raises_on_missing_stub(tmp_path):
    root = tmp_path
    execute = g.make_execute(root=root, _run=lambda *a, **k: None)  # _run won't be reached
    res = execute(root / "corpus" / "ai" / "gone.md", "OBEY")  # file does not exist
    assert res.changed_paths == [] and res.errors  # returns an error Result, does NOT raise


def test_verify_ok_when_lint_and_critic_clean(tmp_path):
    root = tmp_path; d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "openai.md", ["raw/s.md"])
    v = g.make_verify(root=root, _lint=lambda: {"broken_citations": [], "broken_wikilinks": []},
                      _critic=lambda page, src: (True, []))
    assert v([str(d / "openai.md")]).ok is True


def test_verify_fails_when_critic_flags_unsupported_claim(tmp_path):
    root = tmp_path; d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "openai.md", ["raw/s.md"])
    v = g.make_verify(root=root, _lint=lambda: {"broken_citations": [], "broken_wikilinks": []},
                      _critic=lambda page, src: (False, ["claim 'X' not in any cited source"]))
    verdict = v([str(d / "openai.md")])
    assert verdict.ok is False and any("not in any cited source" in n for n in verdict.notes)


def test_verify_fails_when_lint_broken(tmp_path):
    root = tmp_path; d = root / "corpus" / "ai"; d.mkdir(parents=True)
    _stub(d, "openai.md", ["raw/s.md"])
    v = g.make_verify(root=root,
                      _lint=lambda: {"broken_citations": [("corpus/ai/openai.md", "x")], "broken_wikilinks": []},
                      _critic=lambda page, src: (True, []))
    assert v([str(d / "openai.md")]).ok is False   # lint failure alone fails the verdict


def test_dry_run_lists_worklist_no_calls(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(g.sr, "_on_main", lambda *a, **k: True)
    monkeypatch.setattr(g.sr, "acquire_lock", lambda p: True)
    monkeypatch.setattr(g.sr, "release_lock", lambda p: None)
    called = {"loop": False}
    monkeypatch.setattr(g.cust, "run_loop", lambda **k: called.__setitem__("loop", True) or {})
    monkeypatch.setattr(g, "CORPUS", tmp_path / "corpus")
    monkeypatch.setattr(g, "ROOT", tmp_path)
    (tmp_path / "raw").mkdir(); (tmp_path / "raw" / "s.md").write_text("c", encoding="utf-8")
    d = tmp_path / "corpus" / "ai"; d.mkdir(parents=True); _stub(d, "openai.md", ["raw/s.md"])
    rc = g.main(["run", "--dry-run"])
    out = capsys.readouterr().out
    assert rc == 0 and "openai.md" in out and called["loop"] is False   # dry-run does NOT loop


def test_run_invokes_run_loop(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(g.sr, "_on_main", lambda *a, **k: True)
    monkeypatch.setattr(g.sr, "acquire_lock", lambda p: True)
    monkeypatch.setattr(g.sr, "release_lock", lambda p: None)
    monkeypatch.setattr(g, "CORPUS", tmp_path / "corpus")
    monkeypatch.setattr(g, "ROOT", tmp_path)
    (tmp_path / "raw").mkdir(); (tmp_path / "raw" / "s.md").write_text("c", encoding="utf-8")
    d = tmp_path / "corpus" / "ai"; d.mkdir(parents=True); _stub(d, "openai.md", ["raw/s.md"])
    monkeypatch.setattr(g.cust, "run_loop",
                        lambda **k: {"label": "gardener", "stop_reason": "converged_dry", "committed": 1})
    rc = g.main(["run", "--max", "3"])
    out = capsys.readouterr().out
    assert rc == 0 and '"stop_reason": "converged_dry"' in out
