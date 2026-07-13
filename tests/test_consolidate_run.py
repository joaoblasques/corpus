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
