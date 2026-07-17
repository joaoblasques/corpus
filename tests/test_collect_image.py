"""Tests for collect_image.py — the vision-ingest leg (deterministic core; vision stubbed)."""
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_image as ci  # noqa: E402


def _args(**kw):
    return types.SimpleNamespace(**kw)


def test_discover_recurses_and_skips_pdf_hidden_processed(tmp_path):
    w = tmp_path / "watch"
    (w / "sub").mkdir(parents=True)
    (w / "_processed").mkdir()
    (w / "a.png").write_bytes(b"x")
    (w / "sub" / "b.jpeg").write_bytes(b"x")
    (w / "c.pdf").write_bytes(b"x")          # not an image
    (w / ".hidden.png").write_bytes(b"x")    # dotfile
    (w / "_processed" / "old.png").write_bytes(b"x")  # already processed
    names = sorted(d["filename"] for d in ci.discover(w))
    assert names == ["a.png", "b.jpeg"]


def test_discover_missing_dir_returns_empty(tmp_path):
    assert ci.discover(tmp_path / "nope") == []


def test_image_filename_slugifies_and_strips_ext():
    p = ci.image_filename("Pipeline Design Patterns.WEBP", Path("/tmp"))
    assert p.name == "image-pipeline-design-patterns.md"


def test_build_image_source_has_channel_and_fields():
    src = ci.build_image_source(
        {"image_origin": "x.png", "source_path": "/d/x.png", "title": "T",
         "content_sha": "abc", "collected_at": "2026-07-17"},
        "# T\nbody text")
    assert "channel: image" in src
    assert "image_origin: x.png" in src
    assert "source_path: /d/x.png" in src
    assert "content_sha: abc" in src
    assert src.rstrip().endswith("body text")


def test_already_collected_by_sha(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "image-x.md").write_text(
        "---\nchannel: image\ncontent_sha: HASH\n---\nbody", encoding="utf-8")
    assert ci.already_collected("HASH", [d]) is True
    assert ci.already_collected("OTHER", [d]) is False


def test_processable_only_ingested_image_sources(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "image-done.md").write_text(
        "---\nchannel: image\nimage_origin: a.png\nsource_path: /w/a.png\n"
        "corpus_ingested: true\n---\nb", encoding="utf-8")
    (d / "image-pending.md").write_text(          # not yet ingested → excluded
        "---\nchannel: image\nimage_origin: b.png\nsource_path: /w/b.png\n---\nb", encoding="utf-8")
    (d / "pdf-x.md").write_text(                   # ingested but not channel:image → excluded
        "---\nchannel: pdf\ncorpus_ingested: true\n---\nb", encoding="utf-8")
    assert ci.processable([d]) == [("/w/a.png", "a.png")]


def test_vision_extract_parses_json_result_and_handles_failure():
    def ok(cmd, **kw):
        p = types.SimpleNamespace()
        p.returncode = 0
        p.stdout = json.dumps({"result": "# Title\nknowledge"})
        return p
    assert ci.vision_extract("/x.png", _run=ok) == "# Title\nknowledge"

    def fail(cmd, **kw):
        p = types.SimpleNamespace()
        p.returncode = 1
        p.stdout = ""
        return p
    assert ci.vision_extract("/x.png", _run=fail) == ""


def test_cmd_collect_writes_source_titles_it_and_dedups(tmp_path, monkeypatch, capsys):
    w = tmp_path / "watch"
    w.mkdir()
    (w / "a.png").write_bytes(b"imgbytes")
    inbox = tmp_path / "inbox"
    monkeypatch.setattr(ci, "IMG_STORE", tmp_path / "store")   # keep dedup off the real raw/image
    monkeypatch.setattr(
        ci, "vision_extract",
        lambda p, **k: "# Pipeline\nA data pipeline with three distinct stages: ingest, transform, and load.")
    ci.cmd_collect(_args(watch=str(w), inbox=str(inbox), collected_at="2026-07-17",
                         model=None, max=10, dry_run=False))
    src = (inbox / "image-a.md").read_text()
    assert "channel: image" in src and "# Pipeline" in src
    assert "title: Pipeline" in src        # H1 lifted into the title field

    ci.cmd_collect(_args(watch=str(w), inbox=str(inbox), collected_at="2026-07-17",
                         model=None, max=10, dry_run=False))
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert out["duplicate"] == 1 and out["written"] == 0


def test_cmd_collect_skips_empty_extraction(tmp_path, monkeypatch, capsys):
    w = tmp_path / "watch"
    w.mkdir()
    (w / "a.png").write_bytes(b"x")
    inbox = tmp_path / "inbox"
    monkeypatch.setattr(ci, "IMG_STORE", tmp_path / "store")
    monkeypatch.setattr(ci, "vision_extract", lambda p, **k: "too short")  # < 12 words
    ci.cmd_collect(_args(watch=str(w), inbox=str(inbox), collected_at=None,
                         model=None, max=10, dry_run=False))
    assert not (inbox / "image-a.md").exists()
    assert json.loads(capsys.readouterr().out.strip().splitlines()[-1])["failed"] == 1


def test_cmd_collect_dry_run_calls_no_vision(tmp_path, monkeypatch, capsys):
    w = tmp_path / "watch"
    w.mkdir()
    (w / "a.png").write_bytes(b"x")
    inbox = tmp_path / "inbox"
    monkeypatch.setattr(ci, "IMG_STORE", tmp_path / "store")

    def boom(*a, **k):
        raise AssertionError("vision must not be called in a dry run")
    monkeypatch.setattr(ci, "vision_extract", boom)
    ci.cmd_collect(_args(watch=str(w), inbox=str(inbox), collected_at=None,
                         model=None, max=10, dry_run=True))
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert out["written"] == 1 and out["dry_run"] is True
    assert not (inbox / "image-a.md").exists()


def test_cmd_file_moves_ingested_image_into_processed(tmp_path, capsys):
    w = tmp_path / "watch"
    w.mkdir()
    (w / "a.png").write_bytes(b"x")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    (inbox / "image-a.md").write_text(
        f"---\nchannel: image\nimage_origin: a.png\nsource_path: {w}/a.png\n"
        "corpus_ingested: true\n---\nbody", encoding="utf-8")
    ci.cmd_file(_args(watch=str(w), dirs=[str(inbox)], dry_run=False))
    assert not (w / "a.png").exists()
    assert (w / "_processed" / "a.png").exists()
    assert json.loads(capsys.readouterr().out.strip().splitlines()[-1])["moved"] == 1


def test_cmd_file_dry_run_leaves_image_in_place(tmp_path, capsys):
    w = tmp_path / "watch"
    w.mkdir()
    (w / "a.png").write_bytes(b"x")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    (inbox / "image-a.md").write_text(
        f"---\nchannel: image\nimage_origin: a.png\nsource_path: {w}/a.png\n"
        "corpus_ingested: true\n---\nbody", encoding="utf-8")
    ci.cmd_file(_args(watch=str(w), dirs=[str(inbox)], dry_run=True))
    assert (w / "a.png").exists()                       # untouched
    assert not (w / "_processed" / "a.png").exists()
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert out["moved"] == 1 and out["dry_run"] is True
