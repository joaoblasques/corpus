from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "website" / "docs"
FORBIDDEN = ["/Users/", "tilakapash@gmail.com", "ANTHROPIC_API_KEY", "Bearer ", "ghp_", "sk-ant"]


def test_no_private_data_in_published_docs():
    offenders = []
    for md in DOCS.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for needle in FORBIDDEN:
            if needle in text:
                offenders.append(f"{md.relative_to(DOCS)}: {needle}")
    assert not offenders, offenders
