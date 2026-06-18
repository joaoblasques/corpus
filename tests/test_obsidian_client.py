import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import obsidian_client as oc  # noqa: E402


def _git_init(path):
    subprocess.run(["git", "-C", str(path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"], check=True)


def test_remove_vault_note_filesystem_deletes_untracked(tmp_path):
    vault = tmp_path / "vault"; vault.mkdir(); _git_init(vault)
    (vault / "Clippings").mkdir()
    note = vault / "Clippings" / "N.md"; note.write_text("x", encoding="utf-8")
    # never `git add`ed -> untracked; git rm cannot stage it
    removed = oc.remove_vault_note(vault, "Clippings/N.md")
    assert removed is True
    assert not note.exists()                       # filesystem fallback deleted it


def test_remove_vault_note_git_rm_tracked(tmp_path):
    vault = tmp_path / "vault"; vault.mkdir(); _git_init(vault)
    note = vault / "A.md"; note.write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(vault), "add", "A.md"], check=True)
    subprocess.run(["git", "-C", str(vault), "commit", "-qm", "x"], check=True)
    removed = oc.remove_vault_note(vault, "A.md")
    assert removed is True
    assert not note.exists()                       # removed from worktree
    out = subprocess.run(["git", "-C", str(vault), "status", "--porcelain"],
                         capture_output=True, text=True).stdout
    assert "D  A.md" in out                         # staged as a deletion (recoverable)


def test_remove_vault_note_missing_returns_false(tmp_path):
    vault = tmp_path / "vault"; vault.mkdir(); _git_init(vault)
    assert oc.remove_vault_note(vault, "nope.md") is False


def test_reap_reports_tracked_note_with_uncommitted_edits(tmp_path, monkeypatch, capsys):
    """A git-tracked vault note with an uncommitted local edit can't be `git rm`'d
    (git refuses without -f). The reaper must SURFACE it in `not_removed` rather than
    silently leaving it, and must never destroy the uncommitted edit."""
    import json
    vault = tmp_path / "vault"; vault.mkdir(); _git_init(vault)
    note = vault / "n.md"; note.write_text("orig\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(vault), "add", "n.md"], check=True)
    subprocess.run(["git", "-C", str(vault), "commit", "-qm", "x"], check=True)
    note.write_text("EDITED uncommitted\n", encoding="utf-8")  # local edit → git rm refuses
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-n.md").write_text(
        "---\ncorpus_ingested: true\nvault_origin: n.md\n---\nx", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])

    rc = oc.cmd_reap(oc._args(["reap", "--vault", str(vault)]))

    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["notes_removed"] == 0
    assert "n.md" in data["not_removed"]                  # surfaced, not silently dropped
    assert note.read_text() == "EDITED uncommitted\n"     # uncommitted edit preserved


def test_collect_copies_note_and_fetches_url(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Books").mkdir(parents=True)
    (vault / "00_Inbox/Clippings").mkdir(parents=True)
    (vault / "03_Resources/Books/New.md").write_text("---\ntitle: New\n---\nbody", encoding="utf-8")
    (vault / "00_Inbox/Clippings/articles to process.md").write_text("https://a.com/x\n", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(oc, "fetch_url", lambda url: {"title": "Art", "text": "fetched body", "channel": "web"})
    rc = oc.cmd_collect(oc._args(["collect", "--vault", str(vault)]))
    assert rc == 0
    files = {p.name for p in inbox.glob("*.md")}
    assert any(n.startswith("notes-") and "new" in n for n in files)
    assert any(n.startswith("web-art") for n in files)


def test_collect_skips_urls_in_processed_ledger(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "00_Inbox/Clippings").mkdir(parents=True)
    (vault / "00_Inbox/Clippings/articles to process.md").write_text(
        "https://a.com/x\nhttps://b.com/y\n", encoding="utf-8")
    # ledger already lists one url -> it must be skipped (no fetch)
    (vault / "00_Inbox/Clippings/articles_processed.md").write_text(
        "https://a.com/x\n", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    fetched = []

    def fake_fetch(url):
        fetched.append(url)
        return {"title": "T", "text": "body", "channel": "web"}

    monkeypatch.setattr(oc, "fetch_url", fake_fetch)
    oc.cmd_collect(oc._args(["collect", "--vault", str(vault)]))
    assert "https://a.com/x" not in fetched   # in ledger -> skipped
    assert "https://b.com/y" in fetched


def test_collect_dry_run_writes_nothing(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Books").mkdir(parents=True)
    (vault / "03_Resources/Books/New.md").write_text("body", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    oc.cmd_collect(oc._args(["collect", "--vault", str(vault), "--dry-run"]))
    assert list(inbox.glob("*.md")) == []


def test_reap_removes_only_ingested(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    note = vault / "03_Resources/Articles/A.md"; note.write_text("x", encoding="utf-8")
    listf = vault / "00_Inbox/Clippings"; listf.mkdir(parents=True)
    (listf / "articles to process.md").write_text("https://a.com/x\nhttps://b.com/y\n", encoding="utf-8")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    (raw / "web-x.md").write_text("---\ncorpus_ingested: true\nvia_vault_list: 00_Inbox/Clippings/articles to process.md\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])
    calls = []
    monkeypatch.setattr(oc, "remove_vault_note", lambda vault_root, rel: (calls.append(rel), True)[1])
    rc = oc.cmd_reap(oc._args(["reap", "--vault", str(vault)]))
    assert rc == 0
    assert calls == ["03_Resources/Articles/A.md"]                       # note staged for deletion
    remaining = (listf / "articles to process.md").read_text()
    assert "https://a.com/x" not in remaining and "https://b.com/y" in remaining  # processed URL struck
    assert "https://a.com/x" in (listf / "articles_processed.md").read_text()      # appended to ledger


def test_strike_url_removes_prefixed_lines_and_dedups_ledger(tmp_path):
    listf = tmp_path / "articles to process.md"
    listf.write_text("- https://a.com/x\nhttps://b.com/y.\n", encoding="utf-8")
    # strike each url; the list lines carry `- ` prefix / trailing `.`
    oc._strike_url(tmp_path, "articles to process.md", "https://a.com/x")
    oc._strike_url(tmp_path, "articles to process.md", "https://b.com/y")
    remaining = listf.read_text()
    assert "https://a.com/x" not in remaining
    assert "https://b.com/y" not in remaining
    ledger = (tmp_path / "articles_processed.md").read_text()
    assert ledger.count("https://a.com/x") == 1
    assert ledger.count("https://b.com/y") == 1
    # idempotent: calling again for an already-struck url does not double-append
    oc._strike_url(tmp_path, "articles to process.md", "https://a.com/x")
    ledger2 = (tmp_path / "articles_processed.md").read_text()
    assert ledger2.count("https://a.com/x") == 1


def test_reap_rejects_path_traversal(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    # plant a target outside the vault that the traversal would resolve to
    outside = tmp_path / "etc"; outside.mkdir()
    (outside / "x.md").write_text("secret", encoding="utf-8")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "evil.md").write_text(
        "---\ncorpus_ingested: true\nvault_origin: ../etc/x.md\n---\n", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])
    calls = []
    monkeypatch.setattr(oc, "remove_vault_note", lambda vault_root, rel: (calls.append(rel), True)[1])
    oc.cmd_reap(oc._args(["reap", "--vault", str(vault)]))
    assert calls == []   # traversal outside vault must never reach git_rm


def test_collect_dry_run_does_not_fetch(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "00_Inbox/Clippings").mkdir(parents=True)
    (vault / "00_Inbox/Clippings/articles to process.md").write_text(
        "https://a.com/x\n", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])

    fetched = []
    monkeypatch.setattr(oc, "fetch_url", lambda url: fetched.append(url) or {"text": "x", "title": "t"})
    rc = oc.cmd_collect(oc._args(["collect", "--vault", str(vault), "--dry-run"]))
    assert rc == 0
    assert fetched == []   # no network under --dry-run


def test_reap_dry_run_changes_nothing(tmp_path, monkeypatch):
    vault = tmp_path / "vault"; (vault / "03_Resources/Articles").mkdir(parents=True)
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])
    calls = []
    monkeypatch.setattr(oc, "remove_vault_note", lambda vault_root, rel: (calls.append(rel), True)[1])
    oc.cmd_reap(oc._args(["reap", "--vault", str(vault), "--dry-run"]))
    assert calls == []


def test_collect_fetches_inline_note_links(tmp_path, monkeypatch):
    import obsidian_client as oc
    inbox = tmp_path / "inbox"; inbox.mkdir()
    vault = tmp_path / "vault"; (vault / "Clippings").mkdir(parents=True)
    (vault / "Clippings" / "N.md").write_text(
        '---\ntitle: "N"\nsource: "https://src.com/p"\n---\n'
        'read https://good.com/a and https://src.com/p again\n')
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(oc, "fetch_url", lambda url: {"title": "A", "text": "fetched body"})
    rc = oc.cmd_collect(oc._args(["collect", "--vault", str(vault)]))
    assert rc == 0
    webs = list(inbox.glob("web-*.md"))
    assert len(webs) == 1                       # good.com fetched; src.com skipped as source URL
    text = webs[0].read_text()
    assert "via_vault_note: Clippings/N.md" in text
    assert "source_url: https://good.com/a" in text
