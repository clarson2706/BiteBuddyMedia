# The Weekly Loop — three Routines, zero manual steps

*Source of truth for the autonomous weekly content system. Written 2026-07-25;
upgraded to twice-weekly cadence for the Aug-25 sprint (`SPRINT-AUG25.md`).
Executed by `.claude/skills/weekly-loop/SKILL.md`; fired by claude.ai Routines.*

**Goal:** more people on the App Store page. Sunday closes last week's loop (real
numbers → analytics → decisions) and opens next week's (generate → render in Canva →
schedule via Upload-Post). Wednesday is a mini-run that doubles iteration speed.
Connor's week: send the day's DM batch, forward replies, veto anything he dislikes.

---

## The three Routines

All three fire a fresh session in this environment. Routines 1 and 2 need
**Upload-Post + Canva**; Routine 3 needs neither (it only reads the repo and the web).

### Connector / credential status (verified 2026-07-25)

**Upload-Post is not a claude.ai connector and cannot be attached to a Routine.** It is
not in the org's connector directory at all. Publishing therefore uses the **Upload-Post
REST API with an API key**, which is better for automation anyway: no OAuth to expire,
no connector inheritance, identical behaviour in every fired session. Setup and usage:
`Content-Engine/UPLOAD-POST.md`. The one requirement is the environment variable
`UPLOAD_POST_API_KEY` set in this CCR environment's settings.

**Canva is a real connector** and must be attached to Routines 1 and 2 in the claude.ai
Routines UI (Connor did this on 2026-07-25). Routine 3 needs no connectors.

| Routine | Repo source | Canva | Needs | Status |
|---|---|---|---|---|
| 1 Sunday full loop | ✅ `BiteBuddyMedia` | ✅ | `UPLOAD_POST_API_KEY` | ready |
| 2 Wednesday mini loop | ✅ `BiteBuddyMedia` | ✅ | `UPLOAD_POST_API_KEY` | ready |
| 3 Daily DM batch | ✅ `BiteBuddyMedia` | n/a | nothing | ready |

All three verified on the correct repo 2026-07-25. Routines 1 and 3 keep a repo guard
as their first instruction (verify the repo, write nothing if wrong) since a Routine's
source can only be changed in the claude.ai Routines UI, never through the API.

`UPLOAD_POST_API_KEY` was set in the environment on 2026-07-25. Note that environment
variables apply at **session start**, so a session already running when the variable is
added will not see it; only newly fired sessions do. If the key is ever missing or
rejected, Routines 1 and 2 degrade as designed: analytics, generation, and render run
and commit; publishing stops and the report says so.

**Model note:** Routine 3 should run cheaply on Sonnet. Setting a Routine's model is
disabled for this org, so its prompt delegates research and drafting to Sonnet subagents.

**Routine 1 — Sunday full loop.** Sundays 6:00 PM America/Chicago. Prompt:

> Run the weekly loop, full Sunday mode. Follow WEEKLY-LOOP.md and the weekly-loop
> skill end to end: analytics first, then generate, render, and schedule next week,
> process creator pipeline updates, commit everything, and send Connor the weekly
> report and veto window.

**Routine 2 — Wednesday mini loop.** Wednesdays 12:00 PM America/Chicago. Prompt:

> Run the weekly loop, Wednesday mini mode per WEEKLY-LOOP.md: snapshot Mon/Tue
> numbers, kill or re-cut this week's losers and re-cut the early winner into fresh
> covers for the Thu-Sun slots, process creator replies, commit, and send Connor a
> two-line midweek pulse.

**Routine 3 — Daily DM batch.** Every day 8:00 AM America/Chicago. Runs on
**Sonnet 5** (cheap, and the task is research plus short writing, not strategy).
Owns creator-batch generation; the loop runs no longer write batches. Prompt:

> Generate today's BiteBuddy creator DM batch per Outreach/DM-PLAYBOOK.md. Find 10
> Instagram and 10 TikTok nano/micro creators (2k to 60k followers) in our niches who
> are NOT already in Outreach/creators.jsonl. For each one give me: the handle and
> profile link, one sentence on who they are and what the account does, one sentence
> on why they are a good fit for BiteBuddy, and the ready-to-send personalized DM.
> Follow every hard rule in the playbook, especially: no em dashes anywhere, every
> message references something specific and real from that creator's content, and
> never claim we are bigger than we are. Append them to creators.jsonl with status
> dm_written, write the batch to Outreach/batches/<today>.md, commit, and send Connor
> the batch in the message so he can copy and send from his phone.

If run off-schedule, it produces only the current day's batch (see Partial
generation below).

## The Sunday run, in strict order

Each phase gates the next. **Phase 2 must refuse to run if Phase 1 didn't write its
outputs this run** — that rule is the entire fix for the last system's fatal flaw
(a full analytics pipeline whose log stayed 0 bytes forever).

### Phase 0 — PREFLIGHT (added 2026-08-01, runs before everything)

```bash
python3 Content-Engine/preflight.py
```

**A non-zero exit stops the run.** It is not advisory and it is not to be worked
around; if a check is wrong, fix the check in the same commit as the run. It verifies
dependencies (a fresh Routine session has neither pillow nor upload-post installed),
render assets, **unmerged branches carrying content memory**, registry sanity,
directive freshness, the copy guardrails, which platforms are actually linked, whether
the live schedule matches the registry, and whether the queued cadence is legal.

Phase 0 exists because two runs in a row failed in ways it would have caught in five
seconds: a full week of posts stranded on an unmerged branch, and nine posts scheduled
on the live account that appear nowhere in the repo.

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
3. Generate **21 posts** (3/day × 7): copy, caption, pinned comment, hashtags,
   persona, hook family, visual recipe, series slot, platform plan, time slot.
   Slot template per week (adjustable by directives, never by whim):
   - 12 series posts: 4 × each active series (see `Content-Engine/SERIES.md`)
   - 3 re-cuts of last week's winners (fresh cover, same skeleton) — only when
     directives name winners; otherwise 3 extra experiments
   - 6 experiments (new hooks/topics/formats to feed the next report)

   **Seven of the 21 are TikTok-only** — the 1:00 PM flex slot (see Phase 4). Fill
   that slot from the experiment pool first: it is the slot a demo video displaces,
   so it should hold the most expendable content, not a series episode.
4. Append every post to the registry. Write the week's `manifest.json`.

### Phase 3 — RENDER (`Content-Engine/render_slides.py`)
1. Run the renderer over the week's manifest. It writes **two sets**: `tiktok/` at
   1080×1920 (the primary set, TikTok's native carousel size) and `ig/` at 1080×1350,
   from the brand palette, the Baloo 2 brand font, and the real Buddy cutouts. Hand the
   TikTok set to TikTok: 4:5 letterboxes there and throws away a third of the screen on
   the platform that matters most. Buddy poses come from each post's `poses` field in
   the manifest, never from a table inside the script.
2. Canva is **not** the batch render path: `generate-design` emits one page per call so
   it cannot build a carousel, and this environment cannot download Canva exports. Canva
   stays available for one-off polish and manual edits.
3. Commit and push the PNGs, then serve them to Upload-Post from
   `raw.githubusercontent.com` at the **commit SHA** (the repo is public; the SHA is
   immutable, so a later push cannot alter a scheduled post).
4. Eyeball at least one deck before scheduling. A post that fails to render is dropped
   and named in the report, never published half-made.

### Phase 4 — SCHEDULE (Upload-Post REST API, see `Content-Engine/UPLOAD-POST.md`)
1. Preflight via `list_users`: API key valid, plan headroom sufficient, which platforms
   are actually linked (`social_accounts` entries that are not null). Anything unlinked
   is skipped and reported, not guessed at.
2. Schedule every rendered post at its slot, **enforcing the rate rules in code**:
   TikTok ≤3/day · Instagram ≤2/day · never two platforms at the same minute ·
   ≥4h spacing per platform. Captions/crops vary per platform (duplicate-content
   penalty).

   | Platform | Slots (America/Chicago) |
   |---|---|
   | TikTok | **8:00 AM · 1:00 PM · 7:00 PM** — 3/day, the default |
   | Instagram | 12:30 PM (+ 7:30 PM Fri only) — stays at 2/day |
   | YouTube | Short 1/day, 5:00 PM |
   | Facebook | mirrors Instagram +15 min |

   **The 1:00 PM TikTok slot is the flex slot.** It runs a carousel by default and a
   demo video whenever one is queued for that day (see the **demo-drop** skill). A
   demo *replaces* the carousel there rather than adding a fourth post, because
   3/day is TikTok's ceiling, not a target to exceed.

   **The third slot is TikTok-only.** Instagram stays at 2/day: the cap in
   `HOOK-INTELLIGENCE-2026.md` is 2, and the July 22 throttle landed on Instagram.
   Do not fan the flex-slot post out to Instagram to "use" the content.

   Spacing check: 8:00 / 13:00 / 19:00 leaves 5h and 6h gaps. The July 22 incident
   was five *simultaneous* posts, not five posts in a day. Spacing is the thing that
   matters, and this keeps it.
3. Submit the whole week in this one run using `scheduled_date` (ISO-8601) +
   `timezone: America/Chicago`; pass the pinned comment as `first_comment`. Hand Canva
   export URLs straight to the API rather than downloading media locally. Record the
   returned `job_id`s and URLs in the manifest for later reconciliation against
   `get_history`.

### Phase 5 — OUTREACH (creator engine, see `Outreach/`)
1. Daily DM batches are owned by **Routine 3**, not by the loop runs. The loop only
   sanity-checks that batches exist and flags it in the report if Routine 3 has not
   been producing them.
2. Process pipeline updates Connor forwarded (replies, agreements, posted content):
   advance statuses in `creators.jsonl`, generate onboarding packs for new deals,
   grant free-Pro entitlements in RevenueCat.
3. On the run closest to month end: compute creator payouts from attribution data,
   write `payouts.jsonl` lines, and hand Connor the ready-to-send payout DMs with
   PayPal amounts.

### Phase 6 — REPORT, AND MERGE

**Merging is part of the run, not an afterthought.** Commit, push the week branch, open
the PR, and then **merge it to `main`** (or leave it open only if a human veto is
genuinely pending, and say so explicitly in the report). A run that ends on an unmerged
branch has thrown away its own memory: the registry cannot dedupe against it, the
analytics join cannot resolve its posts, and the next run will regenerate topics that
are already scheduled. This happened three times between 07-25 and 07-30.

The report opens with the **conversion scorecard** from `Analytics/CONVERSION.md` —
views, profile views, follows, saves and shares, product page views, downloads, and
views-per-profile-view — because reach stopped being the constraint on 2026-07-31 and
profile conversion became it.

Then message Connor: the week's 21 titles by day, what got
scheduled where, what was dropped and why, the Phase-1 report's three headlines
(went well / didn't / changing), sprint checkpoint status (`SPRINT-AUG25.md` table),
and the creator-pipeline pulse (sent / replied / deals / posts live). **Posts start
Monday 8 AM — Sunday night is Connor's standing veto window.** Silence = go. "Pull
Tuesday's quiz" = I unschedule it.

## Partial generation (any off-schedule run)

**Rule: an off-schedule run is not a special mode. It runs the loop normally and only
generates enough content to cover the slots between now and the next Sunday run.**

Sunday regenerates the whole week from scratch, so generating more than that is waste
that would be thrown away.

1. Compute `slots_remaining` = published slots between now and **the end of Sunday**
   (not the 6:00 PM run time), at the normal 3 posts/day cadence. The Sunday run owns
   Monday through Sunday of the *following* week, so the bridge run owns everything up
   to and including Sunday night. Generating a 7:00 PM post at 6:00 PM the same evening
   is a bad seam; this avoids it.
2. Generate exactly that many posts, drawing from the active series in normal
   rotation (do not skip series just because the batch is small).
3. Everything else is unchanged: analytics first, same hard gate, same render, same
   scheduling with rate limits, same registry appends, same report.

Worked example, a run starting Saturday 02:00: slots left are Saturday (2) and Sunday
(2), so it generates **4 posts**, schedules them, and the Sunday 6:00 PM run then
produces the full Monday-to-Sunday week as usual.

The same rule applies to the DM routine: an off-schedule run produces only the current
day's batch, because Sunday's cycle reseeds the pipeline anyway.

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

**Updated 2026-08-01.** Reach is no longer the constraint: TikTok went from 0 to 1,700
views a day in two weeks. The constraint is that 4,408 views produced 1 follower and 0
profile views, so **the primary optimization target is now profile conversion** — the
one action a TikTok viewer can take that leads anywhere. `Analytics/CONVERSION.md` is
the diagnosis and the setup; the weekly report leads with its scorecard.

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

- **`UPLOAD_POST_API_KEY` missing or rejected at fire time** → full stop after Phase 3:
  everything staged + committed, nothing published, Connor told exactly what to set.
- **Canva missing** → Phases 1–2 still run (analytics + copy committed), render/schedule
  skipped, Connor told.
- **A publish call fails** → retry ×3 with backoff → mark failed in manifest, continue
  with the rest, report it.
- **No analytics data returned** (week 1, or API gap) → Phase 1 still writes the report
  saying exactly that, directives carry `"confidence": "none"`, Phase 2 runs the default
  slot template. The gate is that Phase 1 *ran*, not that data existed.
