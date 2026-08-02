# 2026-W31 weekly report (Jul 27 to Aug 2)

*Phase 1 of the Sunday run, 2026-08-02. Sources: TikTok Studio export (ground truth for
daily series through Aug 1), Upload-Post account aggregates, RevenueCat. Per-post rows
remain unavailable, so every content-level statement below is inference from
account-level movement and is labelled as such.*

## What went well

**TikTok reach recovered and kept climbing.** The Jul 22 throttle bottomed at 40 and 33
views on Jul 23 and 24. The account then ran 553, 358, 245, 532, 717, 1076, 1213, 744
through Aug 1, and Upload-Post shows 821 more on Aug 2. That is roughly 6,900 views across
twelve days against a 895-view lifetime total as of Jul 25. Views per day are up about 5x
week over week.

**Likes scaled with reach and slightly faster.** 25 likes on Jul 31 against 2 to 3 per day
the previous week. Like rate over the last five logged days is 1.56%, which is a normal
band, so the content is not repelling the people it reaches.

**The back catalogue is compounding unattended.** Nothing new was scheduled after ~Jul 26,
yet daily views kept rising for six more days. Thirty-eight videos are live. Inference,
not proof: TikTok is re-serving existing posts. If correct it is the single most
encouraging fact in this report, because it means distribution compounds without new
volume.

## What did not go well

**Zero comments and zero shares. Every day, both platforms, all year.** Not low. Zero. On
~6,900 TikTok views and 709 YouTube views.

**Zero profile views on TikTok per Upload-Post; 13 across the whole export window.** That
is 0.2% of viewers taking one step toward the account.

**The install line barely moved.** RevenueCat: 50 to 53 new customers over the eight days,
MRR flat at $7, 1 subscriber, 1 trial. Roughly 5,400 views produced about 3 installs, and
that is an upper bound because it credits TikTok with every one of them.

**YouTube is dying.** 0 views on Aug 1 and 0 on Aug 2, after averaging ~30/day the week
before. 5 subscribers, 5 lifetime likes, 0 comments.

**The loop did not run.** No Sunday or Wednesday run left a commit. Per `CLAUDE.md` the
Routines were only confirmed enabled Jul 30, so W31 produced no new content at all. The
reach above came from posts published on or before Jul 26.

**The creator engine produced nothing.** 20 DMs written on Jul 25, all still
`status: dm_written`. Zero sent, zero replies, zero deals, zero creator posts,
`payouts.jsonl` empty. The daily DM Routine has been paused since Jul 25.

**Instagram and Facebook are not linked in Upload-Post at all.** Instagram returns an
empty string from `list_users`, so this is not only the spam restriction: there is no
account connected to publish to. Every Instagram plan in the repo is currently inert.

## Sprint checkpoint

W32 (Aug 3) wanted 100 DMs, 6+ cumulative deals, 4+ cumulative creator posts live,
installs/day above 10, and $75 MRR. Actual: 20 DMs written and 0 sent, 0 deals, 0 creator
posts, ~0.4 installs/day, $7 MRR. **That is two consecutive missed checkpoints** (W31
wanted $25), which under the sprint's own rule obliges this report to name the broken
lever rather than restate the plan.

**The broken lever is creator outreach, and it is broken because it is switched off, not
because it failed.** It has never been tested. The organic lever is, unexpectedly, the one
that is working: it produces reach. What it does not produce is action, which is a
different and more fixable problem than "nobody sees us."

## What changes next week

1. **Treat the ask as the failure point, not the hook.** ~6,900 views produced 0 comments
   and 0 shares. A post that takes 1,000 views and produces no comment has not failed at
   attention. Comment-first CTAs on the majority of the week, per the CTA ladder in
   `Content-Engine/CAROUSEL-CONVERSION-SPEC.md` §3.
2. **Cadence to 4 TikTok posts/day** (Connor's call, 2026-08-02). Spacing is what the Jul
   22 incident actually punished, so the four slots are spread 08:00 / 12:00 / 16:00 /
   20:00 with four clear hours between each. This is a deliberate change to the 3/day
   ceiling in `CLAUDE.md`; the risk is stated in the report to Connor.
3. **Five rotating layout templates instead of three**, so a 4/day cadence does not make
   the grid look stamped. TikTok's July 2026 crackdown targets exactly our profile.
4. **Video into the rotation.** Three brand films go into the week's 20:00 slots. They are
   stylistically unlike anything the account has posted and are the cleanest test of
   whether production value moves the needle that reach alone has not.
5. **YouTube keeps its daily Short but stops being a priority.** 0 views two days running
   with 5 subscribers is not a channel yet. It costs nothing to keep feeding.
6. **Unlink-blocked platforms are named, not planned around.** No Instagram or Facebook
   content is generated this week. When Connor relinks Instagram the loop picks it back
   up.

## Tables

Per-series, per-persona, per-hook-family and per-slot tables are **not produced this
week**. Upload-Post exposes no per-post rows for this account, and the TikTok export is
account-level only, so any such table would be fabricated attribution. The first week that
per-post data exists, these return. This absence is itself the strongest argument for
`Analytics/installs.jsonl`: without it nothing here can connect a post to a dollar.

| Account | Followers | Views (window) | Likes | Comments | Shares |
|---|---|---|---|---|---|
| TikTok | 1 | ~6,900 | 75 | 0 | 0 |
| YouTube | 5 | 709 | 5 | 0 | 0 |
| Instagram | not linked | n/a | n/a | n/a | n/a |
| Facebook | not linked | n/a | n/a | n/a | n/a |

| RevenueCat | Jul 25 | Aug 2 |
|---|---|---|
| MRR | $7 | $7 |
| Active subscriptions | 1 | 1 |
| Active trials | 0 | 1 |
| New customers (28d) | 50 | 53 |
