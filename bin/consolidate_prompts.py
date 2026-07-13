#!/usr/bin/env python3
"""consolidate_prompts.py — prompt builders for the consolidation runner (pure strings)."""
from __future__ import annotations


def triage_prompt(topic: str, domain: str, member_titles: list[str]) -> str:
    titles = "\n".join(f"- {t}" for t in member_titles)
    return (
        f"You are triaging a candidate knowledge cluster in the '{domain}' domain of a personal "
        f"corpus. The cluster topic is \"{topic}\". Its member source-summary pages are:\n{titles}\n\n"
        "Decide ONE mode:\n"
        "- \"new-synthesis\": the members form a COHERENT topic worth ONE synthesis page and no "
        "such concept/synthesis page exists yet.\n"
        "- \"deepen-existing\": a concept page for this topic already exists; these members should "
        "feed its expansion instead of a new page.\n"
        "- \"reject\": the members are a grab-bag / too incoherent / too thin to synthesize.\n\n"
        "Reply with STRICT JSON only, no prose: "
        '{"mode": "new-synthesis|deepen-existing|reject", '
        '"title": "<concise Title Case page title>", '
        '"slug": "<kebab-case-slug>", "reason": "<one sentence>"}'
    )


def synthesis_prompt(topic: str, domain: str, slug: str, member_rel_paths: list[str]) -> str:
    members = "\n".join(f"- corpus/{m}" for m in member_rel_paths)
    out_path = f"corpus/{domain}/{slug}.md"
    return (
        f"Write ONE dense `synthesis` page consolidating these source-summary pages on \"{topic}\" "
        f"in the '{domain}' domain. Read every member page first:\n{members}\n\n"
        f"Create EXACTLY this file: {out_path}\n\n"
        "Rules (from CLAUDE.md):\n"
        f"- Frontmatter: type: synthesis, domain: {domain}, status: draft, plus a `consolidates:` "
        "list holding EVERY member path above, `created`/`updated` today, tags [corpus/"
        f"{domain}, synthesis].\n"
        "- Structure: TL;DR first, then the mental model, then patterns/gotchas.\n"
        "- Every non-trivial claim CITES a member's original source via a footnote [^n] (reuse the "
        "members' own source citations). NEVER invent a claim not present in a member. Keep any "
        "verbatim quote to 25 words max, one per source.\n"
        "- Link each member page inline with a root-relative link [title](/"
        f"{domain}/sources/<slug>.md).\n"
        "- Impersonal, reference-dense. Do NOT edit any file other than the one synthesis page."
    )
