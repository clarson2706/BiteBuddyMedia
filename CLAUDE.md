# CLAUDE.md — BiteBuddy marketing

Loaded automatically at session start in this repo. Last verified: 2026-08-01.

> **Read `START-HERE.md` first.** It is the current-state file, loaded by the
> SessionStart hook in `.claude/settings.json`, and it outranks this file wherever the
> two disagree. This file is the standing policy; START-HERE is what is true today.
> Before generating, rendering, scheduling or publishing anything, run
> `python3 Content-Engine/preflight.py` and obey it.

## What this repo is

Everything that gets BiteBuddy in front of people. **Cleared and restarted on
2026-07-25** — see `README.md` for what was removed and why.

**The app is live on the App Store and has effectively zero users.** Distribution is the
bottleneck. Content that does not plausibly drive installs is not worth producing.

## Current state: strategy + autonomous weekly loop, awaiting activation

The operating system is the **weekly loop**, now twice weekly for the Aug-25 sprint
(`SPRINT-AUG25.md`): Sunday full run (analytics → generate → render in Canva →
schedule via Upload-Post → outreach batches → report) + Wednesday mini-run (snapshot,
kill/re-cut, Thu/Fri batches, pulse). Hard gate: generation refuses to run unless
this run's analytics directives were just written. Contract: `WEEKLY-LOOP.md`.
Procedure: `.claude/skills/weekly-loop/SKILL.md`. Series: `Content-Engine/SERIES.md`.
Analytics schemas: `Analytics/README.md`. Dedupe: `Content-Engine/registry.jsonl`.
Gate before any phase: `Content-Engine/preflight.py`. Guardrails in code:
`Content-Engine/copy_lint.py`. Standing list of what is broken: `SYSTEM-AUDIT.md`.
On-demand performance read (read-only, any time): the **media-report** skill +
`Analytics/report.py`. Video track: Connor drops app screen recordings in
`UI-Library/Recordings/_INBOX/`, the **demo-drop** skill edits and schedules them
(one per platform per day, as many days as there are clips); the editing standard
is `Content-Engine/DEMO-EDIT-SPEC.md`.
Creator engine ($0 upfront, 30% of first payment): `Outreach/DM-PLAYBOOK.md` +
`Outreach/CREATOR-TERMS.md`. House rule: **no em dashes in any outbound copy**
(DMs, captions, slides, briefs) — AI tell, trust risk.

## The strategy layer

What's here is the **content intelligence layer** — who we're targeting, which hooks
work, what slides should look like, and the prompt that generates batches:

- `Research/TARGET-USER-PROFILES.md` — 8 personas + 1 anti-persona. Every post names one.
- `Research/HOOK-INTELLIGENCE-2026.md` — hook library, carousel mechanics, per-platform
  cadence limits, 2026 anti-patterns.
- `Content-Engine/MASTER-PROMPT-V5.md` — the 50-post CSV generation prompt.
- `Content-Engine/DESIGN-SYSTEM.md` — brand tokens, 8 slide archetypes, render routes.
- `UI-Library/` — 19 real app screenshots.

**Read all four docs before proposing or building anything.** They are recent, sourced,
and deliberate.

## Two rules learned the hard way

**1. Measurement is not a later phase.** The previous system shipped a complete analytics
pipeline — log, scoring script, leaderboard, directives — and the log stayed 0 bytes
forever. Ten posts went live and nothing was ever recorded. Do not build a content
pipeline whose feedback loop is "we'll wire it up after." The first post should produce a
recorded number, even a hand-copied one.

**2. Don't build around a connector that isn't connected.** The old workflow assumed
Upload-Post throughout and it was never wired up, so the whole thing ran in permanent
dry-run. Check what's actually in the session before designing around it.

## Activation checklist (what still blocks the first live week)

1. ~~`UPLOAD_POST_API_KEY` env var~~ **SET 2026-07-25.** Publishing uses the Upload-Post
   REST API with this key, which remains the right transport for Routines. **Corrected
   2026-08-01:** an Upload-Post *MCP tool set* is also available in-session, so the old
   flat claim that "Upload-Post is not a connector and cannot be attached" is no longer
   true. Plan **verified: Basic (paid)**. See `Content-Engine/UPLOAD-POST.md`.
   **Link state verified live 2026-08-01:** TikTok and YouTube linked and healthy.
   **Instagram is DISCONNECTED, not banned** — `list_users` returns `instagram: ""`,
   an empty string, which is a dropped token that a reconnect in the Upload-Post
   dashboard fixes. The earlier "spam-restricted, only Connor can clear it" reading was
   investigated on 2026-07-29 and does not survive: the post published, Upload-Post
   recorded a failure it should not have, and the token then dropped. Facebook has
   never been linked.
2. ~~The Routines~~ **PARTIAL as of 2026-07-30** — Sunday full loop and Wednesday mini
   are enabled (Canva attached to both). The **daily 8 AM creator DM batch is PAUSED**
   (last fired 2026-07-25, nothing scheduled). If that pause wasn't deliberate, Connor
   re-enables it in the claude.ai Routines UI.
3. ~~**Canva templates**~~ **NOT THE RENDER PATH, resolved 2026-08-01.** Canva cannot
   build a multi-page carousel in one call and this environment cannot download Canva
   exports, so `Content-Engine/render_slides.py` is the render path and Canva is for
   one-off polish. The renderer emits **1080x1920 for TikTok (primary)** and 1080x1350
   for Instagram, with six real slide layouts. Reference decks: `Posts/_TEMPLATES/`.
4. **The conversion layer** — the tracked bio link, the pinned conversion post and the
   first `installs.jsonl` line are still Connor's ~15 minutes, and they are what stands
   between real reach and a measurable install. See `Analytics/CONVERSION.md`.
4. ~~Buddy poses~~ **RESOLVED 2026-07-25** — 13 canonical renders + RGBA cutouts in
   `Brand-Assets/buddy-poses/`. Use them; never generate Buddy with an image model.

## Approval gates

**Updated 2026-07-25 by Connor:** the weekly loop is authorized to schedule and publish
its carousel posts **without per-post approval**. The Sunday-night report is a standing
veto window (posts start Monday 8 AM; silence = go; Connor can name any post to pull).
This authorization covers ONLY the weekly loop's carousels on the linked accounts.

Everything else keeps the strict gate: anything that spends money, changes App Store
copy, DMs/outreach to real people, or publishes outside the weekly loop is **Connor's
call, every time** — draft, show, then act.

App Store listing copy lives in `BiteBuddyMVP/APP_STORE_METADATA.md`, including the
canonical search term every CTA must use. Do not restate it here — point at it.

## Content guardrails (non-negotiable, survive any pipeline rebuild)

- **No medical or outcome claims.** Never "lose X lbs," "guaranteed," "burns fat," or
  crash-diet / disordered-eating framing. Calorie *facts* are fine; health
  *prescriptions* are not.
- **Never feature the Meal Advisor** — it ships as "Coming Soon" / disabled.
- **Real screenshots only** for app slides, from `UI-Library/`. Never redraw, mock, or
  invent UI or numbers.
- **App numbers are AI estimates the user reviews** — keep that honesty visible. Never
  claim scan precision; claim consistency (see the anti-persona in
  `TARGET-USER-PROFILES.md`).
- **Buddy stays visually consistent** and does not appear on every slide — he hosts the
  cover and the CTA, the content carries the body.
- **Every carousel ends with the App Store CTA and the follow ask.** The last slide
  shows the real Today dashboard in a phone, "Download BiteBuddy, free on the App
  Store", the search line, and "Follow @bitebuddyapp for more". This is enforced by
  `render_slides.slide_cta()`, not left to per-post judgement. The follow ask exists
  because the profile tap is the only action a TikTok viewer can actually take, and
  4,408 views have so far produced one follower. See `Analytics/CONVERSION.md`.
- **Platform-safe cadence** — TikTok **3/day (08:00 / 13:00 / 19:00), which is the
  default and also the ceiling**; Instagram ≤2/day; always spaced, never simultaneous.
  Five simultaneous posts on 22 July 2026 is the suspected cause of an Instagram
  throttle. Rate limiting belongs in whatever publishes. The 13:00 TikTok slot is the
  **flex slot**: a demo video *replaces* the carousel there rather than adding a fourth
  post, and the flex-slot post is TikTok-only so Instagram stays at 2.

## Conventions

- Branch as `claude/<short-description>`. Never commit to `main`.
- **A branch is not done until it is merged.** Content memory that lives only on a
  branch does not exist: the registry cannot dedupe against it and analytics cannot
  join to it. Three branches were stranded this way between 07-25 and 07-30, carrying a
  full week of posts. `preflight.py` now fails the run while that is true.
- This repo holds binaries. Do not add build tooling or app code to it.
- Keep rendered assets alongside the copy/prompts that produced them.
