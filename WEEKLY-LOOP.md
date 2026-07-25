# The Weekly Loop — two Routines, zero manual steps

*Source of truth for the autonomous weekly content system. Written 2026-07-25;
upgraded to twice-weekly cadence for the Aug-25 sprint (`SPRINT-AUG25.md`).
Executed by `.claude/skills/weekly-loop/SKILL.md`; fired by claude.ai Routines.*

**Goal:** more people on the App Store page. Sunday closes last week's loop (real
numbers → analytics → decisions) and opens next week's (generate → render in Canva →
schedule via Upload-Post). Wednesday is a mini-run that doubles iteration speed.
Connor's week: send the day's DM batch, forward replies, veto anything he dislikes.

---

## The two Routines

Connor creates both in the claude.ai Routines UI (they must be created there so the
connectors attach; a Routine created from inside a session can only carry that
session's connectors). Both fire a fresh session in this environment with
**Upload-Post + Canva** attached.

**Routine 1 — Sunday full loop.** Sundays 6:00 PM America/Chicago. Prompt:

> Run the weekly loop, full Sunday mode. Follow WEEKLY-LOOP.md and the weekly-loop
> skill end to end: analytics first, then generate, render, and schedule next week,
> write the Mon/Tue/Wed outreach batches, process creator pipeline updates, commit
> everything, and send Connor the weekly report and veto window.

**Routine 2 — Wednesday mini loop.** Wednesdays 12:00 PM America/Chicago. Prompt:

> Run the weekly loop, Wednesday mini mode per WEEKLY-LOOP.md: snapshot Mon/Tue
> numbers, kill or re-cut this week's losers and re-cut the early winner into fresh
> covers for the Thu-Sun slots, write the Thu/Fri outreach batches, process creator
> replies, commit, and send Connor a two-line midweek pulse.

## The Sunday run, in strict order

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

### Phase 5 — OUTREACH (creator engine, see `Outreach/`)
1. Write the Mon/Tue/Wed DM batches (60 personalized messages, 10 IG + 10 TikTok per
   day) into `Outreach/batches/`, each researched against the creator's real profile.
   Hard rules from `Outreach/DM-PLAYBOOK.md` apply, including: **no em dashes in any
   outbound copy.**
2. Process pipeline updates Connor forwarded (replies, agreements, posted content):
   advance statuses in `creators.jsonl`, generate onboarding packs for new deals,
   grant free-Pro entitlements in RevenueCat.
3. On the run closest to month end: compute creator payouts from attribution data,
   write `payouts.jsonl` lines, and hand Connor the ready-to-send payout DMs with
   PayPal amounts.

### Phase 6 — REPORT
Commit + push everything, then message Connor: the week's 14 titles by day, what got
scheduled where, what was dropped and why, the Phase-1 report's three headlines
(went well / didn't / changing), sprint checkpoint status (`SPRINT-AUG25.md` table),
and the creator-pipeline pulse (sent / replied / deals / posts live). **Posts start
Monday 8 AM — Sunday night is Connor's standing veto window.** Silence = go. "Pull
Tuesday's quiz" = I unschedule it.

## The Wednesday mini-run

Half the loop, for speed, ~30 minutes of compute not a full regeneration:

1. **Snapshot:** pull Mon/Tue numbers for this week's live posts, append to the log.
2. **Kill/re-cut:** a post clearly dying (bottom of the week, no saves, no comments)
   gets its remaining sibling slots re-pointed; the early winner gets 2 or 3 fresh
   covers (same body, new hook slide) rendered and swapped into Thu-Sun slots.
   Changes are surgical; no full regeneration midweek.
3. **Outreach:** write Thu/Fri DM batches (40 messages); process forwarded replies.
4. **Pulse:** two lines to Connor. What's winning, what changed. No veto ceremony;
   midweek changes only touch not-yet-published slots.

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
