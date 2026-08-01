# System audit — 2026-08-01

*A full read of the media system: every file, every skill, the live Upload-Post account,
the git history, and the numbers. This is a standing document. When a finding is fixed,
mark it fixed here rather than deleting it, so the same mistake is harder to make twice.*

**Headline: the content system works better than the system around it.** The strategy
docs are good, the research is real, the guardrails are thought through, and TikTok
reach is climbing fast. What is broken is everything between "a post goes out" and "a
person installs the app," plus a set of process failures that quietly destroy the
system's memory of its own work.

Severity: **P0** breaks the mission · **P1** costs real growth · **P2** worth fixing.

---

## P0 — Breaks the mission

### A1. The funnel ends at the view. FIXED IN PART.
4,408 TikTok views produced 1 follower, 0 profile views, 0 comments, 0 shares. Nothing
in any post asked for the one action a TikTok viewer can actually take (tapping the
profile), there is no tracked bio link, and `installs.jsonl` has never existed, so no
install could ever be attributed to anything.

*Fixed here:* every carousel now closes with a follow ask rendered into the slide
(`render_slides.slide_cta`). *Still open, and it is Connor's 15 minutes:* the tracked
bio link with an App Store campaign token, the pinned conversion post, and the first
`installs.jsonl` line. Full diagnosis and setup: `Analytics/CONVERSION.md`.

### A2. Loop runs strand their memory on unmerged branches. FIXED (guard added).
Three branches carry work `main` has never seen: `tender-bardeen-2tb8bj` (a full W31
week, 147 files), `jolly-bardeen-qi8pby` (the same plus a Wednesday mini-run, 163
files), and `marketing-report-brainstorm-azv0rm` (a `Reports/` tree, a `growth-report`
skill, an Instagram investigation and a real `report.py` bug fix).

Consequences, all live right now: the registry on `main` knows about 6 posts while 25
have been generated, so the next generation run **will duplicate topics it already
published**; the analytics join cannot resolve any W31 post; and Connor's veto window
shows a week that is not the week that is scheduled.

The loop's Phase 6 says "open a PR" and nothing says "merge it," so every run since
07-25 has quietly written to a dead end.

*Fixed:* `preflight.py` fails the run when a branch carries content memory neither
`main` nor the current branch has, the SessionStart hook warns before any work begins,
and `WEEKLY-LOOP.md` now requires the merge, not just the PR.

**All three branches were merged on 2026-08-01.** The registry went from 6 posts to 25
and `schedule-drift` now passes. Two conflicts, both resolved without losing data:

- `render_slides.py` — the hardcoded `POSES` table that `jolly-bardeen` extended versus
  this branch's removal of it. Resolved toward the manifest-driven version, and all 24
  pose assignments were migrated into the manifests rather than dropped. Every post in
  W30, W30-flex and W31 now carries its own `poses` field, which is the fix the conflict
  was pointing at: patching a Python dict per post is what made the branch diverge.
- `performance-log.jsonl` — append-only history, so the union is the only correct
  resolution. 48 lines and 35 lines reconciled to 58 distinct snapshots with 25 exact
  duplicates dropped, every surviving line re-parsed as JSON before writing.

### A3. Nine posts are scheduled that exist nowhere in the repo. FIXED (guard added).
`list_scheduled` returns 9 queued posts for Aug 1 to 3. Zero appear in
`registry.jsonl` on `main`. This is A2's symptom, and it is the exact class of failure
the 2026-07-25 rebuild was written to prevent, one level up: the old system's log was
0 bytes, this system's log is fine but points at a branch nobody merged.

*Fixed:* preflight cross-checks the live schedule against the registry and fails on
drift. After the A2 merges it reports `all 8 scheduled posts are present in the
registry`.

---

## P1 — Costs real growth

### B1. Every slide was rendered at Instagram's aspect ratio. FIXED.
`render_slides.py` emitted 1080x1350 only. TikTok is the primary channel and letterboxes
4:5, so roughly a third of the screen was fill bars on the one platform that matters,
and the hook shrank with it. TikTok's native carousel size is 1080x1920.

*Fixed:* the renderer now emits `tiktok/` at 1080x1920 as the primary set and `ig/` at
1080x1350 alongside it, with per-format safe areas. The TikTok spec reserves the bottom
420px for the caption overlay and keeps content clear of the right-hand action rail,
neither of which the old renderer knew about. Buddy was moved to the bottom-left of
covers for the same reason.

### B2. TikTok carousels publish silently, and nothing said so.
TikTok photo posts cannot carry a sound through the API: music is a video-only field.
Sound is a documented distribution lever on Photo Mode, so every carousel this system
publishes competes with a hand tied behind its back, and no document mentioned it.

*Fixed here:* documented in `START-HERE.md`, `Content-Engine/UPLOAD-POST.md` and
`SERIES.md`. The strategic consequences are real and should be acted on: slide 1 has to
carry the entire hook, the demo video track is the *only* format in this system that
gets audio distribution at all (an argument for more demos), and the single
highest-value post of the week is worth Connor posting by hand in the TikTok app.

### B3. Body slides looked like the thing the research says is now penalised. FIXED.
The old typographic slide was one centered sentence in the middle of an empty cream
frame. `HOOK-INTELLIGENCE-2026.md` names "the generic template-y Canva infographic
look" as a 2026 slop tell on an account that already matches the risk profile TikTok's
July crackdown targets (faceless, health, high-frequency, AI-produced).

*Fixed:* six real layouts now exist rather than one — `rank`, `compare`, `grid`, `big`,
`step` and an improved left-aligned type card with an accent rule — plus a four-way
rotating background accent so consecutive slides do not share a silhouette. Reference
decks for all of them live in `Posts/_TEMPLATES/`.

### B4. The renderer required a code edit for every new post. FIXED.
Buddy poses lived in a hardcoded `POSES` dict keyed by post id. A post missing from it
silently rendered the wrong mascot, and every week's run had to patch the script, which
is exactly what the stranded `jolly-bardeen` branch did.

*Fixed:* poses come from the manifest (`post["poses"]`), with a documented default.
Series badges are overridable per post too, so an S2 episode ranking protein per 100
calories no longer wears a chip reading PROTEIN PER DOLLAR.

### B5. Guardrails were enforced by good intentions only. FIXED.
`CLAUDE.md` lists non-negotiable content rules. Nothing checked them. A run under time
pressure, or a future model with a different sense of the line, could publish a medical
claim and nothing would object.

*Fixed:* `Content-Engine/copy_lint.py` turns each rule into an assertion — outcome and
medical claims, precision claims, the Meal Advisor, em dashes, CTA structure, slide
counts, hashtag counts — and `preflight.py` runs it over every manifest. It already
found a real defect: the flex post's caption omitted the App Store search line its
`cta_type: APP` promised.

### B6. The series roster was weighted away from what gets saved. FIXED (roster changed).
Three of four active slots went to psychology and quiz content. The account has 0
saves and 0 shares, which is consistent: nobody saves an essay. The research is most
confident about exactly the format the roster underweighted — chain rankings and cheat
sheets are the most-saved carousel type, and saves are a heavy ranking input.

*Fixed:* `SERIES.md` rebalanced to 5 Ranked + 4 Best Order + 4 Guess + 2 Why Tracking
Fails. The ranked format is also the one Connor independently identified as working.

### B7. No dependency bootstrap. FIXED.
A fresh Routine session has neither `pillow` nor `upload-post` installed, so
`render_slides.py` would have died on import at fire time. Nothing in the loop
installed them.

*Fixed:* preflight checks imports and names the exact `pip install` to run, before any
phase that needs them.

---

## P2 — Worth fixing

### C1. Documentation had drifted from reality on four load-bearing facts. FIXED.
Each of these was stated confidently and each is wrong as of today:

| Claim in the docs | Reality on 2026-08-01 |
|---|---|
| "Upload-Post is not a claude.ai connector and cannot be attached to a Routine" | An Upload-Post MCP tool set is live in-session. The REST API still works and remains the right transport for Routines, but the flat claim is false. |
| "The Instagram account is spam-restricted; only Connor can clear it" | `list_users` returns `instagram: ""` — an empty string. That is a dropped token needing a reconnect, not a ban. A 2026-07-29 investigation on an unmerged branch had already established this. |
| "chipotle.com, chick-fil-a.com, mcdonalds.com, starbucks.com and fdc.nal.usda.gov return 403, so S1 and S2 are blocked" | All return 200. Chain numbers are verifiable, which is what makes the ranked series possible at all. |
| "Analytics/ was scaffolding for a log that never received a line" (README) | The log has 25 lines and real data. The README still describes the pre-reset state. |

### C2. `installs.jsonl` is documented but has never existed.
It is the top rung of the metric ladder and the only thing that can distinguish
"posts like X produce installs" from "posts like Y produce applause." See
`Analytics/CONVERSION.md` §3.4 for the one-line-per-week format, now extended with a
`by_campaign` breakdown.

### C3. `get_history` returns HTTP 400.
The documented reconciliation path ("compare scheduled against actually published")
does not work. `list_scheduled` and per-post analytics via `request_id` do, so
reconciliation should be rebuilt on those. Worth a note rather than a workaround.

### C4. The Wednesday mini-run and the daily DM Routine are unverified here.
`CLAUDE.md` says the 8 AM creator DM batch is paused and last fired 2026-07-25. The
`Outreach/batches/` directory contains exactly one file, from 2026-07-25, which
corroborates it. The creator engine is one of the four sprint levers and it has not run
in a week. That is a decision for Connor, not a bug, but it should not stay invisible.

### C5. Two Canva template links point at single-page "AI starter" designs.
`Content-Engine/TEMPLATES.md` describes a render route the system does not use, since
Canva cannot build a multi-page carousel in one call and this environment cannot
download Canva exports. The file should say plainly that it documents a road not taken.

---

## What was verified live during this audit

- Upload-Post `list_users`: TikTok and YouTube linked and healthy, Instagram empty
  string, Facebook absent, plan `basic`.
- Upload-Post `list_scheduled`: 9 posts queued Aug 1 to 3, cadence and spacing legal.
- Upload-Post `get_analytics`: the TikTok and YouTube numbers quoted throughout.
- `chick-fil-a.com` nutrition pages: four items fetched and used in the reference deck.
- Git: 8 remote branches, 3 unmerged and carrying content memory.
- A fresh render of both reference decks in both formats, inspected slide by slide.
