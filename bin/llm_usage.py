#!/usr/bin/env python3
"""llm_usage.py — summarize raw/.llm_usage.jsonl (local vs Claude, ok rate)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "raw" / ".llm_usage.jsonl"


def summarize(log_path=None) -> dict:
    path = Path(log_path) if log_path else DEFAULT_LOG
    by_provider: Counter = Counter()
    total = local_ok = local_fail = 0
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            total += 1
            by_provider[rec.get("provider")] += 1
            if rec.get("provider") == "ollama":
                local_ok += 1 if rec.get("ok") else 0
                local_fail += 0 if rec.get("ok") else 1
    return {"total": total, "by_provider": dict(by_provider),
            "local_ok": local_ok, "local_fail": local_fail}


def main(argv=None) -> int:
    s = summarize()
    claude = s["by_provider"].get("anthropic", 0)
    print(json.dumps({
        "total_calls": s["total"],
        "local_ollama": s["by_provider"].get("ollama", 0),
        "local_ok": s["local_ok"],
        "local_fail": s["local_fail"],
        "claude": claude,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
