---
name: weekly-loop
description: >-
  Run BiteBuddy's autonomous weekly content cycle end to end: pull last week's
  real per-post metrics from Upload-Post into Analytics/, write the weekly
  report + next-week directives, generate 21 persona-targeted posts steered by
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
  **end of Sunday** at 3 posts/day. The Sunday run owns Mon-to-Sun of the following
  week, so the bridge owns everything through Sunday night. See `WEEKLY-LOOP.md`
  §Partial generation for the worked example.
- Otherwise → the full Sunday mode below.

## Phase 1 — Analytics (never skip; never reorder)

1. Pull metrics via the Upload-Post REST API (`Content-Engine/UPLOAD-POST.md`;
   `pip install upload-post`, key in `UPLOAD_POST_API_KEY`). If the key is absent →
   note it, still do steps 3–5 from whatever exists in the log, mark
   `"confidence": "none"`.
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

## Phase 2 — Generate 21 posts

**Gate:** `next-week-directives.json` must carry this run's `generated_at`. If not,
stop and fix Phase 1. Do not generate from memory of old numbers.

1. Slot template for a full week (directives may shift ±2 slots between categories,
   nothing else): 12 series (4 × 3 active series from `SERIES.md`, +2 to the series
   the directives favor) · 3 winner re-cuts (only if directives name winners) ·
   6 experiments. **On a partial run, generate only `slots_remaining` posts**, keeping
   the series rotation proportional (a 3-post batch is series-heavy, not experiment-heavy).
   Seven of the 21 fill the TikTok-only 13:00 flex slot; draw those from the
   experiment pool first, since a demo video displaces that slot.
2. Every post gets: persona (P1–P8), hook family (the 20 codes), visual recipe (the 8
   archetypes), series or `oneoff`, slide-by-slide copy, caption with one natural search
   keyword, pinned first comment, 3–5 hashtags, platform plan + time slot. Copy rules =
   MASTER-PROMPT-V5 §4–9; guardrails = `CLAUDE.md` (no medical/outcome claims, no Meal
   Advisor, no precision claims, food-positive always).
2a. **Deck shape is fixed by `Content-Engine/CAROUSEL-CONVERSION-SPEC.md`, not chosen
   per post.** Nine slides, each carrying an explicit `role` in the manifest:
   `HOOK · STAKE · VALUE · VALUE · VALUE · PROOF · SAVE · HONEST · CTA`. Value must land
   by slide 3. `PROOF`, `SAVE`, `HONEST` and `CTA` are never dropped; a shorter deck
   drops `VALUE-3` then `STAKE`, to a floor of 7. The CTA ladder in §3 of that spec sets
   which ask each post carries, including the cap of at most 2 `APP` CTAs in any 7
   consecutive posts.
3. Freshness: check `registry.jsonl` — no topic repeat within 90 days, no chain+angle
   repeat within 14, no hook ever reused verbatim. CTA mix per week: ~5 follow,
   ~3 comment, ~3 save/share, ~3 app (exact App Store line only on app CTAs:
   `Search 'BiteBuddy: Ai calorie scanner'`).
4. Factual posts: verify numbers against primary sources during the run; a claim that
   can't be verified gets replaced, not published. Record source URLs in the manifest.
   **Known blocker (2026-07-25):** this environment's network policy returns 403 for
   chipotle.com, chick-fil-a.com, mcdonalds.com, starbucks.com and fdc.nal.usda.gov, so
   chain and label numbers cannot be verified here. While that holds, do NOT generate
   numeric chain claims: prefer behaviour, psychology, and tracking-craft angles, and
   say plainly in the report that S1 and S2 are blocked on network access. Never guess a
   calorie or protein number to fill a slot.
5. Write `Posts/<week>/manifest.json` (one object per post: id, slot, series, persona,
   hook_family, recipe, slides[], caption, pinned_comment, hashtags, platforms,
   status, sources); append every post to `registry.jsonl`.

## Phase 3 — Render the slides

**Primary path: `python3 Content-Engine/render_slides.py Posts/<week>/manifest.json`.**
It reads the manifest and writes `Posts/<week>/<post-id>/NN.png` at 1080x1350 using the
brand palette, the Baloo 2 rounded brand font in `Brand-Assets/fonts/`, and the real
Buddy cutouts from `Brand-Assets/buddy-poses/transparent/`.

Why not Canva, despite the connector being attached (learned 2026-07-25): Canva's
`generate-design` emits **one page per call**, so it cannot build an 8-slide carousel,
and this environment cannot download Canva exports (`export-download.canva.com` is
blocked at the proxy). Canva remains useful for one-off polish and for Connor editing a
deck by hand; it is not the batch render path.

1. **Nothing to wire up per post.** Buddy poses are derived from the post's series and
   hook family by `pick_poses()`, and the layout variant (one of three, so consecutive
   posts do not look stamped) comes from the post id. Override either only when there is
   a reason: `"poses": ["buddy_thinking", "buddy_level_up"]` or `"variant": 2` on the
   post. Add a badge string for any genuinely new series in `BADGES`.
2. Run the script. Eyeball at least one deck by compositing a contact sheet before
   scheduling; never schedule slides you have not looked at.
3. **Commit and push the PNGs before scheduling.** The repo is public, so each slide is
   then served at
   `https://raw.githubusercontent.com/clarson2706/BiteBuddyMedia/<commit-sha>/Posts/<week>/<post-id>/NN.png`.
   Use the **commit SHA**, not the branch name: it is immutable, so a later push cannot
   change what a scheduled post will publish.
4. **Every carousel's last slide must show the real Today dashboard in a phone
   silhouette** (`phone_mock()` handles this automatically). Never ship a text-only
   App Store close. Verify it on every deck before scheduling.
5. A post that fails to render is dropped from the schedule and named in the report.

**Never ask Connor for a screenshot.** Asset autonomy is a rule of the system
(`CAROUSEL-CONVERSION-SPEC.md` §5): every image comes from `UI-Library/**`,
`UI-Library/Recordings/stills/`, or `Brand-Assets/buddy-poses/transparent/`. Before
rendering, check whether any recording in `UI-Library/Recordings/` holds a screen this
week's `PROOF` slides need and has not been harvested yet:

```bash
python3 Content-Engine/harvest_frames.py --input <clip> --sheet /tmp/sheet.jpg
python3 Content-Engine/harvest_frames.py --input <clip> --at 9.5:<date>-<subject>-result
```

Clips in `Recordings/_USED/` are archived, not spent: re-harvesting stills from them is
normal and costs nothing. Look at every frame before using it (privacy scrub,
`DEMO-EDIT-SPEC.md`).

**Food photography:** the design system forbids AI-generated food, and this environment
has no licensed photo source. A recording still of the real scanned plate is the
preferred substitute, since it is the plate the app actually read. Failing that,
typographic recipes (STORY-BEAT, TYPE-CARD, RANK-CARD, QUIZ-CARD) need no photography
and are the default. **A post is never delayed waiting on an asset and never solves a
missing one by generating a fake.**

## Phase 4 — Schedule via the Upload-Post REST API

Read `Content-Engine/UPLOAD-POST.md` first. There is no Upload-Post MCP connector;
use the API key in `UPLOAD_POST_API_KEY` with the official SDK.

1. Preflight with `list_users`: key valid, plan headroom, which `social_accounts` are
   non-null. Unlinked → skip that platform everywhere + report. No key → stop here;
   everything stays committed as `staged`; tell Connor to set the env var.
2. Rate rules enforced in your scheduling math (never trust the slot plan blindly):
   TikTok ≤3/day · IG ≤2/day · ≥4h between same-platform posts · no simultaneous
   cross-platform publishes of the same deck · captions and crops varied per platform.
3. Slots (America/Chicago): TikTok 08:00 + **13:00** + 19:00 · IG 12:30 (+19:30 Fri) ·
   FB mirrors IG +15 min · YouTube Short 17:00 daily (build 30–40s slideshow from the
   deck; title = the hook, keyworded-human).
   **13:00 TikTok is the flex slot**: carousel by default, demo video when one is
   queued that day (it replaces the carousel, never adds a 4th). The flex-slot post is
   **TikTok-only** — IG stays at 2/day, do not fan it out there.
4. Append the App Store link in YouTube descriptions + Facebook captions (they allow
   links); IG/TikTok captions carry the search phrase instead.
   **The caption kwarg for `upload_photos` is `description`, not `caption`.** Passing
   `caption` is silently dropped and the post goes out with only its title. Verify
   `post_caption` is non-empty after publishing, every time.
   **TikTok pinned comments cannot be posted by the API.** `first_comment` is a no-op
   there, so list them for Connor to paste by hand and never report them as posted.
   Both traps are documented in `Content-Engine/UPLOAD-POST.md`.
5. Submit the full week in this run via `scheduled_date` + `timezone`, passing the
   pinned comment as `first_comment` and Canva export URLs as the media (never
   downloaded locally). Write returned `job_id`s/URLs + `status: scheduled` into the
   manifest. Failed publish → 3 retries w/ backoff → `status: failed`, continue,
   report.

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
