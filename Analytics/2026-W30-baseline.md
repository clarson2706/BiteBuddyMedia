# Baseline report — the state of the accounts at reset (2026-07-25)

*Not a weekly loop report. This is the zero point: the first real performance data this
project has ever recorded, pulled from Upload-Post the day the new system was verified.
Every future report measures against this.*

## The numbers

| | TikTok | YouTube |
|---|---|---|
| Followers / subscribers | **1** | **5** |
| Total views | 668 | 433 |
| Posts | 17 | not reported |
| Likes | 2 | 3 |
| Comments | **0** | **0** |
| Shares | **0** | n/a |

**Daily views, TikTok:** 0 through Jul 21 → **194** (Jul 22) → **423** (Jul 23) → 22 (Jul 24) → 29 (Jul 25)

**Daily views, YouTube:** 3 (Jul 19) → **271** (Jul 20) → 73 (Jul 21) → 85 (Jul 22) → **0, 0, 0** (Jul 23, 24, 25)

## What this says

**1. Distribution collapsed, it did not decay.** YouTube going to a flat zero for three
consecutive days after a 271-view day is not normal falloff. TikTok dropping from 423 to
22 in one day is the same shape. Both changes land immediately after the five
simultaneous posts on 22 July. This is the strongest evidence yet that the suspected
throttle is real, on both platforms.

**2. Engagement is effectively nil.** 2 likes and 0 comments across 17 TikTok posts is
not a reach problem, it is a content problem. ~39 views per post with no saves, shares,
or comments means even the people who saw it felt nothing. Zero comments also means zero
"what app is this?" moments, which is the highest-intent signal we have.

**3. The funnel never started.** 1 TikTok follower and 5 YouTube subscribers against
$7 MRR. Nothing here was converting.

## What it changes about the plan

- **Volume was never the bottleneck; quality and cadence-safety were.** The old system
  ran 6 posts/day into an account that had 1 follower. The new loop runs 2/day at
  platform-safe spacing, which is the correct response to a suppressed account.
- **Optimize for comments and saves first, not views.** The metric ladder in
  `WEEKLY-LOOP.md` already says this; this data is why. A post that earns 20 views and
  one "what app is this?" beats a post that earns 400 silent views.
- **78 queued old-system posts were cancelled** on this date rather than allowed to
  continue the pattern that produced these numbers.
- **Expect a recovery period.** If suppression is real, early weeks of the new loop may
  show low reach regardless of content quality. Do not read week 1 as a verdict on the
  content; read the trend across weeks 1 to 3.

## Correction, same day

The first Instagram pull showed 4 comments and 1 follower, and an earlier reading of it
treated Instagram as the more engaged audience. **That was wrong.** Connor confirmed the
comments were posted by the BiteBuddy account itself and the follower is a personal
acquaintance. **Organic engagement across every platform is zero.** Nothing in the
history so far represents a stranger responding to this content, which makes the first
genuine comment from an unknown viewer the single most meaningful milestone available,
well before any view-count target.

## Correction, 2026-07-25 evening — the TikTok daily series above is wrong

Connor supplied TikTok's own Overview export that evening and it contradicts the
Upload-Post numbers used here. The real TikTok series is **195 (Jul 21) → 409
(Jul 22) → 40 (Jul 23) → 33 (Jul 24)**: Upload-Post reported each day's figures
against the following date. The peak was the day of the five simultaneous posts,
not the day after, and the collapse follows it by one day.

The export also counts 9 likes across Jul 21 and 22, where Upload-Post reported 3
lifetime, and **Connor confirmed all 9 came from strangers.**

That breaks the central claim in "What this says" above. "2 likes and 0 comments
across 17 TikTok posts is not a reach problem, it is a content problem" is wrong.
On the two days this account had reach, the old content converted at ~1.5% likes.
It then had reach on no other day in the window. The evidence points at
**distribution**, not at content quality.

It also moves the first-organic-engagement milestone from Jul 25 back to
**Jul 21**. The "Correction, same day" section below is itself now partly wrong:
organic engagement across the platforms was not zero, it was 9 likes on TikTok
that Upload-Post never surfaced. The Instagram half of that correction still
holds. Full reconciliation in `2026-07-25-tiktok-export-reconciliation.md`.

## Caveats

- These are **account-level aggregates**, not per-post. The Upload-Post `get_history`
  endpoint returned HTTP 400, so per-post attribution for the pre-reset posts is not
  available. Future posts get per-post rows because the loop records their IDs at
  schedule time.
- Instagram and Facebook are absent entirely: they were never linked in Upload-Post, so
  none of the old Instagram-targeted posts could have published.
- Raw rows are in `performance-log.jsonl` as `PRE-RESET-AGGREGATE`.
