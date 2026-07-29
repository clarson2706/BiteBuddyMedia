# Publishing via Upload-Post (API key, not a connector)

*Written 2026-07-25 after verifying that Upload-Post is not available as a claude.ai
connector. This is the publishing transport for the weekly loop.*

## Why not the MCP connector

Upload-Post is not in the claude.ai connector directory (verified: the org has Base44,
Canva, Github, Google Drive, Higgsfield, Notion, RevenueCat, Stripe, Supabase, Vercel,
Zapier and nothing else). A locally added developer MCP server lives only on the
machine that added it, so it never reaches claude.ai Routines or this remote
environment.

**Using the REST API instead is strictly better for a scheduled system:**
no OAuth to expire, no connector grants to inherit, works identically in every fired
Routine session, and it exposes scheduling and analytics directly.

## Setup (one time, Connor)

1. Get the API key from the Upload-Post dashboard.
2. Add it to **this CCR environment's environment variables** as `UPLOAD_POST_API_KEY`
   (Claude Code on the web → environment settings). Every Routine-fired session in
   this environment then has it, with no connector attached.
3. Never commit the key. It lives in the environment only; the loop reads
   `os.environ["UPLOAD_POST_API_KEY"]`.

## Auth

Every request carries:

```
Authorization: Apikey <UPLOAD_POST_API_KEY>
```

## What the loop uses

Prefer the official SDK (`pip install upload-post`), which wraps the endpoints and
saves us from hardcoding paths:

```python
from upload_post import UploadPostClient
client = UploadPostClient(os.environ["UPLOAD_POST_API_KEY"])
```

| Need | SDK method | Key parameters |
|---|---|---|
| Preflight: which platforms are linked | `client.list_users()` | returns profiles with a `social_accounts` object; `null` = not linked |
| Publish a carousel | `client.upload_photos(...)` | `user`, `platforms`, photos, `title`, `scheduled_date`, `timezone`, `first_comment`, `facebook_page_id`, `media_type` |
| Publish a YouTube Short | `client.upload_video(...)` | `user`, `platforms`, video, `title`, `scheduled_date`, `timezone`, `first_comment`, `privacy_level` |
| Weekly analytics pull | `client.get_analytics(profile, platforms=[...])` | per-profile, multiple platforms in one call |
| Reconcile what actually posted | `client.get_history(page=1, limit=20)` | pagination |
| Job status | `client.get_status(...)` | for scheduled/async jobs |

Confirmed raw equivalent for carousels, if the SDK is ever unavailable:

```
POST https://api.upload-post.com/api/upload_photos
Authorization: Apikey <key>
```

## Scheduling: the whole week in one pass

`scheduled_date` takes an ISO-8601 datetime and supports up to 365 days ahead, with
`timezone` as an IANA name (`America/Chicago`). A scheduled request returns **202
Accepted** with a `job_id` that later appears in upload history, which is how we
reconcile "scheduled" against "actually published."

This means Phase 4 submits all of next week's posts in one run and does not need any
process to stay alive during the week.

## Two traps that cost us a live post on 2026-07-25

**1. `upload_photos` takes `description`, not `caption`.** `caption` is not a
recognised keyword. It lands in `**kwargs`, is silently dropped, and the post
publishes with only its `title`. There is no error and `success: true` comes back
normally. The only way to catch it is that the response and `get_post_analytics`
both show `post_caption: ""`. **Always check `post_caption` after publishing a
carousel.**

**2. TikTok does not support comments through this API at all.** `create_comment`
on TikTok returns `Comments are not supported on TikTok via the API`, and
`first_comment` is therefore a **no-op on TikTok** even though the parameter is
accepted without complaint.

This one is worse than it sounds. Every TikTok post this project has ever made was
submitted with a `first_comment`, and none of them ever got one. The proof is in
the numbers: the 2026-07-25 08:00 post reached 260 views with **0 comments**, and
our own pinned comment would have counted as 1. The comment-seeding mechanism that
`SERIES.md` and the weekly loop depend on has never once fired on our
highest-reach platform.

**So on TikTok the pinned comment is a manual step for Connor**, or it does not
happen. `first_comment` still works on the platforms that support it. Do not
report a pinned comment as "fired" on TikTok without a comment count to prove it.

Also note: `unpublish_post` covers facebook, youtube, x, linkedin and threads.
**TikTok is not in that list**, so a bad TikTok post cannot be deleted through the
API. Getting a TikTok post right the first time is the only option available.

## A third trap, found 2026-07-29: on Instagram, `success: false` can still mean published

Upload-Post reported a carousel as failed with
`error_code: account_restricted` ("Action suspected as spam"),
`platform_post_id: null` and `post_url: null`. **The post was live on the
Instagram profile anyway**, and Connor got no verification prompt of the kind
Instagram shows for a real account restriction. Minutes later the profile's
Instagram link emptied to `instagram: ""`, so the likeliest mechanic is that the
media published and then a follow-up call or the token itself failed, with the
whole request attributed to failure.

Two rules follow, and they cut in opposite directions from the obvious reading:

- **A failure record is not proof of absence.** Before writing "did not post,"
  look at the profile. This applies with force to the four `2026-W30` Instagram
  jobs, whose empty analytics were once read as "never published"; that claim is
  unproven either way.
- **An empty `get_post_analytics` object is not "zero engagement."** It means
  Upload-Post has no `platform_post_id` to query with. The post may exist and be
  earning reach that this pipeline cannot see. Never average an empty result into
  a total, and never write `status: scheduled` into a manifest as proof of
  delivery.

Practical consequence: **a post published this way is permanently unmeasurable
through `request_id`.** Instagram reach has to come from a native export, the same
rule `Analytics/README.md` already applies to TikTok.

Still poll `get_status` to a terminal state and record `success` per platform —
just treat an Instagram `false` as "verify against the profile," not as settled.
See `Analytics/2026-07-29-instagram-restriction.md`.

## Scheduling notes

**`first_comment` is native** on the platforms that support comments, so the pinned
line is submitted with the post rather than needing a second manual step. See the
TikTok exception above.

## Rules the loop must still enforce itself

The API will happily post whatever we tell it to, so our safety rules stay in our code:

- TikTok ≤3/day · Instagram ≤2/day
- ≥4h spacing between same-platform posts; never two platforms at the same minute
- Vary captions and crops per platform (duplicate-content penalty)
- Skip any platform whose `social_accounts` entry is `null` and report it rather than
  guessing
- Check plan headroom before submitting ~40 posts (free tier is 10 uploads/month)

## Media delivery

Canva export URLs can be handed to Upload-Post directly; its servers fetch the media,
which sidesteps this environment's block on `export-download.canva.com` (see
`TEMPLATES.md`). Do not try to download exports locally first.

## Degradation

If `UPLOAD_POST_API_KEY` is missing or the API rejects auth, the loop still runs
analytics, generation, and render, commits everything as `staged`, publishes nothing,
and reports exactly what is needed. It never fails silently.

## Sources

- [Upload-Post API docs](https://docs.upload-post.com/landing/) ·
  [API reference](https://docs.upload-post.com/api/reference/) ·
  [Analytics API](https://docs.upload-post.com/api/get-analytics/) ·
  [User Profiles API](https://docs.upload-post.com/api/user-profiles/)
- [Official Python SDK](https://github.com/upload-post/upload-post-pip) ·
  [PyPI](https://pypi.org/project/upload-post/)
- [Scheduling guide](https://www.upload-post.com/how-to/schedule-social-media-posts-api/)
