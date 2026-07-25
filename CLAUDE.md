# CLAUDE.md — BiteBuddy marketing

Loaded automatically at session start in this repo. Last verified: 2026-07-25.

## What this repo is

Everything that gets BiteBuddy in front of people. **Cleared and restarted on
2026-07-25** — see `README.md` for what was removed and why.

**The app is live on the App Store and has effectively zero users.** Distribution is the
bottleneck. Content that does not plausibly drive installs is not worth producing.

## Current state: strategy exists, pipeline does not

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

What's **not** here: any production pipeline, any publishing automation, any skills, any
analytics. Building that is the next job, and it should be designed around what Claude
can actually do in-session now (design directly in Canva, schedule via connector) rather
than around manual handoffs.

## Two rules learned the hard way

**1. Measurement is not a later phase.** The previous system shipped a complete analytics
pipeline — log, scoring script, leaderboard, directives — and the log stayed 0 bytes
forever. Ten posts went live and nothing was ever recorded. Do not build a content
pipeline whose feedback loop is "we'll wire it up after." The first post should produce a
recorded number, even a hand-copied one.

**2. Don't build around a connector that isn't connected.** The old workflow assumed
Upload-Post throughout and it was never wired up, so the whole thing ran in permanent
dry-run. Check what's actually in the session before designing around it.

## Known blockers

1. **Upload-Post is not connected** — nothing can publish until Connor adds it in
   claude.ai connector settings, links IG/TikTok/Facebook/YouTube, and passes the free
   tier (10 uploads/month; a real week is ~84).
2. ~~Buddy pose PNGs~~ **RESOLVED 2026-07-25** — all 13 canonical poses are now in
   `Brand-Assets/buddy-poses/`, with RGBA cutouts in `transparent/` ready to composite.
   Use them; never generate Buddy with an image model.
3. **No Canva brand templates** — the brand kit exists, templates do not.

## Approval gates

Anything published to a social account is **Connor's call, every time.** Draft, show,
then post — never post directly. Same for anything that spends money or changes App
Store copy.

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
