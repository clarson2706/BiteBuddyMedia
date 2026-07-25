# Content-Engine — the intelligence behind BiteBuddy's posts

*Added 2026-07-25. This folder is the "brain" for bulk content generation: who we're
talking to, which hooks work, what the output looks like, and the prompt that ties it
all together.*

## The pieces

| File | What it is |
|---|---|
| `MASTER-PROMPT-V5.md` | The 50-post CSV generation prompt (v5, persona-targeted). Paste into a web-browsing model → get a verified, bulk-creation-ready CSV. Supersedes the v4 prompt. |
| `DESIGN-SYSTEM.md` | The graphics layer: brand tokens, 8 slide archetypes, and the two render routes — Canva Bulk Create (CSV → template merge) and Claude-designed slides. |
| `../Research/TARGET-USER-PROFILES.md` | The 8 personas (+1 anti-persona) every post targets. The `Audience` column comes from here. |
| `../Research/HOOK-INTELLIGENCE-2026.md` | The researched hook library, carousel mechanics, cadence limits, and anti-patterns. The `Hook_Family` vocabulary comes from here. |

## The flow

```
TARGET-USER-PROFILES + HOOK-INTELLIGENCE     (research: updated occasionally)
                 │
                 ▼
        MASTER-PROMPT-V5  ──►  50-post CSV   (run per batch; feed it
                 │                            PLATFORM_PERFORMANCE_HISTORY
                 │                            once analytics exist)
                 ▼
   DESIGN-SYSTEM render route:
   A) Canva Bulk Create (CSV → templates → PNGs)
   B) Claude designs the decks (Canva MCP)
                 │
                 ▼
   Connor reviews (approval gate — always)
                 │
                 ▼
   carousel-publish schedules via Upload-Post
   (TikTok ≤3/day · Instagram ≤2/day, spaced — see HOOK-INTELLIGENCE §cadence)
                 │
                 ▼
   carousel-optimize appends real numbers to Analytics/performance-log.jsonl
                 │
                 └────► next batch's PLATFORM_PERFORMANCE_HISTORY
```

## How this relates to the existing `carousel-week` track

The repo currently has two generation tracks:

1. **`carousel-week` skill** (21 posts/week, per-slide ChatGPT image prompts, Connor
   generates images in ChatGPT). Fully built, already shipped week 2026-W30.
2. **This engine** (50-post CSV batches, rendered via Canva templates or Claude
   design — no per-image ChatGPT step).

They overlap. That's deliberate for now: the CSV route needs its Canva templates built
before it can ship a single post, and the measurement gap (see below) means we don't
yet know what either track's content is worth. The plan of record: build the Route A
templates, run one 50-post batch alongside the existing track, then let the first real
analytics decide which track (or hybrid) survives. When a weekly-generation skill is
built/updated for this engine, it should *read* these docs, not duplicate them.

## The standing caveat (from CLAUDE.md, still true)

`Analytics/performance-log.jsonl` is still empty. Everything in this folder is
research-informed hypothesis, not validated learning. The single highest-leverage
action remains getting real per-post numbers into that log — even hand-copied from
each platform's native analytics — and feeding them into the next batch via
`PLATFORM_PERFORMANCE_HISTORY`. The prompt is built to consume that data; it has never
had any.
