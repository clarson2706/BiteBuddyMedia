---
name: weekly-loop
description: >-
  Run BiteBuddy's autonomous weekly content cycle end to end: pull last week's
  real per-post metrics from Upload-Post into Analytics/, write the weekly
  report + next-week directives, generate 14 persona-targeted posts steered by
  those directives, render every deck in Canva from the design system + real
  Buddy/screenshot assets, schedule the full week across TikTok / Instagram /
  Facebook / YouTube via Upload-Post with rate limits enforced, commit
  everything, and send Connor the weekly report. Two modes: full Sunday loop,
  and Wednesday mini mode (snapshot Mon/Tue numbers, kill losers, re-cut the
  early winner into fresh covers, Thu/Fri outreach batches, midweek pulse).
  Both modes write personalized creator-DM batches and process the creator
  pipeline per Outreach/DM-PLAYBOOK.md. Use whenever the task is to run, stage,
  or publish a week of BiteBuddy content, when either Routine fires, or on "run
  the weekly loop". Analytics ALWAYS run first — generation must refuse to
  start if this run's directives file was not just written.
---

# weekly-loop — the whole week in one run

Read `WEEKLY-LOOP.md` first — it is the contract; this file is the procedure.
Then read, in order: `Analytics/README.md` (schemas), `Content-Engine/SERIES.md`,
`Research/TARGET-USER-PROFILES.md`, `Research/HOOK-INTELLIGENCE-2026.md`,
`Content-Engine/MASTER-PROMPT-V5.md` (sections 4–9 are the copy rules; the CSV
contract does not apply here), `Content-Engine/DESIGN-SYSTEM.md`,
`Outreach/DM-PLAYBOOK.md`, and `SPRINT-AUG25.md` while the sprint is live.

Work on a `claude/week-<ISO-week>` branch. Never commit to `main`.

**Mode check first.**
- "Wednesday mini mode" → run only: Phase 1 steps 1–2 (snapshot, no full report),
  the kill/re-cut pass from `WEEKLY-LOOP.md` §Wednesday, Phase 5 step 2 (process
  creator replies), and a two-line pulse to Connor.
- **Any off-schedule run** (someone says "run the loop" on a Tuesday, a Saturday,
  whenever) → run the full Sunday procedure below UNCHANGED, except Phase 2
  generates only `slots_remaining` posts: the published slots between now and the
  next Sunday 6:00 PM America/Chicago at 2 posts/day. Sunday regenerates the whole
  week anyway, so anything beyond that is waste. See `WEEKLY-LOOP.md` §Partial
  generation for the worked example.
- Otherwise → the full Sunday mode below.

## Phase 1 — Analytics (never skip; never reorder)

1. Load the Upload-Post tools (ToolSearch). If absent → note it, still do steps 3–5
   from whatever exists in the log, mark `"confidence": "none"`.
2. For every post in `Content-Engine/registry.jsonl` posted in the last 14 days, fetch
   per-platform metrics. Append one JSONL snapshot per post×platform to
   `Analytics/performance-log.jsonl` (schema in `Analytics/README.md`). Never
   overwrite prior lines — the log is append-only history.
3. Read `Analytics/installs.jsonl` if present; join weekly install counts to the week's
   engagement for the report's honesty check ("reach without installs is not winning").
4. Write `Analytics/<ISO-week>-report.md`:
   - **What went well** — top 3 posts with the *why* (series? hook family? persona?
     recipe? slot?), stated against the metric ladder (saves/shares/comments-intent
     before views).
   - **What didn't** — bottom posts and any series slot underperforming its cost;
     distinguish "weak content" from "weak distribution" where the data allows.
   - **What changes next week** — 3–7 concrete directives, each traceable to a number
     in this report. No vibes.
   - Tables: per-series, per-hook-family, per-persona, per-recipe, per-slot.
5. Write `Analytics/next-week-directives.json` (schema in `Analytics/README.md`) with
   `generated_at` = now. Commit Phase 1 before starting Phase 2.

## Phase 2 — Generate 14 posts

**Gate:** `next-week-directives.json` must carry this run's `generated_at`. If not,
stop and fix Phase 1. Do not generate from memory of old numbers.

1. Slot template for a full week (directives may shift ±2 slots between categories,
   nothing else): 8 series (2 × 3 active series from `SERIES.md`, +2 to the series
   the directives favor) · 2 winner re-cuts (only if directives name winners) ·
   4 experiments. **On a partial run, generate only `slots_remaining` posts**, keeping
   the series rotation proportional (a 3-post batch is series-heavy, not experiment-heavy).
2. Every post gets: persona (P1–P8), hook family (the 20 codes), visual recipe (the 8
   archetypes), series or `oneoff`, slide-by-slide copy (hook → value slides → CTA),
   caption with one natural search keyword, pinned first comment, 3–5 hashtags,
   platform plan + time slot. Copy rules = MASTER-PROMPT-V5 §4–9; guardrails =
   `CLAUDE.md` (no medical/outcome claims, no Meal Advisor, no precision claims,
   food-positive always).
3. Freshness: check `registry.jsonl` — no topic repeat within 90 days, no chain+angle
   repeat within 14, no hook ever reused verbatim. CTA mix per week: ~5 follow,
   ~3 comment, ~3 save/share, ~3 app (exact App Store line only on app CTAs:
   `Search 'BiteBuddy: Ai calorie scanner'`).
4. Factual posts: verify numbers against primary sources during the run; a claim that
   can't be verified gets replaced, not published. Record source URLs in the manifest.
5. Write `Posts/<week>/manifest.json` (one object per post: id, slot, series, persona,
   hook_family, recipe, slides[], caption, pinned_comment, hashtags, platforms,
   status, sources); append every post to `registry.jsonl`.

## Phase 3 — Render in Canva

0. Start from the series templates in `Content-Engine/TEMPLATES.md` when one exists
   for the post's series/recipe (duplicate, swap copy and photos). Note the
   render-phase constraint in that file: hand Canva export URLs directly to
   Upload-Post (this environment cannot download export files locally); store
   design IDs + links in the manifest instead of PNGs.
1. Load the Canva tools. For each post, build the deck per its recipe in
   `DESIGN-SYSTEM.md`: brand palette, one locked headline font, Buddy **only** from
   `Brand-Assets/buddy-poses/transparent/` (pick the pose matching the emotional beat —
   table in `Brand-Assets/buddy-poses/README.md`), app UI **only** real screenshots
   from `UI-Library/`. Real/stock food photography, never AI-rendered food.
2. Export each deck as 1080×1350 PNGs → `Posts/<week>/<post-id>/01.png…`. Keep the
   Canva design links in the manifest so Connor can tweak any deck by hand.
3. Render failure after 2 attempts → drop the post (status `render-failed`), continue.
   13 good posts beat 14 with one broken deck.

## Phase 4 — Schedule via Upload-Post

1. Preflight: account/token, plan headroom, linked platforms. Unlinked → skip that
   platform everywhere + report. No connector → stop here; everything stays committed
   as `staged`; tell Connor precisely what to connect.
2. Rate rules enforced in your scheduling math (never trust the slot plan blindly):
   TikTok ≤3/day · IG ≤2/day · ≥4h between same-platform posts · no simultaneous
   cross-platform publishes of the same deck · captions and crops varied per platform.
3. Slots (America/Chicago): TikTok 08:00 + 19:00 · IG 12:30 (+19:30 Fri) · FB mirrors
   IG +15 min · YouTube Short 17:00 daily (build 30–40s slideshow from the deck; title
   = the hook, keyworded-human).
4. Append the App Store link in YouTube descriptions + Facebook captions (they allow
   links); IG/TikTok captions carry the search phrase instead.
5. Write scheduled IDs/URLs + `status: scheduled` into the manifest. Failed publish →
   3 retries w/ backoff → `status: failed`, continue, report.

## Phase 5 — Outreach (per `Outreach/DM-PLAYBOOK.md`, all hard rules apply)

1. Daily DM batches belong to **Routine 3** (daily 8 AM, Sonnet 5), not to loop runs.
   Here, only verify recent batches exist in `Outreach/batches/` and flag a gap in
   the report if they do not.
2. Process whatever Connor forwarded: advance `creators.jsonl` statuses, draft
   stage-appropriate replies from the playbook, generate onboarding packs (unique
   `ct=` link + code + brief) for new "I agree" deals, grant free-Pro entitlements
   via RevenueCat (`grant-customer-entitlement`).
3. Run closest to month end: compute payouts (30% of attributed first payments, $10
   minimum, roll-forward), append `payouts.jsonl`, draft the payout DMs with the
   math shown.

## Phase 6 — Commit, push, report

1. Commit all of it (analytics, posts, manifest, registry, outreach), push the week
   branch, open a PR titled `Week <ISO-week>: posts + analytics + outreach`.
2. Message Connor: the three report headlines (went well / didn't / changing), the
   week's schedule by day, sprint checkpoint status vs `SPRINT-AUG25.md`, creator
   pipeline pulse (sent / replied / deals / posted), anything dropped/failed/
   unlinked, and the line **"Posts start Monday 8 AM — tonight is the veto window;
   name any post to pull."**

## Hard rules

- Phase order is fixed. No generation before this run's directives exist.
- Everything committed, nothing gitignored. An analytics claim that isn't a line in
  `performance-log.jsonl` doesn't exist.
- The registry is the only dedupe memory — append every post, every run.
- Publishing authority + veto window are defined in `WEEKLY-LOOP.md`; guardrails in
  `CLAUDE.md` outrank every directive and every trend.
