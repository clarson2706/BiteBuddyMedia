# Paid ads, day 1 — 2026-08-04

*First day of Meta paid acquisition. Ad `1872482993643554`. Source: Meta Ads
Manager hourly export, committed verbatim at
`platform-exports/meta-ads-hourly-2026-08-04.xlsx`, normalised into
`paid-ads.jsonl` by `ingest_meta_ads.py`. Totals re-derived from the hourly rows
agree exactly with Meta's own totals row ($7.63 / 1,061 / $7.19 / 2 clicks).*

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
| Video view rate | 73.9% |
| Conversions | 0 |
| Conversions (SKAN) | 0 — **provisional** |
| Cost per conversion | null (no conversions) |

## This was not a day of delivery

Nothing served before 09:00. Delivery ran 14 hours and was heavily back-loaded:

| Window | Impressions | Spend |
|---|---|---|
| 00:00–08:00 | 0 | $0.00 |
| 09:00–19:00 | 342 (32%) | $2.00 (26%) |
| **20:00–23:00** | **719 (68%)** | **$5.63 (74%)** |

Two thirds of the day's impressions landed in the final four hours, while the ad
set was still in learning. Treat this as roughly a quarter-day of data, not a
day, and do not compare it like-for-like against a future full day.

CPM climbed through the day ($1.76 at 12:00 → $9.47 at 21:00, blended $7.19).
That is the normal shape as Meta exhausts cheap inventory and widens delivery,
not a signal about the creative.

## What is readable, and what is not

**Not readable.** Destination CTR at 0.189% rests on **2 clicks**. At n=2 there is
no conclusion available, in either direction. Nothing about the creative,
targeting, or offer can be concluded from day 1, and any change made on this
evidence would be a coin flip that also resets the learning phase.

**Weakly encouraging.** All-clicks CTR of 1.04% is an ordinary healthy number,
and a 73.9% video view rate says the creative is not being scrolled past
instantly. Caveat: Meta's default "video view" is a 3-second play, which is a
soft threshold — this is evidence of non-rejection, not of interest.

**The gap to watch.** 11 all-clicks versus 2 destination clicks. People are
touching the ad and not tapping through. If that ratio holds at a readable
sample size, the problem is the CTA/offer rather than the creative or the
audience. One day is not a readable sample size.

**Conversions.** 0 and 0 (SKAN). Logged as 0 rather than null because Meta
reported them as none, but SKAdNetwork postbacks lag 24–72h, so the row carries
`skan_provisional: true`. Re-ingest 2026-08-04 with `--force` in a few days to
pick up backfilled postbacks before treating this zero as final.

## Independent check that does not depend on attribution

RevenueCat sees every app open regardless of whether SKAN attributes it. As of
2026-08-04: **59 new customers / 61 active users in the trailing 28 days**, 1
active trial, 1 active subscription, $7 MRR. Weekly run-rate is 6–10, so the
organic baseline is **~1.2 new customers/day**.

That is the cleanest read available on whether paid is doing anything: a day
showing 4–5 new customers is the ads working, whatever Meta reports.

It also corrects `CLAUDE.md`, which still says the app has "effectively zero
users." It has ~61 active and one paying. Small, but not zero, and the
distinction matters for how the content is pitched.

## Decision rule for day 2, set before the number is known

Day 2 at a $20 budget and a ~$7 CPM should produce roughly 2,800 impressions,
putting the cumulative total near 3,800 — the first point at which CTR is worth
reading.

- All-clicks CTR holds ≥1% but destination CTR stays under ~0.3% → CTA/offer
  problem, not creative, not targeting.
- All-clicks CTR falls below ~0.7% → creative problem.
- Clicks healthy but installs still 0 past ~$28 cumulative → the App Store
  product page is the leak.
- RevenueCat new-customers stays at ~1/day through a full $20 day → paid is not
  reaching anyone who wants this, independent of what Meta reports.

**Recommendation carried into day 2: change nothing.** Any edit to budget
(beyond ~20%), creative, targeting, or optimisation event restarts the learning
phase and forfeits the only progress day 1 bought. If $20 is already the set
daily budget, let it run untouched. If $20 would be an increase from a lower
budget, hold the current budget instead — the raise is itself a learning reset
and would confound day 2 against day 1.
