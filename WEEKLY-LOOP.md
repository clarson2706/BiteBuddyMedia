# The Weekly Loop — one Routine, zero manual steps

*Source of truth for the autonomous weekly content system. Written 2026-07-25.
Executed by `.claude/skills/weekly-loop/SKILL.md`; fired by a claude.ai Routine.*

**Goal:** more people on the App Store page. Every Sunday evening, one run closes last
week's loop (pull real numbers → write analytics → decide what changes) and opens next
week's (generate → render in Canva → schedule via Upload-Post for the whole week).
Connor does nothing during the week.

---

## The one Routine

| | |
|---|---|
| **When** | Sundays **6:00 PM America/Chicago** (23:00 UTC in CDT) |
| **Fires** | a fresh session in this environment, with this repo |
| **Connectors it must carry** | **Upload-Post** + **Canva** (attach both when creating the Routine in the claude.ai Routines UI — a Routine without them can stage but not render/publish) |
| **Prompt** | `Run the weekly loop. Follow WEEKLY-LOOP.md and the weekly-loop skill end to end: analytics first, then generate, render, schedule next week, commit everything, and send Connor the weekly report.` |

Connor creates this Routine once in the claude.ai Routines UI (it has to be created
there so the connectors attach; a Routine created from inside a session can only carry
that session's connectors).

**Optional hardening (recommended once the loop has run twice):** a second, tiny
Wednesday-noon Routine — "verify this week's scheduled posts still exist in
Upload-Post; repair anything missing; say nothing if all fine." Covers the
run-died-midweek and platform-disconnected failure modes.

## The run, in strict order

Each phase gates the next. **Phase 2 must refuse to run if Phase 1 didn't write its
outputs this run** — that rule is the entire fix for the last system's fatal flaw
(a full analytics pipeline whose log stayed 0 bytes forever).

### Phase 1 — CLOSE the loop (analytics)
1. Pull per-post metrics from Upload-Post analytics for every post published in the
   last 14 days (views, likes, comments, shares, saves, completion where available).
2. Append one snapshot line per post×platform to `Analytics/performance-log.jsonl`.
3. Read `Analytics/installs.jsonl` if Connor has added numbers (optional, manual).
4. Write **`Analytics/<week>-report.md`** — what went well / what didn't / what
   changes next week, with per-series, per-persona, per-hook-family tables.
5. Write **`Analytics/next-week-directives.json`** — the machine-readable steer.
6. Commit. *(All analytics artifacts are committed — nothing gitignored. The old
   system gitignored its rollups, so they could never exist.)*

### Phase 2 — OPEN the loop (generate)
1. Hard gate: `next-week-directives.json` must exist with this run's timestamp.
2. Read the directives + `Content-Engine/registry.jsonl` (everything ever posted —
   the dedupe memory) + the persona/hook/series docs.
3. Generate **14 posts** (2/day × 7): copy, caption, pinned comment, hashtags,
   persona, hook family, visual recipe, series slot, platform plan, time slot.
   Slot template per week (adjustable by directives, never by whim):
   - 8 series posts: 2 × each active series (see `Content-Engine/SERIES.md`)
   - 2 re-cuts of last week's winners (fresh cover, same skeleton) — only when
     directives name winners; otherwise 2 extra experiments
   - 4 experiments (new hooks/topics/formats to feed the next report)
4. Append every post to the registry. Write the week's `manifest.json`.

### Phase 3 — RENDER (Canva)
1. For each post, build the deck from the archetypes in
   `Content-Engine/DESIGN-SYSTEM.md`, compositing the real Buddy cutouts
   (`Brand-Assets/buddy-poses/transparent/`) and real app screenshots (`UI-Library/`).
2. Export 1080×1350 PNGs into `Posts/<week>/<post-id>/`.
3. A post that fails to render is dropped from the schedule and named in the report —
   never published half-made.

### Phase 4 — SCHEDULE (Upload-Post)
1. Preflight: token valid, plan sufficient, which platforms are actually linked.
   Anything unlinked is skipped and reported, not guessed at.
2. Schedule every rendered post at its slot, **enforcing the rate rules in code**:
   TikTok ≤3/day · Instagram ≤2/day · never two platforms at the same minute ·
   ≥4h spacing per platform. Slots: TikTok 8:00 AM + 7:00 PM · Instagram 12:30 PM
   (+ 7:30 PM Fri only) · YouTube Short 1/day 5:00 PM · Facebook mirrors Instagram.
   Captions/crops vary per platform (duplicate-content penalty).
3. Record scheduled IDs/URLs in the manifest.

### Phase 5 — REPORT
Commit + push everything, then message Connor: the week's 14 titles by day, what got
scheduled where, what was dropped and why, and the Phase-1 report's three headlines
(went well / didn't / changing). **Posts start Monday 8 AM — Sunday night is Connor's
standing veto window.** Silence = go. "Pull Tuesday's quiz" = I unschedule it.

## Publishing authority

Connor has authorized this loop to schedule and publish **without per-post approval**
(2026-07-25) — the veto window replaces draft-then-approve **for this Routine's
carousel posts only**. Money, App Store copy, DMs/outreach, and anything outside the
weekly carousels still require explicit approval. Guardrails in `CLAUDE.md` apply to
every slide, always.

## What "success" means (metric ladder)

We optimize the closest measurable proxy to App Store installs, in this order:
1. **Installs** — only if Connor pastes App Store Connect numbers into
   `Analytics/installs.jsonl` (10 seconds/week, optional but decisive)
2. **Link clicks** (YouTube/Facebook links) + **"what app is this?" comments**
3. **Saves + shares** (highest-intent engagement)
4. **Follows / profile activity**
5. Views last — reach without saves is entertainment, not marketing.

A "winner" is a post strong on 2–4, not just 5. The report must say so explicitly.

## Series testing protocol

Defined in `Content-Engine/SERIES.md`. Short version: 3 active series slots, each gets
2 posts/week for a minimum 2 weeks before any verdict (small samples lie); verdicts are
**scale / iterate / kill**, decided in the weekly report by save-rate and
follow-attribution, and a killed series is replaced from the bench, keeping 3 active.

## Failure handling

- **Upload-Post missing/unauthed at fire time** → full stop after Phase 3: everything
  staged + committed, nothing published, Connor told exactly what to reconnect.
- **Canva missing** → Phases 1–2 still run (analytics + copy committed), render/schedule
  skipped, Connor told.
- **A publish call fails** → retry ×3 with backoff → mark failed in manifest, continue
  with the rest, report it.
- **No analytics data returned** (week 1, or API gap) → Phase 1 still writes the report
  saying exactly that, directives carry `"confidence": "none"`, Phase 2 runs the default
  slot template. The gate is that Phase 1 *ran*, not that data existed.
