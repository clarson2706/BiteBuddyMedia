# Media report 2026-08-04 — TikTok reach stopped dead on Aug 3

*Scope: TikTok, 31 Jul to 4 Aug (local, America/Chicago). Requested by Connor
after noticing views collapse. Read-only run of the `media-report` skill.
Per-post numbers pulled via `request_id` from Upload-Post, `post_metrics_source:
platform_api`, captured 2026-08-04 03:45Z.*

---

## 1. Headline

TikTok reach did not decline, it **stopped**. Every post from 08:02 on Aug 3
onward has taken **0 to 4 views**; every post before it took 258 to 307. The
break is between two consecutive posts eleven hours apart, with no taper. That
shape is a distribution shutoff at the account level, not a content problem.

Two things changed on Aug 3, both of which are known TikTok suppression
triggers, and both are still in force: **cadence went from 3 posts/day to 4**,
and the first post of the dead run was a **near-verbatim repost of the previous
morning's post**. 24 more TikTok posts are queued at the 4/day cadence through
Aug 9, so the condition is currently being reinforced roughly every four hours.

The second finding matters more than the first: the ~270 views/post that
disappeared **was never traction**. It is the size of TikTok's automatic
cold-start sample. Across 47 videos the account has 1 follower and **0 comments,
ever**. Restoring reach restores a number that was already not producing
installs.

---

## 2. The data

Per-post TikTok views. Local times, America/Chicago (confirmed from the
scheduler's own `original_timezone` field).

| Local time | Post | Views | Likes |
|---|---|---|---|
| Jul 31 08:02 | Dining hall high-protein plate | 278 | 3 |
| Jul 31 13:02 | POV: you stopped weighing your food | 47 | 0 |
| Jul 31 19:01 | A doctor's food diary request | 112 | 1 |
| Aug 1 08:02 | This plate is 48g protein for 580 cal | 307 | 0 |
| Aug 1 13:02 | 5 things I wish I knew before my first cut | 268 | 7 |
| Aug 1 19:02 | The real reason one bad food day wrecks the log | 258 | 4 |
| Aug 2 08:02 | You're not overeating. You're under-counting. | 263 | 4 |
| Aug 2 13:02 | Two Chick-fil-A orders, protein-efficiency | 265 | 1 |
| Aug 2 19:02 | I thought my lunches were healthy | 274 | 6 |
| **Aug 3 08:02** | **You are not overeating, you are under-counting** | **4** | 0 |
| **Aug 3 12:02** | **Guess the calories: salmon, crab cake** | **3** | 0 |
| **Aug 3 16:02** | **The four foods people always guess wrong** | **1** | 0 |
| **Aug 3 20:02** | **Day four is when tracking dies** | **0** | 0 |

Daily totals: Jul 31 = 437, Aug 1 = 833, Aug 2 = 802, **Aug 3 = 8**.

**Age is not the explanation.** At capture the Aug 3 posts were 14.7h, 10.7h,
6.7h and 2.7h old. Only the last is genuinely too young to judge. The 08:02
post has had most of a day and holds 4 views, against 263 for the post in the
identical slot 24 hours earlier. Four consecutive posts spanning twelve hours
all landing under five views is not variance.

**Note on the account-level daily series.** Upload-Post reports
`08-03=188, 08-04=0`, but its account aggregates are date-shifted by a day and
under-count (`2026-07-25-tiktok-export-reconciliation.md`). The per-post rows
above are unaffected and are what this report rests on. Connor's own figure
("431, then zero") does not reconcile exactly with either source; the shape
agrees and the per-post evidence is stronger, so the exact daily figure is left
open pending a TikTok Studio export.

---

## 3. What changed on Aug 3

**a. Cadence went 3/day to 4/day, and the slots moved.**

Through Aug 2 every day ran 08:00 / 13:00 / 19:00 — the documented ceiling in
`CLAUDE.md`. Aug 3 ran 08:00 / 12:00 / 16:00 / 20:00. That is a fourth post and
a compressed four-hour spacing. Nothing in the repo authorises it; the schedule
was pushed straight to Upload-Post and never committed (last commit is Aug 2).

**This has happened before, on the same causal shape.** On 2026-07-22 five
simultaneous posts were followed the next day by TikTok reach falling 409 → 40 →
33, and by the Instagram restriction that is still unresolved. The
reconciliation doc concluded the collapse follows the cadence violation by about
one day. Aug 3 is the same pattern with a one-post-per-day increment instead of
a five-post burst.

**b. The first dead post is a repost.**

| | Aug 2 08:02 | Aug 3 08:02 |
|---|---|---|
| Title | You're not overeating. You're under-counting. | You are not overeating, you are under-counting |
| Views | 263 | **4** |

Same claim, same three examples (cooking oil, the last third of a plate, bites
while plating), same hashtag set, same slot, 24 hours apart. The image was
re-rendered rather than re-uploaded byte-for-byte, but it is the same post.

This is not isolated. The Chick-fil-A Egg White Grill vs Hash Brown Scramble
Burrito comparison has run on TikTok **three times in six days** (Jul 28, Jul 31,
Aug 2) with a verbatim-identical closing sentence. The salmon / crab cake / 485
cal asset has run twice already and is **queued four more times** through Aug 9.
TikTok deprioritises duplicate and re-uploaded content, and a high-volume,
1-follower, API-posted account recycling assets is close to a textbook spam
signature.

**c. Volume across the account roughly doubled.** `video_count` went 23 → 47 in
about a week. Pinterest was also added and now interleaves with TikTok every two
hours, taking total output to ~8 posts/day. Pinterest appears nowhere in
`CLAUDE.md`'s platform set.

**What I can't confirm from here.** TikTok exposes no ban or restriction flag
through the Upload-Post API, so "the account is suppressed" remains the leading
hypothesis, not a finding. Publishing itself still succeeds — the posts exist at
real URLs and return real IDs. The distinguishing check is in the TikTok app:
**Profile → Settings and privacy → Account → Account status**, which reports
violations and unsearchable status directly.

**What is ruled out.** Content quality. A quality change produces gradual
spread, not 274 → 4 between consecutive posts. And the pre-collapse baseline was
suspiciously uniform (258, 263, 265, 268, 274, 278, 307) — that tight a cluster
is an allocation, not an audience.

---

## 4. What is not working, independent of the drop

Ranked by the metric ladder, the drop is the second story.

- **Installs: unknown.** `Analytics/installs.jsonl` does not exist. Nothing has
  ever been recorded. The top rung of the ladder is empty, which means no post
  in this project has ever been evaluated against the thing it exists to do.
- **Comments: 0.** Across 47 videos and ~3,800 lifetime views. Not low — zero.
- **Followers: 1.** After a week of 3/day posting. `following` also went 7 → 0.
- **Likes: 82 lifetime**, about 1.25% of views on the healthy Aug 1–2 posts
  (26 likes / 2,072 views). Below the ~1.49% the *old* system managed in July.

So the honest read: reach was being handed out for free and converted at
approximately nothing. The Aug 3 collapse took away a number that was not
turning into users.

---

## 5. What I would change

Ordered by urgency. Nothing here is executed — this skill is read-only, and
changes to what publishes belong to `weekly-loop`.

1. **Stop the queue before 08:00 today.** 24 TikTok posts are scheduled at the
   4/day cadence through Aug 9; the next fires at 08:00 America/Chicago. Cancel
   them and re-queue at most 1/day while the account is suspect. Continuing to
   post into a suppressed account at a violating cadence is the one action that
   can still make this worse.
2. **Have Connor check TikTok account status in the app** (path above). This is
   the only way to separate "suppressed" from "something else," it takes a
   minute, and every other decision depends on the answer. If a violation is
   listed, appeal in-app; that is also the only route, as with the Instagram
   restriction from Jul 22 that only Connor can clear.
3. **Deduplicate the queue before anything re-publishes.** The salmon/485 asset
   is queued four more times and the "consistency beats precision" message
   twice. One asset, one post, permanently — enforced in
   `Content-Engine/registry.jsonl`, which already exists for exactly this and is
   evidently not gating the scheduler.
4. **Put the 3/day ceiling somewhere that can actually stop a post.** It is
   documented in `CLAUDE.md` and was violated anyway by a scheduling run that
   never touched the repo. A rule that lives only in prose has now failed twice
   (Jul 22, Aug 3). It belongs as a check in whatever calls Upload-Post.
5. **Create `Analytics/installs.jsonl` and put a real number in it this week**,
   even hand-copied from App Store Connect. Rule 1 in `CLAUDE.md` says
   measurement is not a later phase, and the top of the ladder has been empty
   for the entire life of the project.

**What I would not do yet:** re-cut creative, change hooks, or kill a series.
With four post-platform rows since the break and zero comments to read, there is
no content signal here to act on. Fix distribution first, then judge content
against a clean window.
