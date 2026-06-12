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
    (vault / "03_Resources/Articles").mkdir(parents=True)
    (vault / "03_Resources/Articles/New.md").write_text("body", encoding="utf-8")
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
    monkeypatch.setattr(oc, "git_rm", lambda vault_root, rel: calls.append(rel))
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
    monkeypatch.setattr(oc, "git_rm", lambda vault_root, rel: calls.append(rel))
    oc.cmd_reap(oc._args(["reap", "--vault", str(vault)]))
    assert calls == []   # traversal outside vault must never reach git_rm


def test_reap_dry_run_changes_nothing(tmp_path, monkeypatch):
    vault = tmp_path / "vault"; (vault / "03_Resources/Articles").mkdir(parents=True)
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])
    calls = []
    monkeypatch.setattr(oc, "git_rm", lambda vault_root, rel: calls.append(rel))
    oc.cmd_reap(oc._args(["reap", "--vault", str(vault), "--dry-run"]))
    assert calls == []
