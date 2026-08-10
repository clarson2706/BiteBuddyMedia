# Ad-Creative — AI-generated video concepts (Higgsfield)

**This is not organic content and does not follow the Content-Engine pipeline.**
It exists outside the weekly loop, the registry, and the series roster.

## Why this is a separate lane

`CLAUDE.md`'s content guardrails say: *"Real screenshots only for app slides.
Never redraw, mock, or invent UI or numbers."* The videos here are fully
AI-generated (Higgsfield / Seedance / Kling) — they *reference* real UI
screenshots from `UI-Library/` but the model still approximates layout and
text, and text fidelity is imperfect (known issue — see Status below). That
disqualifies them from the organic pipeline's guardrail, so they never touch
`Content-Engine/`, `Posts/`, or `registry.jsonl`.

This folder is for **paid-ad experimentation and creative exploration only**,
produced in a session working from `BiteBuddyMVP`'s marketing branch
(`claude/ios-app-video-marketing-na3hf2`, now closed/orphaned there since this
repo is the real home for marketing material as of 2026-07-24). Nothing here
is scheduled or published automatically — everything in `Ad-Creative/` needs
Connor's explicit review before any use, same as any other spend/publish
decision per `CLAUDE.md`'s approval gates.

## What's here

- **`generated/`** — 10 rendered 10-second, 9:16, 720p videos (concepts +
  hook variants + hype teasers). Drop zone + manifest; see its README for the
  full list, links, and status of getting the actual video files into the repo.
- **`concepts/`** — the 5 original video-concept scripts (hook, beat sheet,
  screenshot map) that seeded the videos, ported from `BiteBuddyMVP`.

## Status: UI fidelity

Reference-anchored generation (real screenshots fed in as style/end-frame
references) gets meaningfully closer than pure text-to-video, but small
on-screen text can still soften or drift. Treat every video here as a
**creative-direction test**, not a finished, ship-ready ad. If a concept is
worth running as paid spend, the recommended finishing step is compositing
the exact real screenshot PNGs over the AI-generated motion (keeps the
generated hook/human/motion, swaps in pixel-perfect UI) rather than trusting
the raw AI output for anything with legible on-screen text.

## Relationship to the DEMO video track

`Content-Engine/SERIES.md`'s DEMO track (real screen recordings, edited by
`build_demo.py`, scheduled by the `demo-drop` skill) is the organic,
guardrail-compliant video format and is unrelated to this folder. Do not
confuse the two: DEMO = real recordings, ships automatically under the
weekly loop's authorization. `Ad-Creative/` = AI-generated, ships only on
Connor's explicit call.
