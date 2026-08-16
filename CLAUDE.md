# CLAUDE.md — BiteBuddy marketing

Loaded automatically at session start in this repo.

## What this repo is

Everything that gets BiteBuddy in front of people.

**The app is live on the App Store and has effectively zero users. Distribution is the
bottleneck.** Content that does not plausibly drive installs is not worth producing.

## Current state: cleared to assets, awaiting a new content strategy

**Reset on 2026-08-16.** The previous strategy layer — the weekly loop, the content
engine, the persona and hook research, the creator outreach engine, the analytics
pipeline, and every rendered post — was removed so a completely new content strategy
could be designed from scratch.

None of it is lost. The full pre-reset repo is preserved on the branch
`claude/bitebuddy-media-backup-p3jgng` and in `main`'s own git history. See `README.md`
for what was removed and how to get any of it back.

What is left is deliberately just the raw material:

- `Brand-Assets/buddy-poses/` — 13 canonical Buddy renders + RGBA cutouts
- `Brand-Assets/fonts/` — Baloo2, Inter
- `UI-Library/` — 19 real app screenshots, organized by app area, plus recording inboxes

There is currently **no** content pipeline, no generation prompt, no design system, no
scheduler wiring, and no analytics. A new strategy defines those.

## Content guardrails (non-negotiable, survive any pipeline rebuild)

These outlive every strategy. They are brand and legal safety, not tactics.

- **No medical or outcome claims.** Never "lose X lbs," "guaranteed," "burns fat," or
  crash-diet / disordered-eating framing. Calorie *facts* are fine; health
  *prescriptions* are not.
- **Never feature the Meal Advisor** — it ships as "Coming Soon" / disabled.
- **Real screenshots only** for app slides, from `UI-Library/`. Never redraw, mock, or
  invent UI or numbers.
- **App numbers are AI estimates the user reviews** — keep that honesty visible. Never
  claim scan precision; claim consistency.
- **Buddy stays visually consistent** and does not appear on every slide — he hosts the
  cover and the CTA, the content carries the body. Use the canonical poses in
  `Brand-Assets/buddy-poses/`; never generate Buddy with an image model.
- **No em dashes in any outbound copy** (DMs, captions, slides, briefs) — AI tell,
  trust risk.
- **Platform-safe cadence** — never publish simultaneously across platforms. Five
  simultaneous posts on 22 July 2026 is the suspected cause of an Instagram throttle.
  Whatever publishes must enforce spacing and rate limits. Any new cadence ceiling is
  the new strategy's call, but "always spaced, never simultaneous" is not negotiable.

## Approval gates

**The blanket publish authorization is void as of the 2026-08-16 reset.** It covered the
old weekly loop's carousels specifically, and that loop no longer exists.

Until a new strategy is designed and Connor explicitly authorizes it, the strict gate
applies to everything: anything that spends money, changes App Store copy, DMs or reaches
out to real people, or publishes to any account is **Connor's call, every time** — draft,
show, then act.

## Known account and tooling state (carried over, unverified since the reset)

- `UPLOAD_POST_API_KEY` is set. Upload-Post is not a claude.ai connector; publishing uses
  its REST API with that key. The account was on the Basic (paid) plan as of 2026-07-30.
- **Instagram was spam-restricted from 2026-07-22.** Every IG publish after that failed
  ("action suspected as spam / log in to Instagram directly to resolve"). TikTok and
  YouTube published fine. Only Connor can clear it by logging into Instagram directly.
  **Re-check this before designing anything that depends on Instagram.**
- The Sunday and Wednesday Routines pointed at the deleted weekly-loop skill. They must
  be disabled in the claude.ai Routines UI.

Treat all of the above as stale until re-verified.

## App Store listing

Listing copy lives in `BiteBuddyMVP/APP_STORE_METADATA.md`, including the canonical
search term every CTA must use. Do not restate it here — point at it.

## Conventions

- Branch as `claude/<short-description>`. Never commit to `main`.
- This repo holds binaries. Do not add build tooling or app code to it.
- Keep rendered assets alongside the copy/prompts that produced them.
