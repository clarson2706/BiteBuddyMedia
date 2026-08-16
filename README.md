# BiteBuddy Marketing

Everything that gets BiteBuddy in front of people.

**North star: downloads.** The app is live and has effectively no users, so distribution
is the whole problem. App Store listing:
https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752

---

## Status: cleared to assets, 2026-08-16

This repo was reset down to its raw material so a **completely new content strategy**
can be designed from scratch. The previous system was not broken so much as superseded —
it is preserved intact and can be consulted or restored at any time.

### What is here now

```
Brand-Assets/
  buddy-poses/source/        13 canonical Buddy renders
  buddy-poses/transparent/   the same 13, background removed (RGBA)
  fonts/                     Baloo2, Inter
  MASCOT_IMAGE_GEN_PROMPTS.md  MASTER STYLE BLOCK, only for a genuinely new pose
UI-Library/                  19 real app screenshots in 9 app-area folders,
                             plus _INBOX/ and Recordings/ capture inboxes
CLAUDE.md                    content guardrails + repo conventions
README.md                    this file
```

That is it. There is no content pipeline, no generation prompt, no design system, no
scheduler wiring, and no analytics. Building those is the next strategy's job.

## Where the old system went

**Everything is preserved on the branch `archive/pre-reset-2026-08-16`**, which
sits at commit `930c273` — the exact state of `main` immediately before this reset. It is
also in `main`'s own git history, which was not rewritten.

To read a file from the old system without restoring it:

```
git show archive/pre-reset-2026-08-16:WEEKLY-LOOP.md
git show archive/pre-reset-2026-08-16:Research/TARGET-USER-PROFILES.md
```

To restore a file or folder into a working branch:

```
git checkout archive/pre-reset-2026-08-16 -- Research/HOOK-INTELLIGENCE-2026.md
```

To browse the whole thing:

```
git checkout archive/pre-reset-2026-08-16
```

### What was removed

| Removed | What it was |
|---|---|
| `WEEKLY-LOOP.md` | The autonomous twice-weekly loop contract: Sunday full run (analytics → generate → render → schedule → outreach → report) + Wednesday mini-run |
| `.claude/skills/` | `weekly-loop`, `demo-drop`, `media-report` — the executable procedures the Routines fired |
| `SPRINT-AUG25.md` | The 31-day August push: checkpoints, levers, $0-ads rule |
| `Research/` | `TARGET-USER-PROFILES.md` (8 personas + 1 anti-persona), `HOOK-INTELLIGENCE-2026.md` (20-formula hook library, carousel mechanics, cadence limits, 2026 anti-patterns) |
| `Content-Engine/` | `MASTER-PROMPT-V5.md` (50-post CSV generation prompt), `DESIGN-SYSTEM.md` (brand tokens, 8 slide archetypes), `SERIES.md`, `DEMO-EDIT-SPEC.md`, `UPLOAD-POST.md`, the render/build scripts, and `registry.jsonl` (the dedupe registry) |
| `Outreach/` | Creator engine: `DM-PLAYBOOK.md`, `CREATOR-TERMS.md` ($0 upfront / 30% of first payment), creator pipeline + payout ledgers, the 2026-07-25 DM batch |
| `Analytics/` | Performance log, ingest + report scripts, the 2026-W30 baseline, the TikTok export reconciliation, and next-week directives |
| `Posts/` | Every rendered slide and Short from weeks W30 and W30-flex, plus the demos |

**If you ever need to know which topics already went live**, that is in
`Posts/2026-W30/manifest.json` and `Posts/2026-W30-flex/manifest.json` on the archive
branch. Check it before a new strategy re-cuts a topic that already ran.

## Two lessons the removed system paid for

Carried forward deliberately. Whatever gets built next should not re-learn these.

**1. Measurement is not a later phase.** The system before last shipped a complete
analytics pipeline — log, scoring script, leaderboard, directives — and the log stayed
**0 bytes** forever. Ten posts went live across three platforms and not one view,
impression, or click was ever recorded. Every "optimization" it could do was reading from
an empty file. The first post of any new pipeline should produce a recorded number, even
a hand-copied one.

**2. Don't build around a connector that isn't connected.** An earlier workflow assumed
Upload-Post throughout and it was never wired up, so the whole thing ran in permanent
dry-run. Check what is actually in the session before designing around it.

## Before the new strategy goes live

- **Disable the Sunday and Wednesday Routines** in the claude.ai Routines UI. They fire
  the deleted `weekly-loop` skill.
- **Re-check the Instagram spam restriction.** Every IG publish since 2026-07-22 failed;
  only Connor can clear it by logging into Instagram directly.
- **Re-verify Upload-Post** account linkage and plan headroom before assuming anything
  can publish.

## Repo map

| Repo | Holds |
|---|---|
| `BiteBuddyMVP` | iOS app, backend, canonical legal, product docs, App Store metadata |
| **`bitebuddymedia`** | **this repo — marketing strategy, content, assets** |
| `bitebuddy-admin` | ops dashboard over production Supabase |
| `bitebuddy-legal` | published legal mirror. Auto-generated — never edit by hand |
