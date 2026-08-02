# The first real per-post read, and a correction

*2026-08-02. Written after Connor asked whether the posts that actually worked had been
analysed. They had not. This corrects that, and corrects three claims in
`2026-W31-report.md` written earlier the same day.*

## What I got wrong

`2026-W31-report.md` says per-post rows are unavailable and skips every per-series,
per-hook and per-slot table. That claim came from a note in the Jul 25 directives saying
`get_history` returns 400. **`get_history` does still 400, but `get_post_analytics` and
`get_cached_post_analytics` both work.** I never tested them. The tables were skipped for
no reason, the week was generated without them, and the directives were written at
`confidence: low` when real data was one call away.

`performance-log.jsonl` now has **13 genuine per-post rows** in it, the first this project
has ever recorded. That was supposed to be the whole point of the rebuild.

## TikTok, every post the platform reports

| Views | Likes | Type | Post | In repo? |
|---|---|---|---|---|
| **462** | 2 | photo | 5 things people forget to log (MISTAKE, SAVE) | yes |
| 305 | 3 | photo | Most people think they eat the same every day (TRACKED, APP) | yes |
| 293 | **6** | photo | untracked, Jul 28 18:01 | **no** |
| 293 | 2 | photo | untracked, Jul 29 13:02 | **no** |
| 287 | 2 | photo | untracked, Jul 25 13:03 | **no** |
| 281 | 0 | photo | Guess the calories, salmon plate (GUESS, APP) | yes |
| 122 | 0 | photo | untracked, Aug 2 13:02 (partial day) | **no** |
| 104 | 0 | photo | untracked, Jul 29 00:01 | **no** |
| **0** | 0 | photo | POV: the app made you feel worse than the food did (POV, FOLLOW) | yes |
| **1** | 0 | **video** | One photo found all four foods (DEMO, APP) | yes |

YouTube: 53, 34, 32 views on three Shorts. One like total.

## Four findings, in order of how much they matter

### 1. Video is the worst-performing thing this account has ever posted

One view. The nine photo carousels averaged 239 and the median was 287. The demo video was
posted on Jul 26 at 18:02, the same day a photo carousel took 462 views, so it is not a
bad-day effect.

**This is n=1 and should not be over-read.** But it is the only evidence that exists, it
points hard in one direction, and I scheduled three brand-film videos into this week's
20:00 slots without knowing it. That was the blind spot.

### 2. Reach is nearly flat regardless of content

Eight of the nine photo posts land between 104 and 462, and six of those sit in a 281 to
305 band. That is not content-driven variance, that is TikTok handing each post a similar
small test audience and none of them breaking out. **Which means the differences between
this week's 25 carousels will not show up as reach differences.** They will show up, if
anywhere, in engagement rate inside a fixed ~290-view audience, currently 0 to 6 likes and
zero comments on everything.

The practical consequence: judging this week's posts by views will teach us nothing. Likes
per view, and any comment at all, are the only readable signals at this account size.

### 3. One post was zero. Not low. Zero.

"POV: the app made you feel worse than the food did", Jul 26 13:03. Every other photo post
that week got 100+. A hard zero on a platform that gives everything a test audience means
suppression, not indifference. The same concept on YouTube got 34 views, so the creative
rendered fine and the file was not broken.

Best available read: the framing. It is the only post in the set that leads with the app
being harmful, and TikTok's health-content classifier is exactly the thing the
`HOOK-INTELLIGENCE-2026.md` anti-patterns warn about. **Do not write hooks that lead with
the product hurting someone**, even when the payoff is kind. This week's decks were
already clear of that, by luck rather than judgment.

### 4. Roughly fourteen posts went out that this repo has no record of

Five of the ten TikTok posts are untracked: Jul 25 13:03, Jul 28 18:01, Jul 29 00:01, Jul
29 13:02, Aug 2 13:02. TikTok's `video_count` went from 17 on Jul 25 to 36 today, and this
repo accounts for about five of those nineteen.

**Something other than this repo is posting to the account.** That invalidates a claim in
the W31 report: I wrote that nothing was scheduled after Jul 26 and therefore the reach
recovery was the back catalogue compounding. It was not. New posts were going out through
most of that window, they just were not coming from here. The compounding story was wrong.

This also means the two posts scheduled for tonight, which I noticed but did not
investigate, are part of a pattern rather than leftovers. Worth Connor identifying what
that other source is, because right now two systems are posting to one account and neither
can see the other's numbers.

## What this changes

1. **The three brand films are the open question.** Recommendation below; it is Connor's
   call because he chose them deliberately.
2. **Directives go to `confidence: medium`** for the video finding and the suppression
   finding, and stay `low` on anything about hooks or series, where the sample per cut is
   one or two posts.
3. **Next Sunday's report has no excuse.** Per-post pulls run first, every post gets a row,
   and the per-series/per-hook/per-CTA tables get produced from real numbers.
4. **Judge this week on likes-per-view and comments, not views.** Views are being handed
   out at a near-fixed rate and will not discriminate between 25 decks.

## The film recommendation

The evidence says video gets ~1 view on this account and carousels get ~290. Three of the
28 slots are currently films.

**Recommended: keep one, convert two.** Leave "Every tracker dies in week one" on Thursday
20:00, because its copy is the strongest of the three and it is worth one clean test of
whether a produced brand film behaves differently from the screen-recording demo that got
1 view. Convert the other two concepts into carousels, which is the format with nine data
points behind it, and re-slot the films for a later week once there is a second video
reading.

The alternative, running all three, costs about 870 expected views against the carousel
baseline. That is a real but survivable price for testing three films at once, and if
Connor wants the films to run as a set, that is a defensible read of n=1 evidence.

**Decided 2026-08-02: run all three, unchanged.** Connor's call on n=1 evidence, and the
schedule stands. This converts the films from a risk into a stated experiment, so next
week's report must read it as one rather than reopening the question:

- **Hypothesis under test:** produced brand film behaves differently on this account from
  the raw screen-recording demo that took 1 view.
- **Prediction if video is simply throttled here:** all three land under ~20 views.
- **Prediction if the demo's 1 view was about that specific asset:** the films land in the
  photo band, roughly 100 to 460.
- **What settles it:** three readings instead of one. Anything in between, or a split
  across the three, means the variable is the asset and not the format, and the next test
  is publishing natively from the app rather than through the API.
- **What does not settle it:** views alone if all three land near 290. At that point the
  format question is answered and the read moves to likes-per-view, same as the carousels.
