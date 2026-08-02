# Content-Engine — the intelligence behind BiteBuddy's posts

*Added 2026-07-25. This folder is the "brain" for bulk content generation: who we're
talking to, which hooks work, what the output looks like, and the prompt that ties it
all together.*

## The pieces

| File | What it is |
|---|---|
| `MASTER-PROMPT-V5.md` | The 50-post CSV generation prompt (v5, persona-targeted). Paste into a web-browsing model → get a verified, bulk-creation-ready CSV. Supersedes the v4 prompt. |
| `CAROUSEL-CONVERSION-SPEC.md` | **What a deck has to do**: the 9 slide roles, the CTA ladder, the 2026 benchmarks we measure ourselves against, and the asset-autonomy rule. Governs when it and the design system disagree. |
| `DESIGN-SYSTEM.md` | The graphics layer: brand tokens, 8 slide archetypes, and the two render routes — Canva Bulk Create (CSV → template merge) and Claude-designed slides. |
| `render_slides.py` | The actual batch renderer. Manifest in, 1080×1350 PNGs out. Poses and layout variant derived per post, nothing hand-mapped. |
| `harvest_frames.py` | Pulls real app stills out of screen recordings into `UI-Library/Recordings/stills/`, which is why the carousel track never needs a screenshot from Connor. |
| `build_demo.py` | Cuts a raw recording into a 1080×1920 demo post (the video track, driven by the demo-drop skill). |
| `../Research/TARGET-USER-PROFILES.md` | The 8 personas (+1 anti-persona) every post targets. The `Audience` column comes from here. |
| `../Research/HOOK-INTELLIGENCE-2026.md` | The researched hook library, carousel mechanics, cadence limits, and anti-patterns. The `Hook_Family` vocabulary comes from here. |

## The flow

```
TARGET-USER-PROFILES + HOOK-INTELLIGENCE     (research: updated occasionally)
                 │
                 ▼
   Analytics/next-week-directives.json        (hard gate: written this run,
                 │                              or generation refuses to start)
                 ▼
   weekly-loop Phase 2 generates the week
   shape from CAROUSEL-CONVERSION-SPEC        (9 roles, CTA ladder, dedupe
                 │                              against registry.jsonl)
                 ▼
   render_slides.py  ──►  Posts/<week>/<id>/NN.png
   images from UI-Library/** and Recordings/stills/
   (harvest_frames.py refills those from clips; never ask for a screenshot)
                 │
                 ▼
   push, then schedule via Upload-Post at the commit SHA
   (TikTok ≤3/day · Instagram ≤2/day, spaced — see HOOK-INTELLIGENCE §cadence)
                 │
                 ▼
   Phase 1 of the next run appends real numbers to Analytics/performance-log.jsonl
                 │
                 └────► next week's directives
```

## Which route actually runs

**`render_slides.py` is the batch render path, not Canva.** Learned 2026-07-25: Canva's
`generate-design` emits one page per call so it cannot build a carousel, and this
environment cannot download Canva exports. Canva stays useful for one-off polish and for
Connor editing a deck by hand. The Route A / Route B framing in `DESIGN-SYSTEM.md` still
describes the visual language correctly; just read the renderer as the thing that ships.

The weekly-loop skill drives all of it. It *reads* these docs rather than duplicating
them, which is the only way they stay true.

## The standing caveat

`Analytics/performance-log.jsonl` now has real lines in it, but they cover a handful of
posts across a stretch where TikTok reach collapsed after the 22 July cadence incident
and Instagram has been spam-restricted since. So: the numbers exist, and they are not yet
enough to validate anything in this folder. Everything here remains research-informed
hypothesis until several clean weeks land. The benchmarks in
`CAROUSEL-CONVERSION-SPEC.md` §1 are somebody else's numbers and are there to be measured
against, not to be assumed.
