# CLAUDE.md — BiteBuddy marketing

Loaded automatically at session start in this repo. Last verified: 2026-07-25.

## What this repo is

Everything that gets BiteBuddy in front of people. **Cleared and restarted on
2026-07-25** — see `README.md` for what was removed and why.

**The app is live on the App Store and has effectively zero users.** Distribution is the
bottleneck. Content that does not plausibly drive installs is not worth producing.

## Current state: strategy + autonomous weekly loop, awaiting activation

The operating system is the **weekly loop** — one Sunday Routine that closes last
week (analytics) and opens next week (generate → render in Canva → schedule via
Upload-Post), with a hard gate: generation refuses to run unless this run's analytics
directives were just written. Contract: `WEEKLY-LOOP.md`. Procedure:
`.claude/skills/weekly-loop/SKILL.md`. Series testing: `Content-Engine/SERIES.md`.
Schemas + the append-only performance log: `Analytics/README.md`. Dedupe memory:
`Content-Engine/registry.jsonl`.

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

1. **Upload-Post connector** — Connor adds it in claude.ai connector settings, links
   IG (Business/Creator + FB Page) / TikTok / Facebook / YouTube, paid plan (free tier
   is 10 uploads/mo; a week is ~40+).
2. **The Sunday Routine** — Connor creates it in the claude.ai Routines UI with
   **Upload-Post + Canva attached** (must be created there so connectors attach).
   Spec + prompt text: `WEEKLY-LOOP.md`.
3. **Canva templates** — not yet built; until they exist the render phase builds each
   deck from the archetype specs directly.
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
- **Platform-safe cadence** — TikTok ≤3/day, Instagram ≤2/day, always spaced, never
  simultaneous. Five simultaneous posts on 22 July 2026 is the suspected cause of an
  Instagram throttle. Rate limiting belongs in whatever publishes.

## Conventions

- Branch as `claude/<short-description>`. Never commit to `main`.
- This repo holds binaries. Do not add build tooling or app code to it.
- Keep rendered assets alongside the copy/prompts that produced them.
