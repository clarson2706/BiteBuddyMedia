---
name: carousel-publish
description: >-
  Publish a staged week of BiteBuddy carousels — the Sunday-night + Mon–Sun
  publishing half of AUTOMATION-WORKFLOW.md. Runs the readiness check
  across the delivered images, assembles each post's YouTube slideshow Short,
  and schedules every READY post to Instagram, TikTok, Facebook, and YouTube via
  the Upload-Post MCP connector at its locked time slot. Use this whenever the
  task is to verify, schedule, or publish a week of BiteBuddy posts, when Connor
  says "images are in", or when the Sunday-night / posting Routine fires. This is
  the counterpart to the carousel-week (generation) skill — carousel-week stages
  copy + prompts; this one verifies images and pushes posts live. It never writes
  copy and never generates images.
---

# carousel-publish — weekly BiteBuddy carousel publisher

The **publishing half** of `AUTOMATION-WORKFLOW.md`. `carousel-week`
stages the copy, prompts, and `manifest.json`; Connor drops in ChatGPT PNGs; then
**this** skill verifies the week and pushes it live. Two scripts do the
deterministic work; the schedule-to-social step is driven through the
**Upload-Post MCP connector**.

## Scope boundaries
- **Verify + assemble + schedule only.** You do NOT write copy and you do NOT
  generate images. If a post is short on images or a caption breaks a limit, you
  hold that post and report it — you never invent content to fill the gap.
- One "post" = one carousel deck → Instagram + TikTok + Facebook, plus a YouTube
  **Short** assembled from the same slides.
- If the socials aren't linked yet, you run everything up to the send and stop in
  **dry-run** (verified + Shorts built + schedule printed, nothing published).

## Prerequisites (check first, in order)
1. **Upload-Post connector enabled in this session** — the `mcp__Upload-Post__*`
   tools must be present. If they are not, tell Connor to enable Upload-Post in
   this chat's connector settings and stop (you cannot run its OAuth from here).
2. **A staged week with images** under `Posts/<ISO-week>/` — a
   `manifest.json` plus PNGs in each post's `slides/`.

## Read these first
- `AUTOMATION-WORKFLOW.md` — the readiness checklist, cadence, failure
  handling, guardrails (the source of truth).
- `references/platform-specs.md` — per-platform limits and media rules.
- `references/upload-post-mapping.md` — how manifest fields map onto the
  Upload-Post tools (and the URL-vs-upload question).

## Procedure

### 1. Readiness check (deterministic — the gate)
```bash
python3 .claude/skills/carousel-publish/scripts/readiness_check.py --write
```
Auto-detects the upcoming week (or pass `--week 2026-W30`). It classifies every
post **READY / BLOCKED / WAITING**, enforces slide counts, filenames, PNG
validity, ratios, caption/title limits, 3–5 hashtags, slot collisions, and the
**guardrails** (no medical/outcome claims, no Meal Advisor). `--write` advances
each `status` (`verified` / `images-ready` / `draft`).

- **All green** → continue to step 2.
- **Not all green** → schedule the READY posts anyway (don't hold the whole week
  for one bad post), and give Connor an exact fix list for every BLOCKED /
  WAITING post. Never edit copy or add images yourself to force a pass.

### 2. Assemble the YouTube Short for each READY post
```bash
python3 .claude/skills/carousel-publish/scripts/build_youtube_short.py --week <W> --id <id>
```
Produces `<id>/youtube-short.mp4` (1080×1920, slides padded on brand cream). If
local `ffmpeg` is missing the script prints the ffmpeg spec instead — run it via
Upload-Post's `submit_ffmpeg_job` → `get_ffmpeg_job` → `download_ffmpeg_result`
(see the mapping doc). Skip this for any post whose `platforms` omits youtube.

### 3. Preflight the connector
- `get_account_info` — token valid? note the plan and remaining quota (free tier
  = 10 uploads/mo; a full week ≈ 84 publishes needs a paid plan).
- `list_users` — read the profile's `social_accounts`; **only schedule platforms
  that are actually linked.** If none are linked → **dry-run**: stop before any
  upload, print the schedule you would submit, and report that publishing is
  blocked on account linking.

### 4. Schedule every READY post
Per `references/upload-post-mapping.md`, and **after confirming the live tool
schema**:
- Photo carousel → linked subset of {instagram, tiktok, facebook} via
  `upload_photos`, `scheduled_date` = the post's `date` + `time_local` in the
  manifest `timezone`, converted to an absolute UTC instant.
- YouTube Short → `upload_video` with the mp4, same scheduled instant.
- Caption = `caption` + the `hashtags`; title = `title` (≤100 for YouTube).
- Uploads are async: poll `get_status`/`get_job_status` until `success`, write
  the returned post ID/URL into that post's `results`, and set
  `status: scheduled` (or `posted`).

### 5. Failure handling (per AUTOMATION-WORKFLOW.md)
- A publish fails → retry with backoff; still failing → `status: failed`, log the
  error in `results`, notify Connor. Don't silently drop.
- A platform disconnected → skip that platform, post the others, flag the
  reconnect.
- Quota would be exceeded → stop, report how many posts fit, ask before trimming.

### 6. Commit + report
- Commit the updated `manifest.json` (statuses + `results`) and any built
  `youtube-short.mp4` files to the marketing branch and push (retry with backoff
  on network errors).
- Report to Connor: week label; counts (scheduled / blocked / waiting / failed);
  per-BLOCKED and per-WAITING post, the exact fix; and the live schedule (what's
  going out when, to which platforms). If dry-run, say so and name the blocker.

## Guardrails (non-negotiable)
Same as generation — enforced again here because this is the last gate before
anything goes public:
- No medical/outcome claims; calorie facts fine, health prescriptions not.
- Never feature the Meal Advisor (Coming Soon).
- Real screenshots only on app-proof slides.
- Buddy consistent. See `Legal/MEDICAL_AND_NUTRITION_DISCLAIMER.md`.

## What this skill does NOT do
Writing copy, generating/creating images, or staging the week — that's the
`carousel-week` skill. This skill starts once images exist and ends when the week
is scheduled (or held with a clear fix list).
