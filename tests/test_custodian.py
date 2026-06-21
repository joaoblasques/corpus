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


def test_write_digest_appends_block(tmp_path):
    d = tmp_path / "_digest.md"
    c.write_digest("run-1", "gardener", [{"action": "drain", "result": "ingested 3"}],
                   path=d, _now="2026-06-19T13:00")
    c.write_digest("run-2", "gardener", [], path=d, _now="2026-06-20T13:00")
    text = d.read_text()
    assert "run-1" in text and "gardener" in text and "ingested 3" in text
    assert "2026-06-19T13:00" in text and "2026-06-20T13:00" in text
    assert text.count("## ") >= 2   # two appended blocks, newest last


def _loop_kwargs(**over):
    base = dict(constraints="OBEY §2/§7", budget=c.Budget(None), caps=c.Caps(),
                label="test", _now=lambda: "2026-06-19T13:00",
                _verify=lambda paths: c.Verdict(ok=True),
                _govern=lambda v, paths, **k: {"action": "committed", "pages": len(paths)},
                _queue=lambda *a, **k: None,
                _digest=lambda *a, **k: None,
                _finalize=lambda *a, **k: None)
    base.update(over)
    return base


def test_run_loop_stops_converged_when_worklist_dry():
    actions = iter([{"id": 1}])   # one action then StopIteration→None
    out = c.run_loop(next_action=lambda: next(actions, None),
                     execute=lambda a, ctx: c.Result(["corpus/x.md"], {"output_tokens": 5}),
                     **_loop_kwargs())
    assert out["stop_reason"] == "converged_dry" and out["iterations"] == 1


def test_run_loop_stops_on_budget():
    out = c.run_loop(next_action=lambda: {"id": 1},
                     execute=lambda a, ctx: c.Result(["corpus/x.md"], {"output_tokens": 60}),
                     **_loop_kwargs(budget=c.Budget(50)))
    assert out["stop_reason"] == "budget"


def test_run_loop_stops_on_no_progress_repeat_fingerprint():
    out = c.run_loop(next_action=lambda: {"id": 1},
                     execute=lambda a, ctx: c.Result(["corpus/same.md"], {"output_tokens": 1}),
                     **_loop_kwargs())
    assert out["stop_reason"] == "no_progress"   # 2nd iteration repeats the fingerprint


def test_run_loop_stops_on_max_iterations():
    n = iter(range(1000))
    out = c.run_loop(next_action=lambda: {"id": next(n)},
                     execute=lambda a, ctx: c.Result([f"corpus/{next(n)}.md"], {"output_tokens": 1}),
                     **_loop_kwargs(caps=c.Caps(max_iterations=3)))
    assert out["stop_reason"] == "max_iterations" and out["iterations"] == 3


def test_run_loop_routes_proposals_then_stops_on_repeat():
    queued = []
    out = c.run_loop(
        next_action=lambda: {"id": 1},
        execute=lambda a, ctx: c.Result([], {"output_tokens": 1}, proposals=[{"summary": "new rule"}]),
        **_loop_kwargs(_queue=lambda kind, detail: queued.append((kind, detail))))
    # empty changes no longer stop on iteration 1; the REPEAT (2nd identical empty) stops it.
    assert out["stop_reason"] == "no_progress"
    assert queued and queued[0][0] == "proposal"   # proposals still routed


def test_run_loop_single_empty_iteration_does_not_stop():
    seq = [c.Result([], {"output_tokens": 1}),            # iter1: empty (a failed action)
           c.Result(["corpus/x.md"], {"output_tokens": 1}),  # iter2: real change
           None]                                          # iter3: next_action → None
    actions = iter([{"i": 1}, {"i": 2}])
    it = iter(seq)
    out = c.run_loop(next_action=lambda: next(actions, None),
                     execute=lambda a, ctx: next(it), **_loop_kwargs())
    assert out["stop_reason"] == "converged_dry"   # the lone empty did not halt it


def test_smoke_runs_loop_to_convergence_without_commit(monkeypatch, capsys):
    monkeypatch.setattr(c.sr, "acquire_lock", lambda p: True)
    monkeypatch.setattr(c.sr, "release_lock", lambda p: None)
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    digest_calls, finalize_calls, committed = [], [], []
    monkeypatch.setattr(c, "write_digest", lambda *a, **k: digest_calls.append(1))
    monkeypatch.setattr(c, "finalize_commit", lambda *a, **k: finalize_calls.append(1) or {"status": "noop"})
    monkeypatch.setattr(c, "govern", lambda *a, **k: committed.append(1) or {"action": "committed"})
    rc = c.main(["--smoke"])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"stop_reason": "converged_dry"' in out
    assert committed == [] and digest_calls == [] and finalize_calls == []   # smoke commits/writes nothing


def test_write_digest_handles_non_serializable_entry(tmp_path):
    """An entry containing a Path (e.g. a worklist 'action') must not crash json.dumps."""
    from pathlib import Path as _P
    d = tmp_path / "_digest.md"
    c.write_digest("run-x", "gardener", [{"action": _P("/abs/corpus/x.md"), "ok": True}],
                   path=d, _now="2026-06-21T10:00")
    assert "/abs/corpus/x.md" in d.read_text()   # stringified, not crashed


def test_finalize_commit_pushes_after_commit(monkeypatch):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    calls = []
    def run(cmd, **k):
        calls.append(" ".join(cmd))
        out = " M corpus/_digest.md\n" if "status" in cmd else ""
        return types.SimpleNamespace(returncode=0, stdout=out, stderr="")
    res = c.finalize_commit(_run=run)
    assert res["pushed"] is True and res["status"] == "committed"
    assert any("commit" in s for s in calls) and any("push origin main" in s for s in calls)


def test_finalize_commit_pushes_even_when_catalog_unchanged(monkeypatch):
    # per-iteration content commits exist but catalog is unchanged → still push them
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    calls = []
    def run(cmd, **k):
        calls.append(" ".join(cmd))
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")   # clean status
    res = c.finalize_commit(_run=run)
    assert res["status"] == "nothing-to-commit"
    assert any("push" in s for s in calls)        # pushes prior commits anyway
    assert not any("commit -m" in s for s in calls)  # no new catalog commit


def test_finalize_commit_push_failure_is_recorded_not_raised(monkeypatch):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    def run(cmd, **k):
        rc = 1 if "push" in cmd else 0
        out = " M corpus/_digest.md\n" if "status" in cmd else ""
        return types.SimpleNamespace(returncode=rc, stdout=out, stderr="rejected")
    res = c.finalize_commit(_run=run)
    assert res["pushed"] is False   # recorded, no exception
