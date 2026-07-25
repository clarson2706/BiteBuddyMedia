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

**`first_comment` is native**, so our pinned first comment (the swipe-bait line) is
submitted with the post rather than needing a second manual step.

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
