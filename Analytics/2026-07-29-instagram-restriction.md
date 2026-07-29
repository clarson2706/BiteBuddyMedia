# Instagram is linked but account-restricted by Instagram — 2026-07-29

*Written after Connor reported Instagram was connected and asked to ease back
into posting at a 2/day cap. The connection is real; the account is not
publishable. Posting was stopped, not started.*

## What was tested

One carousel published to Instagram only, via the Upload-Post SDK:
"5 things people forget to log" (`Posts/2026-W30/2026-07-25-slot2`, 8 slides,
1080x1350). One post, deliberately, as a connection test before any queue.

- `request_id` `bd6ea5e89e0845fab0650f2fb05f114d`
- `job_id` `d316ded30a09436abdbd8e8e77345eee`
- submitted 2026-07-29 14:24 Chicago, terminal 23 seconds later

## Result: hard failure, account level

```
success: false
error_code: account_restricted
failure_stage: platform_api
error_message: "Action suspected as spam. Activity is restricted. If this is a
  mistake, please review your account... Please log in to Instagram directly and
  resolve any account issues or verification prompts."
```

`post_caption` came back fully populated, so the 2026-07-25 caption trap did
**not** recur. The request was well-formed. Instagram refused the action.

## What this proves, and what it corrects

**The OAuth link is healthy.** `list_users` shows `instagram: bitebuddy_app,
reauth_required: false`, and Upload-Post reached Instagram's API and received a
policy response, not an auth error. "Instagram is connected" is true.

**The account is restricted at Instagram's end.** This is not a throttle, a
shadowban theory, or a reach problem. It is an explicit spam restriction that
blocks the publish action outright.

**Every prior Instagram post silently failed the same way.** All four
`2026-W30` posts carry Instagram `request_id`s in their manifest, and all four
return `{"post": {}, "platforms": {}}` from `get_post_analytics` — empty, not
zero. Nothing this project has ever sent to Instagram has published. The
account's 58 lifetime views, 1 follower and 3 likes predate the pipeline; the
4 comments are ours.

This corrects two earlier readings:
- The 2026-07-25 media report said "our first Instagram post publishes at
  12:30." It did not publish, then or since.
- The 2026-07-29 growth report called Instagram "dark, link state unverified."
  Link state is now verified: **linked, and restricted.**

The reach timeseries fits: 1, 2, 1, 1 on Jul 22 to 25, then flat zero from Jul
26 to today. The suspected trigger remains the five simultaneous posts on
2026-07-22 (`CLAUDE.md` cadence guardrail).

## Why posting was NOT eased back in

Connor authorized a 2/day ramp. It was not started, and the queue was not
written, because **repeated blocked publish attempts are how a temporary
restriction becomes a permanent one.** An account flagged for spam that keeps
firing API publish calls is confirming the flag. One diagnostic attempt was
worth it; a scheduled queue against a restricted account is not.

No Instagram posts are scheduled (`list_scheduled` shows 18 jobs, all TikTok or
YouTube), so nothing will retry automatically. The failure is inert.

## What has to happen next, and only Connor can do it

1. **Open the Instagram app or instagram.com as `bitebuddy_app` and resolve the
   prompt.** A spam restriction almost always surfaces an in-app "we restricted
   some of your activity" notice with a review or verification step. It cannot
   be cleared through any API.
2. **Check for a restriction end date.** Instagram usually names one. That date
   is when posting can resume, not before.
3. **Let the account sit quiet until then.** No API publish attempts.
4. **When it clears, resume at 1/day for the first three days**, not 2 — then
   2/day. The 2/day cap Connor set is the right ceiling; the ramp to it should
   start lower given the account is coming off a restriction.
5. Re-run this exact one-post test before rebuilding any queue. If it returns
   `success: true` with a `post_url`, Instagram is genuinely back.

Until step 1 happens, Instagram stays out of the weekly loop's platform list.
TikTok and YouTube are unaffected and continue on schedule.
