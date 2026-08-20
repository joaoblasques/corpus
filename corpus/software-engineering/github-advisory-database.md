---
type: concept
domain: software-engineering
status: draft
aliases:
  - GitHub Advisory Database
  - advisory database
  - CVE advisory
  - GHSA
  - GitHub security advisories
  - Dependabot alerts
  - private vulnerability reporting
  - PVR
tags:
  - corpus/software-engineering
  - concept
  - security
  - open-source
sources:
  - path: raw/web/web-inside-the-advisory-database-and-what-happens-when-vulnerabi-9961abc5.md
    channel: web
    ingested_at: 2026-08-20
created: 2026-08-20
updated: 2026-08-20
---

# GitHub Advisory Database

**TL;DR**: The GitHub Advisory Database is the human-validated vulnerability dataset powering Dependabot alerts. In 2026 it hit record volume (1,560 reviewed advisories in May 2026 alone — 5× normal), driven by structural growth in the vulnerability disclosure ecosystem; the bottleneck is curator throughput for complex advisories, not data pipeline quality.[^src1]

## What "reviewed" means

A reviewed advisory is not a republished record — it's the result of human verification. Curators:

1. Map the vulnerability to the correct ecosystem package
2. Validate affected and fixed versions against release history
3. Confirm upstream accuracy
4. Check for duplication and consistency
5. Validate classification and scoring

"Publishing faster by skipping verification would increase false positives at scale, which can create more risk than delay."[^src1]

## Scale (2026 context)

- May 2026: 1,560 reviewed advisories published — 5× typical monthly output, highest in database history[^src1]
- March–May 2026: >6,000 advisory decisions per month (new + updates + reviews)
- Private vulnerability reports grew from ~550/week (January) to >3,000/week (May)
- Repository advisories grew from ~650/week to >5,000/week
- GitHub CNA CVE requests: ~4,000 in May 2026 alone, ~10× year-over-year
- 1.7+ million repositories now have private vulnerability reporting enabled
- CVE program published 30,000+ CVEs in 2026 (through May)

## What's hard (complex advisory cases)

Not all advisories are equal. Harder cases compound curation time:

- **Package disambiguation**: "foo" on npm vs. python-foo on PyPI vs. Maven foo
- **Version range reconstruction**: advisory arrives with no affected range — curators trace commits, changelogs, tags
- **Multi-ecosystem advisories**: same library ships to .NET (NuGet) + JavaScript (npm), both need independent verification
- **Conflicting upstream data**: CVE record, maintainer advisory, and commit history disagree[^src1]

## How to submit high-quality advisories (community guidance)

- Include complete data: affected version ranges, root cause, reproduction steps
- Use the package name exactly as it appears in the registry (not the repo or project name)
- List all affected packages separately with ecosystem, name, and version range
- Provide a complete CVSS 3.1 or 4.0 vector string (not just a label like "High")
- Include relevant CWE classification for the underlying weakness
- Request CVEs only when there is clear intent to publish
- Coordinate closely with maintainers and other researchers before submission[^src1]

## GitHub's response to the surge

- Strengthened triage + prioritization to move high-quality submissions faster
- Scaled backend curation infrastructure
- Deployed AI-assisted research tooling (curators still make every decision)
- Improved automation for extracting data from upstream CVE records
- Expanded operational documentation for team onboarding

## Downstream impact

- **Dependabot users**: existing alerts unaffected; new advisories may trigger more slowly (critical issues prioritized)
- **API/feed consumers**: reviewed data is accurate; unreviewed advisories visible but not yet validated
- **Maintainers**: repository advisories flow into the global database; prioritization weighs project impact and severity[^src1]

[^src1]: raw/web/web-inside-the-advisory-database-and-what-happens-when-vulnerabi-9961abc5.md — GitHub Blog, "Inside the Advisory Database and what happens when vulnerability volume breaks records" (2026)
