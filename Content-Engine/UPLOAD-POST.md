# Publishing via Upload-Post (API key, not a connector)

*Written 2026-07-25 after verifying that Upload-Post is not available as a claude.ai
connector. This is the publishing transport for the weekly loop.*

## REST API, and also an MCP tool set

**Corrected 2026-08-01.** This file used to state flatly that Upload-Post "is not in
the claude.ai connector directory" and cannot reach a Routine session. That is no
longer true: an **Upload-Post MCP tool set is available in-session**
(`list_users`, `list_scheduled`, `get_analytics`, `upload_photos`, and the rest), and
it was used to verify every live number in this repo's 2026-08-01 audit.

**The REST API remains the transport the loop should schedule through**, for the
original reasons and they still hold: no OAuth to expire, no connector grant to
inherit, identical behaviour in every fired Routine session, and it works from a plain
`requests` call in a script (`preflight.py` uses exactly that). Use the MCP tools for
interactive inspection; use the REST API for anything a Routine depends on.

Do not write new code that assumes the MCP tools are absent, and do not write code that
assumes they are present either. The key is the dependable path.

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

## Three traps on TikTok, the platform that matters most

**3. TikTok photo posts cannot carry a sound through this API** (added 2026-08-01).
Music is a video-only field in TikTok's Content Posting API; photo posts use a
different content model that has no music parameter. Upload-Post cannot work around it.

So **every carousel this system has ever published to TikTok went out silent**, while
sound is a genuine distribution lever on Photo Mode and TikTok's own composer requires
one when you post by hand. This is not a bug to fix, it is a constraint to design
around, and it has three consequences worth acting on:

- Slide 1 carries the entire hook. There is no audio to help it.
- **Demo videos are the only format in this system that gets audio distribution at
  all**, because the video path does accept a sound. That is an argument for running
  more of them, independent of how they score on saves.
- The single highest-value post of a week is worth Connor posting by hand in the app,
  with a sound picked there. Everything else stays automated.

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
