import sys
from pathlib import Path
import types

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import custodian as c  # noqa: E402


def test_budget_accumulates_output_tokens():
    b = c.Budget(100)
    b.add({"output_tokens": 30})
    b.add({"output_tokens": 25})
    assert b.spent() == 55
    assert b.remaining() == 45
    assert b.exhausted() is False


def test_budget_exhausted_at_cap():
    b = c.Budget(50)
    b.add({"output_tokens": 50})
    assert b.exhausted() is True


def test_budget_none_cap_is_infinite():
    import math
    b = c.Budget(None)
    b.add({"output_tokens": 10_000})
    assert b.remaining() == math.inf and b.exhausted() is False


def test_budget_add_tolerates_missing_usage_key():
    b = c.Budget(10)
    b.add({})            # no output_tokens
    assert b.spent() == 0


def test_caps_defaults():
    caps = c.Caps()
    assert (caps.max_iterations, caps.max_pages_touched, caps.wall_clock_s) == (25, 40, 3600)


def test_fingerprint_stable_and_order_insensitive():
    a = c.fingerprint(["corpus/x.md", "corpus/y.md"], [])
    b = c.fingerprint(["corpus/y.md", "corpus/x.md"], [])
    assert a == b and isinstance(a, str)


def test_fingerprint_differs_on_different_effect():
    assert c.fingerprint(["corpus/x.md"], []) != c.fingerprint(["corpus/y.md"], [])
    assert c.fingerprint(["corpus/x.md"], []) != c.fingerprint(["corpus/x.md"], ["err"])


def test_fingerprint_empty_changes_is_stable():
    assert c.fingerprint([], []) == c.fingerprint([], [])


def _fake_lint(broken_cites=(), broken_links=()):
    return lambda: {"broken_citations": list(broken_cites),
                    "broken_wikilinks": list(broken_links),
                    "orphans": [], "stubs": []}


def test_verify_gate_ok_when_changed_pages_clean():
    v = c.verify_gate(["corpus/data-engineering/x.md"], _lint=_fake_lint())
    assert v.ok is True and v.broken_citations == 0


def test_verify_gate_fails_when_changed_page_sources_broken_citation():
    lint = _fake_lint(broken_cites=[("corpus/data-engineering/x.md", "../../raw/web/missing.md")])
    v = c.verify_gate(["corpus/data-engineering/x.md"], _lint=lint)
    assert v.ok is False and v.broken_citations == 1


def test_verify_gate_ignores_breakage_in_unchanged_pages():
    lint = _fake_lint(broken_cites=[("corpus/other/y.md", "../../raw/web/missing.md")])
    v = c.verify_gate(["corpus/data-engineering/x.md"], _lint=lint)
    assert v.ok is True   # the broken page is not in changed_paths


def test_enqueue_review_appends_entry(tmp_path):
    q = tmp_path / "_review_queue.md"
    c.enqueue_review("proposal", {"summary": "add dbt routing rule"}, path=q)
    c.enqueue_review("verify-failed", {"page": "corpus/x.md"}, path=q)
    text = q.read_text()
    assert "proposal" in text and "add dbt routing rule" in text and "verify-failed" in text


def test_govern_commits_when_ok_and_reversible(monkeypatch):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    calls = []
    def run(cmd, **k):
        calls.append(" ".join(cmd))
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    out = c.govern(c.Verdict(ok=True), ["corpus/x.md"], reversible=True, _run=run)
    assert out["action"] == "committed"
    assert any("commit" in s for s in calls) and any("add" in s for s in calls)


def test_govern_reverts_and_queues_on_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    calls = []
    def run(cmd, **k):
        calls.append(cmd)
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    queued = []
    out = c.govern(c.Verdict(ok=False, broken_citations=1, notes=["broken citation: corpus/x.md"]),
                   ["corpus/x.md"], reversible=True, _run=run,
                   _queue=lambda kind, detail: queued.append((kind, detail)))
    assert out["action"] == "reverted+queued"
    assert ["git", "checkout", "--", "corpus/x.md"] in calls   # reverted exactly the changed path
    assert not any("commit" in " ".join(cmd) for cmd in calls)  # never committed
    assert queued and queued[0][0] == "verify-failed"


def test_govern_skips_off_main(monkeypatch):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: False)
    out = c.govern(c.Verdict(ok=True), ["corpus/x.md"], reversible=True,
                   _run=lambda *a, **k: types.SimpleNamespace(returncode=0, stdout="", stderr=""))
    assert out["action"] == "skipped-not-main"
