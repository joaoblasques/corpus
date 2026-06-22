#!/usr/bin/env python3
"""github_client.py — GitHub transport for the repo collector (via the `gh` CLI).

Lists the user's starred repos and fetches README + markdown docs + a metadata overview.
Leaves stars in place. All `gh` calls go through an injectable subprocess seam.
"""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect_github as cg  # noqa: E402

README_CAP = 40_000
DOC_CAP = 15_000


def _gh(api_args, *, _run=None):
    run = _run if _run is not None else subprocess.run
    return run(["gh"] + api_args, capture_output=True, text=True)


def gh_available(*, _run=None) -> bool:
    try:
        return getattr(_gh(["auth", "status"], _run=_run), "returncode", 1) == 0
    except Exception:  # noqa: BLE001
        return False


def list_starred(max_n=None, *, _run=None) -> list:
    p = _gh(["api", "user/starred", "--paginate"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return []
    try:
        data = json.loads(p.stdout)
    except Exception:  # noqa: BLE001
        return []
    out = []
    for it in data if isinstance(data, list) else []:
        out.append({
            "full_name": it.get("full_name"), "html_url": it.get("html_url"),
            "description": it.get("description") or "", "language": it.get("language") or "",
            "stars": it.get("stargazers_count") or 0, "topics": it.get("topics") or [],
            "default_branch": it.get("default_branch") or "main",
        })
        if max_n and len(out) >= max_n:
            break
    return out


def _decode(content) -> str:
    try:
        return base64.b64decode(content or "").decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return ""


def _readme(full_name, _run) -> str:
    p = _gh(["api", f"repos/{full_name}/readme"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return ""
    try:
        return _decode(json.loads(p.stdout).get("content"))[:README_CAP]
    except Exception:  # noqa: BLE001
        return ""


def _latest_release(full_name, _run) -> str:
    p = _gh(["api", f"repos/{full_name}/releases/latest"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return ""
    try:
        return json.loads(p.stdout).get("tag_name") or ""
    except Exception:  # noqa: BLE001
        return ""


def _docs(full_name, max_docs, _run) -> list:
    out = []
    for sub in ("", "docs"):
        ep = f"repos/{full_name}/contents" + (f"/{sub}" if sub else "")
        p = _gh(["api", ep], _run=_run)
        if getattr(p, "returncode", 1) != 0:
            continue
        try:
            items = json.loads(p.stdout)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(items, list):
            continue
        for it in items:
            name = (it.get("name") or "")
            if not name.lower().endswith(".md"):
                continue
            if sub == "" and name.lower() == "readme.md":
                continue
            text = _decode(it.get("content")) if it.get("content") else ""
            if not text and it.get("url"):
                fp = _gh(["api", it["url"]], _run=_run)
                if getattr(fp, "returncode", 1) == 0:
                    try:
                        text = _decode(json.loads(fp.stdout).get("content"))
                    except Exception:  # noqa: BLE001
                        text = ""
            if text:
                out.append({"path": it.get("path") or name, "text": text[:DOC_CAP]})
            if len(out) >= max_docs:
                return out
    return out


def fetch_repo(repo_item: dict, *, max_docs=8, _run=None) -> dict:
    fn = repo_item["full_name"]
    return {**repo_item,
            "latest_release": _latest_release(fn, _run),
            "readme": _readme(fn, _run),
            "docs": _docs(fn, max_docs, _run)}
