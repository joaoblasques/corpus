import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import youtube_client as yc  # noqa: E402


class _FakeReq:
    def __init__(self, resp): self._resp = resp
    def execute(self): return self._resp


def test_list_playlist_items_maps_fields():
    svc = MagicMock()
    svc.playlistItems().list.return_value = _FakeReq({
        "items": [{
            "id": "ITEM1",
            "snippet": {"title": "Vid A", "resourceId": {"videoId": "VA"},
                        "videoOwnerChannelTitle": "Chan A"},
            "contentDetails": {"videoPublishedAt": "2026-06-01T00:00:00Z"},
            "status": {"privacyStatus": "public"},
        }]})
    svc.playlistItems().list_next.return_value = None
    items = list(yc.list_playlist_items(svc, "PL1"))
    assert items[0]["playlist_item_id"] == "ITEM1"
    assert items[0]["video_id"] == "VA"
    assert items[0]["published"] == "2026-06-01"


def test_delete_playlist_item_404_is_success():
    from googleapiclient.errors import HttpError
    svc = MagicMock()
    resp = MagicMock(); resp.status = 404
    svc.playlistItems().delete.return_value.execute.side_effect = HttpError(resp, b"gone")
    assert yc.delete_playlist_item(svc, "ITEM1") is True


def test_extract_transcript_disabled(monkeypatch):
    # Force the youtube_transcript_api path to raise TranscriptsDisabled
    import youtube_transcript_api as yta
    class FakeApi:
        def fetch(self, *a, **k): raise yta._errors.TranscriptsDisabled("V")
    monkeypatch.setattr(yc, "_transcript_api", lambda: FakeApi())
    body, status = yc.extract_transcript("V")
    assert body == "" and status == "disabled"


def test_extract_transcript_ok(monkeypatch):
    class Snip:
        def __init__(self, s, t): self.start, self.text = s, t
    class FakeApi:
        def fetch(self, vid, languages=None): return [Snip(0, "hello"), Snip(30, "world")]
    monkeypatch.setattr(yc, "_transcript_api", lambda: FakeApi())
    body, status = yc.extract_transcript("VID")
    assert status == "ok"
    assert "hello" in body and "world" in body


def test_run_collects_and_removes_only_with_transcript(tmp_path, monkeypatch):
    # one tech playlist, two videos: one with transcript (removed), one without (kept)
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"},
        {"playlist_item_id": "I2", "video_id": "V2", "title": "B", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript",
                        lambda vid: ("[00:00](x) hi", "ok") if vid == "V1" else ("", "disabled"))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)

    args = yc._args(["run", "--sleep", "0"])
    rc = yc.cmd_run(args)
    assert rc == 0
    assert deleted == ["I1"]                      # only the one WITH a transcript removed
    assert (tmp_path / "youtube-V1-a.md").exists()
    assert (tmp_path / "youtube-V2-b.md").exists()  # kept, recorded with disabled status


def test_run_dry_run_never_deletes(tmp_path, monkeypatch):
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}], "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript", lambda vid: ("[00:00](x) hi", "ok"))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)
    rc = yc.cmd_run(yc._args(["run", "--dry-run", "--sleep", "0"]))
    assert rc == 0 and deleted == []
