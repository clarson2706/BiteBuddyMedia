# Canva template registry

> **This documents a road not taken. Superseded 2026-08-01.**
> The render path is `Content-Engine/render_slides.py`, not Canva. Canva's
> `generate-design` emits one page per call so it cannot build a carousel, and this
> environment cannot download Canva exports (`export-download.canva.com` is 403 at the
> proxy). The designs below are single-page AI starters that were never used to render
> a live post. Canva remains useful for one-off polish and for Connor editing a deck by
> hand. The slide layouts that actually ship are described in `DESIGN-SYSTEM.md` §2 and
> demonstrated in `Posts/_TEMPLATES/`.

*Where the series templates live in Canva. Created 2026-07-25.*

Folder: **BiteBuddy Templates** — https://www.canva.com/folder/FAHQXmgVxy0

| Series | Archetype | Design ID | Edit link | Status |
|---|---|---|---|---|
| S1 Guess the Calories | QUIZ-CARD | `DAHQXrHiByA` | https://www.canva.com/d/KyOA5Dictm2nP7C | AI starter, awaiting Connor's visual pass |
| S2 Protein Per Dollar | RANK-CARD | `DAHQXlgLYpc` | https://www.canva.com/d/8hcaHUdBUEXIP-J | AI starter, awaiting Connor's visual pass |
| S3 Why Tracking Fails | STORY-BEAT | `DAHQXrm4cqs` | https://www.canva.com/d/nh0ssiw9KUUwqY_ | AI starter, awaiting Connor's visual pass |

## Status meanings

- **AI starter** — generated single-page starting point on the brand kit. Connor
  should eyeball each in Canva (5 minutes): fix anything off-brand, then it graduates
  to **approved**. The loop may render from starters, but approved templates are the
  goal.
- Each design is currently ONE page (the generator's limit). The render phase
  duplicates the page per slide and swaps copy/photos per the archetype specs in
  `DESIGN-SYSTEM.md`; cover and CTA pages get added per post (Buddy from
  `Brand-Assets/buddy-poses/transparent/`, real screenshots from `UI-Library/`).

## Render-phase constraint discovered 2026-07-25 (important)

This environment's network policy **blocks downloading Canva export files**
(`export-download.canva.com` returns 403 at the proxy). Two consequences for the
weekly loop, both already designed around:

1. **Publish path:** hand Canva's export URL directly to Upload-Post — its servers
   fetch the file themselves, no proxy involved. Do not try to download exports
   locally first.
2. **Repo archival:** store design IDs + view links in the week's manifest instead
   of PNG files. (If Connor ever allows that domain in the environment's network
   settings, PNG archival can resume; not required.)

Visual QA of rendered slides therefore happens in Canva (Connor's eyeball pass or a
session with the domain allowed), not via local export inspection.
