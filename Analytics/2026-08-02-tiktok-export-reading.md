# TikTok export, 2026-08-02: reach recovered, conversion did not

*Ingested from `platform-exports/tiktok-overview-2026-07-21_2026-08-01.csv` (TikTok
Studio full-range export, 365 rows, 12 with activity). 8 new ACCOUNT-DAILY rows appended
to `performance-log.jsonl`; Jul 21 to 24 were already logged from the previous export and
match it exactly.*

## What the numbers say

| Window | Views | Views/day | Likes |
|---|---|---|---|
| Jul 21 to 24 (incl. the post-Jul-22 collapse) | 677 | 169 | 9 |
| Jul 25 to Aug 1 | 5,438 | 680 | 74 |
| **Jul 28 to Aug 1 (last five days)** | **4,282** | **856** | 67 |

Daily views: 195, 409, **40, 33**, 553, 358, 245, 532, 717, 1076, **1213**, 744.

**The throttle lifted.** Jul 23 and 24 were 40 and 33 views, which is the collapse the
sprint doc describes after the five simultaneous posts on Jul 22. From Jul 25 the account
climbs steadily and peaks at 1,213 views on Jul 31, roughly 30x the floor and about 7x the
pre-incident rate. Likes track it: 25 on Jul 31, against 2 to 3 per day the week before.

**This corrects an earlier read.** A session on 2026-08-02 cited "895 lifetime account
views" from the Jul 25 log and concluded TikTok reach was still collapsed. That was true of
the data available then and is not true now: the account has taken 6,115 views in this
twelve-day window alone. Distribution on TikTok is no longer the binding constraint.

## What did not move

- **Zero comments and zero shares, every day, all year.** Not low. Zero.
- **13 profile views on 6,115 video views: 0.21%.** Almost nobody who watches goes looking
  for the account.
- **RevenueCat, same window: 50 to 53 new customers, so 3 in eight days.** ~5,400 views
  produced roughly three installs, and that is an upper bound since it assumes every new
  customer came from TikTok.

The funnel has moved its bottleneck. It used to be "nobody sees the posts." It is now
"people see the posts and do nothing," and the metric ladder in `WEEKLY-LOOP.md` says
exactly what that means: views without saves, shares or profile activity is entertainment,
not marketing. The posts are being served. The ask is not landing.

## Two confounders, stated rather than glossed

1. **The cadence change straddles this window.** TikTok went to 3 posts/day on 2026-07-25,
   the same day the recovery starts. `SPRINT-AUG25.md` flags this in advance: any
   comparison across Jul 25 reads a cadence change and a content change at once, and this
   one cannot separate them.
2. **Nothing new was scheduled after ~Jul 26.** No loop run has left a commit since then,
   so the climb to 1,213 views/day is most likely the algorithmic tail of posts already
   published rather than the effect of new volume. That is a hypothesis: per-post rows are
   unavailable (Upload-Post `get_history` was returning 400 at last check), so it cannot be
   confirmed from an account-level export. If it is right, it is good news twice over,
   because it means a small back catalogue is still compounding without being fed.

## What this should change

The conversion spec added on 2026-08-02 was built on the assumption that the ask is the
weak link. This export is the first real evidence for that assumption, and it argues for
running the CTA ladder hard: comment-first CTAs until the comment count is non-zero, and
the `SAVE` slide earning its place. A post that takes 1,000 views and produces no comment,
no share and no profile view has failed at the ask, not at the hook.

The next report should compare against the benchmark table in
`Content-Engine/CAROUSEL-CONVERSION-SPEC.md` §1 directly, and say which rungs we miss.
On the evidence here we miss the bottom three by a distance.
