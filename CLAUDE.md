# CLAUDE.md — BiteBuddy marketing

Loaded automatically at session start in this repo. Last verified: 2026-07-24.

## What this repo is

Everything that gets BiteBuddy in front of people. Strategy, research, ideas, the weekly
production pipeline, and every rendered asset published so far. Moved out of `BiteBuddyMVP` on
2026-07-24 — see `README.md` for the layout.

**The app is live on the App Store and has zero users.** Distribution is the bottleneck. Content
that does not plausibly drive installs is not worth producing.

## Before proposing any strategy change

Read `Research/CAROUSEL-MARKETING-PLAYBOOK.md` and `AUTOMATION-WORKFLOW.md` first.
For content generation, also read `Research/TARGET-USER-PROFILES.md`,
`Research/HOOK-INTELLIGENCE-2026.md`, and `Content-Engine/` (the persona-targeted
bulk-generation system, added 2026-07-25). There is an
existing system with reasoning behind it. Replacing something deliberate is a different job from
replacing something accidental, and right now nobody knows which this is — because of the next
point.

## The measurement gap is the main problem

`Analytics/performance-log.jsonl` exists and is **0 bytes**. The rollups built from it
(`leaderboard.json`, `next-week-directives.*`) are gitignored generated outputs, so they cannot
exist either. `carousel-optimize` and its `analyze.py` are built to score posts and set next
week's direction from that log, and it has never had a single line in it.

Ten slots were published 20–23 July across TikTok, Instagram, and YouTube. Not one view,
impression, or click is recorded anywhere. Five went out simultaneously on 22 July and Instagram
may be throttled as a result — unconfirmed, because nothing measures it.

**Do not design a new content strategy on top of this.** Get the numbers first, even by hand from
each platform's native analytics. Rewriting hooks without knowing which hooks failed is guessing.

## Skills

`carousel-week` generates a week of slots. `carousel-publish` handles platform specs and the
Upload-Post mapping. `carousel-optimize` scores performance. They reference paths inside this repo
(`Posts/`, `Analytics/`, `Carousel-Ideas/`) — those were rewritten during the move, so if a path
does not resolve, that is a move artifact worth fixing rather than working around.

**Add a rate limit before the next automated run.** Five simultaneous posts is what likely got
Instagram flagged. `carousel-publish` is where that belongs.

## Two generation guides, deliberately

`.claude/skills/carousel-*` is for Claude. `Posts/2026-W30/CHATGPT-GENERATION-GUIDE.md` is for the
ChatGPT scheduled task that runs Sunday image generation over the GitHub MCP — ChatGPT cannot load
Claude skills, so the knowledge is written out there. Changing strategy means updating both. That
duplication is a real maintenance cost and worth revisiting if the ChatGPT half is retired.

## Approval gates

Anything published to a social account is **Connor's call, every time.** Draft, show, then post —
never post directly. Same for anything that spends money or changes App Store copy.

App Store listing copy lives in `BiteBuddyMVP/APP_STORE_METADATA.md`, including the canonical
search term every carousel CTA must use. Do not restate it here — point at it.

## Conventions

- Branch as `claude/<short-description>`. Never commit to `main`.
- Rendered assets and their `prompts.md` live in the same slot folder. Keep it that way.
- This repo holds binaries. Do not add build tooling or app code to it.
