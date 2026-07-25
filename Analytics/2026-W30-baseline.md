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

## Caveats

- These are **account-level aggregates**, not per-post. The Upload-Post `get_history`
  endpoint returned HTTP 400, so per-post attribution for the pre-reset posts is not
  available. Future posts get per-post rows because the loop records their IDs at
  schedule time.
- Instagram and Facebook are absent entirely: they were never linked in Upload-Post, so
  none of the old Instagram-targeted posts could have published.
- Raw rows are in `performance-log.jsonl` as `PRE-RESET-AGGREGATE`.
