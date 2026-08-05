# Paid ads, day 1 — 2026-08-04

*First day of paid acquisition. Campaign `1872465614907521`, ad group
`1872466642086321`, ad `1872482993643554`, identity "BiteBuddy: AI Calorie
Scanner". Sources: TikTok Ads Manager hourly and creatives exports, committed
verbatim under `platform-exports/`, normalised by `ingest_tiktok_ads.py`.*

> **Correction, same day.** An earlier draft of this file called these Meta ads
> and the ingest script was named `ingest_meta_ads.py`. They are **TikTok Ads**.
> The creatives export settles it: `Sound clicks`, `Paid follows`, `Paid profile
> visits`, `6-second focused views`, `Related ad groups`, `Identity`, and
> `Secondary source: TikTok account` are all TikTok Ads Manager fields, and the
> two carousel Post IDs are our own organic TikTok posts. The platform matters
> here for more than naming — see "the Aug 3 collision" below.

## The day

| Metric | Value |
|---|---|
| Spend | $7.63 |
| Impressions | 1,061 |
| CPM | $7.19 |
| Clicks (destination) | 2 |
| CTR (destination) | 0.189% |
| Clicks (all) | 11 |
| CTR (all) | 1.037% |
| CPC (destination) | $3.81 |
| Video views | 784 |
| Conversions | 0 |
| Conversions (SKAN) | 0 — **provisional**, postbacks lag 24–72h |
| Cost per conversion | null (no conversions) |

Creative rows sum exactly to the day totals on spend, impressions, both click
types, video views and conversions. Both exports agree with each other and with
TikTok's own totals row.

## The Aug 3 collision

**Every creative has `Created on: 2026-08-03`. That is the exact day organic
TikTok reach collapsed** (see `2026-08-04-media-report.md`: 274 views on the last
Aug 2 post, then 4 / 3 / 1 / 0 across all four Aug 3 posts).

So Aug 3 now carries **three** simultaneous changes on one account, not two:

1. Cadence went 3/day to 4/day, breaking the documented ceiling.
2. The 08:02 post was a near-verbatim repost of the previous morning's.
3. **A paid ad account was attached to the same identity and began spending.**

This is recorded as a coincidence in time, not a mechanism. Running ads is not a
documented cause of organic suppression, and it would be exactly the kind of
fabricated cause this repo's analytics rules forbid. But a brand-new ad account
opening on a 1-follower profile that is simultaneously posting four times a day
with recycled creative is a plausible trigger for automated review, and it is now
at least as good a candidate as the other two.

**One inference the paid data does support.** Paid delivered normally on Aug 4
(1,061 impressions, ordinary CPM) while organic sat at zero. TikTok is willing to
show BiteBuddy content to people; it is not willing to show it *organically*.
That is consistent with a reach restriction on the organic side rather than a
whole-account ban, and it is the first independent evidence for the suppression
hypothesis.

## This was not a day of delivery

Nothing served before 09:00. Delivery ran 14 hours and was heavily back-loaded:

| Window | Impressions | Spend |
|---|---|---|
| 00:00–08:00 | 0 | $0.00 |
| 09:00–19:00 | 342 (32%) | $2.00 (26%) |
| **20:00–23:00** | **719 (68%)** | **$5.63 (74%)** |

Treat this as roughly a quarter-day of data, not a day. CPM climbed through the
day ($1.76 at 12:00 → $9.47 at 21:00, blended $7.19), which is the normal shape
as cheap inventory runs out, not a signal about the creative.

## By creative

Retention rates are per *video view*. Carousels have no video, so those cells are
null rather than zero — zero would read as "nobody finished it."

| Creative | Type | Spend | Impr | CPM | →25% | →50% | 100% | Avg play | Dest / All clicks |
|---|---|---|---|---|---|---|---|---|---|
| YOUR_FOOD_HAS_A_WITNESS | video | $2.11 | 299 | $7.06 | 13.6% | 2.5% | 1.1% | 1.66s | 1 / 8 |
| Dark_hype_TT_VO | video | $2.01 | 201 | $10.00 | 17.8% | **8.7%** | **2.7%** | 2.05s | 0 / 0 |
| EVERY_OTHER_TRACKER | video | $1.08 | 177 | $6.10 | 11.5% | 1.8% | 1.2% | **6.37s** | 0 / 1 |
| Dark Hype 2 | video | $1.24 | 161 | $7.70 | **20.0%** | 5.2% | 1.3% | 1.90s | 0 / 0 |
| Chick-fil-A breakfast (Spark) | carousel | $0.67 | 123 | $5.45 | – | – | – | – | **1 / 2** |
| Chick-fil-A ranked (Spark) | carousel | $0.52 | 100 | $5.20 | – | – | – | – | 0 / 0 |

## The one real finding: the hook dies in two seconds

The funnel across all four videos:

**1,061 impressions → 784 autoplays (93%) → ~110 reach the 25% mark → 5 finish.**

That 93% "video view" number is not engagement, it is autoplay. The number that
matters is what happens next, and what happens next is that **86–88% of viewers
leave before the quarter mark**, with an average play time of **1.66–2.05
seconds** on three of the four videos.

This is the highest-leverage thing on the board, and it is a first-two-seconds
problem: the opening frame is not earning the third second. It is also the one
finding here robust enough to act on, because it is consistent across four
independent creatives rather than resting on a click count.

**What is not robust.** Every click comparison. Two destination clicks across the
entire day. The per-creative ranking on retention rests on quartile counts in
single digits (Dark_hype's "best completion" is 5 people). Nothing here justifies
pausing a creative, and pausing one would reset learning anyway.

**One anomaly, flagged not explained.** EVERY_OTHER_TRACKER reports the highest
average play time (6.37s, ~3× the others) alongside the *worst* quartile
retention (11.5% at 25%, 1.8% at 50%). Those two cannot both describe the same
viewing behaviour under any obvious reading. Likely a small-sample or
loop-counting artifact. Do not build on it until a larger day either repeats or
dissolves it.

## Paid engagement is zero

Across 1,061 impressions: **0 follows, 2 likes, 0 comments, 0 shares, 6 profile
visits, 0 sound clicks.** This matches the organic picture exactly — 0 comments
across 47 organic videos — and says the problem is not distribution-specific.
Paying for reach reproduced the same non-response that free reach produced.

## Structural note for later

All six creatives sit inside **one ad** in **one ad group**. TikTok rotates them
internally, which means: creative performance cannot be cleanly compared (budget
allocation between them is the algorithm's choice, not an even split), and a
single creative cannot be paused without editing the ad and resetting learning.
Splitting creatives across ad groups is the fix, but it is a rebuild — not a
day-2 action.

## Independent check that does not depend on attribution

RevenueCat sees every app open whether or not SKAN attributes it. As of
2026-08-04: **59 new customers / 61 active users** trailing 28 days, 1 active
trial, 1 active subscription, $7 MRR. Weekly run-rate 6–10, so the organic
baseline is **~1.2 new customers/day**.

A day showing 4–5 new customers is the ads working, whatever TikTok reports. This
also corrects `CLAUDE.md`, which still says the app has "effectively zero users."

## Decision rule for day 2, set before the number is known

Day 2 at a $20 budget and a ~$7 CPM should produce roughly 2,800 impressions,
putting the cumulative total near 3,800 — the first point at which CTR is worth
reading.

- All-clicks CTR holds ≥1% but destination CTR stays under ~0.3% → CTA/offer
  problem, not creative, not targeting.
- **Reaching-25% rate stays under ~20%** → the hook is the bottleneck, and it is
  the first thing to rebuild once learning allows a change.
- Clicks healthy but installs still 0 past ~$28 cumulative → the App Store
  product page is the leak.
- RevenueCat new-customers stays at ~1/day through a full $20 day → paid is not
  reaching anyone who wants this, independent of what TikTok reports.

**Recommendation carried into day 2: change nothing.** Any edit to budget (beyond
~20%), creative, targeting, or optimisation event restarts learning and forfeits
the only progress day 1 bought. If $20 is already the set daily budget, let it run
untouched. If $20 would be an increase from a lower budget, hold instead — the
raise is itself a learning reset and would confound day 2 against day 1.

**Separate from the budget question:** verify TikTok is actually receiving install
events (TikTok Events Manager / the app's SKAN configuration). A campaign
optimising toward an event it never receives spends the full budget and learns
nothing.
