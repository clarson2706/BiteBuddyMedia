# BiteBuddy Marketing

Everything that gets BiteBuddy in front of people.

**North star: downloads.** The app is live and has effectively no users, so distribution
is the whole problem. App Store listing:
https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752

---

## Status: rebuilt from scratch, 2026-07-25

This repo was cleared and restarted. The previous version was designed around
constraints that no longer apply — ChatGPT generated every slide image, Connor dropped
PNGs into folders by hand, two parallel generation guides had to be kept in sync, and
publishing depended on a connector that was never actually wired up. All of that is
gone.

What survived the reset, deliberately:

```
WEEKLY-LOOP.md                the autonomous weekly system — one Sunday Routine:
                              analytics -> generate -> render (Canva) -> schedule
                              (Upload-Post) -> report. Source of truth.
.claude/skills/weekly-loop/   the executable procedure the Routine fires
Analytics/                    append-only performance log + weekly reports + directives
Research/
  TARGET-USER-PROFILES.md     8 researched personas + 1 anti-persona. Who every post is for.
  HOOK-INTELLIGENCE-2026.md   20-formula hook library, carousel mechanics, cadence
                              limits, 2026 anti-patterns. All sourced.
Content-Engine/
  MASTER-PROMPT-V5.md         the 50-post CSV generation prompt (persona-targeted)
  DESIGN-SYSTEM.md            brand tokens, 8 slide archetypes, render routes
  README.md                   how the pieces fit together
Brand-Assets/
  buddy-poses/                the 13 canonical Buddy renders + RGBA cutouts
  MASCOT_IMAGE_GEN_PROMPTS.md MASTER STYLE BLOCK, only for a genuinely new pose
UI-Library/                   19 real app screenshots + capture inboxes
```

The weekly loop turns the strategy into posts hands-off. Until its first cycles land
real numbers in `Analytics/`, everything remains research-informed hypothesis — see
"the measurement lesson" below.

## What was removed and why

| Removed | Why |
|---|---|
| `Posts/` (145 rendered slides, 10 Shorts, week scaffolding) | ChatGPT-era assets that won't be reused under a new render pipeline |
| `.claude/skills/` (carousel-week, carousel-publish, carousel-optimize) | Built around the old manual workflow; the new pipeline needs its own |
| `AUTOMATION-WORKFLOW.md` | Described a rhythm that depended on the manual image step |
| `Carousel-Ideas/`, `Video-Ideas/` | Concept templates superseded by the persona + hook system |
| `Analytics/` | Scaffolding for a log that never received a single line |
| `Research/CAROUSEL-MARKETING-PLAYBOOK.md`, `VIDEO-MARKETING-RESEARCH.md` | Superseded by `HOOK-INTELLIGENCE-2026.md` (fresher research, same ground) |

**All of it is recoverable from git history** — history was deliberately preserved. If
you ever need to know which topics already went live, they're in the deleted
`Posts/2026-W30/manifest.json`.

## The measurement lesson (do not repeat it)

The old system had a full analytics pipeline — a JSONL log, a scoring script, a
leaderboard, next-week directives — and the log was **0 bytes** the entire time it
existed. Ten posts went live across three platforms and not one view, impression, or
click was ever recorded. Every "optimization" the system could do was reading from an
empty file.

The rebuilt pipeline must capture real numbers from its very first post, even if that
means Connor pasting them in by hand. Measurement is not a later phase.

## Known blockers for the rebuild

1. **Upload-Post is not connected.** Without it, content can be staged and a schedule
   can be shown, but nothing can actually publish. Connor adds it in claude.ai
   connector settings, links Instagram (Business/Creator + FB Page), TikTok, Facebook,
   and YouTube, and moves past the free tier (10 uploads/month).
2. ~~Buddy pose PNGs~~ — **resolved 2026-07-25.** All 13 canonical poses were copied
   out of the iOS app into `Brand-Assets/buddy-poses/`, with background-removed RGBA
   cutouts in `transparent/`. Buddy no longer gets regenerated per slide.
3. **No Canva templates yet.** The brand kit exists; there are zero brand templates, so
   Bulk Create has nothing to merge into.

## Repo map

| Repo | Holds |
|---|---|
| `BiteBuddyMVP` | iOS app, backend, canonical legal, product docs, App Store metadata |
| **`bitebuddymedia`** | **this repo — marketing strategy, content, assets** |
| `bitebuddy-admin` | ops dashboard over production Supabase |
| `bitebuddy-legal` | published legal mirror. Auto-generated — never edit by hand |
