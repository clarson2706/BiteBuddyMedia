# Weekly report — 2026-W31 (run 2026-07-28, off-schedule Tuesday fire)

*This run fired Tuesday 2026-07-28 08:56 America/Chicago, not Sunday. Per
`WEEKLY-LOOP.md` "Partial generation," it runs the full loop unchanged except Phase 2
generates only the slots between now and the end of Sunday 2026-08-02. Analytics below
cover every post in `registry.jsonl` from the last 14 days regardless of that.*

## Headline: Instagram is not publishing anything, and has not since the reset

Every Instagram publish attempt since 2026-07-25 has failed: `list_users` shows the
Instagram entry in `social_accounts` as an empty string, and every IG job in
`get_history` for this account's posts either errors with *"Action suspected as spam.
Activity is restricted"* or never appears at all. That is **4 attempted IG posts, 4
failures** (2026-07-25-slot1, slot2, 2026-07-26-slot1, slot2, plus the demo). Every prior
manifest line reading `"platforms_scheduled": ["instagram", ...]` from the 2026-07-25
bridge run was aspirational, not real: none of it posted. **This run schedules nothing to
Instagram** and this is the top item for Connor below.

## What went well

- **Real per-post rows exist for the first time**, pulled via `get_post_analytics` per
  `request_id` rather than account aggregates. That alone is the fix the system was
  missing.
- **TikTok had its best single day since the 07-22 throttle**: 814 views on 07-26, the
  day three carousel-track posts went out (a slot1, the first DEMO video, and a slot2).
  It's the first sign the account is not permanently capped.
- Two posts cleared 300+ TikTok views with real likes: **"5 things people forget to
  log"** (MISTAKE, P4, oneoff) at 377 views / 2 likes, and **"Most people think they eat
  the same every day"** (TRACKED, P4, oneoff) at 302 views / 3 likes. These are this
  cycle's best-on-the-ladder posts (views + likes both present, no comments yet on
  anything).
- Lifetime TikTok likes moved from 2 (at reset) to 8, all still small numbers but real
  and organic.

## What didn't

- **Instagram: 4-for-4 publish failures**, covered above. This is a distribution
  problem, not a content one — the account itself is flagged, not any specific post.
- **Zero comments across every new-system post**, including
  `2026-07-25-flex1` ("Guess the calories... salmon plate"), which was purpose-built to
  earn the lowest-effort comment possible (drop a number, no editing). 281 views, 0
  comments, 0 likes. The lowest-friction ask we could design still didn't convert. Note
  TikTok's pinned comment never actually posts (API limitation, documented in
  `UPLOAD-POST.md`), so the ask lived only in-slide, which may be part of why.
- **YouTube went flat to zero for three straight days** (07-26, 07-27, 07-28) despite two
  fresh videos posted 07-25 and 07-26 — the same collapse-not-decay shape seen after the
  07-22 five-simultaneous-post incident. Reads as distribution, not content.
- **Per-post data for 07-26 is internally inconsistent.** The account's own daily-view
  series shows 814 views that day; the per-post row for `2026-07-26-slot1` reads 0 views
  at T+2d. Per `Analytics/README.md` Rule #2 (platform exports outrank Upload-Post), this
  is flagged rather than trusted — we do not know which of that day's three posts
  actually drove the spike.
- **S2 (Protein Per Dollar) has had zero posts since the reset.** SERIES.md requires 2
  posts/week minimum before any read; S2 is the only active series with none. This run's
  generation prioritizes closing that gap (see directives).
- **The DEMO video track's first post is the weakest performer so far**: 0 TikTok views
  at T+2d, 27 YouTube views. One data point, too early to verdict, but worth watching.

## What changes next week (directives, each traceable above)

1. **Stop scheduling to Instagram** until Connor manually logs into Instagram and clears
   the "activity restricted" flag. Traces to: 4/4 IG failures this cycle.
2. **Do not read 07-26 as a single-post win.** Treat it as an account-level signal only
   until a platform-native export (not the API) can attribute it to a specific post.
   Traces to: the slot1/day-total mismatch above.
3. **Prioritize closing the S2 gap this generation.** S2 gets its first post since reset
   this cycle (a verified Chick-fil-A protein ranking — see the network note below).
   Traces to: 0 S2 posts vs. SERIES.md's 2/week minimum.
4. **Hold all three series verdicts at "hold."** No series has the minimum 2 weeks x 2
   posts yet (S1: 1 post total, S2: 0, S3: 2). Verdicts before that are noise per
   SERIES.md's own testing protocol.
5. **De-prioritize comment-count as this account's near-term success metric.** Even the
   lowest-effort ask produced zero comments on 281 views. Keep testing it, but do not
   treat "0 comments" as a content failure signal on its own until reach is larger.
6. **Network note, superseding the "known blocker" language in the weekly-loop skill:**
   chipotle.com and fdc.nal.usda.gov both returned normal content when checked live this
   run (2026-07-28); chick-fil-a.com's individual menu-item pages (e.g.
   `/menu/salads/cobb-salad`, `/nutrition-allergens`) rendered real structured nutrition
   data. The JS-driven Chipotle "nutrition calculator" specifically does not render via
   this environment's fetch tool (no JS execution), which is a tool limitation, not a
   network block. This run verified Chick-fil-A protein/calorie numbers directly against
   `chick-fil-a.com`'s own pages; no chain **pricing** data was attempted (menu prices
   require an ordering flow this tool can't execute), so "Protein Per Dollar" content
   this cycle is a protein ranking without a price claim, noted honestly in the manifest.

## Tables

### By series (this cycle's real posted rows only, TikTok)

| Series | Posts | Views (sum) | Likes (sum) | Comments |
|---|---|---|---|---|
| S3 (Why Tracking Fails) | 2 | 264 | 1 | 0 |
| S1 (Guess the Calories) | 1 | 281 | 0 | 0 |
| S2 (Protein Per Dollar) | 0 | - | - | - |
| oneoff | 2 | 679 | 5 | 0 |
| DEMO | 1 | 0 | 0 | 0 |

### By persona

| Persona | Posts | Views (sum, TikTok) |
|---|---|---|
| P1 | 2 | 264 |
| P4 | 3 | 679 |
| P5 | 1 | 281 |

### By hook family

| Family | Posts | Views (sum) |
|---|---|---|
| RIGHTWRONG | 1 | 264 |
| POV | 1 | 0 (see caveat above) |
| MISTAKE | 1 | 377 |
| TRACKED | 1 | 302 |
| GUESS | 1 | 281 |
| OUTCOME | 1 (DEMO) | 0 |

### Platform totals (lifetime, `get_analytics`, captured 2026-07-28)

| Platform | Followers | Lifetime impressions | Likes | Comments |
|---|---|---|---|---|
| TikTok | 1 | 1450 | 8 | 0 |
| YouTube | 5 | 503 | 4 | 0 |
| Instagram | - | not publishing | - | - |

Small-sample caveat holds throughout: this is day 3-4 of a brand-new measurement system
on an account with 1 TikTok follower. Directions, not verdicts.
