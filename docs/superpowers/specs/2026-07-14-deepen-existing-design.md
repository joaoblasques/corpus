# Diagnostic-Driven Deepen-Existing — design spec (2026-07-14)

> Status: **proposed, for review.** Sub-project #2 of the "improve the graph and/or corpus" effort
> (#1 = truthful diagnostic map, shipped; #3 = map interactivity, deferred). Turns the now-truthful
> map's weak-spot signals into a concrete depth-building action.

## Goal

Execute the consolidation **deepen-existing** path: for a coherent cluster of source pages whose
topic already has a concept/entity page, **integrate those sources into deepening that page** —
Gardener-style (Opus writer + fail-closed Sonnet critic) — **prioritized by the map's diagnostic
signal** (thinnest page with the most un-integrated related sources first). This is where
consolidation actually adds value on today's corpus: the supervised run found ~0 new syntheses
but the deepen path is the real lever.

## Grounding (measured 2026-07-14)

**16 deepen-existing candidates** — clusters whose topic matches an existing knowledge page —
and thinness ranks them cleanly: `openai.md` (550w, **7** related sources), `localai.md` (724w, 5),
`cursor.md` (779w, 4), `machine-learning.md` (1192w, 6), … while already-deep pages
(`prompt-engineering.md` 3587w) correctly sink to the bottom. Depth ratio is 1:2.9.

## The core action

For a `deepen-existing` cluster `{topic, domain, members, target_page}`:
1. The Opus writer reads the **current target page** + the **member source pages** (and their cited
   raw sources) and **integrates** the members' material into the page — adding cited claims,
   deepening thin sections — **while preserving every existing cited claim**.
2. The fail-closed Sonnet critic verifies BOTH: (a) every NEW claim traces to a cited member source
   (no fabrication, §7); (b) **no pre-existing citation/footnote was dropped** (the deepen only adds).
3. Members gain `consolidated_into: <target_page>` (kept, never deleted — §7.1), so they aren't re-fed.

## The risky part — editing live knowledge (safe by construction)

Editing an EXISTING page is the most dangerous operation in the corpus. Guards:
- **No free rewrite.** The writer prompt mandates: preserve all existing cited claims verbatim-in-
  meaning; only ADD/weave new cited material; keep `type`/`domain`/frontmatter; impersonal tone.
- **Two-sided critic.** Beyond provenance of new claims, the critic explicitly checks the set of
  footnote citations in the deepened page is a **superset** of the original's (nothing dropped).
- **Revert = `git checkout`.** Unlike synthesis (revert = delete the new file), deepen edits a
  tracked file. On any critic failure/error, restore the page to its exact prior bytes via
  `git checkout -- <path>` (or a saved pre-image) and un-stamp members. Fully reversible.
- **Fail closed.** Critic error, dropped-citation, or unparseable verdict ⇒ revert + queue for human.

## Diagnostic-driven prioritization

Rank deepen candidates by the map's weak-spot signal, thinnest-and-most-material first:
`score = cluster_size / max(page_wordcount, 1)` (high = thin page with lots of un-integrated
sources). Process the top `--max` per run. This is the literal "steer by the map" mechanic — the
pale small nodes get deepened first.

## Architecture — reuse, don't rebuild

- `bin/consolidate_run.py`: the `deepen-existing` branch of `process_cluster` today calls
  `queue_reject`. Extend it to call a new `deepen_page(cluster, target_page, corpus, *, _run, _critic)`
  that runs the writer → critic → stamp-or-`git`-revert flow above. `run_consolidation` gains a
  ranked deepen pass (or a `--mode deepen` / it processes both new-synthesis and deepen clusters,
  ranked by the diagnostic score).
- `bin/consolidate.py`: add `rank_deepen_candidates(corpus, domain)` — the clusters whose topic
  matches an existing page, each with its `target_page` path + word count, sorted by the score.
- `bin/consolidate_prompts.py`: add `deepen_prompt(target_page, member_paths)` (preserve-existing +
  integrate-new).
- Critic: reuse `gardener._critic_call`; add a deterministic **citation-superset check** in
  `consolidate_run` (count `[^...]:` footnotes before/after — the deepened page must retain all
  original footnote targets) as a cheap pre-critic guard.
- `bin/scheduled_run.py`: `run_consolidation` already wired weekly + fixture-guarded — deepen rides
  the same weekly Opus slot. The weekly CALL SITE stays deferred until a supervised first run passes.

## Relationship to Gardener (kept distinct)

Gardener deepens `status: stub` pages from their OWN cited sources. Deepen-existing integrates a
CROSS-SOURCE CLUSTER into any concept/entity page (broader than the page's own citations). Different
targets; both edit `corpus/`, so they must not run concurrently — deepen uses the existing
`.consolidate.lock`; Gardener uses `.gardener.lock`; they never run in the same step.

## Non-goals

- No new-synthesis change (that path already exists). No Gardener change.
- Not nightly — weekly/Opus (cap protection). No wiring of the weekly cron until the supervised run.
- No deletion/supersession of members (flag only). No rewrite that can drop existing content.

## Testing

- `consolidate.py`: `rank_deepen_candidates` — a fixture with a thin page + big cluster outranks a
  deep page + small cluster; only clusters matching an existing page are returned.
- `consolidate_run.py`: `deepen_page` — (1) critic PASS → page edited, members stamped; (2) critic
  FAIL → page restored to prior bytes (git checkout), members un-stamped, queued; (3) the
  citation-superset guard rejects a deepen that drops a `[^footnote]`. All via injected `_run`/`_critic`
  + a `tmp_path` git repo; no real claude, no real corpus.
- Supervised first run (manual, on main): `consolidate_run.py run --mode deepen --max-clusters 1`,
  inspect the deepened page's diff (existing claims intact + new cited material), `okf_lint` 0, then
  decide on wiring the weekly cron.

## Success criteria

- Deepen candidates are ranked thinnest-first; the top candidate is a thin page with many
  un-integrated related sources (e.g. `openai.md`).
- A deepened page GAINS cited material and its footnote set is a superset of the original's; a deepen
  that would drop a citation or fabricate is reverted (page byte-identical to before).
- Zero provenance regressions; fully reversible (git); members flagged not deleted.
- The whole test suite stays green; okf_lint 0.
