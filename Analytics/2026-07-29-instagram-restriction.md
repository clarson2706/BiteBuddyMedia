# Instagram: the post published, Upload-Post recorded it as failed, then the
# connection dropped — 2026-07-29

*Written after a live test, then **substantially corrected the same hour** when
Connor checked the actual Instagram account. The first version of this file
concluded the account was spam-restricted and that no Instagram post had ever
published. Connor's direct observation contradicts both claims. What follows is
the corrected account; the original conclusion is preserved at the bottom so the
error is legible.*

## Timeline (all UTC, 2026-07-29)

| Time | Event | Evidence |
|---|---|---|
| ~19:20 | Instagram fully linked | `list_users` → `instagram: {handle: bitebuddy_app, reauth_required: false}` |
| ~19:21 | Instagram analytics healthy | `get_analytics` → 58 views, 1 follower, reach timeseries |
| 19:24 | One carousel published (`2026-07-25-slot2`, 8 slides) | `request_id bd6ea5e89e0845fab0650f2fb05f114d` |
| 19:24:47 | Upload-Post records **failure** | `success: false`, `error_code: account_restricted`, `platform_post_id: null`, `post_url: null` |
| ~19:45 | **Connor sees the post live on the Instagram account**, and reports **no verification prompt anywhere** | direct observation |
| ~19:50 | Instagram analytics now errors | `get_analytics` → "Profile 'Business_Posts' has no Instagram account connected" |
| ~19:52 | Instagram **gone from the profile** | `list_users` → `instagram: ""` (TikTok and YouTube objects intact) |

## What this actually means

**The post published.** Connor can see it. Instagram accepted the carousel.

**Upload-Post's failure record is wrong, or at best describes a secondary step.**
It returned "Action suspected as spam. Activity is restricted" with a null
`platform_post_id` for a post that exists. The plausible mechanic: Instagram
published the media container, then a follow-up call (permalink read-back, or
the token itself) hit a restriction or expiry, and Upload-Post attributed the
whole request to failure. The absence of any verification prompt on Connor's
side is strong evidence there is **no account-level spam restriction** — that
notice is exactly what Instagram surfaces when there is one.

**The connection then dropped.** `instagram: ""` is not a throttle and not a
ban; it is a missing/revoked token. The likeliest cause is that the Instagram
or Facebook session backing the link expired or was invalidated around the
publish. This is a reconnect problem, not a policy problem.

**Two consequences that matter more than the error string:**

1. **This post is invisible to our analytics.** With `platform_post_id: null`
   and `post_url: null`, `get_post_analytics(request_id)` will never return
   metrics for it. It is live on Instagram and unmeasurable through the
   pipeline. Any reach it earns has to be read from Instagram natively.
2. **The historical claim needs re-testing, not asserting.** All four
   `2026-W30` Instagram `request_id`s return empty analytics objects. The old
   reading was "they never published." The unified explanation that now fits
   better is that **Upload-Post fails to record Instagram posts even when they
   publish** — the same thing that just happened. Whether those four are live
   on the profile is a question only a look at the account answers. Until
   somebody looks, neither "they published" nor "they didn't" is established.

## Open question for Connor (one look settles it)

Scroll the `bitebuddy_app` profile grid. Are the four posts from **July 25 and
26** there — "You didn't quit tracking because you're lazy," "5 things people
forget to log," "POV: the app made you feel worse than the food did," "Most
people think they eat the same every day"?

- **If yes:** Instagram has been publishing all along and our analytics have
  been blind to it. The 7/25 media report and the 7/29 growth report both
  understate Instagram, and the pipeline needs a native-export path for IG the
  way TikTok already has one.
- **If no:** those four genuinely failed, and today's post is the first
  Instagram post this project has landed.

## What to do next

1. **Reconnect Instagram in the Upload-Post dashboard.** The link is empty
   (`instagram: ""`), so nothing can post or be measured until it is re-added.
   Confirm it comes back as a Business/Creator account with the Facebook Page
   still attached.
2. **Do not re-run the earlier failing behaviour blindly.** After reconnecting,
   send exactly one post and poll `get_status` to terminal. If it again returns
   `account_restricted` while the post appears on the profile, the failure
   record is a known Upload-Post defect for this account and we stop trusting
   `success: false` on Instagram alone.
3. **Ramp as Connor set it: 2/day ceiling.** Given the account is coming off a
   suspected July 22 throttle, start at 1/day for the first three days, then 2.
   Spaced, never simultaneous. `CLAUDE.md` cadence rules unchanged.
4. **Treat Instagram reach as native-export-only for now** — the same rule
   `Analytics/README.md` already applies to TikTok, and for the same reason:
   where the platform's own numbers and Upload-Post disagree, the platform wins.

## The original conclusion, preserved (it was wrong)

The first version of this file said: *"The account is restricted at Instagram's
end... Nothing this project has ever sent to Instagram has published... posting
was stopped, not started."* It was written from the API response alone, before
anyone looked at the account. Two of its three claims did not survive contact
with the actual profile. The decision it drove — stop, do not schedule a queue —
was still the right call at the time, because the alternative was firing a
multi-day queue at what looked like a spam-flagged account. The lesson is
narrower and worth keeping: **an Upload-Post `success: false` on Instagram is
not proof a post is absent, and an empty analytics object is not proof of zero
engagement. Look at the profile.**
