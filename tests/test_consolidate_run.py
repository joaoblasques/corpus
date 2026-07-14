import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import consolidate_run as cr  # noqa: E402

def _proc(stdout="", returncode=0, stderr=""):
    class P:  # minimal CompletedProcess stand-in
        pass
    p = P(); p.stdout = stdout; p.returncode = returncode; p.stderr = stderr
    return p

def test_triage_cluster_parses_verdict():
    def fake_run(cmd, **kw):
        assert "--model" in cmd and cr.CONSOLIDATE_TRIAGE_MODEL in cmd
        inner = json.dumps({"mode": "new-synthesis", "title": "RAG Patterns",
                            "slug": "rag-patterns", "reason": "coherent"})
        return _proc(stdout=json.dumps({"result": inner}))
    v = cr.triage_cluster({"topic": "rag", "domain": "ai-engineering",
                           "members": ["ai-engineering/sources/s1.md"]}, _run=fake_run)
    assert v["mode"] == "new-synthesis" and v["slug"] == "rag-patterns"

def test_triage_cluster_fails_closed_on_garbage():
    def fake_run(cmd, **kw):
        return _proc(stdout="not json at all")
    v = cr.triage_cluster({"topic": "x", "domain": "ai-engineering", "members": []}, _run=fake_run)
    assert v["mode"] == "reject"

def test_queue_reject_appends_line(tmp_path):
    review = tmp_path / "_consolidation_review.md"
    cr.queue_reject({"topic": "grab bag", "domain": "ai-engineering", "size": 6},
                    {"mode": "reject", "reason": "incoherent"}, review)
    txt = review.read_text()
    assert "grab bag" in txt and "reject" in txt and "incoherent" in txt


def _write_member(corpus: Path, rel: str):
    p = corpus / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\ntype: source\ndomain: ai-engineering\nstatus: stub\n---\n# M\nbody\n",
                 encoding="utf-8")
    return p

def test_synthesize_returns_path_when_writer_creates_file(tmp_path):
    corpus = tmp_path / "corpus"
    cluster = {"topic": "rag", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_run(cmd, **kw):
        # simulate the writer creating the synthesis page
        out = corpus / "ai-engineering" / "rag-patterns.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("---\ntype: synthesis\n---\n# RAG\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "done"}); p.returncode = 0
        return p

    path = cr.synthesize(cluster, triage, corpus, _run=fake_run)
    assert path is not None and path.name == "rag-patterns.md" and path.exists()

def test_stamp_and_unstamp_members(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/s1.md"]}
    n = cr.stamp_members(cluster, "ai-engineering/rag-patterns.md", corpus)
    assert n == 1
    txt = (corpus / "ai-engineering/sources/s1.md").read_text()
    assert "consolidated_into: ai-engineering/rag-patterns.md" in txt
    # idempotent: stamping again does not duplicate
    assert cr.stamp_members(cluster, "ai-engineering/rag-patterns.md", corpus) == 1
    assert txt.count("consolidated_into:") == 1 or \
        (corpus / "ai-engineering/sources/s1.md").read_text().count("consolidated_into:") == 1
    # unstamp removes it
    assert cr.unstamp_members(cluster, corpus) == 1
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/s1.md").read_text()

def test_process_cluster_commits_on_critic_pass(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering", "size": 5,
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_writer(cmd, **kw):
        (corpus / "ai-engineering" / "rag-patterns.md").write_text(
            "---\ntype: synthesis\n---\n# RAG\ncited[^1]\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.process_cluster(cluster, triage, corpus, tmp_path / "rev.md",
                             _run=fake_writer, _critic=lambda page, src: (True, []))
    assert res["status"] == "synthesized"
    assert (corpus / "ai-engineering" / "rag-patterns.md").exists()
    assert "consolidated_into:" in (corpus / "ai-engineering/sources/s1.md").read_text()

def test_process_cluster_reverts_on_critic_fail(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering", "size": 5,
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_writer(cmd, **kw):
        (corpus / "ai-engineering" / "rag-patterns.md").write_text(
            "---\ntype: synthesis\n---\n# RAG\nfabricated claim\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    review = tmp_path / "rev.md"
    res = cr.process_cluster(cluster, triage, corpus, review,
                             _run=fake_writer, _critic=lambda page, src: (False, ["fabricated"]))
    assert res["status"] == "reverted"
    assert not (corpus / "ai-engineering" / "rag-patterns.md").exists()   # page removed
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/s1.md").read_text()
    assert "reject" in review.read_text() or "rag" in review.read_text()

def test_process_cluster_reverts_when_critic_raises(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering", "size": 5,
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_writer(cmd, **kw):
        (corpus / "ai-engineering" / "rag-patterns.md").write_text(
            "---\ntype: synthesis\n---\n# RAG\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    def raising_critic(page, src):
        raise RuntimeError("critic exploded")

    res = cr.process_cluster(cluster, triage, corpus, tmp_path / "rev.md",
                             _run=fake_writer, _critic=raising_critic)
    assert res["status"] == "reverted"                                   # fail closed
    assert not (corpus / "ai-engineering" / "rag-patterns.md").exists()  # page removed
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/s1.md").read_text()


def test_process_cluster_queues_deepen_and_reject(tmp_path):
    corpus = tmp_path / "corpus"
    review = tmp_path / "rev.md"
    for mode in ("deepen-existing", "reject"):
        res = cr.process_cluster(
            {"topic": "t", "domain": "ai-engineering", "size": 6, "members": []},
            {"mode": mode, "title": "", "slug": "", "reason": "r"}, corpus, review, _run=None)
        assert res["status"] == "queued" and res["mode"] == mode
    assert review.read_text().count("\n") >= 2


def test_run_consolidation_dry_run_lists_without_writing(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering" / "sources"; d.mkdir(parents=True)
    for i in range(5):
        (d / f"s{i}.md").write_text(
            "---\ntype: source\ndomain: ai-engineering\ntags:\n  - source\n  - RAG\n---\n# t\nx\n",
            encoding="utf-8")
    res = cr.run_consolidation(corpus, "ai-engineering", 3, dry_run=True)
    assert res["status"] == "ok" and res["clusters_seen"] >= 1
    assert res["synthesized"] == 0                          # dry-run writes nothing
    # no synthesis page created
    assert not list((corpus / "ai-engineering").glob("rag*.md"))

def test_main_skips_when_not_on_main(monkeypatch, capsys):
    monkeypatch.setattr(cr.sr, "_on_main", lambda *a, **k: False)
    rc = cr.main(["run"])
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["reason"] == "not_on_main"


def _page(corpus, rel, text):
    p = corpus / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p

_ORIG = "---\ntype: entity\ndomain: ai-engineering\n---\n# OpenAI\n\nExisting claim.[^a]\n\n[^a]: [s](../x.md)\n"

def test_deepen_page_commits_on_pass(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering/openai.md", _ORIG)
    _write_member(corpus, "ai-engineering/sources/o1.md")           # helper from earlier tasks
    cluster = {"topic": "openai", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/o1.md"]}

    def fake_writer(cmd, **kw):
        # simulate the writer ADDING a cited claim while keeping [^a]
        pg = corpus / "ai-engineering/openai.md"
        pg.write_text(_ORIG.rstrip() + "\n\nNew claim.[^b]\n\n[^b]: [s](../y.md)\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.deepen_page(cluster, "ai-engineering/openai.md", corpus, tmp_path / "rev.md",
                         _run=fake_writer, _critic=lambda pg, src: (True, []))
    assert res["status"] == "deepened"
    txt = (corpus / "ai-engineering/openai.md").read_text()
    assert "[^a]" in txt and "[^b]" in txt                          # kept old, added new
    assert "consolidated_into:" in (corpus / "ai-engineering/sources/o1.md").read_text()

def test_deepen_page_reverts_and_restores_on_dropped_citation(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering/openai.md", _ORIG)
    _write_member(corpus, "ai-engineering/sources/o1.md")
    cluster = {"topic": "openai", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/o1.md"]}

    def dropping_writer(cmd, **kw):
        # BAD: rewrites the page and DROPS the existing [^a] footnote
        (corpus / "ai-engineering/openai.md").write_text(
            "---\ntype: entity\n---\n# OpenAI\n\nOnly new stuff.[^b]\n\n[^b]: [s](../y.md)\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.deepen_page(cluster, "ai-engineering/openai.md", corpus, tmp_path / "rev.md",
                         _run=dropping_writer, _critic=lambda pg, src: (True, []))
    assert res["status"] == "reverted"
    assert (corpus / "ai-engineering/openai.md").read_text() == _ORIG   # restored byte-for-byte
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/o1.md").read_text()

def test_deepen_page_reverts_on_critic_fail(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering/openai.md", _ORIG)
    _write_member(corpus, "ai-engineering/sources/o1.md")
    cluster = {"topic": "openai", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/o1.md"]}

    def ok_writer(cmd, **kw):
        (corpus / "ai-engineering/openai.md").write_text(
            _ORIG.rstrip() + "\n\nFabricated.[^b]\n\n[^b]: [s](../y.md)\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.deepen_page(cluster, "ai-engineering/openai.md", corpus, tmp_path / "rev.md",
                         _run=ok_writer, _critic=lambda pg, src: (False, ["fabricated"]))
    assert res["status"] == "reverted"
    assert (corpus / "ai-engineering/openai.md").read_text() == _ORIG   # restored
