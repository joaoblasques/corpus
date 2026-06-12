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
