import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import obsidian_client as oc  # noqa: E402


def test_collect_copies_note_and_fetches_url(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    (vault / "00_Inbox/Clippings").mkdir(parents=True)
    (vault / "03_Resources/Articles/New.md").write_text("---\ntitle: New\n---\nbody", encoding="utf-8")
    (vault / "00_Inbox/Clippings/articles to process.md").write_text("https://a.com/x\n", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(oc, "fetch_url", lambda url: {"title": "Art", "text": "fetched body", "channel": "web"})
    rc = oc.cmd_collect(oc._args(["collect", "--vault", str(vault)]))
    assert rc == 0
    files = {p.name for p in inbox.glob("*.md")}
    assert any(n.startswith("notes-new") for n in files)
    assert any(n.startswith("web-art") for n in files)


def test_collect_dry_run_writes_nothing(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    (vault / "03_Resources/Articles/New.md").write_text("body", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    oc.cmd_collect(oc._args(["collect", "--vault", str(vault), "--dry-run"]))
    assert list(inbox.glob("*.md")) == []
